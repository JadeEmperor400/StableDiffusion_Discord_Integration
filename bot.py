import disnake
import os
from disnake.ext import commands
from PIL import Image
from io import BytesIO
import base64
import requests
import uuid

bot = commands.InteractionBot(test_guilds=[]) #Insert Testguild Number

@bot.slash_command()
async def ping(inter):
    await inter.response.send_message("Pong!")

@bot.slash_command()
async def testimg(inter):
    with open("sampleimg.txt", "r") as f:
        txt = f.read()
        myIMG =  BytesIO( base64.b64decode(txt))
        file = disnake.File(myIMG, "SAMP_IMG.png")
        await inter.response.send_message("Sample Image", file = file)

@bot.slash_command()
async def makeme(inter, message:str):
    await inter.response.send_message("Give me a second. . .")

    payload = {
        "prompt":message,
        "sampler_index": "Euler"
    }

    response = requests.post("http://host.docker.internal:7860/sdapi/v1/txt2img", json=payload)
    resp = response.json()
    image = resp["images"][0]
    myIMG =  BytesIO( base64.b64decode(image))
    imageName = uuid.uuid4()
    file = disnake.File(myIMG, f"{imageName}.png")
    #requests.post("http://docker.internal.host:7860")
    await inter.followup.send("Sample Image", file = file)

bot.run(os.environ['BOT_API_KEY'])