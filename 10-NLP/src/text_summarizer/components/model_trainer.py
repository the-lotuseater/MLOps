from src.text_summarizer.config.configuration import ConfigurationManager
from src.text_summarizer.config.configuration import ModelTrainerConfig
from transformers import AutoTokenizer, PegasusForConditionalGeneration, Seq2SeqTrainingArguments
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer,DataCollatorForSeq2Seq,Seq2SeqTrainer
from datasets import load_from_disk
from src.text_summarizer.logging import LOGGER
import os

import torch

class ModelTrainer():
    def __init__(self,model_trainer_config:ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config

    def train(self):
        device = self.model_trainer_config.device if torch.cuda.is_available() else 'cpu'
        tokenizer = AutoTokenizer.from_pretrained(self.model_trainer_config.model_ckpt)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.model_trainer_config.model_ckpt).to(device)
        seq2seq_data_collector = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)
        LOGGER.info(self.model_trainer_config)
        dataset_samsum_pt = load_from_disk(self.model_trainer_config.data_path)
        trainer_args = Seq2SeqTrainingArguments(
            output_dir='pegasus-samsum', 
            num_train_epochs=self.model_trainer_config.num_train_epochs, 
            warmup_steps=self.model_trainer_config.warmup_steps,
            per_device_train_batch_size=self.model_trainer_config.per_device_train_batch_size,
            per_device_eval_batch_size=1,
            weight_decay=self.model_trainer_config.weight_decay,
            logging_steps=self.model_trainer_config.logging_steps,
            eval_strategy=self.model_trainer_config.evaluation_strategy,
            eval_steps=self.model_trainer_config.eval_steps,
            save_steps=self.model_trainer_config.save_steps,
            gradient_accumulation_steps=self.model_trainer_config.gradient_accumulation_steps
        )
        LOGGER.info(f"dataset={dataset_samsum_pt}")
        trainer = Seq2SeqTrainer(
                            model=model_pegasus,
                            args=trainer_args,
                            data_collator=seq2seq_data_collector,
                            train_dataset=dataset_samsum_pt['train'],
                            eval_dataset = dataset_samsum_pt['validation']
                        )
        trainer.train()

        model_pegasus.save_pretrained(os.path.join(self.model_trainer_config.root_dir,'pegasus-samsum-model'))
        tokenizer.save_pretrained(os.path.join(self.model_trainer_config.root_dir,'tokenizer'))