#  _  __         _          ___       _               ___ _           _
# | |/ /_ _ __ _| |_ ___ __/ __| __ _| |___ _ __  ___| _ \ |_  _ __ _(_)_ _
# | ' <| '_/ _` |  _/ _ (_-<__ \/ _` | / _ \ '  \/ -_)  _/ | || / _` | | ' \
# |_|\_\_| \__,_|\__\___/__/___/\__,_|_\___/_|_|_\___|_| |_|\_,_\__, |_|_||_|
#                                                               |___/
# License: BSD License ; see LICENSE
#
# Main authors: Philipp Bucher (https://github.com/philbucher)
#

"""
The ProjectManager takes care of the project, i.e. it handles the Groups and the Application.
It can save and open projects
"""

# python imports
from pathlib import Path
from os import makedirs
import sys
import json
import time
import logging
logger = logging.getLogger(__name__)

# plugin imports
from ..version import GetVersions as GetVersionsPlugin
from kratos_salome_plugin.utilities import PathCheck
from kratos_salome_plugin.salome_utilities import GetVersions as GetSalomeVersions
from kratos_salome_plugin.salome_study_utilities import SaveStudy, OpenStudy
from kratos_salome_plugin.gui.groups_model import GroupsModel


class ProjectManager:
    def __init__(self):
        self.__InitializeMembers()

    def SaveProject(self, save_path: Path) -> bool:
        """save the current project under the given path"""
        PathCheck(save_path)

        save_path = save_path.with_suffix(".ksp") # if necessary change suffix to ".ksp"

        logger.debug('Saving project: "%s" ...', save_path)

        if save_path.is_dir():
            logger.debug('Project "%s" exists already, the plugin related data will be overwritten', save_path)
        else:
            makedirs(save_path)

        # save study
        salome_study_path = save_path / "salome_study.hdf"
        save_successful = SaveStudy(salome_study_path)

        # save plugin data
        project_dict = {"general":{}}

        # general information
        general = project_dict["general"]
        general["version_plugin"] = GetVersionsPlugin()
        general["version_salome"] = GetSalomeVersions()

        localtime = time.asctime( time.localtime(time.time()) )
        general["creation_time"] = localtime

        general["operating_system"] = sys.platform

        # groups
        project_dict["groups"] = self.groups_model.Serialize()

        # application
        if self.application:
            serializing_successful, serialized_app = self.application.Serialize()
            save_successful = save_successful and serializing_successful
            project_dict["application"] = {}
            project_dict["application"]["application_module"] = mod(self.application) # necessary for deserialization
            project_dict["application"]["application_data"] = serialized_app

        # dump to json
        plugin_data_path = save_path / "plugin_data.json"
        with open(plugin_data_path, "w") as data_file:
            json.dump(project_dict, data_file, indent=4)

        logger.debug("Saved project")

        return save_successful

    def OpenProject(self, open_path: Path) -> bool:
        """open a project from the given path"""
        PathCheck(open_path)

        logger.info('opening project: "%s" ...', open_path)

        # check the necessary files exist
        if not open_path.is_dir():
            raise NotADirectoryError('Attempting to open project "{}" failed, it does not exist!'.format(open_path))

        salome_study_path = open_path / "salome_study.hdf"
        plugin_data_path = open_path / "plugin_data.json"

        if not salome_study_path.is_file():
            raise FileNotFoundError('Salome study does not exist in project "{}"'.format(open_path))

        if not plugin_data_path.is_file():
            raise FileNotFoundError('Plugin data file does not exist in project "{}"'.format(open_path))

        # clean leftovers
        self.__InitializeMembers()

        # open study
        open_successful = OpenStudy(salome_study_path)

        with open(plugin_data_path, 'r') as plugin_data_file:
            plugin_data = json.load(plugin_data_file)

        # check versions
        # this might be useful in the future for backwards compatibility
        logger.info("Version plugin: %s",    plugin_data["general"]["version_plugin"])
        logger.info("Salome plugin: %s",     plugin_data["general"]["version_salome"])
        logger.info("Creation time: %s",     plugin_data["general"]["creation_time"])
        logger.debug("Operating system: %s", plugin_data["general"]["operating_system"])

        # loading groups
        self.groups_model.Deserialize(plugin_data["groups"])

        if "application" in plugin_data:
            application_module_name = plugin_data["application"]["application_module"]
            logger.info('loading application from module: "%s"', application_module_name)
            application_module = __import__(application_module_name) # TODO use importlib
            self.application = application_module.Create()
            open_successful = open_successful and self.application.Deserialize(plugin_data["application"]["application_data"])

        logger.info("opened project")

        return open_successful

    def ProjectHasUnsavedChanges(self) -> bool:
        # check if study is empty
        # if not empty check if is modified
        # if is modified then ask if proceed

        # check Salome Study
        # is modified?
        # number of things in study => if nothing is there I don't need to check anything

        # check GroupsManager

        # check Application

        return False

    def __InitializeMembers(self) -> None:
        self.groups_model = GroupsModel()
        self.application = None
