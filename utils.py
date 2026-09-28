import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


# ── Consistent style ──────────────────────────────────────────────────────────

def apply_style():
    """Apply a consistent style for lecture-note figures."""
    mpl.rcParams.update({
        "font.size":          12,
        "axes.labelsize":     13,
        "axes.titlesize":     13,
        "xtick.labelsize":    11,
        "ytick.labelsize":    11,
        "lines.linewidth":    2.0,
        "axes.spines.top":    False,
        "axes.spines.right":  False,
    })


# ── Blackboard-style zero axes ────────────────────────────────────────────────

def set_zero_axes(ax, xlabel=None, ylabel=None):
    """
    Move the left and bottom spines to x=0 and y=0 (blackboard style),
    hide the top and right spines, and optionally add axis labels near
    the ends of the spines.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    xlabel : str, optional
        Label placed at the right end of the horizontal axis.
    ylabel : str, optional
        Label placed at the top end of the vertical axis.
    """
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Hide the zero tick on both axes — its position is obvious from the spines
    ax.set_xticks([t for t in ax.get_xticks() if t != 0])
    ax.set_yticks([t for t in ax.get_yticks() if t != 0])

    # Re-place axis labels at the end of each spine instead of the edge
    if xlabel is not None:
        ax.set_xlabel("")   # clear the default label
        xmin, xmax = ax.get_xlim()
        ymin, _    = ax.get_ylim()
        ax.annotate(
            xlabel,
            xy=(xmax, 0), xycoords="data",
            xytext=(6, 0), textcoords="offset points",
            ha="left", va="center", fontsize=mpl.rcParams["axes.labelsize"],
        )

    if ylabel is not None:
        ax.set_ylabel("")   # clear the default label
        _, ymax = ax.get_ylim()
        ax.annotate(
            ylabel,
            xy=(0, ymax), xycoords="data",
            xytext=(0, 6), textcoords="offset points",
            ha="center", va="bottom", fontsize=mpl.rcParams["axes.labelsize"],
        )


# ── Bifurcation diagram helper ────────────────────────────────────────────────

def plot_bifurcation(ax, branches, param_label="r", var_label="x*",
                     zero_axes=True):
    """
    Plot a bifurcation diagram on the given Axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes to draw on. Create with ``fig, ax = plt.subplots()`` so you
        retain the figure object for further manipulation.
    branches : list of dict
        Each dict describes one branch and may contain:
          - 'x'           (array-like, required) : bifurcation parameter values.
          - 'y'           (array-like, required) : stationary-point values.
          - 'color'       (str, optional)        : line colour; defaults to 'steelblue'.
          - 'linestyle'   (str, optional)        : 'solid' or 'dashed'; defaults to 'solid'.
          - 'label'       (str, optional)        : text to display.
          - 'text_xy'     (tuple, optional)      : (x, y) in data coordinates where the
                                                   label is placed directly on the plot.
                                                   If omitted and 'label' is given, the
                                                   label is added to the legend instead.
          - 'text_kwargs' (dict, optional)       : extra kwargs forwarded to ax.text()
                                                   (e.g. ha, va, fontsize). Only used
                                                   when 'text_xy' is also provided.
    param_label : str
        Label for the horizontal axis (supports LaTeX).
    var_label : str
        Label for the vertical axis (supports LaTeX).
    zero_axes : bool
        If True (default), move spines to x=0 and y=0 (blackboard style).
        Set to False to keep the standard box style.

    Returns
    -------
    lines : list of matplotlib.lines.Line2D
        One Line2D per branch, in the same order as ``branches``.

    Example
    -------
    >>> r1 = np.linspace(0, 1, 100)
    >>> r2 = np.linspace(1, 3, 200)
    >>> fig, ax = plt.subplots()
    >>> plot_bifurcation(
    ...     ax,
    ...     branches = [
    ...         {"x": r1, "y": np.zeros_like(r1), "color": "steelblue", "linestyle": "solid",
    ...          "label": "$x^* = 0$ (stable)",   "text_xy": (0.5,  0.05)},
    ...         {"x": r2, "y": np.zeros_like(r2), "color": "steelblue", "linestyle": "dashed",
    ...          "label": "$x^* = 0$ (unstable)", "text_xy": (2.0, -0.15)},
    ...         {"x": r2, "y": r2 - 1,            "color": "tomato",    "linestyle": "solid",
    ...          "label": "$x^* = r-1$",           "text_xy": (2.5,  1.6)},
    ...     ],
    ...     param_label = "$r$",
    ...     var_label   = "$x^*$",
    ... )
    >>> plt.show()
    """
    lines         = []
    legend_needed = False

    for branch in branches:
        x         = np.asarray(branch["x"])
        y         = np.asarray(branch["y"])
        color     = branch.get("color",     "steelblue")
        linestyle = branch.get("linestyle", "solid")
        label     = branch.get("label",     None)
        text_xy   = branch.get("text_xy",   None)

        # Only pass label to plot() when there is no inline text placement,
        # so it appears in the legend instead.
        plot_label = None if text_xy is not None else label

        (line,) = ax.plot(
            x, y,
            color     = color,
            linestyle = linestyle,
            label     = plot_label,
        )
        lines.append(line)

        # Inline label placed directly on the plot
        if label is not None and text_xy is not None:
            kw = dict(fontsize=mpl.rcParams["font.size"])
            kw.update(branch.get("text_kwargs", {}))
            ax.text(text_xy[0], text_xy[1], label, **kw)

        if label is not None and text_xy is None:
            legend_needed = True

    # Add a legend only if at least one branch uses legend-style labelling
    if legend_needed:
        ax.legend()

    # Apply zero-axes style AFTER plotting so axis limits are already set
    if zero_axes:
        set_zero_axes(ax, xlabel=param_label, ylabel=var_label)
    else:
        ax.set_xlabel(param_label)
        ax.set_ylabel(var_label)

    return lines


def euler_plot(ax, f, exact, x0, h, N, annotate=True):
    """
    Plot the exact solution and Euler approximation on ax.

    Parameters
    ----------
    ax       : matplotlib Axes
    f        : callable, RHS of x'(t) = f(t)
    exact    : callable, exact solution x(t)
    x0       : float, initial condition x(0)
    h        : float, step size
    N        : int, number of Euler steps
    annotate : bool, whether to label x_n points and drop dashed lines
    """

    apply_style()

    # Euler steps
    t_euler = np.array([n * h for n in range(N + 1)])
    x_euler = np.zeros(N + 1)
    x_euler[0] = x0
    for n in range(N):
        x_euler[n + 1] = x_euler[n] + h * f(t_euler[n])

    # Exact solution
    t_fine = np.linspace(0, t_euler[-1] + 0.3, 400)
    x_fine = exact(t_fine)

    # Exact curve
    ax.plot(t_fine, x_fine, color="steelblue", zorder=3, label="Exact")

    # Euler segments
    ax.plot(t_euler, x_euler, color="tomato", zorder=4, label="Euler")

    # Euler points
    for n in range(N + 1):
        ax.plot(t_euler[n], x_euler[n], "o", color="tomato", markersize=4, zorder=5)

        if annotate and n > 0:
            # Vertical dashed drop line
            ax.plot([t_euler[n], t_euler[n]], [0, x_euler[n]],
                    color="gray", linestyle="dashed", linewidth=0.8, zorder=2)
            # Point label
            ax.annotate(
                f"$x_{{{n}}}$",
                xy=(t_euler[n], x_euler[n]),
                xytext=(t_euler[n], x_euler[n] + 0.2),
                fontsize=11,
                ha="center",
                va="bottom",
                zorder=6
            )

    # Axes
    ax.set_xlim(-0.1, t_euler[-1] + 0.5)
    ax.set_ylim(-0.1, max(x_fine.max(), x_euler.max()) + 0.4)
    set_zero_axes(ax, xlabel="$t$", ylabel="$x(t)$")

    # t_n ticks only when annotating
    if annotate:
        ax.set_xticks(t_euler[1:])
        ax.set_xticklabels([f"$t_{{{n + 1}}}$" for n in range(N)])
    else:
        ax.set_xticks([])

    ax.set_yticks([x0])
    ax.set_yticklabels(["$x_0$"])


# ── Cobweb diagram helper ─────────────────────────────────────────────────────

def cobweb_plot(ax, f, x0, N, xlim, annotate=True):
    """
    Draw a cobweb diagram for the iterated map x_{n+1} = f(x_n).

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes to draw on.
    f : callable
        The map function x_{n+1} = f(x_n).
    x0 : float
        Initial condition.
    N : int
        Number of iterations to draw.
    xlim : tuple
        (xmin, xmax) range for plotting f and the diagonal.
    annotate : bool
        If True, label each x_n on the horizontal axis with a dashed drop line.

    Returns
    -------
    xs : list of float
        The orbit [x_0, x_1, ..., x_N].
    """
    xmin, xmax = xlim
    x_plot = np.linspace(xmin, xmax, 400)

    # ── f(x) curve and diagonal ───────────────────────────────────────────────
    ax.plot(x_plot, f(x_plot), color="steelblue", zorder=3, label="$f(x)$")
    ax.plot(x_plot, x_plot,    color="gray",      zorder=2, linestyle="dashed",
            linewidth=1.2, label="$y = x$")

    # ── Compute orbit ─────────────────────────────────────────────────────────
    xs = [x0]
    for _ in range(N):
        xs.append(f(xs[-1]))

    # ── Cobweb lines ──────────────────────────────────────────────────────────
    # For each step: vertical line from (x_n, x_n) to (x_n, f(x_n)),
    # then horizontal line from (x_n, f(x_n)) to (f(x_n), f(x_n))
    for n in range(N):
        xn  = xs[n]
        xn1 = xs[n + 1]
        # Vertical segment
        ax.plot([xn,  xn],  [xn, xn1], color="tomato", lw=1.5, zorder=4)
        # Horizontal segment
        ax.plot([xn, xn1], [xn1, xn1], color="tomato", lw=1.5, zorder=4)

    # Solid vertical line at x0 from x axis
    ax.plot([x0, x0], [0, x0], color="tomato", lw=1.5, zorder=4)

    # ── Annotations ───────────────────────────────────────────────────────────   
    if annotate:
    # Annotate x0 on the x-axis only
        ax.annotate(
            f"$x_0$",
            xy=(x0, 0),
            xytext=(x0, -0.04 * (ax.get_ylim()[1] - ax.get_ylim()[0])),
            ha="center", va="top", fontsize=11,
        )
        for n, xn in enumerate(xs[1:]):
            # Dashed vertical drop line to x-axis
            ax.plot([xn, xn], [0, xn], color="gray", linestyle="dashed",
                    linewidth=0.8, zorder=2)
            # Dashed horizontal drop line to y-axis
            ax.plot([0, xn], [xn, xn], color="gray", linestyle="dashed",
                    linewidth=0.8, zorder=2)
            # Label on x-axis
            ax.annotate(
                f"$x_{{{n + 1}}}$",
                xy=(xn, 0),
                xytext=(xn, -0.04 * (ax.get_ylim()[1] - ax.get_ylim()[0])),
                ha="center", va="top", fontsize=11,
            )
            # Label on y-axis
            ax.annotate(
                f"$x_{{{n + 1}}}$",
                xy=(0, xn),
                xytext=(-0.04 * (ax.get_xlim()[1] - ax.get_xlim()[0]), xn),
                ha="right", va="center", fontsize=11,
            )

    # ── Axes style ────────────────────────────────────────────────────────────
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(xmin, xmax)
    set_zero_axes(ax, xlabel="$x_n$", ylabel="$x_{{{n+1}}}$")
    if annotate:
        ax.set_xticks([])
        ax.set_yticks([])

    return xs


# ── Covid-19 data plotting helper ─────────────────────────────────────────────

def plot_covid_data(ax, csv_path, start_date, end_date,
                    relative_days=True, ylabel="Cases", color="steelblue"):
    """
    Plot COVID (or similar) time-series data from a CSV file.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes to draw on.
    csv_path : str
        Path to the CSV file. Must have columns 'date' (YYYY-MM-DD) and
        'metric_value'.
    start_date : str
        Start of the date range to plot, in 'YYYY-MM-DD' format (inclusive).
    end_date : str
        End of the date range to plot, in 'YYYY-MM-DD' format (inclusive).
    relative_days : bool
        If True (default), the x-axis shows days elapsed since start_date
        (first point = day 0) and is labelled 'Days'.
        If False, the x-axis shows the actual dates and is labelled 'Date'.
    ylabel : str
        Label for the vertical axis. Defaults to 'Cases'.
    color : str
        Colour of the plotted line. Defaults to 'steelblue'.

    Returns
    -------
    df : pandas.DataFrame
        The filtered dataframe, in case you need the data for overlaying models.
    """
    # ── Load and filter ───────────────────────────────────────────────────────
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = df.sort_values("date")
    mask = (df["date"] >= pd.Timestamp(start_date)) & \
           (df["date"] <= pd.Timestamp(end_date))
    df = df.loc[mask].reset_index(drop=True)

    if df.empty:
        raise ValueError(f"No data found between {start_date} and {end_date}.")

    # ── x values ─────────────────────────────────────────────────────────────
    if relative_days:
        x = (df["date"] - df["date"].iloc[0]).dt.days
        xlabel = "Days"
    else:
        x = df["date"]
        xlabel = "Date"

    # ── Plot ─────────────────────────────────────────────────────────────────
    ax.plot(x, df["metric_value"], color=color, zorder=3)

    # ── Axes style ────────────────────────────────────────────────────────────
    ax.set_xlim(x.iloc[0], x.iloc[-1])
    ax.set_ylim(0, df["metric_value"].max() * 1.10)

    if relative_days:
        set_zero_axes(ax, xlabel=xlabel, ylabel=ylabel)
    else:
        # For absolute dates, zero-axes style doesn't make much sense —
        # use a standard bottom spine instead
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
        ax.set_yticks([])

    return df

def _plot_phase_portrait_base(ax, rhs, starts, xlim, ylim,
                              t_max=10, n_grid=20, alpha=0.3,
                              traj_color=None, backward=True,
                              t_arrows=[5], axis_labels=("$x_1$", "$x_2$"),
                              show_ticks=False, show_field=True):
    """
    Private base function for phase portraits. Handles vector field,
    trajectories, clipping, and directional arrows. Called by both
    plot_phase_portrait and plot_phase_portrait_nonlinear.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    rhs : callable
        RHS of the system as rhs(t, y) -> array of shape (2,).
    starts : list of (float, float)
        Initial conditions.
    xlim : tuple
    ylim : tuple
    t_max : float
    n_grid : int
    alpha : float
    traj_color : str, list, or None
    backward : bool
    t_arrows : list of float
    axis_labels : tuple of str
        (xlabel, ylabel). Defaults to ("$x_1$", "$x_2$").
    show_ticks : bool
        If True, show default matplotlib ticks. If False (default), hide all
        ticks.
    show_field : bool
        If True (default), draw the vector field quiver plot. Set to False
        when overlaying a second system on the same axes to avoid duplicate
        vector fields.
    """
    import numpy as np
    from scipy.integrate import solve_ivp

    # ── Vector field ──────────────────────────────────────────────────────────
    if show_field:
        x_grid = np.linspace(xlim[0], xlim[1], n_grid)
        y_grid = np.linspace(ylim[0], ylim[1], n_grid)
        X, Y   = np.meshgrid(x_grid, y_grid)

        UV = np.array([rhs(0, [xi, yi])
                       for xi, yi in zip(X.ravel(), Y.ravel())]).T
        U  = UV[0].reshape(X.shape)
        V  = UV[1].reshape(X.shape)

        norm            = np.sqrt(U**2 + V**2)
        norm[norm == 0] = 1
        U_norm          = U / norm
        V_norm          = V / norm

        ax.quiver(X, Y, U_norm, V_norm,
                  alpha=alpha, color="gray",
                  angles="xy", scale_units="xy",
                  scale=n_grid / (xlim[1] - xlim[0]) * 1.5,
                  width=0.003, zorder=1)

    # ── Trajectories ─────────────────────────────────────────────────────────
    if traj_color is None:
        colors = [f"C{i}" for i in range(len(starts))]
    elif isinstance(traj_color, list):
        colors = [traj_color[i % len(traj_color)] for i in range(len(starts))]
    else:
        colors = [traj_color] * len(starts)

    for (x0, y0), color in zip(starts, colors):
        y0_vec = [x0, y0]

        sol_fwd = solve_ivp(rhs, [0,  t_max], y0_vec,
                            max_step=0.01, dense_output=True)

        if backward:
            sol_bwd = solve_ivp(rhs, [0, -t_max], y0_vec,
                                max_step=0.01, dense_output=True)
            t_bwd  = -sol_bwd.t[::-1]
            y_bwd  =  sol_bwd.y[:, ::-1]
            t_full =  np.concatenate([t_bwd, sol_fwd.t])
            y_full =  np.concatenate([y_bwd, sol_fwd.y], axis=1)
        else:
            t_full = sol_fwd.t
            y_full = sol_fwd.y

        # Clip to plot limits
        in_bounds = (
            (y_full[0] >= xlim[0]) & (y_full[0] <= xlim[1]) &
            (y_full[1] >= ylim[0]) & (y_full[1] <= ylim[1])
        )
        indices = np.where(in_bounds)[0]
        if len(indices) == 0:
            continue

        breaks   = np.where(np.diff(indices) > 1)[0] + 1
        segments = np.split(indices, breaks)

        for seg in segments:
            if len(seg) < 2:
                continue

            ax.plot(y_full[0, seg], y_full[1, seg],
                    color=color, lw=1.5, zorder=3)

            # ── Directional arrows at specified times ─────────────────────
            for t_arrow in t_arrows:
                idx = np.argmin(np.abs(t_full - t_arrow))
                seg_match = np.where(seg == idx)[0]
                if len(seg_match) == 0:
                    continue
                pos = seg_match[0]
                if pos >= len(seg) - 1:
                    continue
                i0 = seg[pos]
                i1 = seg[pos + 1]
                ax.annotate(
                    "",
                    xy    =(y_full[0, i1], y_full[1, i1]),
                    xytext=(y_full[0, i0], y_full[1, i0]),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
                    zorder=5,
                )

        # ── Initial point (only when not plotting backward) ───────────────
        if not backward:
            ax.plot(x0, y0, "o", color=color, markersize=5, zorder=4)

    # ── Axes style ────────────────────────────────────────────────────────────
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")
    set_zero_axes(ax, xlabel=axis_labels[0], ylabel=axis_labels[1])

    if not show_ticks:
        ax.set_xticks([])
        ax.set_yticks([])


def plot_phase_portrait(ax, A, starts, xlim, ylim,
                        t_max=10, n_grid=20, alpha=0.3,
                        traj_color=None, backward=True,
                        t_arrows=[5], show_info=True, ax_info=None,
                        draw_evs=False, axis_labels=("$x_1$", "$x_2$"),
                        show_ticks=False, show_field=True):
    """
    Plot a phase portrait for the linear system x' = A x.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes to draw on.
    A : array-like, shape (2, 2)
        The system matrix.
    starts : list of (float, float)
        Initial conditions (x0, y0) for each trajectory.
    xlim : tuple
        (xmin, xmax) for the plot range.
    ylim : tuple
        (ymin, ymax) for the plot range.
    t_max : float
        Integration time, both forward and backward. Default 10.
    n_grid : int
        Number of grid points per axis for the vector field. Default 20.
    alpha : float
        Transparency of the vector field arrows. Default 0.3.
    traj_color : str, list, or None
        If None, each trajectory gets a colour from the default cycle.
        If a string, all trajectories use that colour.
        If a list, trajectories cycle through the list.
    backward : bool
        If True (default), integrate backward in time as well as forward.
    t_arrows : list of float
        Times at which to place a directional arrow along each trajectory.
    show_info : bool
        If True (default), display the matrix, eigenvalues, and eigenvectors.
    ax_info : matplotlib.axes.Axes or None
        If provided, the matrix/eigenvalue/eigenvector info is laid out in a
        single row in this axes (intended as a short, wide strip above ax).
        If None and show_info is True, such a strip is created above ax.
    draw_evs : bool
        If True, draw lines through the origin along each real eigenvector.
        Default False.
    axis_labels : tuple of str
        (xlabel, ylabel). Defaults to ("$x_1$", "$x_2$").
    show_ticks : bool
        If True, show default matplotlib ticks. Default False.
    show_field : bool
        If True (default), draw the vector field. Set to False when overlaying
        on top of a nonlinear phase portrait.

    Returns
    -------
    None
    """
    import numpy as np
    import sympy as sp

    A = np.array(A)

    rhs = lambda t, y: A @ y

    _plot_phase_portrait_base(
        ax, rhs, starts, xlim, ylim,
        t_max=t_max, n_grid=n_grid, alpha=alpha,
        traj_color=traj_color, backward=backward,
        t_arrows=t_arrows, axis_labels=axis_labels,
        show_ticks=show_ticks, show_field=show_field,
    )

    # ── Eigenvector lines ─────────────────────────────────────────────────────
    if draw_evs:
        vals, vecs = np.linalg.eig(A)

        def _ev_line(ax, vec, linestyle):
            """Draw a line through the origin along vec, clipped to limits."""
            vx, vy = vec
            ts = []
            if abs(vx) > 1e-10:
                ts += [xlim[0] / vx, xlim[1] / vx]
            if abs(vy) > 1e-10:
                ts += [ylim[0] / vy, ylim[1] / vy]
            t_pos = min((t for t in ts if t > 0), default=10)
            t_neg = max((t for t in ts if t < 0), default=-10)
            ax.plot([t_neg * vx, t_pos * vx], [t_neg * vy, t_pos * vy],
                    color="black", lw=1, linestyle=linestyle, zorder=2)
            return t_pos, t_neg

        seen = {}
        for lam, vec in zip(vals, vecs.T):
            if not np.isreal(lam):
                continue
            lam = lam.real
            vec = vec.real / np.linalg.norm(vec.real)
            vx, vy = vec

            t_pos, t_neg = _ev_line(ax, vec, "dashed")

            # Arrows
            if lam > 0:
                for t_tip, t_tail in [(t_pos, 0.8 * t_pos),
                                       (t_neg, 0.8 * t_neg)]:
                    ax.annotate("",
                        xy    =(t_tip  * vx, t_tip  * vy),
                        xytext=(t_tail * vx, t_tail * vy),
                        arrowprops=dict(arrowstyle="->", color="black", lw=1),
                        zorder=3)
            elif lam < 0:
                NEAR = 0.15
                for t_tail in [0.5 * t_pos, 0.5 * t_neg]:
                    ax.annotate("",
                        xy    =(NEAR * np.sign(t_tail) * vx,
                                NEAR * np.sign(t_tail) * vy),
                        xytext=(t_tail * vx, t_tail * vy),
                        arrowprops=dict(arrowstyle="->", color="black", lw=1),
                        zorder=3)

            # Generalised eigenvector for repeated eigenvalues
            for seen_lam, seen_vec in seen.items():
                if abs(lam - seen_lam) < 1e-8:
                    M = A - lam * np.eye(2)
                    u, _, _, _ = np.linalg.lstsq(M, seen_vec, rcond=None)
                    u = u / np.linalg.norm(u)
                    _ev_line(ax, u, "dotted")

            seen[lam] = vec

    # ── Info panel ────────────────────────────────────────────────────────────
    if show_info:
        A_sym    = sp.nsimplify(sp.Matrix(A.tolist()), rational=True)
        eigvects = A_sym.eigenvects()
        eig_vals = []
        eig_vecs = []
        for val, mult, vecs_list in eigvects:
            for v in vecs_list:
                eig_vals.append(val)
                eig_vecs.append(v)

        def fmt_vec(v):
            idx = 0 if v[0] != 0 else 1
            v   = sp.simplify(v / v[idx])
            return (f"\\left(\\begin{{array}}{{c}} {sp.latex(v[0])} \\\\ "
                    f"{sp.latex(v[1])} \\end{{array}}\\right)")

        # Three blocks in one row: matrix | eigenvalues (stacked) | eigenvectors
        matrix_text = (
            f"A = \\left(\\begin{{array}}{{cc}} "
            f"{sp.latex(A_sym[0,0])} & {sp.latex(A_sym[0,1])} \\\\ "
            f"{sp.latex(A_sym[1,0])} & {sp.latex(A_sym[1,1])} "
            f"\\end{{array}}\\right)"
        )
        evals_text = (
            "\\begin{array}{l} "
            + " \\\\ ".join(f"\\lambda_{{{i}}} = {sp.latex(val)}"
                            for i, val in enumerate(eig_vals, 1))
            + " \\end{array}"
        )
        evecs_text = ", \\quad ".join(f"v_{{{i}}} = {fmt_vec(vec)}"
                                      for i, vec in enumerate(eig_vecs, 1))
        text = "$" + " \\quad\\; ".join([matrix_text, evals_text, evecs_text]) + "$"

        # If no info axes is given, create a strip of fixed relative height
        # directly above the phase portrait
        if ax_info is None:
            ax_info = ax.inset_axes([0, 1.02, 1, 0.22])
        ax_info.axis("off")

        ax_info.text(0.5, 0.5, text,
                     transform=ax_info.transAxes,
                     fontsize=12, va="center", ha="center",
                     usetex=True)


def plot_phase_portrait_nonlinear(ax, rhs, starts, xlim, ylim,
                                  t_max=10, n_grid=20, alpha=0.3,
                                  traj_color=None, backward=True,
                                  t_arrows=[5], axis_labels=("$x_1$", "$x_2$"),
                                  show_ticks=False, show_field=True):
    """
    Plot a phase portrait for a nonlinear system x' = f(x, y), y' = g(x, y).

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes to draw on.
    rhs : callable
        RHS of the system as rhs(t, y) -> array of shape (2,).
    starts : list of (float, float)
        Initial conditions (x0, y0) for each trajectory.
    xlim : tuple
        (xmin, xmax) for the plot range.
    ylim : tuple
        (ymin, ymax) for the plot range.
    t_max : float
        Integration time, both forward and backward. Default 10.
    n_grid : int
        Number of grid points per axis for the vector field. Default 20.
    alpha : float
        Transparency of the vector field arrows. Default 0.3.
    traj_color : str, list, or None
        If None, each trajectory gets a colour from the default cycle.
        If a string, all trajectories use that colour.
        If a list, trajectories cycle through the list.
    backward : bool
        If True (default), integrate backward in time as well as forward.
    t_arrows : list of float
        Times at which to place a directional arrow along each trajectory.
    axis_labels : tuple of str
        (xlabel, ylabel). Defaults to ("$x_1$", "$x_2$").
    show_ticks : bool
        If True, show default matplotlib ticks. Default False.
    show_field : bool
        If True (default), draw the vector field. Set to False when overlaying
        on top of another phase portrait.

    Returns
    -------
    None
    """
    _plot_phase_portrait_base(
        ax, rhs, starts, xlim, ylim,
        t_max=t_max, n_grid=n_grid, alpha=alpha,
        traj_color=traj_color, backward=backward,
        t_arrows=t_arrows, axis_labels=axis_labels,
        show_ticks=show_ticks, show_field=show_field,
    )

