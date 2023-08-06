from os import listdir, path, popen
from shutil import copyfile
from sys import version_info

import setuptools

### BELOW GO ALL PACKAGE-DESCRIBING VARIABLES ###
#
# setting variable value to NULL will cause setup
# script to attempt automatic inference (i.e. any
# user-specified value takes precedence over auto
# generated values)
#

PACKAGE_NAME = "indexed_class"
VERSION = "1.1.0"  # custom version string
AUTHOR_NAME = "aachn3"  # package maintainer
AUTHOR_EMAIL = "n45t31@protonmail.com"  # package maintainer contact

SHORT_DESCR = "A mechanism for subclass tree indexation."  # short library description
LONG_DESCR = None  # full library description
LONG_DESCR_CT = None  # full descr content type
PACKAGE_HOME = None  # package homepage url

REQUIREMENTS = []  # PIP install dependencies
PY_VERSION = ">=3.6.0"  # minimum Python version

### END OF PACKAGE-DESCRIBING VARIABLES ###

### AUTO-ASSIGNMENT MECHANISMS ###

ROOT_DIR = path.dirname(path.abspath(__file__))
PACKAGE = path.basename(ROOT_DIR)
PACKAGE_DIR = path.join(ROOT_DIR, PACKAGE)

print(f"{PACKAGE_NAME} in `{ROOT_DIR}/{PACKAGE}` (=`{PACKAGE_DIR}`)")

try:
    copyfile(path.join(ROOT_DIR, ".version"), path.join(PACKAGE_DIR, ".version"))
except:
    pass

# automatic package data
if PACKAGE_NAME is None:
    PACKAGE_NAME = PACKAGE
if VERSION is None:
    try:
        with open(path.join(ROOT_DIR, ".version"), "r") as file:
            VERSION = file.read().strip()
    except:
        try:
            with open(path.join(PACKAGE_DIR, ".version"), "r") as file:
                VERSION = file.read().strip()
        except:
            VERSION = "UNKNOWN"
if AUTHOR_NAME is None:
    try:
        with popen("git config --get user.name") as proc:
            AUTHOR_NAME = proc.read().strip()
            if not AUTHOR_NAME:
                raise ValueError()
    except:
        AUTHOR_NAME = "UNKNOWN"
if AUTHOR_EMAIL is None:
    try:
        with popen("git config --get user.email") as proc:
            AUTHOR_EMAIL = proc.read().strip()
            if not AUTHOR_EMAIL:
                raise ValueError()
    except:
        AUTHOR_EMAIL = ""

# automatic package details
if SHORT_DESCR is None:
    SHORT_DESCR = (
        f"Project `{PACKAGE_NAME}-v{VERSION}' by {AUTHOR_NAME} [{AUTHOR_EMAIL}]"
    )
if LONG_DESCR is None:
    for extension, content_type in [
        (".txt", "text/plain"),
        (".md", "text/markdown"),
        (".rst", "text/x-rst"),
    ]:
        try:
            with open(path.join(ROOT_DIR, f"README{extension}"), "r") as file:
                LONG_DESCR = file.read()
                LONG_DESCR_CT = content_type
                break
        except:
            pass
    else:
        LONG_DESCR = SHORT_DESCR
        LONG_DESCR_CT = "text/plain"
if PACKAGE_HOME is None:
    try:
        with popen("git remote -v get-url --all $(git remote)") as proc:
            PACKAGE_HOME = proc.read().strip()
            if not PACKAGE_HOME:
                raise ValueError()
    except:
        PACKAGE_HOME = ""

# automatic package requirements
if REQUIREMENTS is None:
    try:
        with open(path.join(ROOT_DIR, "requirements.txt"), "r") as file:
            REQUIREMENTS = [line.strip() for line in file]
    except:
        try:
            with open(path.join(PACKAGE_DIR, "requirements.txt"), "r") as file:
                REQUIREMENTS = [line.strip() for line in file]
        except:
            REQUIREMENTS = []
if PY_VERSION is None:
    PY_VERSION = f">={version_info.major}.{version_info.minor}.0"

### END OF AUTO-ASSIGNMENT MECHANISMS ###

### MAIN SETUP FUNCTION ###
setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    url=PACKAGE_HOME,
    description=SHORT_DESCR,
    long_description=LONG_DESCR,
    long_description_content_type=LONG_DESCR_CT,
    install_requires=REQUIREMENTS,
    python_requires=PY_VERSION,
    packages=setuptools.find_packages(),
    py_modules=[
        modfile[:-3] for modfile in listdir(ROOT_DIR) if modfile.endswith(".py")
    ],
    package_data={
        PACKAGE: [".version"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
