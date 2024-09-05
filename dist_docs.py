import os
import shutil
import subprocess

def run_npm_build_and_setup_server(base_dir):
    """
    在指定路径下运行 npm build，复制文件并启动 Python HTTP 服务器。
    """
    docs_dir = os.path.join(base_dir, 'docs')
    vuepress_dist = os.path.join(docs_dir, '.vuepress', 'dist')
    temp_dir = os.path.join(docs_dir, 'temp')
    target_docs = os.path.join(temp_dir, 'docs')

    # Step 1: 在 base_dir 路径下运行 PowerShell 命令 "npm run docs:build"
    try:
        print(f"在 {base_dir} 目录下执行 'npm run docs:build'...")
        subprocess.run(["powershell", "-Command", "npm run docs:build"], cwd=base_dir, check=True)
        print("npm run docs:build 成功")
    except subprocess.CalledProcessError as e:
        print(f"npm run docs:build 失败: {e}")
        return

    # Step 2: 将 .vuepress/dist 文件夹复制到 docs/temp 下，并重命名为 docs
    if os.path.exists(vuepress_dist):
        # 确保 temp 目录存在
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # 如果目标 docs 文件夹已经存在，先删除
        if os.path.exists(target_docs):
            print(f"目标路径中的 {target_docs} 已存在，正在删除...")
            shutil.rmtree(target_docs)

        try:
            # 复制 dist 文件夹到目标
            shutil.copytree(vuepress_dist, target_docs)
            print(f"已将 {vuepress_dist} 复制并重命名为 {target_docs}")
        except Exception as e:
            print(f"复制过程中发生错误: {e}")
            return
    else:
        print(f"{vuepress_dist} 文件夹不存在，无法复制")
        return

    # Step 3: 在 temp 目录下启动 Python HTTP 服务器
    try:
        print(f"在 {temp_dir} 目录下启动 Python HTTP 服务器...")
        subprocess.run(["python", "-m", "http.server", "80"], cwd=temp_dir)
    except subprocess.CalledProcessError as e:
        print(f"启动 HTTP 服务器失败: {e}")

# 示例使用
base_directory = r'F:\Desktop\ed-docs-new-style'  # 将此路径替换为实际路径

run_npm_build_and_setup_server(base_directory)
