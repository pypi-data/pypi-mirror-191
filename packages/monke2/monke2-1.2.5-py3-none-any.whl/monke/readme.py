import functions, pathlib, os, shutil

base_dir = os.getcwd()
dir = pathlib.Path(functions.__file__).resolve().parent
source_path = f'{dir}\\README.txt.py'
destination_path = f'{base_dir}\\README.txt'
shutil.copy(source_path, destination_path)

print('Readme file copied')