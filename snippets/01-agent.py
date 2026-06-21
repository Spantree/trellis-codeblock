import asyncio
from dataclasses import dataclass


@dataclass
class Agent:
    name: str
    model: str = "claude-opus-4"

    async def run(self, prompt: str) -> str:
        await asyncio.sleep(0.1)
        return f"{self.name}: {prompt[:40]}"


async def main() -> None:
    agents = [Agent(f"worker-{i}") for i in range(3)]
    results = await asyncio.gather(*(a.run("hello") for a in agents))
    print("\n".join(results))


asyncio.run(main())
