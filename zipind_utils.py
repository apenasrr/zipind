"""
    Create by: apenasrr
    Source: https://github.com/apenasrr/zipind
"""
import os
import unidecode
import sys


def clean_cmd():

    if sys.platform == 'win32':
        os.system('cls')
    elif sys.platform == 'linux':
        os.system('clear')
    else:
        print('OS not supported')
        sys.exit()


def save_txt(str_content, str_name):

    # UTF-8 can't handle with the follow caracter in a folder name: 
    text_file = open(f"{str_name}.txt", "w", encoding='utf_16')
    text_file.write(str_content)
    text_file.close()


def ensure_folder_existence(folders_path):

    for folder_path in folders_path:
        existence = os.path.isdir(folder_path)
        if existence is False:
            os.mkdir(folder_path)


def normalize_string(string_actual):

    string_new = unidecode.unidecode(string_actual)

    return string_new


def normalize_string_to_link(string_actual):

    string_new = unidecode.unidecode(string_actual)

    for c in r"!@#$%^&*()[]{};:,./<>?\|`~-=_+":
        string_new = string_new.translate({ord(c): "_"})

    string_new = string_new.replace(' ', '_')
    string_new = string_new.replace('___', '_')
    string_new = string_new.replace('__', '_')

    return string_new


def get_folder_name_normalized(path_dir):

    dir_name = os.path.basename(path_dir)
    dir_name_normalize = normalize_string_to_link(dir_name)

    return dir_name_normalize


def test_folders_has_path_too_long(list_path_folder, max_path=260):
    """tests a serie of folders if any of them has files whose pathfile
    has a larger length than stipulated in max_path

    Args:
        list_path_folder (list): list of path_folder to be tested
        max_path (int, optional): max pathfile len permitted. Defaults to 260.

    Returns:
        list: [list_folders_path_approved: less than max_path
               list_folders_path_rejected: bigger than max_path]
    """

    list_folders_path_approved = []
    list_folders_path_rejected = []

    for path_folder in list_path_folder:
        dict_result_test_pathfile_too_long = \
            test_folder_has_pathfile_too_long(path_folder, max_path)
        if dict_result_test_pathfile_too_long['result']:
            list_folders_path_approved.append(path_folder)
        else:
            show_alert_pathfile_too_long(dict_result_test_pathfile_too_long)

            list_folders_path_rejected.append(path_folder)

    return list_folders_path_approved, list_folders_path_rejected


def test_folder_has_pathfile_too_long(path_folder, max_path=260):
    """Test if a folder has any file with pathfile too long

    Args:
        path_folder (string):
    return:
        dict: keys: {result: bol, list_path_file_long: list}
    """

    list_path_file_long = []
    return_dict = {}
    return_dict['result'] = True

    for root, _, files in os.walk(path_folder):
        for file in files:
            file_path = os.path.join(root, file)
            len_file_path = len(file_path)
            if len_file_path > max_path:
                list_path_file_long.append(file_path)

    if len(list_path_file_long) != 0:
        return_dict['result'] = False

    return_dict['list_path_file_long'] = list_path_file_long
    return return_dict


def show_alert_pathfile_too_long(dict_result_test_pathfile_too_long):

    return_ = dict_result_test_pathfile_too_long
    if return_['result'] is False:
        print("Path file too long:")
        for path_file_long in return_['list_path_file_long']:
            print('- ' + path_file_long)
    print('')
