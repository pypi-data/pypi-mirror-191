import asyncio
import websockets as wss
import json
from uuid import uuid4

oi = set()
ip = "0.0.0.0"
mode = "0"

def start():
  global ip
  global mode
  print("Project By Jvsm Games :)")
  ip = input("IP: ")
  mode = input("Mode[Server(0)/Client(1)]: ")
  if mode == "0":
    asyncio.run(main())
  if mode == "1":
    asyncio.run(client())
  



async def send(cmd):
  '''Send a command "cmd" to MineCraft'''
  msg = {
    "header": {
      "version": 1,
      "requestId": f'{uuid4()}',        # A unique ID for the request
      "messagePurpose": "commandRequest",
      "messageType": "commandRequest"
      },
      "body": {
        "version": 1,
        "commandLine": cmd,               # Define the command
        "origin": {
          "type": "player"              # Message comes from player
        }
      }
    }
  await wss.broadcast(oi,json.dumps(msg))     # Send the JSON string



async def echo(ws):
  print("conectado!")
  oi.add(ws)
  await ws.send(str(ws))
  try:
    async for msg in ws:
      print("foi o print:")
      print(msg)
      if "/" in msg:
        print("foi a chamada:")
        await send(msg)
        print("não sei quem foi:")
  except:
    print("desconectado!")
    
    

async def main():
  async with wss.serve(echo, ip ,13777):
      print("\n/connect " + ip + ":13777\n\n")
      await asyncio.Future()
      
async def client():
  async with wss.connect("ws://" + ip + ":13777") as ws:
    p = input("Seu commando(comece com / porfavor): ")
    await ws.send(p)
    r = await ws.recv()
    print(r)