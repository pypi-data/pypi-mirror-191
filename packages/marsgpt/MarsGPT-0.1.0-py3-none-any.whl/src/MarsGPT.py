"""
ChatGPT API
    https://platform.openai.com/docs/api-reference/introduction

    pip install openai asyncio requests tiktoken httpx[socks] OpenAIAuth==0.2.0
"""
import asyncio
import json
import os
import sys
import httpx
import requests
import tiktoken
from OpenAIAuth.OpenAIAuth import OpenAIAuth

ENCODER = tiktoken.get_encoding("gpt2")


def get_max_tokens(prompt: str) -> int:
    """
    Get the max tokens for a prompt
    """
    return 4000 - len(ENCODER.encode(prompt))


class Message:
    """
    A single exchange between the user and the bot
    """

    def __init__(self, text: str, author: str) -> None:
        self.text: str = text
        self.author: str = author


class Conversation:
    """
    A single conversation
    """

    def __init__(self) -> None:
        self.messages: list[Message] = []


CONVERSATION_BUFFER: int = int(os.environ.get("CONVERSATION_BUFFER") or 1500)


class Conversations:
    """
    Conversation handler
    """

    def __init__(self) -> None:
        self.conversations: dict[str][Conversation] = {}

    def add_message(self, message: Message, conversation_id: str) -> None:
        """
        Adds a message to a conversation
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = Conversation()
        self.conversations[conversation_id].messages.append(message)

    def get(self, conversation_id: str) -> str:
        """
        Builds a conversation string from a conversation id
        """
        if conversation_id not in self.conversations:
            return ""
        # Build conversation string from messages and check if it's too long
        conversation = ""
        for message in self.conversations[conversation_id].messages:
            conversation += f"{message.author}: {message.text}<|im_sep|>\n\n"
        if len(ENCODER.encode(conversation)) > 4000 - CONVERSATION_BUFFER:
            self.purge_history(conversation_id)
            return self.get(conversation_id)
        return conversation

    def purge_history(self, conversation_id: str, num: int = 1):
        """
        Remove oldest messages from a conversation
        """
        if conversation_id not in self.conversations:
            return
        self.conversations[conversation_id].messages = self.conversations[
            conversation_id
        ].messages[num:]

    def rollback(self, conversation_id: str, num: int = 1):
        """
        Remove latest messages from a conversation
        """
        if conversation_id not in self.conversations:
            return
        self.conversations[conversation_id].messages = self.conversations[
            conversation_id
        ].messages[:-num]

    def remove(self, conversation_id: str) -> None:
        """
        Removes a conversation
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]


BASE_PROMPT = (
    os.environ.get("BASE_PROMPT")
    or """You are ChatGPT, a large language model by OpenAI. Respond conversationally\n\n\n"""
)


class Chatbot:
    """
    Handles everything seamlessly
    """

    def __init__(
        self,
        email: str,
        password: str,
        proxy=None,
        insecure: bool = False,
        session_token: str = None,
    ) -> None:
        self.proxy = proxy
        self.email: str = email
        self.password: str = password
        self.session_token = session_token
        self.insecure: bool = insecure
        self.api_key: str
        self.conversations = Conversations()
        self.login(email, password, proxy, insecure, session_token)

    async def ask(self, prompt: str, conversation_id: str = None) -> dict:
        """
        Gets a response from the API
        curl https://api.openai.com/v1/completions \
                -H 'Content-Type: application/json' \
                -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ5YW5qaW5nYW5nQGhvdG1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImdlb2lwX2NvdW50cnkiOiJUVyJ9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItSHQzUmhIWGdCMDRrU212cjVpUkdpeXpRIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2ViMzI5ZGMyODhhNWU0YWFiNjBlYjAiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjc2MzgxNTc5LCJleHAiOjE2Nzc1OTExNzksImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb2ZmbGluZV9hY2Nlc3MifQ.G1ews5O4IDneRhOvqsdc6mbngeTID-oYEA7_EeYBpKp7B3tCdgXGrovi1uvM65mBZpObxsy9aAHhqSvD_Zi7P2KOl_exZyR3_GcaM0Jv9isj-aB24wUumLoGvpf4oorcMeWqihejyasW1idFj5Ri40sSMjTnVtrOjJ7j4k16qUiyRq1tiJ7hBqTRSRpKvTieTGS0iHB11B5clk6g3M8KS0H2YHU-47U5PsS4q6kw5wl9PLUYPCNHX0r1jVlbi7yFkOOr2v8Lr9JJDx9jcRrhHZJfjyLJj_KIyndMZAD28ITzOES8LdsvBZag824rKl2WZ7X6VFXmIQwml6Ixv4Apew' \
                -d '{
                "model": "text-davinci-003",
                "prompt": "Say this is a test",
                "max_tokens": 7,
                "temperature": 0
                }'
        """
        if conversation_id is None:
            conversation_id = "default"
        self.conversations.add_message(
            Message(prompt, "User"),
            conversation_id=conversation_id,
        )
        conversation: str = self.conversations.get(conversation_id)
        # Build request body
        header_data = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        body = {
            "model": "text-davinci-003",
            "prompt": BASE_PROMPT + conversation + "ChatGPT: ",
            "max_tokens": get_max_tokens(conversation),
            "temperature": float(os.environ.get("TEMPERATURE") or 0.5),
            "top_p": float(os.environ.get("TOP_P") or 1),
            "stream": True,
            "stop": ["<|im_end|>", "<|im_sep|>"],
            "presence_penalty": float(os.environ.get("PRESENCE_PENALTY") or 1.0),
        }
        body_data = json.dumps(body)
        # print('ask body:', body_data)
        # print('ask header:', header_data)
        async with httpx.AsyncClient(proxies=self.proxy if self.proxy else None).stream(
            method="POST",
            url="https://api.openai.com/v1/completions",
            data=body_data,
            headers=header_data,
            timeout=1080,
        ) as response:
            full_result = ""
            async for line in response.aiter_lines():
                if response.status_code == 429:
                    print("error: " + "Too many requests")
                    error = {"choices": [{"text": "Too many requests", "finish_reason": "error"}]}
                    # yield error
                elif response.status_code == 503:
                    print("error: " + "OpenAI error!")
                    error = {"choices": [{"text": "AI error!", "finish_reason": "error"}]}
                    # yield error
                elif response.status_code != 200:
                    print("error: " + "Unknown error " + str(response.status_code))
                    error = {"choices": [{"text": "AI error!" + str(response.status_code), "finish_reason": "error"}]}
                    # yield error
                else:
                    line = line.strip()
                    if line == "\n" or line == "":
                        continue
                    if line == "data: [DONE]":
                        break
                    try:
                        # Remove "data: " from the start of the line
                        data = json.loads(line[6:])
                        if data is None:
                            continue
                        full_result += data["choices"][0]["text"].replace("<|im_end|>", "")
                        if "choices" not in data:
                            continue
                        yield data
                    except json.JSONDecodeError:
                        continue
            self.conversations.add_message(
                Message(full_result, "ChatGPT"),
                conversation_id=conversation_id,
            )

    def login(self, email, password, proxy, insecure, session_token) -> None:
        """
        Login to the API
        """
        if not insecure:
            auth = OpenAIAuth(email_address=email, password=password, proxy=proxy)
            if session_token:
                auth.session_token = session_token
                auth.get_access_token()
                self.api_key = auth.access_token
                if self.api_key is None:
                    self.session_token = None
                    self.login(email, password, proxy, insecure, None)
                return
            try:
                auth.begin()
                self.session_token = auth.session_token
                self.api_key = auth.access_token
                # print('session_token:', self.session_token)
                # print('api_key:', self.api_key)
            except:
                print("login timeout!")
        else:
            auth_request = requests.post(
                "https://api.openai.com/v1/auth",
                json={"email": email, "password": password},
                timeout=10,
            )
            self.api_key = auth_request.json()["accessToken"]
