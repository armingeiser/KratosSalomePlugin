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
This file contains functions for interacting with the Salome Study
NOTE: This file must NOT have dependencies on other files in the plugin!
(except utilities)
"""

# python imports
import os
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

# plugin imports
from .utilities import PathCheck

# salome imports
from salome import myStudy


def GetNumberOfObjectsInComponent(component) -> int:
    """Counts the number of objects in a component (e.g. GEOM, SMESH)
    adapted from "KERNEL/lib/python3.6/site-packages/salome/salome_study.py"
    """
    num_objs_in_comp = 0
    it = myStudy.NewChildIterator(component)
    while it.More():
        component_child = it.Value()
        num_objs_in_comp += 1 + GetNumberOfObjectsInComponent(component_child) # +1 bcs recursion
        it.Next()
    return num_objs_in_comp

def GetNumberOfObjectsInStudy() -> int:
    """Counts the number of objects in the study, for all components
    adapted from "KERNEL/lib/python3.6/site-packages/salome/salome_study.py"
    """
    # myStudy.DumpStudy() # for debugging

    itcomp = myStudy.NewComponentIterator()
    num_objs_in_study = 0
    while itcomp.More(): # loop components (e.g. GEOM, SMESH)
        component = itcomp.Value()
        num_objs_in_study += GetNumberOfObjectsInComponent(component)
        itcomp.Next()
    return num_objs_in_study

def IsStudyModified() -> bool:
    """returns whether the study has unsaved modifications
    see https://docs.salome-platform.org/latest/tui/KERNEL/kernel_salome.html
    """
    return myStudy.GetProperties().IsModified()

def SaveStudy(file_path: Path) -> bool:
    """saves the study as a single file, non-ascii
    returns whether saving the study was successful
    see https://docs.salome-platform.org/latest/tui/KERNEL/kernel_salome.html
    """
    PathCheck(file_path)

    file_path = file_path.with_suffix(".hdf") # if necessary change suffix to ".hdf"

    if file_path.is_file():
        logger.debug('File "%s" exists already and will be overwritten', file_path)

    # create folder if necessary
    # required bcs otherwise Salome an crash if the folder to save the study in does not yet exist
    if not file_path.parent.is_dir():
        os.makedirs(file_path.parent)

    try:
        save_successful = myStudy.SaveAs(str(file_path), False, False) # args: use_multifile, use_acsii
        if save_successful and not file_path.is_file(): # make sure the file was actually created!
            save_successful = False
            logger.critical('Salome sucessfully saved study but study file was not created: "%s"!', file_path)
    except BaseException as e: # catch all exceptions
        save_successful = False
        logger.error('Exception when saving study: "%s"', e)

    if save_successful:
        logger.debug('Study was saved with path: "%s"', file_path)
    else:
        logger.critical('Study could not be saved with path: "%s"', file_path)

    return save_successful

def OpenStudy(file_path: Path) -> bool:
    """opens a study
    returns whether opening the study was successful
    see https://docs.salome-platform.org/latest/tui/KERNEL/kernel_salome.html
    """
    PathCheck(file_path)

    if not file_path.is_file():
        raise FileNotFoundError('File "{}" does not exist!'.format(file_path))

    if file_path.suffix != ".hdf":
        logger.warning('Opening study from file without ".hdf" extension: "%s"',file_path)

    if IsStudyModified() and GetNumberOfObjectsInStudy() > 0:
        logger.warning('Opening study when current study has unsaved changes')

    try:
        open_successful = myStudy.Open(str(file_path))
    except BaseException as e: # catch all exceptions
        open_successful = False
        logger.error('Exception when opening study: "%s"', e)

    if open_successful:
        logger.debug('Study was openend from path: "%s"', file_path)
    else:
        logger.critical('Study could not be opened from path: "%s"', file_path)

    return open_successful

def ResetStudy() -> None:
    """resets the study, no objects are left afterwards
    see https://docs.salome-platform.org/latest/tui/KERNEL/kernel_salome.html
    """
    logger.debug("Resetting Study")
    myStudy.Clear()
    myStudy.Init()
