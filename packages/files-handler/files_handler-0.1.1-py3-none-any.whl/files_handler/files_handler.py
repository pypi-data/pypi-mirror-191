# Importing libraries
import boto3
import botocore
import os
import shutil

# Local execution paths
result_path = 'output'
input_path = 'input'

class s3_handler:
    """
    Deal with files and connection to S3.
    
    :param bucket: The Bucket.
    :type bucket: string
    :param path_ref: Reference Path to manage the files and folders.
    :type path_ref: string
    """

    def __init__(self, bucket, path_ref):
        self.access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.environ.get('AWS_REGION_NAME')
        self.bucket = bucket
        self.path_ref = path_ref
        self.path_to_predict_images = os.path.join(path_ref, input_path)
        self.folders_handler = folders_handler(self.path_ref)

    # Get image from s3 bucket 
    def get_image_from_s3_bucket(self, s3_image_path):
        """
        Get an image from S3 passing the image path on s3 and saving on reference path + input
        
        :param s3_image_path: The s3 path of image with the image name.
        :type s3_image_path: string
    
        :return: If the image was downloaded or not.
        :rtype: boolean
        """
        try:
            self.folders_handler.verify_and_create_folder(self.path_ref, 'Creating reference directory...')
            self.folders_handler.verify_and_create_folder(self.path_to_predict_images, 'Creating input directory...')

            image_name = os.path.basename(s3_image_path)
            print(f'Downloading file: {image_name} to {self.path_to_predict_images} folder') 
            s3 = boto3.resource('s3', aws_access_key_id=self.access_key_id,  aws_secret_access_key=self.secret_access_key, region_name=self.region_name)
            bucket = s3.Bucket(self.bucket)
            
            bucket.download_file(s3_image_path, os.path.join(self.path_to_predict_images, image_name))
            print(f'File Downloaded')
            return True
        
        except botocore.exceptions.ClientError as e:
            return False

    # Upload resulting image to s3 bucket
    def upload_image_to_s3_bucket(self, image_path, s3_output_path):
        """
        Upload an image to S3 passing the image path on s3 and the S3 Output Path
        
        :param image_path: the path of the image locally with the image name
        :type image_path: string
        :param s3_output_path: the path of the image on S3
        :type s3_output_path: string
    
        :return: If the image was uploaded or not.
        :rtype: boolean
        """
        try:
            print(f'Uploading results to {s3_output_path}')
            s3 = boto3.resource('s3', aws_access_key_id=self.access_key_id,  aws_secret_access_key=self.secret_access_key, region_name=self.region_name)
            bucket = s3.Bucket(self.bucket)

            image_name = os.path.basename(image_path)
            print(f'Complete path: {s3_output_path}/{image_name}')
            bucket.upload_file(image_path, os.path.join(s3_output_path, image_name))
            return True

        except botocore.exceptions.ClientError as e:
            return False

    # Check if results for current image already exists in s3
    def check_if_results_already_exists(self, image_name, s3_output_path):
        
        try:
            s3 = boto3.resource('s3', aws_access_key_id=self.access_key_id,  aws_secret_access_key=self.secret_access_key, region_name=self.region_name)
            try:
                #s3.head_object(Bucket='bucket_name', Key='file_path')
                s3.Object(self.bucket, os.path.join(s3_output_path, image_name)).load()
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

    # Create response message if output already exists in s3
    def get_response_message(self, image_name, s3_output_path):

        results = {}
        results["data"] = {'Image already exists! Path: '+ os.path.join(self.bucket, s3_output_path, image_name)}
        results["success"] = True

        return results

class folders_handler:

    def __init__(self, path_ref):
        self.path_ref = path_ref
        self.path_to_predict_images = os.path.join(path_ref, input_path)
        self.path_to_results = os.path.join(path_ref, result_path)

    # Clear all files in the input and output temporary directories
    def clear_temporary_resources(self):

        print("Clearing temporary files...")

        if os.path.exists(self.path_to_predict_images):
            shutil.rmtree(self.path_to_predict_images)

        if os.path.exists(self.path_to_results):
            shutil.rmtree(self.path_to_results)

    # Create project temporary directories for current execution
    def manage_directories(self, image_name, output_image_name):

        FILE_PATH = os.path.join(self.path_to_predict_images, image_name)
        OUTPUT_FILE_PATH = os.path.join(self.path_to_results, output_image_name)

        self.verify_and_create_folder(self.path_ref, 'Creating dir directory...')
        self.verify_and_create_folder(self.path_to_results, 'Creating output directory...')
        self.verify_and_create_folder(self.path_to_predict_images, 'Creating input directory...')

        return FILE_PATH, OUTPUT_FILE_PATH

    # Helper function to verify if folder already exists, and if not, create the folder
    def verify_and_create_folder(self, path, message=''):
        if not os.path.exists(path):
            print(message)
            os.mkdir(path)
            return True