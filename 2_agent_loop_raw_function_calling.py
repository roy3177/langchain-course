from dotenv import load_dotenv
from langsmith import traceable
import ollama

MAX_ITERATIONS = 10
MODEL = "qwen3:1.7b"

load_dotenv()


# ----- Tools (Langchain  @tool  decorator) -----

@traceable(run_type="tool")
def get_product_price(product:str)-> float:
    """Look up the price of the product in the catalog."""
    print(f" >> executing get_product_price (product='{product}')")
    prices={"laptop":1299.99, "headphones": 145.95, "keyboard":89.50} 
    return prices.get(product,0)

@traceable(run_type="tool")
def apply_discount(price:float, discount_tier:str)->float:
    """Apply a discount tier to a price and return the final price.
       Available tiers: bronze, silver, gold."""
    print(f" >> Executing apply_discount (price={price}, discount_tier='{discount_tier}')")
    discount_precenteges={"bronze": 5, "silver":12, "gold":23}
    discount=discount_precenteges.get(discount_tier,0)
    return round(price*(1-discount/100),2)

# Difference 2 : without @tool, we must MANUALLY deine the JSON schema for each function.
# This is exactly what LangChain's @tool decorator generates automatically from the function's type hints and docstring.

tools_for_llm = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Look up the price of the product in the catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {"type": "string", "description": "The name of the product to look up."}
                },
                "required": ["product"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "apply_discount",
            "description": "Apply a discount tier to a price and return the final price. Available tiers: bronze, silver, gold.",
            "parameters": {
                "type": "object",
                "properties": {
                    "price": {"type": "number", "description": "The original price of the product."},
                    "discount_tier": {"type": "string", "description": "The discount tier to apply (bronze, silver, gold)."}
                },
                "required": ["price", "discount_tier"]
            }
        }
    }
]
# --Helper : traced ollama call --
# Difference 3 : without langchain, we must manually trace LLM calls for langsmith.

@traceable(name="Ollama Chat", run_type="llm")
def ollama_chat_traced(messages):
    return ollama.chat(model=MODEL, tools=tools_for_llm, messages=messages, options={"temperature": 0.0})

# ----- Agent Loop -----

@traceable(name="Ollama Agent Loop")
def run_agent(question:str):
    tools_dict={
        "get_product_price": get_product_price,
        "apply_discount": apply_discount
    }

 
    print(f"Question: {question}")
    print("="*60)

    messages= [
        {
            "role": "system",
            "content": (
                "You are a helpful shopping assistant."
                "You have access to a product catalog tool and discount tool. \n\n"
                "STRICT RULES- you must follow these exactly:\n" 
                "1. NEVER guess or assume any product price." 
                "You MUST call get_product_price first to get the real price. \n"
                "2. Only call apply_discount AFTER you have received a price from get_product_price. Pass the exact price" \
                "returned by get_product_price - do NOT pass a made-up number. \n"
                "3. NEVER calcu;ate discounts yourself using math. "
                "Always use the apply_discount tool \n." \
                "4. If the user does not specify a discount tier, " \
                "ask them which tier to use - do NOT assume one."
            )
        },
        {"role":"user", "content":question},
    ]

    for iteration in range(1, MAX_ITERATIONS + 1): 
        print(f"\n --- Iteration {iteration} ---")

        response=ollama_chat_traced(messages)
        ai_message=response.message

        tool_calls=ai_message.tool_calls

        # If no tool calls, this is the final answer
        if not tool_calls:
            print(f"Final Answer: {ai_message.content}")
            return ai_message.content

        # Process only the FIRST tool call - force one tool per iteration:
        tool_call = tool_calls[0]
        
        # Access attributes directly from the Ollama ToolCall object
        tool_name = tool_call.function.name
        tool_args = tool_call.function.arguments

        print(f"  [Tool Selected] {tool_name} with args: {tool_args}")

        tool_to_use = tools_dict.get(tool_name)
        if tool_to_use is None:
            raise ValueError(f"Tool '{tool_name}' not found")

        # Execute standard Python function directly
        observation = tool_to_use(**tool_args)

        print(f"  [Tool Result] {observation}")
        
        # Append standard Ollama message format back to context
        messages.append(ai_message)
        messages.append({
            "role": "tool",
            "tool_name": tool_name,
            "content": str(observation),
        })

    print("ERROR: Max iterations reached without a final answer.")
    return None


if __name__=="__main__":
    print("Hello LangChan  Agent (.bind_tools) !")
    print()
    result=run_agent("What is the price of a laptop after applying a gold discount?")
