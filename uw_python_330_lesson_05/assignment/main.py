import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_simile():
    """
    Gets a simle from a random simile generator
    """
    response = requests.get("https://random-simile-generator.herokuapp.com/")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")
    # remove quotes from simile
    simile = facts[0].getText().strip()
    simile = simile[1:-1]
    return simile

def parse_pig_latin_html(html):
    """
    Parses pig latin html returned from pig_latinize_text
    """
    soup = BeautifulSoup(html, "html.parser")
    body_text = soup.find("body").text.strip()
    # last part of body text should always be the actual text
    text = body_text.split("\n")[-1].strip()
    return text

def pig_latinize_text(text):
    """
    Translates a piece of text into pig latin
    """
    PIG_LATINIZER = "https://pig-latinizer.herokuapp.com/piglatinize/"
    payload = {"input_text": text}
    pig_latin_html = requests.post(PIG_LATINIZER, data=payload).content
    pig_latin_text = parse_pig_latin_html(pig_latin_html)
    return pig_latin_text

def pig_latin_html(simile, pig_latin):
    """
    Returns html with a wrapping <body> tag
    """
    html = """
    <body>
    <h1>Pig Latinizer</h1>
    <h2>Simile</h2>
    <p>{}</p>
    <h2>Pig Latin</h2>
    <p>{}</p>
    </body>
    """.format(simile, pig_latin)
    return html

def header_html():
    """
    Returns an HTML header
    """
    html = """
    <head>
    <title>Pig Latin</title>
    </head>
    """
    return html

@app.route('/')
def home():
    """
    Returns html with a simile converted to pig latin
    """
    headers = header_html()
    simile = get_simile()
    pig_latin = pig_latinize_text(simile)
    body = pig_latin_html(simile, pig_latin)
    html = f"<html>{headers}\n{body}</html>"
    return html


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    print(get_simile())
    app.run(host='0.0.0.0', port=port)
