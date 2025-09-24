from pydantic import BaseModel, Field


class LinksList(BaseModel):
    links: list[str] = Field(description="A list of links in a website's markup")
