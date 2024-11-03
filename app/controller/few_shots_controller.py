import os
import yaml
import json
from pathlib import Path
from scipy import spatial

from models.query import Query
from util import constant

class FewShotsController:
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent / 'config'

    def get_question_few_shots(self, 
                    q: Query, 
                    few_shots,
                    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
                    top_n: int = 10,
                    bench_mark = 0.40):
        fs_and_relatednesses = [
            (s, relatedness_fn(q.question_embeddings, s.question_embeddings))
            for i, s in enumerate(few_shots) if str(s.id) != str(q.id) and relatedness_fn(q.question_embeddings, s.question_embeddings) >= bench_mark
            #only return those with high related records.
        ]

        if not fs_and_relatednesses:
            return [], []
        #sort by relatednesses
        fs_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
        selected_fs, relatednesses = zip(*fs_and_relatednesses)
        return selected_fs[0:top_n], relatednesses[0:top_n]

    def get_enriched_few_shots(self, 
                    q:Query, 
                    few_shots,
                    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
                    top_n: int = 10,
                    bench_mark = 0.40):
        fs_and_relatednesses = [
            (s, relatedness_fn(q.enriched_embeddings, s.enriched_embeddings))
            for i, s in enumerate(few_shots) if str(s.id) != str(q.id) and relatedness_fn(q.enriched_embeddings, s.enriched_embeddings) >= bench_mark
            #only return those with high related records.
        ]
        
        if not fs_and_relatednesses:
            return [], []
        #sort by relatednesses
        fs_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
        selected_fs, relatednesses = zip(*fs_and_relatednesses)
        return selected_fs[0:top_n], relatednesses[0:top_n]
    
    def load_few_shots(self):
        few_shots_yaml_path = self.config_dir / constant.few_shot_dir 
        few_shots_folders = os.listdir(few_shots_yaml_path)
        yaml_files = [file for file in few_shots_folders if file.endswith('.yaml')]

        few_shots = []
        for yaml_file in yaml_files:
            # loading examples as a list of Query from few_shots folder 
            file_path = os.path.join(few_shots_yaml_path, yaml_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                few_shots.append(Query(data['question'],
                                       id=data['id'], 
                                       enriched=data['enriched'], 
                                       answer=data['answer']))
        
        for s in few_shots:
            #loading embeddings from the embedding folder
            item = self.load_few_shots_embeddings(s.id)
            if item:
                s.question_embeddings = item['question_embeddings']
                s.enriched_embeddings = item['enriched_embeddings']
        few_shots = sorted(few_shots, key=lambda x: x.id)
        return few_shots
    
    def load_few_shots_embeddings(self, id):
        # loading embeddings
        few_shot_embeddings_path = self.config_dir / constant.embeddings_dir / f"{id}.json"
        try:
            with open(few_shot_embeddings_path, 'r') as file:
                item = json.load(file)
                return item 
        except Exception as e:
            return []
    
    def write_few_shots(self, q: Query):
        few_shot_embeddings_path = self.config_dir / constant.few_shot_dir / f"{q.id}.yaml"
        with open(few_shot_embeddings_path, 'w', encoding='utf-8') as file:
            yaml.dump(q.to_yaml_dict(), file, allow_unicode=True, default_flow_style=False)
            file.write('\n')
    

    def write_few_shots_embeddings(self, q: Query):
        few_shot_embeddings_path = self.config_dir / constant.embeddings_dir / f"{q.id}.json"
        with open(few_shot_embeddings_path, 'w') as file:
            json.dump(q.to_embedding_dict(), file, ensure_ascii=False)
            file.write('\n')

    """
    def convert_few_shots_to_query(self, id)->Query:
        few_shots_path = self.config_dir / 'few_shots' / f"{id}.yaml"
        with open(few_shots_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            #load embeddings
            embeddings = self.load_few_shots_embeddings(id)
            q = Query(data['question'],
                      id=id,
                      enriched=data['enriched'],
                      answer=data['answer'],
                      question_embeddings=embeddings['question_embeddings'],
                      enriched_embeddings=embeddings['enriched_embeddings'])
            return q

    """
    
