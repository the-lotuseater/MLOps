from src.text_summarizer.config.configuration import ModelEvaluationConfig
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class PredictionPipeline:

    def __init__(self,model_evaluation_config:ModelEvaluationConfig, device:str):
        self.model_eval_config = model_evaluation_config
        self.device = device
    

    def predict(self,text):
        tokenizer = AutoTokenizer.from_pretrained(self.model_eval_config.tokenizer_path)
        gen_kwargs = {}
        gen_kwargs['length_penalty']=0.8
        gen_kwargs['num_beans']=8
        gen_kwargs['max_length']=128
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_eval_config.model_path).to(self.device)

        inputs = tokenizer(text, max_length=1024, return_tensors="pt", truncation=True)
        summary_ids = model.generate(inputs["input_ids"].to(self.device), **gen_kwargs)
        summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

        return summary_text
