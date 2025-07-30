import json

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    APIKeySecurityScheme, In

)

from src.a2a.agent_executor_service import AgentExecutorService


# Generic function to create an A2A server for any ADK agent


def create_agent_a2a_server(
        agent,
        name,
        description,
        skills,
        host="localhost",
        port=10020,
        status_message="Processing request...",
        artifact_name="response"
):
    capabilities = AgentCapabilities(streaming=True, push_notifications=True)
    agent_card = AgentCard(
        name=name,
        description=description,
        url=f"http://{host}:{port}/",
        version="1.0.0",
        default_input_modes= ["text", "text/plain"],
        default_output_modes=["text", "text/plain"],
        capabilities=capabilities,
        skills=skills,
        security_schemes= {'apiKey':APIKeySecurityScheme(description="API Key for authentication",in_=In.header,name="api_key")}
    )

    # Create Executor with custom parameters
    agent_executor_service = AgentExecutorService(
        agent=agent,
        status_message=status_message,
        artifact_name=artifact_name
    )

    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor_service,
        task_store=InMemoryTaskStore(),
    )

    # Create A2A application
    return A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )
