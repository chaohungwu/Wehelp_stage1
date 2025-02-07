from typing import Annotated
from fastapi import FastAPI, Request,Path, Query, Body
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse,FileResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import json


templates = Jinja2Templates(directory="templates")  # 指定模板目錄
app =FastAPI()#產生FastAPI物件

#隨機產生安全金鑰
app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY")



# ----------動態物件----------

## task4 平方功能
##這邊接收訊息然後驗證登入訊息做回傳
@app.post("/signin")
def Verification(request: Request, body = Body(None)): #greater than or equal to 1
    data = json.loads(body)
    print(data)
    ##檢驗帳號密碼
    if data["account"] == "test" and data["password"] == "test":
        request.session["user_id"] = data["account"]  # 將使用者資訊存入 session
        return {"SIGNED-IN":True, "message":"success"}
    else:
        return {"SIGNED-IN":False , "message":"Username or password is not correct"}


@app.get("/signout")
def signout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


# 錯誤訊息
@app.get("/error", response_class=HTMLResponse)
def error(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

# 成功登入API
@app.get("/member", response_class=HTMLResponse)
def success(request: Request):
    if "user_id" not in request.session:
         return RedirectResponse("/")
    else:
        return templates.TemplateResponse("member.html", {"request": request})



#平方數
@app.get("/square/{number}")
def square(request: Request,number:Annotated[int ,Path(ge=1)]): #大於等於1(正整數)
    # number=int(number)
    # result = number**2    
    return templates.TemplateResponse("square.html",{"request": request})


# ----------靜態物件----------
app.mount("/", StaticFiles(directory="static" ,html=True))#所有靜態文件資料夾
templates = Jinja2Templates(directory="templates")#Jinja2模板


@app.get("/items/{id}", response_class = HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", 
                                      {"request": request, 
                                       "id": id})