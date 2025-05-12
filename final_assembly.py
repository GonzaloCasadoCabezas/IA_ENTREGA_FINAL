import simpy
import random
from logic.fuzzy_logic import Fuzzy_assembler
random.seed(123)

def final_assembly(env, main_factory, components_store, system_load, simulation_results):
    required_components = [
        'Processor', 'GraphicsCard', 'Storage',
        'Box', 'PowerSupply', 'RAM', 'Motherboard', 'CoolingSystem'
    ]
    computer_counter = 0  # Computer assembly counter
    
    while True:
        collected_components = []
        # Component collection phase
        while len(collected_components) < len(required_components):
            component = yield components_store.get()
            
            if component in collected_components:
                print(f'Duplicate {component} received at time {round(env.now)}. Ignoring...')
                continue
                
            collected_components.append(component)
            print(f'{component} for computer {computer_counter} arrived at assembly line at time {round(env.now)}')
        
        # Component verification
        if set(collected_components) == set(required_components):
            difficulty = 6
            fuzzy = Fuzzy_assembler()
            estimated_time = fuzzy.get_assembly_time(difficulty, system_load)
            print(f'Starting assembly of computer {computer_counter} at time {round(env.now)}. Estimated duration: (fuzzy): {estimated_time:.2f}')
            
            # Simulate random assembly failure (10% probability)
            if random.random() < 0.1:
                print(f'ERROR! Computer {computer_counter} assembly failed at time {round(env.now)}. Restarting...')
                collected_components.clear()
                continue  # Restart process without incrementing counter
            
            # Successful assembly simulation
            try:
                yield env.timeout(random.uniform(estimated_time - 1, estimated_time + 1))
                print(f'Computer {computer_counter} successfully assembled at time {round(env.now)}')
                simulation_results.append({
                    "Component": "Computer",
                    "Name": f"Computer_{computer_counter}",
                    "Start_Time": None,
                    "End_Time": env.now,
                    "Total_Time": None,
                    "Assembly_Time": estimated_time,
                    "Main_Assembly_Time": None,
                    "Transport_Time": None,
                    "Status": "Success"
                })
                computer_counter += 1
            except simpy.Interrupt:
                print(f'Assembly interrupted for computer {computer_counter}')
        
        else:
            missing = set(required_components) - set(collected_components)
            print(f'Missing components for computer {computer_counter} at time {round(env.now)}: {", ".join(missing)}')
        
        collected_components.clear()
