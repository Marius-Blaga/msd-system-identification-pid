import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from src.model import MassSpringDamper
import os


class SystemIdentifier:
    """
    Data generation and parameter identification for MSD system.
    """

    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        os.makedirs(self.data_path, exist_ok=True)

    def generate_data(self, m_true=1.0, k_true=10.0, c_true=2.0,
                      noise_level=0.005, t_max=30.0, num_points=2000, seed=42):
        """Generate simulated data with noise"""
        print("🔄 Generating simulated data with noise...")

        np.random.seed(seed)

        system = MassSpringDamper(m=m_true, k=k_true, c=c_true)
        F_step = system.step_input(amplitude=1.0, start_time=2.0)

        result = system.simulate(t_span=(0, t_max), F_func=F_step, num_points=num_points)

        t = result["t"]
        x_true = result["x"]

        x_noisy = x_true + noise_level * np.random.randn(len(x_true))

        df = pd.DataFrame({
            "time": t,
            "input": [F_step(ti) for ti in t],
            "position": x_noisy,
            "position_true": x_true
        })

        filepath = os.path.join(self.data_path, "simulated_data.csv")
        df.to_csv(filepath, index=False)

        print(f"✅ Data saved to: {filepath}")
        print(f"   Noise level: ±{noise_level*100:.1f}% | Samples: {len(df)}")
        return df

    def identify_parameters(self, df, initial_guess=[1.0, 2.0, 10.0]):
        """Parameter identification using least squares"""
        print("\n🔍 Performing parameter identification...")

        t = df['time'].values
        u = df['input'].values
        y = df['position'].values

        def residuals(params):
            m, c, k = params
            model = MassSpringDamper(m=m, k=k, c=c)
            
            def F_func(ti):
                idx = np.argmin(np.abs(t - ti))
                return u[idx]

            # Crucial: same number of points and same time grid
            sim_result = model.simulate((t[0], t[-1]), F_func=F_func, num_points=len(t))
            y_sim = sim_result["x"]

            return y_sim - y

        bounds = ([0.5, 0.5, 5.0], [2.5, 5.0, 20.0])

        result = least_squares(
            residuals, 
            initial_guess, 
            bounds=bounds,
            ftol=1e-12,
            xtol=1e-12,
            gtol=1e-12,
            max_nfev=3000
        )

        m_est = float(result.x[0])
        c_est = float(result.x[1])
        k_est = float(result.x[2])
        cost = float(result.cost)

        m_err = abs(m_est - 1.0) * 100
        c_err = abs(c_est - 2.0) / 2.0 * 100
        k_err = abs(k_est - 10.0) / 10.0 * 100

        print(f"✅ Identification completed!")
        print(f"   Estimated : m = {m_est:.4f} kg | c = {c_est:.4f} Ns/m | k = {k_est:.4f} N/m")
        print(f"   Errors    : m = {m_err:.2f}% | c = {c_err:.2f}% | k = {k_err:.2f}%")
        print(f"   Cost      : {cost:.6f}")
        print(f"   Success   : {result.success}")

        return m_est, c_est, k_est, cost