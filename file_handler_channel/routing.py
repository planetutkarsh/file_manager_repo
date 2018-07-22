from channels import route
from file_handler_channel import consumers

channel_routing = [
    route('websocket.connect', consumers.connect),
    #route('websocket.disconenct', consumers.disconnect),
    route('websocket.receive', consumers.receive)
]
