import os
import requests
from bs4 import BeautifulSoup

# URL of the top 100 books page on Project Gutenberg
top_100_url = "https://www.gutenberg.org/browse/scores/top"

# Create a folder to store downloaded books
os.makedirs("texts", exist_ok=True)


# Function to download the book as plain text
def download_book(text_url, book_title):
    try:
        response = requests.get(text_url)
        response.raise_for_status()
        # Save the text file
        with open(f"gutenberg_books/{book_title}.txt", "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Downloaded: {book_title}")
    except Exception as e:
        print(f"Failed to download {book_title}: {e}")


# Function to scrape the plain text version link from the book page
def get_plain_text_link(book_page_url):
    response = requests.get(book_page_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the link to the plain text version (usually contains 'Plain Text UTF-8')
    text_link = None
    for link in soup.find_all("a", href=True):
        if "Plain Text UTF-8" in link.text:
            text_link = link["href"]
            break

    if text_link:
        # Ensure the link is absolute
        if text_link.startswith("/"):
            text_link = "https://www.gutenberg.org" + text_link
        return text_link
    return None


# Function to scrape top 100 books and download plain text versions
def scrape_and_download_books():
    response = requests.get(top_100_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the links to the book pages from the top 100 list (under <ol>)
    book_list = soup.find("ol")
    for book_item in book_list.find_all("li"):
        book_link = book_item.find("a")["href"]
        book_title = (
            book_item.find("a").text.strip().replace("/", "_")
        )  # Avoid invalid characters

        # Full link to the book page
        book_page_url = "https://www.gutenberg.org" + book_link

        # Get the plain text download link
        text_url = get_plain_text_link(book_page_url)
        if text_url:
            # Download the book
            download_book(text_url, book_title)


# Run the scraper and download books
scrape_and_download_books()
