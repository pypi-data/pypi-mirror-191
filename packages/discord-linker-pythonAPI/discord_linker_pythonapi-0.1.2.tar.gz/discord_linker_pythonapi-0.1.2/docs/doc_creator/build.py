import os, subprocess, shutil


for i in os.listdir("../"):
    if i != 'doc_creator':
        f = f'../{i}'
        if os.path.isdir(f):
            shutil.rmtree(f)
        elif os.path.isfile(f):
            os.remove(f)

if os.name.lower() == "nt":
    commands:list[list[str]] = [
        ["make.bat", "clean"],
        ["sphinx-apidoc.exe", "--force", "-o", "./source/", "../../discord_linker_pythonAPI/"],
        ["make.bat", "html"],
    ]

else:
    commands:list[list[str]] = []

for i in commands:
    subprocess.check_call(i)


for i in os.listdir("build/html"):
    shutil.move(f"build/html/{i}", f"../{i}")

open('../.nojekyll', 'w').close()