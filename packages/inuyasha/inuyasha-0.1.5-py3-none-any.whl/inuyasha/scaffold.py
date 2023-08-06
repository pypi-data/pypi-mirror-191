import os
import platform
import sys


def create_scaffold(project_name):
    """ 创建项目脚手架"""
    if os.path.isdir(project_name):
        print(f"Project folder {project_name} exists, please specify a new project name.")
        return 1
    elif os.path.isfile(project_name):
        print(f"Project name {project_name} conflicts with existed file, please specify a new one.")
        return 1

    print(f"Create new project: {project_name}")
    print(f"Project root dir: {os.path.join(os.getcwd(), project_name)}\n")

    def create_folder(path):
        os.makedirs(path)
        msg = f"Created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        print(path)
        msg = f"Created file:   {path}"
        print(msg)

    create_folder(project_name)
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo")
    for root, dirs, files in os.walk(template_path):
        relative_path = root.replace(template_path, "").lstrip("\\").lstrip("/")
        if dirs:
            for dir_ in dirs:
                create_folder(os.path.join(project_name, relative_path, dir_))
        if files:
            for file in files:
                with open(os.path.join(root, file), encoding="utf-8") as f:
                    create_file(os.path.join(project_name, relative_path, file.replace(".inuyasha", "")), f.read())


def main_scaffold(args):
    # 项目脚手架处理程序入口
    sys.exit(create_scaffold(args.project_name))


if __name__ == '__main__':
    create_scaffold("demos")
