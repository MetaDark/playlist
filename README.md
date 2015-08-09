# Playlist
Keep track of watched items in a list of media files

## Getting Started

### Requirements
- Python 3
- VLC (2.2+ recommended for resuming playback)

Support for more media players will be added in the future

### Generate a playlist file
To get started you will need to create the playlist file. You can create it manually, but I find it easier to just generate a playlist using the linux find command:

    find . -iname <PATTERN> -exec echo '-' {} \; | sort > .playlist

### Start the playlist
Once you have the playlist file generated, run the python script in the same directory and VLC will start the playlist from where you last left off.

    python playlist.py

Note: You will be asked if you completed the video after VLC is closed and will be prompted to continue the playlist.

## File Specification
The file specification is very simple, each line contains the watched status followed by the path of the media file.

    [x/-] [filepath]

### Example:
    x ./Fringe S01E01 Pilot.mp4
    x ./Fringe S01E02 The Same Old Story.mp4
    x ./Fringe S01E03 The Ghost Network.mp4
    x ./Fringe S01E04 The Arrival.mp4
    x ./Fringe S01E05 Power Hungry.mp4
    x ./Fringe S01E06 The Cure.mp4
    x ./Fringe S01E07 In Which We Meet Mr .Jones.mp4
    x ./Fringe S01E08 The Equation.mp4
    x ./Fringe S01E09 The Dreamscape.mp4
    x ./Fringe S01E10 Safe.mp4
    x ./Fringe S01E11 Bound.mp4
    x ./Fringe S01E12 The No-Brainer.mp4
    x ./Fringe S01E13 The Transformation.mp4
    - ./Fringe S01E14 Ability.mp4
    - ./Fringe S01E15 Inner Child.mp4
    - ./Fringe S01E16 Unleashed.mp4
    - ./Fringe S01E17 Bad Dreams.mp4
    - ./Fringe S01E18 Midnight.mp4
    - ./Fringe S01E19 The Road Not Taken.mp4
    - ./Fringe S01E20 There's More Than One Of Everything.mp4
