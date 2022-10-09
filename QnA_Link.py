from elasticsearch import Elasticsearch
from konlpy.tag import Mecab
from KoHisQnA import KoHisQnA

# 검색어
class KoHisQnALink:
    def __init__(self):
        self.es = Elasticsearch("http://202.31.202.147:9200")
        self.qa = KoHisQnA()

    def get_qna_result(self, question):
        search_sentence = question
        mecab_tokenizer = Mecab()
        nouns_list = mecab_tokenizer.nouns(search_sentence)

        resultDict = {"result":[]}

        for noun in nouns_list:
            docs = self.es.search(index='history_dict',
                            body={
                                "size": 2,
                                "query": {
                                    "multi_match": {
                                        "query": noun,
                                        "fields": ["title", "intro", "content", "search"]
                                    }
                                }
                            })

            for doc in docs['hits']['hits']:
                context = doc['_source']['document']
                for i in range(int((len(doc) / 500)) + 1):
                    temp_context = context[500*i:500*(i+1)-1]
                    answer = self.qa.do_ask_to_model(search_sentence, temp_context)
                    temp_context = temp_context.split(".")
                    answer_context = ''
                    for j in range(len(temp_context) - 1):
                        answer_context = answer_context + temp_context[j] + '.'

                    resultDict["result"].append({"answer" : answer[2],
                                                    "ContextWithAsnwer": answer_context,
                                                    "question":question})

        return resultDict