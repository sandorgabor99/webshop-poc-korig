import logging
from logging.handlers import RotatingFileHandler


def setup_logging() -> None:
	logger = logging.getLogger("auth")
	if logger.handlers:
		return
	logger.setLevel(logging.INFO)

	formatter = logging.Formatter(
		"%(asctime)s | %(levelname)s | %(name)s | %(message)s"
	)

	file_handler = RotatingFileHandler(
		"auth.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
	)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)

	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(formatter)
	logger.addHandler(stream_handler)


def get_auth_logger() -> logging.Logger:
	return logging.getLogger("auth")
