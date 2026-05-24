import subprocess

parent_dir = r"S:\library stuff\New folder\isekai life in another world"

ps_command = f'''
Get-ChildItem "{parent_dir}" -Directory | ForEach-Object {{
    Compress-Archive -Path $_.FullName -DestinationPath (Join-Path $_.Parent.FullName ($_.Name + ".zip")) -Force
}}
'''

result = subprocess.run(
    ["powershell", "-Command", ps_command],
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)