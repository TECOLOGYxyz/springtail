import shutil
import os

namePath = r'O:\Tech_TTH-BITCue\Workspace_Hjalte\candida\3rd sending - photos F. candida tes ends\smallExp640\training\val'
fromPath = r'O:\Tech_TTH-BITCue\Workspace_Hjalte\candida\3rd sending - photos F. candida tes ends\smallExp1280'
toPath = r'O:\Tech_TTH-BITCue\Workspace_Hjalte\candida\3rd sending - photos F. candida tes ends\smallExp1280/val'

names = [i for i in os.listdir(namePath)]



for n in names:
    src = os.path.join(fromPath, n)
    dst = os.path.join(toPath, n)

    shutil.move(src, dst)