
from slither import Slither
from pyvis.network import Network
import argparse

def visualize_contract(contract_path: str, output_file: str = "visualization.html"):
    try:
        
        slither = Slither(contract_path)
        
        net = Network(height="800px", width="100%", directed=True)
        net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=250)

        for contract in slither.contracts:
            net.add_node(contract.name, shape="box", color="#4CAF50", title=contract.name)
            
            for function in contract.functions:
                func_label = f"{contract.name}.{function.name}"
                net.add_node(func_label, 
                            title=f"Function: {function.name}\nVisibility: {function.visibility}",
                            color="#2196F3")
                
                
                net.add_edge(contract.name, func_label)
                
                for internal_call in function.internal_calls:
                    call_label = f"{contract.name}.{internal_call.name}"
                    net.add_edge(func_label, call_label, color="#FF9800")
                
                for external_call in function.high_level_calls:
                    contract_name, func_name = external_call
                    if func_name:
                        ext_label = f"{contract_name.name}.{func_name.name}"
                        net.add_edge(func_label, ext_label, color="#F44336", dashes=True)

        net.show(output_file)
        print(f"Visualisasi berhasil dibuat: {output_file}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Contract Visualizer")
    parser.add_argument("contract", help="Path to Solidity contract file")
    parser.add_argument("-o", "--output", default="visualization.html", help="Output HTML file")
    
    args = parser.parse_args()
    
    visualize_contract(args.contract, args.output)
