class Eval:
    def __init__(self, id, question, s_enriched, s_answer, r_enriched, r_answer, result, reason): 
        self.id = id
        self.question = question
        self.s_enriched = s_enriched
        self.s_answer = s_answer
        self.r_enriched = r_enriched
        self.r_answer = r_answer
        self.result = bool(result)
        self.reason = reason
    
    def to_dict(self):
        return { "id": self.id,
                "question": self.question, 
                "s_enriched": self.s_enriched, 
                "s_answer": self.s_answer,
                "r_enriched": self.r_enriched, 
                "r_answer": self.r_answer,
                "result": self.result,
                "reason": self.reason
                }
