import mysql.connector
from typing import Annotated
from fastapi import FastAPI, Request,Path, Query, Body
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse,FileResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

from starlette.middleware.sessions import SessionMiddleware
#資料庫會存入這個變數中
website_db = mysql.connector.connect(
                                    user="root",
                                    password="12345678",
                                    host="localhost",
                                    database="website",
                                    charset="utf8mb4")

# print("DB ready")

templates = Jinja2Templates(directory="templates")  # 指定模板目錄
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY")#隨機產生安全金鑰


## "/signup" 接收註冊資料，檢視註冊資料中是否有重複註冊等問題
"""
1.確認資料庫中不要有相同的帳號(username)
2.如果沒有的話就新增一組進資料庫中
"""
@app.post("/signup")
def sigup_Verification(request: Request, body = Body(None)): #greater than or equal to 1
    data = json.loads(body)
    cursor = website_db.cursor()
    cursor.execute("select username from member;")#選所有的帳號
    myresult = cursor.fetchall()#回傳所有資料庫指令結果
    all_db_username_list = []

    for (x,) in myresult: #因為取出值會有(,)所以要用for (row,) in items:的'方法避免
        all_db_username_list.append(x)

    new_username = data["signup_account"] 

    print(data)

    #如果在資料庫中
    if new_username in all_db_username_list:
        message = "帳號重複"
        return {"sign-up": False, "message": message}
    
    else:#新增新的帳號至資料庫中
        cursor = website_db.cursor()
        new_signup_name = data["signup_name"]
        new_signup_account = data["signup_account"]
        new_signup_password = data["signup_password"]

        cursor.execute("insert into member (name,username,password) values ('{}','{}','{}');".format(new_signup_name, new_signup_account, new_signup_password))#選所有的帳號
        website_db.commit()
        return {"sign-up": True, "message": "SUCCESS!"}







## "/signin" 接收登入帳號密碼資料
"""
1.確認資料庫中是否有相同的帳號和密碼(username)
2.如果沒有的話就登入失敗
2.如果有的話就登入成功，跳入登入頁面(/menber)
"""
@app.post("/signin")
def sigin_Verification(request: Request, body = Body(None)):
    data = json.loads(body)

    account = data["signin_account"]#從前端傳來的輸入帳號
    password = data["signin_password"]#從前端傳來的輸入密碼

    cursor = website_db.cursor()
    cursor.execute("select name, username, password from member where username = '{}';".format(account))#選所有的帳號

    myresult = cursor.fetchall()#回傳所有資料庫指令結果
    """
    這邊有2個可能
    1. 沒有該帳號、2. 密碼錯誤
    """
    if len(myresult)==0:
        return {"sign-in": False, "message": "帳號或密碼輸入錯誤"}

    elif  myresult[0][1] == account and myresult[0][2] != password:
        return {"sign-in": False, "message": "帳號或密碼輸入錯誤"}

    elif myresult[0][1] == account and myresult[0][2] == password:
        request.session["user_id"] = account #將session存入request中

        name = myresult[0][0]#名稱
        return {"sign-in": True, "message": "SUCCESS!", "name":name}

    else:
        return {"sign-in": False, "message": "意外錯誤"}

#登出(清除session)
@app.get("/signout")
def signout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


# 會員頁
@app.get("/member",  response_class=HTMLResponse)
def success(request: Request):
    if "user_id" not in request.session: #如果user_id沒有在session中就等回首頁
         return RedirectResponse("/")
    else:
        return templates.TemplateResponse("member.html", {"request": request})


# 錯誤頁面訊息
@app.get("/error", response_class=HTMLResponse)
def error(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})



# 取得與建立留言
"""
如果傳過來的訊息是空值回傳現在所有的留言
"""
@app.post("/createMessage")
def createMessage(request: Request, body = Body(None)):
    data = json.loads(body)
    print(data)

    # 空值的話{'new_message': ''}
    if data["new_message"] == "":
        cursor = website_db.cursor()
        cursor.execute("select member.name, message.content from message inner join member on message.member_id = member.id order by message.time desc;")#選所有的留言
        
        myresult = cursor.fetchall()#回傳所有資料庫指令結果
        print(myresult)
        
        return{"new_message":False,"message": myresult}


    #有新留言值的話就先新增留言然後回傳所有的留言
    #依照傳回來的名子做id查詢

    else:
        cursor = website_db.cursor()
        #查member_id
        name = data["name"]
        new_message = data["new_message"]
        cursor.execute("select id from member where member.name = %s", (name,))

        myresult = cursor.fetchall()#回傳所有資料庫指令結果
        user_id = myresult[0][0]#member_id(str)

        print(user_id)
        print(new_message)
        print(type(new_message))

        #新增留言
        cursor.execute("insert into message (member_id, content) values(%s,%s)", (user_id, new_message))
        website_db.commit()
        cursor.execute("select member.name, message.content from message inner join member on message.member_id = member.id order by message.time desc;")#選所有的留言
        myresult = cursor.fetchall()#回傳所有資料庫指令結果

        
        return{"new_message":True,"message": myresult}



#刪除留言
@app.post("/deleteMessage")
def createMessage(request: Request, body = Body(None)):
    data = json.loads(body)
    print(data)












# ----------靜態物件----------
app.mount("/", StaticFiles(directory="static" ,html=True))#所有靜態文件資料夾
templates = Jinja2Templates(directory="templates")#Jinja2模板
