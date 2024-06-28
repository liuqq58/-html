# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim-buster

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到容器的 /app 中
COPY . /app

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# 暴露端口
EXPOSE 7051

# 运行 flask 应用
CMD ["flask", "run", "--host=0.0.0.0", "--port=7051"]