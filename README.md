# 🔬 Newton-Raphson Root Finder

An interactive web application for finding roots of nonlinear equations using the **Newton-Raphson method**, with beautiful visualizations and step-by-step iteration tracking.

## ✨ Features

- **Interactive Function Input**: Choose from predefined test functions or enter your own custom expression
- **Real-time Visualization**: See the function curve, tangent lines at each iteration, and convergence path
- **Detailed Iteration Table**: Track every step with xₙ, f(xₙ), f'(xₙ), xₙ₊₁, and error
- **Convergence Analysis**: Log-scale error plots with convergence rate estimation
- **Export Results**: Download iteration data as CSV
- **Responsive Design**: Works on desktop and mobile

## 🚀 Live Demo

**[Try it now on Streamlit Cloud →](https://newton-raphson-root-finder.streamlit.app)**

## 📸 Screenshots

| Visualization | Iteration Table | Convergence |
|---------------|-----------------|-------------|
| Function graph with tangents | Step-by-step iterations | Error convergence |

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/newton-raphson-root-finder.git
cd newton-raphson-root-finder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📦 Dependencies

- **Streamlit** - Web app framework
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computations
- **SymPy** - Symbolic mathematics (automatic derivatives)
- **Pandas** - Data handling

## 🧮 Newton-Raphson Method

The Newton-Raphson method finds roots of f(x) = 0 using the iteration:

```
x_{n+1} = x_n - f(x_n) / f'(x_n)
```

The method uses the tangent line at each approximation to find the next one, typically achieving **quadratic convergence** near the root.

### Predefined Test Functions

| Function | Expression | Typical Root |
|----------|------------|--------------|
| Cubic | x³ - 2x - 5 | ≈ 2.09455 |
| Square root of 2 | x² - 2 | ≈ 1.41421 |
| Cosine fixed point | cos(x) - x | ≈ 0.73908 |
| Plastic ratio | x³ - x - 1 | ≈ 1.32472 |
| Exponential | eˣ - 3x | ≈ 0.61906 |
| Logarithmic | x·ln(x) - 1 | ≈ 1.76322 |
| Sine | sin(x) - x/2 | ≈ 1.89549 |
| Quartic | x⁴ - 3x² + 1 | ≈ 1.61803 |

## 🌐 Deployment

### Streamlit Cloud (Free)

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → Select your fork
4. Main file: `app.py`
5. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app`

### Other Platforms

- **Render**: Use `streamlit run app.py` as start command
- **Railway**: Auto-detects Streamlit
- **Heroku**: Requires `Procfile` with `web: streamlit run app.py --server.port=$PORT`

## 📁 Project Structure

```
newton-raphson-root-finder/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore
└── src/
    └── newton_raphson/
        ├── __init__.py
        └── solver.py     # Core Newton-Raphson implementation
```

## 🎯 Usage

1. **Select a function** from the sidebar (predefined or custom)
2. **Enter initial guess** x₀
3. **Adjust tolerance** and max iterations if needed
4. **Click "Find Root"** to run the solver
5. **Explore results** in the tabs:
   - 📊 Visualization: Interactive plot with tangents
   - 📋 Iteration Table: All steps with values
   - 📈 Convergence: Error analysis
   - 📝 Details: Solver configuration

## 🔬 Mathematical Background

The Newton-Raphson method approximates the root by:
1. Starting with initial guess x₀
2. Drawing tangent line at (x₀, f(x₀))
3. Finding where tangent crosses x-axis → x₁
4. Repeating until |x_{n+1} - x_n| < tolerance

**Convergence**: Quadratic (order 2) for simple roots when f'(root) ≠ 0

**Requirements**: f(x) must be differentiable, f'(x) ≠ 0 near root

## 📝 License

MIT License - feel free to use for learning and projects!

## 🤝 Contributing

PRs welcome! Ideas:
- Add more root-finding methods (Secant, Bisection, Fixed-point)
- Complex root finding
- 3D visualization for systems of equations
- More export formats (JSON, LaTeX)

---

Built with ❤️ using Streamlit, Plotly, and SymPy