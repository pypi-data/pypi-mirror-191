import os
import re
import subprocess

verbose = False

def vprint(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)

def get_python_link_name(pydll_path, os_name):
    if os_name == "linux":
        for so in os.listdir(pydll_path):
            if so.startswith("libpython") and not so.endswith(".so") and so.find(".so") != -1:
                basename = os.path.basename(so[3:so.find(".so")])
                full_path = os.path.join(pydll_path, so)
                return basename, full_path
    return None, None

def format_size(size):

    units = ["Byte", "KB", "MB", "GB", "PB"]
    for i, unit in enumerate(units):
        ref = 1024 ** (i + 1)
        if size < ref:
            div = 1024 ** i
            if i == 0:
                return f"{size} {unit}"
            else:
                return f"{size / div:.2f} {unit}"
    return f"{size} Bytes"

def run_bash_command_out_to_console(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")

    while True:
        realtime_output = p.stdout.readline()
        if realtime_output == "" and p.poll() is not None:
            break

        if realtime_output:
            print(realtime_output, flush=True, end="")
    return p.returncode

def run_bash_command_get_output(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")

    output = ""
    while True:
        realtime_output = p.stdout.readline()
        if realtime_output == "" and p.poll() is not None:
            break

        if realtime_output:
            output += realtime_output
    return output.strip(), p.returncode

# 3.1, 2.5, 3.1.6.8, 2.5.4.0
def version_to_int(version):

    array = version.split(".")
    if len(array) > 4:
        vprint(f"Ignore numbers after 4 digits of the version number, {version}")
        array = array[:4]
    
    multipliers = [1<<24, 1<<16, 1<<8, 1]
    imultiplier = 0
    output_number = 0
    for value in array:
        value = int(re.sub("\D", "", value))
        if value > 255:
            vprint(f"Numbers larger than 255 are trimmed to within 255, when {value} > 255")
            value = 255

        output_number += value * multipliers[imultiplier]
        imultiplier += 1
    return output_number

# return False if version can not meet the limit
def version_limit(version, minimum_limit=None, maximum_limit=None):

    if minimum_limit is None and maximum_limit is None:
        vprint("The return value is always True when both minimum_limit and maximum_limit are None.")
        return True

    iversion = version_to_int(version)
    if minimum_limit is not None:
        iminimum_limit = version_to_int(minimum_limit)
        if iversion < iminimum_limit:
            return False
    
    if maximum_limit is not None:
        imaximum_limit = version_to_int(maximum_limit)
        if iversion > imaximum_limit:
            return False
    return True