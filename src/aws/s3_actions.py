from fastapi import HTTPException, UploadFile
from custom_exceptions.file_exceptions import DeletionFileException, NoFileFoundException, UnexpectedFileError, UploadingFileException
from utils.mixins.file_action import FileActionMixin
import boto3
from config import settings


class S3Service(FileActionMixin):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(S3Service, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, aws_bucket_name: str, aws_access_key: str, aws_secret_key: str):
        if self._initialized:
            return

        self.AWS_BUCKET_NAME = aws_bucket_name
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        self.bucket = self.s3.Bucket(self.AWS_BUCKET_NAME)
        self.initialized = True

    async def s3_upload_file(self, file: UploadFile | None, key: str) -> None:
        try:
            if not file:
                raise NoFileFoundException()
            
            contents = await file.read()
            file_type = self.get_file_type(file.filename)
            self.validate_file_size(len(contents), file_type)

            s3_object = self.bucket.put_object(Key=key, Body=contents)
            if not s3_object:
                raise UploadingFileException(f'Error during uploading file {file.filename}! (problem on s3 side)')
            
        except HTTPException:
            raise
        except Exception as e:
            raise UnexpectedFileError(f'Error during file upload: {str(e)}')


    async def s3_delete_file(self, key: str) -> None:
        try:
            response = self.bucket.delete_objects(
                Delete={'Objects': [{'Key': key}]}
            )
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise DeletionFileException(f'Error during deletion file {key}')

        except HTTPException:
            raise
        except Exception as e:
            raise UnexpectedFileError(f'Error during file deletion: {str(e)}')

    async def s3_download_file(self, key: str) -> bytes:
        try:
            return self.s3.Object(
                bucket_name=self.AWS_BUCKET_NAME,
                key=key
            ).get()['Body'].read()
        except Exception as e:
            raise UnexpectedFileError(f'Error downloading file: {str(e)}')

    async def s3_update_file(self, old_key: str, new_key: str, new_file: UploadFile):
        try:
            await self.s3_delete_file(old_key)
            await self.s3_upload_file(new_file, new_key)
        except Exception as e:
            raise UnexpectedFileError(f'Error updating file: {str(e)}')
        

s3_client = S3Service(
    aws_access_key=settings.aws_access_key_id,
    aws_secret_key=settings.aws_secret_access_key,
    aws_bucket_name=settings.aws_bucket_name
)