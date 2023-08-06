import os
from pathlib import Path
from typing import Union, List

import torch

from nanoQA.components.question_answering.handlers.train import handle_adapter_training
from nanoQA.components.question_answering.reader.base import BaseReader
from nanoQA.schemas import AdapterTrainingArguments


class ReaderWithAdapter(BaseReader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_adapter(self, adapter_location: Union[str, Path]):
        if isinstance(adapter_location, Path):
            adapter_location = str(adapter_location)
        adapter_name = self.model.load_adapter(adapter_location, with_head=False)
        self.model.qa_outputs.load_state_dict(
            torch.load(torch.load(os.path.join(adapter_location, "qa_outputs.bin")))
        )
        self.model.set_active_adapters([adapter_name])
        if self.use_gpu and torch.cuda.is_available():
            self.model.cuda()

    def delete_all_adapters(self, adapter_names: List[str]):
        if adapter_names:
            for adapter_name in adapter_names:
                self.model.delete_adapter(adapter_name)
        self.model.set_active_adapters(None)

    def train(self, training_args: AdapterTrainingArguments):
        # delete adapter name if exists
        self.delete_all_adapters([training_args.adapter_name])
        # add fresh adapter layers, and set it as active
        self.model.add_adapter(training_args.adapter_name)
        self.model.train_adapter(training_args.adapter_name)
        self.model.set_active_adapters([training_args.adapter_name])

        handle_adapter_training(
            model=self.model,
            tokenizer=self.tokenizer,
            data_dir=training_args.data_dir,
            train_filename=training_args.train_filename,
            max_seq_len=training_args.max_seq_len,
            doc_stride=training_args.doc_stride,
            learning_rate=training_args.learning_rate,
            batch_size=training_args.batch_size,
            n_epochs=training_args.n_epochs,
        )

        # save the adapter layers and prediction head.
        self.model.save_adapter(
            save_directory=training_args.save_dir,
            adapter_name=training_args.adapter_name,
            with_head=False,
        )
        prediction_head = self.model.qa_outputs
        torch.save(prediction_head.state_dict(), os.path.join(training_args.save_dir, "qa_outputs.bin"))
