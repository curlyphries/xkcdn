import click
import json
import requests

@click.command() # See click decorators
@click.option('--output', default=None, help='Output file') # output file
@click.option('--num', default=None, help='Comic number to retrieve')
def cli(output, num):
    if (num == None):
        r = requests.get("http://xkcd.com/info.0.json") # get latest comic
    else:
        try: 
            r = requests.get("https://xkcd.com/{}/info.0.json".format(str(num)))
        except requests.ConnectionError:
            print("Comic Not Found")
    data = json.loads(r.text) # make it a dict
    if (output == None): ## If no output is given, give it the comic number
        file = open(str(data['num']) + ".png", 'wb') # kludgy way to take the number and append .png
    else:
        file = open(str(output), 'wb')
    res = requests.get(data["img"]) # get the comic
    file.write(res.content) # write it.
    print("Title Text: " + data['alt'])