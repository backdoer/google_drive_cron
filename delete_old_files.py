#! /usr/bin/env python
from operator import itemgetter, attrgetter
import os
import glob

def _sort_files_by_last_modified(files):
    """ Given a list of files, return them sorted by the last
         modified times. """
    fileData = {}
    for fname in files:
        fileData[fname] = os.stat(fname).st_mtime

    fileData = sorted(fileData.items(), key = itemgetter(1))
    return fileData 

def _delete_oldest_files(sorted_files, keep = 3):
    """ Given a list of files sorted by last modified time and a number to 
        keep, delete the oldest ones. """
    delete = len(sorted_files) - keep
    for x in range(0, delete):
        print("Deleting: " + sorted_files[x][0])
        os.remove(sorted_files[x][0])

def delete(path):
    keep = 3

    file_paths = glob.glob(path)

    # Sort the files according to the last modification time.
    sorted_files = _sort_files_by_last_modified(file_paths)

    _delete_oldest_files(sorted_files, keep)
