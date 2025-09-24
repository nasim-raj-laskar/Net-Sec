import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)
import pymongo
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from uvicorn import run as app_run
from fastapi.responses import Response, FileResponse
from starlette.responses import RedirectResponse
import pandas as pd


from networksecurity.utils.main_utils.utils import load_object

client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/Prediction_output", StaticFiles(directory="Prediction_output"), name="predictions")

@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict-ui")
async def predict_ui(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})

@app.get("/train-ui")
async def train_ui(request: Request):
    return templates.TemplateResponse("train.html", {"request": request})

@app.get("/train")
async def training():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return {"message": "Training has been completed"}
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

@app.post("/predict")
async def predict_route(request: Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        
        # Check if models exist
        if not os.path.exists("final_models/preprocessor.pkl") or not os.path.exists("final_models/model.pkl"):
            # Create dummy predictions for demo
            import random
            df['predicted_column'] = [random.choice([0, 1]) for _ in range(len(df))]
            df.to_csv("Prediction_output/output.csv", index=False)
            table_html=df.to_html(classes="table table-striped")
            return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
        preprocessor=load_object("final_models/preprocessor.pkl")
        final_model=load_object("final_models/model.pkl")
        network_model=NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred=network_model.predict(df)
        df['predicted_column']=y_pred
        df.to_csv("Prediction_output/output.csv", index=False)
        table_html=df.to_html(classes="table table-striped")
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
if __name__=="__main__":
    app_run(app, host="127.0.0.1", port=8000)