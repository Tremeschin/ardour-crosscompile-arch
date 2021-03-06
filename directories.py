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

class Directories:
    def __init__(self, main):
        self.main = main

        self.PKGBUILDS = self.main.utils.ROOT + "PKGBUILDS/"

        self.workspace = self.main.utils.ROOT + "workspace/"
        self.runtime = self.workspace + "runtime/"
        self.ardour_32 = self.workspace + "ardour32/"
        self.ardour_64 = self.workspace + "ardour64/"

        self.bundle_32 = self.workspace + "ardour_bundle_32/"
        self.bundle_64 = self.workspace + "ardour_bundle_64/"

        self.lv2_bundled_32 = self.bundle_32 + "lv2/"
        self.lv2_bundled_64 = self.bundle_64 + "lv2/"
        # Runtime