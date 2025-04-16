import math

# Link lengths (in cm)
L1 = 5.0   # Coxa
L2 = 10.0  # Femur
L3 = 15.0  # Tibia

def inverse_kinematics(x, y, z):
    try:
        # Coxa rotation (α)
        alpha = math.degrees(math.atan2(y, x))

        # Convert to leg plane coordinates
        horizontal_distance = math.hypot(x, y) - L1
        if horizontal_distance < 0:
            raise ValueError("Target too close to the base (inside coxa radius).")

        distance = math.hypot(horizontal_distance, z)

        # Check reachability
        if distance > (L2 + L3):
            raise ValueError("Target out of reach.")

        # Angle at tibia joint (γ) using law of cosines
        cos_gamma = (L2**2 + L3**2 - distance**2) / (2 * L2 * L3)
        gamma = math.degrees(math.acos(cos_gamma))
        gamma = 180 - gamma  # Adjust for mechanical layout

        # Angle at femur joint (β)
        cos_beta = (distance**2 + L2**2 - L3**2) / (2 * L2 * distance)
        beta_offset = math.degrees(math.atan2(z, horizontal_distance))
        beta = beta_offset + math.degrees(math.acos(cos_beta))

        return round(alpha, 2), round(beta, 2), round(gamma, 2)
    except ValueError as e:
        return str(e)

def test_inverse_kinematics():
    test_cases = [
        ("Test 1 (Typical Reachable)", 10, 10, -5),
        ("Test 2 (Close to Base)", 5, 1, -2),
        ("Test 3 (Near Max Reach)", 25, 0, 0),
        ("Test 4 (Unreachable)", 40, 0, 0),
        ("Test 5 (Large Negative Z)", 15, 5, -20),
    ]

    print("HEXAPOD INVERSE KINEMATICS TESTS\n")
    for name, x, y, z in test_cases:
        result = inverse_kinematics(x, y, z)
        print(f"{name}: Target = ({x}, {y}, {z})")
        if isinstance(result, tuple):
            print(f"Joint Angles => α (Coxa): {result[0]}°, β (Femur): {result[1]}°, γ (Tibia): {result[2]}°")
            print("Reachability: ✅ Reachable\n")
        else:
            print(f"Reachability: ❌ {result}\n")

def main():
    print("==== HEXAPOD INVERSE KINEMATICS ====")
    choice = input("Enter '1' for custom input, '2' to run test cases: ")

    if choice == '1':
        try:
            x = float(input("Enter target X coordinate: "))
            y = float(input("Enter target Y coordinate: "))
            z = float(input("Enter target Z coordinate: "))
            result = inverse_kinematics(x, y, z)
            print(f"\nTarget = ({x}, {y}, {z})")
            if isinstance(result, tuple):
                print(f"Joint Angles => α: {result[0]}°, β: {result[1]}°, γ: {result[2]}°")
                print("Reachability: ✅ Reachable")
            else:
                print(f"Reachability: ❌ {result}")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == '2':
        test_inverse_kinematics()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
