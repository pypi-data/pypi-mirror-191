from fastapi import FastAPI
import os
import sys
sys.path.append(os.path.join(os.environ['HOME'],'omspy', 'omspy'))

app = FastAPI()


@app.get('/')
def root():
    return {'hello': 'world'}
