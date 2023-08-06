import logging

from instagrapi import Client

from byb.core import Platform, PostContent
from byb.settings import INSTAGRAM_PASSWORD, INSTAGRAM_USERNAME

log = logging.getLogger(__name__)


class BaseInstagramPlatform(Platform):
    """A base class for instagram platforms which handles authentication."""

    __abstract__ = True

    def setup(self, **kwargs):
        username = kwargs.get("username", INSTAGRAM_USERNAME)
        password = kwargs.get("password", INSTAGRAM_PASSWORD)
        self.client = Client()
        self.client.login(username, password)


class InstagramPost(BaseInstagramPlatform):
    """Create a new instagram post"""

    def post(self, content: PostContent, **kwargs) -> PostContent:
        if content.is_video():
            response = self.client.video_upload(content.media, content.text)
            log.info(f"Got video response: {response}")
        elif content.is_image():
            response = self.client.photo_upload(content.media, content.text)
            log.info(f"Got photo response: {response}")
        return content
