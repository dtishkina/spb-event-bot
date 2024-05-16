import aiohttp
from bs4 import BeautifulSoup
from utils.html_escape import escape_html

async def fetch_new_holland_events():
    URL = "https://www.newhollandsp.ru/events/all-events/"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            page_content = await response.text()

    soup = BeautifulSoup(page_content, "html.parser")
    events = soup.find_all("div", class_="item")

    events_info = []
    for event in events:
        event_url = event.find("a", class_="event")["href"]
        event_url_full = f"https://www.newhollandsp.ru{event_url}" if event_url.startswith('/') else event_url

        img_tag = event.find("img", class_="img-responsive")
        img_url = img_tag["src"] if img_tag else None
        img_url_full = f"https://www.newhollandsp.ru{img_url}" if img_url and img_url.startswith('/') else img_url

        event_name = img_tag["alt"] if img_tag else "Название не указано"
        event_date_tag = event.find("span", class_="event-date")
        event_date = event_date_tag.text.strip() if event_date_tag else "Дата не указана"

        events_info.append({
            "name": event_name,
            "date": event_date,
            "img_url": img_url_full,
            "event_url": event_url_full
        })

    return events_info

async def fetch_sevcableport_events():
    URL = "https://sevcableport.ru/ru/afisha"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            page_content = await response.text()

    soup = BeautifulSoup(page_content, "html.parser")
    cards = soup.find_all("a", class_="ActivityCard_card__3eBST")

    events_info = []
    for card in cards:
        body = card.find("div", class_="ActivityCard_body__2pEAx")
        if not body:
            continue

        event_type = body.find("span", class_="ActivityCard_tag__ZA8YN")
        event_title = body.find("h3", class_="ActivityCard_title__2AUzM")
        event_dates = body.find("span", class_="ActivityCard_decals__3NUGK")
        today_time_elements = body.find_all("span", class_="ActivityCard_date__2S1AS")
        venue = body.find("span", class_="ParentLabel_parent__qC-rf")
        img_tag = card.find("img", class_="ResponsivePicture_image__10h8-")
        event_url = card["href"]
        event_url_full = f"https://sevcableport.ru{event_url}" if event_url.startswith('/') else event_url

        event_info = {
            "type": escape_html(event_type.get_text(strip=True)) if event_type else "Тип не указан",
            "title": escape_html(event_title.get_text(strip=True)) if event_title else "Название не указано",
            "dates": escape_html(event_dates.get_text(strip=True)) if event_dates else "Дата не указана",
            "today_time": escape_html(", ".join([time.get_text(strip=True) for time in today_time_elements])),
            "venue": escape_html(venue.get_text(strip=True)) if venue else "Место проведения не указано",
            "img_url": img_tag["src"] if img_tag else None,
            "event_url": event_url_full
        }
        events_info.append(event_info)

    return events_info
