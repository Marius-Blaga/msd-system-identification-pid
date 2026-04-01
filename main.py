"""
Main script for Stage 1 - Open Loop Simulation
Runs a basic simulation and generates the first plot.
"""

from src.model import MassSpringDamper
from src.visualization import Visualizer


def main():
    print("🚀 Starting Stage 1: Open-Loop Simulation\n")
    
    # 1. Create system (plant)
    msd = MassSpringDamper(m=1.0, k=10.0, c=2.0)
    viz = Visualizer()
    
    # 2. Define step input
    step_input = msd.step_input(amplitude=1.0, start_time=1.0)
    
    # 3. Run simulation
    print("Running simulation...")
    result = msd.simulate(t_span=(0, 25), F_func=step_input)
    
    t = result["t"]
    x = result["x"]
    velocity = result["x_dot"]
    
    print(f"✅ Simulation complete! Final time: {t[-1]:.1f} s")
    
    # 4. Validate steady-state
    expected_ss = 1.0 / msd.k
    simulated_ss = x[-1]
    
    print(f"Expected steady-state: {expected_ss:.4f} m")
    print(f"Simulated steady-state: {simulated_ss:.4f} m\n")
    
    # 5. Plot result
    viz.plot_response(
        t=t,
        x=x,
        title="Open-Loop Step Response\n(m=1 kg, k=10 N/m, c=2 Ns/m)",
        filename="step_response_openloop.png",
        show=True
    )
    
    print("🎉 Stage 1 completed successfully!")
    print("Check the 'figures/' folder for results.")


if __name__ == "__main__":
    main()