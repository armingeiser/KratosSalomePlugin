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
Main Window of the Plugin.
From here other functionalities can be called.
Loosely follows the MVC / PAC pattern, see plugin_controller
"""

# python imports
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

# plugin imports
from kratos_salome_plugin.utilities import GetAbsPathInPlugin
from kratos_salome_plugin.gui.base_window import BaseWindow


class PluginMainWindow(BaseWindow):
    def __init__(self):
        super().__init__(Path(GetAbsPathInPlugin("gui", "ui_forms", "plugin_main_window.ui")))

    def closeEvent(self, event):
        """prevent the window from closing, only hiding it
        Note that this deliberately does not call the baseclass, as the event should be ignored
        """
        logger.debug("Hiding %s", self.__class__.__name__)

        event.ignore()
        self.hide()


# for testing / debugging
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = PluginMainWindow()
    win.ShowOnTop()
    # win.StatusBarWarning("Obacht")
    win.StatusBarInfo("hey")
    sys.exit(app.exec_())
