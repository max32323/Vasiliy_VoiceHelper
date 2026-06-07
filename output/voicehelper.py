"""Импорт нужных библиотек"""
import queue
import sounddevice as sd
import vosk
import json
import skills
import test
import voice
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from skills import *


connect_path = sqlite3.connect('user_path.db')
cursor_path = connect_path.cursor()
cursor_path.execute("""SELECT * FROM your_path""")
path = cursor_path.fetchall()

"""Режим ИИ голосом"""
GPT = None

GPT_t = None
"""Режим когда играет музыка"""
music_form = None

listen_bool = True

"""Очередь"""
q = queue.Queue()

"""Настройка модели"""
model = vosk.Model('vosk-model')
device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

"""Обращение к пользователю"""

"""Добавление в очередь"""
def callback(indata, frames, time, status):
    q.put(bytes(indata))

"""Функция обработки функций"""
def recognize(data, vectorizes, cif):
    global GPT
    global GPT_t
    global music_form
    global listen_bool
    if listen_bool:
        if data == 'спасибо' or data == 'пасибо' or data == 'благодарю':
            voice.speaker('всегда пожалуйста.')
            return
        elif data == 'василий' or data == 'вася' or data == 'васильев':
            cursor_path.execute("""SELECT * FROM your_path""")
            path = cursor_path.fetchall()
            with open(f'{path[0][0]}\my_name', 'r', encoding='utf-8') as file:
                user_name = file.read()
                file.close()
            voice.speaker(f'Да, {user_name}, чем я могу вам помочь?')
            return
        elif data == 'ты молодец' or data == 'ты красавчик' or data == 'ты отличный голосовой помощник':
            voice.speaker('спасибо вам за похвалу')
            return

    trg = test.TRIGGERS.intersection(data.split())
    if not trg:
        return
    data.replace(list(trg)[0], '')
    test_vector = vectorizes.transform([data]).toarray()[0]
    answer = cif.predict([test_vector])[0]
    func_name = answer.split()[0]
    print(GPT)

    if listen_bool:
        if GPT == True:
            if func_name == 'stop_GPT':
                voice.speaker(answer.replace(func_name, ''))
                GPT = skills.stop_GPT()
            elif func_name == 'offbot':
                voice.speaker(answer.replace(func_name, ''))
                skills.offbot()
            else:
                voice.speaker('Начал генерацию ответа на ваш запрос. Немного подождите')
                skills.GPT_answer(str(data))

        elif GPT_t == True:
            if func_name == 'GPT_talk_stop':
                voice.speaker(answer.replace(func_name, ''))
                GPT_t = skills.stop_GPT()
            elif func_name == 'offbot':
                voice.speaker(answer.replace(func_name, ''))
                skills.offbot()
            else:
                skills.GPT_talk(str(data))

        else:
            voice.speaker(answer.replace(func_name, ''))
            if 'как ты считаешь' in data or 'как ты думаешь' in data or 'подскажи мне' in data or func_name == 'text_itog':
                skills.text_itog()
            elif 'запиши в заметки' in data or 'запиши в заметке' in data or 'забежав заметки' in data or 'запиши заметки' in data or 'закажи заметки' in data or func_name == 'write_zamet':
                skills.write_zamet(str(data))
            elif 'зашифровать мой текст' in data or 'зашифрованный текст' in data or 'зашифрован мой текст' in data or 'зашифрованный мой текст' in data or 'зашифруй мой текст' in data or func_name == 'shifr':
                skills.shifr(str(data))
            elif func_name == 'password_server_copy' or 'какой у меня пароль от' in data or 'узнай какой мой пароль от' in data:
                skills.password_server_copy(str(data))
            elif func_name == 'open_web' or 'открой сайт' in data or 'сайт' in data:
                skills.open_web(str(data))
            elif func_name == 'you_video' or 'открой ютуб с запросом' in data or 'открой ютюб с запросом' in data or 'открой ютюб с запросам' in data or 'включи ютуб с запросом' in data or 'открой ютуб с запросам' in data or 'включи ютуб с запросам' in data:
                skills.you_video(str(data))
            elif func_name == 'python_file_create':
                skills.python_file_create(str(data))
            elif func_name == 'create_folder':
                skills.create_folder(str(data))
            elif func_name == 'presentation':
                skills.presentation(str(data))
            elif func_name == 'create_text_file':
                skills.create_text_file(str(data))
            elif func_name == 'menu_weather':
                skills.menu_weather(str(data))
            elif func_name == 'start_GPT':
                GPT = start_GPT()
            elif func_name == 'stop_GPT':
                GPT = stop_GPT()
            elif func_name == 'start_GPT_talk':
                GPT_t = start_GPT_talk()
            elif func_name == 'GPT_talk_stop':
                GPT_t = GPT_talk_stop()
            elif func_name == 'music_norm':
                music_form = True
            elif func_name == 'music_start':
                music_form = True
            elif func_name == 'stop_listen':
                listen_bool = stop_listen()
            else:
                exec(func_name + '()')
            return func_name
    else:
        if func_name == 'start_listen':
            listen_bool = start_listen()

"""Функция получения и произношения текста"""
def main():
    global music_form
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(test.data_set.keys()))
    classifier = LogisticRegression()
    classifier.fit(vectors, list(test.data_set.values()))

    del test.data_set
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0],
                          dtype="int16", channels=1, callback=callback) as stream:

        recognizer = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if len(data) > 0:  # Проверка наличия звука в потоке
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())['text']
                    print(result)
                    name = recognize(result, vectorizer, classifier)
                    print(name)
                    print('Музыка: ', music_form)
                    if name == 'music_norm' and music_form:
                        stream.stop()
                        music_form = skills.music_norm()
                    elif name == 'music_start' and music_form:
                        stream.stop()
                        music_form = skills.music_start(result)
                    if music_form == False:
                        stream.start()

"""Функция получения и произношения текста для меню(не постоянный)"""
def main_2():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device[0],
                          dtype="int16", channels=1, callback=callback) as stream:
        recognizer = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())['text']
                stream.stop()
                return result

"""Запуск"""
if __name__ == '__main__':
    main()

