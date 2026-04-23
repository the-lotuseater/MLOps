import evaluate
from transformers import AutoModelForSeq2SeqLM,AutoTokenizer
from datasets import load_from_disk
from src.text_summarizer.config.configuration import ModelEvaluationConfig
import pandas as pd
from tqdm import tqdm


class ModelEvaluation:
    def __init__(self,model_eval_config:ModelEvaluationConfig,device:str):
        self.model_eval_config = model_eval_config
        self.device = device

    def generate_batch_sized_chunks(self,elements, batch_size):
        for i in range(0,len(elements),batch_size):
            yield elements[i:i+batch_size]


    def calculate_metric_on_test_ds(self,dataset,metric,model,tokenizer,batch_size=16,device='CPU',
                                    column_text='article',column_summary='highlights'):
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text],batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary],batch_size))

        for article_batch, target_batch in tqdm(zip(article_batches,target_batches),total=len(article_batches)):
            inputs = tokenizer(
                                article_batch,
                                max_length=1024,
                                truncation=True,
                                padding='max_length',
                                return_tensors='pt'
                            )
            summaries = model.generate(input_ids=inputs['input_ids'].to(device),
            attention_mask = inputs['attention_mask'].to(device),
            length_penalty=0.8, num_beans = 8, max_length = 128)

        decoded_summaries = [tokenizer.decode(s,skip_special_tokens=True,clean_up_tokenization_spaces=True) for s in summaries]

        decoded_summaries = [d.replace('',' ') for d in decoded_summaries]
        metric.add_batch(predictions=decoded_summaries,references=target_batch)

        score = metric.compute()
        return score
    
    def initiate_evaluation(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_eval_config.tokenizer_path)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.model_eval_config.model_path).to(self.device)

        dataset_samsum_pt = load_from_disk(self.model_eval_config.data_path)

        rouge_metric = evaluate.load('rouge')
        rouge_names = ['rouge1','rouge2','rougeL','rougeLsum']

        score = self.calculate_metric_on_test_ds(dataset_samsum_pt['test'][0:10],rouge_metric,model_pegasus,tokenizer,batch_size=2,column_text='dialogue',column_summary='summary')
        rouge_dict = dict((rn,score[rn].mid.fmeasure) for rn in rouge_names)
        df = pd.DataFrame(rouge_dict, index=['pegasus'])
        df.to_csv(self.model_eval_config.metric_file_name,index=False)
