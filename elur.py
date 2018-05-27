class Elur():
	def __init__(self):
		self.sentence = {}
		with open('sentence.txt') as fi:
			text = fi.read().split('\n')
			current_emo = None
			for line in text:
				if line == '':
					continue
				elif line[0:2] == '==':
					current_emo = line.replace('==', '').replace(' ','')
				elif '##' in line:
					continue
				else:
					self.sentence[line] = current_emo

	def predict(self, text):
		if text in self.sentence:
			return self.sentence[text]
		return 'NEU'

if __name__ != '__main__':
	e = Elur()