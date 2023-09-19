import loguru


def setup_logging():
    # Remove default handler. We don't want to log to the console.
    # loguru.logger.remove()
    # Add a file handler to log to a file
    loguru.logger.add(
        sink="/logs/{time}.log",
        rotation="1 day",
        retention="10 days",
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )
    # Add a handler to log to the console
    loguru.logger.add(
        sink="stdout",
        level="INFO",
        format="{time} {level} {message}",
        backtrace=True,
        diagnose=True,
    )

    return loguru.logger
