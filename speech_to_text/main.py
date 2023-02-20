import os
from flask import Flask, request, flash
from transcriber import Transcriber
from werkzeug.utils import secure_filename

from whatsapp import WhatsAppApi

UPLOAD_FOLDER = 'audios'
ALLOWED_EXTENSIONS = {'ogg', 'mp3', 'wav'}
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')

app = Flask(__name__)
app.secret_key ="fdsatgda4254qgrq3fg/4qe"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

wp = WhatsAppApi()
tr = Transcriber("base")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET'])
def home():
    return "Hello World"

"""
this method is to recive and transform to text the audio directly
just post to the /transcriber and the response is the text of the audio
"""
@app.route('/transcriber', methods=["POST"])
def transcriber():
    if request.method == 'POST':
        # check if there is file paramenter in the request
        if 'file' not in request.files:
            flash("No file part")
            return {'msg': 'No file part'}, 401
        # get the file and put it on a variable
        audio = request.files['file']
        # check if there actualy have something
        if audio.filename == '':
            flash('No selected file')
            return {'msg': 'No selected file'}, 404
        if audio and allowed_file(audio.filename):
            # Save the file int the local
            filename = secure_filename(audio.filename)
            audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Do the magic with whisper
            lg, text = tr.transcribe(
                    os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # remove the file
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Return the message
            return {'msg': 'message processed sucesfully', 
                    'language': lg,
                    'text': text
                }, 200

    return {'msg': 'The http method is not allowed'}, 403


def process_messages(messages):
    audios = []
    for msg in messages:
        if msg.get("type") == "audio":
            audios.append(msg.get("audio").get("id"))
    return audios

def send_transcribed_msgs(audios_id, to):
    for a_id in audios_id:
        path = wp.download_audio(a_id)
        lg, text = tr.transcribe(path)
        wp.send_message(f'language: {lg} - msg: {text}',
            to)    


"""
doc: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples
get the audios in the messages
1- obtain the ID of the audio
entry[] -> changes[] -> value -> messages[] -> audio -> id
2- download the audio and process it
3- send the transcription to the number
"""
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """
    POST: all related to the messages that were sent
    """
    if request.method == 'POST':
        try:
            audios_id = []
            entries = request.json.get("entry")
            for entry in entries:
                changes = entry.get("changes")
                for change in changes:
                    value = change.get("value")
                    messages = value.get("messages")
                    # get the sender number
                    from_num = messages[0]["from"]
                    # proceess the messages = download  + transcribe
                    audios_id = process_messages(messages)
                    # send the text
                    send_transcribed_msgs(audios_id, from_num)
        except Exception as e:
            print(e)
            return {"msg": "Error processing msgs"}, 500
        # Check tomorrow!!!
        return {"msg": "message recived"}, 200
    # Get method on webhook is for registration propouse
    elif request.method == 'GET' and \
        request.args.get('hub.mode') == "subscribe" and \
        request.args.get('hub.verify_token') and \
        request.args.get('hub.verify_token') == WEBHOOK_TOKEN :
            return request.args.get('hub.challenge'), 200
    return {'message': 'Registration failed'}, 403

"""
Send a message to someone
"""
@app.route('/sendmessage', methods=['POST'])
def sendmessages():
    if request.method == 'POST' and \
        request.json and request.token == WEBHOOK_TOKEN:
        wp = WhatsAppApi()
        wp.send_message(request.json['message'], 
            request.json['number'] )
        return {'msg': "Message sent"}, 200
    else:
        return {'msg', "Message without data"}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
