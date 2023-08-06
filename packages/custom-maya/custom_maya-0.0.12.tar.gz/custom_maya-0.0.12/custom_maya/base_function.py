import os


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def maya_file_filter(func):
    """
    将文件名进行检查，只输出Maya文件的路径并且存在的路径。
    :param func:
    :return:
    """

    def inner(script_path=None, *args, **kwargs):
        file_list = kwargs.get('file_list')
        res = []
        for file_path in file_list:
            short_name, suffix = os.path.splitext(os.path.basename(file_path))
            if os.path.exists(file_path) and suffix in ['.ma', '.mb']:
                res.append(file_path)
        print('-' * 20 + str(script_path))
        kwargs['file_list'] = res
        return func(*args, **kwargs)

    return inner
