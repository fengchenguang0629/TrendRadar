# 自动构建并推送Docker镜像脚本 (Windows PowerShell版本)
# 作者: Lingma
# 版本: 1.0
# 描述: 用于自动构建TrendRadar项目镜像并推送到阿里云容器镜像服务

# 配置变量
$IMAGE_NAME = "trendradar"
$TAG = "latest"
$REGISTRY = "registry.cn-beijing.aliyuncs.com"
$REPOSITORY = "fengchenguang/$IMAGE_NAME"

# 获取当前版本号
$VERSION = Get-Content version

# 显示调试信息
Write-Host "=== Debug Info ==="
Write-Host "Current user: $env:USERNAME"
Write-Host "Working directory: $PWD"
Write-Host "PATH: $env:PATH"
Write-Host "Available Docker: $(Get-Command docker -ErrorAction SilentlyContinue)"
Write-Host "=================="

Write-Host "开始构建镜像..."

Write-Host "步骤1: 构建镜像"

# 构建镜像，使用Dockerfile.web文件
docker build -t ${IMAGE_NAME}:${TAG} -f docker/Dockerfile.web .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 镜像构建失败"
    exit 1
}

Write-Host "✅ 镜像构建成功"

Write-Host "步骤2: 登录到Registry"

# 登录到阿里云容器镜像服务
docker login --username="冯晨光" $REGISTRY

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Registry登录失败"
    exit 1
}

Write-Host "✅ Registry登录成功"

Write-Host "步骤3: 重命名镜像"

# 为镜像打上标签
docker tag ${IMAGE_NAME}:${TAG} ${REGISTRY}/${REPOSITORY}:${VERSION}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 镜像重命名失败"
    exit 1
}

Write-Host "✅ 镜像重命名成功"

# 为镜像打上latest标签
docker tag ${IMAGE_NAME}:${TAG} ${REGISTRY}/${REPOSITORY}:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ latest标签创建失败"
    exit 1
}

Write-Host "✅ latest标签创建成功"

Write-Host "步骤4: 推送镜像"

# 推送镜像到Registry
docker push ${REGISTRY}/${REPOSITORY}:${VERSION}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 镜像推送失败"
    exit 1
}

Write-Host "✅ 镜像推送成功"

Write-Host "步骤5: 推送最新标签"

# 推送latest标签
docker push ${REGISTRY}/${REPOSITORY}:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 最新标签推送失败"
    exit 1
}

Write-Host "✅ 最新标签推送成功"

Write-Host "=== 所有操作完成 ==="