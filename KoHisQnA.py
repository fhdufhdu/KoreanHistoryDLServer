import torch
from transformers import AutoModelForQuestionAnswering, BertForQuestionAnswering
from transformers import BertTokenizer

class KoHisQnA:
    def __init__(self):
        DEFAULT_PATH = '/home/fhdufhdu/vscode/Project/data/models/finetunedModel'
        model_path = DEFAULT_PATH
        tokenizer_path = DEFAULT_PATH
        self.change_path(model_path, tokenizer_path)

    def change_path(self, model_path, tokenizer_path) -> None:
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path

        try:
            del self.model, self.tokenizer
        except:
            print('...initailizing...')

        self.model = BertForQuestionAnswering.from_pretrained(self.model_path, return_dict=True)
        self.tokenizer = BertTokenizer.from_pretrained(self.tokenizer_path)

    def do_ask_to_model(self, question, context, add_special_tokens=True, return_tensors='pt') -> tuple:
        inputs = self.tokenizer.encode_plus(
            question, context, add_special_tokens=add_special_tokens, return_tensors=return_tensors)

        # 모델에 데이터 집어넣기
        outputs = self.model(**inputs)
        answer_start_vector = outputs.start_logits
        answer_end_vector = outputs.end_logits
 
        as_idx = torch.argmax(answer_start_vector)
        ae_idx = torch.argmax(answer_end_vector) + 1

        # 정답을 구하기 위한 과기
        input_ids = inputs["input_ids"].tolist()[0]
        text_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
        answer = self.tokenizer.convert_tokens_to_string(
            text_tokens[as_idx:ae_idx])

        return (int(as_idx), int(ae_idx), answer)