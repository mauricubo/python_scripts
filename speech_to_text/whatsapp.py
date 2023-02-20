import os
import requests

WP_WEB_URL = "https://graph.facebook.com/v15.0/"
WP_NUMBER = os.getenv("WP_NUMBER")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

simple_text = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "DEST_PHONE_NUMBER",
    "type": "text",
    "text": {
        "preview_url": True,
        "body": "MESSAGE_CONTENT"
    }
}

class WhatsAppApi:

    """
    Send a simple text message to a contact
    """
    def send_message(self, message, dest_number):
        url = f"{WP_WEB_URL}{WP_NUMBER}/messages"
        headers = {}
        headers['Authorization'] = f'Bearer {ACCESS_TOKEN}'
        msg = simple_text
        msg['to'] = dest_number
        msg['text']['body'] = message
        try:
            response = requests.post(
               url, json=msg, headers=headers
            )
            print(response.status_code)
            print(response.text)
        except Exception as e:
            print(e)
    
    """
    Private method - Save the file in local
    """
    def __save_file_on_local(self, id, media):
        try:
            with open(f'audios/{id}.ogg', 'wb') as audio:
                for chunk in media.iter_content(chunk_size=1024):
                    audio.write(chunk)
            return f'audios/{id}.ogg'
        except Exception as e:
            print(e)
            return None

    """
    Download the audio and send it for text convertion
    """
    def download_audio(self, id):
        # prepare the request
        # 1- Obtain the media url
        url = f"{WP_WEB_URL}/{id}"
        headers = {}
        headers['Authorization'] = f'Bearer {ACCESS_TOKEN}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and \
            response.json:
            media_url = response.json()["url"]
            media = requests.get(media_url, headers=headers)
            # 2- save the file on the local to processing
            local_file = self.__save_file_on_local(id, media)
            if local_file:
                return local_file
        return None