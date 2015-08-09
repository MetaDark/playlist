import logging
import os
import subprocess
import sys

def main(argv):
    playlist_file = argv[0] if len(argv) > 0 else '.playlist'

    logging.basicConfig(level=logging.INFO)
    playlistPlay(playlist_file)

def playlistPlay(path):
    "Open a playlist file and start playing the unwatched items"

    with open(path, 'r+') as playlist_file:
        playlist = Playlist(playlist_file)

        for item in playlist.unwatched():
            if not item.play():
                raise SystemExit()

            sys.stdout.write("Continue playlist? [Y/n]: ")
            response = input().lower()
            if response == 'n' or response == 'no':
                raise SystemExit()

        logging.info("Finished playlist")
        playlist.reset();

class Playlist:
    def __init__(self, playlist_file):
        self.playlist_file = playlist_file

        lines = playlist_file.read().split("\n")
        self.items = [PlaylistItem(self, line) for line in lines if line]

    def __str__(self):
        return "\n".join([str(item) for item in self.items]) + "\n"

    def __iter__(self):
        return self.items.__iter__()

    def unwatched(self):
        return (item for item in self.items if not item.watched)

    def reset(self):
        for item in self.items:
            item.watched = False

        self.save()

    def save(self):
        self.playlist_file.seek(0)
        self.playlist_file.write(str(self))
        self.playlist_file.flush()

class PlaylistItem:
    def __init__(self, playlist, string):
        self.playlist = playlist

        result = string.split(" ", 1)
        self.watched = result[0] == "x"
        self.path = result[1].strip();

    def __str__(self):
        return " ".join(["x" if self.watched else "-", self.path])

    def play(self):
        logging.info('Playing: ' + self.path);

        file_ext = os.path.splitext(self.path)[1]
        if file_ext == 'playlist':
            playlistPlay(self.path)
        else:
            subprocess.call(["vlc", "--fullscreen", self.path, "vlc://quit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        sys.stdout.write("Did you finish watching? [Y/n]: ")
        response = input().lower()
        if not (response == 'n' or response == 'no'):
            self.watched = True
            self.playlist.save()
            return True

        return False

if __name__ == '__main__':
    main(sys.argv[1:])
