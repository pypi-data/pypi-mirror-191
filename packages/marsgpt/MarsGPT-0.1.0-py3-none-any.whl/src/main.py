import sys
import asyncio
from MarsGPT import Chatbot

async def main():
    """
    Chat AI Test
    """
    # params
    email = "xxx@xxx.com"
    password = "xxxxxxx"

    # login
    chatbot = Chatbot(email=email, password=password)
    
    # ask
    try:
        while True:
            print("You:")
            prompt = ""
            while(len(prompt.strip()) == 0):
                prompt = input()

            # # clear
            # chatbot.conversations.remove("default")

            print("ChatGPT:")
            async for line in chatbot.ask(prompt):
                result = line["choices"][0]["text"].replace("<|im_end|>", "")
                print(result, end="")
                sys.stdout.flush()
            print()


    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
    