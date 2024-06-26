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
    delimiters = [
    ",", ".", "^", "<SNAP>", "<POP>", "<BALLOONPOP>", "<BALLOONINFLATE>", 
    "<BLOWJOB1>", "<COCKSUCKING>", "<FORCESWALLOW1>", "<FORCESWALLOW2>", 
    "<GASP1>", "<GASP2>", "<GASP3>", "<GIGGLETIME>", "<GULPING>", "<LOCK>", 
    "<MOANING>", "<ROBOTHEART>", "<SUCTION_MACHINE>", "<SWALLOW>", "<SYNTHPULSE1>", 
    "<SYNTHPULSE2>", "<GRIMES_ANY_SUFFICIENTLY_ADVANCED>", "<GRIMES_MADE NOT BORN>", 
    "<GRIMES_MODERN_GODS_FOR_MODERN_GIRLS>", "<GRIMES_OUR_LADY_OF_PERPETUAL_CHAOS_TM>", 
    "<GRIMES1_DO_YOU_PRAY_AT_THE_ALTAR_OF_CHAOS>", "<GRIMES2_DO_YOU_PRAY_AT_THE_ALTAR_OF_CHAOS>", 
    "<GRIMES3_DO_YOU_PRAY_AT_THE_ALTAR_OF_CHAOS>", "<MYGOD>", "<OHMYGOD>", "<OHMYGOSH>", "<SEXYMOAN>", "<UHOHMYGOD>", "<WOW1>", "<WOW2>", "<SYNTHPULSE1RIGHT>", "<SYNTHPULSE1LEFT>", "<MAGIC>",
    "<EXPERIENCE>", "<GLITTER>", "<WOAH>", "<BAMBIRESET>", "<SPARKLEINTRO>", "<RESET>", "<POWERDOWN>", "<MAGICWINK>", "<DUCKSQUEAK>", "<INHALE>", "<EXHALE>", "<LEVELUP>", "<OHM>",
    "<CROWNBELL>", "<3RDEYEBELL>", "<THROATBELL>", "<HEARTBELL>", "<SOLARBELL>", "<SACRALBELL>", "<ROOTBELL>", "<OHITSYOU>", "<POP2>", "<GRIMES_ANY_SUFFICIENTLY_ADVANCED_GLADOS>", "<MUTELUNATIC>", "<ITSDANGEROUS>", "<ARENTDROIDS>", "<WHATWILLYOUFIND>",
    "<TANTRICHAR3M>", "<1MHARHARAYHAREEWAHHAYGURU>", "<5MSATANAMA>", "<BUBBLEPOP>", "<BUBBLESPOP1>", "<BUBBLESPOP2QUIET>", "<TIMELOCK>"
    ]


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