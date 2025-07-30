from a2a.types import AgentSkill

from src.a2a.a2a_server import create_agent_a2a_server
from src.agent.chat_agent import chat_agent
import uvicorn

from src.auth.oauth2_middleware import OAuth2Middleware

chat_agent_server = create_agent_a2a_server(
    agent=chat_agent,
    name="Intelligent conversation agent",
    description="Intelligent Chat Agent with Web Search Integration",
    skills=[
        AgentSkill(
            id="intelligent_conversation_agent",
            name="Intelligent_conversation_agent",
            description="Intelligent Chat Agent with Web Search Integration",
            tags=["answers", "questions", "conversations"],
            examples=[
                "Best places to visit in the India",
                "Best restaurants Noida near sector 75",
                "Best movies to watch in 2025",
            ],
        )
    ],
    host="localhost",
    port=10020,
    status_message="typing.............",
    artifact_name="conversation_artifact"
)


app = chat_agent_server.build()

# app.add_middleware(
#     OAuth2Middleware,
#     agent_card=chat_agent_server.agent_card,
#     public_paths=['/.well-known/agent.json'],
# )

uvicorn.run(app, host="localhost", port=10020)