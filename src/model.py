import numpy as np
from scipy.integrate import solve_ivp

class MassSpringDamper:
    def __init__(self, m=1.0, k=10.0, c=2.0):
        if m <= 0:
            raise ValueError("The mass needs to be > 0")
        self.m = m
        self.k = k
        self.c = c

    def __repr__(self):
        return f"MassSpringDamper(m={self.m}, c={self.c}, k={self.k})"

    def _dynamics(self, t, state, F_func):
        x, x_dot = state
        F = F_func(t)
        x_ddot = (F - self.c * x_dot - self.k * x) / self.m
        return [x_dot, x_ddot]

    def simulate(self, t_span, x0=None, F_func=None, num_points=1000):
        if x0 is None:
            x0 = [0.0, 0.0]
        if F_func is None:
            F_func = lambda t: 0.0

        t_eval = np.linspace(t_span[0], t_span[1], num_points)

        sol = solve_ivp(
            fun=self._dynamics,
            t_span=t_span,
            y0=x0,
            t_eval=t_eval,
            args=(F_func,),
            method='RK45'
        )

        return {
            "t": sol.t,
            "x": sol.y[0],
            "x_dot": sol.y[1]
        }

    def step_input(self, amplitude=1.0, start_time=0.0):
        return lambda t: amplitude if t >= start_time else 0.0

    def sinusoidal_input(self, amplitude=1.0, frequency=1.0):
        return lambda t: amplitude * np.sin(2 * np.pi * frequency * t)