import json
import requests
from aiohttp import web
from models import Base, engine
from models import Session, Message
from sqlalchemy.exc import IntegrityError


app = web.Application()


async def context(app):
    print ("Start app")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print ("Shut down app")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(context)
app.middlewares.append(session_middleware)


async def get_http_error(error_class, msg):

    return error_class(
            text=json.dumps({"detail": msg}),
            content_type="application/json"
            )
 

async def get_user(session: Session, user_id: int):

    message = await session.get(Message, user_id)
    if message is None:
        raise get_http_error(web.HTTPNotFound, "not found")
    return message


async def add_user(session: Session, message: Message):
    try:
        session.add(message)
        await session.commit()
    except IntegrityError:
        raise web.HTTPConflict(text=json.dumps({"error": "message already exists"}),
                               content_type="application/json")
    return message


class MessageView(web.View):


    @property
    def session(self) -> Session:
        return self.request.session
    
    @property
    def message_id(self):
        return int(self.request.match_info["message_id"])


    async def post(self):
        json_data = await self.request.json()
        message = Message(**json_data)
        message = await add_user(self.session, message)
        return web.json_response({"id": message.id})
    
    
    async def get (self):
        message = await get_user(self.session, self.message_id)
        return web.json_response({
            "id": message.id,
            "title": message.title,
            "text": message.text,
            "name": message.name,
            "created_at": int(message.created_at.timestamp()),
        })


    async def patch(self):
        messege = await get_user(self.session, self.message_id)
        json_data = await self.request.json()
        for field, value in json_data.items():
            setattr(messege, field, value)
        await add_user(self.session, messege)
        return web.json_response({"id": messege.id})
    

    async def delete(self):
        messege = await get_user(self.session, self.message_id)
        await self.session.delete(messege)
        await self.session.commit()
        return web.json_response({"status": "deleted"})

        
app.add_routes(
    [
        web.post("/messages/", MessageView),
        web.get("/messages/{message_id:\d+}", MessageView),
        web.patch("/messages/{message_id:\d+}", MessageView),
        web.delete("/messages/{message_id:\d+}", MessageView),
    ]
)

web.run_app(app)