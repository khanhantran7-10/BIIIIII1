import zipfile
import os

files_to_pack = [
    "index.html",
    "server.py",
    "report_generator.py",
    "vercel.json",
    "requirements.txt",
    "README.md",
    ".gitignore",
    "api/index.py",
    "api/report_generator.py"
]

zip_filename = "smart-bi-studio-vercel.zip"
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    for f in files_to_pack:
        if os.path.exists(f):
            zipf.write(f, arcname=f)
            print(f"Added {f}")
        else:
            print(f"WARNING: File {f} does not exist!")

print("smart-bi-studio-vercel.zip repackaged successfully.")
