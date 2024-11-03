import os
import streamlit as st
import pandas as pd
from controller.eval_controller import EvalController
from controller.schema_controller import SchemaController
from controller.few_shots_controller import FewShotsController
from controller.api_router_controller import APIRouterController
from llms.general import verify_api_key
from util import constant

# functions
def load_css(css_file):
    """Load and inject CSS from a file."""
    with open(css_file) as f:
        st.html(f'<style>{f.read()}</style>')

@st.dialog("提示")
def show_msg(msg):
    if isinstance(msg, Exception):
        # 提示error messages
        #st.write(msg.__repr__())
        st.write(msg)
    else:
        st.write(msg)

## Loading CSS
css_path = os.path.join(os.path.dirname(__file__), constant.css_dir, 'styles.css')
load_css(css_path)

## loading session data
schema_controller = SchemaController()
if "schemas" not in st.session_state:
    st.session_state.schemas = schema_controller.load_all_schemas()

api_route_controller = APIRouterController()
if "routes" not in st.session_state:
    st.session_state.routes =  api_route_controller.load_api_routes()

if "eval_controller" not in st.session_state:
    st.session_state.eval_controller = EvalController()

few_shot_controller = FewShotsController()
if "few_shots" not in st.session_state:
        st.session_state.few_shots = few_shot_controller.load_few_shots()


## UI
with st.sidebar:
    st.session_state.model = st.selectbox(
        "生成模型：", 
        ('glm-4-plus','glm-4-0520', 'glm-4-flash','glm-4-air','gpt-4o','gpt-4o-mini','qwen-max', 'qwen-plus', 'doubao-pro-32k')
    )
    if st.session_state.model:
        os.environ['MODEL'] = st.session_state.model

    API_KEY = st.text_input("模型API_Key:", placeholder="API_KEY")
    if st.session_state.model in constant.DOUBAO_FAMILY:
        END_POINT = st.text_input("模型接入点", placeholder="接入点名称")
        
    num_of_record = st.number_input("数据条数:", value=1, max_value=len(st.session_state.few_shots), min_value=1)
    st.write(f"我们使用：\n1. **{constant.OPENAI_VERIFIER}** 验证 OpenAI 系列模型； \n2. **{constant.GLM_VERIFIER}** 验证 GLM 系列模型； \n3. **{constant.QWEN_VERIFIER}** 验证 QWEN 系列模型； \n4. **{constant.DOUBAO_VERIFIER}** 验证 DOUBAO 系列模型。")

# Setup tabs    
tab_eval,tab_questionnir = st.tabs(["评估", "问题列表"])
with tab_eval:
    if st.button("开始测评!", type="primary"):
        try:
            if len(API_KEY) == 0 or ('END_POINT' in locals() and len(END_POINT) == 0):
                msg = ""
                if len(API_KEY) == 0: msg += "请提供API Key。"
                if 'END_POINT' in locals() and len(END_POINT) == 0: msg += "请提供模型接入点"
                show_msg(msg)
            else:
                #setup API_KEY
                os.environ['API_KEY'] = API_KEY
                if 'END_POINT' in locals() and len(END_POINT) != 0:
                    os.environ['END_POINT'] = END_POINT
                verify_api_key()
        
                evals = []
                #Proceeding 
                with st.status(f"需要处理{len(st.session_state.few_shots)}条数据...", expanded=False) as status:
                    for i, fs in enumerate(st.session_state.few_shots):
                        if i + 1 > num_of_record: break
                        status.update(label = f"处理{i+1}/{num_of_record}条数据...", state = "running", expanded = False)
                        e = st.session_state.eval_controller.scoring_by_few_shot(fs, st.session_state.schemas, st.session_state.routes, st.session_state.few_shots)
                        evals.append(e)
                    status.update(label="数据处理完成", state="complete", expanded=False)
                if evals and len(evals) > 0:
                    #print(f"长度为:{len(evals)}")
                    st.title(f"{st.session_state['model']}测评结果:")
                    total, corrected, percent = st.session_state.eval_controller.metrics(evals)
                    
                    metric_total = "测评总数:"
                    metric_corrected = "正确条数:"
                    metric_percent = "正确率:"
                    col1, col2, col3 = st.columns(3)
                    col1.metric(label=metric_total, value=total, delta=None)
                    col2.metric(label=metric_corrected, value=corrected, delta=None)
                    col3.metric(label=metric_percent, value=percent, delta=None)

                    df = pd.DataFrame(evals)
                    new_column_order = ['id', 'result', 'question', 's_answer', 'r_answer', 'reason']
                    df_sorted = df[new_column_order]
                    st.dataframe(df_sorted, column_config={
                        "id": "id",
                        "result": "正确",
                        "question": "问题",
                        "s_answer": "正确答案",
                        "r_answer": "大模型答案",
                        "reason": "判定" 
                    }, hide_index=True)
        except Exception as ex:
            show_msg(ex) 
                
with tab_questionnir:
    for i in range(0, len(st.session_state.few_shots), constant.COL_PERROW):
        cols = st.columns(constant.COL_PERROW)
        for j in range(constant.COL_PERROW):
            if i + j < len(st.session_state.few_shots):
                with cols[j]:
                    st.html(f"<div class='query-container'><div class='query-id'>ID: {st.session_state.few_shots[i+j].id}</div><div class='query-question'>{st.session_state.few_shots[i+j].question}</div></div>")
    
    
    
                
