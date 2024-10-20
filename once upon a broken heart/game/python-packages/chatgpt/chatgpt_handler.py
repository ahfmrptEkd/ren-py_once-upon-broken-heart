import requests
import json
import time

class ChatGPTHandler:
    def __init__(self, api_key, assistant_id, base_url="https://api.openai.com/v1"):
        self.api_key = api_key
        self.assistant_id = assistant_id
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "assistants=v2"
        }

    def create_thread(self):
        thread_url = f"{self.base_url}/threads"
        thread_response = requests.post(thread_url, headers=self.headers)
        if thread_response.status_code != 200:
            raise Exception(f"Error creating thread: {thread_response.status_code}, {thread_response.text}")
        return thread_response.json()['id']

    def add_message(self, thread_id, content):
        message_url = f"{self.base_url}/threads/{thread_id}/messages"
        message_data = {"role": "user", "content": content}
        message_response = requests.post(message_url, headers=self.headers, json=message_data)
        if message_response.status_code != 200:
            raise Exception(f"Error adding message: {message_response.status_code}, {message_response.text}")

    def create_run(self, thread_id):
        run_url = f"{self.base_url}/threads/{thread_id}/runs"
        run_data = {"assistant_id": self.assistant_id}
        run_response = requests.post(run_url, headers=self.headers, json=run_data)
        if run_response.status_code != 200:
            raise Exception(f"Error creating run: {run_response.status_code}, {run_response.text}")
        return run_response.json()['id']

    def wait_for_completion(self, thread_id, run_id):
        while True:
            run_status_url = f"{self.base_url}/threads/{thread_id}/runs/{run_id}"
            run_status_response = requests.get(run_status_url, headers=self.headers)
            if run_status_response.status_code != 200:
                raise Exception(f"Error checking run status: {run_status_response.status_code}, {run_status_response.text}")
            status = run_status_response.json()['status']
            if status in ['completed', 'failed']:
                return status
            time.sleep(1)

    def get_assistant_response(self, thread_id):
        messages_url = f"{self.base_url}/threads/{thread_id}/messages"
        messages_response = requests.get(messages_url, headers=self.headers)
        if messages_response.status_code != 200:
            raise Exception(f"Error retrieving messages: {messages_response.status_code}, {messages_response.text}")
        
        assistant_message = next((msg for msg in messages_response.json()['data'] if msg['role'] == 'assistant'), None)
        if assistant_message:
            return assistant_message['content'][0]['text']['value']
        else:
            raise Exception("No assistant response found")

    def completion(self, messages):
        thread_id = self.create_thread()
        self.add_message(thread_id, messages[-1]['content'])
        run_id = self.create_run(thread_id)
        status = self.wait_for_completion(thread_id, run_id)
        
        if status == 'failed':
            raise Exception("Run failed")
        
        response_content = self.get_assistant_response(thread_id)
        messages.append({"role": "assistant", "content": response_content})
        return messages
