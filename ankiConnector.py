import requests

ANKI_CONNECT_URL = "http://127.0.0.1:8765"

def createDeck(deck_name):
    payload = {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    response_data = response.json()

    if response_data.get("error"):
        print(f"Error: {response_data['error']}")
    else:
        print(f"Deck '{deck_name}' created successfully!")

def deckExists(deck_name):
    payload = {
        "action": "deckNames",
        "version": 6
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    response_data = response.json()

    if response_data.get("error"):
        print(f"Error: {response_data['error']}")
        return False

    return deck_name in response_data.get("result", [])

def import_card(deckName, fileName, html_content):
    full_deck_name = deckName.split("/")
    full_deck_name = "::".join(full_deck_name)

    if not deckExists(full_deck_name):
        createDeck(full_deck_name)

    note = {
        "deckName": full_deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": fileName,
            "Back": html_content
        },
        "tags": ["imported"],
    }

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": note
        }
    }

    response = requests.post(ANKI_CONNECT_URL, json=payload)
    response_data = response.json()

    if response_data.get("error"):
        print(f"Error: {response_data['error']}")
    else:
        print(f"Note added successfully with ID: {response_data['result']}")

