import os

# Have to give parent folder it will turn zips into cbz for all zips in parent folder


folder = r"S:\library stuff\New folder\isekai life in another world"
for f in os.listdir(folder):
    if f.lower().endswith(".zip"):                  #convert from 
        old_path = os.path.join(folder, f)
        new_name = f[:-4] + ".cbz"                  #convert too
        new_path = os.path.join(folder, new_name)

        # safety check (prevents overwrite)
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"Renamed: {f} -> {new_name}")
        else:
            print(f"Skipped (already exists): {new_name}")