from fastapi import APIRouter, UploadFile, HTTPException, Depends
from services.resume_service import analyze_resume
from services.resume_parser import parse_resume
from services.vacansy_parser import parse_vacansy
import os
import tempfile
from services.habr_client import fetch_habr_vac
from dependencies import get_current_user
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db
from chains.compare_chain import chain_comp
router = APIRouter()



@router.post('/resume/analyze')
async def analyze_res(current_user: User = Depends(get_current_user)):
    if not current_user.resume_text:
        raise HTTPException(status_code=400, detail="Сначала загрузите резюме")
    else:
        
        result = await analyze_resume(current_user.resume_text)
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
    

@router.post("/resume/upload")
async def get_resume(file: UploadFile, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if file.content_type not in ['application/pdf']:
        raise HTTPException(status_code=400, detail="Можно отправлять только PDF файлы")
    else:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name
        try:    
            result = parse_resume(temp_path)
            current_user.resume_text = result
            await db.commit()
        finally:
            os.remove(temp_path)
        return "Резюме успешно сохранено"
    
@router.post("/compare")
async def compare(vacansy_url: str, current_user: User = Depends(get_current_user)):
    vacansy_text = await parse_vacansy(vacansy_url)
    
    return await chain_comp.ainvoke({"resume": current_user.resume_text, "vacancy": vacansy_text})
