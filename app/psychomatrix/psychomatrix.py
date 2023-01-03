from app.database.models import PsychomatrixBasicContent
from app.database.models import PsychomatrixAdditionalContent

from . import html_const

from .pillow import Pillow
from .calculator import Calculator

from .telegraph import Telegraph
from .telegraph import config as telegraph_config
from .telegraph.types import Page
from .telegraph.exceptions import TelegraphException, ContentTooBigError


class Psychomatrix(Calculator):

    @classmethod
    async def __get_basic_content(cls, numbers: list[str]) -> str:
        codes = [
            f'{enum}-нет' if num == '-' else num for enum, num in
            enumerate(numbers, start=1)
        ]
        contents = await PsychomatrixBasicContent.get_in(codes)
        html_content = html_const.BASIC_CONTENT

        html_content += '<hr>'.join(
            f'''{html_const.BASIC_CONTENT_TITLE.format(r.title)
            if r.title else ""}
                {html_const.BASIC_CONTENT_TEXT.format(r.text)
            if r.text else ""}
                {html_const.BASIC_CONTENT_ADVICE.format(r.advice)
            if r.advice else ""}
                {html_const.BASIC_CONTENT_RECOMMENDATION.format(r.recommendation)
            if r.recommendation else ""}
            ''' for r in contents
        )

        return html_content

    @classmethod
    async def __get_additional_content(cls, numbers: list[str]) -> str:
        codes = [
            f'{enum}-0' if num == '-' else f'{enum}-{num}'
            if enum not in [8, 3] else f'{enum}-'
            for enum, num in
            enumerate(numbers, start=1)
        ]
        contents = await PsychomatrixAdditionalContent.get_in(codes)
        html_content = html_const.ADDITIONAL_CONTENT

        html_content += '<hr>'.join(
            f'''{html_const.ADDITIONAL_CONTENT_TITLE.format(r.title)
            if r.title else ""}
                {html_const.ADDITIONAL_CONTENT_LEVEL.format(r.level)
            if r.level else ""}
                {html_const.ADDITIONAL_CONTENT_ANNOTATION.format(r.annotation)
            if r.annotation else ""}
                {html_const.ADDITIONAL_CONTENT_TEXT.format(r.text)
            if r.text else ""}
            ''' for r in contents
        )

        return html_content

    async def _create_content(self, numbers: list[str]) -> list[str]:
        html_basic_content = await self.__get_basic_content(
            numbers=numbers[:9]
        )
        html_additional_content = await self.__get_additional_content(
            numbers=numbers[9:]
        )

        return [html_basic_content, html_additional_content]

    @staticmethod
    async def _create_image(numbers: list[str],
                            birth_date: str) -> bytes:
        pillow = Pillow()
        return await pillow.create_image(numbers, birth_date)

    async def create_page(self) -> Page:
        telegraph = Telegraph()
        author_url = telegraph_config.AUTHOR_URL
        author_name = telegraph_config.AUTHOR_NAME

        numbers = self.get_all_numbers()
        date = self.date.strftime('%-d %B %Y г.')

        contents = await self._create_content(numbers)
        image = await self._create_image(numbers, date)
        image = await telegraph.upload_image(image)

        html_image = html_const.IMAGE_CONTENT.format(image.url)
        html_source = html_const.SOURCE_CONTENT

        html_basic = contents[0]
        html_additional = contents[1]

        try:
            title_page = html_const.BASIC_TITLE_PAGE.format(date)
            html_content = html_image + html_basic + html_additional + html_source

            return await telegraph.create_page(
                title=title_page, html_content=html_content,
                author_name=author_name, author_url=author_url
            )

        except ContentTooBigError:
            additional_title_page = html_const.ADDITIONAL_TITLE_PAGE.format(date)
            additional_html_content = html_image + html_additional + html_source

            additional_page = await telegraph.create_page(
                title=additional_title_page, html_content=additional_html_content,
                author_name=author_name, author_url=author_url
            )

            title_page = html_const.BASIC_TITLE_PAGE.format(date)
            html_additional_button = html_const.ADDITIONAL_CONTINUE.format(additional_page.url)
            html_content = html_image + html_basic + html_additional_button + html_source

            return await telegraph.create_page(
                title=title_page, html_content=html_content,
                author_name=author_name, author_url=author_url
            )
