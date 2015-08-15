#!/usr/bin/env python

import logging
import os
import subprocess
import sys

PLAYLIST_EXTENSION = '.playlist'

def main(argv):
    playlist_file = argv[0] if len(argv) > 0 else PLAYLIST_EXTENSION

    logging.basicConfig(level=logging.INFO)
    playlist_play(playlist_file)

def playlist_play(path):
    "Open a playlist file and start playing the unwatched items"

    completed = False
    with open(path, 'r+') as playlist_file:
        playlist = Playlist(playlist_file)

        continue_playlist = True
        while continue_playlist:
            try:
                item = next(playlist)
                if item.play():
                    item.complete()
                    continue_playlist = prompt_yes_no("Continue playlist?")
                else:
                    continue_playlist = False
            except StopIteration:
                if prompt_yes_no("Finished playlist, restart?"):
                    playlist.reset()
                else:
                    completed = True
                    continue_playlist = False

    return completed

def vlc_play(path):
    "Play a file using vlc"

    print(path)
    subprocess.call(["vlc", "--fullscreen", path, "vlc://quit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return prompt_yes_no("Did you finish watching?")

def prompt_yes_no(prompt):
    "Prompt the user a yes/no question, default to yes"

    sys.stdout.write(prompt + " [Y/n]: ")
    response = input().lower()

    return not (response == 'n' or response == 'no')

class Playlist:
    def __init__(self, playlist_file):
        self.playlist_file = playlist_file

        lines = playlist_file.read().split("\n")
        self.items = [PlaylistItem(self, line) for line in lines if line]

    def __str__(self):
        return "\n".join([str(item) for item in self.items]) + "\n"

    def __iter__(self):
        return self

    def __next__(self):
        return next((item for item in self.items if not item.watched))

    def reset(self):
        for item in self.items:
            item.watched = False

        self.save()

    def save(self):
        self.playlist_file.seek(0)
        self.playlist_file.write(str(self))
        self.playlist_file.flush()

    def resolve_path(self, path):
        relative_dir = os.path.dirname(self.playlist_file.name)
        return os.path.abspath(os.path.join(relative_dir, path))

class PlaylistItem:
    def __init__(self, playlist, string):
        self.playlist = playlist

        result = string.split(" ", 1)
        self.watched = result[0] == "x"
        self.path = result[1].strip();

    def __str__(self):
        return " ".join(["x" if self.watched else "-", self.path])

    def play(self):
        path = self.playlist.resolve_path(self.path)
        basename = os.path.basename(path)
        extension = os.path.splitext(basename)[1]

        logging.info('Playing: ' + path);
        if basename == PLAYLIST_EXTENSION or extension == PLAYLIST_EXTENSION:
            return playlist_play(path)
        else:
            return vlc_play(path)

    def complete(self):
        self.watched = True
        self.playlist.save()

if __name__ == '__main__':
    main(sys.argv[1:])
