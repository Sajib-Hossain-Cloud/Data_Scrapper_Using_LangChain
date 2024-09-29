from langchain_community.document_loaders.chromium import AsyncChromiumLoader
from langchain_community.document_transformers.beautiful_soup_transformer import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
from langchain.chains.openai_functions.extraction import create_extraction_chain
import pprint
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract(content: str, schema: dict, llm: ChatOpenAI):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

def scrape_with_playwright(url:str, attributes:list, llm: ChatOpenAI):
    urls = [url]
    #schema creation
    properties = {}
    for attribute in attributes:
        properties[attribute] = {"type": "string"}
    schema = {"properties": properties, "required": list(properties.keys())}


    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=['p', 'li', 'div', 'a',"span"]
    )
    print("Extracting content with LLM")

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)
    #for each split get the extracted content and merge it
    extracted_content_per_split = []
    for split in splits:
        extracted_content = extract(schema=schema, content=split.page_content, llm=llm)
        extracted_content_per_split.append(extracted_content)

    #extracted_content = extract(schema=schema, content=docs_transformed[0].page_content)
    return_json = {'result':extracted_content}
    return return_json
