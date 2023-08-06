import httpx

from src.ord import models


def get_block(height: int) -> models.Block:
    with httpx.Client() as client:
        url = f"https://ordapi.xyz/block/{height}"
        response = client.get(url)
        return models.Block(**response.json())


def get_content(inscription_id: str) -> str:
    url = "https://ordinals.com/content/" + inscription_id
    with httpx.Client() as client:
        response = client.get(url)
    return response.content.decode("utf-8")


def get_preview(inscription_id: str) -> str:
    url = "https://ordinals.com/preview/" + inscription_id
    with httpx.Client() as client:
        response = client.get(url)
    return response.content.decode("utf-8")


def get_sat(sat: str) -> models.Sat:
    url = "https://ordapi.xyz/sat/" + sat
    with httpx.Client() as client:
        response = client.get(url)
    return models.Sat(**response.json())


def get_inscription(inscription_id: str) -> models.Inscription:
    url = "https://ordapi.xyz/inscription/" + inscription_id
    with httpx.Client() as client:
        response = client.get(url)
    return models.Inscription(**response.json())


def get_tx(tx_id: str) -> models.Tx:
    url = "https://ordapi.xyz/tx/" + tx_id
    with httpx.Client() as client:
        response = client.get(url)
    return models.Tx(**response.json())
