from datetime import datetime

class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.is_booked = False

    def is_available(self):
        return not self.is_booked

class Guest:
    def __init__(self, name, contact, guest_id):
        self.name = name
        self.contact = contact
        self.guest_id = guest_id

class Booking:
    def __init__(self, guest, room, check_in_date, check_out_date):
        self.guest = guest
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.actual_check_out_date = None
        self.price = 0

    def calculate_price(self):
        if not self.actual_check_out_date:
            self.actual_check_out_date = datetime.now().date()

        days = (self.actual_check_out_date - self.check_in_date).days
        days_stayed = max(1, days)
        self.price = days_stayed * self.room.price

        if self.actual_check_out_date > self.check_out_date:
            extra_days = (self.actual_check_out_date - self.check_out_date).days
            self.price += extra_days * self.room.price * 0.5
        return self.price

class Hotel:
    def __init__(self):
        self.rooms = []
        self.bookings = []

    def add_room(self, room_number, room_type, price):
        room = Room(room_number, room_type, price)
        self.rooms.append(room)

    def book_room(self, guest_name, contact, guest_id, room_type, check_in_date, check_out_date):
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()

        for room in self.rooms:
            if room.is_available() and room.room_type.lower() == room_type.lower():
                guest = Guest(guest_name, contact, guest_id)
                booking = Booking(guest, room, check_in_date, check_out_date)
                room.is_booked = True
                self.bookings.append(booking)
                print(f"Room {room.room_number} booked successfully for {guest.name} from {check_in_date} to {check_out_date}.")
                return
        print(f"No available {room_type} rooms.")

    def checkout(self, guest_id):
        for booking in self.bookings:
            if booking.guest.guest_id == guest_id and booking.room.is_booked:
                booking.actual_check_out_date = datetime.now().date()
                total_price = booking.calculate_price()
                booking.room.is_booked = False
                print(f"✅ Checkout successful for {booking.guest.name}. Total price: ₹{total_price:.2f}")
                return
        print(f"No active booking found for Guest ID: {guest_id}.")

    def display_available_rooms(self):
        available = [room for room in self.rooms if room.is_available()]
        if not available:
            print("No available rooms.")
        else:
            print("\nAvailable Rooms:")
            for room in available:
                print(f"Room {room.room_number}: {room.room_type} - ₹{room.price}/night")

    def display_booked_rooms(self):
        booked = [room for room in self.rooms if not room.is_available()]
        if not booked:
            print("No rooms are currently booked.")
        else:
            print("\nBooked Rooms:")
            for room in booked:
                print(f"Room {room.room_number}: {room.room_type}")

def main():
    hotel = Hotel()
    hotel.add_room(1, "Single", 1000)
    hotel.add_room(2, "Double", 1500)
    hotel.add_room(3, "Suite", 2500)

    while True:
        print("\nHotel Management System")
        print("1. Display Available Rooms")
        print("2. Display Booked Rooms")
        print("3. Book Room")
        print("4. Checkout")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            hotel.display_available_rooms()
        elif choice == '2':
            hotel.display_booked_rooms()
        elif choice == '3':
            name = input("Enter guest name: ")
            contact = input("Enter contact: ")
            guest_id = input("Enter guest ID: ")
            room_type = input("Enter room type (Single/Double/Suite): ")
            check_in = input("Enter check-in date (YYYY-MM-DD): ")
            check_out = input("Enter check-out date (YYYY-MM-DD): ")
            hotel.book_room(name, contact, guest_id, room_type, check_in, check_out)
        elif choice == '4':
            guest_id = input("Enter guest ID to checkout: ")
            hotel.checkout(guest_id)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
