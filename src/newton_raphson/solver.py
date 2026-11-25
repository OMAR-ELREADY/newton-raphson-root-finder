"""Newton-Raphson root finding solver with iteration tracking."""

import numpy as np
import sympy as sp
from typing import Callable, Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class IterationResult:
    """Result of a single Newton-Raphson iteration."""
    n: int
    x_n: float
    f_x_n: float
    f_prime_x_n: float
    x_next: float
    error: float


@dataclass
class SolverResult:
    """Complete result of Newton-Raphson solver."""
    root: Optional[float]
    iterations: List[IterationResult]
    converged: bool
    message: str
    function_str: str
    x0: float


class NewtonRaphsonSolver:
    """Newton-Raphson method for finding roots of nonlinear equations."""

    # Predefined test functions
    PREDEFINED_FUNCTIONS = {
        "x³ - 2x - 5": "x**3 - 2*x - 5",
        "x² - 2": "x**2 - 2",
        "cos(x) - x": "cos(x) - x",
        "x³ - x - 1": "x**3 - x - 1",
        "eˣ - 3x": "exp(x) - 3*x",
        "x·ln(x) - 1": "x*log(x) - 1",
        "sin(x) - x/2": "sin(x) - x/2",
        "x⁴ - 3x² + 1": "x**4 - 3*x**2 + 1",
    }

    def __init__(self, function_str: str, x0: float, tolerance: float = 1e-10, max_iterations: int = 100):
        """
        Initialize the solver.

        Args:
            function_str: Function as string (e.g., "x**3 - 2*x - 5")
            x0: Initial guess
            tolerance: Convergence tolerance
            max_iterations: Maximum number of iterations
        """
        self.function_str = function_str
        self.x0 = x0
        self.tolerance = tolerance
        self.max_iterations = max_iterations

        # Parse function and compute derivative symbolically
        self.x = sp.symbols('x')
        self.f_expr = sp.sympify(function_str)
        self.f_prime_expr = sp.diff(self.f_expr, self.x)

        # Convert to numpy functions for fast evaluation
        self.f = sp.lambdify(self.x, self.f_expr, 'numpy')
        self.f_prime = sp.lambdify(self.x, self.f_prime_expr, 'numpy')

    def solve(self) -> SolverResult:
        """
        Run Newton-Raphson iterations.

        Returns:
            SolverResult with all iteration details
        """
        iterations = []
        x_n = self.x0

        for n in range(self.max_iterations):
            try:
                f_x_n = float(self.f(x_n))
                f_prime_x_n = float(self.f_prime(x_n))
            except Exception as e:
                return SolverResult(
                    root=None,
                    iterations=iterations,
                    converged=False,
                    message=f"Evaluation error at x={x_n}: {str(e)}",
                    function_str=self.function_str,
                    x0=self.x0
                )

            # Check for zero derivative
            if abs(f_prime_x_n) < 1e-14:
                return SolverResult(
                    root=None,
                    iterations=iterations,
                    converged=False,
                    message=f"Derivative near zero at x={x_n} (f'={f_prime_x_n})",
                    function_str=self.function_str,
                    x0=self.x0
                )

            # Newton-Raphson update
            x_next = x_n - f_x_n / f_prime_x_n
            error = abs(x_next - x_n)

            iterations.append(IterationResult(
                n=n + 1,
                x_n=x_n,
                f_x_n=f_x_n,
                f_prime_x_n=f_prime_x_n,
                x_next=x_next,
                error=error
            ))

            # Check convergence
            if error < self.tolerance:
                return SolverResult(
                    root=x_next,
                    iterations=iterations,
                    converged=True,
                    message=f"Converged after {n + 1} iterations",
                    function_str=self.function_str,
                    x0=self.x0
                )

            x_n = x_next

        # Max iterations reached
        return SolverResult(
            root=x_n,
            iterations=iterations,
            converged=False,
            message=f"Max iterations ({self.max_iterations}) reached",
            function_str=self.function_str,
            x0=self.x0
        )

    def get_function_for_plotting(self, x_range: Tuple[float, float], num_points: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Get function values for plotting."""
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        y_vals = self.f(x_vals)
        return x_vals, y_vals

    @classmethod
    def get_predefined_functions(cls) -> dict:
        """Return available predefined functions."""
        return cls.PREDEFINED_FUNCTIONS.copy()