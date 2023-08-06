import asyncio

import maya.standalone

from custom_maya import SceneDetails


async def async_function(file_path, sd_obj: SceneDetails):
    """
    Asynchronously read a Maya file using the cmds module
    :param sd_obj:
    :param file_path: Maya文件的路径
    :return:
    """
    sd_obj.set_file_path(file_path)
    sd_obj.func()
    print(f"Successfully read file: {file_path}")


async def async_scene(file_paths, func):
    """
    Asynchronously read multiple Maya files
    :param file_paths: ['file_path1','file_path2']
    :param func:
    :return:
    """
    print('-----开始异步处理程序-----')
    maya.standalone.initialize(name='python')
    # create a list of tasks
    tasks = [asyncio.create_task(async_function(file_path, func)) for file_path in file_paths]
    # wait for all tasks to complete
    await asyncio.gather(*tasks)
    print('-----结束异步处理程序-----')
