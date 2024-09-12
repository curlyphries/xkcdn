import click
import json
import requests
from PIL import Image
from io import BytesIO
import random
import os  # Added for directory handling

# Set the default download directory
default_output_dir = "./comics/"

@click.command()  # See click decorators
@click.option('--output', default=None, help='Output file')  # Output file
@click.option('--num', default=None, help='Comic number to retrieve')
@click.option('--popup', flag_value=True, default=False, help="Show in Pillow window")
@click.option('--random', 'randYN', flag_value=True, default=False, help="Get random comic")
def cli(output, num, popup, randYN):
    if (output != None and popup == True):
        raise Exception("Cannot download and not download comic.")
    
    if (num == None and randYN != True):
        r = requests.get("http://xkcd.com/info.0.json")  # get latest comic
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

    data = json.loads(r.text)  # make it a dict
    res = requests.get(data["img"])  # get the comic
    
    if popup != True:
        if output == None:  # If no output is given, use the default directory and comic number
            output = os.path.join(default_output_dir, str(data['num']) + ".png")
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output), exist_ok=True)

        file = open(output, 'wb')
    else:  # popup mode is enabled
        img = Image.open(BytesIO(res.content))  # get the image bytes
        img.show()  # pop

    if popup != True:
        file.write(res.content)  # write it.
        print(f"Comic saved to {output}")
    
    print("Title Text: " + data['alt'])  # print the title text
