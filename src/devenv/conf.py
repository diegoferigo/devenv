import os
import sys
import pwd
import yaml
import pathlib
import getpass
import subprocess

from devenv.exception import MissingOption
from devenv.exception import WrongOptionType


def loadfile(config_filename):
    with open(config_filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def split(config):
    if "devenv" not in config:
        sys.exit("The yaml file does not contain a 'devenv' key")
    return config.pop("devenv"), config


def process(compose_service, devenv_service):
    for option in devenv_service:
        processor = DevenvConfProcessor(devenv_service, compose_service)
        compose_service = processor.process(option)


class DevenvConfProcessor():
    def __init__(self, devenv_conf, compose_conf):
        self.devenvconf = devenv_conf
        self.composeconf = compose_conf

    def process(self, key):
        """Dispatch method.

        This method processes all the devenv options by calling the
        associated method.
        """
        fcn = getattr(self, "_process_" + key)
        fcn()
        return self.composeconf

    # ===========================
    # PROCESS DEVENV YAML OPTIONS
    # ===========================

    def _process_user(self):
        user = self.devenvconf["user"]

        if isinstance(user, dict):
            try:
                self._child_must_exist(user, "name", str)
                self._child_must_exist(user, "uid", (int, str))
                self._child_must_exist(user, "gid", (int, str))

                name = self._eval_in_shell(user["name"])

                if isinstance(user["uid"], str):
                    uid = self._eval_in_shell(user["uid"])
                else:
                    uid = user["uid"]

                if isinstance(user["gid"], str):
                    gid = self._eval_in_shell(user["gid"])
                else:
                    gid = user["gid"]

                self._add_environment_var("USERNAME=" + name)
                self._add_environment_var("USER_UID=" + str(uid))
                self._add_environment_var("USER_GID=" + str(gid))
            except MissingOption:
                print("While processing 'user' element")
                raise
                sys.exit()
            except WrongOptionType:
                print("While processing 'user' element")
                raise
                sys.exit()
        elif isinstance(user, str):
            try:
                user = self._eval_in_shell(user)
                userdata = pwd.getpwnam(user)
                self._add_environment_var("USERNAME=" + userdata.pw_name)
                self._add_environment_var("USER_UID=" + str(userdata.pw_uid))
                self._add_environment_var("USER_GID=" + str(userdata.pw_gid))
            except Exception:
                print("While processing 'user' element")
                raise
                sys.exit()
        else:
            raise Exception("Element 'user' must be either a dict or a str")

    def _process_project_dir(self):
        project_dir = self.devenvconf["project_dir"]
        project_dir = self._eval_in_shell(project_dir)

        if not isinstance(project_dir, str):
            raise WrongOptionType("project_dir", str)
        self._add_volume(project_dir)

    def _process_resources(self):
        resources = self.devenvconf["resources"]

        if not isinstance(resources, dict):
            raise WrongOptionType("project_dir", dict)

        if "directories" in resources:
            if not isinstance(resources["directories"], list):
                raise WrongOptionType("directories", list)
            for directory in resources["directories"]:
                directory = self._eval_in_shell(directory)
                self._add_volume(directory)

        if "files" in resources:
            if not isinstance(resources["files"], list):
                raise WrongOptionType("files", list)
            for file in resources["files"]:
                file = self._eval_in_shell(file)
                self._add_volume(file, is_file=True)

    def _process_gpu(self):
        gpu = self.devenvconf["gpu"]
        gpu = self._eval_in_shell(gpu)

        if not isinstance(gpu, str):
            raise WrongOptionType("gpu", str)

        if gpu == "intel":
            self._add_device("/dev/dri")
            self._add_volume("/dev/shm")
            self._set_runtime("runc")
        elif gpu == "nvidia":
            self._add_device("/dev/dri")
            self._set_runtime("nvidia")
        else:
            raise Exception("gpu '" + gpu + "' not supported")

    def _process_matlab(self):
        matlab = self.devenvconf["matlab"]
        
        if not isinstance(matlab, dict):
            raise WrongOptionType("matlab", dict)

        try:
            self._child_must_exist(matlab, "folder", str)
            self._child_must_exist(matlab, "dotdir", str)

            matlabfolder = self._eval_in_shell(matlab["folder"])
            matlabdotdir = self._eval_in_shell(matlab["dotdir"])

            if not pathlib.Path(matlabfolder).exists():
                raise Exception(
                    "Matlab folder '" + matlabfolder + "'does not exist")

            self._add_volume(matlabfolder + ":/usr/local/MATLAB:rw")
            self._add_volume(matlabdotdir)
            self._add_environment_var("Matlab_ROOT_DIR=/usr/local/MATLAB")

            if "mac" in matlab:
                mac = self._eval_in_shell(matlab["mac"])

                if not isinstance(mac, str):
                    raise WrongOptionType("mac", str)
                if self._is_mac_address(mac):
                    self._set_mac(mac)
                else:
                    macaddr = self._getmac(mac)
                    self._set_mac(macaddr)

        except MissingOption:
            print("While processing 'user' element")
            raise
            sys.exit()
        except WrongOptionType:
            print("While processing 'user' element")
            raise
            sys.exit()

    def _process_init(self):
        init = self.devenvconf["init"]
        init = self._eval_in_shell(init)

        if not isinstance(init, str):
            raise WrongOptionType("init", str)

        if init == "systemd":
            self._set_init("/sbin/init")
            self._add_volume("/sys/fs/cgroup")
            self._add_tmpfs("/run")  # TODO: check if duplicate
            self._add_tmpfs("/run/lock")
            self._add_cap("SYS_ADMIN")
            self._set_stopsignal("SIGRTMIN+3")
            #self._set_detached(True) # TODO:

    def _process_gdb(self):
        gdb = self.devenvconf["gdb"]

        if not(gdb, bool):
            raise WrongOptionType("gdb", bool)

        if gdb:
            # self._add_cap("SYS_ADMIN")
            self._add_cap("SYS_PTRACE")  # TODO:
            # self._add_security("seccomp:unconfined")

    def _process_x11(self):
        x11 = self.devenvconf["x11"]
        x11 = self._eval_in_shell(x11)

        if not isinstance(x11, str):
            raise WrongOptionType("x11", str)

        if x11 == "xhost":
            self._add_volume("/tmp/.X11-unix")
            self._add_environment_var("DISPLAY")
            # TODO: any better method? Such as a pre-start hook?
            #       Split docker create and docker start?
            if subprocess.call("xhost +si:locahost:" + getpass.getuser()) != 0:
                raise Exception("Failed to grant current user the xhost rights")

        elif x11 == "xauth":
            # Create xauthority file
            self._create_xauth(self._get_xauth_filename())
            self._add_volume(self._get_xauth_filename(), is_file=True)
            self._add_volume("/tmp/.X11-unix")
            self._add_environment_var("DISPLAY")
            self._add_environment_var("XAUTHORITY=" + self._get_xauth_filename())

    def _process_git(self):
        git = self.devenvconf["git"]

        if not isinstance(git, dict):
            raise WrongOptionType("git", dict)

        try:
            self._child_must_exist(git, "username", str)
            self._child_must_exist(git, "email", str)

            git_username = self._eval_in_shell(git["username"])
            git_email = self._eval_in_shell(git["email"])

            self._add_environment_var("GIT_USER_NAME=" + git_username)
            self._add_environment_var("GIT_USER_EMAIL=" + git_email)
            # TODO: gpg
        except MissingOption:
            print("While processing 'git' element")
            raise
            sys.exit()
        except WrongOptionType:
            print("While processing 'git' element")
            raise
            sys.exit()

    # ==============
    # HELPERS _add_*
    # ==============

    def _add_environment_var(self, var):
        if "environment" not in self.composeconf:
            self.composeconf["environment"] = list()
        self.composeconf["environment"].append(var)

    def _add_volume(self, volume, is_file=False):
        # Expand env variables
        volume = os.path.expandvars(volume)

        # Split volume components
        [volume, destination, mode] = self._split_volume(volume)

        # Expand the folder if ~ is used
        path = pathlib.Path(volume).expanduser()

        # Check if the volume is a folder or a file
        if is_file:
            # Create the parent directory if it does not exist
            pathlib.Path(volume).parent.mkdir(parents=True, exist_ok=True)

            # Create the file if it does not exist
            pathlib.Path(volume).touch(exist_ok=True)
        else:
            # Create the directory if it does not exist
            pathlib.Path(volume).mkdir(parents=True, exist_ok=True)

        if "volumes" not in self.composeconf:
            self.composeconf["volumes"] = list()

        self.composeconf["volumes"].append(
            str(path) + ":" + str(destination) + ":" + mode)

    def _add_device(self, device):
        if not pathlib.Path(device).exists():
            raise Exception("Device '" + device + "' does not exist")

        if "devices" not in self.composeconf:
            self.composeconf["devices"] = list()

        self.composeconf["devices"].append(device)

    def _add_tmpfs(self, tmpfs):
        if "tmpfs" not in self.composeconf:
            self.composeconf["tmpfs"] = list()

        self.composeconf["tmpfs"].append(tmpfs)

    def _add_cap(self, cap):
        if "cap_add" not in self.composeconf:
            self.composeconf["cap_add"] = list()

        self.composeconf["cap_add"].append(cap)

    def _add_security(self, security):
        if "security_opt" not in self.composeconf:
            self.composeconf["security_opt"] = list()

        self.composeconf["security_opt"].append(security)

    # ==============
    # HELPERS _set_*
    # ==============

    def _set_runtime(self, runtime):
        if "runtime" in self.composeconf:
            raise Exception("A runtime is already set")
        self.composeconf["runtime"] = runtime

    def _set_mac(self, mac):
        if "mac_address" in self.composeconf:
            raise Exception("A mac address is already set")
        self.composeconf["mac_address"] = mac

    def _set_init(self, init):
        self.composeconf["init"] = init

    def _set_stopsignal(self, signal):
        self.composeconf["stop_signal"] = signal

    # =============
    # OTHER HELPERS
    # =============

    @staticmethod
    def _child_must_exist(root, option, typeid=None):
        if option not in root:
            raise MissingOption(option)
        if typeid is not None:
            if not isinstance(root[option], typeid):
                raise WrongOptionType(option, typeid)

    @staticmethod
    def _eval_in_shell(cmd):
        cmd = os.path.expandvars(cmd)

        if isinstance(cmd, str):
            if cmd[0] == "$" and cmd[1] == "(" and cmd[-1] == ")":
                stdout = subprocess.run(cmd[2:-1].split(), stdout=subprocess.PIPE).stdout
                return stdout.decode().rstrip()
            else:
                return cmd


    def _get_xauth_filename(self):
        # TODO: check container_name if present
        return "/tmp/." + self.composeconf["container_name"] + ".xauth"

    def _split_volume(self, volume):
        volume_components = volume.split(":")

        if len(volume_components) == 1:
            return volume_components[0], volume_components[0], "rw"
        elif len(volume_components) == 2:
            return volume_components[0], volume_components[1], "rw"
        else:
            return \
                volume_components[0], \
                volume_components[1], \
                volume_components[2]

    def _create_xauth(self, xauth_filename):
        # Remove leftovers from previous runs
        self._remove_xauth(xauth_filename)

        # Create the file
        xauth = pathlib.Path(xauth_filename)
        xauth.touch()

        # Populate the file
        cmd = "xauth nlist $DISPLAY |\
               grep -v ffff |\
               sed -e 's/^..../ffff/' |\
               xauth -f " + xauth_filename + " nmerge -"

        if subprocess.call(cmd, shell=True) != 0:
            raise Exception(
                "Failed to populate xauth file '" + xauth_filename + "'")

    def _remove_xauth(self, xauth_filename):
        xauth = pathlib.Path(xauth_filename)
        if xauth.exists():
            xauth.unlink()

    def _getmac(self, interface):
        try:
            mac = open('/sys/class/net/'+interface+'/address').readline()
        except Exception:
            raise Exception("Interface '" + interface + "' not found")
        return mac[0:17]

    def _is_mac_address(self, mac):
        components = mac.split(":")
        if len(components) != 6:
            return False
        for component in components:
            if len(component) != 2:
                return False
        return True
