import hashlib
import os
from pathlib import Path

from send2trash import send2trash
from tinytag import TinyTag


def find_duplicates():
    """Finds duplicate files in the given directory and deletes them."""

    ITUNES_MEDIA_PATH = input_validate_path("Enter path of iTunes music directory to clean: ")

    # Dictionary to store files and their hashes
    files = {}
    artist_files = {}
    deleted = 0
    
    for root, dirs, filenames in os.walk(ITUNES_MEDIA_PATH):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            
            # Get the artist name from the file path
            artist = os.path.join(ITUNES_MEDIA_PATH, TinyTag.get(file_path).artist)
            
            # Calculate the hash of the file
            file_hash = hashlib.sha1()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    file_hash.update(chunk)
            file_hash = file_hash.hexdigest()
            
            # Check if the file is a duplicate
            if file_hash in files:
                # Get the path of the original file
                # original_file = files[file_hash]
                original_artist = artist_files[file_hash]
                if artist == original_artist:
                    os.remove(file_path)
                    deleted += 1
                else:
                    files[file_hash] = file_path
                    artist_files[file_hash] = artist
            else:
                files[file_hash] = file_path
                artist_files[file_hash] = artist
    
    print(deleted, "duplicate files moved to trash.")


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
  find_duplicates()
