
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    
    if not current_question_id:
        return False, "Current question ID is missing."
    if not answer:
        return False, "Answer cannot be empty."
    if not isinstance(answer, str):
        return False, "Answer must be string."
    if 'quiz_answers' not in session:
        session['quiz_answers'] = {}
    session['quiz_answers'][current_question_id] = answer

    session.modified = True
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    PYTHON_QUESTION_LIST = [
        {"id":"q1","question":"what is output of 2+2?", "options":["3","4","5"],"correct_answer":"4"},
    ]

    for index, question in enumerate(PYTHON_QUESTION_LIST):
        if question['id'] == current_question_id:
            if index+1 < len(PYTHON_QUESTION_LIST):
                return PYTHON_QUESTION_LIST[index + 1]
            else:
                return None

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    PYTHON_QUESTION_LIST = [
        {"id": "q1", "question": "what is output of 2+2?", "options": ["3", "4", "5"], "correct_answer": "4"},
    ]
    if 'quiz_answers' not in session or not session['quiz_answers']:
        return  "No answers were provided."
    user_answers = session['quiz_answers']
    score =0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question in PYTHON_QUESTION_LIST:
        question_id = question['id']
        correct_answer = question['correct_answer']
        user_answer = user_answers.get(question_id,"")

        if user_answer.strip().lower() == correct_answer.strip().lower():
            score += 1
    result_message = f"your final score is {score}/{total_questions}. well done"

    return "dummy result"
