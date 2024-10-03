import datetime
import os

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from ..models.load_model import model
import cv2
import numpy as np
from tempfile import NamedTemporaryFile

router = APIRouter()


def generate_video_stream(temp_file_path: str):


    cap = cv2.VideoCapture(temp_file_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        # for result in results:
        #     x1, y1, x2, y2 = result.xyxy[0]
        #     label = result.names[0]
        #     confidence = result.confidence[0]
        #
        #     cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        #     cv2.putText(frame, f'{label} {confidence:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
        #                 (255, 0, 0), 2)

        annotated_frame = results[0].plot()
        _, jpeg_frame = cv2.imencode('.jpg', annotated_frame)

        # Yield the frame to be streamed
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame.tobytes() + b'\r\n\r\n')

    cap.release()
    os.remove(temp_file_path)


@router.get("/stream")
async def stream_video(path: str = ""):
    if not path:
        return 1

    return StreamingResponse(generate_video_stream(path), media_type="multipart/x-mixed-replace; boundary=frame")


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    video_data = file.file.read()

    with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        # Write the uploaded file content to the temporary file
        temp_file.write(video_data)
        temp_file_path = temp_file.name

    return {
        "path": temp_file_path
    }
