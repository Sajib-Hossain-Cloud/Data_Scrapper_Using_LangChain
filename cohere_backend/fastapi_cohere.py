from fastapi import FastAPI, Query
from requests import get
from pydantic import BaseModel
#from cohere_extractor import scrape_extract
from cohere_extractor_v2 import scrape_extract
import uvicorn

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
        data = await  scrape_extract(url, attributes,)
        return data
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":

    uvicorn.run(
        "fastapi_cohere:app",
        host="0.0.0.0",
        reload=False,
        port=8000
    )