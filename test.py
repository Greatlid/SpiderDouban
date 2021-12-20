from PIL import Image,ImageEnhance,ImageFilter
import pytesseract
class img():
    def pre_concert(self,img):   #采用二值化去除背景色,即仅保留黑、白两色。
        width, height = img.size
        threshold = 30
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        for i in range(0, width):
            for j in range(0, height):
                p = img.getpixel((i, j))  # 抽取坐标（i,j）出像素点的RGB颜色值
                #print(p)#(255, 255, 255, 255)
                r,g,b= p
                if r > threshold or g > threshold or b > threshold:
                    img.putpixel((i, j), WHITE)#设置坐标（i,j）处像素点的RGB颜色值为（255.255.255）
                else:
                    img.putpixel((i, j), BLACK)
        print('二值化去除背景色')
        # img.show()
        image_name="./pre_fig.png"
        img.save(image_name)
        return self.noise_remove_pil(image_name,4)
    from PIL import Image
    def noise_remove_pil(self,image_name, k):
        """
        8邻域降噪
        Args:
            image_name: 图片文件命名
            k: 判断阈值

        Returns:

        """

        def calculate_noise_count(img_obj, w, h):
            """
            计算邻域非白色的个数
            Args:
                img_obj: img obj
                w: width
                h: height
            Returns:
                count (int)
            """
            count = 0
            width, height = img_obj.size
            for _w_ in [w - 1, w, w + 1]:
                for _h_ in [h - 1, h, h + 1]:
                    if _w_ > width - 1:
                        continue
                    if _h_ > height - 1:
                        continue
                    if _w_ == w and _h_ == h:
                        continue
                    if img_obj.getpixel((_w_, _h_)) < 230:  # 这里因为是灰度图像，设置小于230为非白色
                        count += 1
            return count

        img = Image.open(image_name)
        # 灰度
        gray_img = img.convert('L')

        w, h = gray_img.size
        for _w in range(w):
            for _h in range(h):
                if _w == 0 or _h == 0:
                    gray_img.putpixel((_w, _h), 255)
                    continue
                # 计算邻域非白色的个数
                pixel = gray_img.getpixel((_w, _h))
                if pixel == 255:
                    continue

                if calculate_noise_count(gray_img, _w, _h) < k:
                    gray_img.putpixel((_w, _h), 255)
        gray_img_name='./noise_remove_pil.png'
        gray_img.save('./noise_remove_pil.png')
        print('降噪处理')
        gray_img.show()
        return self.jiangzao(gray_img_name)
    def jiangzao(self,gray_img_name):
        # 要去掉黑点，就是一个二值化降噪的过程。可以用PIL（Python Image Library）试试
        im = Image.open(gray_img_name)
        im = im.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(2)
        im = im.convert('1')
        im.save('./jiangzao.png')
        im.show()
        return self.ocr(im)

    def ocr(self,im):  ##传入图片进行识别
        #gray_img=Image.open(gray_img_name)
        pytesseract.pytesseract.tesseract_cmd = 'D:/tesseract_OCR/tesseract.exe'
        # text = pytesseract.image_to_string(Image.open('./tmp/jiangzao.png'),lang='chi_sim')##,lang='eng 数字
        text = pytesseract.image_to_string(im, lang='eng')
        print(text)
img0=Image.open('./yanzheng.jfif')
img=img()
img.pre_concert(img0)
