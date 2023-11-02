from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import shortuuid
from furl import furl

PROTOCOL: str = "http"
BASE_URL: str = "localhost"
PORT: int = 8000
APP_ENDPOINT = furl(f"{PROTOCOL}://{BASE_URL}:{PORT}")

app = FastAPI()

url_mappings = {}


class URL(BaseModel):
    url: HttpUrl


@app.post("/shorten", response_model=URL)
async def shorten_url(url_item: URL) -> URL:
    short_key = shortuuid.uuid()[:8]
    short_url = f"http://your_domain/{short_key}"
    url_mappings[short_key] = url_item.url
    return URL(url=short_url)


@app.get("/{short_key}")
async def redirect_to_original(short_key: str):
    if short_key not in url_mappings:
        raise HTTPException(status_code=404, detail="Short URL not found")
    long_url = url_mappings[short_key]
    return {"message": "Redirecting...", "url": long_url}
