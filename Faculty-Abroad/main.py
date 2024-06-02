from app import app

if __name__ == '__main__':
	app.logger.setLevel('INFO')
	app.run(debug = True, port=5001)