import os
import shutil


def copy_files_recursive(src_path: str, dst_path: str) -> None:
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    for filename in os.listdir(src_path):
        src_item = os.path.join(src_path, filename)
        dst_item = os.path.join(dst_path, filename)
        if os.path.isfile(src_item):
            print(f"Copying {src_item} -> {dst_item}")
            shutil.copy(src_item, dst_item)
        else:
            copy_files_recursive(src_item, dst_item)
