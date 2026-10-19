from contextlib import asynccontextmanager
from fastapi import FastAPI
from storage import  StorageConfig

from app.core.config import get_settings
from app.storage.storage_gatway import Storage

settings = get_settings()

config = StorageConfig(
  provider= settings.PROVIDER,
  bucket= settings.BUCKET,
  s3_endpoint_url= settings.ENDPOINT_URL,
  s3_access_key= settings.ACCESS_KEY,
  s3_secret_key= settings.SECRET_KEY,
  ttl_days= settings.TTL,
)

storage = Storage(config= config)

@asynccontextmanager
async def lifespan(app: FastAPI):
  # --- STARTUP LOGIC ---
  print("Application is starting up!")

  storage.cleanup(interval= 3600)
  yield
  
  # --- SHUTDOWN LOGIC ---
  print("Application is shutting down!")

app = FastAPI(title= settings.APP_NAME, lifespan= lifespan)


@app.get("/health")
def health():
  return {
    "status": "ok"
  }