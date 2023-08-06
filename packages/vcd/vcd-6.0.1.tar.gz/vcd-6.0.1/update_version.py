# This is a Python script which updates the version number of the VCD files
# Usage: >python update_version.py <new_version>
#   The script investigates which is the current version (in vcd.version) and replaces
#   it with <new_version>
#   e.g. >python update_version.py "5.0.1"
# Author: Marcos Nieto

import glob
import subprocess

from setuptools_scm import get_version

# flag used during the development of this script to check things work as expected
replace = True


def replace_in_files(extensions, version_old, version_new):
    for extension in extensions:
        files = [
            fn
            for fn in glob.iglob("**/*" + extension, recursive=True)
            if (("node_modules" not in fn) and ("d.ts" not in fn))
        ]

        # for filename in glob.iglob('**/*' + extension, recursive=True):
        for filename in files:
            with open(file=filename, mode="r+") as f:
                text = f.read()
                new_text = text.replace(version_old, version_new)

                if text == new_text:
                    print("\t" + filename + " ------- no " + version_old)
                else:
                    print(
                        "\t"
                        + filename
                        + " replacing "
                        + version_old
                        + " with "
                        + version_new
                    )

                if replace:
                    f.seek(0)
                    f.write(new_text)
                    f.truncate()


# Read user input
# if(len(sys.argv) != 2):
#     print("ERROR: Please provide a valid new version number, e.g.: 5.0.1")
# assert(len(sys.argv) == 2)
# version_new = sys.argv[1]

version_new = get_version()

# Check version
with open(file="vcd.version") as f:
    version_current = f.readlines()[0]
    print(f"Current version is {version_current}")

if version_current == version_new:
    print("Current version is already " + version_new)

else:
    # User confirmation
    warning_message = f"Confirm you want to modify VCD version from {version_current} \
                        to {version_new} (y/n): "
    val = input(warning_message)
    if val == "y" or val == "Y":
        print(f"Proceeding to replace {version_current} with {version_new}")

        # Update files
        extensions = [".py", ".ts"]
        replace_in_files(extensions, version_current, version_new)

        # At the end, update vcd.version
        extensions = [".version"]
        replace_in_files(extensions, version_current, version_new)

        # Run updating documentation (only valid for Windows)
        subprocess.check_call(
            ["pdoc", "--html", "--output-dir", ".\\docs\\pdoc", ".\\vcd", "--force"]
        )  # this will create doc\pdoc

    else:
        print("Cancelled by user.")
