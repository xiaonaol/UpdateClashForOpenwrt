import requests
import urllib.request
import shutil
import subprocess
import os
import glob
import gzip
import zipfile

# 你需要提供你想要获取的仓库的所有者和名称
owner = "MetaCubeX"
repo = "mihomo"

# 构造API的URL
api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/Prerelease-Alpha"

# 发送GET请求，得到响应
response = requests.get(api_url)

# 检查响应的状态码，如果是200，表示成功
if response.status_code == 200:
    # 将响应的内容转换为JSON格式的字典
    data = response.json()

    # 从字典中获取你感兴趣的信息，比如release的名称，标签，下载链接等
    assets = data["assets"]

    # 定义你想要过滤的前缀
    prefix = "mihomo-linux-arm64-alpha"

    # 使用列表推导式和startswith方法来过滤出符合条件的Assets
    asset = [asset for asset in assets if asset["name"].startswith(prefix)]

    if len(asset) != 1:
        print("目标仓库的release有改动，请联系开发者进行维护。")
    else:
        # 获取最新内核名称和下载url
        release_name = asset[0]["name"]
        download_url = asset[0]["browser_download_url"]
        print(f"{release_name}: {download_url}")

        # 如果最新版本压缩包已存在则无需下载
        if os.path.exists(release_name):
            print("Compressed file already existed.")
        else:
            print("Downloading...")
            urllib.request.urlretrieve(download_url, release_name)

        # 获取当前Clash
        current = glob.glob('clash_meta')
        if len(current) != 1:
            # 解压新版内核
            g_file = gzip.GzipFile(release_name)
            open("clash_meta", "wb+").write(g_file.read())
            g_file.close()
        else:
            # 获取当前版本号
            rc, current_version = subprocess.getstatusoutput("clash_meta -v")
            os.system("pkill clash_meta")

            # 解压新版内核
            g_file = gzip.GzipFile(release_name)
            open("clash_meta", "wb+").write(g_file.read())
            g_file.close()

            # 获取更新后的版本号
            rc, updated_version = subprocess.getstatusoutput("clash_meta -v")
    # 删除压缩文件
    os.remove(release_name)

    print("Done!")
else:
    # 如果状态码不是200，表示出错了，打印出错误信息
    print(f"Something went wrong: {response.status_code}")