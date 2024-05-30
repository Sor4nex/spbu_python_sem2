import functools
import json
from dataclasses import dataclass
from typing import TypeVar

import lazyparser as lp


@dataclass
class Balance(lp.JsonORM):
    money: int
    loan: int
    list_of_accounts: list


@dataclass
class OtherBanks(lp.JsonORM):
    bank_name: str
    balance: Balance


@dataclass
class Client(lp.JsonORM):
    name: str
    surname: str
    age: int
    other_bank: OtherBanks
    balance: Balance


def main() -> None:
    json_dict1 = json.load(open("json_examples/ex1.json"))
    json_dict2 = json.load(open("json_examples/ex2.json"))
    client1 = Client.from_json_dict(json_dict1)
    client2 = Client.from_json_dict(json_dict2, strict=True)
    print("client1 fields:", client1.__dict__)
    print("client2 fields:", client2.__dict__)
    print(client1.balance)
    print(client2.balance)
    print(client1.dump_to_json())


if __name__ == "__main__":
    main()
