from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
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


@app.post("/api/chat")
async def chat_endpoint(request: Request):
    headers = {
        "Access-Control-Allow-Origin": "*",  # In production, replace with specific origins
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }

    # Make sure chat history is not empty
    data = await request.json()
    history = data.get("history")
    if not history:
        # Return a 400 error
        return JSONResponse(status_code=400, content={"error": "Chat history is empty"})

    if len(history) == 0:
        # Return a 400 error
        return JSONResponse(status_code=400, content={"error": "Chat history is empty"})

    # If last message is not a user message, return a 400 error
    if history[-1]["role"] != "user":
        return JSONResponse(
            status_code=400, content={"error": "Last message is not a user message"}
        )

    cleaned_history = [
        {"role": message["role"], "content": message["content"]} for message in history
    ]

    async def generate():
        try:
            # Initialize OpenAI client
            client = openai.AsyncOpenAI()

            # Create a chat completion with streaming
            stream = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=cleaned_history,
                stream=True,
                temperature=0.8,
            )

            # Stream the response
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    await asyncio.sleep(0.1)
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(
        generate(), media_type="text/event-stream", headers=headers
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
