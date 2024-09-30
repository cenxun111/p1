# app/database.py
import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)


# 创建数据库会话生成器
def get_session():
    with Session(engine) as session:
        yield session
