import json
import os

BASE_DIR = os.path.dirname(__file__)
CATALOG_FILE = os.path.join(BASE_DIR, "catalog.json")


def load_catalog():
    if not os.path.exists(CATALOG_FILE):
        return {"anime": []}

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_catalog(data):
    temp = CATALOG_FILE + ".tmp"

    with open(temp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    os.replace(temp, CATALOG_FILE)


def get_anime_list():
    return load_catalog()["anime"]


def get_anime(anime_id):
    data = load_catalog()

    for anime in data["anime"]:
        if anime["id"] == anime_id:
            return anime

    return None


def get_episodes(anime_id):
    anime = get_anime(anime_id)

    if anime is None:
        return None

    episodes = []

    for season in anime.get("seasons", []):
        for episode in season.get("episodes", []):
            item = dict(episode)
            item["season"] = season["number"]
            item["seasonTitle"] = season["title"]
            episodes.append(item)

    return episodes


def add_episode(
    anime_id,
    number,
    title,
    video_url,
    season=1,
    season_title="Season 1",
    subtitle_url="",
    audio_language=""
):
    data = load_catalog()

    anime = None

    for item in data["anime"]:
        if item["id"] == anime_id:
            anime = item
            break

    if anime is None:
        return None

    seasons = anime.setdefault("seasons", [])

    target = None

    for current in seasons:
        if current["number"] == season:
            target = current
            break

    if target is None:
        target = {
            "number": season,
            "title": season_title,
            "episodes": []
        }
        seasons.append(target)

    episode = {
        "number": int(number),
        "title": title or f"Episode {number}",
        "videoUrl": video_url or "",
        "subtitleUrl": subtitle_url or "",
        "audioLanguage": audio_language or ""
    }

    replaced = False

    for index, existing in enumerate(target["episodes"]):
        if existing.get("number") == int(number):
            target["episodes"][index] = episode
            replaced = True
            break

    if not replaced:
        target["episodes"].append(episode)

    target["episodes"].sort(
        key=lambda x: x.get("number", 0)
    )

    save_catalog(data)

    return episode
