# Gemini Flight Manager

## Overview

Gemini Flight Manager is <ins>a comprehensive backend system built using FastAPI, designed for managing and simulating flight-related operations</ins>. This system provides a robust platform for handling various aspects of flight management, including flight generation, search, and booking functionalities.

The project leverages FastAPI's **efficient and easy-to-use framework** to create <ins>a high-performance, scalable solution ideal for flight data management</ins>. It comes equipped with an SQLite database (`flights.db`) pre-populated with initial data, allowing for quick deployment and testing.

Key features of Gemini Flight Manager include:
- Advanced search capabilities to query flights based on criteria like origin, destination, and dates.
- Booking system that handles seat availability across different classes and calculates costs accordingly.

Designed with extensibility and scalability in mind, Gemini Flight Manager is well-suited for both educational purposes and as a foundation for more complex flight management applications.

**For the purposes of Gemini Function Calling, you will only need `search_flights` and `book_flight` functions.**

## Demo
- A direct testing on the API endpoints.

https://github.com/TommyCheng023/Gemini_Flights/assets/115842289/bbb33dce-4e67-4680-9d41-9c69a086f96e

- A brief conversation with `Sir Gemini` to book a plane ticket.

https://github.com/TommyCheng023/Gemini_Flights/assets/115842289/b6e31421-b5ec-4e68-80c8-84f6badafe97

---
## Introduction - Content
0. Basic Setup
1. Functionality
2. Self-insight
3. Run The App
4. Appendix
---

## 0. Basic Setup
### Prerequisites
Before you begin, ensure you have the following installed on your system:
- Python 3.6 or higher
- Visual Studio Code (recommended)
- FastAPI
- Uvicorn, an ASGI server for FastAPI
- Google Cloud Platform
  - view specific instructions in my other repository [Gemini Explorer](https://github.com/TommyCheng023/Gemini_Explorer)

### Virtual Environment Setup
- build and activate an environment
```bash
python3 -m venv env
source env/bin/activate
```
### Install Dependencies
The repository provides `requirements.txt`, install by the following command.
```bash
pip install -r requirements.txt
```

### Test Your FastAPI Server
After the installation, you can start the FastAPI server using `uvicorn`. Navigate to the project directory and run:
```bash
uvicorn main:app --reload
```

### Accessory
With the server running, you can access the API at `http://127.0.0.1:8000.`. 

**For interactive API documentation, visit `http://127.0.0.1:8000/docs`, where you can test the API endpoints directly from your browser.**

## 1. Functionality
- The basic settings of the chatbot `Sir Gemini` is similar to what I have done in another project [Gemini Explorer](https://github.com/TommyCheng023/Gemini_Explorer).
  - `llm_function()`
  - way to build a vertexAI project
### Add Features
Our Gemini Flights Manager has two main features: search for flights and book a tickets for flights, both returning JSON objects. Checkout the methods in `services/flight_manager.py`.
- `search_flights()`: The function sends a **GET** request to a FastAPI endpoint to search for flights based on various criteria.
  - related object: `FlightSearchCriteria` from `models.py` as the function parameter
- `book_flight()`: The function sends a **POST** request to a FastAPI endpoint to book for flights based on various criteria.
  - related object: `FlightBookCriteria` from `models.py` as the function parameter

Criterias are classes listing all required and optional keys with their specified variable type as well as the default value. When testing the API endpoints, you can see them

### Chatbot Improvement
There's a new method that improves `Sir Gemini`'s quality of feedback after getting results from the database.

- `handle_response()`: This function is replacing the default method dealing with the output of `chat.send_message()` in order to connect the streamlit app with our special job - check the flights. Starting with an understandable `if` statement, we are taking `search_flights()` as a helper function passing in the temporary criteria generated from the parameter. While the output will be sent back to Google Gemini through another `chat.send_message()` call.

- `llm_function()`: The only change in this helper function is to pass in the response into our `handle_response()` method.


### Define Tools
This step is done at the file creating the chat interface (`sample.py` in this case). 

We got `search_flights()` and `book_flight()` needed to be declared using `FunctionDeclaration()` from `generative_models`.

Here's a brief tutorial:
```python
import vertexai
from vertexai.preview import generative_models
variable = generative_models.FunctionDeclaration (
  name = "something-in-string",   # The name of the function the model can call,
  description = "blablabla"       # Optional but necessary. The string describes the purpose of the function.
  parameters = {"type": "object"},   # Describe the parameters to this function in JSON format.
)
# Those attributes are separated by commas.
```
After that, we need to collect the declared functions into the `Tool` class.
```python
yourTool = generative_models.Tool(
  function_declarations = [functionOne, functionTwo]  # collect them in an array
)
```
Finally, we need to load the model with config. There's only one extra line to be added when loading with `GenerativeModel`.
```python
# enable the tools
tools = [yourTool]
```

## 2. Self-insight
### Modification in `handle_flight_book()`
In the old version of this function, its header is:
```python
def handle_flight_book(flight_number:str, seat_type: str , num_seats: int = 1, flight_id: int = None, db: Session = Depends(get_db)):
```
This is quite massive and inconvenient because if the feature needs a big number of keys as the parameter, the header will be too long and hard to edit. You also need to update the inputs in `main.py`.

Therefore, I replace the parameters with <ins>criteria and db</ins> only and change the input into `criteria: models.FlightBookCriteria = Depends()`.

This is more convenient because you can simply update the criteria in `models.py` and you can access to the key through dot notations.

- new version of the function
<img width="1219" alt="Screen Shot 2024-03-13 at 10 19 42 PM" src="https://github.com/TommyCheng023/Gemini_Flights/assets/115842289/369b86a4-7780-4fcb-ba4a-28ec9ba45231">

- test its performance
<img width="1438" alt="Screen Shot 2024-03-13 at 10 16 19 PM" src="https://github.com/TommyCheng023/Gemini_Flights/assets/115842289/a0b1484d-ea89-4cd4-b64d-1d429b84002a">

### Common Issue Solution
1. Sometimes you may encounter `import (package) not resolved` error especially in either `tool.ipynb` or `sample.py`. There're two methods for you to check with.
  - For macOS, press `command+shit+P` on the keyboard and search for `Python: Select Interpreter`, switch to the recommended one.
  - For macOS, press `command+shit+P` on the keyboard and search for `Developer: Reload Windows`, click on it and wait.

## 3. Run The App
To chat with `Sir Gemini`, get prepare with two terminals.

For the first terminal, type the following command to activate the API server:
```zsh
uvicorn main:app --reload
```
For the second terminal, type the following command to run the streamlit app:
```zsh
streamlit run sample.py
```

## 4. Appendix
### Project Certificate
<img width="1004" alt="Screen Shot 2024-03-14 at 4 26 02 PM" src="https://github.com/TommyCheng023/Gemini_Flights_Manager/assets/115842289/f28c6236-be4e-4d1b-9d85-8916b501f6d1">

### Project Report
[Loom Video](https://www.loom.com/share/bfec733a869948ad83cd209b658dac3b?sid=1374e828-9598-4ef1-be2d-8695a5e91f37)

### Appreciation
- Appreciate Radical AI for providing such a precious experience on AI engineering and backend development.
- I also want to show my gratitude to Talha Sabri and Mikhail Ocampo for detailed instructions.
### About Contributors
- Mikhail Ocampo
  - GitHub Profile: [Mikhail.io](https://github.com/Vy-X-S)
- Xinyang(Tommy) Cheng
  - Personal Website: [About - Xinyang Cheng](https://tommycheng023.github.io/)
  - LinkedIn Profile: [Xinyang(Tommy) Cheng](www.linkedin.com/in/xinyang-cheng-325825260)
### What is JSON?
JSON stands for `JavaScript Object Notation`, which is a lightweight data interchange format that's **easy to read and write for humans and easy to parse and generate for machines**.

Sample Structure:
```JSON
{
  "name": "John Doe",
  "age": 30,
  "isEmployed": true,
  "address": {
    "street": "123 Main St",
    "city": "Anytown"
  },
  "phoneNumbers": [
    {
      "type": "home",
      "number": "123-456-7890"
    },
    {
      "type": "mobile",
      "number": "098-765-4321"
    }
  ]
}
```
