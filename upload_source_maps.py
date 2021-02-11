import glob, os
import sys

import requests

def main(project_read_token, code_version, source_map_path):
    url = "https://api.rollbar.com/api/1/sourcemap"
    headers = {
        'X-Rollbar-Access-Token': project_read_token
    }

    os.chdir(source_map_path)
    for file in glob.glob("*.map"):
        # Strip the ".map" from the filename
        minified_url = file[:-4]
        payload = {
            'version': code_version,
            'minified_url': minified_url
        }
        files = [
            ('source_map', open(file,'rb'))
        ]
        
        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text.encode('utf8'))

    print("Upload Complete!")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python upload_source_maps.py <project_read_token> <code_version> <path_to_source_maps>"
        sys.exit(1)

    project_read_token = sys.argv[1]
    code_version = sys.argv[2]
    source_map_path = sys.argv[3]
    main(project_read_token, code_version, source_map_path)
