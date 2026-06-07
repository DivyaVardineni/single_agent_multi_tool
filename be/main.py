from fastapi import FastAPI,Query
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool 
import mysql.connector
import requests
import os 
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

app=FastAPI()

OPENWEATHER_API_KEY="OPENWEATHER_API_KEY"

conn=mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
     ssl_disabled=False
)




def initialize_database():
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE,
        department VARCHAR(50),
        salary DECIMAL(10,2),
        hire_date DATE
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
        INSERT INTO employees
        (first_name, last_name, email, department, salary, hire_date)
        VALUES
        ('John', 'Doe', 'john.doe@example.com', 'IT', 65000.00, '2023-01-15'),
        ('Jane', 'Smith', 'jane.smith@example.com', 'HR', 55000.00, '2022-08-10'),
        ('Michael', 'Johnson', 'michael.johnson@example.com', 'Finance', 72000.00, '2021-05-20'),
        ('Emily', 'Brown', 'emily.brown@example.com', 'Marketing', 60000.00, '2024-02-01'),
        ('David', 'Wilson', 'david.wilson@example.com', 'IT', 70000.00, '2020-11-12')
        """)

        conn.commit()

    cursor.close()




initialize_database()







@tool
def weather(city:str):
    """this is to get temp of city"""
    res=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}")
    data=res.json()
    return data



@tool
def sqltool(query:str):
    """ this for sql tooling"""
    cursor=conn.cursor(dictionary=True)
    cursor.execute(query)

    allemps=cursor.fetchall()

    return allemps


@tool
def webtool(question:str):
    """this is for wed search tooling"""
    result=client.search(
        query=question,
        max_limit=5

    )
    return result

llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key="API_KEY"
)

client=TavilyClient(
    api_key="api_key_tvly"
)

agent=create_agent(
    model=llm,
    tools=[weather,sqltool,webtool]
)


@app.get("/")
def home():
    return{
        "message":"backend working..."
    }

@app.post("/weather_tooling")
def weather_tool(city:str=Query(...),question:str=Query(...)):
    result= agent.invoke({
        "messages":[{"role":"user","content":f"city{city} question:{question}"}]
    })

    return result


@app.post("/sql_tooling")
def sql_tool(question:str=Query(...)):
    result=agent.invoke({
        "messages":[{"role":"user","content":f"query:{question}"}]
    })

    return result


@app.post("/web_tooling")
def web_tool(question:str=Query(...)):
    result=agent.invoke({
        "messages":[{"role":"user","content":f" question :{question}"}]
    })

    return result