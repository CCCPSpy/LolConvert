import argparse
import os
import ffmpeg

from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.storage.blob import (
    BlobServiceClient,
    generate_account_sas,
    ResourceTypes,
    AccountSasPermissions,
    ContentSettings
)

load_dotenv()
azure_acocunt_name = os.getenv("AZURE_ACCOUNT_NAME")

account_url = f'https://{azure_acocunt_name}.blob.core.windows.net/'
container_name = ""

parser = argparse.ArgumentParser()
parser.add_argument('inputFilename')
parser.add_argument('outputFilename')
args = parser.parse_args()


def convert_file(inputFile):
    output_path = ".\\output\\" + args.outputFilename
    stream = ffmpeg.input(args.inputFilename)
    stream = ffmpeg.output(stream, output_path)
    ffmpeg.run(stream)
    return output_path


sas_token = generate_account_sas(
    account_name=azure_acocunt_name,
    account_key=os.getenv("AZURE_ACCOUNT_KEY"),
    resource_types=ResourceTypes(service=True, object=True),
    permission=AccountSasPermissions(read=True, write=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)

service = BlobServiceClient(
    account_url=account_url,
    credential=sas_token
    )

blob = service.get_blob_client(
    container=container_name,
    blob=args.outputFilename
    )


def upload_blob(blobName):
    content_settings = ContentSettings(content_type='video/mp4')
    with open(blobName, "rb") as data:
        blob.upload_blob(data, content_settings=content_settings)


converted_blob = convert_file(args.inputFilename)
upload_blob(converted_blob)
print(f"URI: {account_url}{container_name}/{args.outputFilename}")
