from chains.resume_chain import chain
from services.resume_parser import parse_resume


async def analyze_resume(text: str) -> str:
    try:    
        result = await chain.ainvoke({'resume': text})
        return result
    except Exception as e:
        #  return "Произошла ошибка! Попробуйте позже"
        return e
        