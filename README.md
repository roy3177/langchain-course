# LangChain Course

A short learning project demonstrating basic usage of [LangChain](https://python.langchain.com/).

## What's here right now

The current part ([main.py](src/langchain_course/main.py)) builds a simple "chain" that demonstrates the core LangChain idea — wiring a prompt template together with a language model:

1. **`PromptTemplate`** — defines a text template with a variable (`{information}`) asking the model to produce a short summary and two interesting facts about a person, given some text about them (currently a text snippet about Elon Musk).
2. **Language model (LLM)** — `ChatGoogleGenerativeAI` (Gemini). There's also a commented-out line (`# llm=ChatOllama(...)`) showing how to run a local model via Ollama instead of calling an external API.
3. **Composing the chain** — the prompt and the model are wired together using LangChain's pipe syntax (`prompt | llm`), and the chain is run with `chain.invoke(...)`.

In short: this is a "Hello World" example for LangChain — text input → structured prompt → model call → response.

## Running

```bash
uv run langchain-course
```

Environment variables (such as a Google API key) need to be set in a `.env` file.
