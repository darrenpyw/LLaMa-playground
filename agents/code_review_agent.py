import requests
from ToolAgents.provider import OpenAIChatAPI
from ToolAgents.agents import ChatToolAgent
from ToolAgents.data_models.messages import ChatMessage

def main():
    # Local OpenAI-compatible API, like vllm or llama-cpp-server
    api = OpenAIChatAPI(
        api_key="token-abc123",
        base_url="http://127.0.0.1:8000/v1",
        model="unsloth/gemma-4-E2B-it-GGUF",
        )
    # Create the ChatAPIAgent
    agent = ChatToolAgent(chat_api=api)

   
    cm = ChatMessage.create_user_message("Analyze the file for security misconfigurations")
    cm.add_text_file_data(file="..\\samples\\nginx.conf")
    
    messages = [
        ChatMessage.create_system_message("You are a cyber security expert in reviewing source code and infrastructure configurations. Respond with professional tone and do not use emojis"),
        cm,
    ]
    
    result = agent.get_streaming_response(
        messages=messages
       
    )

    for res in result:
        print(res.chunk, end='', flush=True)


if __name__ == "__main__":
    main()