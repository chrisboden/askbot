from pathlib import Path

# Create a Path object representing the current working directory
cwd = Path.cwd()
print(cwd)  # prints something like '/home/user/myproject'

# Create a Path object representing a subdirectory of the current working directory
subdir = cwd / 'data'
print(subdir)  # prints something like '/home/user/myproject/subdir'

# Check if the subdirectory exists
if subdir.exists():
  print('Subdirectory exists')
else:
  print('Subdirectory does not exist')

# Join two paths to create a new path
file_path = subdir / 'myfile.txt'
print(file_path)  # prints something like '/home/user/myproject/subdir/myfile.txt'

# Check if the file exists
if file_path.exists():
  print('File exists')
else:
  print('File does not exist')

# Read the contents of the file
with open(file_path, 'r') as f:
  contents = f.read()
  print(contents)
