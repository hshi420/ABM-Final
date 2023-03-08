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
        self.infected_days = 0
        self.quarantine = 0 
         
        
        self.compliance = random.choice([0, 1])
        self.infected = random.choice([0, 1])
        

    # helper functions for deciding new values of infected and compliance
    # added 1 to each item to avoid divide by 0 error
    def decide_infection(self, non_compliance_infected_num, home_count, neighbor_count):
        return int((non_compliance_infected_num+1-home_count)/(neighbor_count - home_count+1) > 0.5) # divide by 0, all neighbors at home, use neighbors instead of 8

    def decide_compliance(self, compliance_num, total_infection_num, home_count, neighbor_count):
        return int(((compliance_num+1-home_count)/(neighbor_count - home_count+1)*0.5 + total_infection_num/len(self.model.schedule.agents)*0.5) > 0.5) 


    def step(self):

        move_prob = random.random()


        # how long the agent has been infected?
        if self.infected:
            self.infected_days += 1

                # check whether the agent has recovered
        if self.infected_days == 14:
            self.infected = 0
            self.infected_days = 0
            self.quarantine = 0

        # if the agent choose to stay, end step
        if move_prob < 0.5 or self.quarantine:
            return

        # initialize variables for moving out
        self.home = 0
        compliance_num = 0
        non_compliance_infected_num = 0
        total_infection_num = 0

        home_pos = self.pos

        # move out
        self.model.grid.move_to_empty(self)


        # calculate new values for compliance and infected
        neighbors = self.model.grid.get_neighbors(self.pos, True, include_center=False)                                                                                    

        home_count = 0
        
        for neighbor in neighbors:
            # count inhome neighbors
            if neighbor.home == 1: 
                home_count += 1
            # count complying neighbors
            if neighbor.compliance == 1:
                compliance_num += 1
            # count non-complying and infected neighbors
            if neighbor.compliance == 0 and neighbor.infected == 1:
                non_compliance_infected_num += 1
        # count total infected agents
        for agent in self.model.schedule.agents:
            if agent.infected == 1:
                total_infection_num += 1

        if not self.infected:
            self.infected = self.decide_infection(non_compliance_infected_num, home_count, len(neighbors))

        if self.infected:
            if random.random() > self.model.self_q_threshold: # if choose to do quarantine
                self.quarantine = 1

        self.compliance = self.decide_compliance(compliance_num, total_infection_num, home_count, len(neighbors))

        # go back home
        self.model.grid.move_agent(self, home_pos)
        self.home = 1

        

