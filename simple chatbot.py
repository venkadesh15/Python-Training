print("Chatbot: Hello! I am your chatbot.")

while True:
    a = input("You: ")    
    b = a.lower()
    
    if b in ["bye", "quit", "exit"]:
        print("Chatbot: Goodbye!")
        break
    elif "hello" in b or "hi" in b:
        print("Chatbot: Hello there! How are you?")
    elif "how are you" in b:
        print("Chatbot: I am fine. what about you?")
    elif "i am fine" in b or "yes" in b or "ok" in b:
        print("Chatbot: What do you want?")
    elif "give me some details or information of your chatbot" in b:
        print("Chatbot: I am a simple Python chatbot.")
    elif "next" in b or "more" in b:
        print("Chatbot: I am a beginner level chatbot so I have enough of message")
    else:
        print("Chatbot: I will get you until you continue", a)

