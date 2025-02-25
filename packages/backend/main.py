from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/test")
async def test_endpoint():
    headers = {
        "Access-Control-Allow-Origin": "*",  # In production, replace with specific origins
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }

    async def generate():
        for i in range(10):
            yield f"Message {i + 1}\n"
            await asyncio.sleep(1)

    return StreamingResponse(generate(), media_type='text/event-stream', headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
