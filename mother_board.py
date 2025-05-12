import random
random.seed(123)
from transport import transport
from logic.fuzzy_logic import Fuzzy_assembler

def mother_board(env, name, mf, assembly_time, components_store, transport_time, system_load):
    """
    Simulates the manufacturing and transportation of a motherboard.
    :param env: Simulation environment.
    :param name: Name of the motherboard.
    :param mf: Main factory resource.
    :param assembly_time: Manufacturing time.
    :param main_assembly_time: Assembly time at the main factory.
    :param components_store: Components store.
    :param transport_time: Transport time to the main factory.
    """
    difficulty = 6
    fuzzy = Fuzzy_assembler()
    main_assembly_time = fuzzy.get_assembly_time(difficulty, system_load)
    
    max_retries = 3  # Retry limit in case of failure
    retries = 0
    
    # Request access to main factory
    print(f'{name}: All motherboard components arrive at time {round(env.now)}')
    
    while retries < max_retries:  # Retry on failure
        # Simulate manufacturing time
        yield env.timeout(assembly_time)
        
        # Simulate 10% failure probability
        if random.random() < 0.1:
            print(f'{name}: Manufacturing failure. Restarting... (Attempt {retries + 1})')
            retries += 1
            continue  # Restart manufacturing process
        
        # Continue if successful
        break  # Exit loop if no failure
    else:
        print(f'{name}: Critical failure. Could not manufacture motherboard.')
        return  # Exit if retry limit exceeded

    with mf.request() as req:
        yield req
        
        # Simulate main factory assembly time
        print(f'{name}: Starts motherboard manufacturing at time {round(env.now)}')
        yield env.timeout(main_assembly_time)
        print(f'{name}: Finishes assembly at time {round(env.now)}')
        
        # Simulate transport to main factory
        arrival = yield env.process(transport(env, transport_time))
        delay = arrival - env.now + transport_time  # Calculate delay
        print(f'{name}: Arrived at Main Factory at time {arrival} (Delay: {delay:.2f})')
        
        
        
        # Check for duplicates in store
        if 'Motherboard' not in components_store.items:
            yield components_store.put('Motherboard')
            print(f'{name}: Motherboard sent to component store at time {round(env.now, 2)}')
        else:
            print(f'{name}: Duplicate motherboard. Ignoring...')