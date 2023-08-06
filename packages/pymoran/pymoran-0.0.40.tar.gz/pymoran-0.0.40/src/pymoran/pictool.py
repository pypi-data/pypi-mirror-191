from PIL import Image, ImageDraw, ImageFilter


class PicStyleClass:
    def __init__(self) -> None:
        pass

    def border_radius(self, img: Image.Image, radius: int):
        '''
        为图像生成圆角
        :param img 需要处理的图像
        :param radius 圆角半径
        return {Image.Image} 处理后的图像
        '''
        # 处理原图并获取基本信息
        img = img.convert('RGBA')
        w, h = img.size

        # 生成一个宽为圆角直径的黑色方块
        img_rec = Image.new('L', (radius * 2, radius * 2), 0)
        # 创建绘制对象
        draw = ImageDraw.Draw(img_rec)
        # 方块内绘制一个内切白色圆形
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

        # 创建一个alpha层，存放四个圆角，使用透明度切除圆角外的图片
        alpha = Image.new('L', img.size, 255)

        # 粘贴左上角
        alpha.paste(img_rec.crop((0, 0, radius, radius)), (0, 0))
        # 粘贴右上角
        alpha.paste(img_rec.crop(
            (radius, 0, radius * 2, radius)), (w - radius, 0))
        # 粘贴左下角
        alpha.paste(img_rec.crop(
            (0, radius, radius, radius * 2)), (0, h - radius))
        # 粘贴右下角
        alpha.paste(img_rec.crop((radius, radius, radius * 2, radius * 2)),
                    (w - radius, h - radius))
        # alpha替换，白色透明，黑色隐藏
        img.putalpha(alpha)

        # 绘制圆角边框
        # draw = ImageDraw.Draw(img)
        # print(img.getbbox())
        # draw.rounded_rectangle(img.getbbox(),
        #                        outline="black",
        #                        width=3,
        #                        radius=radius)
        return img

    def box_shadow(self, img: Image.Image,
                   bgcolor: str = 'white',
                   shadowcolor: str = '#666666',
                   offset: tuple = (0, 0),
                   border: int = 10,
                   radius: int = 5):
        '''
        为图像增加阴影
        :param img 需要处理的图像
        :param bgcolor 阴影图层背景色，默认white
        :param shadowcolor 阴影颜色，默认#666666
        :param offset 阴影偏移量，默认(0,0)不做任何偏移，建议为偶数，遵循左、上原则
        :param border 边框宽度，默认你10，容纳阴影的范围
        :param radius 模糊半径，默认50，值越大模糊越多
        return {Image.Image} 处理后的图像
        '''
        # 处理原图并获取基本信息
        img = img.convert('RGBA')
        w, h = img.size

        # 创建阴影图层
        SHADOW_W = w + abs(offset[0]) + border * 2
        SHADOW_H = h + abs(offset[1]) + border * 2
        img_shadow = Image.new(img.mode, (SHADOW_W, SHADOW_H))

        # 绘制阴影
        SHADOW_LEFT = border + max(offset[0], 0)
        SHADOW_TOP = border + max(offset[1], 0)
        img_shadow.paste(
            shadowcolor,
            [SHADOW_LEFT, SHADOW_TOP, w + SHADOW_LEFT, h + SHADOW_TOP])
        for i in range(radius):
            img_shadow = img_shadow.filter(ImageFilter.BLUR)
        img_shadow.show()

        # # 为阴影添加圆角
        # img_shadow=border_radius(img_shadow,120)

        # 组合图像
        IMG_LEFT = border - min(offset[0], 0)
        IMG_TOP = border - min(offset[1], 0)
        img_shadow.paste(img, (IMG_LEFT, IMG_TOP), img)

        return img_shadow
