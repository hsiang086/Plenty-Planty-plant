##############################
# Copyright © hsiang086 2024 #
##############################

import PyInquirer
import json
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def setup_config(skip=False):
    if 'config.json' in os.listdir('./') and not skip:
        questions = [{
                'type': 'confirm',
                'name': 'overwrite',
                'message': 'Config file already exists, overwrite it?',
            },
        ]
        answers = PyInquirer.prompt(questions)
        if answers['overwrite']:
            setup_config(True)
        else:
            print("Skipping config file creation")
    else:
        if skip:
            config = json.load(open('config.json'))
        else:
            print(f"{bcolors.WARNING}Config file not found. Creating one...")
            config = {}
        
        questions = [{
                'type': 'password',
                'name': 'discord_token',
                'message': 'Enter your Discord bot token:',
            }, {
                'type': 'input',
                'name': 'prefix',
                'message': 'Enter your Discord bot prefix  (default is "!" leave empty to skip):',
            }, {
                'type': 'input',
                'name': 'webhook_url',
                'message': 'Enter your Discord webhook URL:',
            }, {
                'type': 'password',
                'name': 'claude_api_key',
                'message': 'Enter your Claude API key  (optional leave empty to skip):',
            }, {
                'type': 'password',
                'name': 'openai_api_key',
                'message': 'Enter your OpenAI API key  (optional leave empty to skip):',
            }, {
                'type': 'password',
                'name': 'runpod_api_key',
                'message': 'Enter your Runpod API key  (optional leave empty to skip):',
            }, {
                'type': 'input',
                'name': 'runpod_api_LLM_url',
                'message': 'Enter your Runpod LLM API URL  (optional leave empty to skip):',
            }, {
                'type': 'input',
                'name': 'runpod_api_SD_url',
                'message': 'Enter your Runpod SD API URL  (optional leave empty to skip):',
            },
        ]
        answers = PyInquirer.prompt(questions)

        if answers['discord_token']:
            config['DISCORD_TOKEN'] = answers['discord_token']
        if answers['prefix']:
            config['PREFIX'] = answers['prefix']
        if answers['webhook_url']:
            config['WEBHOOK_URL'] = [answers['webhook_url']]
        if answers['claude_api_key']:
            config['CLAUDE_APIKEY'] = answers['claude_api_key']
        if answers['openai_api_key']:
            config['OPENAI_APIKEY'] = answers['openai_api_key']
        if answers['runpod_api_key']:
            config['RUNPOD_APIKEY']['key'] = answers['runpod_api_key']
        if answers['runpod_api_LLM_url']:
            url = answers['runpod_api_LLM_url']
            if url[-1] == '/':
                url = url[:-1]
            config['RUNPOD_APIKEY']['LLMurl'] = url
        if answers['runpod_api_SD_url']:
            url = answers['runpod_api_SD_url']
            if url[-1] == '/':
                url = url[:-1]
            config['RUNPOD_APIKEY']['SDurl'] = url
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print(f"{bcolors.OKGREEN}Config file created successfully")
        

if __name__ == '__main__':
    setup_config()
