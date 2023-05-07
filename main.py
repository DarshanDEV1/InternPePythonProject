from tkinter import *
from tkinter import ttk
import wikipedia
import pyttsx3
import random
from textblob import TextBlob

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")
        master.configure(background='#B2DFDB')

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Create notebook widget for multiple tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(padx=5, pady=5)

        # Create chat tab
        self.chat_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.chat_tab, text="Chat")

        # Create chat window
        self.chat_window = Text(self.chat_tab, bd=1, bg="#FFF", width=50, height=8, font=("Arial", 12), foreground="black")
        self.chat_window.config(state=DISABLED)
        self.chat_window.pack(padx=5, pady=5)

        # Create user input field
        self.user_input = Entry(self.chat_tab, bg="#FFF", width=50, font=("Arial", 12))
        self.user_input.pack(padx=5, pady=5)

        # Create send button
        self.send_button = ttk.Button(self.chat_tab, text="Send", command=self.send_message)
        self.send_button.pack(padx=5, pady=5)

        # Create quit button
        self.quit_button = ttk.Button(self.chat_tab, text="Quit", command=master.quit)
        self.quit_button.pack(padx=5, pady=5)

        # Create wiki tab
        self.wiki_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.wiki_tab, text="Wikipedia")

        # Create wiki search label
        self.wiki_label = ttk.Label(self.wiki_tab, text="Search Wikipedia:")
        self.wiki_label.pack(padx=5, pady=5)

        # Create wiki search field
        self.wiki_input = Entry(self.wiki_tab, bg="#FFF", width=50, font=("Arial", 12))
        self.wiki_input.pack(padx=5, pady=5)

        # Create wiki search button
        self.wiki_button = ttk.Button(self.wiki_tab, text="Search", command=self.search_wikipedia)
        self.wiki_button.pack(padx=5, pady=5)

    def send_message(self):
        message = self.user_input.get()
        self.user_input.delete(0, END)

        # Display user message in chat window
        self.chat_window.config(state=NORMAL)
        self.chat_window.insert(END, "You: " + message + "\n")
        self.chat_window.config(state=DISABLED)

        # Respond to user message
        response = self.get_response(message)

        # Display chatbot response in chat window
        self.chat_window.config(state=NORMAL)
        self.chat_window.insert(END, "Chatbot: " + response + "\n")
        self.chat_window.config(state=DISABLED)

        # Speak chatbot response using text-to-speech engine
        self.engine.say(response)
        self.engine.runAndWait()

    def get_response(self, message):
        greetings = ["hello", "hi", "hey", "hi there", "howdy"]
        goodbyes = ["bye", "goodbye", "see you", "see you later", "take care"]
        thanks = ["thank you", "thanks", "appreciate it", "thanks a lot", "thank you so much"]
        questions = ["what", "when", "where", "why", "who", "how"]
        responses = {
            "hello": ["Hello!", "Hi there!", "Hey!", "Hi! How can I assist you today?"],
            "how are you": ["I'm doing well, thank you for asking.", "I'm great, thanks for asking!"],
            "what's up": ["Not much, how about you?", "Nothing much, how can I assist you today?"],
            "how can you help me": ["I can assist you with any questions or concerns you have. Just let me know what you need help with!"],
            "bye": ["Goodbye!", "Take care!", "See you later!"],
            "thank you": ["You're welcome!", "Anytime!", "Glad I could help!"],
            "default": ["I'm sorry, I didn't understand your question. Could you please rephrase it?"],
            "sentiment": ["Based on my analysis, I think you are feeling {sentiment}.", 
                          "It seems like you are {sentiment}.", 
                          "My analysis suggests that you might be {sentiment}."]
        }
        message = message.lower()
        if message in greetings:
            return random.choice(responses["hello"])
        elif message in goodbyes:
            return random.choice(responses["bye"])
        elif message in thanks:
            return random.choice(responses["thank you"])
        elif any(question in message for question in questions):
            blob = TextBlob(message)
            sentiment = blob.sentiment.polarity
            if sentiment > 0.5:
                return random.choice(responses["sentiment"]).format(sentiment="very happy")
            elif sentiment > 0:
                return random.choice(responses["sentiment"]).format(sentiment="happy")
            elif sentiment == 0:
                return random.choice(responses["sentiment"]).format(sentiment="neutral")
            elif sentiment > -0.5:
                return random.choice(responses["sentiment"]).format(sentiment="unhappy")
            else:
                return random.choice(responses["sentiment"]).format(sentiment="very unhappy")
        elif message in responses:
            return random.choice(responses[message])
        else:
            return random.choice(responses["default"])

    def search_wikipedia(self):
        query = self.wiki_input.get()
        self.wiki_input.delete(0, END)

        try:
            # Search Wikipedia and display summary in new tab
            summary = wikipedia.summary(query)

            # Create new tab for displaying summary
            summary_tab = ttk.Frame(self.notebook)
            self.notebook.add(summary_tab, text=query)

            # Create text widget for displaying summary
            summary_window = Text(summary_tab, bd=1, bg="#FFF", width=80, height=25, font=("Arial", 12), foreground="black")
            summary_window.insert(END, summary)
            summary_window.config(state=DISABLED)
            summary_window.pack(padx=5, pady=5)

            # Speak summary using text-to-speech engine
            #self.engine.say(summary)
            #self.engine.runAndWait()

        except wikipedia.exceptions.DisambiguationError as e:
            # If there are multiple matching pages, display a list of options
            options = "\n".join(e.options)
            self.chat_window.config(state=NORMAL)
            self.chat_window.insert(END, "Chatbot: Please be more specific. Did you mean one of the following?\n" + options + "\n")
            self.chat_window.config(state=DISABLED)
            self.engine.say("Please be more specific. Did you mean one of the following?")
            self.engine.say(options)
            self.engine.runAndWait()

        except wikipedia.exceptions.PageError:
            # If there are no matching pages, display an error message
            self.chat_window.config(state=NORMAL)
            self.chat_window.insert(END, "Chatbot: Sorry, I couldn't find a matching page for your query.\n")
            self.chat_window.config(state=DISABLED)
            self.engine.say("Sorry, I couldn't find a matching page for your query.")
            self.engine.runAndWait()

def __init__(self, master):
    self.master = master
    master.title("Chatbot")
    master.geometry("600x700")

    # Set custom style for notebook tabs
    style = ttk.Style()
    style.theme_create("custom", parent="alt", settings={
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": "#E0E0E0", "foreground": "black"},
            "map": {"background": [("selected", "#FFF"), ("active", "#E0E0E0")], "foreground": [("selected", "black"), ("active", "#000")], "expand": [("selected", [1, 1, 1, 0])]}}})
    style.theme_use("custom")

    # Create chat window
    self.chat_window = Text(master, bd=1, bg="#FFF", width=80, height=25, font=("Arial", 12), foreground="black")
    self.chat_window.config(state=DISABLED)
    self.chat_window.pack(padx=5, pady=5)

    # Create input field and button
    self.input_field = Entry(master, bd=1, bg="#FFF", width=50, font=("Arial", 12), foreground="black")
    self.input_field.bind("<Return>", self.send_message)
    self.input_field.pack(side=LEFT, padx=5, pady=5)

    self.send_button = Button(master, text="Send", command=self.send_message, bd=1, bg="#4CAF50", foreground="white", font=("Arial", 12))
    self.send_button.pack(side=LEFT, padx=5, pady=5)

    # Create notebook for displaying search results
    self.notebook = ttk.Notebook(master, width=550, height=400)
    self.notebook.pack(padx=5, pady=5)

    # Create Wikipedia search tab
    self.create_wiki_tab()

root = Tk()
gui = ChatbotGUI(root)
root.mainloop()
