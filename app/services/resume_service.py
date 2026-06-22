from chains.resume_chain import chain
from services.resume_parser import parse_resume


def analyze_resume(file_path: str) -> str:
    prs_resume = parse_resume(file_path)
    try:    
        result = chain.invoke({'resume': prs_resume})

        return result
    except:
        return "Произошла ошибка! Попробуйте позже"
