#coding=UTF-8
from git import Repo
from git.exc import GitCommandError, RepositoryDirtyError
from threading import Thread
import os,json

repo_url = 'https://github.com/coder-WanFeng/TFMS_VolunteerStation.git'  # 替换为你的GitHub仓库地址
destination_dir = './cache'  # 替换为你要克隆到的本地目录路径
version_json_path = os.path.join(destination_dir, 'version.json')

def check_version():
    if os.path.exists(version_json_path):
        # 读取version.json文件内容
        with open(version_json_path, 'r') as file:
            last_version_data = json.load(file)
            last_version = last_version_data["version"]
        clear_cache(destination_dir)
    else:
        last_version = None
    with open("version.json", 'r') as file:
        local_version_data = json.load(file)
        local_version = local_version_data["version"]
    if last_version != None:
        if int(local_version) < int(last_version):
            print("检测到新版本，正在下载...")
            res = download_last_version(destination_dir="./")
            print("已下载最新版本内容，将在下次启动时加载")
            return res
    else:
        return download_last_version()

def download_last_version(repo_url=repo_url,destination_dir=destination_dir):
    try:
        # 克隆仓库到指定目录
        Repo.clone_from(repo_url, destination_dir)
        result="仓库克隆成功！"
    except GitCommandError as e:
        # Git命令执行错误，例如网络问题、仓库不存在等
        result="Git命令执行错误：{}".format(e)
    except RepositoryDirtyError as e:
        # 如果目标目录已有文件且不是空的git仓库
        result="目标目录不是空的git仓库：{}".format(e)
    except Exception as e:
        # 其他所有异常
        result="发生错误：{}".format(e)
    return result

import os

def clear_cache(directory_path):
    # 获取目录下的所有文件和文件夹
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            # 如果是文件，则删除
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # 如果是文件夹，则递归删除
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"删除cache时出错：{e}")
    os.rmdir(directory_path)

def auto_update():
    res = check_version()
    print(res)
    return {"msg":res,"res":res=="仓库克隆成功！"}
def thread_update():
    # auto_update()
    update_th=Thread(target=auto_update, args=())
    update_th.start()
    update_th.join()