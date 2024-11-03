
import os
from tenacity import retry, stop_after_attempt,wait_fixed
from models.query import Query
from llms.general import complete_verify
from util import constant
from util.logger import logger

PLAN_SYS = "你善于验证答案，用Json输出验证结果"

PLAN_USER = """
请基于Knowledge Graph,'我的问题'，验证'我的计划'是否符合'标准答案',并给出你的Reason。

## CONSTRAIN
-请严格遵循Knowledge Graph所规划的关系
-请使用中文

## 我的问题
{question}

## Knowledge Graph
{schema}
{routes}

## Example
1.
- Question:"金都药业的子公司的一级行业是什么?"
- Standard_Answer:
SOS;
a.金都药业的子公司行业一级
[
    1.公司简称:金都药业->上市公司基本信息;
    2.关联上市公司全称:上市公司基本信息.公司名称->子公司关联信息;
    3.公司名称:子公司关联信息.公司名称->公司工商照面信息;
    4.行业一级:公司工商照面信息.行业一级;
];
EOS;
- My_Answer:
SOS;
a.金都药业的子公司及行业信息
[
    1.公司简称:金都药业->上市公司基本信息;
    2.公司名称:上市公司基本信息.公司名称->子公司关联信息;
    3.公司名称:子公司关联信息.公司名称->公司工商照面信息;
    4.行业一级:公司工商照面信息.行业一级;
];
EOS;
- Evaluation:
{{"pass":false,"reason": "在我的计划中，步骤2使用了公司名称:上市公司基本信息.公司名称->子公司关联信息，而标准答案中使用的是关联上市公司全称:上市公司基本信息.公司名称->子公司关联信息。两者在查询子公司关联信息时使用的属性不同，因此不符合标准答案。"}}

2.
- Question: 审理(2019)川0129民初1361号案件的法院名称是哪个法院，地址在什么地方
- Standard_Answer:
SOS;
a.北京市密云区人民法院的区县区划代码
[
    1.法院名称:北京市密云区人民法院->法院基础信息;
    2.地址:法院基础信息.法院地址->通用地址省市区信息;
    3.省份:通用地址省市区信息.省份,城市:通用地址省市区信息.城市,区县:通用地址省市区信息.区县->通用地址编码;
    4.区县区划代码:通用地址编码.区县区划代码;
];
EOS;
- My Answer:
SOS;
a.北京市密云区人民法院的区县区划代码
[
    1.法院名称:北京市密云区人民法院->法院地址代字信息;
    2.地址:法院地址代字信息.法院地址->通用地址省市区信息;
    3.区县:通用地址省市区信息.区县->通用地址编码;
    4.区县区划代码:通用地址编码.区县区划代码;
];
EOS;
- Evaluation:
{{"pass":false,"reason": "1.在我的计划中，使用了法院地址代字信息来获取法院地址，而根据Knowledge Graph，应该使用法院基础信息来获取法院地址。2.查询通用地址编码应同时使用省份,城市,区县三个条件。"}}

3.
- Question: 天通股份的参保人数有多少人？
- Standard_Answer:
SOS;
a.天通股份的参保人数
[
    1.公司简称:天通股份->上市公司基本信息;
    2.公司名称:上市公司基本信息.公司名称->公司工商照面信息;
    3.参保人数:公司工商照面信息.参保人数;
];
EOS;
- My Answer:
SOS;
a.天通股份的工商照面信息
[
  1.公司名称:天通股份->公司工商照面信息;
  2.参保人数:公司工商照面信息.参保人数;
];
EOS;
- Evaluation:
{{"pass":false,"reason": "根据Knowledge Graph，我的计划中直接使用公司名称查询公司工商照面信息的步骤不符合标准答案的流程。标准答案要求先通过公司简称查询上市公司基本信息，然后再通过上市公司基本信息中的公司名称查询公司工商照面信息。我的计划缺少了这一步骤，因此不符合标准答案。"}}

## 标准答案
{standardanswer}

## 我的计划
{myanswer}

## 结果
{{'pass':True/False,'reason': '...'}}
"""
@retry(stop=stop_after_attempt(constant.MAX_RETRY), wait=wait_fixed(1))
def verify(q: Query, schemas, routes, myanswer):
    schema = "\n".join(str(s) for s in schemas)
    usr_msg = PLAN_USER.format(question = q.question,
                            schema = schema,
                            routes = str(routes),
                            standardanswer = q.answer,
                            myanswer = myanswer                        
                            )
    return complete_verify(PLAN_SYS, usr_msg)
    

