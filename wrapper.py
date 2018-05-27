from elur import e

def predict(text, use='elur'):
	if use == 'elur':
		return e.predict(text)
	else:
		return 'NEU'