"""
Created by: apenasrr
Source: https://github.com/apenasrr/zipind

Compresses a folder into independent parts.
Works in hybrid mode:
- Compact folder dividing into independent parts, grouping your files in
    alphanumeric order.
- Respects the ordering of folders and files.
- Respects the internal structure of folders
- If any file is larger than the defined maximum size, the specific
    file is partitioned in dependent mode.

Do you wish to buy a coffee to say thanks?
LBC (from LBRY) digital Wallet
> bFmGgebff4kRfo5pXUTZrhAL3zW2GXwJSX

We recommend:
mises.org - Educate yourself about economic and political freedom
lbry.tv - Store files and videos on blockchain ensuring free speech
https://www.activism.net/cypherpunk/manifesto.html -  How encryption is essential to Free Speech and Privacy
"""
from __future__ import annotations

import os
from configparser import ConfigParser
from pathlib import Path

from .zipind_core import run
from .zipind_utils import (
    apply_recursive_in_folder,
    clean_cmd,
    ensure_folder_existence,
    sanitize_file_or_folder,
    test_folders_has_path_too_long,
)


def get_folder_script_path():

    folder_script_path_relative = os.path.dirname(__file__)
    folder_script_path = os.path.realpath(folder_script_path_relative)

    return folder_script_path


def get_config_data(path_file_config):
    """get default configuration data from file config.ini

    Returns:
        dict: config data
    """

    config_file = ConfigParser()
    config_file.read(path_file_config)
    default_config = dict(config_file["default"])
    return default_config


def config_update_data(path_file_config, variable_name, variable_value):

    config = ConfigParser()
    config.read(path_file_config)
    config.set("default", variable_name, variable_value)
    with open(path_file_config, "w+") as config_updated:
        config.write(config_updated)


def set_config_max_file_size(path_file_config, max_file_size):

    config_update_data(path_file_config, "file_size", str(max_file_size))


def ask_mb_file():

    mb_per_file = int(
        input("Type the maximum size per part in MB " + "(Ex.: 400): ")
    )

    return mb_per_file


def ask_path_folder_output():

    path_folder_output = input(
        "Paste the folder path where the compressed "
        + "files should be saved: \n"
    )
    ensure_folder_existence([path_folder_output])
    return path_folder_output


def define_path_folder_output(path_folder_output):

    if path_folder_output is not None:
        repeat_path_folder_output = input(
            f"\n{path_folder_output}\n"
            + "Compress files in the folder above? y/n\n"
        )
        if (
            repeat_path_folder_output != ""
            and repeat_path_folder_output != "y"
        ):
            path_folder_output = ask_path_folder_output()
    else:
        path_folder_output = ask_path_folder_output()

    ensure_folder_existence([path_folder_output])
    return path_folder_output


def define_mb_per_file(path_file_config, mb_per_file):

    if mb_per_file is not None:
        repeat_size = input(
            f"Compact in {mb_per_file} " + "MB per file? y/n\n"
        )
        if repeat_size == "n":
            mb_per_file = ask_mb_file()
            set_config_max_file_size(path_file_config, mb_per_file)
    else:
        mb_per_file = ask_mb_file()
        set_config_max_file_size(path_file_config, mb_per_file)

    return mb_per_file


def define_path_folder_input() -> Path:

    input_none = True
    while input_none:
        path_folder_input = Path(
            input("Paste the folder path to be compressed: ")
        )
        path_folder_input
        if not path_folder_input.is_dir():
            print("This folder not exist. Try again.\n")
            continue
        input_none = False
    return path_folder_input


def get_list_ignore_extensions(ignore_extensions):
    list_ignore_extensions = ignore_extensions.split(",")
    if len(list_ignore_extensions) == 1 and list_ignore_extensions[0] == "":
        list_ignore_extensions = []
    return list_ignore_extensions


def ensure_folder_sanitize(path_folder, max_path):

    # ensures that files/folders names are compatible with UTF-8
    apply_recursive_in_folder(sanitize_file_or_folder, path_folder)

    # ensures that the length of the Path_files are not so long
    _, list_folders_path_rejected = test_folders_has_path_too_long(
        [str(path_folder)], max_path
    )

    if list_folders_path_rejected:
        input("\nAfter correcting, press something to continue.\n")
        clean_cmd()
        return False
    else:
        return True


def get_folder_output_suggest(path_folder_input):

    folder_base_parh = os.path.dirname(path_folder_input)
    folder_name_zip = "zip_" + os.path.basename(path_folder_input)
    folder_output_suggest = os.path.join(folder_base_parh, folder_name_zip)
    return folder_output_suggest


def main():

    folder_script_path = get_folder_script_path()
    path_file_config = os.path.join(folder_script_path, "config.ini")

    config_data = get_config_data(path_file_config)
    mb_per_file = int(config_data["file_size"])
    mode = config_data["mode"]
    ignore_extensions = config_data["ignore_extensions"]
    list_ignore_extensions = get_list_ignore_extensions(ignore_extensions)
    max_path = int(config_data["max_path"])

    path_folder_output = config_data["dir_output"]
    if path_folder_output != "":
        ensure_folder_existence([path_folder_output])

    while True:
        print(
            "Zipind - From a folder, make a splitted ZIP with INDependent "
            + "parts\n>> github.com/apenasrr/zipind <<\n"
        )

        # ::. Configuration
        path_folder_input = define_path_folder_input()

        if ensure_folder_sanitize(path_folder_input, max_path) is False:
            continue

        if path_folder_output == "":
            path_folder_output = get_folder_output_suggest(path_folder_input)
        path_folder_output = define_path_folder_output(path_folder_output)
        mb_per_file = define_mb_per_file(path_file_config, mb_per_file)

        # ::. Start the partition operation
        run(
            path_folder_input,
            mb_per_file,
            path_folder_output,
            mode,
            list_ignore_extensions,
        )

        # ::. Repeat or Finish
        # Condition to repeat or end the script
        n_for_quit = input(
            "\nZipind successfully applied zip generating "
            + "independent parts.\n "
            + "Apply Zipind to another folder? y/n\n"
        )

        if n_for_quit == "n":
            return
        else:
            path_folder_output = ""
        # Clean cmd screen
        clean_cmd()


if __name__ == "__main__":
    main()
