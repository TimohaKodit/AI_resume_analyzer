import aiohttp 
import feedparser


async def fetch_habr_vac(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://career.habr.com/vacancies/rss?currency=RUR&sort=relevance&type=all&q={query}") as resp:
            xml_text = await resp.text()


            feed =feedparser.parse(xml_text)
            al = []
            for entry in feed.entries:
                item = {
                    "name": entry.title,
                    "url": entry.link,
                    "id": f"habr_{entry.id.split('/')[-1]}"
                }
                al.append(item)
            return al
                


