from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db.dbs import init_db
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  
    allow_headers=["*"],  
)


app.include_router(router)


app.mount("/static", StaticFiles(directory="static"), name="static")


init_db()


from api.apis import Contact, create_contact, get_all_contacts, get_contact, update_contact, delete_contact, get_birthdays_within_7_days
from schemas import ContactCreateUpdate, ContactResponse


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


