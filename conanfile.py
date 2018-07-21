import os

from conans import ConanFile, tools


class PngConan(ConanFile):
    name = "pngpp"
    version = "0.2.9"
    settings = "compiler", "os"
    requires = 'libpng/1.6.34@bincrafters/stable'
    license = "<Put the package license here>"
    url = "https://github.com/Artalus/conan-pngpp"
    description = "png++: a C++ wrapper library for libpng"
    no_copy_source = True
    # No settings/options are necessary, this is header only
    foldername = 'png++-%s' % version

    def patch_strerror(self, d):
        if self.settings.compiler != "Visual Studio" and self.settings.os != "Macos":
            return

        with open("%s/error.hpp"%d, 'r') as f:
            lines = f.readlines()
        N = 108-1
        print(lines[N])
        assert(lines[N] == '''            return std::string(strerror_r(errnum, buf, ERRBUF_SIZE));\n''')

        lines[N] = '''            return std::string(std::strerror(errnum));\n'''
        with open("%s/error.hpp"%d, 'w') as f:
            lines = f.writelines(lines)


    def source(self):
        dl = 'http://download.savannah.nongnu.org/releases/pngpp'
        filename = '%s/%s.tar.gz' % (dl, self.foldername,)
        tools.get(filename)
        os.rename(self.foldername, "png++")

        self.patch_strerror("png++")
        # self.run("git clone ...") or
        # tools.download("url", "file.zip")
        # tools.unzip("file.zip" )

    def package(self):
        self.copy("png++/*.hpp", "include")

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.includes = ["include"]