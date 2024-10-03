from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .utils.loggerConfiguration import configure_logger_format

from .routes import predict

origins = ['*']

configure_logger_format("fastapi")

app = FastAPI(root_path='/api/v1')

app.add_middleware(CORSMiddleware,
                   allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


app.include_router(predict.router)


@app.get("/")
def health():
    return {"Server": "Ok", "version": "1.0.0", "health": "ok"}

