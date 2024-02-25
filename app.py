from flask import Flask, render_template, request
import urllib.request, json

app = Flask(__name__)

@app.route("/")
def get_list_characters_page():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    url = f"https://rickandmortyapi.com/api/character/?page={page}&per_page={per_page}"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    return render_template("characters.html", characters=dict["results"], page=page, per_page=per_page, has_next_page=dict["info"]["next"] is not None)


@app.route("/profile/<id>")
def get_profile(id):
    url = "https://rickandmortyapi.com/api/character/" + id
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    return render_template("profile.html", profile=dict)

@app.route("/locations")
def get_location():
    url = "https://rickandmortyapi.com/api/location"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    return render_template("locations.html", locations=dict["results"])

@app.route("/episodes")
def get_episodes():
    url = "https://rickandmortyapi.com/api/episode"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    return render_template("episodes.html", episodes=dict["results"])

@app.route("/episode/<id>")
def get_episode_profile(id):
    url = "https://rickandmortyapi.com/api/episode/" + id
    response = urllib.request.urlopen(url)
    data = response.read()
    episode_data = json.loads(data)
    
    characters_data = []
    if "characters" in episode_data:
        for character_url in episode_data["characters"]:
            character_response = urllib.request.urlopen(character_url)
            character_data = json.loads(character_response.read())
            characters_data.append(character_data)

    return render_template("episode.html", episode=episode_data, characters=characters_data)



@app.route("/location/<id>")
def get_location_profile(id):
    url = "https://rickandmortyapi.com/api/location/" + id
    response = urllib.request.urlopen(url)
    data = response.read()
    location_data = json.loads(data)
    
    if "residents" in location_data:
        residents_data = []
        for resident_url in location_data["residents"]:
            resident_response = urllib.request.urlopen(resident_url)
            resident_data = json.loads(resident_response.read())
            residents_data.append(resident_data)
        location_data["residents"] = residents_data

    return render_template("location.html", location=location_data)


@app.route("/lista")
def get_list_characters():
    url = "https://rickandmortyapi.com/api/character/"
    response = urllib.request.urlopen(url)
    characters = response.read()
    dict = json.loads(characters)

    characters = []

    for character in dict["results"]:
        character = {
            "name": character["name"],
            "status": character["status"]
        }

        characters.append(character)

    return {"characters": characters}