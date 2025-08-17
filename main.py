import json
from flask import Flask, render_template, request, redirect, url_for, session
from function.questions import get_questions_dict
from function.auxiliar import selection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# questions = get_questions_dict()
json_path = '/Users/fernando/Desktop/Alvaro/Personal/Study-Guides-Cert/Cisco/Python-Labs/CiscoTest/resources' \
            '/questions.json '
with open(json_path, 'r') as f:
    questions = json.load(f)

responses = []


@app.route('/')
def start():
    session.clear()
    return redirect(url_for('question', qid=0))


@app.route('/question/<int:qid>', methods=['GET', 'POST'])
def question(qid):
    global responses
    if qid >= len(questions):
        return redirect(url_for('summary'))

    q = questions[qid]
    show_result = False
    is_correct = None
    selected = []

    if request.method == 'POST':
        selected = selection(request.form.getlist('answer'))
        session[str(qid)] = selected
        if selected:
            responses.append(selected)

        if 'continue' in request.form:
            return redirect(url_for('question', qid=qid + 1))
        elif 'prev' in request.form:
            return redirect(url_for('question', qid=qid - 1))
        else:
            # Show result for the current question
            correct = sorted(q['correct_answer'])
            is_correct = sorted(selected) == correct
            show_result = True

    previous_answers = session.get(str(qid), [])

    return render_template('question.html',
                           q=q, qid=qid, questions=questions,
                           previous_answers=previous_answers,
                           selected=selected,
                           show_result=show_result,
                           is_correct=is_correct)


@app.route('/summary')
def summary():
    score = 0
    total = len(questions)
    detailed_results = []

    for i, q in enumerate(questions):
        selected = responses[i]
        correct = sorted(q['correct_answer'])
        user_answer = sorted(selected)
        is_correct = user_answer == correct
        if is_correct:
            score += 1
        detailed_results.append({
            'question': q['question_text'],
            'your_answer': user_answer,
            'correct_answer': correct,
            'is_correct': is_correct
        })

    return render_template('summary.html', results=detailed_results, score=score, total=total)


if __name__ == '__main__':
    app.run(debug=True)

