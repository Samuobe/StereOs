import musicbrainzngs

musicbrainzngs.set_useragent(
    "SonneMusic",      # nome app (perfetto per il tuo progetto 😉)
    "1.0",
    "tuamail@example.com"
)

def cerca_brano(titolo, artista=None, album=None):
    query = titolo
    if artista:
        query += f' AND artist:"{artista}"'
    if album:
        query += f' AND release:"{album}"'

    result = musicbrainzngs.search_recordings(
        query=query,
        limit=1
    )

    if not result["recording-list"]:
        return None

    recording = result["recording-list"][0]

    release = recording["release-list"][0]
    
    return {
        "titolo": recording["title"],
        "artista": recording["artist-credit"][0]["artist"]["name"],
        "album": release["title"],
        "release_id": release["id"]
    }


import requests

def get_cover_url(release_id):
    url = f"https://coverartarchive.org/release/{release_id}"
    r = requests.get(url)

    if r.status_code != 200:
        return None

    data = r.json()

    for img in data["images"]:
        if img.get("front"):
            return img["image"]  # URL immagine

    return None


brano = cerca_brano(
    titolo="White Wolf",
    artista="Roses of Thieves",
    album="Demons Ascend"
)

if brano:
    cover_url = get_cover_url(brano["release_id"])
    
    print("Titolo:", brano["titolo"])
    print("Artista:", brano["artista"])
    print("Album:", brano["album"])
    print("Copertina:", cover_url)
else:
    print("Brano non trovato")
