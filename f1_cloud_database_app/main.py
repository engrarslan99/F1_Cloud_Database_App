from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.oauth2.id_token;
from google.auth.transport import requests
from google.cloud import firestore
import starlette.status as status

app=FastAPI()

firestore_db = firestore.Client()

firebase_request_adapter = requests.Request()

app.mount('/static', StaticFiles(directory='static'),name='static')
templates = Jinja2Templates(directory="templates")

def validateFirebaseToken(id_token):

    if not id_token:
        return None
    try:
        user_token = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        return user_token
    except ValueError as err:
        print("Token validation failed:", str(err))
        return None
    
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    drivers = [doc.to_dict() for doc in firestore_db.collection("drivers").stream()]
    teams = [doc.to_dict() for doc in firestore_db.collection("teams").stream()]

    return templates.TemplateResponse("main.html", {
        "request": request, 
        "user_token": user_token,
        "drivers": drivers,
        "teams": teams
    })

def add_driver(data):
    firestore_db.collection("drivers").add(data)

def add_team(data):
    firestore_db.collection("teams").add(data)

@app.get("/add-driver", response_class=HTMLResponse)
async def add_driver_page(request: Request):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    return templates.TemplateResponse("add_driver.html", {
        "request": request,
        "user_token": user_token
    })

@app.get("/driver/{driver_id}", response_class=HTMLResponse)
async def show_driver_details(request: Request, driver_id: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    driver_ref = firestore_db.collection("drivers").document(driver_id)
    driver = driver_ref.get()

    if not driver.exists:
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("driver_details.html", {
        "request": request,
        "driver": driver.to_dict(),
        "user_token": user_token
    })

@app.get("/add-team", response_class=HTMLResponse)
async def add_team_page(request: Request):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    return templates.TemplateResponse("add_team.html", {
        "request": request,
        "user_token": user_token
    })

@app.get("/team/{team_id}", response_class=HTMLResponse)
async def show_team_details(request: Request, team_id: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    team_ref = firestore_db.collection("teams").document(team_id)
    team = team_ref.get()

    if not team.exists:
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("team_details.html", {
        "request": request,
        "team": team.to_dict(),
        "user_token": user_token
    })




@app.post("/add-driver")
async def add_driver(
    request: Request,
    name: str = Form(...), 
    age: int = Form(...), 
    team: str = Form(...),
    total_pole_positions: int = Form(default=0),
    total_race_wins: int = Form(default=0),
    total_points_scored: int = Form(default=0),
    total_world_titles: int = Form(default=0),
    total_fastest_laps: int = Form(default=0)
):
    
    existing_drivers = list(firestore_db.collection("drivers").where("name", "==", name).stream())

    if existing_drivers: 
        return templates.TemplateResponse("add_driver.html", {
            "request": request,
            "error": f"The driver name '{name}' already exists. Try another name."
        })
    
    data = {
        "name": name, "age": age, "team": team,
        "total_pole_positions": total_pole_positions,
        "total_race_wins": total_race_wins,
        "total_points_scored": total_points_scored,
        "total_world_titles": total_world_titles,
        "total_fastest_laps": total_fastest_laps
    }
    doc_ref = firestore_db.collection("drivers").add(data)
    driver_id = doc_ref[1].id  

    firestore_db.collection("drivers").document(driver_id).update({"id": driver_id})

    return RedirectResponse("/", status_code=302)

@app.post("/add-team")
async def add_team(
    request: Request,
    name: str = Form(...), 
    year_founded: int = Form(...),
    total_pole_positions: int = Form(...),
    total_race_wins: int = Form(...),
    total_constructor_titles: int = Form(...),
    previous_season_position: int = Form(...)
):
    existing_teams = list(firestore_db.collection("teams").where("name", "==", name).stream())

    if existing_teams: 
        return templates.TemplateResponse("add_team.html", {
            "request": request,
            "error": f"The team name '{name}' already exists. Try another name."
        })

    data = {
        "name": name, 
        "year_founded": year_founded,
        "total_pole_positions": total_pole_positions,
        "total_race_wins": total_race_wins,
        "total_constructor_titles": total_constructor_titles,
        "previous_season_position": previous_season_position
    }

    doc_ref = firestore_db.collection("teams").add(data)
    team_id = doc_ref[1].id

    firestore_db.collection("teams").document(team_id).update({"id": team_id})

    return RedirectResponse("/", status_code=302)


@app.get("/query-driver", response_class=HTMLResponse)
async def show_driver_query_page(request: Request): 
    return templates.TemplateResponse("query_driver.html", {"request": request})

@app.post("/query-driver")
async def query_driver(
    request: Request,
    attribute: str = Form(...),
    comparison: str = Form(...),
    value: float = Form(...)
):
    drivers_ref = firestore_db.collection("drivers")


    if comparison == "=":
        query = drivers_ref.where(attribute, "==", value)
    elif comparison == ">":
        query = drivers_ref.where(attribute, ">", value)
    elif comparison == "<":
        query = drivers_ref.where(attribute, "<", value)
    else:
        return {"error": "Invalid comparison operator"}

    drivers = [doc.to_dict() for doc in query.stream()]
    
    return templates.TemplateResponse("query_driver_results.html", {"request": request, "drivers": drivers})


@app.get("/query-team", response_class=HTMLResponse)
async def query_team_page(request: Request):
    return templates.TemplateResponse("query_team.html", {"request": request})

@app.post("/query-team", response_class=HTMLResponse)
async def query_team(
    request: Request,
    attribute: str = Form(...),
    comparison: str = Form(...),
    value: int = Form(...)
):
    teams_ref = firestore_db.collection("teams")
    query = None

    if comparison == "=":
        query = teams_ref.where(attribute, "==", value)
    elif comparison == ">":
        query = teams_ref.where(attribute, ">", value)
    elif comparison == "<":
        query = teams_ref.where(attribute, "<", value)

    results = [doc.to_dict() for doc in query.stream()]
    
    return templates.TemplateResponse("query_team_results.html", {
        "request": request,
        "teams": results
    })



@app.get("/edit-driver/{driver_id}", response_class=HTMLResponse)
async def edit_driver(request: Request, driver_id: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    driver_ref = firestore_db.collection("drivers").document(driver_id)
    driver = driver_ref.get()

    if not driver.exists:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": f"Driver with ID {driver_id} not found"
        })

    return templates.TemplateResponse("edit_driver.html", {
        "request": request,
        "driver": driver.to_dict(),
        "driver_id": driver_id,
        "user_token": user_token 
    })

@app.post("/update-driver/{driver_id}")
async def update_driver(request: Request, driver_id: str):
    id_token = request.cookies.get("token") 
    if not id_token:
        return RedirectResponse(url="/", status_code=302)

    user_token = validateFirebaseToken(id_token) 

    if not user_token:
        return RedirectResponse(url="/", status_code=302)

    form_data = await request.form()
    updated_data = {
        "age": int(form_data["age"]),
        "total_pole_positions": int(form_data["total_pole_positions"]),
        "total_race_wins": int(form_data["total_race_wins"]),
        "total_points_scored": int(form_data["total_points_scored"]),
        "total_world_titles": int(form_data["total_world_titles"]),
        "total_fastest_laps": int(form_data["total_fastest_laps"]),
        "team": form_data["team"]
    }

    driver_ref = firestore_db.collection("drivers").document(driver_id)
    driver_ref.update(updated_data)

    return RedirectResponse(url=f"/driver/{driver_id}", status_code=302)



@app.get("/edit-team/{team_id}", response_class=HTMLResponse)
async def edit_team(request: Request, team_id: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    team_ref = firestore_db.collection("teams").document(team_id)
    team = team_ref.get()

    if not team.exists:
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("edit_team.html", {
        "request": request, 
        "team": team.to_dict(),
        "user_token": user_token
        })

@app.post("/update-team/{team_id}")
async def update_team(request: Request, team_id: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    if not user_token:
        return RedirectResponse(url="/", status_code=302)

    form_data = await request.form()
    updated_data = {
        "year_founded": int(form_data["year_founded"]),
        "total_pole_positions": int(form_data["total_pole_positions"]),
        "total_race_wins": int(form_data["total_race_wins"]),
        "total_constructor_titles": int(form_data["total_constructor_titles"]),
        "previous_season_position": int(form_data["previous_season_position"])
    }

    team_ref = firestore_db.collection("teams").document(team_id)
    team_ref.update(updated_data)

    return RedirectResponse(url=f"/team/{team_id}", status_code=302)



@app.post("/delete-driver/{driver_id}")
async def delete_driver(request: Request, driver_id: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    if not user_token:
        return RedirectResponse(url="/", status_code=302)  

    firestore_db.collection("drivers").document(driver_id).delete()  

    return RedirectResponse(url="/", status_code=302)  

@app.post("/delete-team/{team_id}")
async def delete_team(request: Request, team_id: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    if not user_token:
        return RedirectResponse(url="/", status_code=302)

    firestore_db.collection("teams").document(team_id).delete()  

    return RedirectResponse(url="/", status_code=302) 


@app.get("/compare-drivers", response_class=HTMLResponse)
async def compare_drivers_page(request: Request):
    drivers = [doc.to_dict() for doc in firestore_db.collection("drivers").stream()]
    return templates.TemplateResponse("compare_drivers.html", {
        "request": request,
        "drivers": drivers
    })

@app.post("/compare-drivers", response_class=HTMLResponse)
async def compare_drivers(request: Request, driver1_id: str = Form(...), driver2_id: str = Form(...)):
    driver1_ref = firestore_db.collection("drivers").document(driver1_id).get()
    driver2_ref = firestore_db.collection("drivers").document(driver2_id).get()

    if not driver1_ref.exists or not driver2_ref.exists:
        return RedirectResponse(url="/", status_code=302)

    driver1 = driver1_ref.to_dict()
    driver2 = driver2_ref.to_dict()

    return templates.TemplateResponse("compare_drivers_results.html", {
        "request": request,
        "driver1": driver1,
        "driver2": driver2
    })



@app.get("/compare-teams", response_class=HTMLResponse)
async def compare_teams_page(request: Request):
    teams = [doc.to_dict() for doc in firestore_db.collection("teams").stream()]
    return templates.TemplateResponse("compare_teams.html", {
        "request": request,
        "teams": teams
    })

@app.post("/compare-teams", response_class=HTMLResponse)
async def compare_teams(request: Request, team1_id: str = Form(...), team2_id: str = Form(...)):
    team1_ref = firestore_db.collection("teams").document(team1_id).get()
    team2_ref = firestore_db.collection("teams").document(team2_id).get()

    if not team1_ref.exists or not team2_ref.exists:
        return RedirectResponse(url="/", status_code=302)

    team1 = team1_ref.to_dict()
    team2 = team2_ref.to_dict()

    return templates.TemplateResponse("compare_teams_results.html", {
        "request": request,
        "team1": team1,
        "team2": team2
    })