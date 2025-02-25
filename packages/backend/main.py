from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import openai


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
        try:
            # Initialize OpenAI client
            client = openai.AsyncOpenAI()
            
            # Create a chat completion with streaming
            stream = await client.chat.completions.create(
                model="gpt-4o-mini",  
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Tell me an interesting story about technology, one sentence at a time."}
                ],
                stream=True,
                temperature=0.7,
            )

            # Stream the response
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    await asyncio.sleep(0.1)
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(generate(), media_type='text/event-stream', headers=headers)

@app.get("/api/load")
async def load_endpoint():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
