# LLM-Web-Scraping

**Python Version**:3.11

<details>
  <summary><b> Streamlit Frontend</b></summary>

The code for the streamlit frontend is available [here](https://github.com/rukshar/LLM-Web-Scraping/tree/main/streamlit_frontend/scraper_ui.py).

The frontend has 2 fields: 
- URL text input field
- Attributes list input field

Upon clicking the **Extract Attributes** button, the script sends a POST request to a FastAPI API(*ttp://127.0.0.1:8000/extract*) endpoint with the provided URL and attributes.

![frontend](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/streamlit_frontend/frontend.png)

The JSON response from the API is then displayed in the frontend. 

**Fault tolerance** is ensured by keeping the FastAPI API calling logic within try-except blocks. The script displays an error message if the API call fails and the except block handles the error.

## Running the Frontend

Create an Anaconda virtual environment with the following command:
```bash
conda create -n streamlit python=3.11
```

Activate the virtual environment with the following command:
```bash
conda activate streamlit
```

Install the required packages from the requirements.txt file with the following command:
```bash
pip install -r requirements_frontend.txt
```

To run the frontend, run the following command in the terminal:
```bash
streamlit run scraper_ui.py
```

The app runs on the address **http://127.0.0.1:8501**

</details>

<details>
<summary><b> OpenAI + LangChain + FastAPI Backend
</b></summary>

![Diagram](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/openai_backend/web_scrape_llm.jpg)


## FastAPI API

The FastAPI API(*/extract*) is a RESTful API that takes a URL and a list of attribute names as input and returns the extracted attributes from the webpage after calling a method **scrape_with_playwright** that takes input the URL, the list of attribute names and the LLM. The LLM is set to OpenAI's **gpt-3.5-turbo**. The LLM is loaded here to prevent re-initialization of the LLM in the scrape_with_playwright method.

The code for API is in [fastapi_app.py](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/openai_backend/fastapi_app.py)

## Extracting Schema Data from Web Page

The code for extracting scheme data from the web page is in [langchain_extractor.py](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/openai_backend/langchain_extractor.py). Specifically, the code resides in the method **scrape_with_playwright**. The inputs to this method are the URL, the list of attribute names and the LLM. In this case, the LLM is OpenAI's **gpt-3.5-turbo**.

LangChain provides playwright-based **AsyncChromiumLoader** and beautiful-soup-based **BeautifulSoupTransformer** to extract the content from the web page.

A schema is constructed with the **properties** and **required** keys using the list of attribute names.

LangChain's **create_extraction_chain** method is then used to extract the information in a JSON-based format using the LLM, the schema, and the clean web page data.

**Fault tolerance** is ensured by keeping the **scrape_with_playwright** method within try-except blocks in the FastAPI API definition. The script displays an error message if the function call fails and the except block handles the error.

## Running the Backend

Create an Anaconda virtual environment with the following command:
```bash
conda create -n backend python=3.11
```

Activate the virtual environment with the following command:
```bash
conda activate backend
```

Install the required packages from the requirements.txt file with the following command:
```bash
pip install -r requirements_backend.txt
```

To run the backend, run the following command in the terminal:
```bash
uvicorn fastapi_app:app --reload
```

The API is available on the address **http://127.0.0.1:8000/extract**

</details>

<details>
<summary><b>Cohere + LangChain + FastAPI Backend</b></summary>

![cohere diagram](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/cohere_backend/cohere_fastpi.jpg)

## Video Demonstration

[Cohere LLM Web Scraper](https://youtu.be/zhy6VixY-yA)



## FastAPI API

The FastAPI API(*/extract*) is a RESTful API that takes a URL and a list of attribute names as input and returns the extracted attributes from the webpage after calling a method **scrape_extract** that takes input the URL and the list of attribute names.

The code for API is in [fastapi_cohere.py](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/cohere_backend/fastapi_cohere.py)

## Extracting Schema Data from Web Page

The code for extracting schema data from the web page is in [cohere_extractor_v2.py](https://github.com/rukshar69/LLM-Web-Scraping/blob/main/cohere_backend/cohere_extractor_v2.py). Specifically, the code resides in the method **scrape_extract**. The inputs to this method are the URL and the list of attribute names.

### Web Scraping

LangChain provides playwright-based **AsyncChromiumLoader** and beautiful-soup-based **BeautifulSoupTransformer** to extract the content from the web page. However, running **AsyncChromiumLoader** with **FastAPI** led to an error about a conflict in async mechanisms. Therefore, the code in the **AsyncChromiumLoaderWrapper** class was created to address this issue. This Wrapper class inherits from the **AsyncChromiumLoader** class and adds custom asynchronous methods to handle playwright web scraping. The code for the wrapper class is taken from [this GitHub issue](https://github.com/langchain-ai/langchain/issues/10475#issuecomment-1715118795). The GitHub issue discusses the error at length.

### Prompt Engineering

The cleaned html content along with the attributes are inserted into a prompt for the Cohere LLM. The prompt is designed to extract only the attribute/schema values from the html content. The prompt returns a list of JSON objects with the attribute names and their corresponding values.

### Cohere API

Cohere provides free tier api to generate responses using its *command-r* model. The response is converted into a list of dictionaries format and returned to FastAPI API function. 

For this, we split the extracted clean text to prevent overflow of information in the prompt. For each split entered into the prompt, we receive a list of dictionaries. The lists of dictionaries are concatenated and returned to the FastAPI API function.

Here we check if the prompt return can be converted into a list of dictionaries. Otherwise, the returned data is not considered proper response and thus discarded. 

### Fault tolerance

Fault tolerance is ensured by keeping the **scrape_extract** method within try-except blocks in the FastAPI API definition. The frontend displays an error message if the function call fails and the except block handles the error.

The decoding of prompt response to a list of dictionaries is kept in a **try-except** block for **fault tolerance**. 

## Running the Backend

Create an Anaconda virtual environment with the following command:
```bash
conda create -n backend python=3.11
```

Activate the virtual environment with the following command:
```bash
conda activate backend
```

Install the required packages from the requirements.txt file with the following command:
```bash
pip install -r requirements_cohere_backend.txt
```

To run the backend, run the following command in the terminal(after moving to the *cohere_backend* directory):
```bash
uvicorn fastapi_cohere:app --reload
```

The API is available on the address **http://127.0.0.1:8000/extract**


</details>