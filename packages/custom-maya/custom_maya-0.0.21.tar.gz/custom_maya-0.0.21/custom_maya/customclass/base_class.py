import os

import maya.OpenMaya as om
import maya.cmds as cmds

import custom_maya


class CustomObjectBase(object):
    def __init__(self):
        # 储存所有属性的字典
        self.__custom_properties = {}
        # 储存所有信息的字典
        self.__custom_data = {}

    def add_property_to_custom_properties(self, d1):
        self.__custom_properties = {**self.__custom_properties, **d1}

    def get_custom_properties(self):
        return self.__custom_properties


class CustomObject(CustomObjectBase):
    def __init__(self):
        super().__init__()


class CustomScene(CustomObject):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__file_path = ''
        self.__full_path = os.path.normpath(self.__file_path)
        self.__scene_type = ''

    def get_file_details(self):
        return {
            'SceneName': self.get_scene_name(),
            'FullPath': self.get_file_path(),
        }

    def __update_data(self):

        self.add_property_to_custom_properties(
            {
                'SceneName': self.get_scene_name(),
                'FullPath': self.get_file_path(),
            }
        )
        print(f'CustomScene:Updating property to custom properties...')

    def is_maya_file(self):
        """
        如果是Maya类型的文件，则返回后缀名。如果不是，则返回False或这None
        :return:
        """
        if os.path.isfile(self.get_file_path()):
            _, suffix = os.path.splitext(os.path.basename(self.__full_path))
            if suffix in ['.ma', '.mb']:
                return suffix
        return False

    def get_scene_name(self):
        scene_name, _ = os.path.splitext(os.path.basename(os.path.normpath(self.get_file_path())))
        return scene_name

    def get_file_path(self):
        return self.__file_path

    def set_file_path(self, file_path):

        if not self.is_maya_file:
            raise Exception(f'>>{str(file_path)}<< is not a legal address!')
        else:
            self.__file_path = file_path
        print('CustomScene:Setting file_path...')

        self.__update_data()


class CustomSceneFunction(CustomScene):
    def __init__(self):
        super().__init__()

    def has_same_name_transform(self):
        for i in cmds.ls(type='transform'):
            if '|' in i:
                return True
        return False

    def has_duplicate_named_object(self, typ):
        for i in cmds.ls(type=typ):
            if '|' in i:
                return True
        return False

    def has_same_name_joint(self):
        for i in cmds.ls(type='joint'):
            if '|' in i:
                return True
        return False

    def get_objects_with_more_than_4_sides_long_list(self):
        cmds.select(cmds.ls(type='mesh'))
        sel = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(sel)
        poly_objects = []

        for i in range(sel.length()):
            m_obj = om.MObject()
            sel.getDependNode(i, m_obj)

            if m_obj.hasFn(om.MFn.kMesh):
                dag_path = om.MDagPath()
                sel.getDagPath(i, dag_path)
                poly = om.MFnMesh(dag_path)

                for j in range(poly.numPolygons()):
                    vertices = om.MIntArray()
                    poly.getPolygonVertices(j, vertices)

                    if len(vertices) > 4:
                        poly_objects.append(dag_path.fullPathName())
                        break
        cmds.select(cl=True)
        return poly_objects

    def get_root_nodes(self):
        root_nodes = cmds.ls(assemblies=True, long=True)
        return root_nodes

    def get_custom_cameras(self):
        default_camera_list = [
            '|front',
            '|persp',
            '|side',
            '|top',
        ]
        res = []
        for i in cmds.ls(type='camera', long=True):
            camera_name_long = cmds.ls(cmds.listRelatives(i, parent=True), long=True)[0]
            if camera_name_long not in default_camera_list:
                res.append(camera_name_long)
        return res

    def get_file_evaluate(self):
        def convert_bytes(size):
            """ Convert bytes to KB, or MB or GB"""
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return "%3.1f %s" % (size, x)
                size /= 1024.0

        base_name, suffix = os.path.splitext(os.path.basename(self.get_file_path()))
        return {
            'FileName': base_name,
            'Suffix': suffix,
            'Size': convert_bytes(os.path.getsize(self.get_file_path())),
            'IsPathAscii': custom_maya.is_ascii(self.get_file_path()),
            'FirstLetterIsNumber': True if base_name[0].isdigit() else False,
        }

    def get_empty_groups(self):
        return []
