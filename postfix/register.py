from dataclasses import dataclass


class RegisterDoesntExist(Exception):
    pass


class NoRegistersAvailable(Exception):
    pass 


@dataclass
class Register:
    id: int
    content: int = 0
    in_use: bool = False
    
    def __str__(self) -> str:
        return f'r{self.id}'

