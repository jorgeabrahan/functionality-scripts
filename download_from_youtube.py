import yt_dlp
import os
import re

# This file downloads videos or playlists from youtube as audio or video depending on selection and stores
# the files in a folder called: Audio or Video depending on the selected option

def ask_for_option(to_ask_for, options):
    repeat = True
    while repeat:
        print(to_ask_for)
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")
        try:
            selected = int(input("Select the option writing the number: "))
            repeat = selected > len(options) or selected < 1
            if repeat:
                print("Select a valid option!")
            else:
                print("")
                return [selected, options[selected - 1]]
        except ValueError:
            print("The option selected should be a number")


def rename_files(option_str):
    # rename all files once they've been downloaded
    for filename in os.listdir(option_str):
        if '_' not in filename: # if the file hasnt been renamed before
            filepath = os.path.join(option_str, filename)
            if os.path.isfile(filepath): # if the file exists
                name, ext = os.path.splitext(filename) # get file name and extension
                name_parts = name.rsplit(' ', 1) # split name in case it has an auto generated id
                if len(name_parts) == 2:
                    name, video_id = name_parts
                    video_id = f"_{video_id}" # if theres a video id get it
                else:
                    video_id = "" # otherwise video id will be an empty string
                name = name.strip() # trim or remove empty or white spaces at the end and beginning of name
                name = re.sub(r'[-,]', '', name)  # remove all special characters (- and ,)
                name = re.sub(r'\s+', '_', name)  # replace all whitespace characters with '_'
                name = name.lower()
                new_filename = f"{name}{video_id}{ext}"
                new_filepath = os.path.join(option_str, new_filename)
                os.rename(filepath, new_filepath) # rename the file

def get_ydl_opts(option_num, option_str):
    if option_num == 1:
        download_format = 'bestaudio[ext=mp3]/bestaudio'
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }] # after downloading the audio file it makes sure that it has the preferred codec and quality
    else:
        download_format = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        postprocessors = []
    return {
        'format': download_format,
         'outtmpl': f'{option_str}/%(title)s.%(ext)s',
         'postprocessors': postprocessors
    }


def download_from_youtube():
    url = ""
    while len(url) == 0:
        url = input("Playlist or Video URL: ") # get url to download
    option_num, option_str = ask_for_option("Format?", ["Audio", "Video"])

    # download video or videos (in case of playlist)
    with yt_dlp.YoutubeDL(get_ydl_opts(option_num, option_str)) as ydl:
        ydl.download(url)
    # rename all downloaded files
    rename_files(option_str)
