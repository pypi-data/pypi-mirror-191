from typing import Dict, Union


class BaseSsdb:

    def auth(self, password: str) -> bool:
        """
        Auth this ssdb with the given password

        :param password: the given password
        :return: True if auth successfully or there is no password required
        """
        pass

    def info(self) -> Dict[str, str]:
        """
        Get the detail information about this ssdb server.

        :return: Dict[str, str]
        """
        pass

    def dbsize(self) -> int:
        """
        Get the approximate size of this ssdb server

        :return: size in bytes
        """
        pass

    def execute_command(self, cmd: str, *args) -> Union[None, list, int, bool]:
        pass
