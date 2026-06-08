import openai
import string

def russian():
    russian_letters = ''.join(chr(i) for i in range(1040, 1104))  # А-Я, а-я

    digits = string.digits
    a = "'"
    special_characters = '1234567890!@#$%^&*()-—_=+№%[]{},.<>?;:"\\|\\\\`~–' + a + ' ' + 'ё' + 'ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba•'
    result_string = russian_letters + digits + special_characters
    return result_string

b = True

def GPT_answer(text: str):
    global b
    try:
        with open('API_KEY.txt', 'r', encoding='utf-8') as file:
            api = file.read().strip()
        openai.api_key = api
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"Ты помощник который даёт чёткие ответы, делай ответ от 1-ого лица. Главное чтобы твой ответ не превышал 300 символов, а также был на русском языке и быз лишних пробелов! Также сделай ответ от 1-ого лица, без подробностей!"},
                {"role": "user",
                 "content": f"Чёткий ответ для слайда презентации до 300 символом только по теме на русском языке, без доп символов и описания количества слов: {text}'"}
            ]
        )
        reply = chat_completion.choices.message.content
        return reply
    except:
        return 'Ошибка! Проверьте ваш api ключ и соеденение с интернетом!'

#print(GPT_answer('Виды цветов'))