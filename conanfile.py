import os

from conans import ConanFile, tools


class PngConan(ConanFile):
    name = "pngpp"
    version = "0.2.7"
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
        foldername = 'png++-%s' % self.version
        filename = '%s/%s.tar.gz' % (dl, foldername)
        tools.get(filename)
        os.rename(foldername, "png++")

        self.patch_strerror("png++")
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