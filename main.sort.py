# Desc: Program that sorts contents of directories into folders based on a filter file.
# Author: Nathan Gilbert
import shutil, os, sys


def check_directory(directory):
  return os.path.isdir(directory)


def check_file(file):
  return os.path.isfile(file)


def create_folders(main_folder, destination, filter_set):
  image_filetypes = ['tif', 'tiff', 'gif', 'jpeg', 'jpg', 'jif', 'jfif', 'jp2', 'jpx', 'j2k', 'j2c', 'fpx', 'pcd', 'png', 'ai', 'psd']
  document_filetypes = ['xls', 'doc', 'docx', 'pdf', 'txt', 'xlsx', 'xlsm', 'ppt', 'pps', 'pptx']
  audio_filetypes = ['mp3', 'aac', 'ac3', 'wav', 'wma', 'ogg', 'midi', 'mid', 'cda', 'aif']
  video_filetypes = ['mp4', 'h264', 'avi', 'mkv', 'mpeg', 'mpg', 'mov', 'm4v', 'flv', '3gp', 'wmv', 'vob']
  filetype_directories = ['Image files', 'Document files', 'Audio files', 'Video files', 'Misc files']
  main_directory = f'{destination}\{main_folder}'
  sub_directories = {}
  try:
    # Creates main parent folder at target directory
    os.makedirs(main_directory)
  except FileExistsError:
      print(f'{main_directory} already exists')
  finally:
    for name in filetype_directories:
      try:
        # Creates sub directories in main folder
        os.makedirs(f'{main_directory}\{name}')
      except FileExistsError:
        print(f'{main_directory}\{name} already exists')
  for file_type in filter_set:
    # Seperates the file types into their respective folder
    if file_type in image_filetypes:
      sub_directories[file_type] = create_subdirectory(
        main_directory, 'Image files', file_type
      )
    elif file_type in document_filetypes:
      sub_directories[file_type] = create_subdirectory(
          main_directory, 'Document files', file_type
      )
    elif file_type in audio_filetypes:
      sub_directories[file_type] = create_subdirectory(
        main_directory, 'Audio files', file_type
      )
    elif file_type in video_filetypes:
      sub_directories[file_type] = create_subdirectory(
        main_directory, 'Video files', file_type
      )
    else:
      sub_directories[file_type] = create_subdirectory(
        main_directory, 'Misc files', file_type
      )
  return sub_directories


def create_subdirectory(main_directory, sub_directory, file_type):
  try:
    file_type = file_type.upper()
    file_type_path = f'{main_directory}\{sub_directory}\{file_type}'
    # Creates folder at target directory for file type
    os.makedirs(file_type_path)
  except FileExistsError:
    print(f'{main_directory}\{sub_directory} files already exists')
  return file_type_path


def read_filter(filter):
  types = set()
  file = open(filter, 'r')
  for file_type in file:
    types.add(file_type.replace('\n', ''))
  return types


def make_filter():
  while True:
    types = input('Please enter all file types seperated by spaces: ')
    confirm = input(f'Does this look correct? y/n {types} |: ')
    if confirm.lower() == 'y':
      list_types = types.lower().split()
      break
  return set(list_types)


def vaild_inputs(main_folder, directory, destination, filter_path):
  for character in main_folder:
    if character == '_':
      pass
    elif not character.isalnum():
      print('Name of main folder is invalid')
      sys.exit()
  if destination is None:
    destination = directory
  # Checks that all inputs are valid
  if check_directory(directory):
    if filter_path is not None:
      if check_file(filter_path):
        pass
      else:
        print('File filter\'s path is invalid')
        sys.exit()
    if check_directory(destination):
      pass
    else:
      print('Destination path is invalid')
      sys.exit()
  else:
    print('Directory path is invalid')
    sys.exit()
  return destination


def main(main_folder, directory, destination=None, filter_path=None):
  destination = vaild_inputs(main_folder, directory, destination, filter_path)
  if filter_path is not None:
    file_filter = read_filter(filter_path)
  else:
    file_filter = make_filter()
  sub_directories = create_folders(main_folder, destination, file_filter)
  print(sub_directories)
  print('success')

  # for path, dirs, files in os.walk(source):
  #   print(path)
  #   for file in files:
  #     print(os.path.join(path, file))
  #     set.add(get_file_type(file))



if __name__ == '__main__':
  if len(sys.argv) == 3:
    main(*sys.argv[1:])
  elif len(sys.argv) == 4:
    # Check if destiation or filter_path is provided
    if check_directory(sys.argv[3]):
      main(*sys.argv[1:])
    else:
      main(sys.argv[1], sys.argv[2], None, sys.argv[3])
  elif len(sys.argv) == 5:
    main(*sys.argv[1:])
  else:
    print("Err")
