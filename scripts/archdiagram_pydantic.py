from pydantic_ai import Agent, CodeExecutionTool
from pydantic_ai.models.openai import OpenAIResponsesModelSettings
from dotenv import load_dotenv

load_dotenv()

model_settings = OpenAIResponsesModelSettings(
    openai_include_code_execution_outputs=True
)
agent = Agent[None, str](
    "openai-responses:gpt-5.1",
    builtin_tools=[CodeExecutionTool()],
    model_settings=model_settings,
)

result = agent.run_sync(
    "Your job is to return an image of the architecture diagram. To do that you should use python diagrams library to generate the diagram. Then you should run the code to generate the image. You might have to install the diagrams library first."
)
print(result.output)
print("--------------------------------")
print(result.response.builtin_tool_calls)
print("--------------------------------")
print(result)
print("--------------------------------")
