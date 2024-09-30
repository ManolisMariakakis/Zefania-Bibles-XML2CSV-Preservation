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