from PyPDF2 import PdfReader


def parse_resume(file_path: str) -> str:
    with open(file_path, "rb") as file:
        reader = PdfReader(file)

        resume_text = []
        for pages in reader.pages:
            resume_text.append(pages.extract_text())
        try:
            return '\n'.join(resume_text)
        except: 
            return "Произошла ошибка! Проверьте ваше резюме:" \
            "Только PDF файл" \
            "Файл не поврежден" \
            "Файл не пустой"