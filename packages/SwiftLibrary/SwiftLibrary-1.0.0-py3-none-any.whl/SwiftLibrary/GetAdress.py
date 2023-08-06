import aiohttp
import asyncio
from json import loads


class server_bot:
    list_servers = []

    for server_rubika in range(2):
        
        async def GETservers(server):
            
            async with aiohttp.ClientSession() as session:
                
                async with session.get(server) as response:
                    
                    Post =  await response.text()
                    
                    return Post
        loop = asyncio.get_event_loop()
        servers =  loads(loop.run_until_complete(GETservers("https://getdcmess.iranlms.ir/"))).get('data').get('API')
        
        for key,val in servers.items():
            list_servers.append(str(val))