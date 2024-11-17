# -*- coding: utf-8 -*-
"""1_Langchain_And_Huggingface C2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mLWPX7wlSaaHetricCcWjbYIu5fmXkt8

# Huggingface With Langchain

Announcement Link: https://huggingface.co/blog/langchain
"""

## Libraries Required
!pip install langchain-huggingface
## For API Calls
!pip install huggingface_hub
!pip install transformers
!pip install accelerate
!pip install  bitsandbytes
!pip install langchain

## Environment secret keys
from google.colab import userdata
sec_key=userdata.get("HF_TOKEN")

"""## HuggingFaceEndpoint
## How to Access HuggingFace Models with API
There are also two ways to use this class. You can specify the model with the repo_id parameter. Those endpoints use the serverless API, which is particularly beneficial to people using pro accounts or enterprise hub. Still, regular users can already have access to a fair amount of request by connecting with their HF token in the environment where they are executing the code.

"""

from langchain_huggingface import HuggingFaceEndpoint

from google.colab import userdata
sec_key=userdata.get("HUGGINGFACEHUB_API_TOKEN")

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"]=sec_key

repo_id="mistralai/Mistral-7B-Instruct-v0.2"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,token=sec_key)

llm.invoke("What are LLM")

repo_id="mistralai/Mistral-7B-Instruct-v0.3"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,token=sec_key)

llm.invoke("What are transformers")

from langchain import PromptTemplate, LLMChain

question="Who is the best footballer ?"
template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
print(prompt)

llm_chain=LLMChain(llm=llm,prompt=prompt)
print(llm_chain.invoke(question))

"""## HuggingFacePipeline
Among transformers, the Pipeline is the most versatile tool in the Hugging Face toolbox. LangChain being designed primarily to address RAG and Agent use cases, the scope of the pipeline here is reduced to the following text-centric tasks: “text-generation", “text2text-generation", “summarization”, “translation”.
Models can be loaded directly with the from_model_id method

"""

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_id="gpt2"
model=AutoModelForCausalLM.from_pretrained(model_id)
tokenizer=AutoTokenizer.from_pretrained(model_id)

pipe=pipeline("text-generation",model=model,tokenizer=tokenizer,max_new_tokens=100)
hf=HuggingFacePipeline(pipeline=pipe)

hf

hf.invoke("What is deep learning")

## Use HuggingfacePipelines With Gpu
gpu_llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    device=0,  # replace with device_map="auto" to use the accelerate library.
    pipeline_kwargs={"max_new_tokens": 100},
)

from langchain_core.prompts import PromptTemplate

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

chain=prompt|gpu_llm

question="What is artificial intelligence?"
chain.invoke({"question":question})

