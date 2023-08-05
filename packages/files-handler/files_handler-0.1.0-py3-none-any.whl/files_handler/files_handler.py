# Importing libraries
import boto3
import botocore
import os
from .logger import logger
import shutil

# Local execution paths
path_ref = '/opt/program/dir/'
result_path = 'output/'
data_path = 'input/'

# Local image path
path_to_predict_images = path_ref + data_path
path_to_results = path_ref + result_path

class files_handler:

    # Get image from s3 bucket
    def get_image_from_s3_bucket(self, image_name, s3_image_path):

        try:
            self.verify_and_create_folder(os.environ.get('OUTPUT_IMAGE_PATH', path_to_predict_images), 'Creating input directory...')
            logger.info(f'Downloading file: {image_name} to {path_to_predict_images} folder') 
            s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'), region_name=os.environ.get('AWS_REGION_NAME'))
            bucket = s3.Bucket(os.environ.get('BUCKET_NAME', 'imagery-4pris-images'))
            
            bucket.download_file(os.path.join(s3_image_path, image_name), os.path.join(os.environ.get('OUTPUT_IMAGE_PATH', path_to_predict_images), image_name))
            logger.info(f'File Dowloaded')
            return True
        
        except botocore.exceptions.ClientError as e:
            return False

    # Upload resulting image to s3 bucket
    def upload_image_to_s3_bucket(self, image_path, s3_output_path):
        
        try:
            logger.info(f'Uploading results to {s3_output_path}')
            s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'), region_name=os.environ.get('AWS_REGION_NAME'))
            bucket = s3.Bucket(os.environ.get('BUCKET_NAME', 'imagery-4pris-images'))

            image_name = os.path.basename(image_path)
            logger.info(f'Complete path: {s3_output_path}/{image_name}')
            bucket.upload_file(image_path, os.path.join(s3_output_path, image_name))
            return True

        except botocore.exceptions.ClientError as e:
            return False

    # Check if results for current image already exists in s3
    def check_if_results_already_exists(self, image_name, s3_output_path):
        
        try:
            s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'), region_name=os.environ.get('AWS_REGION_NAME'))
            try:
                #s3.head_object(Bucket='bucket_name', Key='file_path')
                s3.Object(os.environ.get('BUCKET_NAME', 'imagery-4pris-images'), os.path.join(s3_output_path, image_name)).load()
                return True
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    # The object does not exist.
                    return False
                else:
                    # Something else has gone wrong.
                    raise
        except botocore.exceptions.ClientError as e:
            return False

    # Clear all files in the input and output temporary directories
    def clear_temporary_resources(self):

        logger.info("Clearing temporary files...")

        if os.path.exists(path_to_predict_images):
            shutil.rmtree(path_to_predict_images)

        if os.path.exists(path_to_results):
            shutil.rmtree(path_to_results)

    # Create project temporary directories for current execution
    def manage_directories(self, image_name, output_image_name):

        FILE_PATH = os.path.join(path_to_predict_images, image_name)
        OUTPUT_FILE_PATH = os.path.join(path_to_results, output_image_name)

        self.verify_and_create_folder(path_ref, 'Creating dir directory...')
        self.verify_and_create_folder(path_to_results, 'Creating output directory...')
        self.verify_and_create_folder(path_to_predict_images, 'Creating input directory...')

        return FILE_PATH, OUTPUT_FILE_PATH

    # Create response message if output already exists in s3
    def get_response_message(self, output_image_name, s3_output_path):

        results = {}
        results["data"] = {'Image already exists! Path: '+os.path.join(os.environ.get('BUCKET_NAME', 'imagery-4pris-images'), s3_output_path, output_image_name)}
        results["success"] = True

        return results

    # Get existing results in s3 by image name, if they already exist (currently not being used)
    def get_results_by_filename(self, image_name, s3_output_path):

        logger.info(f'Getting existent results for {image_name}')
        s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        bucket = s3.Bucket(os.environ.get('BUCKET_NAME', 'imagery-4pris-images'))
        bucket.download_file(os.path.join(s3_output_path, image_name), os.path.join(path_to_results, image_name))

    # Helper function to verify if folder already exists, and if not, create the folder
    def verify_and_create_folder(self, path, message=''):
        if not os.path.exists(path):
            logger.info(message)
            os.mkdir(path)
            return True