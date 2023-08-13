import shutil
import re
import subprocess
from pathlib import Path

from simple503 import make_simple

base_url = "https://github.com/Bing-su/mypypi/releases/download/index"
pattern = r'<a href=".*(?P<last>/[^/]+?/)">'
root = Path(__file__).parent


def remove_if_exists(path):
    if Path.exists(path):
        shutil.rmtree(path)


def fix_main_index():
    index = root.joinpath("index.html")
    data = index.read_text("utf-8")
    data = re.sub(pattern, r'<a href="\g<last>">', data)
    index.write_text(data, "utf-8")


def gen_index():
    packages = root.joinpath("packages")
    wheels = packages.joinpath("wheels")
    indexes = packages.joinpath("indexes")

    zipfiles = list(packages.glob("*.zip"))
    for zipfile in zipfiles:
        shutil.unpack_archive(zipfile, wheels)

    make_simple(wheels, indexes, base_url=base_url)

    ignore = shutil.ignore_patterns("*.whl", "*.tar.gz", "*.metadata")
    shutil.copytree(indexes, root, ignore=ignore, dirs_exist_ok=True)
    fix_main_index()
    remove_if_exists(indexes)
    remove_if_exists(wheels)


if __name__ == "__main__":
    gen_index()
