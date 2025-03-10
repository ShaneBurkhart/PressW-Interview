from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from langchain_openai import ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage, AIMessage, SystemMessage
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
            callback = AsyncIteratorCallbackHandler()
            model = ChatOpenAI(
                model="gpt-4o-mini",
                streaming=True,
                temperature=0.8,
                callbacks=[callback],
            )

            # Convert history to LangChain message format
            messages = []
            for msg in history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
                elif msg["role"] == "system":
                    messages.append(SystemMessage(content=msg["content"]))

            # Start the streaming generation
            task = asyncio.create_task(model.agenerate([messages]))

            try:
                async for token in callback.aiter():
                    yield token
                    # await asyncio.sleep(0.2)

                await task  # Ensure the generation completes
            except asyncio.CancelledError:
                # Handle cancellation gracefully
                await task  # Make sure to await cancelled task
                return
            except Exception as e:
                yield f"Error during streaming: {str(e)}"
                return

        except Exception as e:
            yield f"Error during setup: {str(e)}"
            return

    return StreamingResponse(
        generate(), media_type="text/event-stream", headers=headers
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
