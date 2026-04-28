from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import database 

app = FastAPI(
    title="Olist Dashboard API",
    description="Backend API serving data for the Olist E-commerce Dashboard"
)
