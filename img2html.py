import os
from PIL import Image
from io import BytesIO
import base64

def convert_images_to_html(image_paths):
    # 首先对图片路径列表按照文件名排序
    sorted_image_paths = sorted(image_paths, key=lambda x: os.path.basename(x))

    # HTML头部
    html_head = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }
            img {
                max-width: 100%;
                height: auto;
            }
            @media (min-width: 768px) {
                img {
                    max-width: 50%;
                }
            }
            @media (min-width: 1200px) {
                img {
                    max-width: 33.33%;
                }
            }
        </style>
    </head>
    <body>
    '''

    # HTML尾部
    html_tail = '''
    </body>
    </html>
    '''

    img_tags = []

    # 循环处理排序后的图片路径
    for path in sorted_image_paths:
        try:
            with Image.open(path) as img:
                # 确定图像的原始格式
                original_format = img.format.lower()
                
                # 如果图像不是JPEG或PNG格式，则转换为JPEG
                if original_format not in ['jpeg', 'png']:
                    img = img.convert('RGB') if img.mode == 'RGBA' else img
                
                # 将图像转换为Base64编码的JPEG或PNG，以便嵌入HTML
                buffer = BytesIO()
                img.save(buffer, format="JPEG" if original_format != 'png' else "PNG")
                img_str = base64.b64encode(buffer.getvalue()).decode()

                # 添加图片标签到列表
                img_tags.append(f'<img src="data:image/{("jpeg" if original_format != "png" else "png")};base64,{img_str}" alt="Image">')
        except Exception as e:
            print(f"Error processing image {path}: {e}")
            continue

    # 将HTML头部、图片标签和尾部连接起来形成完整的HTML内容
    html_content = html_head + '\n'.join(img_tags) + html_tail

    return html_content