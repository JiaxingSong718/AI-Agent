import os
import json
import dashscope
from prompt import user_prompt
from dashscope.api_entities.dashscope_response import Message
from dotenv import load_dotenv
load_dotenv()

class LLMModelProvider(object):
    def __init__(self) -> None:
        self.api_key = os.environ.get("API_KEY")
        self.model_name = os.environ.get("MODEL_NAME")
        self._client = dashscope.Generation()

        self.max_retry_time = 3

    def chat(self,prompt,chat_history):
        current_retry_time = 0
        while current_retry_time < self.max_retry_time:
            current_retry_time += 1
            try:
                messages = [Message(role='system',content=prompt)]
                for his in chat_history:
                    messages.append(Message(role='user',content=his[0]))
                    messages.append(Message(role='assistant',content=his[1]))
                messages.append(Message(role='user',content=user_prompt))
                response = self._client.call(
                    model = self.model_name,
                    api_key=self.api_key,
                    messages=messages
                )
                print("response: ",response)
                """
                {
	                "status_code": 200,
	                "request_id": "58d98f0b-d4e5-9d11-a290-258f46dec203",
                    "code": "",
                    "message": "",
                    "output": {
                        "text": null,
                        "finish_reason": null,
                        "choices": [{
                                    "finish_reason": "stop",
                                    "message": {
                                            "role": "assistant",
                                            "content": "这三种蔬菜都是非常常见的食材，可以做出既美味又营养的菜肴。}}]}, "
                                            usage ": {"
                                                input_tokens ": 20, "
                                                output_tokens ": 476, "
                                                total_tokens ": 496}
                    }
                """
                content = json.loads(response['output']['text'])
                return content
            except Exception as err:
                print("调用大模型出错，{}".format(err))
            return {}