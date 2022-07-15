"""
    Command line interface for zipind.py

    Created by: apenasrr
    Source: https://github.com/apenasrr/zipind
"""
import os
import sys
import click

path_folder_src = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.abspath(os.path.join(__file__, path_folder_src))
sys.path.append(lib_path)

import zipind


@click.command()
@click.argument('folder_input', type=click.STRING)
@click.option('-s', '--size', 'mb_per_file',
              default=100,
              type=click.INT,
              help='Size of each part in MegaBytes')
@click.option('-m', '--mode', 'mode',
              default='rar',
              type=click.Choice(['zip', 'rar']),
              help='File archive extension')
@click.option('-i', '--ignore', 'list_ignore_extensions',
              default='',
              help='List of extensions to ignore, separated by comma. ' +
                   'e.g.: mp4,avi')
@click.argument('folder_output', type=click.STRING)
def main(folder_input,
         mb_per_file,
         mode,
         list_ignore_extensions,
         folder_output):
    """
    Zipind - From a folder, make a splitted ZIP with INDependent parts

    DIR: Directory path to archive
    """

    path_dir_input = folder_input
    path_dir_output = folder_output
    if list_ignore_extensions:
        list_ignore_extensions = (list_ignore_extensions
                                  .replace(' ', '')
                                  .split(','))

    zipind.zipind(path_dir_input, mb_per_file, path_dir_output,
                  mode, list_ignore_extensions)


if __name__ == '__main__':
    main()
