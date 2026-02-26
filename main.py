from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from scraper_engine import parse_list_am_generator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/start")
def start_scraping(
    keyword: str = Query(...),
    max_price: int = Query(...),
    max_pages: int = Query(...),
    crc: int = Query(0), # 0 = AMD, 1 = USD
    tg_token: str = Query(""),
    tg_chat_id: str = Query("")
):
    def event_generator():
        for json_str in parse_list_am_generator(keyword, max_price, max_pages, crc, tg_token, tg_chat_id):
            yield f"data: {json_str}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Redirect root to index.html
from fastapi.responses import RedirectResponse
@app.get("/")
def redirect_root():
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
