from fastapi import Depends, FastAPI
from . import modules
from . database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# print(settings.database_password)
# print(settings.database_username)
# print(settings.secret_key)


# modules.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com1", "https://www.example.com1"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
    

@app.get("/")
def root():
    return {"message": "Welcome to my API"}












    



