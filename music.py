import subprocess
import urllib.parse

SONGS = {
    "mockingbird": "https://audiomack.com/cassamy/song/mockingbird?share-user-id=219383185",
    "past lives": "https://audiomack.com/jessiexke/song/past-lives?share-user-id=219383185",
    "another love": "https://audiomack.com/hello_world/song/another-love-tiktok-version?share-user-id=219383185",
    "death bed": "https://audiomack.com/aycpp/song/death-bed-normal?share-user-id=219383185",
    "funk universal": "https://audiomack.com/aledavid56/song/funk-universal?share-user-id=219383185",
    "your love is my drug": "https://audiomack.com/cheefreef/song/kesha-your-love-is-my-drug-8bit-slowed?share-user-id=219383185",
    "i love you so": "https://audiomack.com/hussvrx/song/i-love-you-so-jumpstyle-ultra-slowed-6381770",
    "sua amiga": "https://audiomack.com/phellipmuniz/song/sua-amiga-eu-vou-pegar-1?share-user-id=219383185"
}


def open_url(url):
    subprocess.run([
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        url
    ])


def play_song(song):

    song = song.lower().strip()

    if song in SONGS:
        open_url(SONGS[song])
        return f"Playing {song.title()}."

    query = urllib.parse.quote(song)

    open_url(f"https://audiomack.com/search/{query}")

    return f"Searching Audiomack for {song}."
