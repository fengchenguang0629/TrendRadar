#!/bin/bash

echo "🔨 构建Vue前端..."

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到Node.js，请先安装Node.js 16+"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
npm install

# 构建
echo "🏗️ 构建项目..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ 构建成功！"
    echo "📁 输出目录: dist/"
else
    echo "❌ 构建失败"
    exit 1
fi
