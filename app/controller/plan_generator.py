import os
from tenacity import retry, stop_after_attempt,wait_fixed
from controller.few_shots_controller import FewShotsController
from llms.general import complete
from models.query import Query
from util import constant
from util.logger import logger


ENRICH_SYS = "你说话非常精炼。"

ENRICH_USER = """
请基于Knowledge Graph，改写'我的查询'

## CONSTRAIN
-不要丢失我的查询中任何表名、字段名和值
-不要做过多解释
-不要生成SQL
-严格遵循Knowledge Graph中的给出的规则，不要编造路径
-请在'我的查询'开始增加SOS表示开始
-请在'我的查询'结尾增加EOS表示结束

## Knowledge Graph
{schema}
{routes}

## Examples
{examples}

## 我的查询
Q: {query}
"""
@retry(stop=stop_after_attempt(constant.MAX_RETRY), wait=wait_fixed(1))
def enrich_question(q: Query, schemas, routes, few_shots)->str:
    schema = "\n".join(str(s) for s in schemas)

    #选择合适的few-shot examples
    few_shots_controller = FewShotsController()
    selected_fs, related = few_shots_controller.get_question_few_shots(q,few_shots, bench_mark=0.2)
    logger.debug(f"问题{q.id}使用的{len(selected_fs)}个Few-Shots案例包括:")
    for i, fs in enumerate(selected_fs):
        logger.debug(f"问题{fs.id}.{fs.question}，相关度:{related[i]}")
    
    examples = "".join(f.get_enriched_examples() for f in selected_fs)
    usr_msg = ENRICH_USER.format(
                            query = q.question,
                            schema = schema,
                            routes = str(routes),
                            examples = examples                          
                            )
    return complete(ENRICH_SYS,usr_msg)
    
PLAN_SYS = "你说话非常精炼。"

PLAN_USER = """
请基于Knowledge Graph和Tools，生成'我的查询'的查询路径

## CONSTRAIN
-不要丢失我的查询中任何表名、字段名和值
-不要做过多解释
-不要生成SQL
-严格遵循Knowledge Graph中的给出的规则，不要编造路径
-请在'我的查询'开始增加SOS表示开始
-请在'我的查询'结尾增加EOS表示结束

## Knowledge Graph
{schema}
{routes}

## Tools
1. 总计; 例如，涉案次数:法律文书信息.总计()
2. 合计; 例如: 涉案总额:法律文书信息.合计(涉案金额)
3. 排序;
4. 过滤;
5. 存在;
6. IF...ELSE...;
## Examples
{examples}

## 查询路径
Q: {query}
"""
@retry(stop=stop_after_attempt(constant.MAX_RETRY), wait=wait_fixed(1))
def build(q: Query, schemas, routes, few_shots):
    schema = "\n".join(str(s) for s in schemas)

    few_shots_controller = FewShotsController()
    selected_fs, related = few_shots_controller.get_enriched_few_shots(q,few_shots, bench_mark=0.6)
    logger.debug("该问题使用的Few-Shots案例包括:")
    for i, fs in enumerate(selected_fs):
        logger.debug(f"问题{fs.id}.{fs.question}，相关度:{related[i]}")
    
    examples = "".join(f.get_instructions_examples() for f in selected_fs)
    usr_msg = PLAN_USER.format(
                            query = q.enriched,
                            schema = schema,
                            routes = str(routes),
                            examples = examples                          
                            )
    return complete(PLAN_SYS, usr_msg)
   
