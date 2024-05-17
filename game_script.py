# Import necessary modules from Cassandra, astrapy, langchain, and OpenAI libraries
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from astrapy import DataAPIClient
from langchain.memory import CassandraChatMessageHistory, ConversationBufferMemory
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

# Initialize DataAPIClient with a provided API token to interact with the database
client = DataAPIClient("AstraCS:XBjfFQetKcnYHsPnpxdOiih:00f0e02dcb8b5f638020af471c6ca94bb808ba2e5641c8c69b1cdcd77cf7ac0a")

# Retrieve database object using its API endpoint
db = client.get_database_by_api_endpoint(
  "https://fc66f5db-c53f-4c0f-a63e-567692b7e67-us-east1.apps.astra.datastax.com"
)

# Establish a session with Cassandra using secure connect bundle and authentication provider
session = Cluster(
    cloud={"secure_connect_bundle": "secure-connect-ai-choose-your-own-adventure-game.zip"},
    auth_provider=PlainTextAuthProvider("token", "AstraCS:XBjfFQetKcnYHXsPnpxdOiih:00fe02dcb8b5f638020af471c6ca94bb808ba2e5641c8c69b1cdcd77cf7ac0a"),
).connect()

# Define the keyspace in Cassandra to use
ASTRA_DB_KEYSPACE = "default_keyspace"

# Set the OpenAI API key for authentication
OPENAI_API_KEY = "sk-proj-6LHXPvIMITTTIu9Mb2h6T3BlbkFJbZV5PEGbzNRIKLynCcC"

# Initialize Cassandra chat message history with a session ID, session, keyspace, and time-to-live for messages
message_history = CassandraChatMessageHistory(
    session_id="session_id",
    session=session,
    keyspace=ASTRA_DB_KEYSPACE,
    ttl_seconds=3600
)

# Clear any previous chat history
message_history.clear()

# Initialize conversation buffer memory using Cassandra chat message history
cass_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history
)

# Define a prompt template for the language model to generate responses based on chat history and user input
template = """
You are now the guide of a mystical journey through the trenches of the Sunken Bride. 
A traveler named Viktor Huke seeks the One Piece. 
You must navigate him through challenges, choices, and consequences, 
dynamically adapting the tale based on the traveler's decisions. 
Your goal is to create a branching narrative experience where each choice 
leads to a new path, ultimately determining Viktor Huke's fate. 

Here are some rules to follow:
1. Start by asking the player to choose some kind of weapons that will be used later in the game
2. Have a few paths that lead to success
3. Have some paths that lead to death. If the user dies generate a response that explains the death and ends in the text: "The End.", I will search for this text to end the game

Here is the chat history, use this to understand what to say next: {chat_history}
Human: {user_input}
AI:"""

# Initialize the prompt template with input variables for chat history and user input
prompt = PromptTemplate(
    input_variables=["chat_history", "user_input"],
    template=template
)

# Initialize OpenAI client with the provided API key
llm = OpenAI(
    api_key=OPENAI_API_KEY
)

# Create an LLMChain instance that ties together the language model, prompt, and memory
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=cass_buff_memory
)

# Set the initial choice to start the game
choice = "start the game"

# Begin a loop to interactively generate responses and take user input
while True:
    # Generate a response from the language model based on the user input
    response = llm_chain.predict(user_input=choice)
    print(response.strip())

    # Check if the response indicates the end of the game
    if "The End." in response:
        break

    # Prompt the user for their next input
    choice = input("Your reply:")

# The following lines are just saved keys and other syntax
# print(f"Connected to Astra DB: {db.list_collection_names()}")
# sk-proj-2hUucpMJFpPQu7msMON7T3BlkFJpfxgvGK5zKZR9QU5mtUc school
# sk-proj-f8jFAT0o2d3UrFnHuNPRT3BlbFJ3whFyRTRFEe7Ua07Viet private
# sk-proj-EmaWLbwvMbiRYDj5fyXKT3BlbkJ03l0gDuzvOVMbthfdhuQ private 2
# sk-proj-6LHXPvIMITTTIu9Mb2h6T3BlbkFbZV5PEGbzNRIKLynCccC game
