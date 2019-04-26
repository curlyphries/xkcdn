import click
import json
import requests
from PIL import Image
from io import BytesIO
import random

@click.command() # See click decorators
@click.option('--output', default=None, help='Output file') # output file
@click.option('--num', default=None, help='Comic number to retrieve')
@click.option('--popup', flag_value=True, default=False, help="Show in Pillow window")
@click.option('--random', 'randYN', flag_value=True, default=False, help="Get random comic")
def cli(output, num, popup, randYN):
    if (output != None and popup == True):
        raise Exception("Cannot download and not download comic.")
    if (num == None and randYN != True):
        r = requests.get("http://xkcd.com/info.0.json") # get latest comic
    elif (randYN == True):
        ra = requests.get("http://xkcd.com/info.0.json")
        raData = json.loads(ra.text)
        raRes = int(raData["num"])
        num = random.randint(1, raRes+1)
        r = requests.get("https://xkcd.com/{}/info.0.json".format(num))
    else:
        try: 
            r = requests.get("https://xkcd.com/{}/info.0.json".format(num))
        except requests.ConnectionError:
            raise Exception("404 Not Found")
    data = json.loads(r.text) # make it a dict
    res = requests.get(data["img"]) # get the comic
    if (popup != True):
        if (output == None): ## If no output is given, give it the comic number
            file = open(str(data['num']) + ".png", 'wb') # kludgy way to take the number and append .png
        else:
            file = open(str(output), 'wb')
    else: # popup mode is enabled
        img = Image.open(BytesIO(res.content)) # get the image bytes
        img.show() # pop
    if (popup != True):
        file.write(res.content) # write it.
    print("Title Text: " + data['alt']) # print the title text