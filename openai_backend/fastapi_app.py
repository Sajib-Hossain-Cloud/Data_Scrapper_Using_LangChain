from fastapi import FastAPI, Query
from requests import get
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_extractor import scrape_with_playwright

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
class AttributeRequest(BaseModel):
    url: str
    attributes: list

app = FastAPI()

@app.post("/extract")
async def extract_attributes(request: AttributeRequest):
    """
    Extracts attributes from a given URL.

    Args:
        AttributeRequest request: A request object containing the URL and attributes to extract.

    Returns:
        dict: A JSON object containing the extracted attributes.
    """
    print("In extract attributes method")
    input_data = request.model_dump()
    url = input_data['url']
    attributes = input_data['attributes']
    try:
        # response = get(url)
        # response.raise_for_status()  # Raise exception for non-2xx status codes

        # return {"url":url, "attributes": attributes,  "html": response.text, }

        return scrape_with_playwright(url, attributes, llm)
    except Exception as e:
        return {"error": str(e)}
