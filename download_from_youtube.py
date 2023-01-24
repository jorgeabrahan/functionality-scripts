from pytube import YouTube, Playlist
import os


def ask_for_option(toAskFor, options):
    repeat = True
    while repeat:
        print(toAskFor)
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")
        try:
            selected = int(input("Select the option writing the number: "))
            repeat = selected > len(options) or selected < 1
            if repeat:
                print("Select a valid option")
            else:
                print("")
                return [selected, options[selected - 1]]
        except ValueError:
            print("The option selected should be a number")


def get_file(to_download, format):
    if format == 1:
        return to_download.streams.filter(only_audio=True).first()
    return to_download.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()


def get_files(to_download, format, type):
    files = []
    if type == 1:
        files.append(get_file(to_download, format))
    else:
        for video in to_download.videos:
            files.append(get_file(video, format))
    return files


def get_path(folder, title, type_num):
    def_path = f".\\{folder}"
    # if it is a playlist then create a folder with its name
    if type_num == 2:
        def_path += f"\\{title}"

    print(f"Default path: {def_path} (where \".\\\" means current folder)")
    return input("Enter the path to save the files (leave it blank for the default path): ") or def_path


def set_file_extension(format, full_path):
    if format == 1:
        return f"{full_path}.mp3"
    return f"{full_path}.mp4"


def format_default_name(def_name):
    return def_name.strip().replace("-", "").replace(" ", "_").replace("__", "_").lower()


def get_path_with_new_name(path):
    path_arr = path.split("\\")
    default_name = format_default_name(str(path_arr[len(path_arr) - 1]))
    path_without_file_name = path_arr[:-1]
    while True:
        print(f"Default file name: {default_name}")
        file_name = input(
            'Enter the file name (leave it blank for the default name): ') or default_name
        path_without_file_name.append(file_name)
        full_path = "\\".join(path_without_file_name)
        if os.path.exists(full_path):
            path_without_file_name.pop()
            print(file_name + " already exists")
        else:
            return [full_path, file_name]


def rename_file(out_file, format):
    # path of the file to rename without the extension
    path, ext = os.path.splitext(out_file)
    full_path, file_name = get_path_with_new_name(path)
    new_file = set_file_extension(format, full_path)
    os.rename(out_file, new_file)
    return file_name


def download_from_youtube():
    try:
        print("")
        type_num, type_str = ask_for_option(
            "What do you want to download?", ["Video", "Playlist"])
        url = ""
        while len(url) == 0:
            url = input(f"{type_str} URL: ")
        print("")

        to_download = YouTube(url) if type_num == 1 else Playlist(url)

        format, folder = ask_for_option(
            "What format do you want?", ["Audio", "Video"])

        files = get_files(to_download, format, type_num)
        path = get_path(folder, to_download.title, type_num)
        print("")
        for file in files:
            out_file = file.download(output_path=path)
            file_name = rename_file(out_file, format)
            print(file_name + " has been successfully downloaded\n")
    except FileExistsError:
        print(to_download.title + " already exists")

