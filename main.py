# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os , glob
from os import error
import logging
import pyrogram
import time
import math
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message, Sticker, Document

    
bughunter0 = Client(
    "Sticker-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_STRING = """ Hi {}, 
I'm an AIO Sticker Bot.

● I can do many thing for you, just like Get PNG image format of any sticker,Get Sticker ID and Find Sticker via Its Sticker ID. 

● Still Wonder How I Work ? 
● Use /help to get a Full Brief on How i Works.

"""

HELP_STRING = """ Hi {}, 
Wonder How I Work ?

Here is Full Description How i Works.

1️⃣ Ping ( /ping ) - To Check Bot is alive or not.
If bot replies with some text then bot is alive
2️⃣ Get Sticker ( /getsticker ) - This Command give you a PNG image format of the replied Sticker
3️⃣ Sticker ID ( /stickerid ) - Reply with a sticker and Get Sticker ID and a Unique ID.
4️⃣ Find Sticker ( /findsticker ) - Reply to you Sticker ID or Unique ID of Sticker to Get your Sticker Back

"""

@bughunter0.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
       await message.reply(f"**Sticker ID is**  \n `{message.reply_to_message.sticker.file_id}` \n \n ** Unique ID is ** \n\n`{message.reply_to_message.sticker.file_unique_id}`", quote=True)
    else: 
       await message.reply("Oops !! Not a sticker file")

JOIN_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Updates Channel ⬆️' ,url='https://t.me/MetaverseNetwork'),
        InlineKeyboardButton('Support Group 🆘' ,url='https://t.me/MetaverseNetwork')
        ]]
    )

HELP_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Updates Channel ⬆️' ,url='https://t.me/MetaverseNetwork'),
        InlineKeyboardButton('Support Group 🆘' ,url='https://t.me/MetaverseNetwork')
        ]]
    
    )
        
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")

@bughunter0.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_STRING.format(update.from_user.mention)
    reply_markup = JOIN_BUTTON
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )

@bughunter0.on_message(filters.command(["help"]))
async def start(bot, update):
    text = HELP_STRING.format(update.from_user.mention)
    reply_markup = HELP_BUTTON
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )
    
@bughunter0.on_message(filters.command(["ping"]))
async def ping(bot, message):
    start_t = time.time()
    rm = await message.reply_text("Checking")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")


@bughunter0.on_message(filters.private & filters.command(["getsticker"]))
async def getstickerasfile(bot, message):  
    tx = await message.reply_text("Checking Sticker")
    await tx.edit("Validating sticker..")
    if message.reply_to_message.sticker is False:
        await tx.edit("Not a Sticker File!!")
    else :
          if message.reply_to_message is None: 
               tx =  await tx.edit("Reply to a Sticker File!")       
          else :
               if message.reply_to_message.sticker.is_animated:
                   try :     
                        tx = await message.reply_text("Downloading...")
                        file_path = DOWNLOAD_LOCATION + f"{message.chat.id}.tgs"
                        await message.reply_to_message.download(file_path)  
                        await tx.edit("Downloaded") 
                    #   zip_path= ZipFile.write("")
                        await tx.edit("Uploading...")
                        start = time.time()
                        await message.reply_document(file_path,caption="© @MetaverseNetwork")
                        await tx.delete()   
                        os.remove(file_path)
                    #   os.remove(zip_path)
                   except Exception as error:
                        print(error)
 
               elif message.reply_to_message.sticker.is_animated is False:        
                   try : 
                       tx = await message.reply_text("Downloading...")
                       file_path = DOWNLOAD_LOCATION + f"{message.chat.id}.png"
                       await message.reply_to_message.download(file_path)   
                       await tx.edit("Downloaded")
                       await tx.edit("Uploading...")
                       start = time.time()
                       await message.reply_document(file_path,caption="© @MetaverseNetwork")
                       await tx.delete()   
                       os.remove(file_path)
                   except Exception as error:
                       print(error)

@bughunter0.on_message(filters.private & filters.command(["clearcache"]))
async def clearcache(bot, message):   
    # Found some Files showing error while Uploading, So a method to Remove it !!  
    txt = await message.reply_text("Checking Cache")
    await txt.edit("Clearing cache")
    dir = DOWNLOAD_LOCATION
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist :
           i =1
           os.remove(f)
           i=i+1
    await txt.edit("Cleared "+ str(i) + "File") 
    await txt.delete()
    
@bughunter0.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
       await message.reply(f"**Sticker ID is**  \n `{message.reply_to_message.sticker.file_id}` \n \n ** Unique ID is ** \n\n`{message.reply_to_message.sticker.file_unique_id}`", quote=True)
    else: 
       await message.reply("Oops !! Not a sticker file")


@bughunter0.on_message(filters.private & filters.command(["findsticker"]))
async def findsticker(bot, message):  
  try:
       if message.reply_to_message: 
          txt = await message.reply_text("Validating Sticker ID")
          stickerid = str(message.reply_to_message.text)
          chat_id = str(message.chat.id)
          await txt.delete()
          await bot.send_sticker(chat_id,f"{stickerid}")
       else:
          await message.reply_text("Please reply to a ID to get its STICKER.")
  except Exception as error:
        txt = await message.reply_text("Not a Valid File ID")

      
bughunter0.run()
