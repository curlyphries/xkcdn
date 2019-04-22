import click
import json
import requests

@click.command()
@click.option('--output', default=None, help='Output file')
def cli(output):
    r = requests.get("http://xkcd.com/info.0.json")
    data = json.loads(r.text)
    if (output == None):
        file = open(str(data['num']) + ".png", 'wb')
    else:
        file = open(str(output), 'wb')
    res = requests.get(data["img"])
    file.write(res.content)