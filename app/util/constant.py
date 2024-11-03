## GLM Models
GLM4PLUS = "glm-4-plus"
GLM40520 = "glm-4-0520"
GLM4 = "glm-4"
GLM4AIR = "glm-4-air"
GLM4FLASH = "glm-4-flash"
EMBEDDING = "embedding-2"
GLM_VERIFIER =GLM40520
GLM_FAMILY = [GLM4PLUS,GLM40520,GLM4,GLM4AIR,GLM4FLASH]

## OpenAI Models
GPT4O = "gpt-4o"
GPT4OMINI = "gpt-4o-mini"
OPENAI_VERIFIER = GPT4O
OPENAI_FAMILY= [GPT4O,GPT4OMINI]
## QWEN
QWENMAX = "qwen-max"
QWENPLUS = "qwen-plus"
QWEN_VERIFIER = QWENMAX
QWEN_FAMILY = [QWENMAX,QWENPLUS]

#DOUBAO
DOUBAOPRO32K = "doubao-pro-32k"
DOUBAO_VERIFIER = DOUBAOPRO32K
DOUBAO_FAMILY = [DOUBAOPRO32K]

DEFAULT_MODEL = GLM4PLUS

MAX_RETRY = 3
log_path = "logs/"
config_path = "config/"
few_shot_dir = "few_shots"
embeddings_dir = "embeddings"
eval_dir = "eval"
css_dir = "css"

# UI
COL_PERROW = 4



