import os

folder_path = '/home/root/screenly_assets/'

for filename in os.listdir(folder_path):
    if filename.endswith(".tmp"):
        os.remove(os.path.join(folder_path, filename))
