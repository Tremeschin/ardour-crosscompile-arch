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

from config import *

class Actions:
    def __init__(self, main):
        self.main = main

    def run(self):
        if CLONE_ARDOUR:
            self.main.utils.sprint("CLONE_ARDOUR", 'a')
            self.main.download.git_clone("https://github.com/Ardour/ardour", self.main.directories.ardour)
        
        if PULL_ARDOUR:
            self.main.utils.sprint("PULL_ARDOUR", 'a')
            raise NotImplementedError

        if CHECK_NEEDED_PACKAGES:
            self.main.utils.sprint("CHECK_NEEDED_PACKAGES", 'a')
            self.main.pacman.get_installed_packages()
            self.main.pacman.requirements.check_installed()

        if FIX_CREATE_HARD_LINK_A:
            self.main.utils.sprint("FIX_CREATE_HARD_LINK_A", 'a')
            # Mingw can't seem to find this
            self.main.utils.sed_replace(
                "return CreateHardLinkA (new_path.c_str(), existing_file.c_str(), NULL);",
                "return false;",
                self.main.directories.ardour + "/libs/pbd/file_utils.cc"
            )
        
        if FIX_FFTW:
            self.main.utils.sprint("FIX_FFTW", 'a')
            # FFTW threads can't be imported with -lfftw3_threads
            self.main.utils.sed_replace(
                "fftwf_make_planner_thread_safe ();",
                "void fftwf_make_planner_thread_safe ();",
                self.main.directories.ardour + "/libs/pbd/file_utils.cc"
            )