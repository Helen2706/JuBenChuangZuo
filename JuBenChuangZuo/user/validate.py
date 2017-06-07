#!/usr/bin/env python
# coding=utf-8

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

def generate_verification_image_code():
    # 随机字母:
    def rndChar():
        return chr(random.randint(65, 90))

    # 随机颜色1:
    def rndColor():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2:
    def rndColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    width = 160
    height = 28
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 22)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:

    for x in range(0, width, 4):
        for y in range(0, height, 4):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    strs = ''
    for t in range(4):
        s = rndChar()
        draw.text((44 * t + 7, 7), s, font=font, fill=rndColor2())
        strs = strs + s

    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    image.save('static/img/code/code.jpg', 'jpeg');
    return strs

