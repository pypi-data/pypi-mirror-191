Speech input provides a simple function to get an input from speech. It works like the buildin input function.
Under the hood it is just a speechrecognition wrapper using the Google speech recognizer.
By default, it uses a pre-defined key, please use your own Google speech recognition API Key with set_key(api_key: str).
To obtain your own API key, simply follow the steps on the API Keys page at the Chromium Developers site: https://www.chromium.org/developers/how-tos/api-keys/
You can specify a language in the speech_input function. Default is "en-US".

Prerequisites:
pip install speechrecognition
pip install pyaudio

Installation:
pip install speechinput

Code:
import speechinput as si

# Set google speech key
si.set_key('GOOGLE-API-KEY')

# With prefix
si.sinput('Say something:')

# silence output
inp = si.sinput('silent')
print(f'You said: {inp}')