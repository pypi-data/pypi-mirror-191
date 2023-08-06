import re
from typing import Dict, Tuple
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image

zh_pt = re.compile(r"[\u4e00-\u9fa5|\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5]")

en_pt = re.compile(r"[a-zA-Z]")


def is_zh(char: str):
    return not not zh_pt.match(char)


def is_en(char: str):
    return not not en_pt.match(char)


class Drawer:
    '''绘制器

    示例代码：

    ```
    from easy_wrap import Drawer

    text = "... the text you want to render ....测试自动换行"

    font_path = "msyh.ttc"
    font_size = 30
    drawer = Drawer(font_path, font_size)

    image_width = 180
    canvas = drawer.draw_text(text, image_width)

    # save the image
    canvas.save(open("test.png", "wb")) 
    ```
    '''

    def __init__(self, fontpath: str, fontsize: int = 26) -> None:
        self._canvas = Image.new('RGB', (100, 100))
        self._draw = ImageDraw.Draw(self._canvas)
        self._font = ImageFont.truetype(fontpath, fontsize)
        
        self.char_width_dict: Dict[str, int] = {}
        '''所有字符的渲染宽度'''
        
        h1 = self.get_text_height("a\na")
        h2 = self.get_text_height("a")
        self.char_height: int = h1 - h2
        '''所有字符的渲染高度'''

    def get_text_height(self, text: str):
        """获取文本渲染后的高度

        Args:
            text (str): 文本

        Returns:
            int|None: 当bbox为None时返回None，否则返回高度
        """        
        self._draw.rectangle((0, 0, 100, 100), fill=(0, 0, 0))
        self._draw.text((0, 0), text, font=self._font)
        bbox = self._canvas.getbbox()
        if bbox:
            left, top, right, down = bbox
            return down

    def get_text_width(self, text: str):
        """获取文本渲染后的宽度

        Args:
            text (str): 文本

        Returns:
            int|None: 当bbox为None时返回None，否则返回宽度
        """        
        self._draw.rectangle((0, 0, 100, 100), fill=(0, 0, 0))
        self._draw.text((0, 0), text, font=self._font)
        bbox = self._canvas.getbbox()
        if bbox:
            left, top, right, down = bbox
            return right

    def get_char_width(self, char: str):
        """获取字符渲染后的宽度

        Args:
            char (str): 字符

        Returns:
            int: 返回字符的宽度
        """     
        
        # 汉字宽度一致
        if is_zh(char):
            char = "汉"

        if char not in self.char_width_dict:
            w1 = self.get_text_width(f"[{char}]")
            w2 = self.get_text_width("[]")
            self.char_width_dict[char] = w1 - w2

        return self.char_width_dict[char]

    def auto_wrap(self, text: str, width_max: int):
        """对纯文本自动换行，不渲染图片

        Args:
            text (str): 文本
            width_max (int): 最大宽度

        Returns:
            list[str]: 自动换行后的文本数组
        """
        lines = []
        for chars in text.split("\n"):
            # 换行的最小单位
            units = []

            last_word = ""
            for char in chars:
                if is_en(char):
                    last_word += char
                else:
                    units.append(last_word)
                    units.append(char)
                    last_word = ""
            units.append(last_word)

            width = 0
            line = ""
            for unit in units:
                w = 0
                for char in unit:
                    w += self.get_char_width(char)

                width += w
                if width > width_max:
                    lines.append(line)
                    line = unit
                    width = w
                else:
                    line += unit

            lines.append(line)
        return lines

    def draw_text(self, text: str, width_max: int, ft_color: Tuple[int, int, int] = (0, 0, 0), bg_color: Tuple[int, int, int] = (255, 255, 255)):
        """渲染文本为图片，并自动换行

        Args:
            text (str): 文本
            width_max (int): 图片宽度
            ft_color (Tuple[int, int, int], optional): 字体颜色. Defaults to (0, 0, 0).
            bg_color (Tuple[int, int, int], optional): 背景颜色. Defaults to (255, 255, 255).

        Returns:
            PIL.Image: 图片
        """
        # 自动换行
        lines = self.auto_wrap(text, width_max)
        text = "\n".join(lines)

        # 计算高度
        height_max = len(lines)*self.char_height

        # 绘图
        canvas = Image.new('RGB', (width_max, height_max), color=bg_color)
        draw = ImageDraw.Draw(canvas)
        draw.text((0, 0), text, font=self._font, fill=ft_color)
        return canvas
