from flask import Flask, request, render_template, redirect, url_for
from model import personality_scores

app = Flask("personality")


def link_to_id(spotify_link):
    spotify_link = spotify_link.split("?")[0]
    spotify_link = spotify_link.replace("https://open.spotify.com/playlist/", "")
    return spotify_link


@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        spotify_link = request.form["playlist"]
        return redirect(url_for("personality_page", spotify_link=spotify_link))
    else:
        return render_template("home.html")


@app.route("/notfound", methods=["GET", "POST"])
def not_found_page():
    if request.method == "POST":
        spotify_link = request.form["playlist"]
        return redirect(url_for("personality_page", spotify_link=spotify_link))
    else:
        return render_template("home_not_found.html")


@app.route("/personality_description")
def personality_page():
    spotify_link = request.args.get("spotify_link")  # Retrieve the parameter from the query string

    if spotify_link is None:
        # print(spotify_link)
        return redirect(url_for("not_found_page"))
    else:
        playlist_id = link_to_id(spotify_link)
        scores = personality_scores.big_5_scores(playlist_id)
        if scores is None:
            return redirect(url_for("not_found_page"))
        else:
            description = personality_scores.persinality_description(scores)
            return render_template("personality_scores.html", scores=scores, description=description)


if __name__ == '__main__':
    app.run(debug=True)
