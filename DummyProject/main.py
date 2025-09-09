from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True


@app.get('/blog')
def index():

    return {"data": "blog list!"}

@app.get('/blog/{id}')
def show(id:int):
    return {"data": id}



@app.post('/blog')
def create(request: Blog):
    return {"data": f"Blog is created with title as {request.title}"}


@app.get('/blog/{id}/comments')
def show(id:int):
    return {"data": id}