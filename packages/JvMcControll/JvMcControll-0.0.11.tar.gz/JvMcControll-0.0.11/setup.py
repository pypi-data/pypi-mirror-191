from setuptools import setup
import os

dc = os.getcwd() + "/"

with open(dc + "README.md", "r") as arq:
    readme = arq.read()

setup(name='JvMcControll',
    version='0.0.11',
    license='MIT License',
    author='Jvsm Games',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='jvsm5000wt@gmail.com',
    keywords='websocket',
    description=u'Hospede seu mcbe controller ou jogue no de seus amigos :)',
    packages=['JvMcControll'],
    install_requires=['websockets', 'asyncio'],)