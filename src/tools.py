import asyncio
import aiohttp
from livekit.agents import function_tool, RunContext
from langchain_community.tools import DuckDuckGoSearchRun
import logging
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv('.env.local')



@function_tool()
async def getGlobalWarmingData():
    """
    Fetch earth's current temperature.
    """
    url = 'https://global-warming.org/api/temperature-api'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f'HTTP error {response.status}')
                data = await response.json()

                # Get the latest record (last element in the list)
                latest = data['result'][-1]
                return (f"As of Today, the global mean surface temperature anomaly is {latest['station']}°C ")
    except Exception as e:
        print(f'An error occurred: {e}')


@function_tool()
async def internetSearch(query: str) -> str:
    """
    Search the internet for answers.
    """
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(query=query, include_answer="advanced")
        print(response['answer'])
        return response
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."  

if __name__ == '__main__':
    asyncio.run(internetSearch("What is global warming?"))
                