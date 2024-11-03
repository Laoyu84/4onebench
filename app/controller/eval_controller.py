
import json
import traceback
import random
import string
import time
from pathlib import Path

from controller.plan_generator import build,enrich_question
from controller.plan_verifier import verify
from controller.schema_controller import SchemaController
from controller.api_router_controller import APIRouterController
from controller.few_shots_controller import FewShotsController
from models.query import Query
from util.logger import logger
from util import constant

class EvalController:
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent / constant.eval_dir
    
    def scoring_by_few_shot(self, fs, schemas, routes, few_shots):
        try: 
            logger.info(f"处理问题{fs.id}...")
            run_q = Query(fs.question,id=fs.id,question_embeddings=fs.question_embeddings, enriched_embeddings=fs.enriched_embeddings)
            #run_q.set_question_embeddings()
            logger.debug("生成Enriched question:")
            run_q.enriched = enrich_question(run_q, schemas,routes,few_shots)
            #run_q.set_enriched_embeddings()
            logger.debug(run_q.enriched)
            logger.debug("生成Routine:")
            run_q.answer = build(run_q,schemas,routes,few_shots)
            logger.debug(run_q.answer)
            result = verify(fs,schemas,routes,run_q.answer)
            logger.debug(result)
            return {"id": fs.id, 
                            "question": fs.question,
                            "s_enriched": fs.enriched,
                            "s_answer": fs.answer,
                            "r_enriched": run_q.enriched,
                            "r_answer": run_q.answer,
                            "result": result["pass"],
                            "reason": result["reason"] }     
        except Exception as ex:
            logger.error(f"处理问题 {fs.id} 时发生未预期的错误: {ex}")
            logger.info(f"错误详情: {traceback.format_exc()}")
            

    def scoring(self, ids):
        schema_controller = SchemaController()
        schemas = schema_controller.load_all_schemas()
        
        api_route_controller = APIRouterController()
        routes = api_route_controller.load_api_routes()

        few_shots_controller = FewShotsController()
        few_shots = few_shots_controller.load_few_shots()

        evals = []
        for fs in few_shots:
            if fs.id in ids:
                try: 
                    e = self.scoring_by_few_shot(fs, schemas, routes, few_shots)
                    evals.append(e)
                except Exception as e:
                    logger.error(f"处理问题 {fs.id} 时发生未预期的错误: {e}")
                    logger.info(f"错误详情: {traceback.format_exc()}")
                    continue
        if len(evals) > 0:
            self.write_evals(evals)
    
    
    def load_evals(self, model):
        try: 
            eval_filename = model + "-eval.jsonl"
            eval_path = self.config_dir / eval_filename
            evals = []
            with open(eval_path, 'r') as file:
                for line in file:
                    if line.strip():  # Make sure to skip any empty lines
                        item = json.loads(line)
                        #e = Eval(item['id'], item['question'], item['s_enriched'], item['s_answer'],
                        #    item['r_enriched'],item['r_answer'],item['result'], item['reason'])
                        evals.append(item)
            evals = sorted(evals, key=lambda x: x['id'])
            return evals
        except FileNotFoundError:
            logger.info(f"没有找到文件")

    def metrics(self, evals):
        corrected = sum(1 for e in evals if e["result"] is True)
        return len(evals), corrected, str(round(corrected/len(evals)*100,2)) + "%"
    
    def write_evals(self, evals):
        eval_filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.json'
        eval_path = self.config_dir / eval_filename
        
        with open(eval_path, 'w') as file:
            for e in evals:
                json.dump(e, file, ensure_ascii=False)
                file.write('\n')

    def try_api_key(self):
        logger.info("testing!")
