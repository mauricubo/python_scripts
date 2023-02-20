# Speech to text API

Speech to text app ist an Flask api that transcribe whatsapp audios into a text and send it back to the user.

![Speech to text](https://blog.mauricubo.com/content/images/2023/02/whatsapp_audio-1.gif)

---
### Whisper
I have used whisper to transcribe the audio into text. This is an OpenAI library that allows you to procees audio and returns the text of the audio and more metadata.

[OpenAI-Whisper](https://openai.com/blog/whisper/)

---
### Whatsapp API
In order to integrate our speach to text function with the Whatsapp Cloud API, we need to create the webhook that allow us to receive the messages that we send to our api Whatsapp number.

![Diagram-flow](https://blog.mauricubo.com/content/images/2023/02/whatsapp-webhook-1.jpg)

---
### Installation

1. Install the requirements ...
```bash 
pip install -r requeriments.txt --no-cache-dir 
```

2. Export the environment variables
```bash
export WP_NUMBER='<your_app_wp_number>'
export ACCESS_TOKEN='<your_app_wp_token>'
export WEBHOOK_TOKEN='<your_generated_token>'
```

3. Run the development server
```bash
python main.py
```
---

For more details read this blog post
[Speech to text](https://blog.mauricubo.com/speech-to-text/)
