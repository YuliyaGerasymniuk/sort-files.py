import sys
import os
import shutil
from constants import map


def get_main_path():
    args = sys.argv
    if len(args) == 1:
        file_folder = input("Введіть шлях до папки: ")
    else:
        file_folder = args[1]
    while True:
        if not os.path.exists(file_folder):
            if file_folder:
                file_folder = input("Введіть шлях до папки: ")
        else:
            if os.path.isdir(file_folder):
                break
            else:
                print(f"{file_folder} не папка")
                file_folder = ""

    return file_folder


video_folder = ["avi", "mp4", "mov", "mkv", "gif"]
audio_folder = ["mp3", "ogg", "wav", "amr", "m4a", "wma"]
images_folder = ["jpeg", "png", "jpg", "svg"]
doc_folder = ["doc", "docx", "txt", "pdf", "xlsx", "pptx", "html", "scss", "css", "map"]
arch_folder = ["zip", "gz", "tar", "rar"]


def normalize(file):
    lists = file.split(".")
    name_file = ".".join(lists[:-1])
    new_name = ""
    for elem in name_file:
        if elem in map:
            new_name += map[elem]
        elif (ord("A") <= ord(elem) <= ord("Z")) or (ord("a") <= ord(elem) <= ord("z")) or elem.isdigit():
            new_name += elem
        else:
            new_name += "_"

    return new_name + "." + lists[-1]


def handling_file(file, file_path, path_main):
    video_path = os.path.join(path_main, "video")
    if not os.path.exists(video_path):
        os.makedirs(video_path)

    audio_path = os.path.join(path_main, "audio")
    if not os.path.exists(audio_path):
        os.makedirs(audio_path)

    images_path = os.path.join(path_main, "images")
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    documents_path = os.path.join(path_main, "documents")
    if not os.path.exists(documents_path):
        os.makedirs(documents_path)

    archives_path = os.path.join(path_main, "archives")
    if not os.path.exists(archives_path):
        os.makedirs(archives_path)

    file_name_divide = normalize(file).split(".")
    file_ending = ""
    if len(file_name_divide) > 1:
        file_ending = file_name_divide[-1]
    if not file_ending.lower():
        return None
    else:
        if file_ending in video_folder:
            new_path = os.path.join(video_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(video_path, normalize(file)))

        elif file_ending in audio_folder:
            new_path = os.path.join(audio_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(audio_path, normalize(file)))

        elif file_ending in images_folder:
            new_path = os.path.join(images_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(images_path, normalize(file)))

        elif file_ending in doc_folder:
            new_path = os.path.join(documents_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(documents_path, normalize(file)))

        elif file_ending in arch_folder:
            new_path = os.path.join(archives_path, file)

            try:
                shutil.unpack_archive(shutil.move(file_path, new_path),
                                      os.path.join(archives_path, normalize(file).rstrip(file_ending)))
            except shutil.ReadError:
                print(
                    f"архів {normalize(file)} не може розпакуватись.")
            finally:
                os.rename(os.path.join(archives_path, file), os.path.join(archives_path, normalize(file)), )

        else:
            os.replace(file_path, os.path.join(path_main, normalize(file)))
            return None


def around_dir():
    files = os.listdir(main_path)
    for file in files:
        file_path = os.path.join(main_path, file)
        if os.path.isfile(file_path):
            handling_file(file, file_path, main_path)
        else:
            around_dir()
            if not os.listdir(file_path):
                os.rmdir(file_path)
                continue


if __name__ == "__main__":
    main_path = get_main_path()
    around_dir()
