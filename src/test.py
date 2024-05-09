def radians_to_compass_direction(radians):
    degrees = radians * (180 / 3.14159)  # Convert radians to degrees
    degrees %= 360  # Normalize degrees within [0, 360)
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = int((degrees + 22.5) / 45) % 8  # Determine which part of the circle you're in
    
    main_direction = directions[index]
    
    # Determine the 4 closest directions
    if main_direction == 'N':
        closest_directions = ['N', 'NE', 'NW', 'E', 'W']
    elif main_direction == 'NE':
        closest_directions = ['NE', 'E', 'N', 'SE', 'NW']
    elif main_direction == 'E':
        closest_directions = ['E', 'SE', 'NE', 'S', 'N']
    elif main_direction == 'SE':
        closest_directions = ['SE', 'S', 'E', 'SW', 'NE']
    elif main_direction == 'S':
        closest_directions = ['S', 'SW', 'SE', 'W', 'E']
    elif main_direction == 'SW':
        closest_directions = ['SW', 'W', 'S', 'NW', 'SE']
    elif main_direction == 'W':
        closest_directions = ['W', 'NW', 'SW', 'N', 'S']
    else:  # main_direction == 'NW'
        closest_directions = ['NW', 'N', 'W', 'NE', 'SW']
    
    return closest_directions

# Example usage:
radians = 3.14  # Your radians value for West
directions = radians_to_compass_direction(radians)
print("Directions:", directions)
