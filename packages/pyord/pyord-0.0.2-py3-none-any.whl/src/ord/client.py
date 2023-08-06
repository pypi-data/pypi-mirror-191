from typing import Generator

import httpx
from bs4 import BeautifulSoup

from src.ord import models


def is_node_healthy() -> bool:
    with httpx.Client() as client:
        url = "https://ordinals.com/status"
        response = client.get(url)
    return response.status_code == 200


def get_block_count() -> int:
    with httpx.Client() as client:
        url = "https://ordinals.com/block-count"
        response = client.get(url)
    return int(response.content.decode("utf-8"))


def get_block(height: int) -> models.Block:
    with httpx.Client() as client:
        url = f"https://ordapi.xyz/block/{height}"
        response = client.get(url)
    return models.Block(**response.json())


def get_content(inscription_id: str) -> bytes:
    url = "https://ordinals.com/content/" + inscription_id
    with httpx.Client() as client:
        response = client.get(url)
    return response.content


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


def inscription_ids(start: int = 0, stop: int | None = None) -> Generator[str, None, None]:
    """
    Iterate over all inscription ids starting from 0. Making 1 http request per 100 inscriptions.

    Args:
        start: inscription index to start at (inclusive)
        stop: inscription index to stop at (exclusive), or None to iterate over all inscriptions

    Returns:
        Generator yielding one inscription id at a time
    """
    i = start
    while True:
        url = f"https://ordinals.com/inscriptions/{start + 99}"
        with httpx.Client() as client:
            response = client.get(url)

        soup = BeautifulSoup(response.content, "html.parser")
        thumbnails = soup.find("div", class_="thumbnails")
        inscription_links = thumbnails.find_all("a")
        ids = [link["href"].split("/")[-1] for link in inscription_links]
        for one_id in reversed(ids):
            yield one_id
            i += 1
            if stop and i >= stop:
                return


def get_tx(tx_id: str) -> models.Tx:
    url = "https://ordapi.xyz/tx/" + tx_id
    with httpx.Client() as client:
        response = client.get(url)
    return models.Tx(**response.json())
