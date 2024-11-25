import os
import requests
from bs4 import BeautifulSoup
import time

base_url = "https://www.gutenberg.org/ebooks/search/"

params = {"query": "classic", "submit_search": "Go!"}

os.makedirs("texts/english", exist_ok=True)


def download_book(text_url, book_title):
    try:
        response = requests.get(text_url)
        response.raise_for_status()
        content = response.text.strip()
        if content:

            with open(f"texts/english/{book_title}.txt", "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Downloaded: {book_title}")
        else:
            print(f"Skipped empty file: {book_title}")
    except Exception as e:
        print(f"Failed to download {book_title}: {e}")


def get_plain_text_link(book_page_url):
    response = requests.get(book_page_url)
    soup = BeautifulSoup(response.content, "html.parser")

    text_link = None
    for link in soup.find_all("a", href=True):
        if "Plain Text UTF-8" in link.text:
            text_link = link["href"]
            break

    if text_link:
        if text_link.startswith("/"):
            text_link = "https://www.gutenberg.org" + text_link
        return text_link
    return None


def is_english_book(book_page_url):
    response = requests.get(book_page_url)
    soup = BeautifulSoup(response.content, "html.parser")

    language_tag = soup.find("tr", property="dcterms:language")
    if language_tag:
        language_content = language_tag.get("content")
        if language_content and language_content.startswith("en"):
            return True
    return False


def process_search_page(page_number):
    params["start_index"] = (page_number - 1) * 25
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    book_items = soup.find_all("li", class_="booklink")
    for book_item in book_items:
        book_link = book_item.find("a")["href"]
        book_title = (
            book_item.find("span", class_="title").text.strip().replace("/", "_")
        )

        book_page_url = "https://www.gutenberg.org" + book_link

        if is_english_book(book_page_url):
            text_url = get_plain_text_link(book_page_url)
            if text_url:
                download_book(text_url, book_title)
            else:
                print(f"Skipped (no plain text found): {book_title}")
        else:
            print(f"Skipped (not English): {book_title}")

        time.sleep(1)


def scrape_and_download_books():
    for page_number in range(1, 26):
        print(f"Processing page {page_number}...")
        process_search_page(page_number)
        time.sleep(2)


scrape_and_download_books()
