from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from webdriver_manager.chrome import ChromeDriverManager;
from selenium.webdriver.chrome.options import Options;
from flask import Flask, render_template, request, redirect, url_for, session;
from PIL import Image;
import os;
import json;
import requests;

app = Flask(__name__, template_folder="Template")

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/search/<artist>")
def search(artist):
    genres_image_json = session.get("genres_image_json", None)
    return render_template("search.html", artist=artist, genres_image_json=genres_image_json)
@app.route("/automation", methods = ["POST", "GET"])
def run_automation():
    if request.method == "POST":
        artist = request.form.get("artist")
        genres_image_json = find(artist)
        session["genres_image_json"] = genres_image_json
        return redirect(url_for("search", artist=artist))

def find(band: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get("https://www.wikipedia.org/")
    searchInput = WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.ID, "searchInput")))
    searchInput.send_keys(band)
    searchInput.submit()

    try:
        infoboxLabels = WebDriverWait(driver, timeout=5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "infobox-label")))
        genreRow = None
        genresLinks = None
        genres = []
        genresOutput = []
        for label in infoboxLabels:
            if label.get_attribute("innerText") == "Genres":
                genreRow = label.find_element(By.XPATH, ".//ancestor::tr")
                genresData = genreRow.find_element(By.CLASS_NAME, "infobox-data")
                genresLinks = genresData.find_elements(By.TAG_NAME, "a")
        if genresLinks:
            for genreLink in genresLinks:
                try:
                    genreLink.find_element(By.XPATH, ".//ancestor::sup")
                except:
                    genres.append(genreLink.get_attribute("innerText"))
        for genre in genres:
            output = ""
            genreWords = genre.split()
            for i in range(len(genreWords)):
                if i == 0:
                    output += genreWords[i].capitalize()
                else:
                    output += " " + genreWords[i].capitalize()
            genresOutput.append(output)

        if not genresOutput:
            genres = None
        else:
            output = genresOutput[0]
            for genre in genresOutput[1::1]:
                output += ", " + genre
            #get image if available
            imageLink = None
            try:
                imageContainer = driver.find_element(By.CLASS_NAME, "image")
                image = imageContainer.find_element(By.XPATH, ".//img")
                imageLink = image.get_attribute("src")
            except Exception as e:
                #print("inner block: " + repr(e))
                imageLink = None
            genres_image_dict = {}
            genres_image_dict["artist"] = band
            genres_image_dict["genres"] = genresOutput
            genres_image_dict["image"] = imageLink
            genres_image_json = json.dumps(genres_image_dict)
            #print(genres_image_json)
            driver.quit()
            return genres_image_json
    except Exception as e:
        #print("outer block: " + repr(e))
        driver.quit()
        genres_image_dict = {}
        genres_image_json = json.dumps(None)
        #print(genres_image_json)
        return genres_image_json

if __name__ == "__main__":
    SECRET = os.urandom(12)
    app.secret_key = SECRET
    app.run(debug=True)