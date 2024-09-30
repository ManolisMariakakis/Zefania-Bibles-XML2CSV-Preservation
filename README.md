# Zefania Bibles XML to CSV Preservation

This repository provides tools for converting XML files of Zefania Bible translations into CSV format. It includes functionality to discover ZIP files of Bible translations from the Zefania SourceForge project, download them, and extract the XML files for further processing.

## Description

The main purpose of this project is to convert XML Bible files into a CSV format that is compatible with the [OBS Studio Bible Dock Plugin](https://github.com/ManolisMariakakis/bible-dock-plugin). This conversion ensures that Bible texts can be easily integrated into the plugin. The XML files are originally hosted on SourceForge and are downloaded as ZIP archives.

## Requirements

- Python 3.x
- Required libraries:
  - `xml.etree.ElementTree` (part of Python's standard library)
  - `csv` (part of Python's standard library)
  - `os` (part of Python's standard library)
  - `shutil` (part of Python's standard library)
  - `beautifulsoup4` (install via pip)

## How to Use

### Downloading the ZIP Files

To obtain the `.zip` files for the Zefania Bible XML files, follow these steps:

1. **Download the Activity Page**:
   - Visit the [SourceForge Zefania Sharp Activity Page](https://sourceforge.net/p/zefania-sharp/activity/) and save the page as an HTML file. Ensure to capture enough entries to find the desired `.zip` links.

2. **Process the HTML File**:
   - Use the provided Python script to extract the download links from the saved HTML file. This script utilizes Tkinter for file selection and BeautifulSoup for HTML parsing.

   Here's the code used to extract the links:

   ```python
   from tkinter import Tk
   from tkinter import filedialog
   from bs4 import BeautifulSoup

   # Create a Tkinter root window (it won't be shown)
   root = Tk()
   root.withdraw()  # Hide the root window

   # Open a file dialog and allow the user to select a text file
   file_path = filedialog.askopenfilename(
       title="Select an HTML file", 
       filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("All Files", "*.*"))
   )

   # Check if the user selected a file
   if file_path:
       # Read the selected file
       with open(file_path, 'r', encoding='utf-8') as file:
           html_content = file.read()

       # Parse the HTML using BeautifulSoup
       soup = BeautifulSoup(html_content, 'html.parser')

       # Find all <a> tags inside <h1> within <li> elements
       links = soup.select('.timeline li h1 a')

       # Extract the href attributes that end with .zip/download and start with the specified URL
       zip_download_links = [
           link['href'] for link in links 
           if link['href'].endswith('.zip/download') and link['href'].startswith('http://sourceforge.net/projects/zefania-sharp/files/Bibles')
       ]

       # Write the extracted links to result.txt
       with open('result.txt', 'w', encoding='utf-8') as result_file:
           for link in zip_download_links:
               result_file.write(link + '\n')

       print("Links have been written to result.txt.")
   else:
       print("No file selected.")
   ```

3. **Run the Script**:
   - Execute the script in your Python environment. It will prompt you to select the saved HTML file. Once processed, the script will write all valid `.zip` download links to a file named `result.txt`.

4. **Download the ZIP Files**:
   - Use the links found in `result.txt` to download the `.zip` files using `curl`. Here’s an example of how to use `curl` in the command line:

   ```bash
   curl -L -o SF_2009-01-20_AFR_AFR3353_%281933_1953%20AFRIKAANS%20BYBEL%29.zip https://sourceforge.net/projects/zefania-sharp/files/Bibles/AFR/1933/1953%20Afrikaans%20Bybel/SF_2009-01-20_AFR_AFR3353_%281933_1953%20AFRIKAANS%20BYBEL%29.zip/download
   ```
   Replace `<URL>` with the actual link from `result.txt`. You can run this command for each link.

## Generating Curl Commands

To prepare curl commands for downloading ZIP files, you can use the following script. This script reads URLs from a file, generates curl commands for each URL, and saves the commands to an output file.

```python
import urllib.parse

def generate_curl_command(url):
    # Extract the filename from the URL
    parsed_url = urllib.parse.urlparse(url)
    path_segments = parsed_url.path.split('/')
    
    # The second-to-last segment in the path contains the filename
    raw_filename = path_segments[-2]
    
    # Decode the filename to handle URL-encoded characters (e.g., %20 -> space)
    decoded_filename = urllib.parse.unquote(raw_filename)
    
    # Clean up the filename: remove unnecessary characters and replace spaces
    cleaned_filename = decoded_filename.replace(' ', '_').replace('(', '').replace(')', '')
    
    # Create the full curl command
    curl_command = f'curl -L -o "{cleaned_filename}" {url}'
    
    return curl_command

def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            url = line.strip()  # Remove any surrounding whitespace or newline characters
            if url:  # Ensure the line is not empty
                curl_command = generate_curl_command(url)
                outfile.write(curl_command + '\\n')  # Write the curl command to the output file

# Example usage
input_file = 'result.txt'
output_file = 'result_curl.txt'
process_file(input_file, output_file)

print(f'Curl commands written to {output_file}.')


### Unzipping the ZIP Files

Once you have downloaded the `.zip` files, you can unzip all ZIP files in the folder using the following Python script:

```python
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
```

To run this unzip script, execute the following command in the terminal:

```bash
python3 unzip_and_rename.py
```

### Converting XML to CSV

After downloading and extracting the `.zip` files, you can convert the XML files to CSV format using the following Python script:

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
                    formatted_row = f'{book_number},{chapter_number},{verse_number},"{verse_text}"\n'
                    
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

