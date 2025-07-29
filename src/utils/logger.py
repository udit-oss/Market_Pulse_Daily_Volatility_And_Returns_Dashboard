import logging
from pathlib import Path

def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    A simple logger that writes INFO+ to both:
     • stdout (console)
     • logs/pipeline.log (persistent file)
    """

    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(ch)

        fh = logging.FileHandler(log_dir / "pipeline.log")
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(fh)

    return logger