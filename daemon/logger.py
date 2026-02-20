import logging
import sys

# Simple ANSI color codes
RESET = "\033[0m"
COLORS = {
    "DAEMON": "\033[36m",  # cyan
    "WEB": "\033[35m",  # magenta
    "DEBUG":   "\033[90m",  # grey
    "INFO":    "\033[32m",  # green
    "WARNING": "\033[33m",  # yellow
    "ERROR":   "\033[31m",  # red
    # "CRITICAL": ""
}

class ColorFormatter(logging.Formatter):
	def __init__(self, service_name: str):
		fmt = "%(asctime)s [%(service)s] %(levelname)s: %(message)s"
		super().__init__(fmt)
		self.service_name = service_name

	def format(self, record: logging.LogRecord) -> str:
		if self.service_name == "DAEMON":
			record.service = f"{COLORS['DAEMON']}{self.service_name}{RESET}"
		else:
			record.service = f"{COLORS['WEB']}{self.service_name}{RESET}"

		# Colorize level name
		level = record.levelname
		color = COLORS.get(level, "")
		record.levelname = f"{color}{level}{RESET}" if color else level

		return super().format(record)

def setup_loggin_config(service_name: str):
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(ColorFormatter(service_name))

	root = logging.getLogger()
	root.handlers.clear()
	root.setLevel(logging.INFO)
	root.addHandler(handler)