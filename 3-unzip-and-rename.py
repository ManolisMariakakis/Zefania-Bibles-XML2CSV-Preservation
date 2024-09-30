import os
import zipfile
import urllib.parse

# Function to URL-decode the filename
def decrypt_url(filename):
    base_name = filename.replace('.zip', '')
    decrypted_url = urllib.parse.unquote(base_name)
    return decrypted_url

current_folder = os.getcwd()

# Iterate through all the files in the folder
for item in os.listdir(current_folder):
    if item.endswith(".zip"):
        zip_path = os.path.join(current_folder, item)
        
        try:
            # Unzip the file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(current_folder)
            print(f'Unzipped: {item}')
            
            # URL-decode to rename the original file
            decrypted_name = decrypt_url(item)  # Get decrypted name without .zip extension
            new_zip_path = os.path.join(current_folder, decrypted_name + ".zip")
            
            # Rename the original .zip file
            os.rename(zip_path, new_zip_path)
            print(f'Renamed: {item} to {decrypted_name}.zip')
        
        except zipfile.BadZipFile:
            print(f"Error: {item} is not a valid zip file. Skipping...")
        except Exception as e:
            print(f"Error with {item}: {e}. Skipping...")

print("Completed unzipping and renaming all valid .zip files.")