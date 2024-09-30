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
                outfile.write(curl_command + '\n')  # Write the curl command to the output file

# Example usage
input_file = 'result.txt'
output_file = 'result_curl.txt'
process_file(input_file, output_file)

print(f'Curl commands written to {output_file}.')
