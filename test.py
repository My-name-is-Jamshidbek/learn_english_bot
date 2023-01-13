# import soundfile as sf
#
# # o'qiladigan ovozli habar
# OGG_FILE = "example.ogg"
#
# # ovozli habar faylini .wav formatiga aylantirish
# data, samplerate = sf.read(OGG_FILE)
# sf.write("example.wav", data, samplerate)
#
#
# import speech_recognition as sr
#
# # O'qiladigan ovozli habar
# AUDIO_FILE = "example.wav"  # mp3 faylga o'zgartirish
#
# # Ovozli habarni matnga aylantirish
# r = sr.Recognizer()
# with sr.AudioFile(AUDIO_FILE) as source:
#     audio = r.record(source)  # ovozli habar o'qiladi
#
# # Matnni chiqarish
# print(r.recognize_google(audio))

#
# from gtts import gTTS
#
# # aylantiriladigan matn
# text = "a p p l e"
#
# # ovozli habar yaratish
# tts = gTTS(text)
#
# # ovozli habarni saqlash
# tts.save("example.mp3")
