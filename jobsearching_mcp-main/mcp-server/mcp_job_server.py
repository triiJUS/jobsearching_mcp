from dotenv import load_dotenv
import os
from fastmcp import FastMCP
from duckduckgo_search import DDGS
from pydantic import BaseModel, Field

# Load .env variables
load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
MY_NUMBER = os.getenv("MY_NUMBER")

print(f"Auth Token: {AUTH_TOKEN}")
print(f"My WhatsApp Number: {MY_NUMBER}")

class JobSearchInput(BaseModel):
    query: str = Field(description="Search query for jobs")

# No authentication for now
server = FastMCP(name="Job Search MCP Server")

@server.tool(description="Search for jobs using DuckDuckGo")
def search_jobs(param: JobSearchInput) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(param.query, max_results=5))
    jobs = "\n\n".join(f"{r['title']} - {r['href']}" for r in results)
    return jobs or "No jobs found"

if __name__ == "__main__":
    server.run(transport="http", host="0.0.0.0", port=8086)