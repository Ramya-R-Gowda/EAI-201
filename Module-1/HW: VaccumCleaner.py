class VacuumCleaner:
    def __init__(self, shape):
        self.shape = shape
        self.state = "rest"

    def command(self, action):
        if action == "start":
            self.state = "cleaning"
            print(f"{self.shape} vacuum started cleaning.")
            self.clean_mode()
        elif action == "stop":
            self.state = "rest"
            print(f"{self.shape} vacuum stopped.")
        elif action == "left":
            print(f"{self.shape} vacuum turned left.")
        elif action == "right":
            print(f"{self.shape} vacuum turned right.")
        elif action == "dock":
            self.state = "docking"
            print(f"{self.shape} vacuum docking at charging station.")
        else:
            print(f"Action '{action}' not recognized.")

    def clean_mode(self):
        print("\nChoose cleaning category: 1. Solid  2. Liquid")
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        if choice == 1:
            self.solid_clean()
        elif choice == 2:
            self.liquid_clean()
        else:
            print("Invalid choice.")

    def solid_clean(self):
        print("\nSolid options: 1. Dust  2. Papers/Rocks  3. Others")
        try:
            opt = int(input("Enter solid type: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        if opt == 1:
            self.shape = "Rectangle"
            print("Cleaning dust... Shape optimized to Rectangle for efficiency.")
        elif opt == 2:
            self.shape = "Circle"
            print("Cleaning papers/rocks... Shape optimized to Circle for better suction.")
        elif opt == 3:
            self.shape = "Square"
            print("Cleaning other solids... Shape optimized to Square for balance.")
        else:
            print("Invalid solid option.")

    def liquid_clean(self):
        print("\nLiquid options: 1. Water  2. Others")
        try:
            opt = int(input("Enter liquid type: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        if opt == 1:
            self.shape = "Funnel"
            print("Cleaning water... Shape changed to Funnel.")
        elif opt == 2:
            self.shape = "Cone"
            print("Cleaning other liquids... Shape changed to Cone.")
        else:
            print("Invalid liquid option.")


# --- Main Program ---
shapes = ["Circle", "Square", "Triangle", "Pentagon"]
print("Available vacuum shapes:", shapes)

user_shape = input("Choose a vacuum shape: ")

if user_shape.capitalize() in [s.capitalize() for s in shapes]:
    vac = VacuumCleaner(user_shape.capitalize())

    while True:
        print("\nActions: start | left | right | dock | stop | exit")
        action = input("Enter action: ").lower()
        if action == "exit":
            print("Exiting program.")
            break
        vac.command(action)

        if action == "stop":
            print("Session ended.")
            break
else:
    print("Invalid shape. Please restart and choose from the given list.")
