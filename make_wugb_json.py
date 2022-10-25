#!/usr/bin/env python3

"""
This script scans a sub-directory of `/mnt/data1/www/html` on `plutus`
(128.91.213.129), and saves a JSON file that includes all bigWig (bw)
files in the sub-directory. The JSON file can be loaded by Washington
University Genome Browser (WUGB).

Two arguments are required by the script:
  * genome type, such as `hg19` or `hg38`
  * sub-directory name

Two new files will be generated in the sub-directory:
  * `wugb.json`: JSON file for WUGB
  * `wugb_url.txt`: the URL of WUGB
"""

import json
import os
import sys

# Web server config
LOCAL_SERVER_ROOT = "/mnt/data1/www/html/"
LOCAL_HTTP_MAIN = "http://faryabi05.med.upenn.edu/"
WUGB_MAIN = "https://epigenomegateway.wustl.edu/browser"

# Output filenames
JSON_FILENAME = "wugb.json"
URL_FILENAME = "wugb_url.txt"

def chk_bw_dir(dir_name):
    """
    Check whether:
     * `dir_name` is a directory
     * `dirname` is a sub-directory of `LOCAL_SERVER_ROOT`

    Return the absolute path of `dir_name`.
    """

    abs_path = os.path.abspath(dir_name)
    if not os.path.isdir(abs_path):
        print(f"ERROR: '{dir_name}' is not a directory")
        sys.exit(2)

    if not abs_path.startswith(HTML_ROOT):
        print(f"ERROR: '{dir_name}' is not located in '{LOCAL_SERVER_ROOT}'")
        sys.exit(3)

    return abs_path


# Main
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: make_wugb_json.py [genome_type] [input_directory]")
        sys.exit(1)

    genome_type = sys.argv[1]
    bw_dir = sys.argv[2]

    abs_bw_dir = chk_bw_dir(bw_dir)
    wugb_hub = list()
    for root, _, files in os.walk(abs_bw_dir):
        # Make sure `root` is accessible by all users
        os.chmod(root, 0755)

        for f in files:
            if not f.endswith(".bw"):
                continue

            abs_file_path = os.path.join(root, f)
            sub_url = os.path.relpath(abs_file_path, start=LOCAL_SERVER_ROOT)
            local_url = LOCAL_HTTP_MAIN + sub_url
            hub_entry = dict()
            hub_entry["type"] = "bigwig"
            hub_entry["url"] = local_url
            hub_entry["name"] = f.split('.')[0]
            hub_entry["showOnHubLoad"] = True

    # Create `wugb.json` in `bw_dir`
    json_path = os.path.join(abs_bw_dir, JSON_FILENAME)
    with open(json_filename, "w") as ofh:
        json.dump(wugb_hub, ofh, indent=2)

    # Create `wugb_url.txt` in `bw_dir`:
    url_path = os.path.join(abs_bw_dir, URL_FILENAME)
    url_str = f"{WUGB_MAIN}/#?genome={genome_type}&hub={local_url}"
    with open(url_filename, "w") as ofh:
        ofh.write(url_str, "\n")

    # Print `url_str` on stdout
    print(f"JSON file is saved at: '{json_filename}'")
    print(f"View it at: {url_str}")
    print(f"URL is saved at: '{url_filename}'")
