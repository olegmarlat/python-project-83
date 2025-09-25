from bs4 import BeautifulSoup


def parse_page(response):
    status_code = response.status_code
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text
    description = soup.find("meta", {"name": "description"}).get("content")
    header = soup.find("h1").text
    return status_code, header, title, description
