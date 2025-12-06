#!/bin/bash

echo "🔍 验证Web项目配置..."
echo ""

# 检查Node.js
echo "1️⃣ 检查Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "   ✅ Node.js: $NODE_VERSION"
else
    echo "   ❌ Node.js未安装"
    exit 1
fi

# 检查npm
echo ""
echo "2️⃣ 检查npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "   ✅ npm: $NPM_VERSION"
else
    echo "   ❌ npm未安装"
    exit 1
fi

# 检查Python
echo ""
echo "3️⃣ 检查Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python3未安装"
    exit 1
fi

# 检查Flask
echo ""
echo "4️⃣ 检查Flask..."
if python3 -c "import flask" 2>/dev/null; then
    echo "   ✅ Flask已安装"
else
    echo "   ❌ Flask未安装"
    exit 1
fi

# 检查Flask-CORS
echo ""
echo "5️⃣ 检查Flask-CORS..."
if python3 -c "import flask_cors" 2>/dev/null; then
    echo "   ✅ Flask-CORS已安装"
else
    echo "   ❌ Flask-CORS未安装"
    exit 1
fi

# 检查项目文件
echo ""
echo "6️⃣ 检查项目文件..."
FILES=(
    "src/main.js"
    "src/App.vue"
    "src/components/Layout.vue"
    "src/pages/Dashboard.vue"
    "src/pages/Crawler.vue"
    "src/pages/Config.vue"
    "src/pages/Keywords.vue"
    "src/router/index.js"
    "src/stores/index.js"
    "app.py"
    "package.json"
    "vite.config.js"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file 缺失"
    fi
done

echo ""
echo "✅ 所有检查完成！"
echo ""
echo "📝 下一步："
echo "   1. npm install"
echo "   2. npm run build"
echo "   3. python3 app.py"
echo "   4. 访问 http://localhost:5000"
