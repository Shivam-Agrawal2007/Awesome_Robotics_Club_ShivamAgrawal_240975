# alpha = math.degrees(math.atan2(y, x))
	This computes the rotation around the vertical axis.
	It's simply the angle from the center to the point (x, y) on the ground.

# horizontal_distance = math.hypot(x, y) - L1
	We're removing the fixed coxa offset from the XY projection.
	Now we have the "horizontal leg" we need to reach from femur + tibia.

# distance = math.hypot(horizontal_distance, z)
	This is the straight-line distance from the femur-tibia joint to the target point.

# if distance > (L2 + L3):
    raise ValueError("Target out of reach.")
	If the point is farther than the sum of femur + tibia, it’s unreachable.

# cos_gamma = (L2**2 + L3**2 - distance**2) / (2 * L2 * L3)
gamma = math.degrees(math.acos(cos_gamma))
gamma = 180 - gamma
	We use the law of cosines to find the angle between femur and tibia.
	180 - gamma adjusts for the physical direction the leg would bend.

# cos_beta = (distance**2 + L2**2 - L3**2) / (2 * L2 * distance)
beta_offset = math.degrees(math.atan2(z, horizontal_distance))
beta = beta_offset + math.degrees(math.acos(cos_beta))
	This is also done using law of cosines.
	But we also add the angle between the "horizontal distance" and vertical (z) to get correct leg orientation.

# test_cases = [
        ("Test 1 (Typical Reachable)", 10, 10, -5),
        ("Test 2 (Close to Base)", 5, 1, -2),
        ("Test 3 (Near Max Reach)", 25, 0, 0),
        ("Test 4 (Unreachable)", 40, 0, 0),
        ("Test 5 (Large Negative Z)", 15, 5, -20),
    ]
	Define different test cases.
