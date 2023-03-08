import mesa
import random 
import itertools

from .agent_q import Person


class Infection(mesa.Model):
    """Model class for iterated, spatial prisoner's dilemma model."""

    # working with random seed
    seed = random.random()

    # This dictionary holds the payoff for this agent,
    # keyed on: (my_move, other_move)

    def __init__(
        self, width=50, height=50, self_q_threshold = 0.5, schedule_type="Random", seed=seed
    ):
        """
        Create a new Spatial Prisoners' Dilemma Model.

        Args:
            width, height: Grid size. There will be one agent per grid cell.
            schedule_type: Can be "Sequential", "Random", or "Simultaneous".
                           Determines the agent activation regime.
            payoffs: (optional) Dictionary of (move, neighbor_move) payoffs.
        """
        # allow random seed
        mesa.Model.reset_randomizer(self, seed) #comment this out -- helps for replicability
        random.seed(seed)        

        self.grid = mesa.space.SingleGrid(width, height, torus=True)
        self.schedule_type = schedule_type
        self.schedule = mesa.time.RandomActivation(self)
        self.person_percent = 0.1
        self.width = width
        self.height = height
        self.self_q_threshold = self_q_threshold
        

        # Create agents
        width = self.width
        height = self.height

        x_list, y_list = list(range(width)), list(range(height))

        combinations = list(itertools.product(x_list, y_list))

        self.random.shuffle(combinations)


        for i in range(int(self.person_percent * height * width)):
            pos = combinations[i]
            agent = Person(pos, self)
            self.grid.place_agent(agent, pos)
            self.schedule.add(agent)


        self.datacollector = mesa.DataCollector(
             {
                 "Infection_Num": lambda m: len(
                     [a for a in m.schedule.agents if a.infected == 1]
                 )
             }
         )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run(self, n):
        """Run the model for n steps."""
        for _ in range(n):
            self.step()
