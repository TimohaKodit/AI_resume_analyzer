from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.resume_router import router
from api.auth_router import auth_router


app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(auth_router)



@app.get("/")
def root():
    return {"status": "ok"}
