from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_url: Path
    local_data_file: Path
    unzip_dir: Path

@dataclass
class DataTransformationConfig:
    root_dir: str
    data_path: str
    tokenizer_name: str


@dataclass
class ModelTrainerConfig:
  model_ckpt:str
  num_train_epochs: int
  warmup_steps: int
  per_device_train_batch_size: int
  weight_decay: int
  logging_steps: int
  evaluation_strategy: str
  eval_steps: int
  save_steps: int
  gradient_accumulation_steps: int
  data_path: str
  device: str


@dataclass
class ModelEvaluationConfig:
   root_dir: str
   data_path: str
   model_path: str
   tokenizer_path: str
   metric_file_name: str