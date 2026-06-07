import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-1].id) #базавая модель Василия, скачайте модель для использования

def speaker(text):
	engine.say(text)
	engine.runAndWait()



