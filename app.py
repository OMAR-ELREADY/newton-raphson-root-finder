"""Streamlit app for Newton-Raphson Root Finder."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from src.newton_raphson import NewtonRaphsonSolver, SolverResult


# Page config
st.set_page_config(
    page_title="Newton-Raphson Root Finder",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .iteration-table {
        font-family: 'Monospace', monospace;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)


def create_iteration_table(result: SolverResult) -> pd.DataFrame:
    """Create a DataFrame for iteration display."""
    data = []
    for it in result.iterations:
        data.append({
            "Iteration": it.n,
            "xₙ": f"{it.x_n:.10f}",
            "f(xₙ)": f"{it.f_x_n:.6e}",
            "f'(xₙ)": f"{it.f_prime_x_n:.6e}",
            "xₙ₊₁": f"{it.x_next:.10f}",
            "|Error|": f"{it.error:.6e}"
        })
    return pd.DataFrame(data)


def create_plot(result: SolverResult, x_range: tuple = None) -> go.Figure:
    """Create interactive Plotly visualization."""
    if x_range is None:
        # Auto-determine range from iterations
        x_vals = [it.x_n for it in result.iterations] + [it.x_next for it in result.iterations]
        x_min, x_max = min(x_vals), max(x_vals)
        margin = (x_max - x_min) * 0.3 if x_max != x_min else 1.0
        x_range = (x_min - margin, x_max + margin)

    # Get function values for plotting - use normalized expression
    solver = NewtonRaphsonSolver(result.function_str, result.x0)
    x_plot, y_plot = solver.get_function_for_plotting(x_range)

    # Use original expression for display if available
    display_expr = getattr(result, 'original_function_str', result.function_str)

    fig = go.Figure()

    # Function curve
    fig.add_trace(go.Scatter(
        x=x_plot,
        y=y_plot,
        mode='lines',
        name=f'f(x) = {display_expr}',
        line=dict(color='#667eea', width=3),
        hovertemplate='x: %{x:.4f}<br>f(x): %{y:.4f}<extra></extra>'
    ))

    # Zero line
    fig.add_trace(go.Scatter(
        x=[x_range[0], x_range[1]],
        y=[0, 0],
        mode='lines',
        name='y = 0',
        line=dict(color='gray', width=1, dash='dash'),
        hoverinfo='skip'
    ))

    # Iteration points
    x_iters = [it.x_n for it in result.iterations]
    y_iters = [it.f_x_n for it in result.iterations]

    # Tangent lines for each iteration
    for i, it in enumerate(result.iterations):
        # Tangent line: y = f'(x_n)(x - x_n) + f(x_n)
        x_tangent = np.array([x_range[0], x_range[1]])
        y_tangent = it.f_prime_x_n * (x_tangent - it.x_n) + it.f_x_n
        fig.add_trace(go.Scatter(
            x=x_tangent,
            y=y_tangent,
            mode='lines',
            name=f'Tangent {it.n}',
            line=dict(color='rgba(118, 75, 162, 0.3)', width=1, dash='dot'),
            showlegend=(i == 0),
            legendgroup='tangents',
            hovertemplate=f'Tangent {it.n}<br>x: %{{x:.4f}}<br>y: %{{y:.4f}}<extra></extra>'
        ))

    # Iteration points on curve
    fig.add_trace(go.Scatter(
        x=x_iters,
        y=y_iters,
        mode='markers+lines',
        name='Iterations',
        marker=dict(
            size=12,
            color=list(range(len(x_iters))),
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Iteration"),
            line=dict(width=2, color='white')
        ),
        line=dict(color='#764ba2', width=2, dash='dot'),
        hovertemplate='Iteration: %{customdata}<br>xₙ: %{x:.6f}<br>f(xₙ): %{y:.6f}<extra></extra>',
        customdata=[f"#{it.n}" for it in result.iterations]
    ))

    # Root point (final)
    if result.converged and result.root is not None:
        fig.add_trace(go.Scatter(
            x=[result.root],
            y=[0],
            mode='markers',
            name=f'Root ≈ {result.root:.8f}',
            marker=dict(size=16, color='#00d4aa', symbol='star', line=dict(width=2, color='white')),
            hovertemplate=f'Root: {result.root:.10f}<br>f(root): 0<extra></extra>'
        ))

    # Initial guess
    fig.add_trace(go.Scatter(
        x=[result.x0],
        y=[solver.f(result.x0)],
        mode='markers',
        name=f'x₀ = {result.x0}',
        marker=dict(size=14, color='#ff6b6b', symbol='diamond', line=dict(width=2, color='white')),
        hovertemplate=f'Initial guess: {result.x0}<br>f(x₀): {solver.f(result.x0):.6f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text=f"Newton-Raphson: f(x) = {display_expr}",
            font=dict(size=18, color='#333'),
            x=0.5
        ),
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_white",
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1
        ),
        height=600,
        margin=dict(l=60, r=60, t=80, b=60)
    )

    return fig


def create_convergence_plot(result: SolverResult, tolerance: float = 1e-10) -> go.Figure:
    """Create convergence analysis plot."""
    fig = go.Figure()

    iterations = [it.n for it in result.iterations]
    errors = [it.error for it in result.iterations]
    f_values = [abs(it.f_x_n) for it in result.iterations]

    fig.add_trace(go.Scatter(
        x=iterations,
        y=errors,
        mode='lines+markers',
        name='|xₙ₊₁ - xₙ|',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=iterations,
        y=f_values,
        mode='lines+markers',
        name='|f(xₙ)|',
        line=dict(color='#764ba2', width=3),
        marker=dict(size=8)
    ))

    # Tolerance line
    fig.add_trace(go.Scatter(
        x=[1, len(iterations)] if iterations else [1, 2],
        y=[tolerance, tolerance],
        mode='lines',
        name='Tolerance',
        line=dict(color='red', width=2, dash='dash')
    ))

    fig.update_layout(
        title="Convergence Analysis",
        xaxis_title="Iteration",
        yaxis_title="Error / |f(x)|",
        yaxis_type="log",
        template="plotly_white",
        height=400,
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )

    return fig


def main():
    # Header
    st.markdown('<h1 class="main-header">🔬 Newton-Raphson Root Finder</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Interactive visualization of Newton-Raphson method for finding roots of nonlinear equations</p>', unsafe_allow_html=True)

    # Sidebar - Input
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Function input method
        input_method = st.radio(
            "Function Input",
            ["Predefined Functions", "Custom Expression"],
            help="Choose a test function or enter your own"
        )

        predefined_funcs = NewtonRaphsonSolver.get_predefined_functions()

        if input_method == "Predefined Functions":
            func_name = st.selectbox(
                "Select Function",
                options=list(predefined_funcs.keys()),
                index=0
            )
            function_str = predefined_funcs[func_name]
            st.code(f"f(x) = {function_str}", language="python")
        else:
            function_str = st.text_input(
                "Enter f(x) = 0",
                value="x**3 - 2*x - 5",
                help="Supports: x^3 or x³, 2x or 2*x, sin(x), cos(x), exp(x), log(x) or ln(x), sqrt(x), π, eˣ"
            )
            st.caption("Examples: x^3 - 2x - 5  |  x³ - 2x - 5  |  2x + 3  |  sin(x) - x/2  |  e^x - 3x  |  √x - 1")

        # Initial guess
        x0 = st.number_input(
            "Initial Guess (x₀)",
            value=2.0,
            step=0.1,
            format="%.4f",
            help="Starting point for iterations"
        )

        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            tolerance = st.number_input(
                "Tolerance",
                value=1e-10,
                format="%.2e",
                help="Stop when |xₙ₊₁ - xₙ| < tolerance"
            )
            max_iter = st.slider(
                "Max Iterations",
                min_value=10,
                max_value=200,
                value=100,
                step=10
            )

        # Run button
        run_button = st.button("🚀 Find Root", type="primary", use_container_width=True)

    # Main content
    if run_button:
        with st.spinner("Running Newton-Raphson iterations..."):
            try:
                solver = NewtonRaphsonSolver(
                    function_str=function_str,
                    x0=x0,
                    tolerance=tolerance,
                    max_iterations=max_iter
                )
                result = solver.solve()

                # Store in session state for persistence
                st.session_state['result'] = result
                st.session_state['function_str'] = function_str
                st.session_state['x0'] = x0
                st.session_state['solver'] = solver
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try: x^3 - 2x - 5, sin(x) - x/2, e^x - 3x, √x - 1, ln(x) - 1")
                st.stop()

    # Display results if available
    if 'result' in st.session_state:
        result: SolverResult = st.session_state['result']

        # Status metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            status = "✅ Converged" if result.converged else "⚠️ Not Converged"
            st.metric("Status", status)

        with col2:
            st.metric("Iterations", len(result.iterations))

        with col3:
            root_str = f"{result.root:.8f}" if result.root is not None else "—"
            st.metric("Root", root_str)

        with col4:
            final_error = result.iterations[-1].error if result.iterations else 0
            st.metric("Final Error", f"{final_error:.2e}")

        # Message
        if result.converged:
            st.success(f"🎯 {result.message}")
        else:
            st.warning(f"⚠️ {result.message}")

        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualization", "📋 Iteration Table", "📈 Convergence", "📝 Details"])

        with tab1:
            st.plotly_chart(create_plot(result), use_container_width=True)

            # Plot controls
            col1, col2 = st.columns(2)
            with col1:
                x_min = st.number_input("X Min", value=-5.0, step=0.5)
            with col2:
                x_max = st.number_input("X Max", value=5.0, step=0.5)
            if st.button("Update Plot Range"):
                st.rerun()

        with tab2:
            df = create_iteration_table(result)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Iteration": st.column_config.NumberColumn("Iteration", width="small"),
                    "xₙ": st.column_config.TextColumn("xₙ", width="medium"),
                    "f(xₙ)": st.column_config.TextColumn("f(xₙ)", width="medium"),
                    "f'(xₙ)": st.column_config.TextColumn("f'(xₙ)", width="medium"),
                    "xₙ₊₁": st.column_config.TextColumn("xₙ₊₁", width="medium"),
                    "|Error|": st.column_config.TextColumn("|Error|", width="medium"),
                }
            )

            # Download button
            csv = df.to_csv(index=False)
            download_name = getattr(result, 'original_function_str', function_str)
            st.download_button(
                "📥 Download CSV",
                csv,
                f"newton_raphson_{download_name.replace('*', '').replace(' ', '_').replace('^', '')}.csv",
                "text/csv"
            )

        with tab3:
            st.plotly_chart(create_convergence_plot(result, tolerance), use_container_width=True)

            # Convergence rate estimation
            if len(result.iterations) >= 3:
                st.subheader("📊 Convergence Rate Analysis")
                errors = [it.error for it in result.iterations[-4:]]
                if errors[0] > 0 and errors[1] > 0:
                    rate = np.log(errors[1] / errors[0]) / np.log(errors[0] / errors[1]) if errors[1] != errors[0] else 2
                    st.info(f"Estimated convergence order: ~{rate:.2f} (quadratic expected for Newton-Raphson)")

        with tab4:
            st.subheader("📝 Solver Details")
            col1, col2 = st.columns(2)
            with col1:
                if hasattr(result, 'original_function_str') and result.original_function_str != result.function_str:
                    st.write(f"**Original:** f(x) = {result.original_function_str}")
                    st.write(f"**Parsed:** f(x) = {result.function_str}")
                else:
                    st.write(f"**Function:** f(x) = {result.function_str}")
                st.write(f"**Initial guess:** x₀ = {result.x0}")
                st.write(f"**Tolerance:** {tolerance}")
                st.write(f"**Max iterations:** {max_iter}")
            with col2:
                st.write(f"**Iterations performed:** {len(result.iterations)}")
                st.write(f"**Converged:** {'Yes' if result.converged else 'No'}")
                if result.root is not None:
                    solver = st.session_state.get('solver')
                    if solver:
                        st.write(f"**Root:** {result.root:.12f}")
                        st.write(f"**f(root):** {solver.f(result.root):.2e}")

            # Show the formula
            st.markdown("---")
            st.subheader("📐 Newton-Raphson Formula")
            st.latex(r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}")
            st.caption("The method uses the tangent line at each point to find the next approximation.")

    else:
        # Welcome screen
        st.info("👈 Configure your function and initial guess in the sidebar, then click **Find Root**")

        # Example gallery
        st.subheader("🎯 Example Functions to Try")
        cols = st.columns(3)
        examples = [
            ("x³ - 2x - 5", "2.0", "Root ≈ 2.09455"),
            ("cos(x) - x", "0.5", "Root ≈ 0.73908"),
            ("eˣ - 3x", "1.0", "Root ≈ 0.61906"),
        ]
        for col, (func, guess, root) in zip(cols, examples):
            with col:
                st.code(f"f(x) = {func}")
                st.write(f"x₀ = {guess}")
                st.success(f"Root: {root}")


if __name__ == "__main__":
    main()