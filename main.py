from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as book_router

app = FastAPI()
config = dotenv_values(".env")
  

@app.on_event("startup")
def startup_db_client():
    try:
        app.mongodb_client = MongoClient(config["URI"])
        app.database = app.mongodb_client[config["DB_NAME"]]
        app.coll = app.database["book"]

        if "book" not in app.database.list_collection_names():
            app.coll.insert_one({"_id": "dummy", "message": "This is a placeholder document."})
            print("'book' collection created with a dummy document.")
            app.coll.delete_one({"_id": "dummy"})  # Remove dummy document

        print("Connected to MongoDB:", app.mongodb_client.list_database_names())
    except Exception as e:
        print("Failed to connect to MongoDB:", str(e))
        raise e


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(book_router, tags=["books"], prefix="/book")
