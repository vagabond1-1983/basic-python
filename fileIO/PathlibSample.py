from pathlib import Path

cmd = Path.cwd()
print(cmd)

sample_file = Path.joinpath(cmd, "sample.txt")
print(str(sample_file))
print(sample_file.exists())

print("---\nfind all sub directories")
for child in cmd.iterdir():
    if child.is_dir():
        print(child)

main_pyfile = Path.joinpath(cmd, "main.py")
print(
    f"""---\nmore details for main.py
name: {main_pyfile.name}
suffix: {main_pyfile.suffix}
size: {str(main_pyfile.stat().st_size)}
"""
)
