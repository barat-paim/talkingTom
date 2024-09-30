from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable
from langchain_core.runnables import RunnableSequence, RunnableLambda

load_dotenv()

# Access environment variables
langchain_tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")
langchain_endpoint = os.getenv("LANGCHAIN_ENDPOINT")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
langchain_project = os.getenv("LANGCHAIN_PROJECT")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI model
openai.api_key = openai_api_key
client = wrap_openai(openai.Client())

# Memory to keep track of the conversation
memory = ConversationBufferMemory()

# Define the prompt template of the conversation
template = """
You are a News Anchor. {task}
"""
prompt_template = PromptTemplate(
    input_variables=["task"],
    template=template
)

# Initialize the ChatOpenAI model
llm = ChatOpenAI()

# Define the run_chain function
@traceable
def run_chain(task):
    return llm.invoke({"prompt": prompt_template.format(task=task)})

# Create a RunnableSequence
runnable_sequence = RunnableSequence(
    RunnableLambda(run_chain, task="What's happening in technology?"),
    RunnableLambda(run_chain, task="Wait, tell me a silly joke."),
    RunnableLambda(run_chain, task="What's happening in technology?")
)

# Invoke the sequence
response = runnable_sequence.invoke()
print(response)

#### Define the Intervention Function
def intervention_engine(task, intervertion_task):
    # Step 1: Generate initial response
    print("Original Task: ", task)
    original_response = run_chain(task=task)
    print("Original Response: ", original_response)

    # Step 2: Perfrom the intervention task
    print("\n[Intervention] User: ", intervention_task)
    intervention_resposne = run_chain(task=intervention_task)
    print("Intervention Response: ", intervention_resposne)

    # Step 3: Resume the Original Task
    print("\n[Resume] Well, Continuing from where we left off...")
    resumed_response = run_chain(task=task)
    print("Resumed Response: ", resumed_response)

#### Test the Intervention Engine
if __name__ == "__main__":
    original_task = "Tell me about the latest news in technology."
    intervention_task = "Wait, tell me a silly joke."
    intervention_engine(original_task, intervention_task)