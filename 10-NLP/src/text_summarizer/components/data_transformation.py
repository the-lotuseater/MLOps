import os
from src.text_summarizer.logging import LOGGER
from transformers import AutoTokenizer
from datasets import load_from_disk

from src.text_summarizer.entity import DataTransformationConfig


class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig):
        self.data_transformation_config = data_transformation_config
        self.tokenizer = AutoTokenizer.from_pretrained(data_transformation_config.tokenizer_name)

    def convert_examples_to_features(self,batch):
        input_encodings = self.tokenizer(
            batch['dialogue'],
            max_length=1024,
            truncation=True
        )

        target_encodings = self.tokenizer(
            batch['summary'],
            max_length=1024,
            truncation=True
        )

        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }
    
    def convert(self):
        dataset_samsum = load_from_disk(self.data_transformation_config.data_path)
        dataset_samsum_pt = dataset_samsum.map(self.convert_examples_to_features, batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.data_transformation_config.root_dir,'samsum_dataset'))