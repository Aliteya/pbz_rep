# main.py
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.crud import *  
from app.database import conn
from typing import Optional
from datetime import date
import logging


app = FastAPI()
templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.DEBUG)

@app.post("/owners/add")
def create_owner(contact: str = Form(...), type_of_owner: str = Form(...), name: str = Form(...), owners_fullname : str = Form(...)):
    try:
        add_owner(contact, type_of_owner, name, owners_fullname)
        return RedirectResponse(url="/owners/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/objects/add")
def create_object(type: str = Form(...), adress: str = Form(...), name: str = Form(...), number_of_places: int = Form(...), owner_id: int = Form(...)):
    try:
        add_object(type, adress, name, number_of_places,owner_id)
        return RedirectResponse(url="/objects/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/popularities/add")
def create_popularity(event_date: date = Form(...), number_of_visitors: int = Form(...), object_id: int = Form(...)):
    try:
        add_popularity(event_date, number_of_visitors, object_id)
        return RedirectResponse(url="/popularities/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/events/add")
def create_event(fut_event_date: date = Form(...), event_name: str = Form(...), event_type: str = Form(...), object_id: int = Form(...)):
    try:
        add_event(fut_event_date, event_name, event_type, object_id)
        return RedirectResponse(url="/events/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dates/add")
def create_date(opening_date: date = Form(...), closing_date: date = Form(...), object_id: int = Form(...)):
    try:
        add_date(opening_date, closing_date, object_id)
        return RedirectResponse(url="/dates/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# обновление
@app.get("/owners/put/{owner_id}")
def edit_owner_page(request: Request):
    owner_id = request.path_params['owner_id']
    owner = get_owner_by_id(owner_id)

    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return templates.TemplateResponse("edit_owner.html", {"request": request, "owner": owner})

@app.post("/owners/put/{owner_id}")
def edit_owner(request: Request, contact: str = Form(...), type_of_owner: str = Form(...), name: str = Form(...), owners_fullname: str = Form(...)):
    try:
        owner_id = request.path_params['owner_id']
        update_owner(owner_id, contact, type_of_owner, name, owners_fullname)
        return RedirectResponse(url="/owners/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#----------------

@app.get("/objects/put/{object_id}")
def edit_object_page(request: Request):
    object_id = request.path_params['object_id']
    object = get_object_by_id(object_id)
    owners = get_owners()
    logging.debug("Инфа об объекте:", object)

    if object is None:
        raise HTTPException(status_code=404, detail="Object not found")
    return templates.TemplateResponse("edit_object.html", {"request": request, "object": object, "owners": owners})
    
@app.post("/objects/put/{object_id}")
def edit_object(request: Request, type: str = Form(...), adress: str = Form(...), name: str = Form(...), number_of_places: int = Form(...),owner_id: int = Form(...)):
    try:
        object_id = request.path_params['object_id']
        update_object(object_id, type, adress, name, number_of_places,owner_id)
        return RedirectResponse(url="/objects/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-------------    

@app.get("/popularities/put/{popularity_id}")
def edit_popularity_page(request: Request):
    popularity_id = request.path_params['popularity_id']
    popularity = get_popularity_by_id(popularity_id)
    logging.debug("Инфа об популярности: %s", popularity)

    if popularity is None:
        raise HTTPException(status_code=404, detail="Popularity not found")
    return templates.TemplateResponse("edit_popularity.html", {"request": request, "popularity": popularity})

@app.post("/popularities/put/{popularity_id}")
def edit_popularity(request: Request, event_date: date = Form(...), number_of_visitors: int = Form(...)):
    try:
        popularity_id = request.path_params['popularity_id']
        update_popularity(popularity_id, event_date, number_of_visitors)
        return RedirectResponse(url="/popularities/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-------------------

@app.get("/events/put/{event_id}")
def edit_event_page(request: Request):
    event_id = request.path_params['event_id']
    event = get_event_by_id(event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return templates.TemplateResponse("edit_event.html", {"request": request, "event": event})

@app.post("/events/put/{event_id}")
def edit_event(request: Request, fut_event_date: date = Form(...), event_name: str = Form(...), event_type: str = Form(...)):
    try:
        event_id = request.path_params['event_id']
        update_event(event_id, fut_event_date, event_name, event_type)
        return RedirectResponse(url="/events/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#---------------------

@app.get("/dates/put/{date_id}")
def edit_date_page(request: Request):
    date_id = request.path_params['date_id']
    date = get_date_by_id(date_id)

    if date is None:
        raise HTTPException(status_code=404, detail="Date not found")
    return templates.TemplateResponse("edit_date.html", {"request": request, "date": date})

@app.post("/dates/put/{date_id}")
def edit_date(request: Request, opening_date: date = Form(...), closing_date: date = Form(...)):
    try:
        date_id = request.path_params['date_id']
        update_date(date_id, opening_date, closing_date)
        return RedirectResponse(url="/dates/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# удаление 
@app.post("/owners/{owner_id}")
def remove_owner(request: Request):
    try:
        owner_id = request.path_params['owner_id']
        delete_owner(owner_id)
        return RedirectResponse(url="/owners/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/objects/{object_id}")
def remove_object(request: Request):
    try:
        object_id = request.path_params['object_id']
        delete_city_object(object_id)
        return RedirectResponse(url="/objects/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/popularities/{popularity_id}")
def remove_popularity(request: Request):
    try:
        popularity_id = request.path_params['popularity_id']
        delete_popularity(popularity_id)
        return RedirectResponse(url="/popularities/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/events/{event_id}")
def remove_event(request: Request):
    try:
        event_id = request.path_params['event_id']
        delete_event(event_id)
        return RedirectResponse(url="/events/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/dates/{date_id}")
def remove_date(request: Request):
    try:
        date_id = request.path_params['date_id']
        delete_date(date_id)
        return RedirectResponse(url="/dates/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#---особые--селекты-----
@app.get("/objects/currrent")
def view_current_objects(request: Request):
    curr_objects = fetch_current_objects()
    return templates.TemplateResponse("but_curr_object.html", {"request": request, "curr_objects": curr_objects})

@app.get("/events/upcoming")
def view_upcoming_events(request: Request):
    upcoming_events = fetch_upcoming_events()
    return templates.TemplateResponse("upcoming_events.html", {"request": request, "upcoming_events": upcoming_events})

@app.get("/objects/current_type")
def view_curr_type_objects(request: Request):
    cur_type_objects = fetch_curr_type_objects()
    return templates.TemplateResponse("but_curr_type_object.html", {"request": request, "curr_type_objects": cur_type_objects})

#----обычные-----селекты----------
@app.get("/owners/", response_class=HTMLResponse)
def view_owners(request: Request):
    owners = get_owners() 
    return templates.TemplateResponse("view_owners.html", {"request": request, "owners": owners})

@app.get("/objects/", response_class=HTMLResponse)
def view_objects(request: Request):
    objects = get_objects() 
    owners = get_owners()
    return templates.TemplateResponse("view_objects.html", {"request": request, "objects": objects, "owners": owners})

@app.get("/popularities/", response_class=HTMLResponse)
def view_popularities(request: Request):
    popularities = get_popularities() 
    objects = get_objects() 
    return templates.TemplateResponse("view_popularities.html", {"request": request, "popularities": popularities, "objects": objects})

@app.get("/events/", response_class=HTMLResponse)
def view_events(request: Request):
    events = get_events() 
    objects = get_objects() 
    return templates.TemplateResponse("view_events.html", {"request": request, "events": events, "objects": objects})

@app.get("/dates/", response_class=HTMLResponse)
def view_dates(request: Request):
    dates = get_dates() 
    objects = get_objects() 
    return templates.TemplateResponse("view_dates.html", {"request": request, "dates": dates, "objects": objects})


@app.on_event("shutdown")
def shutdown_db_connection():
    conn.close()