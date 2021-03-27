class Logger:
    max_level = 0  # Do not print messages with a level higher than this max_level

    @staticmethod
    def log(msg: str, level: int = 0):
        if level <= Logger.max_level:
            print('    ' * level + msg)


if __name__ == '__main__':
    Logger.max_level = 1
    Logger.log("Let's start", level=0)
    Logger.log('Hello world', level=1)
    Logger.log('The quick brown fox jumps over the lazy dog', level=2)
