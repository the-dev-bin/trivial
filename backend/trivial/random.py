import aiohttp
import json
import random


async def get_random_trivia(trivia_length):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://opentdb.com/api.php', params={'amount': trivia_length}) as resp:
            opentdb_resp = await resp.json()
            return translate_opentdb(opentdb_resp['results'])


def translate_opentdb(results):

    trivia = {
        'name': 'New Trivia Set',
        'config': {
            'show_players': True,
            'timer': 20
        },
        'questions': []
    }

    for item in results:
        choices = [{'text': x} for x in item['incorrect_answers']]
        choices.append({'text': item['correct_answer'], 'correct': True})
        random.shuffle(choices)
        trivia['questions'].append({
            'text': item['question'],
            'choices': choices
        })

    return trivia
