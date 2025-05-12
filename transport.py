import random
random.seed(123)

def transport(env, transport_time):
    """
    Simulates component transportation with random delays.
    :param env: Simulation environment
    :param transport_time: Base transportation time
    :return: Actual arrival time (rounded to 2 decimal places)
    """
    # Generate random delay between 0-2 time units
    delay = random.uniform(0, 2)
    total_time = transport_time + delay
    
    # Simulate transportation process
    yield env.timeout(total_time)
    
    # Return precise arrival time
    return round(env.now, 2)