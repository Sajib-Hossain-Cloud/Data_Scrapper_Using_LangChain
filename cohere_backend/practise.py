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

# Example usage
data1 = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}]
data2 = [1, 2, 3]
data3 = None
data4 = {'a': 1, 'b': 2}

print(is_list_of_dicts(data1))  # True
print(is_list_of_dicts(data2))  # False
print(is_list_of_dicts(data3))  # False (handles None case)
print(is_list_of_dicts(data4))  # False (not a list)
