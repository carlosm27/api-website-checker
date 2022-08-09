import typing

from piccolo.utils.pydantic import create_pydantic_model
from piccolo.engine import engine_finder

from fastapi import FastAPI,HTTPException, status
from sql.tables import Website
from services import website_checker, scheduler
from api.connectivity_checker import api_checker
from rocketry import Rocketry

WebsiteModelIn: typing.Any = create_pydantic_model(table=Website, model_name="WebsiteModelIn")

WebsiteModelOut: typing.Any = create_pydantic_model(table=Website, include_default_columns=True,
                                                    model_name="WebsiteModelOut")

app = FastAPI()
rocketry_app = Rocketry()

app.mount("/api/", api_checker)


@app.get("/website")
async def websites():
    try:
        website = await Website.select()
        return website
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")


@app.post("/website", response_model= WebsiteModelOut)
async def add_website(website_model: WebsiteModelIn):
    try:
        website = Website(**website_model.__dict__)
        await website.save()
        return WebsiteModelOut(**website.__dict__)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")


@app.get("/website/{id}")
async def website_by_id(id: int):
    website = await Website.select().where(id == Website.id)
    if not website:
         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")
    return website

@rocketry_app.task("every 10 seconds")
@app.get("/website/status/{id}")
async def website_status(id: int):
    website = await Website.select().where(id == Website.id)
    if not website:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")
    url =  website[0]['url']
    url_status = website_checker.site_is_online(url)
    result_status = website_checker.display_check_result(url_status, url)
    if result_status != 'Online!':
        raise HTTPException (status.HTTP_500_INTERNAL_SERVER_ERROR, detail ="Internal Server Error")
    return result_status


@app.delete("/website/{id}")
async def delete_website(id: int):
    website = await Website.objects().get(id == Website.id)
    if not website:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")
    website_selected = await Website.select().where(id == Website.id)
    url = website_selected[0]['url']
    await website.remove()
    return f'{url} deleted'



@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")

@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")


