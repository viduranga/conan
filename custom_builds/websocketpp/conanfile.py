#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import tools, CMake

from forwardmeasure.conan_utils import ConfigurableConanFile

class ConanWebsocketpp(ConfigurableConanFile):
    (
        name,
        version,
        dependencies,
        exports,
    ) = ConfigurableConanFile.init_conan_config_params()
    exports += ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]

    author = "Prashanth Nandavanam<pnandavanam@bopttomline.com>"
    description = "Header only C++ library that implements RFC6455 The WebSocket Protocol"
    url = "https://github.com/bincrafters/conan-websocketpp"
    homepage = "https://github.com/zaphoyd/websocketpp"
   
    # Indicates License type of the packaged library
    license = 'BSD 3-Clause "New" or "Revised" License'                  
    generators = ["cmake"]
    default_options = {"asio": "boost"}

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "asio": ["boost", "standalone"],
    }
    default_options = {
        "asio": "boost"
    }

    zlib_reference = dependencies["zlib"]
    boost_reference = dependencies["boost"]
    asio_reference = dependencies["asio"]
    openssl_reference = dependencies["openssl"]

    def requirements(self):
        self.requires.add(self.openssl_reference)
        self.requires.add(self.zlib_reference)
        if self.options.asio == 'standalone':
            self.requires.add(self.asio_reference)
        else:
            self.requires.add(self.boost_reference)
    # Packages the license for the conanfile.py

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"

    def source(self):
        archive_name = "{0}-{1}".format(self.name, self.version)
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        os.rename(archive_name, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_TESTS'] = False
        cmake.definitions['BUILD_EXAMPLES'] = False
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="COPYING", dst="license", src=self._source_subfolder)
        # We have to copy the headers manually, since the current install() step
        # in the 0.8.1 release doesn't work with the cmake wrapper.
        self.copy(pattern="*.hpp", dst="include/websocketpp", src=self._source_subfolder + '/websocketpp')

    def package_id(self):
        self.info.header_only()