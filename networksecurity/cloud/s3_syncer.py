import os
class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_name):
        command = f"aws s3 sync {folder} {aws_bucket_name}/"
        os.system(command)

    def sync_folder_from_s3(self, folder, aws_bucket_name):
        command = f"aws s3 sync s3://{aws_bucket_name} {folder}"
        os.system(command)