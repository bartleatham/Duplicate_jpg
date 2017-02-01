#! /usr/bin/env python

import argparse
import os
import sys
import datetime
import shutil
import hashlib
from PIL import Image

#########################################
###First find all .jpg files and move them to ./year/date folders
def find_and_move(src_dir):
    for i in src_dir:
        if os.path.exists(i):
            for dirName, subdirs, fileList in os.walk(i):
                for filename in fileList:
                    name, ext = os.path.splitext(filename)
                    if ext == '.jpg' or ext == '.JPG':
                        path = os.path.join(dirName, filename)
                        find_date_original(path)
                        new_path = "./%s/%s" % (year,month)
                        #print new_path
                        create_dir(new_path)
                        new_path_file = os.path.join(new_path, filename)
                        if not os.path.isfile(new_path_file):
                            shutil.move(filename, new_path)
                        else:
                            print (new_path_file + ' Already Exists!')
        else:
            print('%s is not a valid path, please verify' % i)
            return {}
   
def find_date_original(filename):
    global year
    global month
    #if exif data exists, get date created, otherwise year and date are unknown
    try:
        d = Image.open(filename)._getexif()[36867]
    #convert unicode date from exif data to a string object
        date_obj = datetime.datetime.strptime(d, '%Y:%m:%d %H:%M:%S')
        year = date_obj.year
        month = date_obj.strftime("%B")
        day = date_obj.day
    #print year, month, day
    except KeyError:
        print("is this working?")
        year = "unknown"
        month = "unknown"
    return year, month

# check if year or year/month dir exists, create it if not
def create_dir(directory):
    if not os.path.exists(directory):
        print ("Creating %s" % directory)
        os.makedirs(directory)


#########################################
###Search through folders for duplicate files, identify and rename with _DUP
def find_duplicates(folders):
    """
    Takes in an iterable of folders and prints & returns the duplicate files
    """
    dup_size = {}
    for i in folders:
        # Iterate the folders given
        if os.path.exists(i):
            # Find the duplicated files and append them to dup_size
            join_dicts(dup_size, find_duplicate_size(i))
        else:
            print('%s is not a valid path, please verify' % i)
            return {}

    #print('Comparing files with the same size...')
    dups = {}
    for dup_list in dup_size.values():
        if len(dup_list) > 1:
            join_dicts(dups, find_duplicate_hash(dup_list))
    print_results(dups)
    return dups

def find_duplicate_size(parent_dir):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parent_dir):
        #print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Check to make sure the path is valid.
            if not os.path.exists(path):
                continue
            # Calculate sizes
            file_size = os.path.getsize(path)
            # Add or append the file path
            if file_size in dups:
                dups[file_size].append(path)
            else:
                dups[file_size] = [path]
    return dups

def find_duplicate_hash(file_list):
    dups = {}
    for path in file_list:
        file_hash = hashfile(path)
        if file_hash in dups:
            #rename duplicate file with _DUP
            name, ext = os.path.splitext(path)
            os.rename(path, name + ext + '_DUP')
            dups[file_hash].append(path)
        else:
            dups[file_hash] = [path]
    return dups

# Joins two dictionaries, adds dict2 entry to dict1 if they are the same
def join_dicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]

def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def print_results(dict1):
    # if the length of values is greater than 1, we have duplicates
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    #for k, v in dict1.iteritems():
    #    print (k, v)
    if len(results) > 0:
        print('Duplicates Found:')
        print(
            'The following files are identical. The name could differ, but the'
            ' content is identical'
            )
        print('___________________')
        for result in results:
            for subresult in result:
                print('\t\t%s' % (subresult))
            print('___________________')
    else:
        print('No duplicate files found.')


def main():
    parser = argparse.ArgumentParser(description='Find duplicate files')
    parser.add_argument(
        'folders', metavar='dir', type=str, nargs='+',
        help='A directory to parse for duplicates',
        )
    args = parser.parse_args()
    find_and_move(args.folders)
    find_duplicates(args.folders)

if __name__ == '__main__':
    sys.exit(main())
