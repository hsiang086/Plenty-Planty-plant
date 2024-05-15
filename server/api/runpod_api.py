##############################
# Copyright © hsiang086 2024 #
##############################

import aiohttp
from api import LlmAPI

class RunpodAPI(LlmAPI):
    def __init__(self, config: dict):
        super().__init__(config)
    
    async def main(self):
        apikey = self.config['RUNPOD_APIKEY']['key']
        url = self.config['RUNPOD_APIKEY']['url'] + '/runsync'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apikey}',
        }
        payload = {
            "input": {
                "prompt": self.user_message,
                "sampling_params": {
                    "max_tokens": 15,
                    "temperature": 0.25,
                },
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                return await response.json()
            
if __name__ == "__main__":
    import json
    config = json.load(open('../../config.json'))
    runpod = RunpodAPI(config=config)
    import asyncio
    print(asyncio.run(runpod.main()))
