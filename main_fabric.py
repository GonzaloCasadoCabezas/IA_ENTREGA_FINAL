import simpy
import random
import itertools
import pandas as pd
from datetime import datetime
from logic.fuzzy_logic import Fuzzy_assembler
random.seed(123)

# Import component manufacturing processes
from components.storage import storage
from components.box import box
from components.power_supply import power_supply
from components.ram import ram
from components.mother_board import mother_board
from components.processor import processor
from components.cooling_system import cooling_system
from components.graphics_card import graphics_card
from core.final_assembly import final_assembly

simulation_results = []

# Component configuration
components = {
        'Processor': processor,
        'GraphicsCard': graphics_card,
        'Storage': storage,
        'Box': box,
        'PowerSupply': power_supply,
        'RAM': ram,
        'Motherboard': mother_board,
        'CoolingSystem': cooling_system
    }

# Dificulty by component (for fuzzy logic)   
component_difficulties = {
    'Processor': 6,
    'GraphicsCard': 7,
    'Storage': 3,
    'Box': 3,
    'PowerSupply': 5,
    'RAM': 2,
    'Motherboard': 6,
    'CoolingSystem': 4
}


def track_component_process(env, name, component_type, mf, assembly_time,
                          components_store, transport_time, system_load):
    """
    Wrapper function to track component manufacturing process and collect data
    """
    start_time = env.now
    status = "Success"
    
    
    try:
        # Get the correct process function
        process_func = components[component_type]

        # Calcular tiempo de ensamblaje con lógica difusa
        difficulty = component_difficulties[component_type]
        fuzzy = Fuzzy_assembler()
        main_assembly_time = fuzzy.get_assembly_time(difficulty, system_load)

        yield env.process(process_func(
            env, name, mf, assembly_time, components_store, transport_time, system_load
        ))
    except Exception as e:
        status = f"Failed: {str(e)}"
    
    end_time = env.now
    total_time = end_time - start_time
    
    # Store results
    simulation_results.append({
        "Component": component_type,
        "Name": name,
        "Start_Time": start_time,
        "End_Time": end_time,
        "Total_Time": total_time,
        "Assembly_Time": assembly_time,
        "Main_Assembly_Time": main_assembly_time,
        "Transport_Time": transport_time,
        "Status": status
    })

if __name__ == '__main__':
    env = simpy.Environment()
    main_factory = simpy.Resource(env, capacity=1)
    components_store = simpy.Store(env)
    
    from itertools import product
    
    component = list(components.keys())
    transport_times = [2, 3, 4 ,5, 6, 7, 8]
    
    SYSTEM_LOAD = random.randint(0,9)
    
    # Create manufacturing processes USING THE TRACKING FUNCTION
    combinations = list(product(component, transport_times))

    for component_type in components:
        for i in range(1000):  # <-- generates 1000 units for each component
            env.process(track_component_process(
                env,
                f"{component_type}_{i}",
                component_type,
                main_factory,
                1 + i,  
                components_store,
                2 + (i % 3),  
                SYSTEM_LOAD
            ))
            i+1


    # Start final assembly process
    env.process(final_assembly(env, main_factory, components_store, system_load=SYSTEM_LOAD, simulation_results=simulation_results))
        
    # Run the simulation
    env.run()
    
    # Verify data collection
    print(f"\nTotal de registros recolectados: {len(simulation_results)}")
    
    # Create DataFrame if we have data
    if simulation_results:
        df = pd.DataFrame(simulation_results)
        
        # Debug: show column names
        print("\nColumnas disponibles:", df.columns.tolist())
        
        # Calculate transport delay if possible
        required_cols = ['Transport_Time', 'End_Time', 'Start_Time', 
                        'Assembly_Time', 'Main_Assembly_Time']
        if all(col in df.columns for col in required_cols):
            df['Transport_Delay'] = df['Transport_Time'] - (
                df['End_Time'] - df['Start_Time'] - 
                df['Assembly_Time'] - df['Main_Assembly_Time']
            )
        
        # Save to CSV
        csv_filename = "simulation_results.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\nCSV generado correctamente: {csv_filename}")
        print("\nPrimeras filas:")
        print(df.head())
    else:
        print("\nError: No se recolectaron datos durante la simulación")
        print("Posibles causas:")
        print("1. Los procesos no llegaron a ejecutarse completamente")
        print("2. La función track_component_process no se llamó correctamente")
        print("3. La simulación terminó antes de recolectar datos")
