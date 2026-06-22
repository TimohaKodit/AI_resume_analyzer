from fastapi import APIRouter, UploadFile, HTTPException
from services.resume_service import analyze_resume
import os
import tempfile
from services.habr_client import fetch_habr_vac



router = APIRouter()


@router.post('/analyze')
async def analyze_res(file: UploadFile):
    if file.content_type not in ['application/pdf']:
        raise HTTPException(status_code=400, detail="Можно отправлять только PDF файлы")
    else:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        try:
            result = analyze_resume(temp_path)
        finally:
            os.remove(temp_path)

        return result
    

@router.get('/vacancies')
async def get_vacans(query: str):
    try:
        vacancies = await fetch_habr_vac(query)
        if not vacancies:
            raise HTTPException(status_code=400, detail="Неп существует таких вакансий")
        else:
            return vacancies
    except:
        return "Ошибка"