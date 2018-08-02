#!/usr/bin/env python3
import requests
import argparse
import sys, re

# License  : Free Domain
# Author   : Unknown
# Requires : python2.7

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    # endif
    save_response_content(response, destination)
# enddef

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
        # endif
    # endfor
    return None
# enddef

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    print("Saving to {}".format(destination))
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
            # endif
        # endfor
    # endwith
# enddef

if __name__ == "__main__":
    prsr = argparse.ArgumentParser()
    prsr.add_argument("--url",   help="GDrive Shareable Link",   type=str, default=None)
    prsr.add_argument("--ofile", help="Output file name.",       type=str, default=None)
    args = prsr.parse_args()

    if not args.__dict__["url"]:
        print("--url is requied.")
        if not args.__dict__["ofile"]:
            print("--ofile is required.")
        # endif
        sys.exit(-1)
    # endif

    # Verify url
    url_patt = r'drive\.google\.com\/open\?id=([\w]+)'
    s_obj    = re.search(url_patt, args.__dict__["url"])
    if not s_obj:
        print('--url expected in this form https://drive.google.com/open?id=FILE_ID')
        sys.exit(-1)
    # endif
    download_file_from_google_drive(s_obj.groups()[0], args.__dict__["ofile"])
# endif
