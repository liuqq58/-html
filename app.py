from flask import Flask, request, send_file, jsonify, redirect
import os
from img2html import convert_images_to_html

app = Flask(__name__, static_folder='frontend', static_url_path='')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files[]')
    if not files:
        return "No files uploaded", 400

    images = []
    for file in files:
        if file.filename == '':
            continue
        filename = file.filename
        file.save(os.path.join("/tmp", filename))
        images.append(os.path.join("/tmp", filename))

    # 调用img2html.py进行图片转换
    html_content = convert_images_to_html(images)

    # 直接返回转换后的HTML内容，而非下载链接
    return html_content, 200

@app.route('/download/converted.html')
def download():
    # 提供HTML文件下载
    return send_file('/tmp/output.html', as_attachment=True)

@app.route('/')
def index():
    # 重定向到前端页面
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7051)