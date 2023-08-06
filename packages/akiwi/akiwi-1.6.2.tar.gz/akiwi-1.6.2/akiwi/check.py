
from . import utils

def native_find_version(name, command, extract_fn):
    output, code = utils.run_bash_command_get_output(command)
    if code != 0:
        utils.vprint(f"Can not find {name}")
        return None

    try:
        version = extract_fn(output)
    except Exception as e:
        utils.vprint(f"To find {name} version, Failed to extract version from the output[{output}]")
        utils.vprint(e)

    utils.vprint(f"Find {name}: {version}")
    return version

__extrace_fn_fristrow_lastspace = lambda x:x.split("\n")[0].split(" ")[-1]

def where(name):
    output, code = utils.run_bash_command_get_output(f"whereis {name}")
    if code != 0:
        utils.vprint(f"Can not find {name}")
        return None
    
    array = output.split("\n")[0].split(" ")
    if len(array) > 1:
        utils.vprint(f"Find {name} location is {array[1]}")
        return array[1]
    
    utils.vprint(f"Can not find {name}")
    return None

def cmake(): return native_find_version("cmake", "cmake --version", __extrace_fn_fristrow_lastspace)
def gplusplus(): return native_find_version("g++", "g++ --version", __extrace_fn_fristrow_lastspace)
def gcc(): return native_find_version("gcc", "gcc --version", __extrace_fn_fristrow_lastspace)

def nvcc(): 
    def extrace_nvcc(output):
        return output.split("\n")[-1].split(" ")[-1][1:]
    return native_find_version("nvcc", "nvcc --version", extrace_nvcc)