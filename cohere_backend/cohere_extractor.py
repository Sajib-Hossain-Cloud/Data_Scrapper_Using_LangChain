import cohere
from langchain_community.document_loaders.chromium import AsyncChromiumLoader
from langchain_community.document_transformers.beautiful_soup_transformer import BeautifulSoupTransformer
import os
from dotenv import load_dotenv
from async_chrome_loader import AsyncChromiumLoaderWrapper

load_dotenv()

async def scrape_extract(url:str, attributes:list):
    print('In scrape extract')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    co = cohere.Client(COHERE_API_KEY) #load cohere client

    #extract textual content from webpage
    # loader = AsyncChromiumLoader([url])
    # docs = loader.load()
    loader = AsyncChromiumLoaderWrapper(urls=[url])
    docs = await loader.load_async()

    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=['p', 'li', 'div', 'a',"span"]
    )
    html_content = docs_transformed[0].page_content #will be used in prompt
    print('Extracted content: ', html_content[:20])

    #join the attrs in a string to be used in prompt
    joined_attributes = ", ".join(attributes)

    #define prompt
    # The prompt should output a list of json dictionaries with the key and value of the attributes

    # message = f"""
    # You are an expert data extractor. You are given partial HTML content and a set of schema/attributes. Both are delimited by triple ```. Your job is to extract the attribute values from the HTML content. The output should only contain a json dictionary of attribute key and attribute extracted value. Do not output anything else.
    # HTML content:
    # ```
    # {html_content}
    # ```
    # Attribute values:
    # ```
    # {joined_attributes}
    # ```
    # """

    message = f"""
    You are an expert data extractor. You are given partial HTML content and a set of schema/attributes. Both are delimited by triple ```. Your job is to extract the attribute values from the HTML content. The output should only contain a 
    list of json dictionaries where each element dictionary should contain a set of attribute key and its associated attribute extracted values. Do not output anything other than the list of dictionaries.
    Attribute values:
    ```
    {joined_attributes}
    ```
    HTML content:
    ```
    {html_content}
    ```
    """

    #get cohere response
    response = co.chat(
        message=message, 
        #model="command", 
        model="command-r", #claimed to be better performing
        temperature=0.0
    )

    answer = response.text
    dictionary = eval(answer) #convert string format to dictionary the desired format
    print(dictionary)
    return {"Result":dictionary}

if __name__ == "__main__":
    scrape_extract( url="https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html", attributes=['book_author', 'book_price', 'book_name', 'book_rating'])
