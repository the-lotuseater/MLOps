from fastapi import FastAPI
import uvicorn
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from src.text_summarizer.pipeline.stage_5_prediction_pipeline import PredictionPipeline
from src.text_summarizer.config.configuration import ModelEvaluationConfig, ConfigurationManager
from pydantic import BaseModel


class Msg(BaseModel):
    text:str

app = FastAPI()
pred_pipeline:PredictionPipeline = None
model_eval_config:ModelEvaluationConfig = None

@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def training():
    response = Response('Training was successful!')
    try:
        os.system('python main.py')
    except Exception as e:
        response = Response(f'Error Occured! {e}')
    return response

@app.post('/predict')
async def predict_route(request:Msg):
    global pred_pipeline
    try:
        if pred_pipeline == None:
            await load_model()
        
        result = pred_pipeline.predict(request.text)
        return {'summary':result}
    except Exception as e:
        raise e
    
@app.put('/load')
async def load_model():
    global pred_pipeline,model_eval_config
    config_manager = ConfigurationManager()
    model_eval_config = config_manager.get_model_evaluation_config()
    pred_pipeline = PredictionPipeline(model_evaluation_config=model_eval_config,device=config_manager.config.device)

    
if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0', port=8080)