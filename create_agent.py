from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# 环境变量设置key的方式为：OPENAI_API_KEY
agent = create_agent(
    "openai:gpt-5.4",
    tools=[search, get_weather],
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)

# 显式传入工具调用参数
# llm = ChatOpenAI(
#     model="gpt-5.4",
#     api_key="sk-xxx",   # 👈 关键
# )
# agent = create_agent(
#     llm,
#     tools=[search, get_weather],
#     system_prompt="You are a helpful assistant.",
# )

# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
# )

result = agent.invoke(
    {"messages": [{"role": "user", "content": "search wechat news."}]}
)

print(result["messages"][-1].content_blocks)