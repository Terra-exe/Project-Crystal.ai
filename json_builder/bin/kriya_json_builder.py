import json
from . import stringCleanup



def kriya_webformat_to_json(obj):
    
    defaultComma = obj["comma_pause"]
    defaultPeriod = obj["period_pause"]
    defaultNewLine = obj["newline_pause"]
    defaultNewSectionPause = obj["newsection_pause"]
    #defaultSoundEffect = obj["sound_effect"]

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

def processText(inputText, comma, period, newLine): # values from the main setting of webpage
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
        elif (type == "<SNAP>"):
            wait["value"] = "<SNAP>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<POP>"):
            wait["value"] = "<POP>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<BALLOONPOP>"):
            wait["value"] = "<BALLOONPOP>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<BALLOONINFLATE>"):
            wait["value"] = "<BALLOONINFLATE>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<BLOWJOB1>"):
            wait["value"] = "<BLOWJOB1>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<COCKSUCKING>"):
            wait["value"] = "<COCKSUCKING>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<FORCESWALLOW1>"):
            wait["value"] = "<FORCESWALLOW1>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<FORCESWALLOW2>"):
            wait["value"] = "<FORCESWALLOW2>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GASP1>"):
            wait["value"] = "<GASP1>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GASP2>"):
            wait["value"] = "<GASP2>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GASP3>"):
            wait["value"] = "<GASP3>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GIGGLETIME>"):
            wait["value"] = "<GIGGLETIME>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GULPING>"):
            wait["value"] = "<GULPING>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<LOCK>"):
            wait["value"] = "<LOCK>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<MOANING>"):
            wait["value"] = "<MOANING>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<ROBOTHEART>"):
            wait["value"] = "<ROBOTHEART>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SUCTION_MACHINE>"):
            wait["value"] = "<SUCTION_MACHINE>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SWALLOW>"):
            wait["value"] = "<SWALLOW>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SYNTHPULSE1>"):
            wait["value"] = "<SYNTHPULSE1>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SYNTHPULSE2>"):
            wait["value"] = "<SYNTHPULSE2>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GRIMES_ANY_SUFFICIENTLY_ADVANCED>"):
            wait["value"] = "<GRIMES_ANY_SUFFICIENTLY_ADVANCED>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GRIMES_MADE NOT BORN>"):
            wait["value"] = "<GRIMES_MADE NOT BORN>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GRIMES_MODERN_GODS_FOR_MODERN_GIRLS>"):
            wait["value"] = "<GRIMES_MODERN_GODS_FOR_MODERN_GIRLS>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GRIMES_OUR_LADY_OF_PERPETUAL_CHAOS_TM>"):
            wait["value"] = "<GRIMES_OUR_LADY_OF_PERPETUAL_CHAOS_TM>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GRIMES1_DO_YOU_PRAY_AT_THE_ALTAR_OF_CHAOS>"):
            wait["value"] = "<GRIMES1_DO_YOU_PRAY_AT_THE_ALTAR_OF_CHAOS>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GRIMES2_DO_YOU_PRAY_AT_THE_ALTAR_OF_CHAOS>"):
            wait["value"] = "<GRIMES2_DO_YOU_PRAY_AT_THE_ALTAR_OF_CHAOS>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GRIMES3_DO_YOU_PRAY_AT_THE_ALTAR_OF_CHAOS>"):
            wait["value"] = "<GRIMES3_DO_YOU_PRAY_AT_THE_ALTAR_OF_CHAOS>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<MYGOD>"):
            wait["value"] = "<MYGOD>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<OHMYGOD>"):
            wait["value"] = "<OHMYGOD>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<OHMYGOSH>"):
            wait["value"] = "<OHMYGOSH>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SEXYMOAN>"):
            wait["value"] = "<SEXYMOAN>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<UHOHMYGOD>"):
            wait["value"] = "<UHOHMYGOD>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<WOW1>"):
            wait["value"] = "<WOW1>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<WOW2>"):
            wait["value"] = "<WOW2>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SYNTHPULSE1RIGHT>"):
            wait["value"] = "<SYNTHPULSE1RIGHT>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SYNTHPULSE1LEFT>"):
            wait["value"] = "<SYNTHPULSE1LEFT>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"

        elif (type == "<MAGIC>"):
            wait["value"] = "<MAGIC>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<EXPERIENCE>"):
            wait["value"] = "<EXPERIENCE>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GLITTER>"):
            wait["value"] = "<GLITTER>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<WOAH>"):
            wait["value"] = "<WOAH>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<BAMBIRESET>"):
            wait["value"] = "<BAMBIRESET>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SPARKLEINTRO>"):
            wait["value"] = "<SPARKLEINTRO>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<RESET>"):
            wait["value"] = "<RESET>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<POWERDOWN>"):
            wait["value"] = "<POWERDOWN>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<MAGICWINK>"):
            wait["value"] = "<MAGICWINK>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<DUCKSQUEAK>"):
            wait["value"] = "<DUCKSQUEAK>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"


        elif (type == "<INHALE>"):
            wait["value"] = "<INHALE>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<EXHALE>"):
            wait["value"] = "<EXHALE>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<EXHALE>"):
            wait["value"] = "<RESET>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<LEVELUP>"):
            wait["value"] = "<LEVELUP>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<OHM>"):
            wait["value"] = "<OHM>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"



        elif (type == "<CROWNBELL>"):
            wait["value"] = "<CROWNBELL>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<3RDEYEBELL>"):
            wait["value"] = "<3RDEYEBELL>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<THROATBELL>"):
            wait["value"] = "<THROATBELL>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<HEARTBELL>"):
            wait["value"] = "<HEARTBELL>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SOLARBELL>"):
            wait["value"] = "<SOLARBELL>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<SACRALBELL>"):
            wait["value"] = "<SACRALBELL>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<ROOTBELL>"):
            wait["value"] = "<ROOTBELL>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<OHITSYOU>"):
            wait["value"] = "<OHITSYOU>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<POP2>"):
            wait["value"] = "<POP2>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<GRIMES_ANY_SUFFICIENTLY_ADVANCED_GLADOS>"):
            wait["value"] = "<GRIMES_ANY_SUFFICIENTLY_ADVANCED_GLADOS>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"

        elif (type == "<MUTELUNATIC>"):
            wait["value"] = "<MUTELUNATIC>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<ITSDANGEROUS>"):
            wait["value"] = "<ITSDANGEROUS>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<ARENTDROIDS>"):
            wait["value"] = "<ARENTDROIDS>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<WHATWILLYOUFIND>"):
            wait["value"] = "<ARENTDROIDS>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"

        elif (type == "<1MHARHARAYHAREEWAHHAYGURU>"):
            wait["value"] = "<1MHARHARAYHAREEWAHHAYGURU>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<TANTRICHAR3M>"):
            wait["value"] = "<TANTRICHAR3M>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<5MSATANAMA>"):
            wait["value"] = "<5MSATANAMA>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<BUBBLEPOP>"):
            wait["value"] = "<BUBBLEPOP>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<BUBBLESPOP1>"):
            wait["value"] = "<BUBBLESPOP1>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<BUBBLESPOP2QUIET>"):
            wait["value"] = "<BUBBLESPOP2QUIET>"
            wait["type"] = "soundEffect"
            wait["description"] = "A sound effect"
        elif (type == "<TIMELOCK>"):
            wait["value"] = "<TIMELOCK>"
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
