# 使用官方 Python 3.10 slim 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用可能使用的端口（根据实际情况调整）
EXPOSE 8000

# 设置启动命令（根据实际情况调整）
CMD ["python", "main.py"]