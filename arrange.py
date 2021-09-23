#!/usr/bin/env python3
from os import listdir
from os.path import isfile, expanduser
from argparse import ArgumentParser
from sys import exit

from engine.DIR.DIR import DIR
from engine.Extensions.Extensions import Extensions
from engine.File.File import File

parser = ArgumentParser(description='Arrange the given directory')
parser.add_argument('-d', '--dir', help='For specifying a directory')

parser.add_argument('-ae', '--add_ext',
                    help='add a hyphen separated list of filetypes to a directory (specified using -d)')
parser.add_argument('-re', '--remove_ext',
                    help='Omit a hyphen separated list of filetypes from being cleaned (specified using -d)')
parser.add_argument('-r', '--remove_directory',
                    help='Omit the given directory having filetypes added to')
parser.add_argument('-c', '--clean_directory',
                    help='Clean the given directory')

args = parser.parse_args()

home = expanduser('~')
json_file_path = f'{home}/.config/arrange.json'
ext = Extensions(json_file_path)


def main():
    global args

    if not isfile(json_file_path):
        setup_json()

    if args.add_ext:
        if args.dir:
            directory, extensions_set = setup(args.dir, args.add_ext)

            ext.add_extensions(directory, extensions_set)
            ext.write_json_file()
        else:
            print('Specify directory using -d argument')
            exit()
    elif args.remove_ext:
        if args.dir:
            directory, extensions_set = setup(args.dir, args.remove_ext)

            ext.remove_extensions(directory, extensions_set)
            ext.write_json_file()
        else:
            print('Specify directory using -d argument')
            exit()
    elif args.remove_directory:
        directory = setup_dir(args.remove_directory)

        ext.remove_directory(directory)
        ext.write_json_file()
    elif args.clean_directory:
        directory = setup_dir(args.clean_directory)

        clean_directory(directory)
    else:
        clean_directory(f'{home}/Downloads')


def setup_json():
    print("This is the first time for the program to run...")
    print("adding extensions to json file...")
    ext.add_extensions(DIR(f'{home}/Pictures'), {'jpg', 'jpeg', 'png', 'gif'})
    ext.add_extensions(DIR(f'{home}/Documents'), {'doc', 'docx', 'pdf', 'csv', 'xlsx'})
    ext.add_extensions(DIR(f'{home}/Videos'), {'mp4', 'mkv'})
    ext.add_extensions(DIR(f'{home}/Music'), {'mp3'})
    ext.write_json_file()
    print("done!")
    print('Cleaning your Downloads folder...')
    clean_directory(f'{home}/Downloads')
    print('DONE')


def clean_directory(directory):
    for file in listdir(directory):
        file = f'{directory}/{file}'
        file = File(file, json_file_path)
        file.main()


def setup(directory, extensions):
    directory = setup_dir(directory)
    extensions_set = setup_extensions_set(extensions)
    return directory, extensions_set


def setup_extensions_set(extensions):
    extensions = extensions.split('-')
    return set(extensions)


def setup_dir(directory):
    directory = DIR(directory)
    directory.create_directory()
    return directory


if __name__ == '__main__':
    main()
