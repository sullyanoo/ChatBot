import json

class ChatBotLogic:
    def __init__(self):

        self.obj = []
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

    def display_response(self, response):
        if self.current_message_index == 1:
            valid = self.is_string(response)
            if valid:
                self.obj.append(str(response))
            else:
                self.display_error(f"Nome inválido, tente novamente!\n")
                self.current_message_index -= 1

        elif self.current_message_index == 2:
            valid = self.is_string(response)
            if valid:
                self.obj.append(str(response))
            else:
                self.display_error(f"Insira um e-mail válido!\n")
                self.current_message_index -= 1

        elif self.current_message_index == 3:
            valid = self.is_int(response)
            if valid:
                self.obj.append(int(response))
            else:
                self.display_error(f"Insira um CNPJ válido!\n")
                self.current_message_index -= 1

    def display_next_message(self):
        if self.current_message_index < len(self.messages):
            self.current_message_index += 1
        elif self.current_message_index >= len(self.messages):
            self.input_product()

    def input_product(self):
        response = input("Enter product choice: ")
        if response == "1":
            self.obj.append("Scope")
            self.sprint_messages_scope()

        elif response == "2":
            self.obj.append("IPSEC")
            self.sprint_messages_ipsec()
            
        elif response == "3":
            self.obj.append("Sitef")
            self.sprint_messages_sitef()

    def sprint_messages_scope(self):
        for i in self.messages_scope:
            print(i)

    def sprint_messages_ipsec(self):
        for i in self.messages_ipsec:
            print(i)

    def sprint_messages_sitef(self):
        for i in self.messages_sitef:
            print(i)

    def display_error(self, message):
        print(f"Error: {message}")

    def is_string(self, value):
        valid = value.isdigit()
        return not valid and isinstance(value, str)

    def is_int(self, value):
        valid = value.isdigit()
        return valid

    def get_current_message(self):
        return self.messages[self.current_message_index]

    def save_data_to_json(self):
        data = {
            "Name": self.obj[0] if len(self.obj) > 0 else None,
            "Email": self.obj[1] if len(self.obj) > 1 else None,
            "CNPJ": self.obj[2] if len(self.obj) > 2 else None,
            "Scope": self.obj[3] if len(self.obj) > 3 and "Scope" in self.obj else None,
            "IPSEC": self.obj[4] if len(self.obj) > 4 and "IPSEC" in self.obj else None,
            "Sitef": self.obj[5] if len(self.obj) > 5 and "Sitef" in self.obj else None
        }

        with open("data.json", "w") as json_file:
            json.dump(data, json_file)
