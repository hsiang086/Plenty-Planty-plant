##############################
# Copyright © hsiang086 2024 #
##############################

import aiohttp
from api import APIs

class RunpodAPI(APIs):
    def __init__(self, config: dict):
        super().__init__(config)
    
    async def Llm(self, hu, temperature):
        # self.setUserMessage(soil_hu=hu, hu=hu)
        apikey = self.config['RUNPOD_APIKEY']['key']
        url = self.config['RUNPOD_APIKEY']['LLMurl'] + "/runsync"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apikey}',
        }
        payload = {
            "input": {
                "prompt": self.user_message,
                "sampling_params": {
                    "max_tokens": 15,
                    "temperature": temperature,
                },
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                return await response.json()
            
    async def Sd(self):
        apikey = self.config['RUNPOD_APIKEY']['key']
        url = self.config['RUNPOD_APIKEY']['SDurl'] + "/runsync"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apikey}',
        }
        payload = {
            "input": {
                "prompt": self.sd_prompt,
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 25,
                "refiner_inference_steps": 50,
                "guidance_scale": 7.5,
                "strength": 0.3,
                "seed": None,
                "num_images": 1,
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
    import base64
    b = asyncio.run(runpod.Sd())
    b = b['output']['image_url'][len('data:image/png;base64,'):]
    with open('image.jpg', 'wb') as f:
        f.write(base64.b64decode(b))