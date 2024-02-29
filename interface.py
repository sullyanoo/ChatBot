import tkinter as tk
from tkinter import scrolledtext
import json
import uuid

class ChatBot:
    def __init__(self, master):
        self.master = master
        master.title("ChatBot Comnect")

        self.obj = []
        self.name = None
        self.email = None
        self.cnpj = None
        self.scope = None
        self.sitef = None
        self.ipsec = None
        self.subScope = None
        self.subIpsec = None
        self.subSitef = None
        self.response = None

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

        self.protocolo = self.gerar_protocolo()
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

        self.display_next_message(self.response)

    def process_user_input(self):
        self.response = self.entry.get()
        self.if_not_user_input(self.response)
        self.display_response(self.response) ## Put this block in a separate function
        self.deleteEntry()

    def display_response(self, response): ## Nome
        if self.current_message_index == 1:
            valid = self.is_string(response)
            if valid:
                self.name = response
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

        self.display_next_message(response)

    def display_next_message(self, response):

        if self.current_message_index < len(self.messages): ## Checks if the index is smaller than the size of the list.
            message = self.messages[self.current_message_index] ## Armazena o dado da lista em uma variavel mensagem.
            self.display_message(f"{message}\n") ## Displays the content of the message on the display
            self.text_area.yview(tk.END)  ## Scroll to the end of the text area.
            self.current_message_index += 1 ## Add 1 to the index to go to the next message.
        
        elif self.current_message_index >= len(self.messages):
            self.input_product(response)
    
    def input_product(self, response):
        self.clear_text_area()
        self.display_message(f"Ok {self.name}, como eu posso te ajudar? Selecione o produto no qual você deseja atendimento.\n")
        self.sprint_messages_product()
        
        # Get the user input

        if response == "1":
            self.obj.append("Scope")
            self.subProduct("Scope", self.messages_scope)
            
        elif response == "2":
            self.obj.append("IPSEC")
            self.subProduct("Ipsec", self.messages_ipsec)
        
        elif response == "3":
            self.obj.append("Sitef")
            self.subProduct("Sitef", self.messages_sitef)

        
    def subProduct(self, product, sub_options):
        self.clear_text_area()
        self.display_message(f'Entendi {self.name}. Para soluções {product}, escolha a opção que mais se adequa a sua solicitação.\n')
        self.sprint_sub_messages(sub_options)
        
        # Get the user input for sub-options
        
        valid_input = False
        while not valid_input:
            get_response = self.entry.get()
            if (self, f'sub{product}') != None:
                if get_response in ["1", "2", "3"]:
                    if get_response == "1":
                        setattr(self, f"sub{product}", sub_options[0])
                    elif get_response == "2":
                        setattr(self, f"sub{product}", sub_options[1])
                    elif get_response == "3":
                        setattr(self, f"sub{product}", sub_options[2])
            valid_input = True

        self.deleteEntry()
        self.mount_obj()
        print(self, f'sub{product}')
        print(get_response)    


    def sprint_sub_messages(self, sub_options):
        for i in sub_options:
            self.text_area.insert(tk.END, f"{i}\n")

    def display_completion(self):
        self.text_area.insert(tk.END, f'{self.name}, agradeço as informações fornecidas, segue o seu número de protocolo de atendimento {self.protocolo}\n')
        self.entry.config(state=tk.DISABLED) 
        
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
           
    def is_string(self, value): ## Checks input type for string.
        valid = value.isdigit()
        if valid:
             return False
        else:
            return isinstance(value, str)
    
    def is_int(self, value): ## Checks entry type is integer.
        valid = value.isdigit()
        if valid:
             return True
        else:
            return False
    
    def if_not_user_input(self, user_input):
        if not user_input:  ## Check if user_input is empty.
            return 
       
    def deleteEntry(self):
        self.entry.delete(0, tk.END)  ## Clear the entry after sending.
        self.response = None
        return
    
    def gerar_protocolo(self): # Generates a random protocol.
        protocolo = str(uuid.uuid4())
        return protocolo
    
    def mount_obj(self):
        self.name =  self.obj[0] if len(self.obj) > 0 else None
        self.email = self.obj[1] if len(self.obj) > 1 else None
        self.cnpj =  self.obj[2] if len(self.obj) > 2 else None
        self.scope = self.obj[3] if len(self.obj) > 3 and "Scope" in self.obj else None
        self.ipsec = self.obj[4] if len(self.obj) > 4 and "IPSEC" in self.obj else None
        self.sitef = self.obj[5] if len(self.obj) > 5 and "Sitef" in self.obj else None
		
def main():
    root = tk.Tk()
    chatbot = ChatBot(root)
    root.mainloop()

    save_data_to_json(chatbot) ## Call the function Json.
    save_data_to_txt(chatbot)

def save_data_to_json(chatbot_instance): ## Function saves information in (Json) file.
    data = {

        "Name":  chatbot_instance.name,
        "Email": chatbot_instance.email,
        "CNPJ":  chatbot_instance.cnpj,
        "Scope": chatbot_instance.scope,
        "SubScope": chatbot_instance.subScope,
        "Sitef": chatbot_instance.sitef,
        "SubSitef": chatbot_instance.subSitef,
        "IPSEC": chatbot_instance.ipsec,
        "SubIpsec": chatbot_instance.subIpsec,
        "Protocolo": chatbot_instance.protocolo
        
    }

    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

def save_data_to_txt(chatbot_instance): ## Function saves informatios in (.txt) file.
    data = f"""
        Name: {chatbot_instance.name}
        Email: {chatbot_instance.email}
        CNPJ: {chatbot_instance.cnpj}
        Scope: {chatbot_instance.scope}
        SubScope:{chatbot_instance.subScope}
        Sitef: {chatbot_instance.sitef}
        SubSitef: {chatbot_instance.subSitef}
        IPSEC: {chatbot_instance.ipsec}
        SubIpsec: {chatbot_instance.subIpsec}
        Protocolo: {chatbot_instance.protocolo}
        """

    with open("data.txt", "w") as txt_file:
        txt_file.write(data)

if __name__ == "__main__":
    main()