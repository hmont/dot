import torch

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

class Classifier:
    def __init__(self):
        self.tokenizer = None
        self.model = None

    def setup(self):
        self.tokenizer = AutoTokenizer.from_pretrained('model')
        self.model = AutoModelForSequenceClassification.from_pretrained('model')

    def predict(self, text) -> int:
        """
        0 = Very Negative
        1 = Negative
        2 = Neutral
        3 = Positive
        4 = Very Positive
        """
        if not self.tokenizer or not self.model:
            raise ValueError("You must setup() the classifier first")

        _input = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = self.model(**_input)

        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return torch.argmax(probabilities, dim=-1).tolist()[0]