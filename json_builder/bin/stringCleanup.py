import string 
import re

def scrubCharacters(inputText):
    # Define a string of characters to keep
    keep_chars = string.ascii_letters + string.digits + '., \n'
    
    # Use the translate method to remove unwanted characters
    cleaned_text = inputText.translate(str.maketrans('', '', string.punctuation))
    cleaned_text = ''.join(filter(lambda x: x in keep_chars, cleaned_text))
    
    return cleaned_text

def segmentTextForTime(inputText):

    #print("INPUT TEXT")
    #print(inputText)

    #print("INPUT TEXT")
    newLineReplacedText = inputText.replace("\n", "^")
    #newLineReplacedText = "hello world^I^love^^You.^^Ok, yes.^^Ok. More words and sentences. Thanks, bobby I owe you, lots of dogs."
    #print("NEWLINE REPLACED TEXT")
    #print(newLineReplacedText)
    #print("NEWLINE REPLACED TEXT")
    
    
    #segments = re.split(r'[,:;\?!]+|\n', inputText)  # split into segments at periods, question marks, exclamation marks, colons, and newlines
    result = []

    

    # Input string to be segmented
    #input_string = "This is a sample, input string^with some special characters."

    # List of strings to use as segment delimiters
    delimiters = [",", ".", "^"]

    # Create a regular expression pattern from the delimiters
    pattern = '|'.join(map(re.escape, delimiters))

    # Split the input string using the regular expression pattern and capture the delimiters
    segments = re.split('({})'.format(pattern), newLineReplacedText)
    segments = [seg.strip() for seg in segments if seg.strip()]
    # Create a list of tuples that mirror the segments and have the appropriate delimiter as the second element
    couples = [(seg, "#" if seg not in delimiters else seg) for seg in segments]


    result = couples
   # print("CHANGED INPUT TEXT")
   # print(couples)
   # print("CHANGED INPUT TEXT")
    
    return result