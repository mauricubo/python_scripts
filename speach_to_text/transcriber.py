import whisper

class Transcriber:
   def __init__(self, model):
      self.model = whisper.load_model(model)

   """
      convert speach to text and return two variables
      - language: eg "en"
      - text: eg "Good morning, this is a whatsapp audio"
   """
   def transcribe(self, audio):
      try:
         result = self.model.transcribe(audio, fp16=False)
         return result["language"], result["text"]
      except Exception as e:
         print(e)
      return None, None
