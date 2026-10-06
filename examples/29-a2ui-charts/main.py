from pathlib import Path
from a2a.helpers import new_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from agent_nebula_secureagent import SecureAgent
from examples.example_paths import config_path
from a2ui_transport import a2ui_part
from presentation import load_presentation
HERE=Path(__file__).resolve().parent
class ChartExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue)->None:
        values=[("us-east",80),("us-west",50),("eu-west",30)]
        series=[{"label":label,"value":value} for label,value in values]
        await event_queue.enqueue_event(new_message([a2ui_part([load_presentation(HERE/"presentation.json", {"series":series})])]))
    async def cancel(self, context, event_queue): raise NotImplementedError
agent=SecureAgent(config=config_path(HERE,"secureagent.conf"),a2ui_config=config_path(HERE,"a2ui.conf")); agent.use_protocol("a2a",role="server",config=config_path(HERE,"a2aserver.conf")); agent.a2a_skill("traffic-chart",ChartExecutor())
if __name__=="__main__": agent.run()
