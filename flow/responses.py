from gemini.promts import instruccion
import google.generativeai as genai
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
conversations = []
instruction = instruccion

def get_gemini_response(question):
    while True:
        response = chat.send_message(question + "\n" + instruction)
        print(response.text)
        question = ''
        if question.strip() == '':
            break
    
    return response
