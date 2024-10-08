import logging

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

from taskmasterexp.schemas.users import User
from taskmasterexp.settings import DEMO_TOPIC

from ..client import get_chat_model
from ..tools import get_current_time

logger = logging.getLogger(__name__)


human_template = "{text}"


async def get_demo_chat_agent(user: User) -> AgentExecutor:
    logger.info("Starting a demo chat agent")

    messages = [
        ("system", "You are a helpful assistant"),
        (
            "system",
            "You are doing a demo for the user and you will tell them that this is a demo",
        ),
        ("human", f"My name is {user.name}"),
        ("system", f"You are an expert on {DEMO_TOPIC}"),
        ("system", "You should answer in less than 1300 characters"),
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]

    tools = [get_current_time]

    chat_prompt = ChatPromptTemplate.from_messages(messages)

    agent = create_openai_tools_agent(get_chat_model(), tools, chat_prompt)

    return AgentExecutor(agent=agent, tools=tools, verbose=True)
