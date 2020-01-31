#  _  __         _          ___       _               ___ _           _
# | |/ /_ _ __ _| |_ ___ __/ __| __ _| |___ _ __  ___| _ \ |_  _ __ _(_)_ _
# | ' <| '_/ _` |  _/ _ (_-<__ \/ _` | / _ \ '  \/ -_)  _/ | || / _` | | ' \
# |_|\_\_| \__,_|\__\___/__/___/\__,_|_\___/_|_|_\___|_| |_|\_,_\__, |_|_||_|
#                                                               |___/
# License: BSD License ; see LICENSE
#
# Main authors: Philipp Bucher (https://github.com/philbucher)
#

# python imports
import unittest, sys, os

# plugin imports
sys.path.append(os.pardir) # required to be able to do "from plugin import xxx"
from plugin.utilities import utils

# tests imports
import testing_utilities

if utils.IsExecutedInSalome():
    # imports that have dependenices on salome, hence can only be imported if executed in salome
    import salome
    import GEOM
    import salome_study
    import plugin.utilities.salome_utilities as salome_utils


class TestSalomeTestCaseStudyCleaning(testing_utilities.SalomeTestCase):
    # test to make sure that the cleaning of studies between tests works correctly

    # the order of execution is not deterministic, hence we need a flag
    already_executed = False
    num_objs_in_study = None

    def setUp(self):
        super(TestSalomeTestCaseStudyCleaning, self).setUp()

        # create geometry
        O = self.geompy.MakeVertex(0, 0, 0)
        OX = self.geompy.MakeVectorDXDYDZ(1, 0, 0)
        OY = self.geompy.MakeVectorDXDYDZ(0, 1, 0)
        OZ = self.geompy.MakeVectorDXDYDZ(0, 0, 1)
        Box_1 = self.geompy.MakeBoxDXDYDZ(200, 200, 200)
        self.geompy.addToStudy( O, 'O' )
        self.geompy.addToStudy( OX, 'OX' )
        self.geompy.addToStudy( OY, 'OY' )
        self.geompy.addToStudy( OZ, 'OZ' )
        self.geompy.addToStudy( Box_1, 'Box_1' )

        # create mesh
        from salome.smesh import smeshBuilder
        Mesh_1 = self.smesh.Mesh(Box_1)
        Regular_1D = Mesh_1.Segment()
        Max_Size_1 = Regular_1D.MaxSize(34.641)
        MEFISTO_2D = Mesh_1.Triangle(algo=smeshBuilder.MEFISTO)
        NETGEN_3D = Mesh_1.Tetrahedron()
        isDone = Mesh_1.Compute()

        ## Set names of Mesh objects
        self.smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
        self.smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN 3D')
        self.smesh.SetName(MEFISTO_2D.GetAlgorithm(), 'MEFISTO_2D')
        self.smesh.SetName(Max_Size_1, 'Max Size_1')
        self.smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')

    def test_1(self):
        self.__CheckStudy()

    def test_2(self):
        self.__CheckStudy()

    def __CheckStudy(self):
        if TestSalomeTestCaseStudyCleaning.already_executed:
            # make sure the number of components is the same!
            current_num_objs_in_study = GetNumberOfObjectsInStudy(self.study)
            # if this check fails it means that the study was not cleaned, leftover objects exist!
            self.assertEqual(current_num_objs_in_study, TestSalomeTestCaseStudyCleaning.num_objs_in_study)
        else:
            TestSalomeTestCaseStudyCleaning.already_executed = True
            # if executed for the first time then count the components
            TestSalomeTestCaseStudyCleaning.num_objs_in_study = GetNumberOfObjectsInStudy(self.study)


def GetNumberOfObjectsInStudy(the_study):
    # adapted from python script "salome_study" in KERNEL py-scripts
    def GetNumberOfObjectsInComponent(SO):
        num_objs_in_comp = 0
        it = the_study.NewChildIterator(SO)
        while it.More():
            CSO = it.Value()
            num_objs_in_comp += 1 + GetNumberOfObjectsInComponent(CSO)
            it.Next()
        return num_objs_in_comp

    fct_args = []
    if salome_utils.GetVersionMajor() < 9:
        fct_args.append(the_study)
    # salome_study.DumpStudy(*fct_args) # for debugging

    itcomp = the_study.NewComponentIterator()
    num_objs_in_study = 0
    while itcomp.More(): # loop components (e.g. GEOM, SMESH)
        SC = itcomp.Value()
        num_objs_in_study += 1 + GetNumberOfObjectsInComponent(SC)
        itcomp.Next()
    return num_objs_in_study


class TestSalomeUtilities(testing_utilities.SalomeTestCaseWithBox):
    def test_IsMesh(self):
        meshes = [
            self.mesh_tetra.GetMesh()
        ]

        not_meshes = [
            self.mesh_tetra, # maybe this should be true ...?
            self.sub_mesh_tetra_f_1,
            self.sub_mesh_tetra_g_1,
            self.box,
            self.face_1,
            self.group_faces
        ]

        for mesh in meshes:
            self.assertTrue(salome_utils.IsMesh(mesh))

        for not_mesh in not_meshes:
            self.assertFalse(salome_utils.IsMesh(not_mesh))

    def test_IsSubMesh(self):
        sub_meshes = [
            self.sub_mesh_tetra_f_1,
            self.sub_mesh_tetra_g_1
        ]

        not_sub_meshes = [
            self.mesh_tetra,
            self.mesh_tetra.GetMesh(),
            self.box,
            self.face_1,
            self.group_faces
        ]

        for sub_mesh in sub_meshes:
            self.assertTrue(salome_utils.IsSubMesh(sub_mesh))

        for not_sub_mesh in not_sub_meshes:
            self.assertFalse(salome_utils.IsSubMesh(not_sub_mesh))

    def test_GetSalomeObject(self):
        if salome_utils.GetVersionMajor() < 9:
            self.skipTest("This test does not work with salome 8")

        object_id_list = [
            (salome.smesh.smeshBuilder.meshProxy, "0:1:2:3"),
            (salome.smesh.smeshBuilder.submeshProxy, "0:1:2:3:7:1"),
            (salome.smesh.smeshBuilder.submeshProxy, "0:1:2:3:10:1"),
            (GEOM._objref_GEOM_Object, "0:1:1:1"),
            (GEOM._objref_GEOM_Object, "0:1:1:1:1"),
            (GEOM._objref_GEOM_Object, "0:1:1:1:5")
        ]

        for obj_id in object_id_list:
            self.assertTrue(salome_utils.ObjectExists(obj_id[1]))
            self.assertEqual(obj_id[0], type(salome_utils.GetSalomeObject(obj_id[1]))) # the returned type is not correct in version 8

    def test_GetSalomeID(self):
        # this test might fail if salome orders the ids differently in different versions
        # it should not, since the order in which the objects are added is always the same
        object_id_list = [
            ("0:1:2:3", self.mesh_tetra.GetMesh()),
            ("0:1:2:3:7:1", self.sub_mesh_tetra_f_1),
            ("0:1:2:3:10:1", self.sub_mesh_tetra_g_1),
            ("0:1:1:1", self.box),
            ("0:1:1:1:1", self.face_1),
            ("0:1:1:1:5", self.group_faces)
        ]

        for obj_id in object_id_list:
            self.assertEqual(obj_id[0], self.GetSalomeID(obj_id[1], obj_id[0]))

    def test_GetObjectName(self):
        identifier = self.GetSalomeID(self.box, "0:1:1:1")
        self.assertEqual(salome_utils.GetObjectName(identifier), self.name_main_box)

        identifier = self.GetSalomeID(self.mesh_tetra.GetMesh(), "0:1:2:3")
        self.assertEqual(salome_utils.GetObjectName(identifier), self.name_main_mesh_tetra)

        identifier = self.GetSalomeID(self.sub_mesh_hexa_g_2, "0:1:2:4:10:2")
        self.assertEqual(salome_utils.GetObjectName(identifier), self.name_mesh_group)

    def test_ObjectExists(self):
        identifier = self.GetSalomeID(self.box, "0:1:1:1")
        self.assertTrue(salome_utils.ObjectExists(identifier))

        identifier = self.GetSalomeID(self.mesh_tetra.GetMesh(), "0:1:2:3")
        self.assertTrue(salome_utils.ObjectExists(identifier))

        identifier = self.GetSalomeID(self.sub_mesh_hexa_g_2, "0:1:2:4:10:2")
        self.assertTrue(salome_utils.ObjectExists(identifier))

        self.assertFalse(salome_utils.ObjectExists("0:1:2:4:10:2:1:1:4:7:8")) # random identifier, should not exist
        self.assertFalse(salome_utils.ObjectExists("0:15555")) # random identifier, should not exist


if __name__ == '__main__':
    unittest.main()
