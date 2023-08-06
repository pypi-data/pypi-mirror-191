'''
    Copy right 2023.
'''

import sys
import argparse
import os
import json
import shutil
import platform
import uuid
import traceback
from urllib.parse import urlencode
from . import http
from . import utils
from . import version
from collections import OrderedDict

class ChangeCWD:
    def __init__(self, dir):
        self.dir = os.path.abspath(dir)
        self.old = os.path.abspath(os.getcwd())
    
    def __enter__(self):
        os.chdir(self.dir)
        utils.vprint(f"Enter {self.dir}")

    def __exit__(self, *args, **kwargs):
        os.chdir(self.old)
        utils.vprint(f"Leave {self.dir}, Enter {self.old}")


class Cmd:
    def __init__(self, actions):
        self.parser    = argparse.ArgumentParser()
        self.subparser = self.parser.add_subparsers(dest="cmd")
        self.actions   = actions

    def add_cmd(self, name : str, help : str = None)->argparse._ActionsContainer:
        return self.subparser.add_parser(name, help=help)

    def help(self):
        self.parser.print_help()

    def hello(self):
        utils.gprint(
        "      ___                       ___                 \n"+
        "     /\\__\\          ___        /\\__\\          ___   \n"+
        "    /:/  /         /\\  \\      /:/ _/_        /\\  \\  \n"+
        "   /:/__/          \\:\\  \\    /:/ /\\__\\       \\:\\  \\ \n"+
        "  /::\\__\\____      /::\\__\\  /:/ /:/ _/_      /::\\__\\\n"+
        " /:/\\:::::\\__\\  __/:/\\/__/ /:/_/:/ /\\__\\  __/:/\\/__/       Welcome to KIWI World ! Enjoy One-Click Magic!\n"+
        f" \\/_|:|~~|~    /\\/:/  /    \\:\\/:/ /:/  / /\\/:/  /                             {version.version}  \n"+
        "    |:|  |     \\::/__/      \\::/_/:/  /  \\::/__/                     https://www.zifuture.com\n"+
        "    |:|  |      \\:\\__\\       \\:\\/:/  /    \\:\\__\\    \n"+
        "    |:|  |       \\/__/        \\::/  /      \\/__/    \n"+
        "     \\|__|                     \\/__/                \n"
        "\n"
        "You can use 'kiwi --help' to show the more message."
        )

    def run(self, args, addi_args):
        args = self.parser.parse_args(args)
        if args.cmd is None:
            self.hello()
            return False

        return self.actions.private_run_cmd(args, addi_args)


class Config:
    def __init__(self):
        self.SERVER      = "https://www.zifuture.com/api"
        self.CACHE_ROOT  = os.path.expanduser('~/.kiwi')
        self.VENV_DIR   = os.path.join(self.CACHE_ROOT, "venv")
        self.CONFIG_JSON  = os.path.join(self.CACHE_ROOT, "config.json")
        self.CURRENT_ENV = "base"
        self.VENV_JSON  = os.path.join(self.VENV_DIR, f"{self.CURRENT_ENV}.json")
        self.INSTALLED_LIBS_JSON  = os.path.join(self.CACHE_ROOT, "libs.json")
        self.OS_NAME     = platform.system().lower()
        self.PY_VERSION  = ".".join(sys.version.split(".")[:2])
        self.KIWI_ROOT   = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
        self.CWD         = os.path.abspath(os.path.curdir)
        self.PYLIB_DIR   = os.path.join(sys.exec_prefix, "lib")
        self.PYLIB_NAME, self.PYLIB_PATH = utils.get_python_link_name(self.PYLIB_DIR, self.OS_NAME)
        self.DATA_DIR    = os.path.join(self.CACHE_ROOT, "data")
        self.PKG_DIR     = os.path.join(self.CACHE_ROOT, "pkg")
        self.LIB_DIR     = os.path.join(self.CACHE_ROOT, "lib")
        self.CODE_DIR    = os.path.join(self.CACHE_ROOT, "code")
        os.makedirs(self.CACHE_ROOT, exist_ok=True)
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.PKG_DIR,  exist_ok=True)
        os.makedirs(self.LIB_DIR,  exist_ok=True)
        os.makedirs(self.CODE_DIR, exist_ok=True)
        os.makedirs(self.VENV_DIR, exist_ok=True)
        
        self.ACCESS_TOKEN = ""
        self.dynamic_keys = [
            "DATA_DIR", "CODE_DIR", "PKG_DIR", "ACCESS_TOKEN", "SERVER", "CURRENT_ENV"
        ]
        self.INSTALLED_LIBS = {}
        self.VENV           = {"libs":{}, "macros":{}}
        self.setup()

        self.CURRENT_MACROS = self.VENV["macros"]
        self.CURRENT_LIBS   = self.VENV["libs"]
        vars_map = self.get_dict()
        for key in vars_map:
            os.environ["KIWI_" + key] = vars_map[key]

        for key in self.CURRENT_MACROS:
            os.environ["KIWI_" + key] = self.CURRENT_MACROS[key]

    def get_dict(self):
        return {
            "SERVER"     : self.SERVER,
            "CACHE_ROOT" : self.CACHE_ROOT,
            "CONFIG_JSON" : self.CONFIG_JSON,
            "VENV_JSON" : self.VENV_JSON,
            "INSTALLED_LIBS_JSON" : self.INSTALLED_LIBS_JSON,
            "CURRENT_ENV": self.CURRENT_ENV,
            "OS_NAME" : self.OS_NAME,
            "PY_VERSION" : self.PY_VERSION,
            "KIWI_ROOT" : self.KIWI_ROOT,
            "CWD" :       self.CWD,
            "PYLIB_DIR" : self.PYLIB_DIR,
            "PYLIB_NAME" : self.PYLIB_NAME,
            "PYLIB_PATH" : self.PYLIB_PATH,
            "DATA_DIR" : self.DATA_DIR,
            "PKG_DIR" : self.PKG_DIR,
            "LIB_DIR" : self.LIB_DIR,
            "CODE_DIR" : self.CODE_DIR,
            "ACCESS_TOKEN" : self.ACCESS_TOKEN
        }

    def setup(self):
        # load config
        cfg = utils.loadjson_dict(self.CONFIG_JSON)
        if cfg is not None:
            for key in cfg:
                if key in self.dynamic_keys:
                    if cfg[key] is not None:
                        setattr(self, key, cfg[key])
                else:
                    utils.gprint(f"Unknow config name {key}")
        else:
            self.dump_config()
        
        cfg = utils.loadjson_dict(self.INSTALLED_LIBS_JSON)
        if cfg is not None:
            self.INSTALLED_LIBS = cfg

        self.VENV_JSON  = os.path.join(self.VENV_DIR, f"{self.CURRENT_ENV}.json")
        cfg = utils.loadjson_dict(self.VENV_JSON)
        if cfg is not None:
            self.VENV = cfg
        else:
            self.dump_venv()

    def dump_config(self):
        return utils.dumpjson_dict(self.CONFIG_JSON, {key:getattr(self, key) for key in self.dynamic_keys})

    def dump_installed_libs(self):
        return utils.dumpjson_dict(self.INSTALLED_LIBS_JSON, self.INSTALLED_LIBS)

    def dump_venv(self):
        return utils.dumpjson_dict(self.VENV_JSON, self.VENV)

    def __repr__(self):
        sb  = ["Config:"]
        dic = self.get_dict()
        for key in dic:
            val = dic[key]
            sb.append(f"   {key} = {val}")
        return "\n".join(sb)
    
    def create_env(self, name, copyfrom):

        if copyfrom is not None:
            env_file  = os.path.join(self.VENV_DIR, f"{copyfrom}.json")
            if not os.path.exists(env_file):
                utils.gprint(f"Invalid enviroment '{copyfrom}'")
                return False

            dst_env_file  = os.path.join(self.VENV_DIR, f"{name}.json")
            shutil.copyfile(env_file, dst_env_file)
            return True

        env_file  = os.path.join(self.VENV_DIR, f"{name}.json")
        env_dict  = {"libs": {}, "macros": {}}
        try:
            with open(env_file, "w") as f:
                json.dump(env_dict, f)
            return True
        except:
            utils.gprint(f"Failed to create env '{name}'")
        return False

    def activate_env(self, name):
        
        env_json  = os.path.join(self.VENV_DIR, f"{name}.json")
        if not os.path.exists(env_json):
            utils.gprint(f"Not exists virtual enviroment: {name}")
            return False
        
        cfg = utils.loadjson_dict(env_json)
        if cfg is None:
            utils.gprint(f"Failed to load the virtual enviroment: {name}")
            return False

        self.VENV_JSON  = env_json
        self.VENV = cfg
        self.CURRENT_ENV = name
        self.CURRENT_MACROS = self.VENV.get("macros", {})
        self.CURRENT_LIBS   = self.VENV.get("libs", {})
        vars_map = self.get_dict()
        for key in vars_map:
            os.environ["KIWI_" + key] = vars_map[key]

        for key in self.CURRENT_MACROS:
            os.environ["KIWI_" + key] = self.CURRENT_MACROS[key]
        self.dump_venv()
        self.dump_config()
        return True
    
    def check_package(self, name, version_min=None, version_max=None):

        if name not in self.CURRENT_LIBS:
            return False, None, None
        
        version, folder_name, description = self.CURRENT_LIBS[name]
        if utils.version_limit(version, version_min, version_max):
            return True, version, folder_name
        
        return False, "", ""

class Actions:
    def __init__(self, app):
        self.app = app
        self.cfg : Config = app.cfg

    def private_run_cmd(self, args, _addi_args):
        
        cmd = args.cmd
        if not hasattr(self, cmd):
            return False

        del args.__dict__["cmd"]
        return getattr(self, cmd)(args, _addi_args)

    def __rmtree(self, dir):
        dir = dir.strip()
        if dir == "." or dir == ".." or dir == "/":
            utils.vprint(f"Can not remove directory [{dir}]")
            return

        if os.path.exists(dir):
            utils.vprint(f"Remove directory: {dir}")
            shutil.rmtree(dir)

    def __run_py(self, file, args):
        utils.vprint(f"Run python script file: {file} at {os.getcwd()}")

        try:
            code_dir = os.path.realpath(os.path.dirname(file))
            union_name = str(uuid.uuid1()).replace("-", "")
            code_name  = f"___tempcode_{union_name}"
            temp_code_file = os.path.join(code_dir, f"{code_name}.py")
            shutil.copyfile(file, temp_code_file)
            sys.path.insert(0, code_dir)
            m = __import__(code_name, globals(), locals(), ["*"])
            utils.remove(temp_code_file)
            result =  getattr(m, "run")(self.app, args)
        except Exception as e:
            traceback.print_exc()
            result = False
        
        self.__rmtree(".kiwi/__pycache__")
        return result

    def __run_bash(self, file):
        utils.vprint(f"Run bash script file: {file} at {os.getcwd()}")

        try:
            code_dir = os.path.realpath(os.path.dirname(file))
            temp_code_file = os.path.join(code_dir, "___tempcode.sh")
            shutil.copyfile(file, temp_code_file)
            code = os.system(f'bash \"{temp_code_file}\"')
            utils.remove(temp_code_file)
            return code == 0
        except Exception as e:
            traceback.print_exc()
            return False

    def __run_link(self, file):
        if not os.path.exists(file):
            return False

        try:
            dir = os.path.realpath(os.path.dirname(file))
            with ChangeCWD(dir):
                utils.vprint(f"Run link script file: {file} at {os.getcwd()}")

                dic = self.cfg.get_dict()
                for name in dic:
                    os.environ[name] = dic[name]

                for i, line in enumerate(open(file, "r").readlines()):
                    line = line.replace("\n", "")
                    opts = line.split(" ", maxsplit=1)
                    if len(opts) != 2: continue

                    op    = opts[0]
                    param = opts[1]
                    if op == "link":
                        ps = param.split(" ")
                        if len(ps) == 2:
                            fa = os.path.abspath(ps[0])
                            fb = os.path.abspath(ps[1])
                            utils.vprint(f"Run link command: ln -s \"{fa}\" \"{fb}\"")

                            if os.system(f"ln -s \"{fa}\" \"{fb}\"") != 0:
                                utils.gprint(f"Failed to run command: ln -s \"{fa}\" \"{fb}\"")
                                return False
                        elif len(ps) == 1:
                            fa = os.path.abspath(ps[0])
                            p  = ps[0].rfind(".so")
                            if p == -1:
                                utils.gprint(f"Can not process this command: {line}")
                                return

                            fb = os.path.abspath(ps[0][:p+3])
                            utils.vprint(f"Run link command: ln -s \"{fa}\" \"{fb}\"")

                            if os.system(f"ln -s \"{fa}\" \"{fb}\"") != 0:
                                utils.gprint(f"Failed to run command: ln -s \"{fa}\" \"{fb}\"")
                                return False
                        else:
                            utils.gprint(f"Invalid command in line: {i}, {line}")
                            return False

                    elif op == "cmd":
                        utils.vprint(f"Run command: {param}")

                        if os.system(param) != 0:
                            utils.gprint(f"Invalid command: {param}")
                            return False
            utils.remove(file)
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    def __atomatic_run(self, work_dir, args):
        with ChangeCWD(work_dir):
            auto_config_file = ".kiwi/auto.py"
            if os.path.exists(auto_config_file):
                utils.vprint(f"Run automatic script {auto_config_file}")
                if not self.__run_py(auto_config_file, args):
                    return False
            else:
                utils.vprint(f"The non-existent file {auto_config_file}")

            auto_config_file = ".kiwi/auto.sh"
            if os.path.exists(auto_config_file):
                utils.vprint(f"Run automatic script {auto_config_file}")
                return self.__run_bash(auto_config_file)
            else:
                utils.vprint(f"The non-existent file {auto_config_file}")
        return True

    def __register_lib(self, folder_name, lib_file, update_installed_lib=True):
        try:
            this_prefix = os.path.dirname(os.path.realpath(lib_file))
            lines = open(lib_file, "r").readlines()
            attributes = {}
            for line in lines:
                key, value = line.strip().split("=", 2)
                key   = key.strip()
                value = value.strip()
                if key in attributes:
                    utils.vprint(f"Duplicate name {key}:{value} was found and the value will be overwritten")
                
                attributes[key] = value.replace("${this}", this_prefix)

            if "NAME" not in attributes:
                utils.gprint(f"The library [{folder_name}] lack the required attribute NAME")
                return False

            if "VERSION" not in attributes:
                utils.gprint(f"The library [{folder_name}] lack the required attribute VERSION")
                return False

            lib_name = attributes["NAME"]
            version  = attributes["VERSION"]
            description = attributes.get("DESCRIPTION", "")

            if update_installed_lib:
                utils.vprint(f"Add new library {lib_name} {version}")
                self.cfg.INSTALLED_LIBS[folder_name] = {"name": lib_name, "version": version, "description": description}
                if not self.cfg.dump_installed_libs():
                    return False
            
            self.cfg.CURRENT_LIBS[lib_name] = [version, folder_name, description]
            if not self.cfg.dump_venv():
                return False

            for key in attributes:
                if key not in ["NAME", "VERSION", "DESCRIPTION"]:
                    utils.vprint(f"Register macro: {key} = {attributes[key]}")
                    self.cfg.CURRENT_MACROS[key] = attributes[key]
            return self.cfg.dump_venv()
        except:
            utils.gprint(f"Failed to register lib {folder_name}")
            pass
        return False

    def config(self, args : argparse.Namespace, addi_args):

        if args.key is None and args.value is None:
            utils.gprint(self.cfg)
            return False

        if args.value is None:
            utils.gprint(getattr(self.cfg, args.key))
            return False
        
        if args.key not in self.cfg.dynamic_keys:
            utils.gprint(f"Unsupport config name {args.key}")
            return False

        setattr(self.cfg, args.key, args.value)
        self.cfg.dump_config()
        utils.gprint("Success!")
        return True

    def auth(self, args : argparse.Namespace, addi_args):
        setattr(self.cfg, "ACCESS_TOKEN", args.token)
        self.cfg.dump_config()
        utils.gprint("Success!")
        return True

    def get(self, args : argparse.Namespace, addi_args):
        repo = args.repo
        if repo.find("/") == -1:
            utils.gprint(f"Invalid repo name: {repo}")
            return False

        owner, proj = repo.split("/")
        os.environ["KIWI_REPO_OWNER"] = owner
        os.environ["KIWI_REPO_NAME"] = proj

        file = os.path.join(self.cfg.CODE_DIR, repo + ".zip")
        fileurl = f"{self.cfg.SERVER}/public/repo/zip/{repo}?accessToken={self.cfg.ACCESS_TOKEN}"
        md5url  = f"{self.cfg.SERVER}/public/repo/shortinfo/{repo}?accessToken={self.cfg.ACCESS_TOKEN}"
        if not http.require_file_and_check_md5(fileurl, md5url, file, f"Getting {repo}", args.update, utils.verbose)[0]:
            utils.gprint(f"Failed to get repo {repo}.")
            return False

        if args.save is not None:
            proj = args.save

        if args.rmtree:
            self.__rmtree(proj)

        os.environ["KIWI_REPO_SAVE_TO"] = proj
        http.extract_zip_to(file, proj, utils.verbose)

        if not args.disable_run:
            self.__atomatic_run(proj, args)
        else:
            utils.vprint(f"Do not run any automatic scripts, because disable_run is set.")
        return True

    def getd(self, args : argparse.Namespace, addi_args):
        data = args.data
        if data.find("/") == -1:
            utils.gprint(f"Invalid data name: {data}")
            return False

        owner, dname = data.split("/")
        os.environ["KIWI_DATA_OWNER"] = owner
        os.environ["KIWI_DATA_NAME"] = dname

        file = os.path.join(self.cfg.DATA_DIR, data + ".zip")
        fileurl = f"{self.cfg.SERVER}/public/data/download/{data}?accessToken={self.cfg.ACCESS_TOKEN}"
        md5url  = f"{self.cfg.SERVER}/public/data/shortinfo/{data}?accessToken={self.cfg.ACCESS_TOKEN}"
        ok, info, state = http.require_file_and_check_md5(fileurl, md5url, file, f"Getting {data}", args.update, utils.verbose)
        if not ok:
            utils.gprint(f"Failed to install data {data}.")
            return False

        if args.save is not None:
            dname = args.save
        
        if args.rmtree:
            self.__rmtree(dname)

        os.environ["KIWI_DATA_SAVE_TO"] = dname
        if info["type"] == "PythonScript":
            if not args.disable_run:
                return self.__run_py(file, args)
            else:
                utils.gprint(f"Script run denied: {file}")
                return False
        elif info["type"] == "BashScript":
            if not args.disable_run:
                return self.__run_bash(file)
            else:
                utils.gprint(f"Script run denied: {file}")
                return False
    
        http.extract_zip_to(file, dname, utils.verbose)
        if not args.disable_run:
            return self.__atomatic_run(dname, args)
        else:
            utils.vprint(f"Do not run any automatic scripts, because disable_run is set.")
        return True

    def install(self, args : argparse.Namespace, addi_args):

        pkg = args.pkg
        if pkg.find("/") == -1:
            utils.gprint(f"Invalid pkg name: {pkg}")
            return False

        owner, dname = pkg.split("/")
        os.environ["KIWI_PKG_OWNER"] = owner
        os.environ["KIWI_PKG_NAME"] = dname

        file = os.path.join(self.cfg.PKG_DIR, pkg + ".zip")
        fileurl = f"{self.cfg.SERVER}/public/pkg/download/{pkg}?accessToken={self.cfg.ACCESS_TOKEN}"
        md5url  = f"{self.cfg.SERVER}/public/pkg/shortinfo/{pkg}?accessToken={self.cfg.ACCESS_TOKEN}"
        ok, info, state = http.require_file_and_check_md5(fileurl, md5url, file, f"Getting {pkg}", args.update, utils.verbose)
        if not ok:
            utils.gprint(f"Failed to install pkg {pkg}.")
            return False

        if args.save is None:
            install_to = os.path.join(self.cfg.LIB_DIR, dname)
        else:
            install_to = args.save

        if state == "Cached" and os.path.isdir(install_to) and (dname in self.cfg.INSTALLED_LIBS):
            if not args.force:
                lib_file = os.path.abspath(os.path.join(install_to, ".kiwi.lib"))
                if os.path.exists(lib_file):
                    self.__register_lib(dname, lib_file, False)
                utils.gprint(f"Package {dname} is already installed. Configured it to the current environment {self.cfg.CURRENT_ENV}")
                utils.vprint(f"[install {pkg}] Since the installation directory already exists and is registered, we do not do anything without force")
                return True
            
        if not args.normtree:
            self.__rmtree(install_to)

        os.environ["KIWI_PKG_INSTALL_TO"] = install_to
        if info["type"] == "PythonScript":
            if not args.disable_run:
                return self.__run_py(file, args)
            else:
                utils.gprint(f"Script run denied: {file}")
                return False
        elif info["type"] == "BashScript":
            if not args.disable_run:
                return self.__run_bash(file)
            else:
                utils.gprint(f"Script run denied: {file}")
                return False
        else:
            http.extract_zip_to(file, install_to, utils.verbose)

            if not args.disable_run:
                if not self.__atomatic_run(install_to, args):
                    return False
            else:
                utils.vprint(f"Do not run any automatic scripts, because disable_run is set.")
            
            utils.gprint(f"Install to {install_to}")
            link_file = os.path.abspath(os.path.join(install_to, ".kiwi.link"))
            if os.path.exists(link_file):
                if not self.__run_link(link_file):
                    return False

            lib_file = os.path.abspath(os.path.join(install_to, ".kiwi.lib"))
            if os.path.exists(lib_file):
                return self.__register_lib(dname, lib_file)
            return True

    def clean(self, args : argparse.Namespace, addi_args):
        self.__rmtree(self.cfg.CODE_DIR)
        self.__rmtree(self.cfg.PKG_DIR)
        self.__rmtree(self.cfg.DATA_DIR)
        os.makedirs(self.cfg.DATA_DIR, exist_ok=True)
        os.makedirs(self.cfg.PKG_DIR,  exist_ok=True)
        os.makedirs(self.cfg.CODE_DIR, exist_ok=True)
        return True

    def qr(self, args : argparse.Namespace, addi_args):
        return self.app.run_with_command("getd sxai/qrimg -u -save=.")

    def libs(self, args : argparse.Namespace, addi_args):

        utils.gprint(f"{len(self.cfg.CURRENT_LIBS)} libraries found:")
        for i, key in enumerate(self.cfg.CURRENT_LIBS):
            name, version, descriptin = self.cfg.CURRENT_LIBS[key]
            path = os.path.join(self.cfg.LIB_DIR, key)
            utils.gprint(f"{i+1}. {name}-{version}\t{descriptin}\t{path}")
        return True

    def macros(self, args : argparse.Namespace, addi_args):

        utils.gprint(f"{len(self.cfg.CURRENT_MACROS)} macros found:")
        for i, key in enumerate(self.cfg.CURRENT_MACROS):
            value = self.cfg.CURRENT_MACROS[key]
            utils.gprint(f"{i+1}. {key} = {value}")
        return True
    
    def activate(self, args : argparse.Namespace, addi_args):
        return self.cfg.activate_env(args.name)
    
    def create(self, args : argparse.Namespace, addi_args):
        return self.cfg.create_env(args.name, args.copyfrom)
    
    def envs(self, args : argparse.Namespace, addi_args):
        utils.gprint(f"Current virtual enviroment: {self.cfg.CURRENT_ENV}")
        envs = os.listdir(self.cfg.VENV_DIR)
        for file in envs:
            if file.endswith(".json") and not file.startswith("."):
                name = os.path.splitext(file)[0]
                path = os.path.join(self.cfg.VENV_DIR, file)
                if name == self.cfg.CURRENT_ENV:
                    utils.gprint(f"* {name}   --   {path}")
                else:
                    utils.gprint(f"  {name}   --   {path}")
        return True

    def repvar(self, args : argparse.Namespace, addi_args):
        
        directory = args.directory
        if directory is None:
            directory = os.path.abspath(".")
        
        default_list = ".json;makefile;cmakelists.txt;.sh;.bash"
        filter_list  = default_list
        if args.filter is not None:
            filter_list = args.filter

        if args.inverse:
            vars_map  = {self.cfg.CURRENT_MACROS[key]:key for key in self.cfg.CURRENT_MACROS}
            select_names = [
                "DATA_DIR", "CODE_DIR", "PKG_DIR", "LIB_DIR", "PYLIB_PATH", "PYLIB_DIR", "KIWI_ROOT",
                "CACHE_ROOT"
            ]
            vars_dict = self.cfg.get_dict()
            for name in select_names:
                vars_map[vars_dict[name]] = name

            list_vars = [[key, vars_map[key]] for key in vars_map]
            list_vars = sorted(list_vars, key=lambda x:len(x[0]), reverse=True)
            vars_map = OrderedDict(list_vars)
        else:
            vars_map  = {key:self.cfg.CURRENT_MACROS[key] for key in self.cfg.CURRENT_MACROS}
            select_names = [
                "DATA_DIR", "CODE_DIR", "PKG_DIR", "LIB_DIR", "PYLIB_NAME", "PYLIB_PATH", "PYLIB_DIR", "KIWI_ROOT", "CWD", "PY_VERSION",
                "OS_NAME", "CACHE_ROOT"
            ]
            vars_dict = self.cfg.get_dict()
            for name in select_names:
                vars_map[name] = vars_dict[name]

        filter_list = filter_list.split(";")
        for d, ds, fs in os.walk(directory):
            if os.path.basename(d) == ".kiwi":
                utils.vprint(f"Ignore directory {d}")
                continue

            for file in fs:
                full_path = os.path.join(d, file)
                basename = file.lower()
                suffix = os.path.splitext(basename)[1]
                if basename in filter_list or suffix != "" and suffix in filter_list:
                    utils.replace_file_with_var_map(full_path, vars_map, args.inverse)
        return True
        
    def run(self, args : argparse.Namespace, addi_args):

        file    = args.runfile
        workdir = args.workdir

        if file is None:
            file = os.path.abspath(".kiwi/auto.py")
            if not os.path.exists(file):
                cwd = os.path.abspath(os.getcwd())
                p = cwd.rfind("/")
                while p != -1:
                    file = os.path.join(cwd[:p], ".kiwi/auto.py")
                    if os.path.exists(file):
                        break
                    p = cwd.rfind("/", 0, p)
                    
            if not os.path.exists(file):
                file = os.path.abspath(".kiwi/auto.sh")
                if not os.path.exists(file):
                    cwd = os.path.abspath(os.getcwd())
                    p = cwd.rfind("/")
                    while p != -1:
                        file = os.path.join(cwd[:p], ".kiwi/auto.sh")
                        if os.path.exists(file):
                            break
                        p = cwd.rfind("/", 0, p)

        if not os.path.exists(file):
            utils.gprint("Can not found any auto script to run.")
            return False

        if workdir is None:
            workdir = os.path.dirname(os.path.dirname(file))

        with ChangeCWD(workdir):

            if addi_args is not None:
                allargs = addi_args
                kwargs_map = {}
                args_list  = []
                for item in allargs:
                    if item.startswith("--") or item.startswith("-"):
                        stlen = 2 if item.startswith("--") else 1
                        line = item[stlen:]
                        p = line.find("=")
                        if p != -1:
                            kwargs_map[line[:p]] = line[p+1:]
                        else:
                            kwargs_map[line] = True
                    else:
                        args_list.append(item)
                args.args = args_list
                args.__dict__.update(kwargs_map)

            if file.endswith(".py"):
                return self.__run_py(file, args)
            elif file.endswith(".sh"):
                return self.__run_bash(file)
            return False

    def search(self, args : argparse.Namespace, addi_args):
        param = urlencode({"key": args.key, "accessToken": self.cfg.ACCESS_TOKEN})
        url = f"{self.cfg.SERVER}/public/search/list?" + param
        data = http.request_text(url)
        if data is None:
            return False

        utils.gprint(f"Search {len(data)} results using {args.key}")
        for i, (size, shortDescription, createTime, dtype, path) in enumerate(data):
            
            i += 1
            if dtype in ["Data", "Package"]:
                if shortDescription is not None:
                    utils.gprint(f"{i}[{dtype}]: {path}, {utils.format_size(size)}, {shortDescription}")
                else:
                    utils.gprint(f"{i}[{dtype}]: {path}, {utils.format_size(size)}")
            else:
                if shortDescription is not None:
                    utils.gprint(f"{i}[{dtype}]: {path}, {shortDescription}")
                else:
                    utils.gprint(f"{i}[{dtype}]: {path}")
        return True

class Application:
    def __init__(self):
        self.cfg     = Config()
        self.actions = Actions(self)
        self.setup_env()

        cmd = Cmd(self.actions)
        c = cmd.add_cmd("config", "Configure")
        c.add_argument("key",   nargs="?", type=str, help=f"config name, support: {', '.join(self.cfg.dynamic_keys)}")
        c.add_argument("value", nargs="?", type=str, help="config value")

        c = cmd.add_cmd("get", "Get code from server")
        c.add_argument("repo", type=str, help="repo name")
        c.add_argument("-update", action="store_true", help="Force update")
        c.add_argument("-save", type=str, help="Unzipped folder")
        c.add_argument("-rmtree", action="store_true", help="Unzip the data after remove the save folder.")
        c.add_argument("-disable-run", action="store_true", help="Disable auto run")

        c = cmd.add_cmd("run", "Run the project automation script")
        c.add_argument("-runfile", type=str, help="script file, default is .kiwi/auto.py or .kiwi/auto.sh")
        c.add_argument("-workdir", type=str, help="workspace dir, default is solution dir")

        c = cmd.add_cmd("auth", "Set auth ACCESS_TOKEN")
        c.add_argument("token", type=str, help="Access token name")

        c = cmd.add_cmd("getd", "Get data from server")
        c.add_argument("data", type=str, help="data name")
        c.add_argument("-update", action="store_true", help="Force update")
        c.add_argument("-save", type=str, help="Unzipped folder")
        c.add_argument("-rmtree", action="store_true", help="Unzip the data after remove the save folder.")
        c.add_argument("-disable-run", action="store_true", help="Disable auto run")

        c = cmd.add_cmd("clean", "Clean cache files.")
        c = cmd.add_cmd("libs", "List all installed library.")
        c = cmd.add_cmd("macros", "List all installed library's macros.")
        c = cmd.add_cmd("repvar", "Macro variable replacement in the specified directory tree.")
        c.add_argument("directory", nargs="?", type=str, help="specified directory")
        c.add_argument("-filter", type=str, help="specified file filter", default=".json;.cu;.cpp;.cuh;.h;.hpp;.cpp;makefile;cmakelists.txt;.sh;.bash;.py;.c")
        c.add_argument("-inverse", action="store_true", help="inverse replace")

        c = cmd.add_cmd("activate", "Activate the current environment as specified")
        c.add_argument("name", type=str, help="Virtual environment name")

        c = cmd.add_cmd("create", "Create the current environment as specified")
        c.add_argument("name", type=str, help="Virtual environment name")
        c.add_argument("-copyfrom", type=str, help="Copy from virtual environment name")

        c = cmd.add_cmd("envs", "Create the current environment as specified")

        c = cmd.add_cmd("install", "Install package from server")
        c.add_argument("pkg", type=str, help="package name")
        c.add_argument("-update", action="store_true", help="Force update")
        c.add_argument("-save", type=str, help="Unzipped folder")
        c.add_argument("-normtree", action="store_true", help="Unzip the data after remove the save folder.")
        c.add_argument("-disable-run", action="store_true", help="Disable auto run")
        c.add_argument("-force", action="store_true", help="Ignore existing installations and enforce them")

        c = cmd.add_cmd("search", "Search solution / data / package")
        c.add_argument("key", type=str, help="search name")

        c = cmd.add_cmd("qr", "下载手写AI微信二维码，以联系到手写AI")
        self.cmd = cmd

    def setup_env(self):
        os.makedirs(self.cfg.CACHE_ROOT, exist_ok=True)

    def run_with_command(self, args=None)->bool:

        if args is not None and isinstance(args, str):
            args = args.split(" ")
        elif args is None:
            args = sys.argv[1:]

        for i in range(len(args)):
            if args[i] == "-verbose":
                del args[i]
                utils.verbose = True
                break
        
        addi_args = None
        if len(args) > 0:
            if(args[0] == "run"):
                addi_args = []
                old_args  = []
                skip = [False] * len(args) 
                for i in range(1, len(args)):
                    if skip[i]: continue

                    arg = args[i]
                    if not (arg.startswith("-runfile") or arg.startswith("-workdir")):
                        addi_args.append(arg)
                    else:
                        if arg.find("=") == -1:
                            if i + 1 < len(args):
                                old_args.append(arg)
                                old_args.append(args[i + 1])
                                skip[i + 1] = True
                        else:
                            old_args.append(arg)
                args = ["run"] + old_args
        return self.cmd.run(args, addi_args)