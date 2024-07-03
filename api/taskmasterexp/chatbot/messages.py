import logging
from typing import Annotated

from fastapi import APIRouter, Form, status
from twilio.rest import Client

from taskmasterexp.settings import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    WHATSAPP_NUMBER,
)

from .dependencies import WhatsAppAgent

logger = logging.getLogger(__name__)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

router = APIRouter(prefix="/messages", tags=["messages"])


def _send_message(text: str, destination: str):
    client.messages.create(
        from_=f"whatsapp:{WHATSAPP_NUMBER}", body=text, to=destination
    )


@router.post("/webhook", status_code=status.HTTP_204_NO_CONTENT)
async def receive_message(
    agent: WhatsAppAgent,
    From: Annotated[str, Form()],
    Body: Annotated[str, Form()],
):
    logger.info(f"Received message: {Body}")
    response = await agent.ainvoke(
        {
            "history": [],
            "text": Body,
        }
    )
    _send_message(response["output"], destination=From)
