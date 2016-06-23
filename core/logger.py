import logging

log_format = logging.Formatter('%(asctime)s -- %(message)s')

def CreateLogger(toconsole=True, tofile=True, filepath=None, level='WARNING', logID="pi_control"):
    try:
        if filepath is None:
            filepath = "/tmp/" + logID + ".log"
            print("Using temporary log file - " + filepath)

        # Create logger instance
        logger = logging.getLogger(logID)
        SetLevel(logger, level)

        if toconsole:
                ## Console Output
                log_out_console = logging.StreamHandler()

                SetLevel(log_out_console, level)
                assert SetLevel, "Error: Failed to set console logging level"

                log_out_console.setFormatter(log_format)
                logger.addHandler(log_out_console)

        if tofile:
                ## File output
                log_out_file = logging.FileHandler(filepath)

                SetLevel(log_out_file, level)
                assert SetLevel, "Error: Failed to set file logging level"

                log_out_file.setFormatter(log_format)
                logger.addHandler(log_out_file)

        if not toconsole and not tofile:
            assert False, "Error: No log output set - must be at least one"

        return logger

    except:
        return False


# Set logging level
def SetLevel(log_output, level):
    try:
        if level == 'CRITICAL':
            log_output.setLevel(logging.CRITICAL)
        elif level == 'ERROR':
            log_output.setLevel(logging.ERROR)
        elif level == 'WARNING':
            log_output.setLevel(logging.WARNING)
        elif level == 'INFO':
            log_output.setLevel(logging.INFO)
        elif level == 'DEBUG':
            log_output.setLevel(logging.DEBUG)
        else:
            assert False, "Error: Invalid logging level"

        return True

    except:
        return False
