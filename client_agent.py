from src.a2a.a2a_tool_client import A2AToolClient

a2a_client = A2AToolClient()

a2a_client.add_remote_agent("http://localhost:10020")


remote_agents = a2a_client.list_remote_agents()
for k, v in remote_agents.items():
    print(f"Remote agent url: {k}")
    print(f"Remote agent name: {v['name']}")
    print(f"Remote agent skills: {v['skills']}")
    print(f"Remote agent version: {v['version']}")
    print("----\n")
