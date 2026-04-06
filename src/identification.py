import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from src.model import MassSpringDamper
import os


class SystemIdentifier:
    """
    Handles data generation and parameter identification
    for the Mass-Spring-Damper system.
    """

    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        os.makedirs(self.data_path, exist_ok=True)

    def generate_data(self,
                      m_true=1.0,
                      k_true=10.0,
                      c_true=2.0,
                      noise_level=0.02,
                      t_max=30.0,
                      num_points=2000,
                      seed=42):
        """
        Generates simulated data with realistic noise.
        """

        print("🔄 Generating simulated data with noise...")

        # Reproducibility
        np.random.seed(seed)

        # True system (ground truth)
        system = MassSpringDamper(m=m_true, k=k_true, c=c_true)

        # Input signal (step)
        F_step = system.step_input(amplitude=1.0, start_time=2.0)

        # Simulation
        result = system.simulate(
            t_span=(0, t_max),
            F_func=F_step,
            num_points=num_points
        )

        t_sim = result["t"]
        x_true = result["x"]

        # Add Gaussian noise
        noise = noise_level * np.random.randn(len(x_true))
        x_noisy = x_true + noise

        # Create dataset
        df = pd.DataFrame({
            "time": t_sim,
            "input": [F_step(t) for t in t_sim],
            "position": x_noisy,
            "position_true": x_true
        })

        # Save to CSV
        filepath = os.path.join(self.data_path, "simulated_data.csv")
        df.to_csv(filepath, index=False)

        print(f"✅ Data generated and saved to: {filepath}")
        print(f"   Noise level: ±{noise_level * 100:.1f}%")
        print(f"   Number of samples: {len(df)}")

        return df

    def identify_parameters(self,
                            df: pd.DataFrame,
                            initial_guess=[1.0, 2.0, 10.0]):
        """
        Performs parameter identification using least squares.

        Returns:
            dict: Estimated parameters and cost
        """

        print("\n Starting parameter identification (least squares)...")

        # Extract data
        t = df["time"].values
        u = df["input"].values
        y = df["position"].values

        # Residual function
        def residuals(params):
            m, c, k = params

            model = MassSpringDamper(m=m, k=k, c=c)

            # Interpolated input signal
            def F_func(ti):
                return np.interp(ti, t, u)

            # Simulate model with same time resolution
            result_sim = model.simulate(
                t_span=(t[0], t[-1]),
                F_func=F_func,
                num_points=len(t)
            )

            y_sim = result_sim["x"]

            return y_sim - y

        # Parameter bounds (realistic)
        bounds = ([0.1, 0.1, 1.0], [5.0, 20.0, 50.0])

        # Optimization
        result = least_squares(
            residuals,
            initial_guess,
            bounds=bounds,
            ftol=1e-8
        )

        m_est, c_est, k_est = result.x
        cost = result.cost

        print("✅ Identification complete!")
        print(f"   Estimated parameters:")
        print(f"      m = {m_est:.4f} kg")
        print(f"      c = {c_est:.4f} Ns/m")
        print(f"      k = {k_est:.4f} N/m")
        print(f"   Cost (error): {cost:.6f}")

        return {
            "m": m_est,
            "c": c_est,
            "k": k_est,
            "cost": cost
        }