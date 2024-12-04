from fastapi import FastAPI, HTTPException, Request, Form, status, Response, Cookie, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from user_db import register_user, authenticate_user
import uvicorn
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from logger import logger
import os

load_dotenv()


sessions = {}

templates = Jinja2Templates(directory='templates')

app =FastAPI()

@app.get("/", response_class=HTMLResponse) 
async def home(request: Request):
  current_username=request.cookies.get("username")
  if current_username:
     sessions[current_username]=True
     redirect_response = RedirectResponse(url='/secure', status_code=status.HTTP_303_SEE_OTHER)
     return redirect_response
  return templates.TemplateResponse('login.html', {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
  logger.info(f"Method=get;Name=Register;Cookies:{request.cookies}")
  return templates.TemplateResponse('register.html', {"request": request})

@app.post("/register")
async def register_user_form(username: str = Form(...), password: str = Form(...)):
  if not register_user(username, password):
    raise HTTPException(status_code=400, detail='Username already exist')
  return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)

@app.post("/login")
async def login_user(response: Response, username: str = Form(...), password: str = Form(...)):
  if not authenticate_user(username, password):
    raise HTTPException(status_code=401, detail="Invalid credentials")
  sessions[username] = True
  redirect_response = RedirectResponse(url='/secure', status_code=status.HTTP_303_SEE_OTHER)
  redirect_response.set_cookie(key="username", value=username)

  return redirect_response

def get_current_username(username: str = Cookie(None)):
  if not username:
    raise HTTPException(status_code=401, detail = "Not authenticated")
  return username

@app.get("/secure")
async def secure_page(request: Request, username: str=Depends(get_current_username)):
  #check to see if user is logged in(has active session)
  if not sessions.get(username):
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
  return templates.TemplateResponse("secure.html", {"request": request, "username": username})

@app.get("/logout")
def logout_user(request:Request,response: Response):
  # redirect_response = RedirectResponse(url="/", status_code=status.HTTP_301_MOVED_PERMANENTLY)
  current_username=request.cookies.get("username")
  if sessions.get(current_username):
     del sessions[current_username]
     
  response.delete_cookie("username")
  
  
def run() -> None:
    """Runs the FastAPI application."""
    try:
        PORT= int(os.environ.get('PORT',8080)) 
        HOST=str(os.environ.get('HOST'))
        logger.info('Starting App')
        uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    run()
