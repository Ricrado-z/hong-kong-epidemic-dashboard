#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub上传助手
帮助用户将项目上传到GitHub
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} 失败")
            print(f"错误信息: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ {description} 异常: {e}")
        return False

def check_git_status():
    """检查Git状态"""
    print("🔍 检查Git状态...")
    
    # 检查是否有未提交的更改
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("⚠️  发现未提交的更改，正在添加...")
        if not run_command("git add .", "添加文件"):
            return False
        if not run_command('git commit -m "更新项目文件"', "提交更改"):
            return False
    
    print("✅ Git状态正常")
    return True

def upload_to_github():
    """上传到GitHub"""
    print("=" * 60)
    print("🚀 GitHub上传助手")
    print("=" * 60)
    
    # 检查Git状态
    if not check_git_status():
        return False
    
    # 获取用户输入
    print("\n📝 请提供以下信息：")
    username = input("请输入您的GitHub用户名: ").strip()
    repo_name = input("请输入仓库名称 (默认: hong-kong-epidemic-dashboard): ").strip()
    
    if not repo_name:
        repo_name = "hong-kong-epidemic-dashboard"
    
    if not username:
        print("❌ 用户名不能为空")
        return False
    
    # 构建仓库URL
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    print(f"\n📋 仓库URL: {repo_url}")
    
    # 确认信息
    confirm = input(f"\n确认上传到 {repo_url} ? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ 取消上传")
        return False
    
    # 添加远程仓库
    print(f"\n🔗 添加远程仓库...")
    if not run_command(f"git remote add origin {repo_url}", "添加远程仓库"):
        # 如果远程仓库已存在，先删除再添加
        print("🔄 远程仓库已存在，正在重新设置...")
        run_command("git remote remove origin", "删除现有远程仓库")
        if not run_command(f"git remote add origin {repo_url}", "重新添加远程仓库"):
            return False
    
    # 推送到GitHub
    print(f"\n📤 推送到GitHub...")
    if not run_command("git branch -M main", "设置主分支"):
        return False
    
    if not run_command("git push -u origin main", "推送到GitHub"):
        return False
    
    # 显示成功信息
    print("\n" + "=" * 60)
    print("🎉 上传成功！")
    print("=" * 60)
    print(f"📊 您的项目已上传到: https://github.com/{username}/{repo_name}")
    print(f"🔗 访问地址: https://github.com/{username}/{repo_name}")
    print("\n📋 后续操作:")
    print("1. 访问GitHub仓库页面")
    print("2. 检查文件是否完整")
    print("3. 分享给其他人")
    print("\n🔄 更新代码:")
    print("git add .")
    print("git commit -m '更新说明'")
    print("git push")
    
    return True

def main():
    """主函数"""
    try:
        upload_to_github()
    except KeyboardInterrupt:
        print("\n👋 操作已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    main()
