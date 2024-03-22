from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='buff.steam-api',
    version='0.1.0',
    python_requires='>=3.7',
    url='https://github.com/',
    license='Unlicense',
    description='Yet another steam trade bot w/ buff.163.com',
    long_description=long_description,
    packages=['buff-steam-api'],
    install_requires=[
        'fastapi==0.*',
        'uvicorn==0.*',
        'psycopg2==2.*',
        'asyncpg==0.*',
    ],
    author='Renato Rocha',
    author_email='renatorocha21@ua.pt',
)