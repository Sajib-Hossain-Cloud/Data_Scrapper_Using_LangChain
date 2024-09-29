#Streamlit app that takes a url and a list of attribute names as input
import streamlit as st
from streamlit_tags import st_tags
import requests 

#command: streamlit run scraper_ui.py
def get_attributes(url: str, attributes: list[str] ):
  """
  A function that sends a POST request to a specified API endpoint with provided URL and attributes.
  
  Parameters:
      url (str): The URL to send the request to.
      attributes (list[str]): A list of attributes to send in the request.
  
  Returns:
      dict: A dictionary containing the JSON response data from the API, or an error message if the request fails.
  """
  print('In get attributes method')
  api_url = "http://127.0.0.1:8000/extract"
  # Prepare the data to send in the request
  data = {
      "url": url,
      "attributes": attributes
  }

  try:
    # Send a POST request to the API endpoint
    response = requests.post(api_url, json=data)
    response.raise_for_status()  # Raise exception for non-2xx status codes

    # Get the JSON response from the API
    json_data = response.json()

    # return the received JSON data
    return json_data

  except requests.exceptions.RequestException as e:
    return {"Error": f"Request failed: {e}"}

st.title("Webpage Attribute Extractor")

url = st.text_input("Enter the URL of the webpage")
attributes = st_tags(
    label='**Enter Attributes:**',
    text='Press enter to add more',
    #value=['Zero', 'One', 'Two'],
    #suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'],
    maxtags=10,
    key="aljnf" ) #Assign a key so the component is not remount every time the script is rerun



if st.button("Extract Attributes"):
  if url and attributes:
    with st.spinner('Getting Data...'):
      attribute_values = get_attributes(url, attributes)
      st.json(attribute_values)
  else:
    st.warning("Please enter a URL and select attributes")