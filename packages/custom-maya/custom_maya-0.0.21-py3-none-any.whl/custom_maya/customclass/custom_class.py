import maya.cmds as cmds

from .base_class import CustomSceneFunction


class SceneEvaluate(CustomSceneFunction):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def get_scene_evaluate_for_html(self):
        return {
            'FileEvaluate': {
                'File': self.get_file_evaluate(),
            },
            'SceneEvaluate': {
                'Transform': self.get_transform_evaluate(),
                'Polygon': self.get_poly_evaluate(),
                'Joint': self.get_joint_evaluate(),
                'BlendShape': self.get_blendshape_evaluate(),
                'Camera': self.get_camera_evaluate(),
                'Light': self.get_light_evaluate(),
                'Settings': self.get_settings_evaluate(),
            },
        }

    def get_index_evaluate(self):
        return {
            **{'Path': self.get_file_path()},
            **self.get_file_evaluate(),
            # **self.get_transform_evaluate(),
            **self.get_poly_evaluate(),
            **self.get_transform_evaluate(),
            # **self.get_joint_evaluate(),
            # **self.get_blendshape_evaluate(),
            # **self.get_camera_evaluate(),
            # **self.get_light_evaluate(),
        }

    def get_scene_evaluate(self):
        return {
            **self.get_poly_evaluate(),
            **self.get_joint_evaluate(),
            **self.get_light_evaluate(),
            **self.get_camera_evaluate(),
            # 其他信息
            **{
                'AllTransformsUnique': self.has_duplicate_named_object('transform'),
                'RootTransforms': len(cmds.ls(assemblies=True, long=True)) - 4,
            },
            **self.get_blendshape_evaluate(),
        }

    def get_transform_evaluate(self):
        return {
            'Transforms': len(cmds.ls(type='transform')),
            # 'EmptyGroup': len(self.get_empty_groups()),
        }

    def get_camera_evaluate(self):
        return {
            'Cameras': len(cmds.ls(type='camera')),
            'CamerasWithOutDefault': len(self.get_custom_cameras()),
        }

    def get_light_evaluate(self):
        return {
            'Lights': len(cmds.ls(type='light')),
            'DuplicateNamedLight': self.has_duplicate_named_object('light'),
        }

    def get_poly_evaluate(self):
        __meshes = cmds.ls(type='mesh')
        return {
            'Verts': cmds.polyEvaluate(__meshes, vertex=True) if len(__meshes) > 0 else 0,
            'Edges': cmds.polyEvaluate(__meshes, edge=True) if len(__meshes) > 0 else 0,
            'Faces': cmds.polyEvaluate(__meshes, face=True) if len(__meshes) > 0 else 0,
            'Tris': cmds.polyEvaluate(__meshes, triangle=True) if len(__meshes) > 0 else 0,
            'UVs': cmds.polyEvaluate(__meshes, uv=True) if len(__meshes) > 0 else 0,
            'Ngons': len(self.get_objects_with_more_than_4_sides_long_list()),
            'AllMeshesUnique': not self.has_duplicate_named_object('mesh'),
        }

    def get_joint_evaluate(self):
        return {
            'Joints': len(cmds.ls(type='joint')),
            'AllJointsUnique': self.has_duplicate_named_object('joint'),
        }

    def get_settings_evaluate(self):
        return {
            'Up axis': cmds.upAxis(q=True, axis=True),
            'Linear': cmds.currentUnit(q=True, linear=True),
            'Angular': cmds.currentUnit(q=True, angle=True),
            'AnimStartTime': cmds.playbackOptions(q=True, animationStartTime=True),
            'AnimEndTime': cmds.playbackOptions(q=True, animationEndTime=True),
            'PlaybackStartTime': cmds.playbackOptions(min=True, q=True),
            'PlaybackEndTime': cmds.playbackOptions(max=True, q=True),
            'Framerate':cmds.currentUnit(q=True,time=True),
        }

    def get_blendshape_evaluate(self):
        blend_shapes = cmds.ls(type='blendShape')
        morph_target_counter = 0
        for bs in blend_shapes:
            morph_target_counter += cmds.blendShape(bs, query=True, weightCount=True)
        return {
            'BlendShapes': len(blend_shapes),
            'MorphTargets': morph_target_counter
        }


class SceneDetails(SceneEvaluate):
    def __init__(self):
        super().__init__()

    def func(self):
        pass
