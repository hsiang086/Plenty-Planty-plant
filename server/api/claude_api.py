import anthropic
from api import APIs

class ClaudeAPI(APIs):
    def __init__(self, config: dict):
        super().__init__(config)
        self.client = anthropic.Anthropic(api_key=self.config['CLAUDE_APIKEY'])
    
    def main(self):
        try:
            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": self.user_message},
                ]
            )
        except Exception as e:
            return f"Error: {e}"
        return message.content

if __name__ == "__main__":
    import json
    config = json.load(open('../../config.json'))
    claude = ClaudeAPI(config=config)
    print(claude.main())
