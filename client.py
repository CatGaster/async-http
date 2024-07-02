import aiohttp

import asyncio

async def main():

    client = aiohttp.ClientSession()

    response = await client.post("http://127.0.0.1:8080/messages/",
        json={"title": "some_title", "name": "netolgy", "text": "bla_bla"})     
    
    data = await response.text()
    print (data)
    print (response.status)


    # response = await client.get("http://127.0.0.1:8080/messages/1")
    # data = await response.text()
    # print(data)


    # response = await client.patch("http://127.0.0.1:8080/messages/1",
    #     json={"title": "some_patched_title","name": "netolgy", "text": "bla_bla_bla"})

    # data = await response.text()
    # print(data)
    # print(response.status)
    # print(response.headers)


    # response = await client.delete("http://127.0.0.1:8080/messages/1")

    # data = await response.text()
    # print(data)
    # print(response.status)

    await client.close()

asyncio.run(main())

