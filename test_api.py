"""Test para verificar los endpoints de la API.

Uso: primero levantar el servidor con:
    python api.py

Luego en otra terminal:
    python test_api.py
"""
import requests

BASE = "http://localhost:5000"
IMDB_ID = "tt3107288"  # The Flash (serie)
PERSON_ID = "nm1227814"  # Grant Gustin
LOCALE = "es"


def test_health():
    r = requests.get(f"{BASE}/")
    assert r.status_code == 200
    data = r.json()
    print("[OK] Health check:", data["message"])


def test_search():
    r = requests.get(f"{BASE}/search", params={"q": "The Flash", "locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    titles = data["titles"]
    print(f"[OK] Search: {len(titles)} resultados")
    t = titles[0]
    print(f"     {t['title_localized']} ({t['title']}) - {t['year']}")
    print(f"     Plot: {(t.get('plot') or 'N/A')[:100]}...")
    print(f"     Géneros: {t.get('genres', [])}")


def test_movie():
    r = requests.get(f"{BASE}/movie/{IMDB_ID}", params={"locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    print(f"[OK] Movie: {data['title']} ({data.get('title_localized', '')})")
    print(f"     Plot: {data['plot'][:100]}...")
    print(f"     Rating: {data['rating']} | Géneros: {data['genres']}")


def test_name():
    r = requests.get(f"{BASE}/name/{PERSON_ID}", params={"locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    print(f"[OK] Name: {data['name']}")
    print(f"     Known for: {data.get('knownfor', [])[:3]}")


def test_season_episodes():
    r = requests.get(f"{BASE}/series/{IMDB_ID}/season/1", params={"locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    eps = data["episodes"]
    print(f"[OK] Season 1: {len(eps)} episodios")
    ep = eps[0]
    print(f"     S01E01 - {ep['title']} (Rating: {ep['rating']})")


def test_all_episodes():
    r = requests.get(f"{BASE}/series/{IMDB_ID}/episodes", params={"locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    print(f"[OK] All episodes: {len(data)} episodios total")


def test_akas():
    r = requests.get(f"{BASE}/akas/{IMDB_ID}", params={"locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    print(f"[OK] AKAs: {len(data)} títulos alternativos")


def test_reviews():
    r = requests.get(f"{BASE}/reviews/{IMDB_ID}", params={"locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    print(f"[OK] Reviews: {len(data)} reviews")


def test_trivia():
    r = requests.get(f"{BASE}/trivia/{IMDB_ID}", params={"locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    print(f"[OK] Trivia: {len(data)} items")


def test_filmography():
    r = requests.get(f"{BASE}/filmography/{PERSON_ID}", params={"locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    print(f"[OK] Filmography: {len(data)} categorías")


def test_parental_guide():
    r = requests.get(f"{BASE}/parental-guide/{IMDB_ID}", params={"locale": LOCALE})
    assert r.status_code == 200
    data = r.json()
    print(f"[OK] Parental Guide: {len(data.get('categories', []))} categorías")


if __name__ == "__main__":
    tests = [
        test_health,
        test_search,
        test_movie,
        test_name,
        test_season_episodes,
        test_all_episodes,
        test_akas,
        test_reviews,
        test_trivia,
        test_filmography,
        test_parental_guide,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"[FAIL] {t.__name__}: {e}")
            failed += 1
        print()

    print(f"=== Resultado: {passed} passed, {failed} failed ===")
