twitter_setup:
	pip install -r twitter/requirements.txt
	cp twitter/settings.py.sample twitter/settings.py
	@echo "\nChange configurations in twitter/settings.py:\nDATADIR, TWITTER_KEYS['consumer_key'], TWITTER_KEYS['consumer_secret']"
