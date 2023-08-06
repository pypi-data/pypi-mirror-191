import abc

from .data import DataObject, SameMimeType
from .aws import S3StorageClassMixin, s3_uri, S3_URI_PATTERN, S3_URI_BUCKET_PATTERN
from .awss3bucketobjectkey import is_folder, KeyDecodeException, encode_key, decode_key
from heaobject.root import desktop_object_type_for_name
from heaobject.data import AWSS3FileObject
from heaobject.bucket import AWSBucket
from typing import Optional
from humanize import naturalsize


class Folder(DataObject, SameMimeType):
    """
    Represents a directory in the HEA desktop.
    """
    def __init__(self):
        super().__init__()

    @classmethod
    def get_mime_type(cls) -> str:
        """
        Returns the mime type of instances of the Folder class.

        :return: application/x.folder
        """
        return 'application/x.folder'

    @property
    def mime_type(self) -> str:
        """
        Read-only. Always returns 'application/x.folder'.
        """
        return type(self).get_mime_type()


class AWSS3Folder(Folder, S3StorageClassMixin):
    """
    Represents folders stored in AWS S3.
    """

    @property
    def id(self) -> Optional[str]:
        key_ = self.key
        return encode_key(key_) if key_ else None

    @id.setter
    def id(self, id: Optional[str]):
        try:
            self.key = decode_key(id) if id is not None else None
        except KeyDecodeException as e:
            raise ValueError(f'Invalid id {id}') from e

    @property
    def name(self) -> Optional[str]:
        key_ = self.key
        return encode_key(key_) if key_ else None

    @name.setter
    def name(self, name: Optional[str]):
        try:
            self.key = decode_key(name) if name is not None else None
        except KeyDecodeException as e:
            raise ValueError(f'Invalid name {name}') from e

    @property
    def key(self) -> Optional[str]:
        """
        The object's key.
        """
        try:
            return self.__key
        except AttributeError:
            self.__key: str | None = None
            return self.__key

    @key.setter
    def key(self, key: Optional[str]):
        if key:
            self.__key = key
            if self.__key is not None and is_folder(self.__key):
                key_: str | None = self.__key.strip('/')
            else:
                key_ = self.__key
            print(key_)
            if key_ is not None:
                self.__display_name: str | None = key_.rsplit('/', maxsplit=1)[-1]
            else:
                self.__display_name = None
        else:
            self.__display_name = None

    @property
    def display_name(self) -> str:
        """
        The object's display name. It's the last part of the object's key, minus the trailing slash.
        """
        try:
            result = self.__display_name
        except AttributeError:
            self.__display_name = None
            result = self.__display_name
        return result if result is not None else super().display_name  # type: ignore

    @display_name.setter
    def display_name(self, display_name: str):
        if display_name is not None:
            if '/' in display_name:
                raise ValueError(f'display_name {display_name} cannot contain slashes')
            try:
                key = self.__key
            except AttributeError:
                key = None
            if key is not None:
                key_rsplit = key.rsplit('/', 1)
                if len(key_rsplit) > 1:
                    key = key_rsplit[-2] + f'/{display_name}' if len(key_rsplit) > 1 else display_name
                else:
                    key = f'{display_name}/'
            else:
                key = f'{display_name}/'
            self.key = key

    @property
    def s3_uri(self) -> Optional[str]:
        """
        The object's S3 URI, computed from the bucket id and the id field.
        """
        return s3_uri(self.bucket_id, self.key)

    @s3_uri.setter
    def s3_uri(self, s3_uri: Optional[str]):
        """
        The object's S3 URI, computed from the bucket id and the id field.
        """
        if s3_uri is not None and not s3_uri.startswith('s3://'):
            raise ValueError(f'Invalid s3 URI {s3_uri}')
        match = S3_URI_PATTERN.fullmatch(s3_uri) if s3_uri else None
        if match:
            bucket_and_key = match.groupdict()
            self.bucket_id = bucket_and_key['bucket']
            self.key = bucket_and_key['key']
        elif s3_uri is not None:
            raise ValueError(f'Invalid s3 URI {s3_uri}')
        else:
            self.bucket_id = None
            self.key = None

    @property
    def bucket_id(self) -> Optional[str]:
        """
        The object's bucket name.
        """
        try:
            return self.__bucket_id
        except AttributeError:
            self.__bucket_id: str | None = None
            return self.__bucket_id

    @bucket_id.setter
    def bucket_id(self, bucket_id: Optional[str]):
        self.__bucket_id = bucket_id

    @property
    def presigned_url(self) -> Optional[str]:
        """
        The object's presigned url.
        """
        try:
            return self.__presigned_url
        except AttributeError:
            return None

    @presigned_url.setter
    def presigned_url(self, presigned_url: Optional[str]):
        presigned_url_ = str(presigned_url) if presigned_url is not None else None
        if presigned_url_ is not None and not presigned_url_.startswith('https://'):
            raise ValueError(f'Invalid presigned URL {presigned_url_}')
        self.__presigned_url = presigned_url_


class Item(DataObject):
    """
    Represents an item in a folder. Items contain the actual object being pointed to as a nested
    """
    def __init__(self):
        super().__init__()
        self.__actual_object_type_name: Optional[str] = None
        self.__actual_object_id: Optional[str] = None
        self.__actual_object_uri: Optional[str] = None
        self.__folder_id: Optional[str] = None
        self.__volume_id: Optional[str] = None
        self.__size: Optional[int] = None

    @property
    def mime_type(self) -> str:
        """
        Read-only. Always returns 'application/x.item'.
        """
        return 'application/x.item'

    @property
    def actual_object_type_name(self) -> Optional[str]:
        """
        The name of the type of the actual HEAObject.
        """
        return self.__actual_object_type_name

    @actual_object_type_name.setter
    def actual_object_type_name(self, actual_object_type_name: Optional[str]) -> None:
        self.__actual_object_type_name = str(actual_object_type_name) if actual_object_type_name is not None else None

    @property
    def actual_object_id(self) -> Optional[str]:
        """
        The id of the actual HEAObject.
        """
        return self.__actual_object_id

    @actual_object_id.setter
    def actual_object_id(self, actual_object_id: Optional[str]) -> None:
        self.__actual_object_id = str(actual_object_id) if actual_object_id is not None else None

    @property
    def actual_object_uri(self) -> Optional[str]:
        """
        The actual HEAObject's URI.
        """
        return self.__actual_object_uri

    @actual_object_uri.setter
    def actual_object_uri(self, actual_object_uri: Optional[str]) -> None:
        self.__actual_object_uri = str(actual_object_uri) if actual_object_uri is not None else None

    @property
    def folder_id(self) -> Optional[str]:
        """
        The id of this item's folder.
        """
        return self.__folder_id

    @folder_id.setter
    def folder_id(self, folder_id: Optional[str]) -> None:
        self.__folder_id = str(folder_id) if folder_id is not None else None

    @property
    def volume_id(self) -> Optional[str]:
        """
        The id of this item's volume.
        """
        return self.__volume_id

    @volume_id.setter
    def volume_id(self, volume_id: Optional[str]) -> None:
        self.__volume_id = str(volume_id) if volume_id is not None else None

    @property
    def size(self) -> Optional[int]:
        """Size of the item in bytes"""
        return self.__size

    @size.setter
    def size(self, size: Optional[int]) -> None:
        self.__size = int(size) if size is not None else None

    @property
    def human_readable_size(self) -> str | None:
        return naturalsize(self.size) if self.size else None


class AWSS3Item(Item, S3StorageClassMixin, abc.ABC):
    @property
    @abc.abstractmethod
    def s3_uri(self) -> str | None:
        pass


    @s3_uri.setter
    @abc.abstractmethod
    def s3_uri(self, s3_uri: str | None):
        pass

    @property
    def bucket_id(self) -> Optional[str]:
        """
        The object's bucket name.
        """
        try:
            return self.__bucket_id
        except AttributeError:
            self.__bucket_id: str | None = None
            return self.__bucket_id

    @bucket_id.setter
    def bucket_id(self, bucket_id: Optional[str]):
        self.__bucket_id = bucket_id



class AWSS3BucketItem(AWSS3Item):
    @property
    def id(self) -> Optional[str]:
        return self.bucket_id

    @id.setter
    def id(self, id: Optional[str]):
        self.bucket_id = id

    @property
    def name(self) -> Optional[str]:
        return self.bucket_id

    @name.setter
    def name(self, name: Optional[str]):
        self.bucket_id = name

    @property
    def display_name(self) -> str:
        return self.bucket_id

    @display_name.setter
    def display_name(self, display_name: str):
        self.bucket_id = display_name

    @property
    def s3_uri(self) -> Optional[str]:
        """
        The object's S3 URI, computed from the bucket id field or set with this property.
        """
        return s3_uri(self.bucket_id)

    @s3_uri.setter
    def s3_uri(self, s3_uri: Optional[str]):
        match = S3_URI_BUCKET_PATTERN.fullmatch(s3_uri) if s3_uri else None
        if match:
            bucket_and_key = match.groupdict()
            self.bucket_id = bucket_and_key['bucket']
        elif s3_uri is not None:
            raise ValueError(f'Invalid s3 bucket URI {s3_uri}')
        else:
            self.bucket_id = None

    @property
    def actual_object_type_name(self) -> Optional[str]:
        try:
            return self.__actual_object_type_name
        except AttributeError:
            return None

    @actual_object_type_name.setter
    def actual_object_type_name(self, actual_object_type_name: Optional[str]):
        if actual_object_type_name:
            type_ = desktop_object_type_for_name(actual_object_type_name)
            if not issubclass(type_, AWSBucket):
                raise TypeError(f'Type must be {AWSBucket} but was {type_}')
            self.__actual_object_type_name = actual_object_type_name
        else:
            self.__actual_object_type_name = None


class AWSS3FolderFileItem(AWSS3Item):
    """
    Represents items stored in AWS S3.
    """

    @property
    def id(self) -> Optional[str]:
        key_ = self.key
        return encode_key(key_) if key_ else None

    @id.setter
    def id(self, id: Optional[str]):
        try:
            self.key = decode_key(id) if id is not None else None
        except KeyDecodeException as e:
            raise ValueError(f'Invalid id {id}') from e

    @property
    def name(self) -> Optional[str]:
        key_ = self.key
        return encode_key(key_) if key_ else None

    @name.setter
    def name(self, name: Optional[str]):
        try:
            self.key = decode_key(name) if name is not None else None
        except KeyDecodeException as e:
            raise ValueError(f'Invalid name {name}') from e

    @property
    def key(self) -> Optional[str]:
        """
        The object's key.
        """
        try:
            return self.__key
        except AttributeError:
            self.__key: str | None = None
            return self.__key

    @key.setter
    def key(self, key: Optional[str]):
        if key:
            self.__key = key
            if self.__key is not None and is_folder(self.__key):
                key_: str | None = self.__key.strip('/')
            else:
                key_ = self.__key
            if key_ is not None:
                self.__display_name: str | None = key_.rsplit('/', maxsplit=1)[-1]
            else:
                self.__display_name = None
        else:
            self.__display_name = None

    @property
    def display_name(self) -> str:
        """
        The object's display name. It's the last part of the object's key, minus any trailing slash for folders.
        Setting this property will make this item a file.
        """
        try:
            result = self.__display_name
        except AttributeError:
            self.__display_name = None
            result = self.__display_name
        return result if result is not None else super().display_name  # type: ignore

    @display_name.setter
    def display_name(self, display_name: str):
        if display_name is not None:
            if '/' in display_name:
                raise ValueError(f'display_name {display_name} cannot contain slashes')
            try:
                key = self.__key
            except AttributeError:
                key = None
            key_end_part = f'{display_name}/' if self.actual_object_type_name and issubclass(desktop_object_type_for_name(self.actual_object_type_name), AWSS3Folder) else f'{display_name}'
            if key is not None:
                key_rsplit = key.rsplit('/', 1)
                if len(key_rsplit) > 1:
                    key = key_rsplit[-2] + f'/{key_end_part}' if len(key_rsplit) > 1 else key_end_part
                else:
                    key = f'{key_end_part}'
            else:
                key = f'{key_end_part}'
            self.key = key


    @property
    def s3_uri(self) -> Optional[str]:
        """
        The object's S3 URI, computed from the bucket id and the id field.
        """
        return s3_uri(self.bucket_id, self.key)

    @s3_uri.setter
    def s3_uri(self, s3_uri: Optional[str]):
        """
        The object's S3 URI, computed from the bucket id and the id field.
        """
        match = S3_URI_PATTERN.fullmatch(s3_uri) if s3_uri else None
        if match:
            bucket_and_key = match.groupdict()
            self.bucket_id = bucket_and_key['bucket']
            self.key = bucket_and_key['key']
        elif s3_uri is not None:
            raise ValueError(f'Invalid s3 URI {s3_uri}')
        else:
            self.bucket_id = None
            self.key = None

    @property
    def actual_object_type_name(self) -> Optional[str]:
        try:
            return self.__actual_object_type_name
        except AttributeError:
            return None

    @actual_object_type_name.setter
    def actual_object_type_name(self, actual_object_type_name: Optional[str]):
        if actual_object_type_name:
            type_ = desktop_object_type_for_name(actual_object_type_name)
            if issubclass(type_, AWSS3Folder):
                key = self.key
                if key and not key.endswith('/'):
                    self.key = key + '/'
            elif issubclass(type_, AWSS3FileObject):
                key = self.key
                if key and key.endswith('/'):
                    self.key = key[:-1]
            else:
                raise TypeError(f'Type must be {AWSS3Folder} or {AWSS3FileObject} but was {type_}')
            self.__actual_object_type_name = actual_object_type_name
        else:
            key = self.key
            if key and key.endswith('/'):
                self.key = key[:-1]
            self.__actual_object_type_name = None

