from flask import Flask, render_template, request, redirect, jsonify
import json
import string
import random
import threading

app = Flask(__name__)

LINKS_FILE = 'links.json'

def load_links():
    try:
        with open(LINKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_links(links):
    with open(LINKS_FILE, 'w') as file:
        json.dump(links, file)

links = load_links()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-short-link', methods=['POST'])
def generate_short_link():
    data = json.loads(request.data)
    long_link = data['longLink']
    domain = data['domain']

    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(6))

    short_link = code

    links[short_link] = long_link

    save_links(links)

    return jsonify({'shortLink': domain + '/' + short_link})

@app.route('/<string:code>')
def redirect_to_long_link(code):
    if code in links:
        long_link = links[code]
        return redirect(long_link)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run("0.0.0.0")
