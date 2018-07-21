import os

from conans import ConanFile, tools


class PngConan(ConanFile):
    name = "png++"
    version = "0.2.9"
    settings = "compiler"
    requires = 'libpng/1.6.34@bincrafters/stable'
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Png here>"
    no_copy_source = True
    # No settings/options are necessary, this is header only
    foldername = '%s-%s' % (name, version)

    def patch_vs(self, d):
        with open("%s/error.hpp"%d, 'r') as f:
            lines = f.readlines()
        N = 108-1
        print(lines[N])
        assert(lines[N] == '''            return std::string(strerror_r(errnum, buf, ERRBUF_SIZE));\n''')
        lines[N] = '''            return std::string(std::strerror(errnum));\n'''
        with open("%s/error.hpp"%d, 'w') as f:
            lines = f.writelines(lines)


    def source(self):
        '''retrieval of the source code here. Remember you can also put the code
        in the folder and use exports instead of retrieving it with this
        source() method
        '''
        dl = 'http://download.savannah.nongnu.org/releases/pngpp'
        filename = '%s/%s.tar.gz' % (dl, self.foldername,)
        tools.get(filename)
        os.rename(self.foldername, self.name)

        if self.settings.compiler == "Visual Studio":
            self.patch_vs(self.name)
        # self.run("git clone ...") or
        # tools.download("url", "file.zip")
        # tools.unzip("file.zip" )

    def package(self):
        self.copy("%s/*.hpp"%self.name, "include")

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.includes = ["include"]