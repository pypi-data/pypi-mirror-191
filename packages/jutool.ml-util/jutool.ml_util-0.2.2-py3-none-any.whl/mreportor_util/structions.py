import abc
from enum import Enum
from code_util.markdown import markdowndoc


class node_state_enum(Enum):
    Notset = 1
    Completed = 2
    InWork = 3
    Abandon = 4
    InOptimize = 5


class node_base(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def Name() -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def Version() -> int:
        pass

    @staticmethod
    @abc.abstractmethod
    def from_node() -> type:
        pass

    @staticmethod
    @abc.abstractmethod
    def from_node_message() -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def target_node() -> type:
        pass

    @staticmethod
    @abc.abstractmethod
    def target_message() -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def base_node() -> type:
        pass

    @staticmethod
    def state() -> node_state_enum:
        return node_state_enum.Notset


class goal_mark(node_base):
    @staticmethod
    def base_node() -> type:
        return None


class goal_mark_start(goal_mark):
    @staticmethod
    def target_node() -> type:
        return None

    @staticmethod
    def target_message() -> str:
        return None

    @staticmethod
    def Name() -> str:
        return "Start"

    @staticmethod
    def Version() -> int:
        return 0

    @staticmethod
    def from_node() -> type:
        return None

    @staticmethod
    def from_node_message() -> str:
        return ""


class mind_step(node_base):
    pass


class act_step(node_base):

    @staticmethod
    def from_node() -> type:
        return None

    @staticmethod
    def from_node_message() -> str:
        return None

    @staticmethod
    def target_node() -> type:
        return None

    @staticmethod
    def target_message() -> str:
        return None

    @staticmethod
    def key_methods() -> []:
        return []

    @staticmethod
    def work_timespan() -> (str, str):
        return None

    @staticmethod
    def optimize_timespans() -> {str: (str, str)}:
        return None

    @staticmethod
    def custom_out(doc: markdowndoc) -> bool:
        return False
