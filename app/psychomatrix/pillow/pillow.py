from dataclasses import dataclass
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw

from . import config


@dataclass
class Pillow:

    @staticmethod
    def _open_image() -> Image:
        image = config.IMAGE

        return Image.open(image)

    @classmethod
    def _paste_birth_date(cls, draw: ImageDraw, birth_date: str) -> bool:
        draw_options = {
            'font': ImageFont.truetype(config.FONT,
                                       size=config.FONT_SIZE_BIRTH_DATE),
            'fill': config.FILL_BIRTH_DATE,
            'anchor': config.ANCHOR
        }
        draw.text(config.XY_BIRTH_DATE, text=birth_date, **draw_options)

        return True

    @staticmethod
    def _paste_numbers(draw: ImageDraw, numbers: list[str]) -> bool:
        draw_options = {
            'font': ImageFont.truetype(config.FONT, size=config.FONT_SIZE_NUM),
            'fill': config.FILL_NUM,
            'anchor': config.ANCHOR
        }
        draw.text(config.XY_0, text=numbers[0], **draw_options)
        draw.text(config.XY_1, text=numbers[1], **draw_options)
        draw.text(config.XY_2, text=numbers[2], **draw_options)
        draw.text(config.XY_3, text=numbers[3], **draw_options)
        draw.text(config.XY_4, text=numbers[4], **draw_options)
        draw.text(config.XY_5, text=numbers[5], **draw_options)
        draw.text(config.XY_6, text=numbers[6], **draw_options)
        draw.text(config.XY_7, text=numbers[7], **draw_options)
        draw.text(config.XY_8, text=numbers[8], **draw_options)
        draw.text(config.XY_9, text=numbers[9], **draw_options)
        draw.text(config.XY_10, text=numbers[10], **draw_options)
        draw.text(config.XY_11, text=numbers[11], **draw_options)
        draw.text(config.XY_12, text=numbers[12], **draw_options)
        draw.text(config.XY_13, text=numbers[13], **draw_options)
        draw.text(config.XY_14, text=numbers[14], **draw_options)
        draw.text(config.XY_15, text=numbers[15], **draw_options)
        draw.text(config.XY_16, text=numbers[16], **draw_options)

        return True

    async def create_image(self, numbers: list[str], birth_date: str) -> bytes:
        image = self._open_image()
        draw = ImageDraw.Draw(image)

        self._paste_birth_date(draw, birth_date)
        self._paste_numbers(draw, numbers)

        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=100)

        return buffer.getvalue()
