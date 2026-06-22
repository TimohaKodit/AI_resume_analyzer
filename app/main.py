from fastapi import FastAPI
from api.resume_router import router
from api.auth_router import auth_router


app = FastAPI(title="AI Resume Analyzer")

app.include_router(router)
app.include_router(auth_router)



@app.get("/")
def root():
    return {"status": "ok"}
