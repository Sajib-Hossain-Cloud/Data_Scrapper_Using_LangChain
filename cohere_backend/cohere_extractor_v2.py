import cohere
from langchain_community.document_loaders.chromium import AsyncChromiumLoader
from langchain_community.document_transformers.beautiful_soup_transformer import BeautifulSoupTransformer
import os
from dotenv import load_dotenv
from async_chrome_loader import AsyncChromiumLoaderWrapper
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

def is_list_of_dicts(data):
  """Checks if the data is a list of dictionaries.

  Args:
      data: The data to be checked.

  Returns:
      True if the data is a list of dictionaries, False otherwise.
  """

  # Check if data is a list
  if not isinstance(data, list):
    return False

  # Check if all elements in the list are dictionaries
  return all(isinstance(item, dict) for item in data)

def concatenate_arrays(arrays):
  """Concatenates a list of arrays, handling None values.

  Args:
      arrays: A list of arrays to concatenate.

  Returns:
      A new list containing the concatenated elements from all non-None arrays.
  """

  # Use list comprehension to filter out None values and concatenate the remaining elements
  return [element for array in arrays if array is not None for element in array]


def get_list_dict(html_content, joined_attributes, cohere_connector):
	
	message = f"""
	You are an expert data extractor. You are given partial HTML content and a set of schema/attributes. Both are delimited by triple ```. Your job is to extract the attribute values from the HTML content. The output should only contain a 
	list of json dictionaries where each element dictionary should contain a set of attribute key and its associated attribute extracted values. Do not output anything other than the list of dictionaries. There should be no characters before or after the list of dictionaries.
	Attribute values:
	```
	{joined_attributes}
	```
	HTML content:
	```
	{html_content}
	```
	"""

	response = cohere_connector.chat(
		message=message, 
		model="command-r", 
		temperature=0.0
	)

	answer = response.text
	print(answer)
	print('=======================')
	try:
		
		dictionary = json.loads(answer)
		print(type(dictionary))
		if is_list_of_dicts(dictionary):
			#print(dictionary)
			return dictionary
	except json.decoder.JSONDecodeError as e:
		print( f"Error decoding JSON: {e}" )



async def scrape_extract(url:str, attributes:list):

    joined_attributes = ", ".join(attributes) #joining the attributes in a string to be input in the prompt

    print('In scrape extract')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    co = cohere.Client(COHERE_API_KEY) #load cohere client

    #extract textual content from webpage
    loader = AsyncChromiumLoaderWrapper(urls=[url])
    docs = await loader.load_async()

    #clean the scraped web page to keep the relevant information
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=['p', 'li', 'div', 'a',"span"]
    )

    #split the extracted clean text to prevent overflow of information in the prompt
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)
    print("Number of splits: ", len(splits))

    list_of_all_dict = []
    s = 1
    for split in splits:
        print(f'=====================SPLIT={s}=========================')
        extracted_content = get_list_dict( html_content=split.page_content, joined_attributes=joined_attributes, cohere_connector=co)
        print(extracted_content)
        
        if extracted_content is not None:
            list_of_all_dict.append(extracted_content)
        s+=1
        # if s== 3:
        #     break

    print('CONCATENATED ARRAY')
    result = concatenate_arrays(list_of_all_dict)

    return {"Result":result}

if __name__ == "__main__":
    scrape_extract( url="https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html", attributes=['book_author', 'book_price', 'book_name', 'book_rating'])
