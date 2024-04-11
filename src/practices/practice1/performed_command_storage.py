from typing import Optional

import src.practices.practice1.actions as acts

INFO_LIST_CONDITION = """list: {},
list length: {}"""
INFO_AVAILABLE_COMMANDS = """Available commands:
1. insert (position) (value)
2. insert_start (value)
3. insert_end (value)
4. change_position (first position) (second position)
5. add (position) (value)
6. subtract (position) (value)
7. add_to_all (value)
8. subtract_from_all (value)
9. reverse
10. remove (position)
11. undo
12. exit
input: """
ERROR_ACTION_NOT_FOUND = "\nerror: cannot find action {}\n"
ERROR_WRONG_ARGS_TYPE = "\nerror: some arguments are not integers\n"
ERROR_WRONG_INDEX = "\nerror: some index are out of range\n"
ERROR_UNKNOWN = "\nerror: unexpected error occurred, full message:"


class PerformedCommandStorage:
    def __init__(self, given_list: Optional[list] = None) -> None:
        self.commands_list: list = []
        self.object_list: list = given_list if given_list is not None else []

    def apply(self, action: acts.Action) -> None:
        action.apply(self.object_list)
        self.commands_list.append(action)

    def undo(self) -> None:
        if self.is_empty():
            raise ValueError(f"command storage has nothing to undo")
        self.commands_list.pop(-1).undo(self.object_list)

    def is_empty(self) -> bool:
        return not len(self.commands_list)


def main() -> None:
    user_input = [""]
    user_list: list = []
    command_storage = PerformedCommandStorage(user_list)
    while user_input[0] != "exit":
        print(INFO_LIST_CONDITION.format(command_storage.object_list, len(command_storage.object_list)))
        user_input = input(INFO_AVAILABLE_COMMANDS.format(user_list, len(user_list))).split()
        if user_input[0] == "undo":
            try:
                command_storage.undo()
            except ValueError as error:
                print("\nerror:", error, "\n")
            continue
        if user_input[0] == "exit":
            continue
        try:
            action = acts.ACTIONS_REGISTRY.dispatch(user_input[0])
            command_storage.apply(action(*[int(elem) for elem in user_input[1:]]))
        except KeyError:
            print(ERROR_ACTION_NOT_FOUND.format(user_input[0]))
        except ValueError:
            print(ERROR_WRONG_ARGS_TYPE)
        except IndexError:
            print(ERROR_WRONG_INDEX)
        except Exception as error:
            print(ERROR_UNKNOWN, error)


if __name__ == "__main__":
    main()
