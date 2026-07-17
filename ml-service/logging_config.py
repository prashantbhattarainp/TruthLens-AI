import logging


def configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        force=True,
    )


def get_logger() -> logging.Logger:
    return logging.getLogger('truthlens.ml_service')
