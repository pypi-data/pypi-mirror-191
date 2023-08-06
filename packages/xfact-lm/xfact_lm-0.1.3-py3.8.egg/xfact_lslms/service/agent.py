import logging
import json
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from xfact_lslms.log_helper import setup_logging
from xfact_lslms.service.amq_communications import CommunicationLayer

logger = logging.getLogger(__name__)

class LanguageModelAgent():
    def __init__(self, model_path, device='cuda'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(device)
        self.model.eval()
        self.device = device

    def infer(self, text, tokenizer_kwargs, generate_kwargs):
        toks = self.tokenizer(text, return_tensors="pt", **tokenizer_kwargs)
        ids = toks["input_ids"].to(self.device)
        outs = self.model.generate(input_ids=ids, **generate_kwargs).cpu()
        prediction = self.tokenizer.batch_decode(outs, skip_special_tokens=True)

        logger.info(f"Predicting on {text}")
        logger.info(f"Predicted {prediction}")

        return {
            "input_text": text,
            "decoded_text": prediction
        }


if __name__ == "__main__":
    setup_logging()
    lm = LanguageModelAgent("google/flan-t5-xl")
    comms = CommunicationLayer("lm", lambda message: lm.infer(**message))
    comms.listen()

