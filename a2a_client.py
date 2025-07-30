from src.a2a.a2a_tool_client import A2AToolClient


async def main():
    agent_url = "http://localhost:10020"
    #agent_gateway_url = "http://localhost:3000"
    a2a_client = A2AToolClient()
    a2a_client.add_remote_agent(agent_url)
    remote_agents = a2a_client.list_remote_agents()
    for k, v in remote_agents.items():
        print(f"Remote agent url: {k}")
        print(f"Remote agent name: {v['name']}")
        print(f"Remote agent skills: {v['skills']}")
        print(f"Remote agent version: {v['version']}")
        print("----\n")

    question = "What are the best place to visit in the India?"
    print(f"Question: {question}")
    response = await a2a_client.create_task(agent_url, question, api_key="12345")
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
