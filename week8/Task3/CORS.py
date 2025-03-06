from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    #"*",  # 允許所有來源
    "http://localhost",
    # "http://localhost:8080",
    # "https://your-domain.com",  # 允許特定網域
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法
    allow_headers=["*"],  # 允許所有標頭
    #max_age=[600]
)


@app.get("/api/data")
async def read_data():
    data = {"message": "Hello World!"}
    return data



