#!/bin/bash

set -e

echo "🚀 TrendRadar Web 快速启动"
echo "================================"
echo ""

# 检查是否在web目录
if [ ! -f "package.json" ]; then
    echo "❌ 请在web目录下运行此脚本"
    exit 1
fi

# 清理旧文件
#echo "🧹 清理旧文件..."
#rm -rf node_modules package-lock.json dist

# 安装依赖
echo "📦 安装依赖..."
npm install

# 构建项目
echo "🏗️ 构建项目..."
npm run build

# 检查构建结果
if [ ! -d "dist" ]; then
    echo "❌ 构建失败"
    exit 1
fi

echo ""
echo "✅ 构建完成！"
echo ""
echo "🌐 启动应用..."
echo "   访问地址: http://localhost:5000"
echo "   按 Ctrl+C 停止服务"
echo ""

# 启动Flask应用
python3 app.py
