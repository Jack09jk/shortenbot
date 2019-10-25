from telethon import events
import subprocess
import os
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import asyncio
import time
from pathlib import Path
from xtrabot import loader, utils

class WebUpload(loader.module):
    async def _(event):
        if event.fwd_from:
        return
        event = await utils.answer(event, "Processing...")
        PROCESS_RUN_TIME = 100
        input_str = event.text.split(" ", maxsplit=2)[1]
        selected_transfer = event.text.split(" ", maxsplit=2)[2]
        if input_str:
            file_name = input_str
        else:
            reply = await event.get_reply_message()
            file_name = await bot.download_media(reply.media, Var.TEMP_DOWNLOAD_DIRECTORY)
        file_temp_name = Path(file_name).stem
        reply_to_id = event.message.id
        CMD_WEB = {"anonfiles": "curl -F \"file=@{}\" https://anonfiles.com/api/upload", "transfer": "curl --upload-file \"{}\" https://transfer.sh/{}", "filebin": "curl -X POST --data-binary \"@test.png\" -H \"filename: {}\" \"https://filebin.net\"", "anonymousfiles": "curl -F file=\"@{}\" https://api.anonymousfiles.io/", "megaupload": "curl -F \"file=@{}\" https://megaupload.is/api/upload", "bayfiles": ".exec curl -F \"file=@{}\" https://bayfiles.com/api/upload"}
        try:
            selected_one = CMD_WEB[selected_transfer].format(file_name, file_temp_name)
        except KeyError:
            await utils.answer(event, "Invalid transfer option selected")
        cmd = selected_one
        start_time = time.time() + PROCESS_RUN_TIME
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        output = f"**OUTPUT**:\n`{stdout.decode()}`\n\n**INFO**:\n`{stderr.decode()}`"
        await utils.answer(event, output)