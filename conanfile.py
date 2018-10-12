import os

from conans import ConanFile, tools


class PngConan(ConanFile):
    name = "pngpp"
    version = "0.2.5"
    settings = "compiler", "os"
    requires = 'libpng/1.6.34@bincrafters/stable'
    homepage = "http://www.nongnu.org/pngpp/"
    url = "https://github.com/Artalus/conan-pngpp"
    license = "http://www.nongnu.org/pngpp/license.html"
    exports = ["COPYING"]
    description = "png++: a C++ wrapper library for libpng"
    no_copy_source = True
    # No settings/options are necessary, this is header only

    def patch_strerror(self, d):
        with open("%s/error.hpp"%d, 'r') as f:
            lines = f.readlines()
        N = 34-1
        print(lines[N])
        assert(lines[N] == '''#include <stdexcept>\n''')

        lines.insert(N, '''#include <cstring>\n''')
        with open("%s/error.hpp"%d, 'w') as f:
            lines = f.writelines(lines)

    def patch_win32(self, d):
        if self.settings.compiler != "Visual Studio":
            return

        with open("%s/config.hpp"%d, 'r') as f:
            lines = f.readlines()
        N = 39-1
        print(lines[N])
        assert(lines[N] == '''#elif defined(__WIN32)\n''')

        lines[N] = '''#elif defined(_WIN32)\n'''
        with open("%s/config.hpp"%d, 'w') as f:
            lines = f.writelines(lines)


    def source(self):
        dl = 'http://download.savannah.nongnu.org/releases/pngpp'
        foldername = 'png++-%s' % self.version
        filename = '%s/%s.tar.gz' % (dl, foldername)
        tools.get(filename)
        os.rename(foldername, "png++")

        self.patch_strerror("png++")
        self.patch_win32("png++")
        # self.run("git clone ...") or
        # tools.download("url", "file.zip")
        # tools.unzip("file.zip" )

    def package(self):
        self.copy("png++/*.hpp", "include")
        self.copy("copying", "licenses", src="png++")

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.includes = ["include"]
