import os
import sys
import time
import shutil
import asyncio
import zipfile
from pathlib import Path

from pyrogram.types import Message

from Tempest import app, gen




app.CMD_HELP.update(
    {"zip" : (
        "zip",
        {
        "zip [reply to file]" : "Zip a file and save it in your local directories.",
        "unzip [file path]" : "Unzip a file and save it in your local directories.",
        "new [file name]" : "Create a python file with your codes."
        }
        )
    }
)



async def unzipfiles(zippath):
    foldername = zippath.split("/")[-1]
    extract_path = f"./downloads/{foldername}"
    shutil.unpack_archive(zippath, extract_path)
    return extract_path




@app.on_message(gen("zip", exclude =["sudo"]))
async def zip_handler(_, m: Message):
    reply = m.reply_to_message
    if not reply:
        return await app.send_edit(f"Reply to a file. . .", text_type=["mono"], delme=4)

    elif reply:
        if not reply.media:
            return await app.send_edit("Reply to some media . . .", text_type=["mono"])

        await app.send_edit("Zipping . . .", text_type=["mono"])

        if app.TEMP_DICT:
            loc = app.TEMP_DICT
        else:
            loc = "./downloads"
        dl = await app.download_media(
            reply,
            block=False
        )
        zipfile.ZipFile(dl.replace("/app/downloads/", "") + ".zip", "w").write(dl)
        place = dl.replace("/app/downloads/", "") + ".zip"
        await app.send_edit(f"**Your file is compressed and saved here:** \n`{place}`")
    else:
        await app.send_edit("Something went wrong . . .", delme=3, text_type=["mono"])




@app.on_message(gen("unzip", exclude =["sudo"]))
async def unzip_handler(_, m: Message):
    if app.long() == 2:
        if app.textlen() <= 4096:
            loc = m.text.split(None, 1)[1]
            await app.send_edit("Unzipping file . . .", text_type=["mono"])
            extract_path = await unzipfiles(loc)
            await app.send_edit(f"File unzipped and saved here: `{extract_path}`")
        elif app.textlen() > 4096:
            await app.send_edit("Text is too long !", delme=4, text_type=["mono"])
    else:
        await app.send_edit("Give me the file path to unzip the file . . .", delme=4, text_type=["mono"])




@app.on_message(gen("new", exclude =["sudo"]))
async def createfile_handler(app, m:Message):
    reply = m.reply_to_message
    mytext = "Making file . . ."
    filepath = None

    try:
        if app.textlen() > 4096:
            return await app.send_edit("The message is too long. (it must be <= 4096)", delme=4, text_type=["mono"])

        if app.long() == 1:
            return await app.send_edit("Give me filename & content of file after command.", text_type=["mono"], delme=4)

        if reply and app.long() >= 2:
            name = m.text.split(None, 1)[1]
            await app.send_edit(mytext, text_type=["mono"])
            text = reply.text or reply.caption or "None"
            await app.create_file(
                filename=name, 
                content=text,
                send=True
            )

        # if replied to text without file name
        elif not reply and app.long() >= 3:
            await app.send_edit(mytext, text_type=["mono"])
            name = m.text.split(None, 1)[1]
            text = m.text.split(None, 2)[2]
            await app.create_file(
                filename=name, 
                content=text,
                send=True
            )

        # if replied to text with file name
        elif not reply and app.long() == 1:
            await app.send_edit("Are you dumb, give me the file contents with the file name.", text_type=["mono"], delme=4)

        else:
            await app.send_edit("Something went wrong !")

    except Exception as e:
        await app.error(e)





