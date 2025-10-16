import os
import sys
import platform

def is_really_empty(folder_path):
    """判断文件夹是否真正为空（不含任何文件/子目录，或仅含.gitkeep但无其他内容）"""
    try:
        entries = os.listdir(folder_path)
        # 如果目录完全为空，视为空目录
        if not entries:
            return True
        # 如果目录中只有.gitkeep文件，视为已处理
        if len(entries) == 1 and entries[0] == ".gitkeep":
            return False
        # 其他情况视为非空
        return False
    except Exception as e:
        # 忽略无权限访问的目录
        if "Permission denied" in str(e) or "拒绝访问" in str(e):
            return False
        print(f"检查文件夹 {folder_path} 时出错: {e}")
        return False

def create_gitkeep_for_empty_folders(root_dir):
    # 转换为绝对路径，确保路径正确性
    root_dir = os.path.abspath(root_dir)
    
    # 验证目录存在性
    if not os.path.exists(root_dir):
        print(f"错误: 目录 {root_dir} 不存在")
        return
        
    if not os.path.isdir(root_dir):
        print(f"错误: {root_dir} 不是一个目录")
        return
    
    # 安全检查：显示当前要处理的目录并要求确认
    print(f"\n警告：即将处理以下目录及其所有子目录：")
    print(f"   {root_dir}")
    confirm = input("是否继续？(y/n)：").strip().lower()
    if confirm != 'y' and confirm != 'yes':
        print("操作已取消")
        return
    
    # 第一阶段：收集所有符合条件的空目录
    empty_folders = []
    for dirpath, _, _ in os.walk(root_dir):
        # 确保始终在指定的根目录范围内
        if not dirpath.startswith(root_dir):
            print(f"警告：尝试访问目录 {dirpath} 超出了指定根目录范围，已跳过")
            continue
            
        if is_really_empty(dirpath):
            empty_folders.append(dirpath)
    
    # 第二阶段：为收集到的空目录统一创建.gitkeep
    created_count = 0
    for folder in empty_folders:
        # 再次验证路径是否在根目录范围内
        if not folder.startswith(root_dir):
            print(f"警告：目录 {folder} 超出处理范围，已跳过")
            continue
            
        gitkeep_path = os.path.join(folder, ".gitkeep")
        try:
            with open(gitkeep_path, 'w') as f:
                pass  # 创建空文件
            created_count += 1
            print(f"已在 {folder} 创建 .gitkeep")
        except Exception as e:
            print(f"在 {folder} 创建 .gitkeep 时出错: {e}")
    
    print(f"\n处理完成，共识别 {len(empty_folders)} 个空目录，成功创建 {created_count} 个 .gitkeep 文件")

if __name__ == "__main__":
    # 获取并验证根目录
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]
    else:
        root_directory = os.getcwd()
    
    # 特殊处理Windows系统，防止意外遍历所有驱动器
    if platform.system() == "Windows":
        # 确保路径是有效的驱动器或子目录
        if not os.path.abspath(root_directory).startswith(('C:\\', 'D:\\', 'E:\\', 'F:\\')):
            print(f"警告：在Windows系统上检测到非标准路径，已自动更正为当前工作目录")
            root_directory = os.getcwd()
    
    create_gitkeep_for_empty_folders(root_directory)
