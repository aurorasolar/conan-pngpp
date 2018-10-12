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

    def source(self):
        dl = 'http://download.savannah.nongnu.org/releases/pngpp'
        foldername = 'png++-%s' % self.version
        filename = '%s/%s.tar.gz' % (dl, foldername)
        tools.get(filename)
        os.rename(foldername, "png++")

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