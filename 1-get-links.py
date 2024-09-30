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