from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from deepagents.backends import StateBackend
from langgraph.checkpoint.memory import MemorySaver
from deepagents.backends.utils import create_file_data
from langchain_quickjs import CodeInterpreterMiddleware
from pathlib import Path
from deepagents.backends import FilesystemBackend
from skills.weather.weather import get_weather as weather_tool

# state backend 适合在内存中动态创建和修改技能文件，或者从网络等非文件系统来源加载技能
backend = StateBackend() 
# 也可以使用 FilesystemBackend 来直接从本地文件系统加载技能
# backend = FilesystemBackend(
#     root_dir="."
# )
checkpointer = MemorySaver()

# -------------------------
# 自动加载 skills 目录
# -------------------------
skills_files = {}
skills_root = Path("./skills")
for skill_file in skills_root.rglob("SKILL.md"):
    # skills/weather/SKILL.md
    relative_path = skill_file.as_posix()
    # /skills/weather/SKILL.md
    virtual_path = f"/{relative_path}"
    print(f"加载 Skill: {virtual_path}")
    skills_files[virtual_path] = create_file_data(
        skill_file.read_text(encoding="utf-8")
    )
print(f"\n共加载 {len(skills_files)} 个 Skill")
print("-" * 50)

agent = create_deep_agent(
    model="openai:gpt-5.4",  # 或 gpt-4o / gpt-5.x
    backend=backend,
    # skills=["/skills"],  # ⭐ 自动扫描 skills 目录 需要结合 FilesystemBackend
    skills=["/skills/"],  # ⭐ 显式指定技能文件路径 需要结合 StateBackend
    tools=[weather_tool],
    checkpointer=checkpointer,
    middleware=[CodeInterpreterMiddleware(skills_backend=backend)], # for interpreter skills
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "广州天气怎么样"
            }
        ],
        "files": skills_files, # 将技能文件注入到 agent 的调用上下文中 StateBackend 必须
    },
    config={
        "configurable": {
            "thread_id": "12345"
        }
    }
)
# print("\n结果：", result)
print(result["messages"][-1].content)
