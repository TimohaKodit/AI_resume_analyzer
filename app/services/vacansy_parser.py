import aiohttp
from bs4 import BeautifulSoup


async def parse_vacansy(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html_text = await resp.text()
            soup = BeautifulSoup(html_text, 'html.parser')
            print(html_text[:500])
            return soup.find("div", class_ ="style-ugc").get_text()
    
