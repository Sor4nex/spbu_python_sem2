from dataclasses import dataclass
from typing import TypeVar

import lazyparser as lp


@dataclass
class Balance(metaclass=lp.MetaDataclass):
    money: int
    loan: int
    list_of_accounts: list


@dataclass
class OtherBanks(metaclass=lp.MetaDataclass):
    bank_name: str
    balance: Balance


@dataclass
class Client(metaclass=lp.MetaDataclass):
    name: str
    surname: str
    age: int
    other_bank: OtherBanks
    balance: Balance


def main() -> None:
    client1 = lp.parse_class_from_json(Client, "json_examples/ex1.json")
    client2 = lp.parse_class_from_json(Client, "json_examples/ex2.json", strict=True)
    print("client1 fields:", client1.__dict__)
    print("client2 fields:", client2.__dict__)
    print(client1.balance)
    print(client2.balance)
    print(lp.dump_class_to_json(client1))


if __name__ == "__main__":
    main()
