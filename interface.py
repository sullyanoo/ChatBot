import tkinter as tk
from tkinter import scrolledtext
import json
from chatbot_logic import *

class ChatBot:
    def __init__(self, master):
        self.master = master
        master.title("ChatBot Comnect")

        self.obj = []
        self.user_input = None
        self.user_product = None
        self.name = None
        self.email = None
        self.cnpj = None
        self.scope = None
        self.sitef = None
        self.ipsec = None

        self.messages = [
            
            "Olá sou o assistente virtual da Comnect, como posso ajudar? Para iniciarmos sua sessão digite seu nome!: ",
            "Digite o seu e-mail:",
            "Digite o CNPJ do cliente que deseja atendimento:"
        ]

        self.messages_product = [
            '[1] - Scope', '[2] - IPSEC', '[3] - Sitef'
        ]

        self.messages_scope = [
            '[1] - Problemas de cadastro de contrato.', '[2] - PDV não esta realizando transações.', '[3] - Solicitação de carga de tabela.'
        ]

        self.messages_ipsec = [
            '[1] - Configuração de tunel.' , '[2] - Alteracão de tunel .' , '[3] - Tunel não está apresentando trafego.'

        ]

        self.messages_sitef = [
            '[1] - Carga de tabelas.', '[2] - PDV não esta conectando.' , '[3] - Configuração de loja.'

        ]

        self.current_message_index = 0
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
        user_input = self.inputUser()
        self.display_response(user_input) ## Put this block in a separate function
        self.deleteEntry()

    def display_response(self, response): ## Nome
        if self.current_message_index == 1:
            valid = self.is_string(response)
            if valid:
                self.obj.append(str(response))
            else:
                self.display_error(f"Nome inválido, tente novamente!\n")
                self.current_message_index -= 1  ## Decrement the index to retry the same message.

        elif self.current_message_index == 2: ## Email
            valid = self.is_string(response)
            if valid:
                self.obj.append(str(response))
            else:
                self.display_error(f"Insira um e-mail válido!\n")
                self.current_message_index -= 1  ## Decrement the index to retry the same message.

        elif self.current_message_index == 3: # CNPJ
            valid = self.is_int(response)
            if valid:
                self.obj.append(int(response))
            else:
                self.display_error(f"Insira um CNPJ válido!\n")
                self.current_message_index -= 1  ## Decrement the index to retry the same message.
        
        self.display_next_message()

    def display_next_message(self):
        if self.current_message_index < len(self.messages): ## Checks if the index is smaller than the size of the list.
            message = self.messages[self.current_message_index] ## Armazena o dado da lista em uma variavel mensagem.
            self.display_message(f"{message}\n") ## Apresenta no display o conteudo da mensagem
            self.text_area.yview(tk.END)  ## Role para o final da área de texto.
            self.current_message_index += 1 ## Acrescenta 1 ao index para ir para a proxima mensagem.
        
        elif self.current_message_index >= len(self.messages):
            self.input_product()
    
    def input_product(self):
        self.clear_text_area()
        self.display_message(f"Ok {self.name}, como eu posso te ajudar? Selecione o produto no qual voce deseja atendimento.\n")
        self.sprint_messages_product()
        response = self.inputUser()
        self.if_not_user_input(response)
        self.deleteEntry()

        if response == "1":
            self.clear_text_area()
            self.display_message(f'Entendi {self.name}. Para soluções Scope, escolha a opção que mais se adequa a sua solicitação.\n')
            self.sprint_messages_scope()
            if "Scope" not in self.obj:
                self.obj.append("Scope")

        elif response == "2":
            self.clear_text_area()
            self.display_message(f'Vamos lá! {self.name}. Para soluções IPSEC, escolha a opção que mais se adequa a sua solicitação.\n')
            self.sprint_messages_ipsec()
            if "IPSEC" not in self.obj:
                self.obj.append("IPSEC")

        elif response == "3":
            self.clear_text_area()
            self.display_message(f'Ok, {self.name}. Para soluções Sitef, escolha a opção que mais se adequa a sua solicitação.\n')
            self.sprint_messages_sitef()
            if "Sitef" not in self.obj:
                self.obj.append("Sitef")
        
        self.mount_obj()

    def mount_obj(self):
        self.name = self.obj[0] if len(self.obj) > 0 else None
        self.email = self.obj[1] if len(self.obj) > 1 else None
        self.cnpj = self.obj[2] if len(self.obj) > 2 else None
        self.scope = self.obj[3] if len(self.obj) > 3 and "Scope" in self.obj else None
        self.ipsec = self.obj[4] if len(self.obj) > 4 and "IPSEC" in self.obj else None
        self.sitef = self.obj[5] if len(self.obj) > 5 and "Sitef" in self.obj else None


    def display_error(self, message):
        self.text_area.insert(tk.END, f"{message}\n") ## Function that returns an error message.

    def display_message(self, message):
        self.text_area.insert(tk.END, f"{message}\n") ## Function that returns a display message.
        return

    def clear_text_area(self):
        self.text_area.delete(1.0, tk.END)  ## Deletes all content from beginning to end.
        return

    def sprint_messages_product(self): ## Scroll through the list and display the products on the display.
        for i in self.messages_product:
            self.text_area.insert(tk.END, f"{i}\n")

    def sprint_messages_scope(self): ## Scroll through the list and display the products Scope on the display.
        for i in self.messages_scope:
            self.text_area.insert(tk.END, f"{i}\n")
        
    def sprint_messages_ipsec(self): ## Scroll through the list and display the products IPSEC on the display.
        for i in self.messages_ipsec:
            self.text_area.insert(tk.END, f"{i}\n")

    def sprint_messages_sitef(self): ## Scroll through the list and display the products Sitef on the display.
        for i in self.messages_sitef:
            self.text_area.insert(tk.END, f"{i}\n")
           
    def is_string(self, value): ## Verifica o tipo de entrada para string.
        valid = value.isdigit()
        if valid:
             return False
        else:
            return isinstance(value, str)
    
    def is_int(self, value): ## Verifica o tipo da entrada para inteiro.
        valid = value.isdigit()
        if valid:
             return True
        else:
            return False
    
    ## Implementar essa função depois para limpar o código.
    def inputUser(self):
        user_input = self.entry.get()
        return user_input
    
    def if_not_user_input(self, user_input):
       if not user_input:  ## Check if user_input is empty.
            return user_input 
       
    def deleteEntry(self):
        self.entry.delete(0, tk.END)  ## Clear the entry after sending.
        return

def main():
    root = tk.Tk()
    chatbot = ChatBot(root) ## Adicionar após o root (,chatbot_logic).
    ##chatbot_logic = ChatBotLogic()
    root.mainloop()

    save_data_to_json(chatbot) ## Call the function Json.
    save_data_to_txt(chatbot)

def save_data_to_json(chatbot_instance): ## Function saves information in (Json) file.
    data = {
        "Name":  chatbot_instance.name,
        "Email": chatbot_instance.email,
        "CNPJ":  chatbot_instance.cnpj,
        "Scope": chatbot_instance.scope,
        "Sitef": chatbot_instance.sitef,
        "IPSEC": chatbot_instance.ipsec
    }

    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

def save_data_to_txt(chatbot_instance): ## Function saves informatios in (.txt) file.
    data = f"""
        Name: {chatbot_instance.name}
        Email: {chatbot_instance.email}
        CNPJ: {chatbot_instance.cnpj}
        Scope: {chatbot_instance.scope}
        Sitef: {chatbot_instance.sitef}
        IPSEC: {chatbot_instance.ipsec}
        """

    with open("data.txt", "w") as txt_file:
        txt_file.write(data)

if __name__ == "__main__":
    main()