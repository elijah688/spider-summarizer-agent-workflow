from agents import Agent, Runner, RunResult
from src.model.model import LinksList
from src.scrape_tools.scrape_tools import get_links
from src.instructions.instructions import curator


class Curator:
    def __init__(self):
        self.agent = Agent(
            name="Evaluator",
            instructions=curator,
            output_type=LinksList,
            model="gpt-5-nano",
        )

    def __get_all_before_hash(self, s: str) -> str:
        before = s.split("#", 1)

        if len(before) > 0:
            return before[0]
        return ""

    def __get_clean_links(self, url: str, rl_res: RunResult) -> list[str]:
        res: LinksList = rl_res.final_output
        relevant_links: list[str] = res.links

        clean_links = []
        for rl in relevant_links[0:4]:
            cl = self.__get_all_before_hash(rl)
            if len(cl) > 0:
                if cl.find("http") == -1:
                    clean_links.append(url + cl)
                else:
                    clean_links.append(cl)
        return clean_links

    async def get_relevant_links(self, url: str):
        links = await get_links(url)
        rl_res = await Runner.run(self.agent, f"Get the relevant links: {links}")
        return self.__get_clean_links(url, rl_res)
