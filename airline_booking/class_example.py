class Flight:
    counter = 1
    def __init__(self, origin, destination, duration):
        #super(, self).__init__()

        #keep track of id counter
        self.id = Flight.counter
        Flight.counter += 1

        #keep track of passengers in this list
        self.passengers = []

        #details about flight
        self.origin = origin
        self.destination = destination
        self.duration = duration

    def print_f(self):
        print(f"Flight origin: {self.origin}")
        print(f"Flight destination: {self.destination}")
        print(f"Flight duration: {self.duration}")

        print()
        print("Passengers in this flight: ")
        for p in self.passengers:
            print(f"{p.name}")

    def add_passenger(self, pax):
        self.passengers.append(pax) #add passenger into List
        pax.flight_id = self.id #self is the object of flight,
                              #p is the object of passenger
        #each passenger's flight id = id of flight they are on.
        #it is how it keep tracking which flight associated with passenger
    def delay(self, amount):
        self.duration += amount

class Passenger:
    def __init__(self, name):
        self.name = name


def main():
    #create flight
    f = Flight(origin="Hanoi", destination="Vaasa", duration=790)
    f.delay(5)

    p1 = Passenger("Han")
    p2 = Passenger("Blue")

    f.add_passenger(p1)
    f.add_passenger(p2)
    f.print_f()

if __name__=="__main__":
    main()
