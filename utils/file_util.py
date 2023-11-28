import os
import pathlib
from pathlib import Path
import json


class FilesUtility():
    user_file_path: str = "data"
    user_file_name: str = ""
    user_file_ext: str = ""
    image_dir: str = ""
    is_break: bool = False
    image_prefix: str = 'save_'
    image_ext: str = '.png'
    excel_ext: str = '.xlsx'
    jd_path: str = "data/jd"
    resumes_path: str = "data/resumes"
    jd_save_path: str = "processed/jd"
    resumes_save_path: str = "processed/resumes"
    processed_save_path: str = "data/processed"

    def __init__(self) -> None:
        pass


def create_directory(file_path, directory_name):
    path = Path(file_path)
    if check_if_file(path):
        path = path.parent

    str_path = str(path)
    images_path = directory_name + '/'

    if not str_path.endswith("/"):
        p = Path(str_path + '/' + images_path)
    else:
        p = Path(str_path + images_path)

    p.mkdir(exist_ok=True)


def check_if_file(path):
    return path.is_file()


def create_dirs():
    p = pathlib.Path('')
    p.mkdir(parents=True, exist_ok=True)
    pass


def get_folder_path():
    pass


def load_jsonl(path):
    data = []
    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            data.append(json.loads(line))
    return data


def delete_images(images_len, path):
    for i in range(images_len):
        os.remove(path)


def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")


def delete_directory(path, directory):
    try:
        os.rmdir(path)
        print("Directory '% s' has been removed successfully" % directory)
    except OSError as error:
        print(error)
        print("Directory '% s' can not be removed" % directory)


def get_user_input():
    return input("Enter File Path : ")
