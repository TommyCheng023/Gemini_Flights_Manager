# Gemini Flight Manager

## Overview

Gemini Flight Manager is a comprehensive backend system built using FastAPI, designed for managing and simulating flight-related operations. This system provides a robust platform for handling various aspects of flight management, including flight generation, search, and booking functionalities.

The project leverages FastAPI's efficient and easy-to-use framework to create a high-performance, scalable solution ideal for flight data management. It comes equipped with an SQLite database (`flights.db`) pre-populated with initial data, allowing for quick deployment and testing.

Key features of Gemini Flight Manager include:
- Advanced search capabilities to query flights based on criteria like origin, destination, and dates.
- Booking system that handles seat availability across different classes and calculates costs accordingly.

Designed with extensibility and scalability in mind, Gemini Flight Manager is well-suited for both educational purposes and as a foundation for more complex flight management applications.

**For the purposes of Gemini Function Calling, you will only need `search_flights` and `book_flight` functions.**

## Installation

### Prerequisites
Before you begin, ensure you have the following installed on your system:
- Python 3.6 or higher
- FastAPI
- Uvicorn, an ASGI server for FastAPI

## Virtual Environment Setup
### build and activate an environment
```bash
python3 -m venv env
source env/bin/activate
```
### install dependencies
The repository provides `requirements.txt`, install by the following command.
```bash
pip install -r requirements.txt
```

## Launch the FastAPI Server
### Run Command
After the installation, you can start the FastAPI server using Uvicorn. Navigate to the project directory and run:

```bash
uvicorn main:app
```

### Accessory
With the server running, you can access the API at `http://127.0.0.1:8000.`

For interactive API documentation, visit `http://127.0.0.1:8000/docs`, where you can test the API endpoints directly from your browser.
