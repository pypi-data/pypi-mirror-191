import aiohttp
from SwiftRubika.Configs import encryptio
import json
from json import dumps, loads

async def http(ssion,auth,jsons):
	enc = encryptio(auth)
	
	async with aiohttp.ClientSession() as session:
		async with session.post(ssion, data = dumps({"api_version":"5","auth": auth,"data_enc":enc.encrypt(dumps(jsons))}) , headers = {'Content-Type': 'application/json'}) as response:
			response =  await response.text()
			return response

async def httpfiles(session,data,head):
	async with aiohttp.ClientSession() as session:
		async with session.post(session, data = data  , headers = head) as response:
			response =  await response.text()
			return response