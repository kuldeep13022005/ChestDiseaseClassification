import os
import gdown
import zipfile
from Respire.Utils import *
from Respire.Logger import logging
from Respire.Exception import CustomException
from Respire.Entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    def download_file(self)-> str:
        try: 
            dataset_url, zip_download_dir = self.config.Source_URL, self.config.Local_Data_File
            os.makedirs(os.path.dirname(zip_download_dir), exist_ok=True)
            
            if os.path.exists(zip_download_dir) and os.path.getsize(zip_download_dir) > 1024 * 1024:
                logging.info(f"File already exists at {zip_download_dir} with size {os.path.getsize(zip_download_dir)} bytes, skipping download.")
                return

            logging.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            if "drive.google.com" in dataset_url or "google" in dataset_url:
                file_id = dataset_url.split("/")[-2]
                prefix = 'https://drive.google.com/uc?export=download&confirm=t&id='
                gdown.download(prefix+file_id, zip_download_dir)
            else:
                import urllib.request
                req = urllib.request.Request(
                    dataset_url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req) as response, open(zip_download_dir, 'wb') as out_file:
                    out_file.write(response.read())

            logging.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

        except Exception as e:
            import sys
            from Respire.Exception import CustomException
            # Make sure we pass the correct arguments to CustomException if it expects (error_message, error_detail)
            # Check CustomException signature or wrap it nicely.
            raise CustomException(e, sys)
        
    
    def extract_zip_file(self):
        try:
            unzip_path = self.config.Unzip_Dir
            os.makedirs(unzip_path, exist_ok=True)
            with zipfile.ZipFile(self.config.Local_Data_File, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
            logging.info(f"Extracted data from {self.config.Local_Data_File} into {unzip_path}")

            import shutil
            temp_data_dir = os.path.join(unzip_path, "Data")
            target_data_dir = os.path.join(unzip_path, "Chest-CT-Scan-data")
            os.makedirs(target_data_dir, exist_ok=True)

            if os.path.exists(temp_data_dir):
                logging.info(f"Merging split directories under {temp_data_dir} into {target_data_dir}")
                splits = ["train", "valid", "test"]
                for split in splits:
                    split_dir = os.path.join(temp_data_dir, split)
                    if os.path.exists(split_dir):
                        for class_folder in os.listdir(split_dir):
                            src_class_path = os.path.join(split_dir, class_folder)
                            
                            # Map folder names to unified classes
                            folder_lower = class_folder.lower()
                            if "adenocarcinoma" in folder_lower:
                                unified_name = "adenocarcinoma"
                            elif "large" in folder_lower:
                                unified_name = "large.cell.carcinoma"
                            elif "normal" in folder_lower:
                                unified_name = "normal"
                            elif "squamous" in folder_lower:
                                unified_name = "squamous.cell.carcinoma"
                            else:
                                unified_name = class_folder
                                
                            dest_class_path = os.path.join(target_data_dir, unified_name)
                            os.makedirs(dest_class_path, exist_ok=True)
                            
                            # Move files and prevent name collision
                            for img_file in os.listdir(src_class_path):
                                src_file = os.path.join(src_class_path, img_file)
                                dest_file = os.path.join(dest_class_path, f"{split}_{img_file}")
                                shutil.move(src_file, dest_file)
                shutil.rmtree(temp_data_dir)
                logging.info(f"Successfully merged splits and removed temporary directory {temp_data_dir}")

        except Exception as e:
            raise CustomException(e)