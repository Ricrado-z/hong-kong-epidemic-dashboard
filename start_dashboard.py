#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
香港疫情数据可视化大屏 - 启动脚本
一键启动整个应用
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """检查依赖包"""
    required_packages = ['flask', 'pandas', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print(f"pip3 install {' '.join(missing_packages)}")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def check_data_file():
    """检查数据文件"""
    data_file = Path("data/香港各区疫情数据_20250322.xlsx")
    if not data_file.exists():
        print(f"❌ 数据文件不存在: {data_file}")
        return False
    
    print("✅ 数据文件存在")
    return True

def start_application():
    """启动应用"""
    print("🚀 正在启动香港疫情数据可视化大屏...")
    
    # 切换到backend目录
    backend_path = Path("src/backend")
    if not backend_path.exists():
        print("❌ 后端目录不存在")
        return False
    
    # 启动Flask应用
    try:
        os.chdir(backend_path)
        print("📊 访问地址: http://localhost:8080")
        print("🔄 正在启动服务器...")
        
        # 延迟打开浏览器
        def open_browser():
            time.sleep(3)
            webbrowser.open('http://localhost:8080')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # 启动Flask应用
        subprocess.run([sys.executable, "app.py"])
        
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🏥 香港疫情数据可视化大屏启动器")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查数据文件
    if not check_data_file():
        return
    
    # 启动应用
    start_application()

if __name__ == "__main__":
    main()
