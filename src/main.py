import os
import shutil
import sys

from copystatic import copy_files_recursive
from page_generator import generate_pages_recursive

STATIC_DIR = "static"
DOCS_DIR = "docs"
CONTENT_DIR = "content"
TEMPLATE_PATH = "template.html"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if os.path.exists(DOCS_DIR):
        print(f"Deleting {DOCS_DIR} directory...")
        shutil.rmtree(DOCS_DIR)

    print(f"Copying {STATIC_DIR} to {DOCS_DIR}...")
    copy_files_recursive(STATIC_DIR, DOCS_DIR)

    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, DOCS_DIR, basepath)


if __name__ == "__main__":
    main()
