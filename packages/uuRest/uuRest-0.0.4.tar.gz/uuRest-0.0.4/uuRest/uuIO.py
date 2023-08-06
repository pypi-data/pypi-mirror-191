import os
import json
from pathlib import Path
from typing import List, Dict


def dict_to_str(value: dict, encoding: str = "utf-8") -> str:
    """
    Converts dict to str
    :param value:
    :param encoding:
    :return:
    """
    return json.dumps(value, indent=4, ensure_ascii=False)


def load_json(filename: str, encoding: str = "utf-8") -> json:
    """
    Nacte json ze souboru
    :param filename: cesta k souboru v json formatu
    :param encoding:
    :return: vrati instanci json tridy
    """
    with open(filename, "r", encoding=encoding) as file:
        return json.load(file)


def save_json(value_json: json or dict, filename: str, encoding: str = "utf-8") -> None:
    """
    Ulozi json do souboru
    :param value_json: json
    :param filename: cesta k souboru
     :param encoding:
    :return:
    """
    with open(filename, "w", encoding=encoding) as file:
        json.dump(value_json, file, indent=4, ensure_ascii=False)


def load_textfile(filename: str, encoding=None) -> str:
    """
    Nacte text ze souboru
    :param filename: nazev souboru
    :param encoding:
    :return:
    """
    with open(filename, "r", encoding=encoding) as file:
        return file.read()


def save_textfile(value: str, filename: str, encoding=None) -> None:
    """
    Ulozi text do souboru
    :param value:
    :param filename:
    :param encoding:
    :return:
    """
    with open(filename, "w", encoding=encoding) as file:
        file.write(value)


# def copy_file(source_filename: str, destination_filename_or_directory: str) -> None:
#     """
#     Zkopiruje soubor ze zdrojove cesty do cilove cesty
#     :param source_filename:
#     :param destination_filename_or_directory:
#     :return:
#     """
#     copy2(source_filename, destination_filename_or_directory)


# def copy_folder(src: str, dst: str, symlinks=False, ignore=None):
#     """
#     Zkopiruje adresar vcetne souboru ze zdrojove cesty do cilove
#     :param src:
#     :param dst:
#     :param symlinks:
#     :param ignore:
#     :return:
#     """
#     create_folder_structure(Path(dst))
#     for item in os.listdir(src):
#         s = os.path.join(src, item)
#         d = os.path.join(dst, item)
#         if os.path.isdir(s):
#             copytree(s, d, symlinks, ignore)
#         else:
#             copy2(s, d)


def create_folder_structure(directory: Path) -> None:
    if not directory.exists():
        directory.mkdir(parents=True)


def test_if_two_files_are_equal(filename1: str, filename2: str, encoding=None) -> bool:
    """
    Overi jestli jsou dva soubory stejne, nebo ne
    :param filename1:
    :param filename2:
    :param encoding:
    :return:
    """
    if not os.path.exists(filename1):
        return False
    if not os.path.exists(filename2):
        return False
    s1 = load_textfile(filename=filename1, encoding=encoding)
    s2 = load_textfile(filename=filename2, encoding=encoding)
    return s1 == s2


# def get_text_by_xpath(xml: ET, value: str, default: str = None) -> str:
#     element = xml.find(value)
#     if element is None:
#         return default
#     else:
#         return element.text


def search_folder(path: str, recursive: bool = True, list_of_extensions: List[str] = None,
                  filename_must_not_start_with: str = None, filename_must_start_with: str = None) -> List[str]:
    """
    Prohleda adresar a najde v nem vsechny soubor a slozky
    :param path:
    :param recursive:
    :param list_of_extensions:
    :return: vrati seznam souboru a seznam slozek
    :param filename_must_not_start_with:
    :param filename_must_start_with:
    """
    # ziska seznam vsech souboru a podadresaru v aktualni slozce
    list_of_files = []
    try:
        list_of_files = os.listdir(path)
    except PermissionError:
        pass
    all_files = []
    all_folders = []
    # pokud neni seznam pripon prazdny, tak jej prevede do lowercase a zabezpeci, ze pripona obsahuje tecku
    if list_of_extensions is not None:
        list_of_extensions = [(extension.lower() if extension.startswith(".") else f".{extension.lower()}") for extension in list_of_extensions]
    # projde vsechny nalezene soubory a podadresare
    for filename in list_of_files:
        # ziska uplny nazev cesty
        full_path = os.path.join(path, filename)
        # pokud se jedna o slozku, prida ji do seznamu slozek
        if os.path.isdir(full_path):
            all_folders.append(full_path)
            # pokud se ma prohledavat rekurzivne, tak slozku prohleda
            if recursive:
                recursive_files, recursive_folders = search_folder(full_path, recursive, list_of_extensions, filename_must_not_start_with, filename_must_start_with)
                all_files += recursive_files
                all_folders += recursive_folders
        # pokud se jedna o soubor tak jej prida do seznamu
        else:
            filename, extension = os.path.splitext(full_path)
            basename = os.path.basename(full_path)
            if ((list_of_extensions is None) or (extension.lower() in list_of_extensions)) and \
                    ((filename_must_not_start_with is None) or (basename.startswith(filename_must_not_start_with) is False)) and \
                    ((filename_must_start_with is None) or (basename.startswith(filename_must_start_with) is True)):
                all_files.append(full_path)
    # vrati vysledek
    return all_files, all_folders


def clear_folder(path: str, recursive: bool = True, list_of_extensions: List[str] = None, filename_must_not_start_with: str = None) -> None:
    """
    Removes everything inside a folder including subfolders and files if the recursive parameter is set to true
    but the main folder will not be deleted
    :param path: path of the main folder which will be cleared
    :param recursive: indicator if subfolders needs to be deleted as well
    :param list_of_extensions: list of extensions of file which will be deleted. If list of extensions is None then all files will be deleted
    :param filename_must_not_start_with: If filename starts with specific prefix then it will not be deleted
    :return:
    """
    if os.path.exists(path):
        files, directories = search_folder(path, recursive=recursive, list_of_extensions=list_of_extensions, filename_must_not_start_with=filename_must_not_start_with)
        for file in files:
            os.remove(file)
        if recursive:
            for directory in directories:
                os.rmdir(directory)


def delete_folder(path: str) -> None:
    """
    Deletes entire folder including subfolders and files
    :param path:
    :return:
    """
    if os.path.exists(path):
        clear_folder(path)
        os.rmdir(path)


def delete_file(filename: str) -> None:
    """
    Deletes file
    :param filename:
    :return:
    """
    os.remove(filename)
