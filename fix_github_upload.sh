#!/bin/bash
# GitHub上传问题修复脚本

echo "🔧 GitHub上传问题修复脚本"
echo "================================"

# 检查当前状态
echo "📋 当前Git状态:"
git status --short

echo ""
echo "📋 当前远程仓库:"
git remote -v

echo ""
echo "🔧 修复步骤:"
echo "1. 删除现有的远程仓库配置"
git remote remove origin 2>/dev/null || echo "   远程仓库不存在，跳过"

echo "2. 检查是否有未提交的更改"
if [ -n "$(git status --porcelain)" ]; then
    echo "   发现未提交的更改，正在提交..."
    git add .
    git commit -m "修复GitHub上传问题"
else
    echo "   没有未提交的更改"
fi

echo ""
echo "✅ 修复完成！"
echo ""
echo "📝 下一步操作:"
echo "1. 在GitHub上创建新仓库"
echo "2. 运行以下命令（替换YOUR_USERNAME为您的GitHub用户名）:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/hong-kong-epidemic-dashboard.git"
echo "   git push -u origin main"
echo ""
echo "或者运行交互式上传脚本:"
echo "   python3 upload_to_github.py"
