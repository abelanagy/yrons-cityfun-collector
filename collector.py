# TODO add file save dir dialog
# TODO add progress bar

import argparse
import json
import requests
import shutil
import os
import datetime

parser = argparse.ArgumentParser(description='Collects the images from yrons cityfun module')

parser.add_argument('filename', help='the path of the file exported from phpmyadmin')
parser.add_argument('-z', '--zip', help='zips the images after collection', action='store_true')
parser.add_argument('-v', '--verbose', help='prints more information', action='store_true')
parser.add_argument('-d', '--dir', dest='dir', help='the directory to save the images to', default='images')

args = parser.parse_args()

try:
    with open(args.filename) as f:
        data = json.load(f)
        if data[2]['name'] != 'fileUploads' or data[2]['database'] != 'cityfun':
            print('Wrong file format', data[2]['name'], data[2]['database'])
            exit() 
        else:
            rows = data[2]['data']
            if args.verbose:
                print(f"Found {len(rows)} images in table, starting download")
            try:
               os.mkdir(args.dir)
            except:
                print('Directory already exists')
                pass
            for row in rows:
                fileExtension = row['filename'].split('.')[-1]
                filename = ''.join(row['filename'].split('.')[:-1])
                res = requests.get(row['fullLink'], stream=True)
                if res.status_code == 200:
                    with open(f"{args.dir}/{row['jwt']}-{filename}.{fileExtension}", 'wb') as f:
                        shutil.copyfileobj(res.raw, f)
                        if args.verbose:
                            print(f"Downloading {filename}.{fileExtension}, and saving as {row['jwt']}-{filename}.{fileExtension}")
                else:
                    print('Error while downloading image')
                    exit()
    if args.zip:
        shutil.make_archive('images', 'zip', args.dir)
        shutil.rmtree(args.dir)
    print('Done')
except FileNotFoundError:
    print('File not found')
    exit()
    
