import time
from datetime import datetime, timedelta

class Vehicle:
    def __init__(self):
        self.license_plate = input("Enter License Plate: ")
        self.vehicle_type = input("Enter Vehicle Type (Car/Bike): ")

class ParkingSlot:
    def __init__(self, slot_number):
        self.slot_number = slot_number
        self.is_occupied = False
        self.vehicle = None

class Ticket:
    def __init__(self, vehicle, slot_number):
        self.vehicle = vehicle
        self.slot_number = slot_number
        self.entry_time = datetime.now()
        self.exit_time = None

    def calculate_fee(self):
        self.exit_time = datetime.now()
        total_time = (self.exit_time - self.entry_time).seconds // 60  # Minutes
        fee = 0
        if total_time > 15:  # Grace period 15 mins
            if self.vehicle.vehicle_type == "Car":
                fee = ((total_time - 15) // 60) * 20
            elif self.vehicle.vehicle_type == "Bike":
                fee = ((total_time - 15) // 60) * 10
        return fee

class ParkingLot:
    def __init__(self):
        total_slots = int(input("Enter total parking slots: "))
        self.slots = [ParkingSlot(i + 1) for i in range(total_slots)]
        self.tickets = {}  # Maps license_plate -> Ticket

    def park_vehicle(self):
        vehicle = Vehicle()
        for slot in self.slots:
            if not slot.is_occupied:
                slot.is_occupied = True
                slot.vehicle = vehicle
                ticket = Ticket(vehicle, slot.slot_number)
                self.tickets[vehicle.license_plate] = ticket
                print(f"✅ Vehicle {vehicle.license_plate} parked at slot {slot.slot_number}")
                return
        print("❌ Parking Lot Full!")

    def remove_vehicle(self):
        license_plate = input("Enter License Plate to Exit: ")
        if license_plate in self.tickets:
            ticket = self.tickets.pop(license_plate)
            for slot in self.slots:
                if slot.slot_number == ticket.slot_number:
                    slot.is_occupied = False
                    slot.vehicle = None
                    fee = ticket.calculate_fee()
                    print(f"✅ Vehicle {license_plate} exited. Fee: ₹{fee}")
                    return
        print("❌ Vehicle not found!")

    def display_available_slots(self):
        available_slots = [slot.slot_number for slot in self.slots if not slot.is_occupied]
        print(f"🅿️ Available slots: {available_slots}" if available_slots else "❌ No available slots.")

def main():
    lot = ParkingLot()

    while True:
        print("\n1. Park Vehicle\n2. Remove Vehicle\n3. Display Available Slots\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            lot.park_vehicle()
        elif choice == '2':
            lot.remove_vehicle()
        elif choice == '3':
            lot.display_available_slots()
        elif choice == '4':
            print("Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
