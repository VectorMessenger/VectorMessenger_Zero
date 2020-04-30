# CONST
VERSION = '#dev0'
ICON_MAIN_PATH = './data/ico/main.ico'

# DICTS
strings = {
	'title': f'Localhost Messenger (version: {VERSION})'
}

# Test Functions
def _testMessageBox(messageBox):
	from time import sleep
	messageString = ''
	arrayMessage = ('test_0: Все понятно, автор запустил тест месседжбокса.', '\ntest_34: Мда, вот это неожиданная ситуация конечно.', '\ntest_12: Да реално.\n', 'test_2: Застал в расплох так сказать.\n')
	for i in range(40):	
		for i in range(len(arrayMessage)):
			messageString = messageString + arrayMessage[i]
			messageBox['text'] = messageString
			sleep(0.05)