import mysql.connector
from typing import Annotated
from fastapi import FastAPI, Request,Path, Query, Body
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse,FileResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

from starlette.middleware.sessions import SessionMiddleware
import base64
import os

#資料庫會存入這個變數中
website_db = mysql.connector.connect(
                                    user="root",
                                    password="12345678",
                                    host="localhost",
                                    database="website",
                                    charset="utf8mb4")

templates = Jinja2Templates(directory="templates")  # 指定模板目錄
app = FastAPI()

# base64.b32encode(os.urandom(20))
# base64.b64encode(os.urandom(24))
random_token = base64.b32encode(os.urandom(20))
app.add_middleware(SessionMiddleware, secret_key = random_token)#隨機產生安全金鑰
print(random_token)



## "/signup" 接收註冊資料，檢視註冊資料中是否有重複註冊等問題
"""
1.確認資料庫中不要有相同的帳號(username)
2.如果沒有的話就新增一組進資料庫中
"""
@app.post("/signup")
def sigup_Verification(request: Request, body = Body(None)): #greater than or equal to 1
    data = json.loads(body)
    cursor = website_db.cursor()
    """
    這邊修改成先用資料庫做篩選
    如果回傳值是null就可以註冊
    回傳有值的話就不能註冊

    這邊前端傳過來的資料為 名稱、帳號、密碼、
    """

    ##新的註冊姓名
    new_username = data["signup_account"]

    #查這個帳號有沒有在資料庫中
    cursor.execute("select username from member where username= %s;", (new_username,))
    myresult = cursor.fetchall()#回傳所有資料庫指令結果
    # print("123",myresult)
    # print(myresult[0])
    

    #如果在資料庫中
    if len(myresult) != 0:
        message = "帳號重複"
        # print(message)
        return {"sign-up": False, "message": message}

    #新增新的帳號至資料庫中
    else:
        print("ok")
        cursor = website_db.cursor()
        new_signup_name = data["signup_name"]
        new_signup_account = data["signup_account"]
        new_signup_password = data["signup_password"]
        new_signu_data = (new_signup_name,new_signup_account,new_signup_password)
        
        #插入新的資料到資料庫
        cursor.execute("insert into member (name,username,password) values (%s,%s,%s);", new_signu_data)
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
    cursor.execute("select name, username, password ,id from member where username = %s;", (account,))#選所有符合的帳號
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
        


        request.session["user_id"] = myresult[0][1] #將session存入request中
        request.session["user_id_index"] = myresult[0][3] #將session存入request中

        name = myresult[0][0]#名稱
        name_id = myresult[0][3]#名稱id

        return {"sign-in": True, "message": "SUCCESS!", "name":name , "name_id":name_id}

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
    # print(data)

    name = request.session["user_id"]
    name_id = request.session["user_id_index"]
    
    new_message = data["new_message"]

    print(data["new_message"])

    # 空值的話{'new_message': ''，重傳所有的留言}
    if data["new_message"] == "":
        print(data["new_message"])

        cursor = website_db.cursor()
        cursor.execute("select member.name, message.content, message.id, member.id from message inner join member on message.member_id = member.id order by message.time desc;")#選所有的留言
        myresult = cursor.fetchall()#回傳所有資料庫指令結果
        
        return{"new_message":False,"message": myresult,"siginin_id":name_id}


    #有新留言值的話就先新增留言然後回傳所有的留言
    #依照session裡儲存的帳號做id查詢
    else:
        cursor = website_db.cursor()
        #查member_id
        cursor.execute("select id from member where member.name = %s", (name,))

        myresult = cursor.fetchall()#回傳所有資料庫指令結果
        # user_id = myresult[0][0]#member_id(str)

        #新增留言
        cursor.execute("insert into message (member_id, content) values(%s,%s)", (name_id, new_message))
        website_db.commit()
        cursor.execute("select member.name, message.content, message.id, member.id from message inner join member on message.member_id = member.id order by message.time desc;")#選所有的留言
        myresult = cursor.fetchall()#回傳所有資料庫指令結果


        print("aaaa",name)
        return{"new_message":True,"message": myresult, "siginin_id":name_id}



#刪除留言
@app.post("/deleteMessage")
def createMessage(request: Request, body = Body(None)):
    data = json.loads(body)
    # print(data)
    # data2 = data
    # print(data["message_index"])
    name_id = request.session["user_id_index"]
    cursor = website_db.cursor()
    cursor.execute("delete from message where message.id = %s",(data["message_index"],))
    website_db.commit()

    cursor.execute("select member.name, message.content, message.id, member.id from message inner join member on message.member_id = member.id order by message.time desc;")#選所有的留言
    myresult = cursor.fetchall()#回傳所有資料庫指令結果


    return{"new_message":False,"message": myresult, "siginin_id":name_id}



# ----------靜態物件----------
app.mount("/", StaticFiles(directory="static" ,html=True))#所有靜態文件資料夾
templates = Jinja2Templates(directory="templates")#Jinja2模板
