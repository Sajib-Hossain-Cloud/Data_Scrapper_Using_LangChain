import cohere
from langchain_community.document_loaders.chromium import AsyncChromiumLoader
from langchain_community.document_transformers.beautiful_soup_transformer import BeautifulSoupTransformer
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

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


def get_list_dict(html_content, joined_attributes):
	
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

	response = co.chat(
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


COHERE_API_KEY = os.getenv('COHERE_API_KEY')

co = cohere.Client(COHERE_API_KEY)

loader = AsyncChromiumLoader(["https://www.scrapethissite.com/pages/simple/"])
#loader = AsyncChromiumLoader(["https://quotes.toscrape.com/page/2/"])
# loader = AsyncChromiumLoader(["https://books.toscrape.com/index.html"])
# loader = AsyncChromiumLoader(["https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"])
docs = loader.load()
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(
    docs, tags_to_extract=['p', 'li', 'div', 'a',"span"]
)

# attributes = ['book_author', 'book_price', 'book_name', 'book_rating']
# attributes = ['quote_author', 'quote', 'tags']
attributes = ['country_name', 'country_area', 'country_population']
joined_attributes = ", ".join(attributes)


# html_content = """
# Books to Scrape (../../index.html) We love being scraped!        Home (../../index.html)    Books (../category/books_1/index.html)    Poetry (../category/books/poetry_23/index.html)   A Light in the Attic         Start of product page               A Light in the Attic  £51.77   In stock (22 available)        <small><a href="/catalogue/a-light-in-the-attic_1000/reviews/"> 0 customer reviews </a></small>  <a id="write_review" href="/catalogue/a-light-in-the-attic_1000/reviews/add/#addreview" class="btn btn-success btn-sm"> Write a review </a>   Warning! This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.  /col-sm-6  /row   Product Description   It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love th It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius? RockabyeRockabye baby, in the treetopDon't you know a treetopIs no safe place to rock?And who put you up there,And your cradle, too?Baby, I think someone down here'sGot it in for you. Shel, you never sounded so good. ...more   Product Information     UPC a897fe39b1053632    Product Type Books    Price (excl. tax) £51.77    Price (incl. tax) £51.77    Tax £0.00    Availability  In stock (22 available)    Number of reviews  0        End of product page
# """

html_content = docs_transformed[0].page_content
# attributes = "book_author, book_price, book_name, book_rating"

#rewrite the message variable to set the html_content variable inside
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
splits = splitter.split_documents(docs_transformed)
print("Number of splits: ", len(splits))

list_of_all_dict = []
s = 0
for split in splits:
	print('=================================================')
	extracted_content = get_list_dict( html_content=split.page_content, attributes=joined_attributes)
	print(extracted_content)
	
	if extracted_content is not None:
		list_of_all_dict.append(extracted_content)
	s+=1
	if s== 3:
		break

print('CONCATENATED ARRAY')
print(concatenate_arrays(list_of_all_dict))

