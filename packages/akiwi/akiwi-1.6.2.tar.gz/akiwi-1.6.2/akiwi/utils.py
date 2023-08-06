import os
import re
import subprocess
import json
import traceback

verbose = False

def vprint(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)

def gprint(*args, **kwargs):
    print(*args, **kwargs)

def get_python_link_name(pydll_path, os_name):
    if os_name == "linux":
        for so in os.listdir(pydll_path):
            if so.startswith("libpython") and not so.endswith(".so") and so.find(".so") != -1:
                basename = os.path.basename(so[3:so.find(".so")])
                full_path = os.path.join(pydll_path, so)
                return basename, full_path
    return "", ""

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

def remove(file):
    try:
        os.remove(file)
        vprint(f"Remove success, file: {file}")
    except:
        vprint(f"Can not remove file: {file}")

def loadjson_dict(file):
    try:
        if os.path.exists(file):
            with open(file, "r") as f:
                val = json.load(f)

            if not isinstance(val, dict):
                vprint(f"A worng config file found, I will remove it.{file}")
                remove(file)
                return None
            return val
        return None
    except:
        vprint(f"Failed to load json: {file}")
        return None

def dumpjson_dict(file, obj):
    try:
        with open(file, "w") as f:
            json.dump(obj, f, indent=4)
        return True
    except:
        print(f"An error encounter when dump the obj to file: {file}")
        return False

def replace_with_var_map(file, text, vars_dict, inverse=False):
    replaced = False
    printed  = False
    printed_dict = set()
    file_name = os.path.basename(file)

    if not inverse:
        items = re.split("(\${@[A-Za-z.\-_]{1,64}})", text)
        for i, item in enumerate(items):
            if item.startswith("${@") and item.endswith("}"):
                var_name = item[3:-1]
                if var_name in vars_dict:
                    if not printed:
                        printed = True
                        vprint(f"Replace the file variables: {file}")

                    if var_name not in printed_dict:
                        printed_dict.add(var_name)
                        vprint(f" {file_name} -- {var_name} -> {vars_dict[var_name]}")
                    items[i] = vars_dict[var_name]
                    replaced = True
                else:
                    vprint(f"Can not find variable {var_name}")
        
        if replaced:
            text = "".join(items)
    else:
        for value in vars_dict:
            name = vars_dict[value]
            if text.find(value) != -1:
                replaced = True
                if not printed:
                    printed = True
                    vprint(f"Replace the file variables: {file}")

                vprint(f" {file_name} -- {value} -> {name}")
                text = text.replace(value, f"${{@{name}}}")
    return replaced, text

def replace_file_with_var_map(file, vars_dict, inverse=False):

    try:
        if not os.path.exists(file):
            print("--", file)
            vprint(f"Can not replace variable in file: {file}")
            return False

        try:
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError as e:
            print(f"Can not replace variable in file, it is binary file: {file}")
            return False

        replaced, new_text = replace_with_var_map(file, text, vars_dict, inverse)
        if replaced:
            with open(file, "w", encoding="utf-8") as f:
                f.write(new_text)
        return True
    except:
        traceback.print_exc()
        vprint(f"Can not replace variable in file: {file}")
    return False