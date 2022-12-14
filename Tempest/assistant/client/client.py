"""
This file creates Assistant's client.
"""

from pyrogram import Client
from Tempest.core import Core





class Bot(Core, Client):
    """ Assistant (Shion) """
    def __init__(self):
        super().__init__(
            name="Shion",
            api_id=self.API_ID,
            api_hash=self.API_HASH,
            bot_token=self.TOKEN,
	)
        self.start()
        self.me = self.get_chat("me")
        self.id = self.me.id
        self.dc_id = self.me.dc_id
        self.name = self.me.first_name
        self.username = f"@{self.me.username}"
        self.bio = self.me.bio if self.me.bio else ""
        self.pic = self.download_media(self.me.photo.big_file_id) if self.me.photo else None
        self.is_bot = True
        self.stop()
