from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from langserve.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langserve import add_routes
from Model import chain as chat_chain

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/chat/playground")


class InputChat(BaseModel):
    """Input for the chat endpoint."""
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )


def message_to_dict(message: BaseMessage) -> dict:
    """Convert message to dictionary for processing."""
    return {
        "type": message.type,
        "content": message.content,
    }


def dict_to_message(message_dict: dict) -> BaseMessage:
    """Convert dictionary back to message."""
    message_type = message_dict["type"]
    if message_type == "human":
        return HumanMessage(content=message_dict["content"])
    elif message_type == "ai":
        return AIMessage(content=message_dict["content"])
    elif message_type == "system":
        return SystemMessage(content=message_dict["content"])
    else:
        raise ValueError(f"Unknown message type: {message_type}")


def process_input_chat(input_chat: InputChat) -> List[BaseMessage]:
    """Process input chat to convert messages to appropriate types."""
    return [dict_to_message(message_to_dict(message)) for message in input_chat.messages]


add_routes(
    app,
    chat_chain.with_types(input_type=InputChat),
    path="/chat",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type="chat",
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
