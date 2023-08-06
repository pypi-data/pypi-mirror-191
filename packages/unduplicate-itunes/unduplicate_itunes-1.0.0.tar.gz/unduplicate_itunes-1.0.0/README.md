# unduplicate-itunes
Moves duplicate song files from your itunes directory to the trash.

Given that iTunes doesn't automatically remove missing songs (that you have deleted because they are duplicates), you will still need to manually remove the missing song entries from iTunes itself.

## Behavior
* Directories (usually albums folders) that only contain duplicate files will be moved to the trash.
* A log file of all actions is output once the script finishes.

## Install
```
pip install unduplicate-itunes
```
## Usage
Just run [remove_by_artist_and_title.py](/unduplicate_itunes/remove_by_artist_and_title.py) and follow the prompts.

There are other scripts included that try to find duplicate by other methods but they are unfinished.
