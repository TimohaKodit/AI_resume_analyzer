import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

class HH_Client():
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.headers = {
            "User-Agent": os.getenv("HH_USER_AGENT")
        }

    async def search_hh(self, text: str, page: int = 0, per_page: int = 8, area_id: str = "113") -> dict:
        """Поиск вакансий для ручного запроса"""
        params = {
            "text": text,
            "area": area_id,                   
            "per_page": per_page,              
            "page": page,                      
            "order_by": "publication_time",    
        }
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                async with session.get(self.BASE_URL, params=params) as resp:
                    print(resp.status)
                    if resp.status != 200:
                        return {"items": [], "pages": 0}
                    data = await resp.json()
                    print(data)
                    items = []
                    for item in data.get('items', []):
                        salary = "Зарплата не указана"
                        if item.get('salary'):
                            s = item['salary']
                            fr, to, cur = s.get('from'), s.get('to'), s.get('currency', 'RUB')
                            if fr and to: salary = f"{fr} - {to} {cur}"
                            elif fr: salary = f"от {fr} {cur}"
                            elif to: salary = f"до {to} {cur}"

                        items.append({
                            'id': str(item['id']),
                            'name': item['name'],
                            'employer_name': item['employer']['name'],
                            'url': item['alternate_url'],
                            'salary_text': salary,
                            'price': salary  # Добавляем этот ключ, чтобы alerts.py точно его увидел
                        })
                    return items
            except Exception as e:
                print(f"Ошибка HH Search: {e}")
                return []
                
