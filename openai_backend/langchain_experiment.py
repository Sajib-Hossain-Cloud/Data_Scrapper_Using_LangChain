from langchain_community.document_loaders.chromium import AsyncChromiumLoader
from langchain_community.document_transformers.beautiful_soup_transformer import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
from langchain.chains.openai_functions.extraction import create_extraction_chain
import pprint
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load HTML
loader = AsyncChromiumLoader(["https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"])
html = loader.load() #list of documents

# Transform
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=['p', 'li', 'div', 'a',"span"])

print(docs_transformed[0].page_content)
# Grab the first 1000 tokens of the site
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=0
)
splits = splitter.split_documents(docs_transformed)

pprint.pprint(splits)

#print(docs_transformed[0].page_content)
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

schema = {
    "properties": {
        "book_author": {"type": "string"},
        "book_author": {"type": "string"},
        "book_name": {"type": "string"},
        "book_rating": {"type": "string"},
    },
    "required": ["book_author", "book_author", "book_name", "book_rating"],
}


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)


def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=['p', 'li', 'div', 'a',"span"]
    )
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    # splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    #     chunk_size=1000, chunk_overlap=0
    # )
    # splits = splitter.split_documents(docs_transformed)

    # Process the first split
    extracted_content = extract(schema=schema, content=docs_transformed[0].page_content)
    pprint.pprint(extracted_content)
    return extracted_content


# urls = ["https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"]
# extracted_content = scrape_with_playwright(urls, schema=schema)