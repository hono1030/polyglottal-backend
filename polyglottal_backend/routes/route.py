from fastapi import APIRouter, HTTPException
from polyglottal_backend.models.messages import Message
from polyglottal_backend.config.database import collection_name
from polyglottal_backend.schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

async def post_message(message: Message):
    try:
        response = collection_name.insert_one(dict(message))
        print("Inserted message with ID:", response.inserted_id)
        return response
    except Exception as e:
        print("Error inserting message:", e)
        raise e
    
# GET Request Method
@router.get("/database")
async def get_messages():
    messages = list_serial(collection_name.find())
    return messages

@router.put("/database/{id}")
async def put_message(id: str, message: Message):
    try : 
        id = ObjectId(id)
        existing_doc = collection_name.find_one({"_id": id, "is_deleted": False})
        if not existing_doc:
            return HTTPException(status_code=404, detail=f"Message does not exists")
        
        response = collection_name.find_one_and_update({"_id":id}, {'$set': dict(message)})
        return {"status_code": 200, "message": "Message Updaed Successfully"}
    
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")

@router.delete("/database")
async def delete_message():
    try:
        collection_name.delete_many({})
        return {"status_code": 200, "message": "Messages Deleted Successfully"}
    
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")
