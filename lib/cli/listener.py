command_list = {
    ":q!": exit
}


class Listener:
    def __init__(self) -> None:
        pass
    
    def parse_command(self, command:str):
        command_list[command]()

    def listen(self, prompt:str) -> dict:
        response = input(f"{prompt} > ")

        # We have potentially used a command
        if response[0] == ":":
            self.parse_command(response)

        return response
        