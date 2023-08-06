import os
import sys
import time
from pathlib import Path

from send2trash import send2trash
from tinytag import TinyTag


def main() -> None:

  print("\nMake sure to backup your music directory before entering it into this script...\n")

  ITUNES_MEDIA_PATH = input_validate_path("Enter path of iTunes music directory to clean: ")

  duplicates = find_duplicates(ITUNES_MEDIA_PATH)
  DUPLICATES_TOTAL = len(duplicates)

  print(len(duplicates), "duplicate files detected in:", ITUNES_MEDIA_PATH)
  if(len(duplicates) == 0):
    return
  choice = input("Delete {} files? [y/n]: ".format(len(duplicates)))
  if(choice != "y"):
    print("Cancelled. Nothing deleted.")
    return

  dirs_to_delete = find_dirs_with_only_duplicate_files(duplicates)

  # don't track duplicate files for individual trashing that are already going to be trashed via their directory
  # this is for performance (and avoiding error) reasons with send2trash
  for dir in dirs_to_delete:
    files = os.listdir(dir)
    for f in files:
      f = os.path.join(dir, f)
      if(f in duplicates):
        duplicates.remove(f)

  send2trash(dirs_to_delete)
  send2trash(duplicates)

  log_output(dirs_to_delete, duplicates, DUPLICATES_TOTAL)


def log_output(dirs_to_delete, duplicates, DUPLICATES_TOTAL):

  print("Deleted", len(dirs_to_delete), "directories containing only duplicate files.")
  print("Deleted", len(duplicates), "individual files.")
  print("Deleted", DUPLICATES_TOTAL, "total duplicate files.")

  timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
  LOG = "deleted_duplicate_songs_{}.log".format(timestamp)
  old_stdout = sys.stdout

  with open(LOG, "w") as log_file:
    sys.stdout = log_file
    
    print(timestamp, "\n")
    
    # directories of files
    i = 1
    print("Deleted", len(dirs_to_delete), "directories containing only duplicate files.")
    for dir in dirs_to_delete:
      print(i, ":", dir)
      i += 1
    
    # individual files
    i = 1
    print("\nDeleted", len(duplicates), "individual files.")
    for f in duplicates:
      print(i, ":", Path(f).name)
      print(i, ":", "Path:", Path(f))
      i += 1

    print("\nDeleted", DUPLICATES_TOTAL, "total duplicate files.")

  sys.stdout = old_stdout
  print("Log output:", LOG)


def find_dirs_with_only_duplicate_files(duplicates: list[Path]) -> list[Path]:
  '''
  Determine which directories only have duplicates in them
  in order to delete both the directory and the file.
  '''
  dirs_with_duplicates = []
  for f in duplicates:
    if(Path(f).parent not in dirs_with_duplicates):
      dirs_with_duplicates.append(Path(f).parent)

  dirs_to_delete = []
  for dir in dirs_with_duplicates:
    files = os.listdir(dir)

    containing_duplicates = []
    for f in files:
      if(os.path.join(dir, f) not in duplicates):
        containing_duplicates.append(False)
        break
      else:
        containing_duplicates.append(True)

    if(False not in containing_duplicates):
      dirs_to_delete.append(dir)
  
  return dirs_to_delete


def find_duplicates(dir) -> list[str]:
    """Finds duplicate files in the given directory and deletes them."""
    # Dictionary to store files and their metadata
    files = {}
    duplicates = []
    
    for root, dirs, filenames in os.walk(dir):
        # sort by shortest filename in order to put non duplicated files first
        filenames.sort(key=lambda x: x, reverse=True)
        for filename in filenames:
            file_path = os.path.join(root, filename)
            
            # Get the artist name and song title from the file metadata
            tags = TinyTag.get(file_path)
            artist = tags.artist
            title = tags.title
            
            # Check if the file is a duplicate
            if(artist, title) in files:
                # Get the path of the original file
                # original_file = files[(artist, title)]
                duplicates.append(file_path)
            else:
                files[(artist, title)] = file_path
    
    return duplicates


def input_validate_path(message_and_user_input: str, prefix="", postfix="", no_cwd=False) -> Path:
  '''
  Take user input and validates if it's a valid path.
  prefix and postfix surround message_and_user_input. This is useful for modifying the user input on the fly.
  Keep asking for input if it's an invalid path.
  Return a Path object of a valid string.
  '''
  input_path = input(message_and_user_input)
  try:
      custom_plugin_path = Path(os.path.join(prefix, input_path, postfix))
  except:
      print("Invalid path!")
      return input_validate_path(message_and_user_input, prefix, postfix, no_cwd)

  if(no_cwd and (str(input_path) == '.' or str(input_path) == "")):
    print("Invalid relative path to current directory!")
    return input_validate_path(message_and_user_input, prefix, postfix, no_cwd)
  
  if(not custom_plugin_path.exists()):
    print("Invalid path: {}".format(custom_plugin_path))
    return input_validate_path(message_and_user_input, prefix, postfix, no_cwd)
  return custom_plugin_path


if(__name__ == "__main__"):
  main()
