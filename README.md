
# Zefania-XML2CSV-Preservation

This repository contains scripts and utilities for converting XML Bible files from the [Zefania XML project](https://sourceforge.net/projects/zefania-sharp/files/Bibles/) to CSV format. The XML files are bundled in `.zip` archives and need to be downloaded and extracted before conversion.

## Features

- **Download**: Retrieve XML Bible files from SourceForge using `curl`.
- **Conversion**: Convert Zefania XML Bible files to CSV format.
- **Preservation**: Safeguard the XML files and provide an accessible CSV format for further data processing.

## Prerequisites

- `curl`: For downloading the zip files from SourceForge.
- `unzip`: To extract the XML files from the downloaded zip archives.
- `python` or any tool to handle XML to CSV conversion (see instructions below).

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/ManolisMariakakis/Zefania-XML2CSV-Preservation.git
cd Zefania-XML2CSV-Preservation
```

### 2. Download XML Bible Files

You can download Bible files from SourceForge using `curl`. For example:

```bash
curl -L -O https://sourceforge.net/projects/zefania-sharp/files/Bibles/English/eng-kjv2006.zip/download
```

This will download the file as `eng-kjv2006.zip`.

### 3. Extract XML Files

Once you’ve downloaded the `.zip` file, you need to extract the XML files:

```bash
unzip eng-kjv2006.zip -d ./xml_files/
```

This will extract the XML files into a directory called `xml_files`.

### 4. Convert XML to CSV

To convert the XML files to CSV format, you can use a custom Python script or any XML-to-CSV conversion tool. Here’s a basic Python script example:

```python
import xml.etree.ElementTree as ET
import csv

def xml_to_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Define the CSV headers (customize as per the XML structure)
        writer.writerow(["Book", "Chapter", "Verse", "Text"])

        for book in root.findall(".//BIBLEBOOK"):
            book_name = book.attrib['bname']
            for chapter in book.findall(".//CHAPTER"):
                chapter_number = chapter.attrib['cnumber']
                for verse in chapter.findall(".//VERS"):
                    verse_number = verse.attrib['vnumber']
                    verse_text = verse.text
                    writer.writerow([book_name, chapter_number, verse_number, verse_text])

# Example usage
xml_to_csv('./xml_files/eng-kjv2006.xml', './csv_files/eng-kjv2006.csv')
```

This script extracts Bible text from XML and saves it to CSV. You may need to adjust it according to the specific XML schema you are working with.

### 5. View and Use CSV Files

After conversion, the CSV files will be available in the `csv_files/` directory, and you can use them for data analysis, display, or integration into other projects.

## Notes

- The SourceForge repository contains Bible translations in many languages. Adjust the `curl` command to download other language files by browsing the [SourceForge directory](https://sourceforge.net/projects/zefania-sharp/files/Bibles/).
- Ensure you have sufficient disk space for downloading and extracting large XML files.

## Contributions

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions for improvements or new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
