# TODO add file save dir dialog
# TODO add progress bar
# TODO add dir naming

import argparse
import json
import requests
import shutil
import os
import datetime

parser = argparse.ArgumentParser(description='Collects the images from yrons cityfun module')

parser.add_argument('filename', help='the path of the file exported from phpmyadmin')
parser.add_argument('-z', '--zip', help='zips the images after collection', action='store_true')

args = parser.parse_args()

try:
    with open(args.filename) as f:
        data = json.load(f)
        if data[2]['name'] != 'fileUploads' or data[2]['database'] != 'cityfun':
            print('Wrong file format')
            exit() 
        else:
            rows = data[2]['data']
            os.mkdir('images')
            for row in rows:
                fileExtension = row['filename'].split('.')[-1]
                filename = ''.join(row['filename'].split('.')[:-1])
                res = requests.get(row['fullLink'], stream=True)
                if res.status_code == 200:
                    with open(f"images/{row['jwt']}-{filename}.{fileExtension}", 'wb') as f:
                        shutil.copyfileobj(res.raw, f)
                else:
                    print('Error while downloading image')
                    exit()
    if args.zip:
        shutil.make_archive('images', 'zip', 'images')
        shutil.rmtree('images')
    print('Done')
except FileNotFoundError:
    print('File not found')
    exit()
    
