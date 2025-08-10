from dotenv import load_dotenv
import os
from fastmcp import FastMCP
from duckduckgo_search import DDGS
from pydantic import BaseModel, Field

# Load .env only if running locally
if not os.getenv("RAILWAY_STATIC_URL"):
    load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
MY_NUMBER = os.getenv("MY_NUMBER")

# If Railway provides URL, get it from env
RAILWAY_URL = os.getenv("RAILWAY_STATIC_URL")

print(f"Auth Token: {AUTH_TOKEN}")
print(f"My WhatsApp Number: {MY_NUMBER}")

if RAILWAY_URL:
    print(f"🚀 Public MCP URL: {RAILWAY_URL}/mcp")

class JobSearchInput(BaseModel):
    query: str = Field(description="Search query for jobs")

server = FastMCP(name="Job Search MCP Server")

@server.tool(description="Search for jobs using DuckDuckGo")
def search_jobs(param: JobSearchInput) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(param.query, max_results=5))
    jobs = "\n\n".join(f"{r['title']} - {r['href']}" for r in results)
    return jobs or "No jobs found"

if __name__ == "__main__":
    # Railway gives us a PORT variable — use it if available
    port = int(os.getenv("PORT", 8086))
    server.run(transport="http", host="0.0.0.0", port=port)
