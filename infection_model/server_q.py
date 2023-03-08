import mesa

from .portrayal import portrayPerson
from .model_q import Infection


# Make a world that is 50x50, on a 500x500 display.
canvas_element = mesa.visualization.CanvasGrid(portrayPerson, 50, 50, 500, 500)

model_params = {
    "height": 50,
    "width": 50
}

server = mesa.visualization.ModularServer(
    Infection, [canvas_element], "infection", model_params
)
