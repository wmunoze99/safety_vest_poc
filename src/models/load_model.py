from ultralytics import YOLO
from ..utils.loggerConfiguration import Logger

logger = Logger().logger

logger.info("Loading model...")
model = YOLO("./src/models/Safety Vest 3.pt")
logger.info("Model loaded")
