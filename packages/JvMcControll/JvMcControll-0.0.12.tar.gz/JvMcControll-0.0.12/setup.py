from setuptools import setup
import os

dc = os.getcwd() + "/"

with open(dc + "README.md", "r") as arq:
    readme = arq.read()

setup(name='JvMcControll',
    version='0.0.12',
    license='MIT License',
    author='Jvsm Games',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='jvsm5000wt@gmail.com',
    keywords='websocket',
    description=u'Este script Python é projetado para ajudar streamers de Minecraft Bedrock a tornar suas transmissões mais interativas, permitindo que o chat envie comandos diretamente ao jogo por meio de uma conexão WebSocket.',
    packages=['JvMcControll'],
    install_requires=['websockets', 'asyncio'],)