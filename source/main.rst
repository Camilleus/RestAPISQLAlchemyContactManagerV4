Main
====

.. module:: main
   :platform: Unix, Windows
   :synopsis: Main module of the application.

.. code-block:: python

   from fastapi import FastAPI
   from fastapi.staticfiles import StaticFiles
   from db.dbs import init_db
   from api.routes import router
   from fastapi.middleware.cors import CORSMiddleware

   app = FastAPI()

   # Add middleware for CORS requests
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "DELETE"],
       allow_headers=["*"],
   )

   # Include router defined in routes.py
   app.include_router(router)

   # Serve 'static' folder as static resource
   app.mount("/static", StaticFiles(directory="static"), name="static")

   # Initialize the database
   init_db()

   # Imports functions from api.apis and classes from schemas.py
   from api.apis import (Contact, create_contact, get_all_contacts, get_contact,
                         update_contact, delete_contact, get_birthdays_within_7_days)
   from schemas import ContactCreateUpdate, ContactResponse

   @app.get("/")
   def read_root():
       """
       Root endpoint, returns a welcome message.
       """
       return {"message": "Hello, world!"}
