import numpy as np

def euler_step(t, X, f, dt):
    """
    Perform a single step of the Euler method to approximate the solution of a differential equation.

    Args:
        t (float): Current time.
        X (array): Current value of the solution.
        f (function): Function that defines the differential equation.
        dt (float): Time step.

    Returns:
        array: Approximate solution at time t+dt.
    """

    

    return X + f(t, X) * dt


def rk4_step(t, X, f, dt):
    """
    Perform a single step of the fourth-order Runge-Kutta method to approximate the solution of a differential equation.

    Args:
        t (float): Current time.
        X (array): Current value of the solution.
        f (function): Function that defines the differential equation.
        dt (float): Time step.

    Returns:
        array: Approximate solution at time t+dt.
    """

    k1 = f(t, X)
    k2 = f(t, X + 0.5 * dt * k1)
    k3 = f(t, X + 0.5 * dt * k2)
    k4 = f(t, X + dt * k3)
    return X + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


def midpoint_step(t, X, f, dt):
    """
    Perform a single step of the midpoint method to approximate the solution of a differential equation.

    Args:
        t (float): Current time.
        X (array): Current value of the solution.
        f (function): Function that defines the differential equation.
        dt (float): Time step.

    Returns:
        array: Approximate solution at time t+dt.
    """

    k1 = f(t, X)
    k2 = f(t + dt / 2, X + dt / 2 * k1)
    return X + dt * k2


def improved_euler_step(t, X, f, dt):
    """
    Perform a single step of the improved Euler method to approximate the solution of a differential equation.

    Args:
        t (float): Current time.
        X (array): Current value of the solution.
        f (function): Function that defines the differential equation.
        dt (float): Time step.

    Returns:
        array: Approximate solution at time t+dt.
    """

    k1 = f(t, X)
    k2 = f(t + dt, X + dt * k1)
    return X + dt * (k1 + k2) / 2


def solve_to(f, x0, t0, t1, dt, dt_max, step_func=rk4_step):
    """
    Solve a differential equation numerically using a given numerical method from a starting time to an end time.

    Args:
        f (function): Function that defines the differential equation.
        x0 (array): Initial value of the solution.
        t0 (float): Starting time.
        t1 (float): End time.
        dt (float): Time step.
        dt_max (float): Maximum time step.
        step_func (function): Numerical method to use (default is the fourth-order Runge-Kutta method).

    Returns:
        tuple: Tuple of arrays representing the time points and the approximate solutions at those time points.
    """
    if not callable(f):
        raise TypeError("The argument 'f' must be a function.")
    if not isinstance(t0, (int, float)):
        raise TypeError("The argument 't0' must be a number.")
    if not isinstance(t1, (int, float)):
        raise TypeError("The argument 't1' must be a number.")
    if t0 <= 0:
        raise ValueError("The argument 't0' must be positive.")
    if t1 <= 0:
        raise ValueError("The argument 't1' must be positive.")
    if not isinstance(x0, np.ndarray):
        raise TypeError("The argument 'x0' must be a numpy array.")
    if not isinstance(dt, (int, float)):
        raise TypeError("The argument 'dt' must be a number.")
    if dt <= 0:
        raise ValueError("The argument 'dt' must be positive.")
    if dt_max <= 0:
        raise ValueError("The argument 'dt' must be positive.")
    if not callable(step_func):
        raise ValueError("The argument 'step_func' must be a function.")



    t = np.arange(t0, t1+dt, dt)
    X = np.zeros((len(t), len(x0)))
    X[0] = x0
    for i in range(1, len(t)):
        dt = min(t[i]-t[i-1], dt_max)
        X[i] = step_func(t[i-1], X[i-1], f, dt)
    return t, X