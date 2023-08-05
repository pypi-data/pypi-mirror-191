# SpeechRecognitionCover

This library is using SpeechRecognition and make it easyer to use!!!

This is easy example:


      
    from SpeechRecognitionCover import Cover
    recognizer = Cover()
    while true:
        output = recognizer.recognize(noises=True)
        print('this is the output' + output)
      
      

If you are in a noisy place:

      
    from SpeechRecognitionCover import Cover
    recognizer = Cover()
    while true:
        output = recognizer.recognize(noises=True)
        print('this is the output' + output)
      
And you can use audio files as wel:

    from SpeechRecognitionCover import Cover
    recognizer = Cover()
    file_name = "<Your's file name>"
    print(recognizer.audio_file(file_name))