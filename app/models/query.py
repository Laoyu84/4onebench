
from llms.zhipu import get_embeddings
class Query: 
    def __init__(self, question, id=0, enriched="", answer="", question_embeddings=[], enriched_embeddings=[]):
        
        self.id = id
        self.question = question
        self.enriched = enriched
        self.answer = answer
        if len(question_embeddings):
            self.question_embeddings = question_embeddings
        else:
            self.question_embeddings = []
        
        if len(enriched_embeddings) > 0:
            self.enriched_embeddings = enriched_embeddings
        else:
            self.enriched_embeddings = []
    
    def set_question_embeddings(self):
        self.question_embeddings = get_embeddings(self.question)

    def set_enriched_embeddings(self):
        if len(self.enriched) > 0:
            self.enriched_embeddings = get_embeddings(self.enriched)

    def get_enriched_examples(self):
        return f"Q:{self.question}\n\nA:{self.enriched}"
    
    def get_instructions_examples(self):
        return f"Q:{self.enriched}\n\nA:{self.answer}"

    def to_yaml_dict(self):
        return { "question": self.question, "enriched": self.enriched, "id": self.id,"answer": self.answer}
    
    def to_embedding_dict(self):
        return {"id": self.id, "question": self.question,"enriched": self.enriched,"question_embeddings": self.question_embeddings, "enriched_embeddings": self.enriched_embeddings}
    