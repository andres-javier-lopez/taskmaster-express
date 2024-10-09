import logging

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

from taskmasterexp.auth.dependencies import CurrentUserWA, CurrentUserWS
from taskmasterexp.helpers import get_current_time, get_weekday
from taskmasterexp.schemas.tasks import Task
from taskmasterexp.schemas.users import User
from taskmasterexp.settings import DEMO_PHONE_NUMBERS

from .client import get_chat_model
from .demo import get_demo_chat_agent
from .tools import tools

logger = logging.getLogger(__name__)


human_template = "{text}"


async def _get_chat_agent(user: User) -> AgentExecutor:
    logger.info(f"Getting chat prompt for user {user.uuid}")

    task_template = "[title]\n[description]\nStatus: [status]\n"

    if not user.email:
        email_message = (
            "The user does not have an email address associated,"
            " ask for an email address when you greet them."
            " Be polite and only ask once."
        )
    else:
        email_message = (
            "The user already has an email address, "
            "we won't be able to associate a new one"
        )

    messages = [
        ("system", "You are a helpful assistant"),
        ("system", "You are helping the user to organize their tasks"),
        ("system", "The url for the aplication is https://helpitdone.com"),
        ("system", f"The user's uuid is {user.uuid}"),
        ("human", f"My name is {user.name}"),
        ("system", f"The task format is: <{Task.ai_format_template()}>"),
        ("system", "You will list the tasks as: \n1.[title]\n2.[title]\n..."),
        ("system", "If the task list is empty you will say that there are no tasks"),
        (
            "system",
            "When giving more details about a tasks "
            f"you will present them as {task_template}.",
        ),
        ("system", "Greet back the user, only provide task information if asked"),
        ("system", "Don't guess the date, use the 'get_current_time' tool instead"),
        (
            "system",
            "When using a tool always use the task's uuid provided by 'get_task_list' "
            "as the 'task_id'. Don't guess the task's uuid.",
        ),
        (
            "system",
            "Always get the task's updated information before providing information "
            "or interacting with the task, use the 'get_task_list' tool to get "
            "the list of tasks, or the 'get_task' tool to get a specific task.",
        ),
        (
            "system",
            "Only mark a task as done if the user has already done it, "
            "if the user says that it *will* or *should* do it, set a due date instead."
            "If you are not sure, ask for confirmation.",
        ),
        ("system", f"Today is {get_weekday()}, {get_current_time()}"),
        ("system", email_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
    logger.info(messages)

    chat_prompt = ChatPromptTemplate.from_messages(messages)

    agent = create_openai_tools_agent(get_chat_model(), tools, chat_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


async def get_chat_agent(
    user: CurrentUserWS,
) -> AgentExecutor:
    return await _get_chat_agent(user)


async def get_whatsapp_chat_agent(
    user: CurrentUserWA,
) -> AgentExecutor:
    if user.phone_number in DEMO_PHONE_NUMBERS:
        return await get_demo_chat_agent(user)
    return await _get_chat_agent(user)
