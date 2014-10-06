from pypdevs.simulator import Simulator
from city_model import City

if __name__ == "__main__":
    city = City()
    sim = Simulator(city)
    #sim.setVerbose(None)
    sim.setStateSaving("custom")
    sim.setMessageCopy("custom")
    sim.simulate()
