import asyncio
import websockets as wss
import json
from uuid import uuid4

oi = set()
ip = "0.0.0.0"
mode = "0"
nick = "Steve"
block = "Mamaco"
alerted = False

def start():
  global ip
  global mode
  global nick
  global block
  ip = input("IP: ")
  mode = input("Mode[Server(0)/Client(1)]: ")
  if mode == "0":
    block = input("Deseja Proibir Algum Comando? Liste-os separando-os com vírgula(,): ")
    block = (block + "se divirta, deixe um like")
    asyncio.run(main())
  if mode == "1":
    nick = input("Seu NickName: ")
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
  await ws.send(block)
  try:
    async for msg in ws:
      print(msg)
      if "oi" in msg:
        await ws.send("ola")
      if "/" in msg:
        await send(msg)
  except:
    print("desconectado!")
    
    

async def main():
  async with wss.serve(echo, ip ,13777):
      print("\n/connect " + ip + ":13777\n\n")
      await asyncio.Future()
      
async def client():
  global alerted
  global block
  async with wss.connect("ws://" + ip + ":13777") as ws:
    if alerted == False:
  	r = await ws.recv()
      print("Comandos Proibidos: " + r)
      alerted = True
      block = r
    canSend = True
    p = input("Seu commando(comece com / porfavor): ")
    for i in block.split(","):
      if i in p:
        canSend = False
    if canSend == True:
      await ws.send(p)
      await ws.send('/tellraw @a {"rawtext":[{"text":"§5[' + nick + '] Usou ' + p + '"}]}')
    else:
      print("Esse comando não pode ser Executado.")
    await client()