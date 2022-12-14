"""
Inline about page for help menu.
"""

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardMarkup,
	InputMediaPhoto,
	CallbackQuery
)

from Tempest.userbot.client import app





@app.bot.on_callback_query(filters.regex("about-tab"))
@app.alert_user
async def _about(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(
            media="Tempest/core/resources/images/shion.png", 
            caption=app.about_tab_string()
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                app.bot.BuildKeyboard(
                    (
                        ["Home", "close-tab"],
                        ["Back", "home-tab"]
                    )
                )
            ]
        )
    )
