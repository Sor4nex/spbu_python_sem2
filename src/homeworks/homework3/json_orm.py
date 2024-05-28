import functools
from dataclasses import dataclass
from typing import TypeVar

import lazyparser as lp


@dataclass
class Balance(metaclass=lp.MetaORM):
    money: int
    loan: int
    list_of_accounts: list


@dataclass
class OtherBanks(metaclass=lp.MetaORM):
    bank_name: str
    balance: Balance


@dataclass
class Client(metaclass=lp.MetaORM):
    name: str
    surname: str
    age: int
    other_bank: OtherBanks
    balance: Balance


def main() -> None:
    client1 = Client.from_json("json_examples/ex1.json")
    client2 = Client.from_json("json_examples/ex2.json", strict=True)
    print("client1 fields:", client1.__dict__, isinstance(client1.__dict__["balance"], functools.partial))
    print("client2 fields:", client2.__dict__)
    print(client1.balance)
    print(client2.balance)
    print(client1.dump_to_json())


if __name__ == "__main__":
    main()
