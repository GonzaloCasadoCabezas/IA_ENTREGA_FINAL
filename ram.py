import random
from transport import transport
from logic.fuzzy_logic import Fuzzy_assembler

def ram(env, name, mf, assembly_time, components_store, transport_time, system_load):
    """
    Simulates the manufacturing and transportation of a RAM memory.
    :param env: Simulation environment.
    :param name: Name of the RAM memory.
    :param mf: Main factory resource.
    :param assembly_time: Manufacturing time.
    :param main_assembly_time: Assembly time at main factory.
    :param components_store: Components storage.
    :param transport_time: Transportation time to main factory.
    """
    difficulty = 2
    fuzzy = Fuzzy_assembler()
    main_assembly_time = fuzzy.get_assembly_time(difficulty, system_load)
    
    max_retries = 3  # Max retries in case of failure
    retries = 0

    # Request access to main factory
    print(f'{name}: All RAM components arrived at time {round(env.now)}')
    
    while retries < max_retries:  # Retry on failure
        # Simulate manufacturing time
        yield env.timeout(assembly_time)
        
        # Simulate 10% failure probability
        if random.random() < 0.1:
            print(f'{name}: Manufacturing failure. Restarting... (Attempt {retries + 1})')
            retries += 1
            continue  # Restart manufacturing process
        
        # Continue if no failure
        break  # Exit loop if successful
    else:
        print(f'{name}: Critical failure. RAM could not be manufactured.')
        return  # Exit function if max retries reached

    with mf.request() as req:
        yield req
        
        # Simulate main factory assembly
        print(f'{name}: RAM assembly started at time {round(env.now)}')
        yield env.timeout(main_assembly_time)
        print(f'{name}: Assembly completed at time {round(env.now)}')
        
        # Simulate transportation
        arrival = yield env.process(transport(env, transport_time))
        delay = arrival - env.now + transport_time
        print(f'{name}: Arrived at Main Factory at {arrival}(Delay: {delay:.2f})')
        
        # Check for duplicates
        if 'RAM' not in components_store.items:
            yield components_store.put('RAM')
            print(f'{name}: RAM sent to component store at time {round(env.now, 2)}')
        else:
            print(f'{name}: Duplicate RAM. Ignoring...')
     
