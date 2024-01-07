import enum
import logging

file_content_lines: list

logger = logging.getLogger('report_analyzer')


def read_report_file():
    print("Please input crash report file path: ")
    file_path: str = input()

    logger.debug("Reading report file...")
    with open(file_path, 'r', encoding='utf-8') as f:
        global file_content_lines
        file_content_lines = f.readlines()
        logger.debug("Reading complete!")


def start_analyze():
    logger.debug("Starting analyze...")

    locate_result = LocateResult()

    for line in file_content_lines:
        pass


class CrashType(enum):
    # jvm and os
    OUT_OF_MEMORY = "Please check if there is a memory leak, or increase your -Xmx value."
    STACK_OVERFLOW = ("This might be caused by some bugs, if you are sure that is not caused by bugs, please increase "
                      "your stack limit.")
    OTHER_JVM_ERROR = "This might be a random error, please contact mod author or check your jvm."

    # mods
    MOD_REQUIREMENT_ERROR = "Please check your mod requirements."
    MOD_LOADING = "Exception when loading mods, please remove the mod."
    MOD_RUNTIME_SINGLE_ERROR = "Probably caused by a mod which works incorrectly, please contact mod author."
    MOD_RUNTIME_CONFLICT = "Probably caused by mod conflict, you should try to remove one mod."

    # minecraft
    WATCHDOG = "Watchdog was triggered. Probably caused by performance problems."
    ENTITY_ERROR = "Probably caused by a random error, if not, please remove that entity by using world editor."
    BLOCK_ERROR = "Probably caused by a random error, if not, please remove that block by using world editor."
    PLAYER_ERROR = "Probably caused by a random error, if not, please contact that player."


class LocateResult:
    # locating
    description: str
    exception_type: str
    exception_message: str
    exception_stack: str


class AnalyzeResult:
    key_words: list
    crash_type: list[CrashType]

    locate_result = LocateResult()


if __name__ == '__main__':
    logger.level = 10

    read_report_file()
    start_analyze()
