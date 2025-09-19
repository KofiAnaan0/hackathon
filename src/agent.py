from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)

import os
from tools import getGlobalWarmingData, internetSearch
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
# from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv('.env.local')


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            tools=[getGlobalWarmingData, internetSearch]
        )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        preemptive_generation=True,
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=google.LLM(model="gemini-2.0-flash"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        # turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            # noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await session.generate_reply(
        instructions=(
                "Spark curiosity from the start: first, reveal Earth's current temperature change with the 'getGlobalWarmingData' tool. "
                "Then invite the user to imagine what could happen if global temperatures rise by 2 °C. "
                "Finally, enrich the conversation by uncovering the answer with the 'internetSearch' tool, keeping the user engaged and intrigued."
            )
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
    