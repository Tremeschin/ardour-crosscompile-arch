"""
MIT License

Copyright (c) 2020 Tremeschin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pyunpack import Archive
import neotermcolor
import subprocess
import zipfile
import shutil
import sys
import os

cprint = neotermcolor.cprint

# Set neotermcolor styles
neotermcolor.set_style('a', color='magenta', attrs='bold') # Action
neotermcolor.set_style('e', color='red',     attrs='bold') # Error
neotermcolor.set_style('w', color='yellow',  attrs='bold') # Warning
neotermcolor.set_style('i', color='cyan',    attrs='bold') # Info
neotermcolor.set_style('q', color='yellow',  attrs='bold') # Question
neotermcolor.set_style('c', color='blue',    attrs='bold') # Check
neotermcolor.set_style('o', color='green',   attrs='bold') # Ok


# Intents for printing pretty stuff
class Indents:
    ACTION =   "\n\n  >> text\n"
    ERROR =    "[## ERROR ##] text"
    WARNING =  "[WARNING] :: text"
    INFO =     "[INFO] text"
    QUESTION = " > text:"
    CHECK =    "[CHECKING] text"
    OK =       "[OK] text"


# Utilities class
class Utils:
    def __init__(self, main):
        self.main = main
        self.ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
    
    # (S)tyled (print) with indents
    def sprint(self, text: str, style="info") -> None:
        # Defaults and indents
        indent = {
            "a": Indents.ACTION,
            "e": Indents.ERROR,
            "w": Indents.WARNING,
            "q": Indents.QUESTION,
            "c": Indents.CHECK,
            "o": Indents.OK,
        }.get(style[0], Indents.INFO)
        
        cprint(indent.replace("text", text), style=style)

    # Make directory if doesn't exist
    def mkdir_dne(self, path: str, check: bool = True) -> None:
        
        # Warn "checking" for the user
        self.sprint(f"MKDIR DNE [{path}]", 'c')

        # Does directory already exist?
        if not os.path.exists(path):
            self.sprint(f"Directory doesn't exist, creating", 'w')
            os.makedirs(path)
            if check:
                if not os.path.exists(path):
                    self.sprint(f"Could NOT create directory [{path}]", 'e')
                    sys.exit(-1)
            self.sprint("Directory created successfully!!", 'o')
        else:
            # Path already exist
            self.sprint("Path already exists", 'o')
    
    # Delete a directory and its contents
    def rmdir(self, path: str) -> None:

        # Warn "checking" for the user
        self.sprint(f"RMDIR [{path}]", 'c')
        
        if os.path.isdir(path):

            # Delete the directory
            shutil.rmtree(path, ignore_errors=True)
            
            # Directory still exists? Ew, error
            if os.path.isdir(path):
                self.sprint(f"Tried to remove directory [{path}] but still exists", 'e')
                sys.exit(-1)
        else:
            self.sprint("Directory doesn't exist, skipping...", 'o')

    # Same as `sed -i "s/old/new/g" path`
    def sed_replace(self, old: str, new: str, path: str) -> None:

        self.sprint(f"Replacing [ \"{old}\" ] --> [ \"{new}\" ] on file [{path}]", 'i')
        
        # Read every line of original file
        with open(path, "r") as f:
            data = [line for line in f]
        
        # Replace every line from old to new
        data = [line.replace(old, new) for line in data]
        
        # Overwrite the file with new replaced values
        with open(path, "w") as f:
            for line in data:
                f.write(line)

    # Get the environment vars modified with env_vars dict
    def custom_env(self, env_vars: dict) -> dict:
        env = os.environ.copy()
        for env_var in env_vars.keys():
            env[env_var] = env_vars[env_var]
        return env

    # Unzip a file and save to a dst dir
    def unzip(self, src: str, dst: str, mkdir_dne=True) -> None:
        
        self.sprint(f"Extracting [{src}] zip to directory [{dst}]", 'i')

        # Make dir if doesn't exist
        if mkdir_dne:
            self.mkdir_dne(dst)
        
        # Extract it
        with zipfile.ZipFile(src, 'r') as f:
            f.extractall(dst)
        
    # Extract a compressed file (more generic)
    def extract_file(self, src, dst):
        self.sprint(f"Extracting [{src}] zip to directory [{dst}]", 'i')
        Archive(src).extractall(dst)


# Python's subprocess utilities because I'm lazy remembering things
class SubprocessUtils:
    def __init__(self, main):
        self.main = main

    # Get the commands from a list to call the subprocess
    def from_list(self, cmd_list):
        self.main.utils.sprint(f"Creating subprocess from list {cmd_list}", 'i')
        self.command = cmd_list
        self.name = cmd_list[0]

    # Get the command from a string (for shell=True calls)
    def from_string(self, string):
        self.main.utils.sprint(f"Creating subprocess from string [{string}]", 'i')
        self.command = string
        self.name = string.split(" ")[0]

    # Run the subprocess with or without a env / working directory
    def run(self, working_directory=None, env=None, shell=False):

        self.main.utils.sprint(f"Run SubprocessUtils with name [{self.name}]", "i")
        
        # Copy the environment if nothing was changed and passed as argument
        if env is None:
            env = os.environ.copy()
        
        # Runs the subprocess based on if we set or not a working_directory
        if working_directory == None:
            self.process = subprocess.call(
                self.command,
                env=env,
                shell=shell
            )
        else:
            self.process = subprocess.call(
                self.command,
                env=env,
                cwd=working_directory,
                shell=shell
            )

    # Wait until the subprocess has finished
    def wait(self):
        self.main.utils.sprint(f"Waiting SubprocessUtils with name [{self.name}] to finish", "i")
        self.process.wait()
        self.main.utils.sprint(f"SubprocessUtils [{self.name}] finished", "o")

    # Kill subprocess
    def terminate(self):
        self.main.utils.sprint(f"Terminating SubprocessUtils with name [{self.name}]", "w")
        self.process.terminate()
        self.main.utils.sprint(f"Terminated subprocess", "o")

    # See if subprocess is still running
    def is_alive(self):

        # Get the status of the subprocess
        status = self.process.poll()

        # None? alive
        if status == None:
            self.main.utils.sprint(f"SubprocessUtils with name [{self.name}] is alive", "i")
            return True
        else:
            self.main.utils.sprint(f"SubprocessUtils with name [{self.name}] is not alive", "w")
            return False