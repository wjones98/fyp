import boto3
import os


class File:

    LANDING_FOLDER = 'C:\\Users\\wajon\\OneDrive\\Documents\\GitHub\\fyp\\landing\\'
    BUCKET = 'fyp-data-repo'
    S3_CLIENT = boto3.client('s3')

    def __init__(self, file):
        self.file = file
        self.file_name = file.filename
        self.full_path = os.path.join(self.LANDING_FOLDER, self.file_name)
        return

    def upload_file_landing(self):
        self.file.save(self.full_path)

    def delete_file_landing(self):
        os.remove(self.full_path)

    def upload_file_s3(self):
        return self.S3_CLIENT.upload_file(self.full_path, self.BUCKET, self.file_name)
