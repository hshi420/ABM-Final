import mesa
import random



class Person(mesa.Agent):
    """Agent member of the iterated, spatial prisoner's dilemma model."""

    def __init__(self, pos, model, starting_move=None):
        """
        Create a new Prisoner's Dilemma agent.

        Args:
            pos: (x, y) tuple of the agent's position.
            model: model instance
            starting_move: If provided, determines the agent's initial state:
                           C(ooperating) or D(efecting). Otherwise, random.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.home = 1
        
        
        self.compliance = random.choice([0, 1])
        #print(self.compliance)
        self.infected = random.choice([0, 1])
        

    def decide_infection(self, non_compliance_infected_num, home_count):
        return int(non_compliance_infected_num/(8 - home_count) > 0.5) # divide by 0, all neighbors at home, use neighbors instead of 8

    def decide_compliance(self, compliance_num, total_infection_num, home_count):
        return int((compliance_num/(8 - home_count)*0.5 + total_infection_num/len(self.model.schedule.agents)*0.5) > 0.5) 


    def step(self):

        move_prob = random.random()

        # check if the agent want to move
        if move_prob < 0.5:
            return

        self.home = 0
        compliance_num = 0
        non_compliance_infected_num = 0
        total_infection_num = 0

        home_pos = self.pos

        # move out
        self.model.grid.move_to_empty(self)

        neighbors = self.model.grid.get_neighbors(self.pos, True, include_center=False)

        home_count = 0
        
        for neighbor in neighbors:

            if neighbor.home == 1: 
                home_count += 1
                
            if neighbor.compliance == 1:
                compliance_num += 1

            if neighbor.compliance == 0 and neighbor.infected == 1:
                non_compliance_infected_num += 1

        for agent in self.model.schedule.agents:
            if agent.infected == 1:
                total_infection_num += 1

        if not self.infected:
            self.infected = self.decide_infection(non_compliance_infected_num, home_count)

        self.compliance = self.decide_compliance(compliance_num, total_infection_num, home_count)

        # go back home
        self.model.grid.move_agent(self, home_pos)
        self.home = 1
