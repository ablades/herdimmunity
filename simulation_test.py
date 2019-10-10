import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
from simulation import Simulation
import pytest

#Test constructor
def test_constructor():
    v = Virus("Test", .25, .25)
    sim = Simulation(100, .25, v, initial_infected=4)
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
    assert len(sim.population) == 100

def test_simulation_should_continue():
    v = Virus("Test", .25, .25)
    sim = Simulation(100, .25, v, initial_infected=4)
    sim1 = Simulation(100, .25, v, initial_infected=4)
    sim2 = Simulation(100, .25, v, initial_infected=4)

    #Check if all are dead
    for person in sim.population:
        person.is_alive = False

    assert sim._simulation_should_continue() == False

    #make everyone vaccinated
    for person in sim1.population:
        person.is_vaccinated = True

    assert sim1._simulation_should_continue() == False

    #check that all survivors are vaccinated
    for person in sim2.population:
        person.is_vaccinated = True

    #kill off 3 people
    sim2.population[0].is_alive = False
    sim2.population[90].is_alive = False
    sim2.population[86].is_alive = False
    sim2.total_dead = 3
    assert sim2._simulation_should_continue() == False

def test_run():
    v = Virus("Test", .25, .25)
    sim = Simulation(100, .25, v, initial_infected=4)

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