## Logger Service Overview

The logging configuration defines how log messages are formatted, where they are sent, and what log levels are captured.

Logging levels (from lowest to highest) are:

```pgsql
DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
```
Logs will only be displayed or written if they meet or exceed the specified level in both the handler and root logger.

---

## Configuration Breakdown

### Formatters

Formatters define how log messages appear.
```json
  "formatters": {
    "simple": {
      "format": "%(asctime)s - %(name)s %(lineno)d - %(levelname)s - %(message)s",
      "datefmt": "%m-%d-%Y %I:%M:%S%p %Z"
    }
```
Example output:

```arduino
11-02-2025 02:15:44PM EST - my_module 42 - INFO - Process started successfully
```

---

### Handlers

Handlers determine where logs are sent (console, file, etc) and which log levels they record.

Console handler:

```json
    "console": {
      "class": "logging.StreamHandler",
      "level": "DEBUG",
      "formatter": "simple",
      "stream": "ext://sys.stdout"
    }
```

- Outputs logs in the terminal (stdout).
- Displays messages at level `DEBUG` or higher (depending on the root logger level).

Info file handler:

```json
    "info_file_handler": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "INFO",
      "formatter": "simple",
      "filename": "logs/info.log",
      "maxBytes": 10485760,
      "backupCount": 20,
      "encoding": "utf8"
    }
```
- Writes logs of `INFO` level or higher to `logs/<name>.log`.
- Rotates the file when it reaches 10mb (maxBytes), keeping a backup of 20. If log is name `app.log`, once max has been reached, then `app2.log`.

Error file handler:

```json
    "error_file_handler": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "ERROR",
      "formatter": "simple",
      "filename": "logs/errors.log",
      "maxBytes": 10485760,
      "backupCount": 20,
      "encoding": "utf8"
    }
```
- Same as the info log handler, except it won't log anything below `ERROR` into the `errors.log`.
- Also uses log rotation for file management.

---

### Loggers

Loggers are name entities used within Python modules.
They control how specific parts of the application handle logging.

```json
"loggers": {
  "my_module": {
    "level": "ERROR",
    "handlers": ["console"],
    "propagate": false
  }
}
```

- To retrieve this logger in code, use:

```python
import logging
logger = logging.getLogger("my_module")
```

- In this example, messages logged through the console will only display `ERROR` or higher.
- This will not `propagate` to the root logger because it is set to false.

What is `propagate`?

Say you have this structure:

```json
"loggers": {
  "my_module": {
    "level": "ERROR",
    "handlers": ["console"],
    "propagate": false
  }
},
"root": {
  "level": "DEBUG",
  "handlers": ["file_handler"]
}
```

With `propagate = false` the message is handled only by `my_module`'s handlers (console in this case). It does not go to the root logger's handlers (so it won't appear in `file_handler`)

---

### Root Logger

The root logger is the default logger for all messages not handled by named loggers.

```json
"root": {
  "level": "DEBUG",
  "handlers": ["console", "info_file_handler", "error_file_handler"]
}
```
- Sends logs to both the console and the two file handlers.
- Controls the minimum threshold for all attached handlers.

Handlers and the root logger work together to determine which messages appear:

| Root Level | Handler Level | Result (Messages That Appear)                |
| ---------- | ------------- | -------------------------------------------- |
| DEBUG      | INFO          | INFO and above                               |
| INFO       | DEBUG         | INFO and above *(DEBUG messages suppressed)* |
| DEBUG      | DEBUG         | All messages (DEBUG and above)               |
| ERROR      | INFO          | Only ERROR and CRITICAL                      |

For example, if the root level is `ERROR`, console handler is `INFO`, and file handler is `CRITICAL`:
- Console handler will only output `ERROR` and above because the root level is `ERROR`.
- File handler will only output `CRITICAL` even though the root level is `ERROR`

---

### Recommended Usage

- For normal operations, set the root level to `INFO` and handlers to `DEBUG`.
> Unless you want your file handlers outputting certian log levels to certain log files, example `errors.log` or `criticals.log`.
- For debugging, set the root level to `DEBUG`.

For usage in code:

```python
import logging
from logger_service import setup_logging # This is a module I created.

logger = logging.getLogger(__name__)
setup_logging()

def function():
  logger.info("starting function")
  a + b = c
  logger.info("finished function")

if __name__ == "__main__":
  function()
```

---

### References

[Good logging practice in Python](https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/)

