import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

async def main():
    print("1. MCP client bana raha hoon...", flush=True)
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    print("2. Tools la raha hoon...", flush=True)
    tools = await client.get_tools()
    print("3. Tools mil gaye:", [t.name for t in tools], flush=True)

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    agent = create_agent(model, tools)

    print("4. Model ko question bhej raha hoon...", flush=True)
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    print("5. Jawab:", result["messages"][-1].content, flush=True)

if __name__ == "__main__":
    asyncio.run(main())