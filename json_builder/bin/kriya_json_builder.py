import json
import sys
sys.path.insert(1, r'\\server\python server\Bambi Voice API\json_builder\bin')
#sys.path.append(r"C:\python server\website\json_builder\bin")
import stringCleanup

import string
SOURCE_FOLDER = "C:\\python server\\Bambi Voice API\\json_builder\\src\\"
OUTPUT_FOLDER = "C:\\python server\\Bambi Voice API\\json_builder\\output\\"

def kriya_file_to_json(filename, title, defaultBreakLong, defaultWaitLong, defaultPauseMedium, defaultPauseShort, speed):
    data = {"title": title, "kriya": []}
    with open(filename, "r") as file:
        for line in file:
            setTime = False
            setCommaPause = False
            setPeriodPause = False
            setNewLine = False

            if line.strip() == "":  # break for empty lines
                setNewLine = True
                defineTime = {"value": defaultBreakLong, "timeframe": "s", "type": "breakLong"}
                wait = {"wait": defineTime}
                data["kriya"].append(wait)
                continue

            if line.startswith("#"):  # if line starts with "#" it's a time marker
                line = line.rstrip('\n')
                value = line[1:-2]
                timeframe = line[-2:-1]
            
                defineTime = {"value": value, "timeframe": timeframe, "type": "waitLong"}
                wait = {"wait": defineTime}
                step["substeps"].append(wait)
                continue

            if line and line[0].isdigit():  # if line starts with a number, it's a new exercise
                exercise = {"exercise": line.strip(), "steps": []}
                data["kriya"].append(exercise)
            else:
                step = {"substeps": []}
                parts = line.strip().split(", ")
                for part in parts:
                    substep = {"substep": part}
                    step["substeps"].append(substep)
                exercise["steps"].append(step)

    # output the data in JSON format
    with open(OUTPUT_FOLDER + "output.json", "w") as f:
        f.write(json.dumps(data, indent=4))

def kriya_webformat_to_json(obj):
    
    defaultComma = obj["comma_pause"]
    defaultPeriod = obj["period_pause"]
    defaultNewLine = obj["newline_pause"]
    defaultNewSectionPause = obj["newsection_pause"]

   # print("##############")
  #  print(defaultComma)
   # print(obj["period_pause"])
   # print("##############")
    title = obj["title"] + ".json"
    json_dict = {}


    json_dict["title"] = title
    json_dict["voice"] = obj["voice"]
    json_dict["kriya"] = []

    i = 1
    while i <= obj["stepcount"]:
        kriya = {}
        kriya["exercise"] = "Step " + str(i) + ")"
        kriya["steps"] = []
        kriya["wait"] = []
        
        

            #steps
        steps = {}
        steps["substeps"] = []
       
                #substeps
                    #substep
        substeps = processText(obj["step" + str(i)], defaultComma, defaultPeriod, defaultNewLine)
      
                    #substepwait
        substepwait = {}
        substepwait["value"] = "null"
        substepwait["timeframe"] = "s"
        substepwait["type"] = "pauseMedium"
        substepwait["description"] = "period, comma, newline"

        
        sectionWaitTime = 0
        if obj["pause" + str(i)] == "":
            sectionWaitTime = defaultNewSectionPause
        else:
            sectionWaitTime = obj["pause" + str(i)]
    
        wait = {}
        wait["value"] = sectionWaitTime
        wait["timeframe"] = "s"
        wait["type"] = "breakLong"
        wait["description"] = "new section"

        #substeps["substep"] = (substep)
        #substeps["wait"].append(substepwait)
        #steps["substeps"] = substeps
        steps["substeps"].append(substeps)
        kriya["steps"].append(steps)
        kriya["wait"].append(wait)
        json_dict["kriya"].append(kriya)

        


        i+=1
        #exercise

        
    print(json.dumps(json_dict)) #This is the proper json format for beautifyier
    return json_dict
    #return json_str

def processText(inputText, comma, period, newLine):
    string_parts = stringCleanup.segmentTextForTime(inputText)

    result = []

    substeps = {}

    i = 1
    print("Here's an idea why don't I make it so that Side by side tuples that are exactly the same if they are a wait object")
    for segment, type in string_parts:
        wait = {}
        if (type == ","):
            wait["value"] = str(comma)
            wait["timeframe"] = "s"
            wait["type"] = "pauseShort"
            wait["description"] = "comma"
        elif (type == "."):
            wait["value"] = str(period)
            wait["timeframe"] = "s"
            wait["type"] = "pauseMedium"
            wait["description"] = "period"
        elif (type == "^"):
            wait["value"] = str(newLine)
            wait["timeframe"] = "s"
            wait["type"] = "waitLong"
            wait["description"] = "New Line"
        elif (type == "#"):
            substeps["substep" + str(i)] = segment
        else:
            wait["value"] = "null"
        
        if (type != "#"):
            substeps["substep"+ str(i)] = wait
        

        i+=1

    result = substeps

    return result


def run_from_file(file, title):
    filename = SOURCE_FOLDER + file
    kriya_file_to_json(filename, title, 20, 10, 5, 2, 1)

def run_from_web(title, defaultBreakLong, defaultWaitLong, defaultPauseMedium, defaultPauseShort, speed):
    tmptxt = SOURCE_FOLDER + title
    #kriya_obj_to_json(tmptxt, title, defaultBreakLong, defaultWaitLong, defaultPauseMedium, defaultPauseShort, speed)

#if __name__ == "__main__":
    #run_from_file("kriya_for_transforming_the_lower_to_the_higher_triangle.txt", "kriya_for_transforming_the_lower_to_the_higher_triangle")