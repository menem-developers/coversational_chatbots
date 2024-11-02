from app.db.session import *
from app.schemas.ai_chatbot import *
from app.models.ai_chatbot import *
import time
import hashlib
import time
import random
import string

def generate(sender_user_id, receiver_user_id):
    current_time = int(time.time() * 1000)
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    unique_string = f"{min(sender_user_id, receiver_user_id)}-{max(sender_user_id, receiver_user_id)}-{current_time}-{suffix}"
    unique_id = hashlib.md5(unique_string.encode()).hexdigest()
    return unique_id

def generate_messageid():
    current_time = int(time.time() * 1000)
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    message_id = f"{current_time}-{suffix}"
    return message_id

async def store_message(Messages:Chat):
    if Messages.chat_id is None:
        db_person_one= None
        db_person_two= None
        db_page_one= None
        db_page_two= None
        db_page_a= None
        db_person_a= None
        if Messages.person_one_id and Messages.person_two_id:
            db_person_one = await MessageRecords.find_one(MessageRecords.person_one_id==Messages.person_one_id,MessageRecords.person_two_id==Messages.person_two_id)
            db_person_two = await MessageRecords.find_one(MessageRecords.person_one_id==Messages.person_two_id,MessageRecords.person_two_id==Messages.person_one_id)
        if Messages.page_one_id and Messages.page_two_id:
            db_page_one = await MessageRecords.find_one(MessageRecords.page_one_id==Messages.page_one_id,MessageRecords.page_two_id==Messages.page_two_id)
            db_page_two = await MessageRecords.find_one(MessageRecords.page_one_id==Messages.page_two_id,MessageRecords.page_two_id==Messages.page_one_id)
        if Messages.page_id and Messages.person_id:    
            db_page_a = await MessageRecords.find_one(MessageRecords.person_id==Messages.person_id,MessageRecords.page_id==Messages.page_id)
            db_person_a = await MessageRecords.find_one(MessageRecords.person_id==Messages.page_id,MessageRecords.page_id==Messages.person_id)
        if db_person_one is None and db_person_two is None and db_page_one is None and db_page_two is None and db_page_a is None and db_person_a is None:
            if Messages.person_one_id is not None and Messages.person_two_id is not None:
                Messages.chat_id=generate(Messages.person_one_id,Messages.person_two_id)
            if Messages.page_one_id and Messages.page_two_id:
                Messages.chat_id=generate(Messages.page_one_id,Messages.page_two_id) 
            if Messages.page_id and Messages.person_id:
                Messages.chat_id=generate(Messages.page_id,Messages.person_id)     
            db_message = await MessageRecords.find_one(MessageRecords.chat_id==Messages.chat_id)
            if db_message is None:
                new_messages = {}
                for old_message_id, allmessage in Messages.messages.items():
                    allmessage.timestamp = int(time.time() * 1000)
                    new_message_id = generate_messageid()
                    allmessage.message_id = new_message_id
                    new_messages[new_message_id] = allmessage
                    old_message_id = new_message_id 
                Messages.messages = new_messages
                task = MessageRecords(**Messages.dict())
                await task.insert()
                return task
            else:
                return None
        else:
            return None        
    else:
        new_messages = {}
        for old_message_id, allmessage in Messages.messages.items():
            allmessage.timestamp = int(time.time() * 1000)
            new_message_id = generate_messageid()
            allmessage.message_id = new_message_id
            new_messages[new_message_id] = allmessage
        Messages.messages = new_messages
        task = MessageRecords(**Messages.dict())
        db_message = await MessageRecords.find_one(MessageRecords.chat_id == Messages.chat_id)
        db_message.messages.update(task.messages)
        await db_message.save()
        db_message = await MessageRecords.find_one(MessageRecords.chat_id == Messages.chat_id)
    return db_message


async def change_status(Messages: Messagestatus):
    db_message = await MessageRecords.find_one(MessageRecords.chat_id == Messages.chat_id)
    
    if db_message:
        updated_messages = {
            key: {**message.dict(), 'read_receipts': Messages.read_receipts}
            for key, message in db_message.messages.items()
            if message.read_receipts is None
        }
        if updated_messages:
            await db_message.update({"$set": {"messages": updated_messages}})
    
    return Messages

async def delete_chat(Messages: deletemessage):
    db_message = await MessageRecords.find_one(MessageRecords.chat_id == Messages.chat_id)

    if db_message:
        updated_messages = {
            key: {**message.dict(), 'deleted_by_user': message.deleted_by_user or [] + Messages.deleted_by_user or []}
            for key, message in db_message.messages.items()
        }
        try:
            if updated_messages:
                await db_message.update({"$set": {"messages": updated_messages}}) 
            if any(len(message.deleted_by_user) >= 2 for message in db_message.messages.values()):
                db_message = await MessageRecords.find_one(MessageRecords.chat_id == Messages.chat_id).delete_one()
        except Exception as e:
            if updated_messages:
                await db_message.update({"$set": {"messages": updated_messages}})

    return Messages


# async def message_get(chat_id: str, page: int = 1, size: int = 10):
#     page = max(page, 1)
#     skip = (page - 1) * size
#     db_message = await MessageRecords.find_one(MessageRecords.chat_id == chat_id)
#     if db_message and db_message.messages:
#         sorted_messages = sorted(db_message.messages.values(), key=lambda msg: msg.timestamp, reverse=True)
#         paginated_messages = sorted_messages[skip:skip + size]
#         has_more = len(sorted_messages) > skip + size

#         return {
#             "messages": paginated_messages,
#             "page": page,
#             "has_more": has_more,
#         }
#     return {"messages": [], "page": page, "has_more": False}


async def message_get(chat_id: str, user_id: int, page: int, size:int):
    try:
        page = max(page, 1)
        skip = (page - 1) * size
        
        # Fetch the message record by chat_id
        db_message = await MessageRecords.find_one(MessageRecords.chat_id == chat_id)
        
        if db_message and db_message.messages:
            # Sort messages by timestamp in reverse order (newest first)
            sorted_messages = sorted(db_message.messages.values(), key=lambda msg: msg.timestamp, reverse=True)
            
            # Filter out messages where the user_id is in the deleted_by_user list
            filtered_messages = [
    msg for msg in sorted_messages 
    if not any(deleted.user_id == user_id for deleted in (msg.deleted_by_user or []))
]



            
            # Apply pagination
            paginated_messages = filtered_messages[skip:skip + size]
            has_more = len(filtered_messages) > skip + size

            return {
                "messages": paginated_messages,
                "page": page,
                "has_more": has_more,
            }
        
        # Return empty if no messages are found
        return {"messages": [], "page": page, "has_more": False}

    except Exception as e:
        # Log the error and return a default response
        print(f"An error occurred: {e}")
        return {"messages": [], "page": page, "has_more": False}



async def delete_message_by_id(Messages: Messagestatus):
    db_message = await MessageRecords.find_one(MessageRecords.chat_id == Messages.chat_id)
    if db_message:
        if Messages.message_id in db_message.messages:
            await db_message.update({"$unset": {f"messages.{Messages.message_id}": 1}})
    return Messages

async def delete_chat_by_id(chat_id: str):
    try:
        db_message = await MessageRecords.find_one(MessageRecords.chat_id == chat_id).delete_one()
        return chat_id
    except:
        return None
    
async def message_settings(settingsdata:UserprofileSchema):
    try:
        db_settingsdata= None
        if settingsdata.page_id:
            db_settingsdata = await Userprofile.find_one(Userprofile.page_id == settingsdata.page_id)
        if  settingsdata.person_id:
            db_settingsdata = await Userprofile.find_one(Userprofile.person_id == settingsdata.person_id) 
        if db_settingsdata:
            await db_settingsdata.update({"$set": {"visibility": settingsdata.visibility}})
        else:    
            setting = Userprofile(**settingsdata.dict())
            await setting.insert()
        return settingsdata   
    except:
        return None     
    
async def restrict_message(restrictdata:restrictprofileSchema):
    try:
        db_person_one= None
        db_person_two= None
        db_page_one= None
        db_page_two= None
        db_page_a= None
        db_person_a= None
        if restrictdata.person_one_id and restrictdata.person_two_id:
            db_person_one = await Restrictprofile.find_one(Restrictprofile.person_one_id==restrictdata.person_one_id,Restrictprofile.person_two_id==restrictdata.person_two_id)
            db_person_two = await Restrictprofile.find_one(Restrictprofile.person_one_id==restrictdata.person_two_id,Restrictprofile.person_two_id==restrictdata.person_one_id)
        if restrictdata.page_one_id and restrictdata.page_two_id:
            db_page_one = await Restrictprofile.find_one(Restrictprofile.page_one_id==restrictdata.page_one_id,Restrictprofile.page_two_id==restrictdata.page_two_id)
            db_page_two = await Restrictprofile.find_one(Restrictprofile.page_one_id==restrictdata.page_two_id,Restrictprofile.page_two_id==restrictdata.page_one_id)
        if restrictdata.page_id and restrictdata.person_id:    
            db_page_a = await Restrictprofile.find_one(Restrictprofile.person_id==restrictdata.person_id,Restrictprofile.page_id==restrictdata.page_id)
            db_person_a = await Restrictprofile.find_one(Restrictprofile.person_id==restrictdata.page_id,Restrictprofile.page_id==restrictdata.person_id)

        if db_person_one:
            await db_person_one.update({"$set": {"report": restrictdata.report,"reprt_statement": restrictdata.reprt_statement,"block":restrictdata.block}})
            return restrictdata
        if db_person_two:
            await db_person_two.update({"$set": {"report": restrictdata.report,"reprt_statement": restrictdata.reprt_statement,"block":restrictdata.block}})
            return restrictdata
        if db_page_one:
            await db_page_one.update({"$set": {"report": restrictdata.report,"reprt_statement": restrictdata.reprt_statement,"block":restrictdata.block}})
            return restrictdata
        if db_page_two:
            await db_page_two.update({"$set": {"report": restrictdata.report,"reprt_statement": restrictdata.reprt_statement,"block":restrictdata.block}})
            return restrictdata
        if db_page_a:
            await db_page_a.update({"$set": {"report": restrictdata.report,"reprt_statement": restrictdata.reprt_statement,"block":restrictdata.block}})
            return restrictdata
        if db_person_a:
            await db_person_a.update({"$set": {"report": restrictdata.report,"reprt_statement": restrictdata.reprt_statement,"block":restrictdata.block}})
            return restrictdata                   
        else:
            setting = Restrictprofile(**restrictdata.dict())
            await setting.insert()
        return restrictdata 
    except:
        return None         

