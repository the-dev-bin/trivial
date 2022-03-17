import requests
import json
import random


def get_random_trivia(trivia_length):
    trivia = {
        'name': 'New Trivia Set',
        'config': {
            'show_players': True,
            'timer': 20
        },
        'questions': []
    }
    results = json.loads(requests.get(url='https://opentdb.com/api.php', params={'amount': trivia_length}).text)['results']
    for item in results:
        choices = [{'text': x} for x in item['incorrect_answers']]
        choices.append({'text': item['correct_answer'], 'correct': True})
        random.shuffle(choices)
        trivia['questions'].append({
            'text': item['question'],
            'choices': choices
        })

    return json.dumps(trivia, indent=2)
