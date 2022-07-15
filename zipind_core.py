"""
    Create by: apenasrr
    Source: https://github.com/apenasrr/zipind
"""
import os
import subprocess
import sys

import natsort
import pandas as pd

from zipind_utils import get_folder_name_normalized, normalize_string, save_txt


def constant_store_expansion():
    """
    when packaging files and splitting them,
    the total package volume increases by 4096 bytes
    """

    return 4096


def extension_to_ignore(file, ignore_extensions):
    """check if file need to be ignored

    Args:
        file (str): file_path or file_name
        ignore_extensions (list): Extensions to ignore

    Returns:
        bol: True to ignore. False to not ignore.
    """

    file_lower = file.lower()
    if len(ignore_extensions) == 0:
        return False
    elif file_lower.endswith(tuple(ignore_extensions)):
        return True
    else:
        return False


def df_sort_human(df, column_name):
    """
    Sort files and folders in human way.
    So after folder/file '1' comes '2', instead of '10' and '11'.
    Simple yet flexible natural sorting in Python.
    When you try to sort a list of strings that contain numbers,
    the normal python sort algorithm sorts lexicographically,
    so you might not get the results that you expect:
    More info: https://github.com/SethMMorton/natsort

    :input: DataFrame. With columns [file_folder, file_name]
    :return: DataFrame. Sort in a human way by [file_folder, file_name]
    """

    def sort_human(list_):

        list_ = natsort.natsorted(list_)
        return list_

    def sort_df_column_from_list(df, column_name, sorter):
        """
        :input: df: DataFrame
        :input: column_name: String
        :input: sorter: List
        :return: DataFrame
        """

        sorterIndex = dict(zip(sorter, range(len(sorter))))
        df["order"] = df[column_name].map(sorterIndex)
        df.sort_values(["order"], ascending=[True], inplace=True)
        df.drop(["order", column_name], axis=1, inplace=True)
        return df

    list_path_file = df[column_name].tolist()
    sorter = sort_human(list_path_file)
    df = sort_df_column_from_list(df, column_name, sorter)
    return df


def get_list_all_videos_sort(path_dir, ignore_extensions=[]):
    """list all file sorted

    Args:
        path_dir (str): folder path
        ignore_extensions (list, optional): Extensions to ignore.
                                            Defaults to [''].

    Returns:
        list: sorted list of all files in folder
    """

    list_all_videos = []
    for root, _, files in os.walk(path_dir):
        for file in files:
            file_lower = file.lower()
            if extension_to_ignore(file_lower, ignore_extensions):
                continue
            path_file = os.path.join(root, file)
            list_all_videos.append(path_file)
    # natural sort
    #  normalize latin characters
    df = pd.DataFrame(list_all_videos, columns=["path_file"])
    df["path_file_norm"] = ""
    df["path_file_norm"] = df["path_file"].apply(normalize_string)

    #  process natsort
    df_sort = df_sort_human(df, "path_file_norm")
    list_all_videos_sort = df_sort["path_file"].to_list()
    return list_all_videos_sort


def create_archive_file_from_list_file(
    path_file_archive, list_files, max_size=None, mode="rar"
):

    if mode != "rar" and mode != "zip":
        print("Error: zip mode not identified")
        return

    if len(list_files) > 1:
        stringa = "\n\n".join(list_files)
        save_txt(stringa, "files_to_zip")
        file = "files_to_zip.txt"
        if mode == "rar":
            create_rar_file(path_file_archive, f"@{file}", max_size)
        else:
            create_zip_file(path_file_archive, f"@{file}", max_size)
        os.remove(file)

    else:
        path_file_list = list_files[0]
        if mode == "rar":
            create_rar_file(path_file_archive, f'"{path_file_list}"', max_size)
        else:
            create_zip_file(path_file_archive, f'"{path_file_list}"', max_size)


def create_rar_file(path_file_archive, path_origin, max_size=None):

    if max_size is None:
        str_max_size = ""
    else:
        # Adjustment required by WinRAR
        #  Define '1m' as 1 million bytes and not 1.048.576
        max_size = max_size * ((1024**2) / (10**6))
        # keep only 3 decimal to avoid bug in winrar api
        decimal_limit = 3
        max_size = int(max_size * (10**decimal_limit)) / (
            10**decimal_limit
        )

        str_max_size = str(max_size)

    # -ep0 -> preserve folders structure
    subprocess.call(
        '"%ProgramFiles%\\WinRAR\\Rar.exe" a -cfg- -ep0 -inul '
        + "-m0 -md4m -mt5 -r -s "
        + f'-v{str_max_size}M "{path_file_archive}" '
        + f"{path_origin}",
        shell=True,
    )


def get_sevenzip_caller():
    """Get str 7zip caller for CLI interface, by trying all possibles syntax
    Ref.: https://info.nrao.edu/computing/guide/file-access-and-archiving/7zip/7z-7za-command-line-guide

    Returns:
        str: 7zip caller for CLI interface
    """

    list_sevenzipcaller = ["7za", "7z"]
    for sevenzipcaller in list_sevenzipcaller:
        result = subprocess.Popen(
            [sevenzipcaller],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        if "Copyright" in str(result.communicate()[0]):
            return sevenzipcaller
    return ""


def create_zip_file(path_file_archive, path_origin, max_size=None):
    """
    Create zip file with 7-zip
    """

    seven_zip_app = get_sevenzip_caller()

    if max_size is None:
        str_max_size = ""
    else:
        str_max_size = str(max_size)

    # -scsUTF-16LE -> Define encoding as UTF16
    # -spf2 -> preserve folders structure
    # windows
    subprocess.call(
        f"{seven_zip_app} a -v{str_max_size}m -spf2 -mx0 "
        + f'"{path_file_archive}" '
        + f"{path_origin} -scsUTF-16LE",
        shell=True,
    )


def get_dict_tasks(
    path_dir,
    mb_per_file=999,
    path_dir_output=None,
    mode="rar",
    ignore_extensions=[],
):

    """
    Build a task list pack, separating files into size-limited groups.
    :input: path_dir: String. Folder path
    :input: mb_per_file: Integer. Max size of each rar file
    :input: path_dir_output: String. Folder path output
    :input: ignore_extensions: List. Extensions to ignore
    :return: Dict. keys: [mb_per_file, tasks]
                    tasks: list. List of lists.
                            [output_path_file, list_path_files]
    """

    abs_path_dir = os.path.abspath(path_dir)
    abs_path_dir_mother = os.path.dirname(abs_path_dir)
    dir_name_base = os.path.basename(abs_path_dir)

    # if destination folder is not specified,
    #  use the parent of the source folder
    if path_dir_output is None:
        archive_path_file_name_base = os.path.join(
            abs_path_dir_mother, dir_name_base
        )
    else:
        dir_name_base = get_folder_name_normalized(dir_name_base)
        archive_path_file_name_base = os.path.join(
            path_dir_output, dir_name_base
        )

    # set variables
    zip_file_no = 1
    bytesprocessed = 0
    bytesperfile = mb_per_file * (1024**2) - constant_store_expansion()

    rar_path_file_name = (
        f"{archive_path_file_name_base}-%03d.{mode}" % zip_file_no
    )
    list_path_files = []

    do_create_rar_by_list = False
    do_create_rar_by_single = False
    dict_tasks = {}
    dict_tasks["mb_per_file"] = mb_per_file
    list_task = []

    # build tasks to compress
    list_all_videos_sort = get_list_all_videos_sort(
        path_dir, ignore_extensions
    )

    for path_file in list_all_videos_sort:
        filebytes = os.path.getsize(path_file)

        # list_file it's about to get too big? compact before
        if bytesprocessed + filebytes > bytesperfile:

            do_create_rar_by_list = True
            do_create_rar_by_single = False
            if filebytes > bytesperfile:
                do_create_rar_by_single = True
                do_create_rar_by_list = False

        if do_create_rar_by_list:
            # make dir with files in list
            print(f"Destiny: {rar_path_file_name}\n")

            task = []
            task.append(rar_path_file_name)
            task.append(list_path_files)
            list_task.append(task)

            bytesprocessed = 0
            list_path_files = []
            do_create_rar_by_list = False

            # configure to next file rar
            zip_file_no += 1
            rar_path_file_name = (
                f"{archive_path_file_name_base}-%03d.{mode}" % zip_file_no
            )
            do_create_rar_by_single = False

            # add focus file to another list
            print(f"Add file {path_file}")
            list_path_files.append(path_file)
            bytesprocessed += filebytes

            # skip to another file
            continue

        if do_create_rar_by_single:
            if len(list_path_files) > 0:
                print(f"Destiny: {rar_path_file_name}\n")

                task = []
                task.append(rar_path_file_name)
                task.append(list_path_files)
                list_task.append(task)

                # Configure to next file rar
                zip_file_no += 1
                rar_path_file_name = (
                    f"{archive_path_file_name_base}-%03d.{mode}" % zip_file_no
                )
                bytesprocessed = 0
                list_path_files = []

            list_path_files = [path_file]

            task = []
            task.append(rar_path_file_name)
            task.append(list_path_files)
            list_task.append(task)

            # configure to next file rar
            zip_file_no += 1
            rar_path_file_name = (
                f"{archive_path_file_name_base}-%03d.{mode}" % zip_file_no
            )
            do_create_rar_by_single = False
            list_path_files = []
            # skip to another file
            continue

        # Case list not full and focus file is small
        # put file in list
        print(f"Add file {path_file}")
        list_path_files.append(path_file)
        bytesprocessed += filebytes

    #  in last file, if list was not empty
    if len(list_path_files) > 0:
        # make dir with files in list
        print(f"Creating... {rar_path_file_name}")

        task = []
        task.append(rar_path_file_name)
        task.append(list_path_files)
        list_task.append(task)

    # dict_tasks: object with tasks to compress
    dict_tasks["tasks"] = list_task
    return dict_tasks


def zipind(
    path_dir,
    mb_per_file=999,
    path_dir_output=None,
    mode="rar",
    ignore_extensions=[],
):
    """
    Compresses a folder into independent parts.
    Requirement: Have Winrar installed
    :input: path_dir: String. Folder path
    :input: mb_per_file: Integer. Max size of each rar file
    :input: path_dir_output: String. Folder path output
    :input: ignore_extensions: List. Extensions to ignore
    :return: None
    """

    # Creates grouped files for independent compression
    dict_tasks = get_dict_tasks(
        path_dir, mb_per_file, path_dir_output, mode, ignore_extensions
    )

    # Start Compression
    zipind_process(dict_tasks, mode)


def zipind_process(dict_tasks, mode="rar"):

    mb_per_file = dict_tasks["mb_per_file"]
    task_len = len(dict_tasks["tasks"])
    for index, task in enumerate(dict_tasks["tasks"]):
        rar_path_file_name = task[0]
        list_path_files = task[1]
        create_archive_file_from_list_file(
            rar_path_file_name, list_path_files, mb_per_file, mode
        )
        print(f"{index+1}/{task_len} - Done")
