import json
import os
from pathlib import Path
from .JsonParser import DataJsonParser
from .JsonParser import ModelJsonParser
from .JsonSerializer import Dataset_stats, Metric_stats
from .ExpTimer import ExpTimer

_JSON_EXTS = [".json"]


class Experiment:
    def __init__(self, exp_path) -> None:
        if not os.path.exists(exp_path):
            raise FileNotFoundError("File {} not found".format(exp_path))

        self.data_config = {}
        self.model_config = {}
        self.validate_path(exp_path)

        with open(exp_path, 'r') as f:
            exp_config = json.load(f)

        self.init_exp_module_list(exp_config)
        self.timer_stats = ExpTimer()

    def init_exp_module_list(self, exp_config: dict):
        self.data_config = DataJsonParser(exp_config)
        self.model_config = ModelJsonParser(exp_config)

    def save(self):
        result_path = self.model_config.result_path
        self.validate_path(result_path)

        parent_dir = Path(result_path).parent.absolute()
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)
        
        with open(result_path, 'w+') as f:
            exp_result = {}

            exp_result['config'] = {**self.model_config.__dict__,**self.data_config.__dict__}
            exp_result['timer'] = self.timer_stats.serialize()
            exp_result['dataset'] = self.dataset_stats.__dict__
            exp_result['test_result'] = self.test_stats.__dict__
            exp_result['val_result'] = self.val_stats.__dict__
            json.dump(exp_result, f)

    def validate_path(self, file_path):
        if Path(file_path).suffix not in _JSON_EXTS:
            raise FileNotFoundError("File is not {} format".format(_JSON_EXTS))

    def dataload_init(self):
        self.timer_stats.dataload_init()
        self.dataset_stats = Dataset_stats()
        
    def dataload_duration(self):
        self.timer_stats.dataload_duration()

    def train_init(self):
        self.timer_stats.train_init()
        self.test_stats = Metric_stats()
        self.val_stats = Metric_stats()
        
    def train_duration(self):
        self.timer_stats.train_duration()
        
    def epoch_init(self):
        self.timer_stats.epoch_init()
    
    def epoch_duration(self):
        self.timer_stats.epoch_duration()
        
        
    