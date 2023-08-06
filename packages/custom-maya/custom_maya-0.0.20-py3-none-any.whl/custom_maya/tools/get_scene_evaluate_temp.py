import asyncio
import copy
import os
import time

import pandas as pd

import maya.cmds as cmds
from custom_maya import SceneDetails, async_scene


class MyFuncClass(SceneDetails):
    """

    """
    all_data = []
    all_scene_details = []
    counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_details = {}
        self.counter += 1

    def set_scene_details(self):
        # self.scene_details['File'] = self.get_file_path()
        self.scene_details['SheetName'] = self.get_file_path().replace('\\', '.').replace(':', '..')
        self.scene_details['MorphTargets'] = cmds.ls(type='blendShape')
        self.scene_details['BlendShapes'] = self.get_blend_shapes_detail()
        self.all_scene_details.append(copy.copy(self.scene_details))

    def get_blend_shapes_detail(self):
        res = []
        blend_shapes = cmds.ls(type='blendShape')
        for bs in blend_shapes:
            res.append(cmds.listAttr(f'{bs}.w', m=True))
        return res

    @classmethod
    def check_maya_path(cls, paths):
        res = []
        for i in paths:
            if not os.path.exists(i):
                res.append(i)

    @classmethod
    def check_excel_path(cls, path):
        try:
            pd.DataFrame([{}]).to_excel(path, index=False)
        except PermissionError:
            raise PermissionError('请关闭所要保存的Excel文件')
            return
        except FileNotFoundError:
            raise FileNotFoundError('你输入的保存Excel文件的路径时错误的')
            return
        except Exception as e:
            # print(e)
            raise Exception('你输入的保存Excel文件的路径时错误的，请重新输入正确的文件名')

    @classmethod
    def export_data(cls, excel_path):
        df = pd.DataFrame(cls.all_data)
        # print(cls.all_scene_details)
        temp_path = os.path.join(os.path.expanduser('~'), 'custom_maya_get_scene_evaluate_temp.xlsx')
        try:
            with pd.ExcelWriter(excel_path, mode='a') as writer:
                df.to_excel(writer, index=False, sheet_name='概要')
                num = 0
                for i in cls.all_scene_details:
                    pd.DataFrame([i]).to_excel(writer, sheet_name=f'sheet_{num}', index=False)
                    num += 1
        except Exception as e:
            excel_path = temp_path
            print(e)
            # raise Exception('输出Excel的文件路径有误，已将数据存储到临时文件中。请检查现有的数据是否正确，并且注意输入的Excel保存路径是否正确。')
        finally:
            pass
            # with pd.ExcelWriter(excel_path, mode='a') as writer:
            #     df.to_excel(writer, index=False, sheet_name='概要')
            #     num = 0
            #     for i in cls.all_scene_details:
            #         pd.DataFrame([i]).to_excel(writer, sheet_name=f'sheet_{num}', index=False)
            #         num += 1

    def func(self):
        import maya.cmds as cmds

        cmds.file(self.get_file_path(), open=True, f=True)
        # print(f'进入Maya文件并打印文件名-->{self.get_file_path()}')
        short_name, _ = os.path.splitext(os.path.basename(self.get_file_path()))

        self.add_property_to_custom_properties(
            {
                **self.get_custom_properties(),
                **self.get_scene_evaluate()
            }
        )

        self.all_data.append(self.get_custom_properties())
        self.set_scene_details()
        print('写入文件中...')


def get_file_path_list(root_dir):
    res = []
    suffix_list = ['.mb', '.ma']

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            short_file_name, suffix = os.path.splitext(os.path.basename(file))
            full_path = os.path.join(root, file)
            if suffix in suffix_list:
                res.append(full_path)
    return res


def get_scene_details_temp(file_paths=[], export_to_excel_path=None):
    mf = MyFuncClass()
    MyFuncClass.check_excel_path(export_to_excel_path)

    # 执行程序
    asyncio.run(async_scene(file_paths, mf))
    # if export_to_excel_path:
    MyFuncClass.export_data(export_to_excel_path)


if __name__ == '__main__':
    get_scene_details_temp(export_to_excel_path=os.path.join(os.path.expanduser("~"), 'test.xlsx'),
                      file_paths=get_file_path_list(r'D:\test_scenes'))
