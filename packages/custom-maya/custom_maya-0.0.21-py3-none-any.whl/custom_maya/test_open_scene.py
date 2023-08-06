# import maya.standalone
# maya.standalone.initialize(name='python')
# import maya.cmds as cmds
# import pymel.core as pm
#
#
# path1 = r'D:\Maya\test_scenes\test_scene1.mb'
#
#
# def open_file(file_path):
#     cmds.file(file_path, f=True, options='v=0', iv=True, typ='mayaBinary', o=True)
#
#
# def import_fbx(file_path):
#     cmds.file(file_path, i=True, type='FBX', iv=True)
#
# def get_d():
#     all_joint = pm.ls(type='joint')
#
#     joint_index = {}
#
#     for i in all_joint:
#         index = len(i.longName().split('|'))
#         joint_index[i.name()] = index
#     return joint_index
#
# open_file(path1)
#
# for i in get_d():
#     print(i, get_d().get(i))
#
# zz = cmds.playblast(format='avi',clearCache=1,viewer=0, fp=4, percent=50, quality=70, filename=r"C:/Users/qiaoyuanzhen/zz.avi1")
# print(zz)
#
# print('Finished!!!!!!!')
# playblast  -format avi -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "none" -quality 70;

# import_fbx(r"")
# try:
#     cmds.parent('NULL', w=True)
# except Exception as ret:
#     print(ret)
# scene1 = get_d()
#
# cmds.file(new=True, f=True)
#
#
# import_fbx(r"")
# try:
#     cmds.parent('NULL', w=True)
# except Exception as ret:
#     print(ret)
# scene2 = get_d()
#
# cmds.file(new=True, f=True)
#
# l1 = list(scene1.keys())
# l2 = list(scene2.keys())
#
# common_list = list(set(l1).intersection(set(l2)))
#
# text = ''
# diff_joint_list = []
# for i in common_list:
#     if scene1[i] != scene2[i]:
#         diff_joint_list.append(i)
#
#
# with open('xx.txt','w')as f:
#     f.write('\n'.join(diff_joint_list))