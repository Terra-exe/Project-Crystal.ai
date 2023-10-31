import json
from . import stringCleanup



def kriya_webformat_to_json(obj):
    
    defaultComma = obj["comma_pause"]
    defaultPeriod = obj["period_pause"]
    defaultNewLine = obj["newline_pause"]
    defaultNewSectionPause = obj["newsection_pause"]
    defaultSoundEffect = obj["sound_effect"]

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
        kriya["soundeffect"] = []
        
        

            #steps
        steps = {}
        steps["substeps"] = []
       
                #substeps
                    #substep
        substeps = processText(obj["step" + str(i)], defaultComma, defaultPeriod, defaultNewLine, defaultSoundEffect)
      
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

        soundeffect = {}
        wait["value"] = sectionWaitTime
        wait["type"] = "soundEffect"
        wait["description"] = "a sound effect"

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

def processText(inputText, comma, period, newLine, soundEffect): # values from the main setting of webpage
    string_parts = stringCleanup.segmentTextForTime(inputText)

    result = []

    substeps = {}

    i = 1
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
        elif (type == "9"):
            wait["value"] = str(soundEffect)
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "#"):
            substeps["substep" + str(i)] = segment
        else:
            wait["value"] = "null"
        
        if (type != "#"):
            substeps["substep"+ str(i)] = wait
        

        i+=1

    result = substeps

    return result
