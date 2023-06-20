import logging

import aiohttp
import secrets

from . import config
from .types import Account, Page, Image
from .utils import json_dumps, html_to_nodes
from .exceptions import (TelegraphException, RetryAfterError, ContentTooBigError,
                         FileTypeError, FileToBigError, FileEmptyError)


class Telegraph:

    def __init__(self):
        self.api_url = config.API_URL
        self.base_url = config.BASE_URL

    async def _method(self, method: str, data: dict = None, path: str = ''):
        data = data.copy() if data is not None else {}
        data['access_token'] = config.get_access_token()

        async with aiohttp.ClientSession() as session:
            response = await session.post(url=self.api_url.format(
                method=method, path=path), data=data, trust_env=True)
            json_response = await response.json()

            if isinstance(json_response, list):
                error = json_response[0].get('error')
            else:
                error = json_response.get('error')

            if error:
                if isinstance(error, str) and error.startswith("CONTENT_TOO_BIG"):
                    raise ContentTooBigError
                elif isinstance(error, str):
                    raise TelegraphException(error)
                else:
                    logging.error(error)
                    raise TelegraphException(json_response)

            return json_response.get('result')

    async def create_account(self,
                             short_name: str,
                             author_name: str = '',
                             author_url: str = ''
                             ):
        """
        Use this method to create a new Telegraph account

        :param short_name: Account name, helps users with several accounts
         remember which they are currently using
        :param author_name: Default author name used when creating new articles
        :param author_url: Default profile link, opened when users click
         on the author's name below the title
        """
        data = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        response = await self._method('createAccount', data=data)

        return Account(**response)

    async def create_page(self,
                          title: str,
                          html_content: str,
                          author_name: str = '',
                          author_url: str = '',
                          return_content: bool = False
                          ) -> Page:
        """
        Use this method to create a new Telegraph page

        :param title: Page title
        :param html_content: Content in HTML format
        :param author_name: Author name, displayed below the article's title
        :param author_url: Profile link, opened when users click
         on the author's name below the title
        :param return_content: If true, a content field will be
         returned to the Page object
        """
        content = html_to_nodes(html_content)
        content_json = json_dumps(content)

        data = {
            'title': title,
            'author_name': author_name,
            'author_url': author_url,
            'content': content_json,
            'return_content': return_content
        }
        response = await self._method('createPage', data=data)

        return Page(**response)

    async def upload_image(self, image: bytes) -> Image:
        """
        Allowed only .jpg, .jpeg and .png files.
        :param image: bytes
        """
        form = aiohttp.FormData(quote_fields=False)
        form.add_field(secrets.token_urlsafe(8), image)

        async with aiohttp.ClientSession() as session:
            response = await session.post(url=self.base_url.format(
                endpoint="upload"), data=form, trust_env=True)
            json_response = await response.json()

            if isinstance(json_response, list):
                error = json_response[0].get('error')
            else:
                error = json_response.get('error')

            if error:
                if isinstance(error, str) and 'flood' in error.lower():
                    raise RetryAfterError(error)
                elif isinstance(error, str) and error.startswith('File type invalid'):
                    raise FileTypeError(error)
                elif isinstance(error, str) and error.startswith('File too big'):
                    raise FileToBigError(error)
                elif isinstance(error, str) and error.startswith('File empty'):
                    raise FileEmptyError(error)

                else:
                    logging.error(error)
                    raise TelegraphException(error)

            return [Image(**obj) for obj in json_response][0]
