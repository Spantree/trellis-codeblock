from anthropic import Anthropic

client = Anthropic()


def ask(prompt: str) -> str:
    resp = client.messages.create(
        model="claude-opus-4",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text
