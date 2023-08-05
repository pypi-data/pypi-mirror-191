import os
import click
from google.cloud import storage

def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def download_from_bucket(bucket_name, source_blob_name, destination_file_name):
    """Downloads a file from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(
        "File {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )


@click.command()
def main():
    """Main entry point for the CLI."""
    while True:
        action = click.prompt("What do you want to do?", type=click.Choice(["upload", "download", "exit"]))
        if action == "upload":
            bucket_name = click.prompt("Bucket name", type=str, default='test')
            source_file_name = click.prompt(f"Source file name", type=str)
            destination_blob_name = click.prompt(f"Destination file name ('./<example.py>')", type=str)
            upload_to_bucket(bucket_name, source_file_name, destination_blob_name)
        elif action == "download":
            bucket_name = click.prompt("Bucket name", type=str, default='test')
            source_blob_name = click.prompt(f"Source file name, ('test/<example.py>')", type=str)
            destination_file_name = click.prompt("Destination file name", type=str, default="my-downloaded-file.txt")
            download_from_bucket(bucket_name, source_blob_name, destination_file_name)
  
        else:
            break


# @click.command()
# def main():
#     """Main entry point for the CLI."""
#     while True:
#         action = click.prompt("What do you want to do?", type=click.Choice(["upload", "download", "project_name", "exit"]))
#         if action == "upload":
#             bucket_name = click.prompt("Bucket name", type=str, default=config.bucket_name)
#             local_path = click.prompt(f"Source file name", type=str)
#             blob_path = click.prompt(f"Destination file name ('{config.project_name}/<example.py>')", type=str)
#             upload(blob_path, local_path, bucket_name)

#         elif action == "download":
#             bucket_name = click.prompt("Bucket name", type=str, default=config.bucket_name)
#             blob_path = click.prompt(f"Source file name, ('{config.project_name}/<example.py>')", type=str)
#             local_path = click.prompt("Destination file name", type=str, default="my-downloaded-file.txt")
#             download(blob_path, local_path, bucket_name)
#         elif action == "project_name":
#             print(config.project_name)
#         else:
#             break


if __name__=="__main__":
    main()