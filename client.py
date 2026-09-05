import ollama

completion = ollama.chat(
    model = "llama3.2.:3b",
    messages = [
        {
            "role": "system",
            "content": "you are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Assistant."
        },
        {
            "role": "user",
            "content": "What is coding?"
        }
    ]
)
print(completion["message"]["content"])