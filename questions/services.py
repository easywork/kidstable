from . import models

def verify(questions_, answers_):
    results = []
    for i in range(0, len(questions_)):
        question = models.Question(questions_[i])
        if answers_[i] == '':
            results.append(False)
            continue
        if question.getAnswer() == int(answers_[i]):
            results.append(True)
        else:
            results.append(False)
    return results

            
