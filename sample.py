import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Tool, Part, Content, ChatSession
from services.flight_manager import search_flights
import os
os.environ['GRPC_DNS_RESOLVER'] = 'native'

project = "gemini-flights-417016"
try:
    vertexai.init( project = project )
except Exception as e:
    st.error(f"Failed to initialize Vertex AI: {e}")
    st.stop()

# Define Tool - Search Flights
get_search_flights = generative_models.FunctionDeclaration(
    name="get_search_flights",
    description="Tool for searching a flight with origin, destination, and departure date",
    parameters={
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "The airport of departure for the flight given in airport code such as LAX, SFO, BOS, etc."
            },
            "destination": {
                "type": "string",
                "description": "The airport of destination for the flight given in airport code such as LAX, SFO, BOS, etc."
            },
            "departure_date": {
                "type": "string",
                "format": "date",
                "description": "The date of departure for the flight in YYYY-MM-DD format"
            },
        },
        "required": [
            "origin",
            "destination",
            "departure_date"
        ]
    },
)

# Define Tool - Book Flights
get_book_flights = generative_models.FunctionDeclaration(
    name="get_book_flights",
    description="Tool for booking a flight with flight_id, seat_type and number of seats, which is optional.",
    parameters={
        "type": "object",
        "properties": {
            "flight_id": {
                "type": "integer",
                "description": "A unique integer representing the flight such as 23, 100, 5, etc., entered by the user."
            },
            "seat_type": {
                "type": "string",
                "description": "There're three possible inputs for this category: economy, business, first-class."
            },
        },
        "required": [
            "flight_id",
            "seat_type"
        ]
    },
)

# Define tool and model with tools
search_tool = generative_models.Tool(
    function_declarations=[get_search_flights, get_book_flights],
)

config = generative_models.GenerationConfig(temperature=0.4)
# Load model with config
try: 
    model = GenerativeModel(
        "gemini-pro", 
        tools = [search_tool],
        generation_config = config
    )
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# helper function to unpack responses
def handle_response(response):
    
    # check if there's a function call
    if response.candidates[0].content.parts[0].function_call.args:
        # function call exists, unpack and load into a function
        response_args = response.candidates[0].content.parts[0].function_call.args
        
        # package into a dictionary
        function_params = {}
        for key in response_args:
            value = response_args[key]
            function_params[key] = value
        
        # unpack the dictionary and pass in the tool
        results = search_flights(**function_params)
        
        # condition: a success in actual response in the FastAPI server
        if results:
            intermediate_response = chat.send_message(
                # send that back to Google Gemini
                Part.from_function_response(
                    name="get_search_flights",
                    response = results
                )
            )
            
            return intermediate_response.candidates[0].content.parts[0].text
        else:
            return "Search Failed"
    else:
        # return just text
        return response.candidates[0].content.parts[0].text

# helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    try:
        response = chat.send_message(query) # chat.send_message(): invoke Google Gemini by sending the parameter
        output = handle_response(response) # call handle_respons() to GET an output
    except Exception as e:
        st.error(f"Failed to send message or receive response: {e}")
        return
    
    with st.chat_message("model"):
        # tell streamlit to create an 'output' text and then applying that to the ChatSession
        st.markdown(output)
    st.session_state.messages.append(
        {
            # append into the session memory that the user has made a query
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            # append the model output
            "role": "model",
            "content": output
        }
    )

# make the page
st.title("Gemini Flights")
try:
    chat = model.start_chat()
except Exception as e:
    st.error(f"Failed to start chat session: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for index, message in enumerate(st.session_state.messages):
    content = Content(
            role = message["role"],
            parts = [ Part.from_text(message["content"]) ]
        )
    
    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat.history.append(content)

if len(st.session_state.messages) == 0:
    # Invoke initial message
    initial_prompt = "Introduce yourself as a flights management assistant, Sir Gemini, powered by Google Gemini and designed to search/book flights. You use emojis to be interactive. For reference, the year for dates is 2024"

    llm_function(chat, initial_prompt)

query = st.chat_input("Check your flights...")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)
