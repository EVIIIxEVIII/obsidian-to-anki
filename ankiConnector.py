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

def cardExists(front_text):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'"Front:{front_text}"'
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    if response.status_code == 200:
        result = response.json()
        if result.get("error") is None:
            note_ids = result["result"]
            if note_ids:
                return note_ids[0]
            else:
                return False
        else:
            print(f"Error: {result['error']}")
    else:
        print(f"HTTP Error: {response.status_code}")

    return False

def updateCard(deck, front, back, id):
    update_fields_payload = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": id,
                "fields": {
                    "Front": front,
                    "Back": back
                }
            }
        }
    }

    response_fields = requests.post(ANKI_CONNECT_URL, json=update_fields_payload)
    if response_fields.status_code == 200:
        result = response_fields.json()
        if result.get("error") is None:
            print("Fields updated successfully!")
        else:
            print(f"Error updating fields: {result['error']}")
    else:
        print(f"HTTP Error when updating fields: {response_fields.status_code}")

    change_deck_payload = {
        "action": "changeDeck",
        "version": 6,
        "params": {
            "cards": [id],
            "deck": deck
        }
    }

    response_deck = requests.post(ANKI_CONNECT_URL, json=change_deck_payload)

    if response_deck.status_code == 200:
        result = response_deck.json()
        if result.get("error") is None:
            print("Deck updated successfully!")
        else:
            print(f"Error updating deck: {result['error']}")
    else:
        print(f"HTTP Error when updating deck: {response_deck.status_code}")

def createCard(deckName, fileName, html_content):
    note = {
        "deckName": deckName,
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

def import_card(deckName, fileName, html_content):
    fullDeckName = deckName.split("/")
    fullDeckName = "::".join(fullDeckName)

    if not deckExists(fullDeckName):
        createDeck(fullDeckName)

    cardId = cardExists(fileName)
    if cardId is None:
        createCard(fullDeckName, fileName, html_content)
    else:
        updateCard(fullDeckName, fileName, html_content, cardId)
