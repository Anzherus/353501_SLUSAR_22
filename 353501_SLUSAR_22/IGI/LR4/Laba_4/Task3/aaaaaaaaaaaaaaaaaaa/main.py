# main.py
"""
Arcsin(x) Calculator using Power Series Expansion
Lab Work #3: Numerical Methods for Special Functions with Class Implementation
Version: 3.0
Developer: Slusar Stanislav
Date: 2025-05-02
"""

from arcsin_calculator import ArcsinCalculator, ArcsinInputHandler

def main():
    print("\n=== Arcsin(x) Calculator ===")
    print(f"Version: {ArcsinCalculator.version}")
    print("Computes arcsin(x) using power series expansion with statistical analysis")
    
    input_handler = ArcsinInputHandler()
    
    while True:
        try:
            print("\nChoose input method:")
            print("1 - Manual input")
            print("2 - Random generation")
            print("3 - Exit")
            choice = input("Your choice (1/2/3): ").strip()
            
            if choice == '1':
                input_handler.initialize_from_input()
            elif choice == '2':
                input_handler.initialize_from_generator()
            elif choice == '3':
                print("\nProgram completed.")
                break
            else:
                print("Error: invalid choice")
                continue
                
            eps = input_handler.input_eps()
            input_handler.calculator.run_calculations(eps)
            input_handler.calculator.print_results_table()
            
            # Plot results
            if len(input_handler.calculator.results) > 1:
                save_plot = input("Save plot to file? (y/n): ").strip().lower()
                if save_plot == 'y':
                    filename = input("Enter filename (e.g., plot.png): ").strip()
                    input_handler.calculator.plot_results(filename)
                else:
                    input_handler.calculator.plot_results()
            
            if input("\nRepeat calculations? (y/n): ").strip().lower() != 'y':
                print("\nProgram completed.")
                break
                
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            if input("Continue? (y/n): ").strip().lower() != 'y':
                break

if __name__ == "__main__":
    main()