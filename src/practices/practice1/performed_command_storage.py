from typing import Optional

import src.practices.practice1.actions as acts

INFO_LIST_CONDITION = """list: {},
list length: {}"""
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


def prepare_commands_string() -> str:
    result_str = """Available commands:
0. exit"""
    for i, command in enumerate(acts.ACTIONS_REGISTRY.registry.keys()):
        result_str += f"\n{i+1}. {command}"
    result_str += "\ninput: "
    return result_str


def main() -> None:
    user_input = [""]
    user_list: list = []
    command_storage = PerformedCommandStorage(user_list)
    info_available_commands_str = prepare_commands_string()
    while user_input[0] != "exit":
        print(INFO_LIST_CONDITION.format(command_storage.object_list, len(command_storage.object_list)))
        user_input = input(info_available_commands_str.format(user_list, len(user_list))).split()
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
