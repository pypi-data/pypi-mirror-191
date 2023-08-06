import asyncio
import os

import maya.cmds as cmds
from jinja2 import Environment, FileSystemLoader, PackageLoader

from custom_maya import SceneDetails, async_scene, CustomSceneFunction


def get_templates_env(package_name='custom_maya', template_path='templates'):
    file_loader = PackageLoader(package_name, template_path)
    # 创建一个Jinja2环境
    env = Environment(loader=file_loader)
    return env


class CData:
    def __init__(self):
        self.th = []
        self.tds = []

    def get_data(self):
        return {
            'TH': self.th,
            'TDs': self.tds
        }


class Alert(CustomSceneFunction):
    class AData:
        def __init__(self, cls, message):
            """
            class:
            primary,secondary,success,danger,warning,info,light,dark
            """
            self.cls = cls
            self.message = message

        def get_data(self):
            return {
                'Class': self.cls,
                'Message': self.message,
            }

    def __init__(self):
        super().__init__()
        self.__alert_data = []
        if len(self.get_objects_with_more_than_4_sides_long_list()) > 0:
            self.append_alert(
                self.AData(
                    'danger',
                    'There are polygons with more than 4 sides.'
                )
            )

        if True if os.path.basename(self.get_file_path()).isdigit() else False:
            self.append_alert(
                self.AData(
                    'warning',
                    'Filenames start with a number.'
                )
            )

    def get_alert_data(self):
        return self.__alert_data

    def append_alert(self, adata: AData):
        self.__alert_data.append(adata.get_data())


class PerSceneInfo(SceneDetails):
    def __init__(self, index_page_path: str = None):
        super().__init__()
        self.index_page_path = index_page_path
        self.si = SceneIndex(self.index_page_path)

    def __del__(self):
        self.si.output()

        os.startfile(self.index_page_path)

    def get_blend_shapes_detail(self):
        """
        获取场景中所有的BlendShape和其中的Morphtarget对象的列表
        :return:
        {
            'TH': ['BlendShape', 'Morphtargets'],
            'TDs': [
                [
                    ['BlendShape1'], [f'BS1_MT{i}' for i in range(30)]
                ],
                [
                    ['BlendShape2'], ['BS2_MT1']
                ],
                [
                    ['BlendShape3'], []
                ],
            ]
        }
        """
        cdt = CData()
        cdt.th = ['BlendShape', 'Morphtargets']
        blend_shapes = cmds.ls(type='blendShape')

        for bs in blend_shapes:
            mt_list = cmds.listAttr(f'{bs}.w', m=True)
            ml = mt_list if isinstance(mt_list, list) else []
            cdt.tds.append([[bs], ml])
        return cdt.get_data()

    def get_data(self):
        data = {
            'headers': {
            },
            'SecondHeader': {
                'IndexPath': self.si.get_index_page_path(),
            },
            'summary': {
                'FileName': self.get_scene_name(),
                'FilePath': self.get_file_path(),
            },
            'content': {
                'Alerts': {
                    'AlertList': Alert().get_alert_data()
                },
                'Evaluate': self.get_scene_evaluate_for_html(),
                'Tables': {
                    'BlendShapes': self.get_blend_shapes_detail(),
                }
            }
        }
        return data

    def get_save_html_path(self):
        dirname = os.path.dirname(self.get_file_path())
        base_name, suffix = os.path.splitext(os.path.basename(self.get_file_path()))
        absolute_path = os.path.join(dirname, f'{base_name}.html')
        return absolute_path

    def output(self, data):
        # 创建一个Jinja2环境
        env = get_templates_env()
        template = env.get_template('per_scene.html')
        output = template.render(data)
        with open(self.get_save_html_path(), "w", encoding='utf-8') as f:
            f.write(output)

    def open_file(self):
        cmds.file(self.get_file_path(), open=True, f=True)

    def func(self):

        try:
            # 打开场景
            self.open_file()

            self.output(self.get_data())
            self.si.finished_file_list.append(self.get_file_path())
            self.si.finished_html_list.append(self.get_save_html_path())
            self.si.index_evaluate.append(self.get_index_evaluate())
        except Exception as e:
            self.si.failed_file_list.append(self.get_file_path())


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


class SceneIndex:

    def __init__(self, index_page_path):
        self.finished_file_list = []
        self.failed_file_list = []
        self.finished_html_list = []
        self.__index_page_path = index_page_path
        self.index_evaluate = []

    def modify_index_evaluate(self):
        for per_d in self.index_evaluate:
            path_with_suf, _ = os.path.splitext(per_d.get('Path'))
            if path_with_suf in [p[:-5] for p in self.finished_html_list]:
                per_d['Path'] = path_with_suf + '.html'

    def get_data(self):
        self.modify_index_evaluate()
        return {
            'FinishedFileList': self.finished_file_list,
            'FailedFileList': self.failed_file_list,
            'FinishedHtmlList': self.finished_html_list,
            'IndexEvaluate': self.index_evaluate,
            'IndexThList': list(self.index_evaluate[0].keys()) if len(self.index_evaluate) > 0 else [],
        }

    def get_index_page_path(self):
        return self.__index_page_path

    def output(self):
        # 创建一个Jinja2环境
        env = get_templates_env()
        template = env.get_template('index.html')
        output = template.render(self.get_data())
        with open(self.get_index_page_path(), "w", encoding='utf-8') as f:
            f.write(output)


def get_scene_details(root_dir: str = None, file_list: list = None, index_page_path: str = None):
    if index_page_path:
        index_page_path = index_page_path
    elif root_dir:
        index_page_path = os.path.join(root_dir, 'check_scene_index.html')
    else:
        index_page_path = os.path.join(os.path.expanduser('~'), 'check_scene_index.html')

    if file_list:
        pass
    elif root_dir:
        file_list = get_file_path_list(root_dir)

    mf = PerSceneInfo(index_page_path=index_page_path)
    asyncio.run(async_scene(file_list, mf))
    del mf


if __name__ == '__main__':
    get_scene_details(root_dir=r'd:\test_scenes')
