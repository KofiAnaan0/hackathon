import asyncio
import aiohttp
from livekit.agents import function_tool, RunContext
from langchain_community.tools import DuckDuckGoSearchRun
import logging

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
                return (f"As of {latest['time']}, the global temperature anomaly is {latest['station']}°C "
                        f"This {latest['time']} is the most recent data available on global warming.")
    except Exception as e:
        print(f'An error occurred: {e}')

@function_tool()
async def curiosity_web_search() -> str:
    """
    Search the web using DuckDuckGo to see the Future.
    """
    try:
        query = "What happens if the earth's temperature rises by 2 degrees Celsius?"
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        print(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."  

if __name__ == '__main__':
    asyncio.run(curiosity_web_search())
                