# Kratos Salome Plugin
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE) [![Github CI](https://github.com/philbucher/KratosSalomePlugin/workflows/Plugin%20CI/badge.svg)](https://github.com/philbucher/KratosSalomePlugin/actions) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6a94f3a9a36b409285fe6c27d8adf9d9)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=philbucher/KratosSalomePlugin&amp;utm_campaign=Badge_Grade)

Plugin for the [SALOME platform](https://www.salome-platform.org/) with which it can be used as preprocessor for the finite element programm [KratosMultiphysics](https://github.com/KratosMultiphysics/Kratos).

**Note:** This plugin is currently work in progress. Furthermore it is more research oriented, which means that the user has to have more knowledge of Kratos itself.
For a more consolidated solution please check the [GiD interface](https://github.com/KratosMultiphysics/GiDInterface).

**How does it work?**
This plugin is purely python based, which means that Salome does not have to be compiled. It is sufficient to download the binaries provided by Salome and set up the plugin by following the instructions in the next section.
The plugin works with meshes created in the *Mesh* module of Salome.

## Setup
  - Clone the repo

  - Windows
    - Add `SALOME_PLUGINS_PATH` pointing to the directory where the code was cloned to to the [Environment Variables](https://www.computerhope.com/issues/ch000549.htm)

  - Linux
    - export the `SALOME_PLUGINS_PATH` variable pointing to the directory where the code was cloned to, e.g.
    `export SALOME_PLUGINS_PATH="${HOME}/software/KratosSalomePlugin/plugin"`

  - In Salome: Click `Tools/Plugin/Kratos Multiphysics` in order to load the plugin.
    Newer versions of Salome (>= 9.3) have a small icon with which the plugin can be loaded:
    <img src="plugin/utilities/kratos_logo.png" width="24">

**Troubleshooting Salome**
  - Cannot save files on Windows:
    add "@SET SALOME_TMP_DIR=%TEMP%" at the end of "SALOME-8.2.0-WIN64\WORK\set_env.bat"

  - Installation on Ubuntu 18.04:
    - Problem:
        `SALOME_Session_Server: error while loading shared libraries: libicui18n.so.55: cannot open shared object file: No such file or directory`

        Download and install missing package: <https://www.ubuntuupdates.org/package/core/xenial/main/security/libicu55>

    - Problem:
        `SALOME_Session_Server: error while loading shared libraries: libpcre16.so.3: cannot open shared object file: No such file or directory`

        Install missing package:
        `sudo apt-get install libpcre16-3`

    - Problem:
        `SALOME_Session_Server: error while loading shared libraries: libpng12.so.0: cannot open shared object file: No such file or directory`

        Download and install missing package:
        1. `wget http://mirrors.kernel.org/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1_amd64.deb`
        2. `sudo dpkg -i libpng12-0_1.2.54-1ubuntu1_amd64.deb`

    - Problem: Meshing requires `libgfortran.so.3` but, gcc7 only has *.4

        `sudo apt-get install libgfortran3`

## Usage

## Examples
Examples for the plugin can be found under *plugin/applications/APP_NAME/examples*.
They can also be loaded inside the plugin after loading the corresponding application.

## Contributors

## Acknowledgements
