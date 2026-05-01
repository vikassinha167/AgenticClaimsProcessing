from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

endpoint = "https://thepracticaledu-foundry.services.ai.azure.com/api/projects/tpe-project"

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = "nEWAGENT"

# Creating a new agent
new_agent = project_client.agents.create_version(
    agent_name=my_agent,
    definition=PromptAgentDefinition(
        kind="prompt",
        model="gpt-4o",
        instructions="You are a healthcare claims assistant.",
    ),
    description="Created programmatically by the sample script",
)

print(f"Created agent version: {new_agent.version}, id: {new_agent.id}")


# Invoking the agent
my_version = new_agent.version

openai_client = project_client.get_openai_client()

# Reference the agent to get a response
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Tell me what you can help with."}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
)

print(f"Response output: {response.output_text}")




