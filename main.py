import enum
import json
import logging

file_content_map: dict[int, str]

logger: logging.Logger


def read_report_file():
    print("Please input crash report file path: ")
    file_path: str = input()

    logger.info("Reading report file...")
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content_lines = f.readlines()

        global file_content_map
        file_content_map = dict(zip([x for x in range(1, len(file_content_lines) + 2)], file_content_lines))

        logger.debug("File content map: " + str(file_content_map))
        logger.info("Reading complete!")


def start_analyze():
    logger.info("Starting analyze...")

    logger.info("Start locating...")
    locate_result = LocateResult()

    for num, content in file_content_map.items():
        logger.debug(f'Located at line {num}, content: {content}')

        if content.startswith('Description') and locate_result.description is None:
            locate_result.description = content.replace('Description: ', '')
            logger.info(f'Detected description at line {num}: {locate_result.description}')

            expect_stack_and_msg = file_content_map[num + 2]

            if expect_stack_and_msg.__contains__(":"):
                psd = expect_stack_and_msg.split(': ')

                locate_result.exception_type.append(psd[0])
                logger.info(f'Detect exception_type at line {num + 2}')

                locate_result.exception_message.append(psd[1])
                logger.info(f'Detect exception_msg at line {num + 2}')

        if content.replace(" ", "").startswith('at') and not (locate_result.exception_stack.__contains__(content)):
            locate_result.exception_stack.append(content)
            logger.info(f'Detect exception_stack at line {num}')

    logger.info("Locate finished!")
    logger.debug("Locate result: ")
    logger.debug(locate_result.description)
    logger.debug(json.dumps(locate_result.exception_type))
    logger.debug(json.dumps(locate_result.exception_message))
    logger.debug(json.dumps(locate_result.exception_stack))


class CrashType(enum.Enum):
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
    description: str = None
    exception_type: list[str] = list()
    exception_message: list[str] = list()
    exception_stack: list[str] = list()


class AnalyzeResult:
    key_words: list[str] = list()
    crash_type: list[CrashType] = list()

    locate_result = LocateResult()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S")
    logger = logging.getLogger('report_analyzer')

    read_report_file()
    start_analyze()
