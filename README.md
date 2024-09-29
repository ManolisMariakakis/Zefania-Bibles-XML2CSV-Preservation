
# Zefania-Bibles-XML2CSV-Preservation

This repository contains Python scripts to process Zefania XML Bible files, converting them into CSV format, while also unzipping files downloaded from SourceForge and renaming them by URL-decoding the filenames.

## Features

1. **Download**: Retrieve XML Bible files from SourceForge using `curl`.
2. **Unzipping**: Extract all `.zip` files in the current directory and rename them by URL-decoding the filenames.
3. **Conversion**: Convert Zefania XML Bible files to CSV format, stripping unwanted characters from verse text.
4. **Preservation**: Original XML files are copied into the `csv/` directory after conversion.
5. **Error Handling**: Handles potential file parsing and file not found errors for both `.zip` and XML files.

## Prerequisites

- `curl`: For downloading the `.zip` files from SourceForge.
- `python`: The scripts are written in Python, so make sure Python 3 is installed.

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/ManolisMariakakis/Zefania-Bibles-XML2CSV-Preservation.git
cd Zefania-Bibles-XML2CSV-Preservation
```

### 2. Download XML Bible Files

You can download Bible files from SourceForge using `curl`. For example:

```bash
curl -L -O https://sourceforge.net/projects/zefania-sharp/files/Bibles/English/eng-kjv2006.zip/download
```

This will download the file as `eng-kjv2006.zip`.

### 3. Run the Unzip Script

Once you’ve downloaded the `.zip` files, you can run the provided unzip script, which will extract the files and rename them with URL-decoded filenames.

```bash
python3 unzip_and_rename.py
```

#### What the Script Does:
- Extracts all `.zip` files in the current folder.
- Renames the original `.zip` files by URL-decoding any encoded characters (e.g., `%20` to spaces).
  
### 4. Run the XML to CSV Conversion Script

After extracting the XML files, run the conversion script to convert the XML files to CSV:

```bash
python3 xml_to_csv.py
```

#### What the Script Does:
- Converts all `.xml` files in the current folder to `.csv`.
- Saves the generated CSV files in a `csv/` folder.
- Copies the original XML files into the `csv/` folder for preservation.

### 5. CSV Structure

The CSV files generated from XML have the following columns:

- **Book Number**: Numeric value representing the book number in the Bible.
- **Chapter Number**: Numeric value representing the chapter number within the book.
- **Verse Number**: Numeric value representing the verse number within the chapter.
- **Verse Text**: The actual text of the verse, enclosed in double quotes, and with any quotes within the verse removed.

Example CSV output:

```csv
Book Number,Chapter,Verse Number,Verse Text
1,1,1,"In the beginning, God created the heavens and the earth."
1,1,2,"Now the earth was formless and empty, darkness was over the surface of the deep..."
```

## Python Scripts Overview

### Unzip and Rename Script (`unzip_and_rename.py`)

This script processes all `.zip` files in the current directory, extracts their contents, and renames the original `.zip` files by URL-decoding the filenames.

```python
import os
import zipfile
import urllib.parse

# Function to URL-decode the filename
def decrypt_url(filename):
    # Strip the ".zip" extension before decoding
    base_name = filename.replace('.zip', '')
    # Decode the URL-encoded parts of the filename
    decrypted_url = urllib.parse.unquote(base_name)
    return decrypted_url

# Get the current folder
current_folder = os.getcwd()

# Iterate through all the files in the folder
for item in os.listdir(current_folder):
    if item.endswith(".zip"):
        zip_path = os.path.join(current_folder, item)
        
        try:
            # Unzip the file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract all the contents to the current folder
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
```

### XML to CSV Conversion Script (`xml_to_csv.py`)

This script converts Zefania XML Bible files to CSV format, extracting the book, chapter, and verse details.

```python
import xml.etree.ElementTree as ET
import csv
import os
import shutil

def convert_xml_to_csv(xml_path, csv_path):
    try:
        # Parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing {xml_path}: {e}")
        return
    except FileNotFoundError:
        print(f"File not found: {xml_path}")
        return

    # Open CSV file for writing
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        # Loop through each book
        for book in root.findall('BIBLEBOOK'):
            book_number = int(book.get('bnumber'))  # Convert to integer
            
            # Loop through each chapter in the book
            for chapter in book.findall('CHAPTER'):
                chapter_number = int(chapter.get('cnumber'))  # Convert to integer
                
                # Loop through each verse in the chapter
                for verse in chapter.findall('VERS'):
                    verse_number = int(verse.get('vnumber'))  # Convert to integer
                    
                    # Get the verse text and remove any quotes
                    verse_text = verse.text.strip().replace('"', '') if verse.text else ''
                    
                    # Create the formatted string for the current row
                    formatted_row = f'{book_number},{chapter_number},{verse_number},"{verse_text}"
'
                    
                    # Write the formatted row string directly to the file
                    file.write(formatted_row)

def process_all_xml_files_in_folder():
    # Get the current directory
    current_dir = os.getcwd()
    csv_dir = os.path.join(current_dir, 'csv')  # Create a path to the 'csv' folder

    # Create the csv directory if it doesn't exist
    os.makedirs(csv_dir, exist_ok=True)

    # Get a list of all XML files in the current directory
    xml_files = [f for f in os.listdir(current_dir) if f.endswith('.xml')]

    # Process each XML file
    for xml_file in xml_files:
        xml_file_path = os.path.join(current_dir, xml_file)  # Full path to the XML file
        
        # Define the output CSV file path in the csv directory
        csv_file_name = os.path.basename(xml_file_path)  # Get the base name of the XML file
        csv_file_path = os.path.join(csv_dir, os.path.splitext(csv_file_name)[0] + '.csv')  # Change the extension to .csv
        
        # Convert XML to CSV
        convert_xml_to_csv(xml_file_path, csv_file_path)
        shutil.copy2(xml_file_path, csv_dir)  # Use copy2 to preserve metadata

# Process all XML files in the current folder
process_all_xml_files_in_folder()
```

## License

This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for more details.
