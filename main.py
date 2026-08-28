from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch






llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)

tools = [TavilySearch()]

agent = create_agent(
    model=llm,
    tools=tools
)


def main():
    print("Hello from langchain-course!")

    result = agent.invoke({
        "messages": [
            HumanMessage(
                content="Use the search tool to find the weather in Tokyo."
            )
        ]
    })

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()