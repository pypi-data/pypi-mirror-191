import os
import boto3
import botocore


class S3Object:
    """
    This class represents an object on Amazon's S3 storage
    """

    def __init__(self, bucket: str, prefix: str, filename: str):
        self._bucket = bucket
        self._prefix = prefix
        self._filename = filename
        self._s3 = boto3.resource('s3')

    @classmethod
    def upload_file(cls, file_path: str, bucket: str, prefix: str, filename="", override_object=False) -> "S3Object":
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: the specified path \"{file_path}\" does not contain a file!")
        if filename == "":
            filename = os.path.basename(file_path)
        new_object = cls(bucket, prefix, filename)
        if new_object.exists() and not override_object:
            raise FileExistsError(f"An object with the same key (\"{new_object.key()}\") already exists on the given bucket (\"{new_object._bucket}\")")
        try:
            new_object._s3.meta.client.upload_file(file_path, new_object._bucket, new_object.key())
        except botocore.exceptions.ClientError as e:
            raise ConnectionError(f"Failed to upload the file \"{file_path}\" to S3 and create object {new_object}! The following error was encountered: {e}")
        except Exception as e:
            raise RuntimeError(f"An error was encountered while uploading the file \"{file_path}\" to S3: {e}")
        return new_object

    @property
    def bucket(self) -> str:
        return self._bucket

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def filename(self) -> str:
        return self._filename

    def key(self) -> str:
        return self._prefix + self._filename

    def download(self, download_path: str, replace_file=False) -> None:
        if os.path.isdir(download_path):
            file_path = os.path.join(download_path, self._filename)
        else:
            file_path = download_path
        if os.path.exists(file_path) and not replace_file:
            raise FileExistsError(f"Error: the specified path \"{file_path}\" already contais a file named \"{self._filename}\"")
        key = self._prefix + self._filename
        try:
            with open(file_path, "wb") as file:
                self._s3.Bucket(self._bucket).download_fileobj(key, file)
        except botocore.exceptions.ClientError as e:
            raise ConnectionError(f"Failed to download the object {self}! The following error was encountered: {e}")
        except Exception as e:
            raise RuntimeError(f"An error was encountered while saving the object {self}: {e}")

    def version_id(self) -> str:
        try:
            version_id = self._s3.Object(self._bucket, self._prefix + self._filename).version_id
        except botocore.exceptions.ClientError as e:
            raise ConnectionError(f"Failed to retrieve object's {self} version id! The following error was encountered: {e}")
        except Exception as e:
            raise RuntimeError(f"An error was encountered while retrieving the object's {self} info: {e}")
        return version_id

    def exists(self) -> bool:
        try:
            self._s3.Object(self._bucket, self._prefix + self._filename).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise RuntimeError(f"Failed to verify if object {self} exists! The following error was while trying to reach AWS: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to verify if object {self} exists! The following error was encountered: {e}")
        return True

    def __str__(self):
        return f"{{\n\t\"bucket\": \"{self._bucket}\",\n\t\"prefix\": \"{self._prefix}\",\n\t\"filename\": \"{self._filename}\"\n}}"

    def __repr__(self):
        return f"S3Object(bucket=\"{self._bucket}\", prefix=\"{self._prefix}\", filename=\"{self._filename}\")"
