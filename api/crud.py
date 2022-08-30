import typing

from piccolo.utils.pydantic import create_pydantic_model

from fastapi import FastAPI,HTTPException, status
from sql.tables import Website
from services import website_checker


WebsiteModelIn: typing.Any = create_pydantic_model(table=Website, model_name="WebsiteModelIn")

WebsiteModelOut: typing.Any = create_pydantic_model(table=Website, include_default_columns=True,
                                                    model_name="WebsiteModelOut")

app_crud = FastAPI()


@app_crud.get("/website")
async def websites():
    try:
        website = await Website.select()
        return website
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")


@app_crud.post("/website", response_model= WebsiteModelOut)
async def add_website(website_model: WebsiteModelIn):
    try:
        website = Website(**website_model.__dict__)
        await website.save()
        return WebsiteModelOut(**website.__dict__)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")


@app_crud.get("/website/{id}")
async def website_by_id(id: int):
    website = await Website.select().where(id == Website.id)
    if not website:
         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")
    return website


@app_crud.get("/website/status/{id}")
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


@app_crud.delete("/website/{id}")
async def delete_website(id: int):
    website = await Website.objects().get(id == Website.id)
    if not website:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Website Not Found")
    website_selected = await Website.select().where(id == Website.id)
    url = website_selected[0]['url']
    await website.remove()
    return f'{url} deleted'

if __name__=="__main__":
    app_crud.run()