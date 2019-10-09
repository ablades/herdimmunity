import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, population_size, v_percentage, virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have died as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # Stores created population in self.population attribute
    
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.pop_size = population_size # Int
        self.initial_infected = initial_infected # Int
        self.total_infected = initial_infected# Int
        self.current_infected = initial_infected # Int
        self.vacc_percentage = v_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = f"{virus.name}_simulation_pop_{self.pop_size}_vp_{self.vacc_percentage}_infected_{self.initial_infected}.txt"
        self.newly_infected = []
        self.newly_dead = []
        self.population = self._create_population(self.initial_infected)

        #Create Logger and write metadata
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(self.pop_size,self.vacc_percentage,self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.
        '''
        
        #Array of persons
        self.population = []
        #Get count of vaccinated people
        vacc_count = int(self.pop_size * self.vacc_percentage)
        #Add vaccinated people to population
        for i in range(vacc_count):
            self.population.append(Person(self.next_person_id, True))
            self.next_person_id += 1
        
        #Add infected people to population
        for i in range(self.initial_infected):
            self.population.append(Person(self.next_person_id, False, self.virus))
            self.next_person_id += 1

        #Add rest of population
        for person in range(self.pop_size - vacc_count - initial_infected):
            self.population.append(Person(self.next_person_id, False))
            self.next_person_id += 1
        
        #List of population
        return self.population

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        #Check if everyone is dead
        if self.total_dead == self.pop_size:
            return False

        #Get count of population that is alive and vaccinated
        vacc_count = 0
        for person in self.population:
            if person.is_alive and person.is_vaccinated:
                vacc_count += 1

        #Check if all survivors are vaccinated 
        if vacc_count == self.pop_size - self.total_dead:
            #All survivors are vaccinated
            return False

        return True


            
    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        time_step_counter = 0
        should_continue = self._simulation_should_continue()

        while should_continue:
            #Round of simulation
            self.time_step()

            #Log the current timestep
            self.logger.log_time_step(time_step_counter, len(self.newly_infected), len(self.newly_dead),self.total_infected, self.total_dead)

            self._infect_newly_infected()
            #increment time step
            time_step_counter += 1
            #Check population
            should_continue = self._simulation_should_continue()

        print(f"The simulation has ended after {time_step_counter} turns.")

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a random person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''

        for person in self.population:
            #If person is alive and has infection, interact
            if person.is_alive and person.infection:
                
                interactions = 0
                while(interactions < 100):
                    #randomly select member  of the population
                    rand_person = self.population[random.randrange(0, self.pop_size)]

                    #counts as an interaction
                    if rand_person.is_alive:
                        interactions +=1
                        self.interaction(person, rand_person)
                


        #roll population survival 
        for person in self.population:
            #if person is infected 
            if person.is_alive and person.infection:
                
                #Person survived infection -> becomes vaccinated
                if person.did_survive_infection():
                    self.logger.log_infection_survival(person, False)
                #Person has died
                else:
                    self.logger.log_infection_survival(person, True)
                    self.current_infected -= 1
                    self.total_dead += 1
                    self.newly_dead.append(person._id)



    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        #Check if random_person has virus
        r_person_sick = False
        if random_person.virus is None:
            r_person_sick = False
        else:
            r_person_sick = True


        #Chance to infect
        #Person has been infected by chance
        if random.random() < self.virus.repro_rate:
            self.logger.log_interaction(person, random_person, r_person_sick, random_person.is_vaccinated, did_infect=True)
            #random_person has no immunity and is now infected
            if random_person.is_vaccinated is False and r_person_sick is False:
                self.newly_infected.append(random_person._id)

        #Did not infect
        else:
            self.logger.log_interaction(person, random_person, r_person_sick ,random_person.is_vaccinated, did_infect=False)

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        #infect each person
        for person_id in self.newly_infected:
            self.population[person_id].infection = self.virus
            self.current_infected += 1

        #reset newly lists
        self.newly_infected = []
        self.newly_dead = []

#Test constructor
def test_constructor():
    v = Virus("Test", .25, .25)
    sim = Simulation(100, .25, v, initial_infected=4)
    #assert len(sim.population) == 100
    assert sim.next_person_id == 100
    assert sim.total_infected == 4
    assert sim.vacc_percentage == .25
    assert sim.virus == v
    assert sim.initial_infected == 4
    assert sim.current_infected == 4
    assert sim.total_dead == 0
    assert sim.file_name == "Test_simulation_pop_100_vp_0.25_infected_4.txt"
    assert sim.newly_infected == []
    assert sim.newly_dead == []


#Test create population 
def test_create_population():
    v = Virus("Test", .25, .25)
    sim = Simulation(100, .25, v, initial_infected=4)
    #vaccinated count
    v_count = 0
    #infected count
    i_count = 0

    #Check entire population
    for person in sim.population:
        #Make sure everyone is alive in population at start
        assert person.is_alive == True

        #count number of vaccinated people
        if person.is_vaccinated:
            v_count += 1
        #person has infection
        if person.infection is not None:
            i_count += 1

    #verify correct number of infected and vaccinated people
    assert v_count == 25
    assert i_count == 4



if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()
