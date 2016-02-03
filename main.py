# coding=utf-8
import math
from PIL import Image, ImageFilter
from numpy import *
import BlendFilter


class GaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


def glowing_edge(img):
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    width, height = img.size
    pix = img.load()

    for w in xrange(width - 1):
        for h in xrange(height - 1):
            bottom = pix[w, h + 1]  # 下方像素点
            right = pix[w + 1, h]  # 右方像素点
            current = pix[w, h]  # 当前像素点

            # 对r, g, b三个分量进行如下计算
            # 以r分量为例：int(2 * math.sqrt((r[current]-r[bottom])^2 + r[current]-r[right])^2))
            pixel = [int(math.sqrt((item[0] - item[1]) ** 2 + (item[0] - item[2]) ** 2) * 2)
                     for item in zip(current, bottom, right)[:3]]
            pixel.append(current[3])

            pix[w, h] = tuple([min(max(0, i), 255) for i in pixel])  # 限制各分量值介于[0, 255]

    return img


def opposition(img):
    im_array = array(img)

    im_array = 255 - im_array

    return Image.fromarray(im_array)


#
# img = glowing_edge(img)
# img = opposition(glowing_edge(img))

# box = (100, 100, 400, 400)
# region = img.crop(box)
# region = region.transpose(Image.ROTATE_180)
# img.paste(region, box)


def getBlending(mode, top, bottom):
    t_pix = top.load()
    b_pix = bottom.load()
    width = top.size[0]
    height = top.size[1]

    newImg = Image.new('RGBA', (width, height), 0)
    n_pix = newImg.load()

    method = mode()

    for x in range(width):
        for y in range(height):
            r, g, b, a = t_pix[x, y]
            n_pix[x, y] = (method.doBlend(t_pix[x, y][0], b_pix[x, y][0]),
                           method.doBlend(t_pix[x, y][1], b_pix[x, y][1]),
                           method.doBlend(t_pix[x, y][2], b_pix[x, y][2]),
                           )

    return newImg


def convertToArgb(img):
    return img.convert('RGBA')


def colorize(img, red, green, blue):
    '''
    @效果：颜色渲染
    @param img: instance of Image
    @return: instance of Image
    '''

    red = max(0, red)
    red = min(255, red)
    green = max(0, green)
    green = min(255, green)
    blue = max(0, blue)
    blue = min(255, blue)

    gray_img = img.convert("L")

    width, height = img.size
    pix = img.load()
    gray_pix = gray_img.load()

    for w in xrange(width):
        for h in xrange(height):
            gray = gray_pix[w, h]
            r, g, b = pix[w, h]

            r = int(red * gray / 255)
            g = int(green * gray / 255)
            b = int(blue * gray / 255)

            pix[w, h] = r, g, b

    return img


def lighting(img, power, center=None):
    '''
    @效果：灯光
    @param img: instance of Image
    @param power: 光照强度
    @param center: 光源坐标(x, y)，默认在图片中心
    @return: instance of Image
    '''
    if img.mode != "RGB":
        img = img.convert("RGB")

    width, height = img.size

    if center is None:
        center = width / 2, height / 2

    radius = int(math.sqrt(center[0] ** 2 + center[1] ** 2))  # 半径

    pix = img.load()

    for w in xrange(width):
        for h in xrange(height):
            # 当前像素点到光源中心距离
            distance = int(math.sqrt((w - center[0]) ** 2 + (h - center[1]) ** 2))

            if distance < radius:
                brightness = power * (radius - distance) / radius
                # 光亮值和到光源中心的距离成反比

                r, g, b = pix[w, h]
                r = min(r + brightness, 255)
                g = min(g + brightness, 255)
                b = min(b + brightness, 255)
                a = 255
                pix[w, h] = r, g, b

    return img


def getSim(rgb, r, g, b):
    return sqrt((rgb[0] - r) ^ 2 + (rgb[1] - g) ^ 2 + rgb[2] ^ 2)


def solarize(img):
    '''
    @效果：曝光
    @param img: instance of Image
    @return: instance of Image
    '''
    if img.mode != "RGB":
        img = img.convert("RGB")

    return img.point(lambda i: i ^ 0xFF if i < 128 else i)


def changeColor(img):
    img_pix = img.load()
    width = img.size[0]
    height = img.size[1]
    for x in range(width):
        for y in range(height):
            print getSim(img_pix[x, y], 255, 255, 255)
    return img


img = Image.open('demo.png')

img.show()

t_pix = img.load()

img_copy = img.copy()
#
img = opposition(glowing_edge(img))
#
img = img.filter(GaussianBlur(radius=2))
#

img = getBlending(BlendFilter.Multiply, img,
                  img_copy)

img = lighting(img, 100, (554, 10))

# img = img.point(lambda i: i * 1.1)

for x in range(img.size[0]):
    for y in range(img.size[1]):
        if getSim(t_pix[x, y], 255, 255, 255) < 7:
            print "change:" + str(x) + ":" + str(y)
            t_pix[x, y] = (int(t_pix[x, y][0] * 0.7),
                           int(t_pix[x, y][1] * 1.7),
                           int(t_pix[x, y][2] * 1.1))
        if getSim(t_pix[x, y], 0, 0, 0) < 7:
            print "change:" + str(x) + ":" + str(y)
            t_pix[x, y] = (int(t_pix[x, y][0] * 0.92),
                           int(t_pix[x, y][1]),
                           int(t_pix[x, y][2] * 0.1))

img.show()

# img_copy = img.copy()
# #
# img = opposition(glowing_edge(img))
# #
# img = img.filter(GaussianBlur(radius=2))
# #
#
# img = getBlending(BlendFilter.Multiply, img,
#                   img_copy)
#
# img = lighting(img, 100, (554, 10))
#
# # img = img.point(lambda i: i * 1.1)
#
# img.show()
#
# changeColor(img)
