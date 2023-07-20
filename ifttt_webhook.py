#############
###IMPORTS###
#############

from flask import Flask, Blueprint
from flask import request
import requests
import sqlite3
import asyncio

##################
###MAIN GLOBALS###
##################

DBPATH = r"mysite/database/database.db"
IFTTT_URL_DOMAIN = "https://maker.ifttt.com/trigger/"
IFTTT_URL_JSON = "/json/with/key/"
IFTTT_KEY = "d_zqQFhFGSIOpIcaQ0gzl2"
IFTTT_WEBHOOK_APP_EVENT_NAME = "webhook"

#DB SOURCES
DBSOURCES = {
    "DBSOURCE_TEST" : "test",
    "DBSOURCE_ALEXA" : "alexa",
    "DBSOURCE_CONSOLE" : "console",
    "DBSOURCE_WEB" : "web",
    "DBSOURCE_SCRIPT" : "code"
}


#DB CATAGORIES
DBCATAGORIES = {
    "DBCATAGORY_DEFAULT" : 'default',
    "DBCATAGORY_WISDOM" : "wisdom",
    "DBCATAGORY_AFFIRMATION" : "affirmation",
    "DBCATAGORY_CRYSTAL" : "crystal",
    "DBCATAGORY_REMINDERS" : "daily reminder",
    "DBCATAGORY_MEDITATION_REMINDERS" : "meditation reminder",
    "DBCATAGORY_BODY_SCAN" : "body scan"
}


#############
###GENERIC###
#############

#Trim a json string to text
def trim(jstring):
    jstring = jstring.strip("{}").split(":")[0].strip("'")
    jstring = jstring.replace('"', '')
    jstring = jstring.strip()
    jstring = jstring.lower()
    jstring = jstring.replace(".", "").replace("!", "").replace(";", "").replace(",", "").replace("-", "").replace("_", "").replace("#", "").replace("$", "").replace(":", "").replace("?", "")
    return jstring



##############
###DATABASE###
##############

def add_to_database(string, source, catagory):
    dbresult = ''
    # Connect to the database
    connection = sqlite3.connect(DBPATH)
    # Create the table if it does not already exist
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY,
            text TEXT,
            source SOURCE,
            catagory1 CATAGORY1
        )
    ''')

    # Check if the text already exists in the database
    cursor.execute("SELECT * FROM texts WHERE text=?", (string,))
    result = cursor.fetchone()
    # If the text does not exist, add it to the database
    if not result:
        cursor.execute("INSERT INTO texts (text, source, catagory1) VALUES (?, ?, ?)", (string, source, catagory))
        connection.commit()
        dbresult += "Text added to the database:"
    else:
        dbresult = "Text already exists in the database:"

    print(dbresult, string)
    # Close the cursor and connection
    cursor.close()
    connection.close()
    return dbresult

def remove_from_database(string):
    # Connect to the database
    connection = sqlite3.connect(DBPATH)

    # Create a cursor object
    cursor = connection.cursor()

    # Remove the string from the database
    sql = "DELETE FROM texts WHERE text = ?"
    val = (string,)
    cursor.execute(sql, val)

    # Commit the changes
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

def read_random_entry():
    # Connect to the database
    connection = sqlite3.connect(DBPATH)

    # Create a cursor object
    cursor = connection.cursor()

    # Get a random entry from the database
    sql = "SELECT text FROM texts ORDER BY RANDOM() LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Return the result
    return result[0]

def read_random_entry_catagory(catagory):
    # Connect to the database
    connection = sqlite3.connect(DBPATH)

    # Create a cursor object
    cursor = connection.cursor()

    # Get a random entry from the database filtered by the given catagory
    sql = "SELECT text FROM texts WHERE catagory1=? ORDER BY RANDOM() LIMIT 1"
    cursor.execute(sql, (catagory,))
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Return the result
    return result[0]

###########
###IFTTT###
###########



def send_webhook_to_ifttt(event_name, value):
    # Define your IFTTT Webhooks URL, using the event name you created
    url = f"https://maker.ifttt.com/trigger/{event_name}/json/with/key/d_zqQFhFGSIOpIcaQ0gzl2"

    #url = f"{IFTTT_URL_DOMAIN}{event_name}{IFTTT_URL_JSON}{IFTTT_KEY}"

    # Define the data to send with the webhook
    payload = { value : [] }

    # Send the webhook
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print("Webhook sent successfully!")
    else:
        print(f"Error sending webhook: {response.text}")
    return response.status_code



#######################
###WEBHOOK#############
###TO##################
###IFTTT & DATABASE####
#######################

def send_and_add(data, source, catagory):
    data = str(request.get_json())
    print(data)
    trimmed_data = trim(data)
    print(trimmed_data)
    dbresult = add_to_database(trimmed_data, source, catagory)
    send_webhook_to_ifttt(IFTTT_WEBHOOK_APP_EVENT_NAME, trimmed_data)
    return source + " POST Webhook received and processed " + dbresult + " \n\n" + trimmed_data, 200

##############
###WEBHOOKS###
##############


webhook = Blueprint("webhook", __name__)


#Alexa Webhook
@webhook.route("/alexa_post_webhook", methods=["POST"])
def handle_alexa_post_webhook():
    return send_and_add(str(request.get_json()), "alexa", "default")

#Testing Webhook
@webhook.route("/testing_post_webhook", methods=["POST"])
def handle_testing_post_webhook():
    return send_and_add(str(request.get_json()), "test", "default")

#@webhook.route('/')
#def hello_world():
#    send_webhook_to_ifttt(IFTTT_WEBHOOK_APP_EVENT_NAME, "Online")
#    return 'Hello from Flask3!'

#bulkAdd
@webhook.route('/bulk_add')
def bulk_add():
    meditation_reminder_data_array = ["Spinal cord", "Rib cage", "Pelvis", "Buttock", "Hip flexor right and left", "Quadriceps right and left", "Shin right and left", "Achilles tendon right and left", "Arch of foot right and left", "Instep right and left", "Jaw", "Nape of neck", "Chest upper, middle, and lower", "Underarm right and left", "Biceps right and left", "Triceps right and left", "Wrist flexor right and left", "Wrist extensor right and left", "Fingers right and left", "Fingertips right and left", "Arm pit right and left", "Side waist", "Hip right and left", "Groin", "Adductor muscle right and left", "Outer thigh right and left", "Inner thigh right and left", "Knee cap right and left", "Shin bone right and left", "Foot arch right and left", "Forehead", "Tongue", "Throat", "Collarbone right and left", "Shoulder right and left", "Upper arm right and left", "Elbow right and left", "Forearm right and left", "Wrist right and left", "Palm right and left", "Back of hand right and left", "Thumb right and left", "First, second, third, and fourth finger right and left", "Heart center", "Lungs right and left", "Diaphragm", "Navel center", "Low belly", "Hip joint right and left", "Thigh right and left", "Knee right and left", "Lower leg right and left", "Ankle right and left", "Heel right and left", "Sole of foot right and left", "Top of foot right and left", "Big toe right and left", "Second toe right and left", "Third, fourth, and little toe right and left", "Space around toes right and left", "Calf right and left", "Back of knee right and left", "Hamstring right and left", "Glute right and left", "Tailbone", "Sacrum", "Low back", "Lumbar spine", "Middle back and lower ribs", "Shoulder blade right and left", "Thoracic spine", "Neck and cervical spine", "Back of skull", "Crown of head", "Temple right and left", "Eye right and left", "Nostril right and left", "Cheekbone right and left", "Ear right and left", "Inside cheek right and left", "Upper and lower lip", "Chin", "Front of throat", "Side of chest right and left", "Sternum"]
    for item in meditation_reminder_data_array:
        add_to_database(item, "console", "body scan")

    return 'Updating Bulk'

@webhook.route('/body_scan')
def body_scan():
    #entry = "" + read_random_entry_catagory("body_scan")
    #while True:
        # Wait for a random amount of time between 1 and 10 seconds
        #time.sleep(random.randint(10, 20))
    entry = "" + read_random_entry()
    send_webhook_to_ifttt(IFTTT_WEBHOOK_APP_EVENT_NAME, entry)
    return 'Scanning Loop'

@webhook.route('/jillian')
def jillian_love():
    send_webhook_to_ifttt(IFTTT_WEBHOOK_APP_EVENT_NAME, "Jillian sends love.")
    return 'You have just sent Terra a text-to-speech message to their Alexa! \n\n It said \"Jillian Sends love!\"'


###################
###App Functions###
###################

#Define what app is running. And start the script.
def run_app_script(app_title, data):
    import app_scripts
    app_title = app_title.lower()
    print("Received WEB webhook")
    context = {
        "DBSOURCES" : DBSOURCES,
        "DBCATAGORIES" : DBCATAGORIES,
        "DBPATH" : DBPATH,
        "IFTTT_WEBHOOK_APP_NAME": IFTTT_WEBHOOK_APP_EVENT_NAME
    }

    app_scripts.pituitary_gland_kriya.run(context, data)
    return "Script Running"