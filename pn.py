import os

folder = r"S:\library stuff\New folder\isekai life in another world\7.5"

files = sorted(os.listdir(folder))

for i, file in enumerate(files, start=1):
    old_path = os.path.join(folder, file)
    ext = os.path.splitext(file)[1]
    new_name = f"{i:03}{ext}"
    new_path = os.path.join(folder, new_name)

    os.rename(old_path, new_path)