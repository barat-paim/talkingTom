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
    prompt = prompt_template.format(task=task)
    return llm.invoke(prompt)

# Conversation state
is_paused = False
last_response = ""

def handle_user_input(user_input):
    global is_paused, last_response

    if "wait" in user_input.lower():
        is_paused = True
        return "No problem, take your time."

    if "sorry" in user_input.lower() and "interrupted" in user_input.lower():
        is_paused = False
        return f"As I was mentioning, {last_response}"

    if is_paused:
        return "I understand. Let me know when you're ready to continue."

    # Generate response for the new task
    response = run_chain(task=user_input)
    last_response = response.content.strip()
    return last_response

#### Test the Conversation Flow
if __name__ == "__main__":
    user_inputs = [
        "What is the latest news about AI in cancer research?",
        "Wait a second, someone’s calling me.",
        "My wife wants me to fix the ceiling fan.",
        "You were saying, sorry I interrupted."
    ]

    for user_input in user_inputs:
        print(f"User: {user_input}")
        ai_response = handle_user_input(user_input)
        print(f"AI: {ai_response}")