# 4onebench
Routine-Gen is a crucial part for LLM-based agents, enabling them to effectively orchestrate IT assets, such as APIs, to accomplish tasks. 
![Flow of LLMs-based Agent](images/arch-1.png)
However, there is a lack of systems to evaluate the effectiveness of LLMs in routine generation in a business context. 

The purpose of **4-One Bench** is to create a lightweight evaluation system that can help users quickly assess the Routine-Gen capabilities of LLMs. 

## Evaluation
We have conducted an evaluation of models from OpenAI, Zhipu, Ali Cloud, and Doubao. Below are the results regarding their Routine-Gen accuracy:
![Flow of LLMs-based Agent](images/eval_result.png)

## Features and Architecture
The architecture of 4-One Bench utilize a **Generator-Verifier** design pattern. In this setup, the **Generator** converts tasks into routines based on predefined knowledge graphs , while the **Verifier** employs LLMs to validate generated routines  

Furthermore, the evaluation system has 4 "One" features:

![Flow of LLMs-based Agent](images/arch-2.png)

### One-Query
Our dataset includes 51 "one-sentence tasks". 

### One-Knowledge Graph
Based on the tasks, a knowledge graph that describes IT asset relationships will guide LLMs to generate routines. Additionally, users can define their own knowledge graph.

### One-Shot
Considering the critical factors of response time and accuracy in real business environments, 4-One Bench only evaluates the likelihood that LLMs can successfully generate a Routine in a single attempt.

### One-Syntax
4-One Bench has developed a proprietary syntax for defining the orchestration of IT assets. Users also have the flexibility to create their own custom syntax.
![Syntax](images/syntax.png)

## LLMs Supported
1. OpenAI: gpt-4o, gpt-4o-mini; 
2. Zhipu: glm-4-plus, glm-4-0520, glm-4-flash, glm-4-air;
3. Ali Cloud: qwen-max, qwen-plus
4. Bytedance: doubao-pro-32k
5. Deepseek: deepseek-chat 
## Demo

## Launch the evaluation
1. Create and activate a new virtual environment 
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Use the following script to launch the evaluation:

```bash
streamlit run app/app.py
```

## Contact
Follow my public WeChat account to stay updated:

![qr_code](images/qr_code.jpg)

or send email to uncleyu89@gmail.com for any questions.
## License

This project is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for details.
