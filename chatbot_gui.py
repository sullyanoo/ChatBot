import tkinter as tk
from tkinter import scrolledtext
from chatbot_logic import *

class ChatBotGUI:
    def __init__(self, master, chatbot_logic):
        self.master = master
        master.title("ChatBot Comnect")

        self.chatbot_logic = chatbot_logic

        self.create_widgets()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.master, width=30)
        self.entry.pack(pady=10)

        self.send_button = tk.Button(self.master, text="Enviar", command=self.process_user_input)
        self.send_button.pack()

        self.quit_button = tk.Button(self.master, text="Sair", command=self.master.quit)
        self.quit_button.pack()

        self.display_next_message()

    def process_user_input(self):
        user_input = self.input_user()
        self.display_response(user_input)
        self.delete_entry()

    def display_response(self, response):
        self.chatbot_logic.display_response(response)
        self.display_next_message()

    def display_next_message(self):
        self.chatbot_logic.display_next_message()
        message = self.chatbot_logic.get_current_message()
        self.display_message(f"{message}\n")
        self.text_area.yview(tk.END)

    def input_user(self):
        return self.entry.get()

    def delete_entry(self):
        self.entry.delete(0, tk.END)

    def display_message(self, message):
        self.text_area.insert(tk.END, f"{message}\n")

def main():
    root = tk.Tk()
    chatbot_logic = ChatBotLogic()
    chatbot_gui = ChatBotGUI(root, chatbot_logic)
    root.mainloop()

if __name__ == "__main__":
    main()
