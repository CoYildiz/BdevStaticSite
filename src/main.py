import os
import shutil

from copystatic import copy_files_recursive

STATIC_DIR = "static"
PUBLIC_DIR = "public"


def main():
    if os.path.exists(PUBLIC_DIR):
        print(f"Deleting {PUBLIC_DIR} directory...")
        shutil.rmtree(PUBLIC_DIR)

    print(f"Copying {STATIC_DIR} to {PUBLIC_DIR}...")
    copy_files_recursive(STATIC_DIR, PUBLIC_DIR)


if __name__ == "__main__":
    main()
