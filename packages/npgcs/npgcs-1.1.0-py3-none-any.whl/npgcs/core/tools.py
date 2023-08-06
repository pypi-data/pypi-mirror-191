"""
referencecs:
GCS code: https://github.com/googleapis/python-storage/tree/e770f1b0355e22412114159b0558ad753ac9d28e/samples/snippets
BigQuery: https://github.com/googleapis/python-bigquery/blob/a3f4351633f006b3132d8a8625ad7921b3d57699/samples/snippets/create_table_external_hive_partitioned.py
BgiQuery: https://github.com/googleapis/python-bigquery/blob/35627d145a41d57768f19d4392ef235928e00f72/samples/load_table_uri_parquet.py
"""
import asyncio
import logging
import os
from io import BytesIO
from typing import Optional

from google.api_core import exceptions
from google.api_core.retry import Retry, if_exception_type
from google.cloud import storage

logger = logging.getLogger(__name__)
logger.propagate = False  # remove duplicated log
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

_MY_RETRIABLE_TYPES = (
    exceptions.TooManyRequests,  # 429
    exceptions.InternalServerError,  # 500
    exceptions.BadGateway,  # 502
    exceptions.ServiceUnavailable,  # 503
)


class NPGCS(object):
    def __init__(self, project_id, gcp_service_account_path: Optional[str] = None):
        self.project_id = project_id
        self.path_json_key = gcp_service_account_path
        self.__add_environment()
        self.client = self.__get_gcs_client()

    def __add_environment(self):
        if self.path_json_key:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.path_json_key

    def __get_gcs_client(self):
        return storage.Client(self.project_id)

    def create_bucket(
        self,
        bucket_name: str,
        location: str = "asia-southeast1",
        storage_class: str = "Standard",
    ) -> bool:
        bucket = self.client.bucket(bucket_name)
        bucket.location = location
        bucket.storage_class = storage_class
        try:
            bucket.create()
        except Exception as e:
            print(f"Error: {e}")
            return False
        else:
            return True

    def delete_bucket(self, bucket_name: str) -> bool:
        bucket = self.client.bucket(bucket_name)
        try:
            bucket.delete()
        except Exception as e:
            print(f"Error: {e}")
            return False
        else:
            return True

    def list_blobs(self, bucket_name, prefix=None, delimiter=None, suffix=None):
        """Lists all the blobs in the bucket that begin with the prefix.
        This can be used to list all blobs in a "folder", e.g. "public/".
        The delimiter argument can be used to restrict the results to only the
        "files" in the given "folder". Without the delimiter, the entire tree under
        the prefix is returned. For example, given these blobs:
            a/1.txt
            a/b/2.txt
        If you specify prefix ='a/', without a delimiter, you'll get back:
            a/1.txt
            a/b/2.txt
        However, if you specify prefix='a/' and delimiter='/', you'll get back
        only the file directly under 'a/':
            a/1.txt
        As part of the response, you'll also get back a blobs.prefixes entity
        that lists the "subfolders" under `a/`:
            a/b/
        """
        if prefix:
            # Note: Client.list_blobs requires at least package version 1.17.0.
            blobs = self.client.list_blobs(
                bucket_name, prefix=prefix, delimiter=delimiter
            )
        else:
            blobs = self.client.list_blobs(bucket_name)

        blob_list = []
        for blob in blobs:
            if suffix:
                if str(blob.name).lower().endswith(suffix) and (
                    not blob.name.lower().endswith("/")
                ):
                    blob_list.append(blob.name)
            elif not blob.name.lower().endswith("/"):
                blob_list.append(
                    {
                        "blob_name": blob.name,
                        "blob_dt_created": blob.time_created,
                    }
                )
            else:
                print(f"Listing skipped: {blob.name}")

        if delimiter:
            print("Prefixes:")
            for prefix in blobs.prefixes:  # type: ignore
                print(prefix)
        return blob_list

    @Retry(predicate=if_exception_type(_MY_RETRIABLE_TYPES))
    def copy_blob(self, bucket_source, blob_source, bucket_destination, blob_destination):
        source_bucket = self.client.bucket(bucket_source)
        source_blob = source_bucket.blob(blob_source)
        destination_bucket = self.client.bucket(bucket_destination)
        blob_copy = source_bucket.copy_blob(
            source_blob, destination_bucket, blob_destination
        )

    @Retry(predicate=if_exception_type(_MY_RETRIABLE_TYPES))
    def delete_blob(self, bucket_name, blob_name):
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()

    @Retry(predicate=if_exception_type(_MY_RETRIABLE_TYPES))
    def download_blob(self, bucket_name, source_blob_name, destination_file_name=None):
        """Downloads a blob from the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your GCS object
        # source_blob_name = "storage-object-name"

        # The path to which the file should be downloaded
        # destination_file_name = "local/path/to/file"

        bucket = self.client.bucket(bucket_name)

        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        blob = bucket.blob(source_blob_name)
        if destination_file_name:
            self.create_local_path(destination_file_name)
        else:
            destination_file_name = self.auto_gen_local_path(source_blob_name)
        blob.download_to_filename(destination_file_name)

        logging.info(
            "Downloaded storage object {} from bucket {} to local file {}.".format(
                source_blob_name, bucket_name, destination_file_name
            )
        )

    @Retry(predicate=if_exception_type(_MY_RETRIABLE_TYPES))
    def download_blob_to_stream(self, bucket_name, source_blob_name):
        """Downloads a blob to a stream or other file-like object."""

        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your GCS object (blob)
        # source_blob_name = "storage-object-name"

        # The stream or file (file-like object) to which the blob will be written
        # import io
        file_obj = BytesIO()

        bucket = self.client.bucket(bucket_name)

        # Construct a client-side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` in that it doesn't
        # retrieve metadata from Google Cloud Storage. As we don't use metadata in
        # this example, using `Bucket.blob` is preferred here.
        blob = bucket.blob(source_blob_name)
        blob.download_to_file(file_obj)

        logging.debug(f"Downloaded blob {source_blob_name} to file-like object.")
        file_obj.seek(0)
        return file_obj

    @Retry(predicate=if_exception_type(_MY_RETRIABLE_TYPES))
    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        logging.info(f"File {source_file_name} uploaded to {destination_blob_name}.")

    @Retry(predicate=if_exception_type(_MY_RETRIABLE_TYPES))
    def upload_blob_from_stream(self, bucket_name, file_obj, destination_blob_name):
        """Uploads bytes from a stream or other file-like object to a blob."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The stream or file (file-like object) from which to read
        # import io
        # file_obj = io.BytesIO()
        # file_obj.write(b"This is test data.")

        # The desired name of the uploaded GCS object (blob)
        # destination_blob_name = "storage-object-name"

        # Construct a client-side representation of the blob.
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Rewind the stream to the beginning. This step can be omitted if the input
        # stream will always be at a correct position.
        file_obj.seek(0)

        # Upload data from the stream to your bucket.
        blob.upload_from_file(file_obj)

        logging.info(f"uploaded to {bucket_name}.{destination_blob_name}")

    @Retry(predicate=if_exception_type(_MY_RETRIABLE_TYPES))
    async def async_upload_blob(self, bucket_name, local_files):
        """Uploads a number of files in parallel to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        bucket = self.client.bucket(bucket_name)

        loop = asyncio.get_running_loop()

        tasks = []

        for local_file in local_files:
            blob = bucket.blob(local_file)
            tasks.append(
                loop.run_in_executor(None, blob.upload_from_filename, local_file)
            )

        # If the method returns a value (such as download_as_string), gather will return the values
        await asyncio.gather(*tasks)
        print("job is done")

    # ================================= helper func =================================
    def create_local_path(self, destination_file_name: str) -> bool:
        """create local path if not exist"""
        path = os.path.dirname(destination_file_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return True

    def auto_gen_local_path(self, source_blob_name: str) -> str:
        """auto generate local path"""
        path = os.path.join(os.getcwd(), source_blob_name)
        self.create_local_path(path)
        return path
