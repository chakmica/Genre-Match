function getGenres(genres_image_json_string) {
  genres_image_json = JSON.parse(genres_image_json_string);
  if (genres_image_json != null) {
    const output = document.createElement("div");
    genres = genres_image_json.genres;
    image = genres_image_json.image;
    artist = genres_image_json.artist;
    document.getElementById("artist-title").innerText = artist;
    if (genres.length < 3) {
      let loop = "";
      for (let i = 0; i < genres.length; i++) {
        loop += "<div class='genre'><h2>" + genres[i] + "</h2></div>";
      }
      output.innerHTML = loop;
    } else {
      output.innerHTML =
        "<div class='genre'><h2>" +
        genres[0] +
        "</h2></div><div class='genre'><h2>" +
        genres[1] +
        "</h2></div><div class='genre'><h2>" +
        genres[2] +
        "</h2></div>";
    }
    if (image != null) {
      document.getElementById("artist-picture").src = image;
    }
    const artist_div = document.getElementById("artist-genres");
    artist_div.appendChild(output);
  }
}
