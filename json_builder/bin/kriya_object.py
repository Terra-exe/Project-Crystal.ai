class Kriya:
    def __init__(self, title, voice, kriya):
        self.title = title
        self.voice = voice
        self.kriya = kriya

    def print_kriya(self):
        print(f"Title: {self.title}")
        print(f"Voice: {self.voice}")
        print("Kriya:")
        for exercise in self.kriya:
            print(f"\tExercise: {exercise.exercise}")
            for step in exercise.steps:
                print(f"\t\tStep:")
                for substep in step.substeps:
                    for key, value in substep.__dict__.items():
                        print(f"\t\t\t{key}: {value}")
                    if hasattr(exercise, 'wait'):
                        for wait in exercise.wait:
                            print(f"\t\tWait: {wait.value}{wait.timeframe} ({wait.type} - {wait.description})")
                if hasattr(exercise, 'wait'):
                    for wait in exercise.wait:
                        print(f"\t\tWait: {wait.value}{wait.timeframe} ({wait.type} - {wait.description})")
        print("success")



class Exercise:
    def __init__(self, exercise, steps, wait):
        self.exercise = exercise
        self.steps = steps
        self.wait = wait

class Step:
    def __init__(self, substeps):
        self.substeps = substeps
        

class Substep:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Wait:
    def __init__(self, value, timeframe, type, description):
        self.value = value
        self.timeframe = timeframe
        self.type = type
        self.description = description


def create_kriya_obj_from_json(json_obj):

    title = json_obj['title']
    voice = json_obj['voice']
    kriya_list = []
    for kriya in json_obj['kriya']:
        exercise = kriya['exercise']        
        steps_list = []
        for step in kriya['steps']:
            substeps_list = []
            for substep_key in sorted(step.keys()):
                if substep_key != 'substeps':
                    continue
                substeps = step[substep_key]
                for substep_dict in substeps:
                    substep = Substep(**substep_dict)
                    substeps_list.append(substep)
            steps_list.append(Step(substeps_list))
        waits_list = []
        for wait_dict in kriya['wait']:
            wait = Wait(**wait_dict)
            waits_list.append(wait)
        kriya_list.append(Exercise(exercise, steps_list, waits_list))
    return Kriya(title, voice, kriya_list)


