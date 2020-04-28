from multiprocessing import Process
import time

def asyncFileWriter():
	for i in range(10):
		with open('TEST_WOW.txt', 'a') as txt:
			txt.write(f':D oh wow #{i}\n')
		time.sleep(5)

if __name__ == '__main__':
	proc = Process(target=asyncFileWriter)
	proc.start()
	print('Niggers are gay')