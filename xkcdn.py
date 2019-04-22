import click
import json
import requests

@click.command()
def xkcdn():
    r = requests.get("http://xkcd.com/info.0.json")
    data = json.loads(r.text)
    file = open(str(data['num']) + ".png", 'wb')
    res = requests.get(data["img"])
    file.write(res.content)

if __name__ == '__main__':
    xkcdn()