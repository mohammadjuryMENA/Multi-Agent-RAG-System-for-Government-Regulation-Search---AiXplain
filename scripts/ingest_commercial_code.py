import requests
from bs4 import BeautifulSoup
import time
from aixplain.factories import IndexFactory
from aixplain.modules.model.record import Record
from dotenv import load_dotenv
load_dotenv()
SECTIONS = ["1101", "2101", "3101", "4101", "5101", "6101", "7101", "8101", "9101", "10101", "11101", "12101", "13101", "14101", "15101", "16101", "17101"]  # Example: update with actual Commercial Code sections as needed
BASE_URL = "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=COM&sectionNum={}"
INDEX_NAME = "Commercial Code Index"
INDEX_DESC = "California Commercial Code sections scraped from the official website."
def fetch_section(section_num):
    url = BASE_URL.format(section_num)
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.find("h3")
    title = title.text.strip() if title else f"Section {section_num}"
    content = soup.find("div", {"class": "section"})
    text = content.text.strip() if content else ""
    return {"section": section_num, "title": title, "text": text}
def main():
    try:
        index = IndexFactory.create(name=INDEX_NAME, description=INDEX_DESC)
    except Exception as e:
        print(f"Index may already exist: {e}")
        from aixplain.factories import IndexFactory as IF
        index = IF.get_by_name(INDEX_NAME)
    for sec in SECTIONS:
        print(f"Fetching section {sec}...")
        entry = fetch_section(sec)
        if entry and entry['text']:
            rec = Record(
                value=entry['text'],
                attributes={"section": entry['section'], "title": entry['title']}
            )
            index.upsert([rec])
        time.sleep(0.5)
    print(f"Upserted all sections to aiXplain index '{INDEX_NAME}'")
if __name__ == "__main__":
    main() 