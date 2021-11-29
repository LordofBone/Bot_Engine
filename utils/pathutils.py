import stat
import os
import pip


def delete_with_override(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if not name == ".gitkeep":
                filename = os.path.join(root, name)
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)
        for name in dirs:
            os.chmod(os.path.join(root, name), stat.S_IWUSR)
            os.rmdir(os.path.join(root, name))
    # os.chmod(path, stat.S_IWUSR)
    # os.rmdir(path)


def bot_installer():
    pip.main(['install', '-e', 'Chatbot_8/'])
