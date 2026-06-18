import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    handlers=(logging.StreamHandler(), logging.FileHandler('logs/app.log', 'w')))

logger = logging.getLogger()