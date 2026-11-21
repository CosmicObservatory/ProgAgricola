from pathlib import Path
import os

# Project Folder Path
PATH_ROOT = Path(__file__).parents[2]

PATH_FOLDERDATA = PATH_ROOT / "data"

LEVELS_DATA = ["pure", "raw", "calified", "clean", "tidy"]

SOURCES = ["DGSIAP", "INEGI", "MAPBIOMAS"]

for level in LEVELS_DATA:
    for source in SOURCES:
        path_folder = PATH_FOLDERDATA / level / source
        os.makedirs(path_folder, exist_ok=True)

