def add_dynamic_bounds(yali, y):
    """Use external concentrations to bound the uptake flux of glucose."""
    biomass, glucose, xpool_ac_em = y  # expand the boundary species
#    glucose_max_import = -10 * glucose / (5 + glucose)
#    yali.reactions.y001714.lower_bound = glucose_max_import


def dynamic_system(t, y):
    """Calculate the time derivative of external species."""

    biomass, glucose, xpool_ac_em = y  # expand the boundary species

    # Calculate the specific exchanges fluxes at the given external concentrations.
    with yali:
        add_dynamic_bounds(yali, y)

        cobra.util.add_lp_feasibility(yali)
        feasibility = cobra.util.fix_objective_as_constraint(yali)
        lex_constraints = cobra.util.add_lexicographic_constraints(
            yali, ['xBIOMASS', 'y001714', 'xPOOL_AC_EM'], ['max', 'max','max'])

    # Since the calculated fluxes are specific rates, we multiply them by the
    # biomass concentration to get the bulk exchange rates.
    fluxes = lex_constraints.values
    fluxes *= biomass

    # This implementation is **not** efficient, so I display the current
    # simulation time using a progress bar.
    if dynamic_system.pbar is not None:
        dynamic_system.pbar.update(1)
        dynamic_system.pbar.set_description('t = {:.3f}'.format(t))

    return fluxes

dynamic_system.pbar = None


def infeasible_event(t, y):
    """
    Determine solution feasibility.

    Avoiding infeasible solutions is handled by solve_ivp's built-in event detection.
    This function re-solves the LP to determine whether or not the solution is feasible
    (and if not, how far it is from feasibility). When the sign of this function changes
    from -epsilon to positive, we know the solution is no longer feasible.

    """

    with yali:

        add_dynamic_bounds(yali, y)

        cobra.util.add_lp_feasibility(yali)
        feasibility = cobra.util.fix_objective_as_constraint(yali)

    return feasibility - infeasible_event.epsilon

infeasible_event.epsilon = 1E-6
infeasible_event.direction = 1
infeasible_event.terminal = True

-------------------------------------------------------------------------------------------------
ts = np.linspace(0, 25, 50)  # Desired integration resolution and interval
y0 = [0.1, 10, 0]

with tqdm() as pbar:
    dynamic_system.pbar = pbar

    sol = solve_ivp(
        fun=dynamic_system,
        events=[infeasible_event],
        t_span=(ts.min(), ts.max()),
        y0=y0,
        t_eval=ts,
        rtol=1e-6,
        atol=1e-8,
        method='BDF'
    )
-------------------------------------------------------------------------------------------------------
fig, ax1 = plt.subplots()

ax1.plot(sol.t, sol.y.T[:, 0], color='r', marker='+', markersize=5)
ax2 = plt.twinx(ax1)
ax2.plot(sol.t, sol.y.T[:, 1], color='b', marker='x', markersize=5)

ax3 = ax1.twinx()
ax3.plot(sol.t, sol.y.T[:, 2],color="green")
ax3.spines['right'].set_position(('outward',60))

plt.grid(axis = 'both', color = 'green', linestyle = '--', linewidth = 0.5)

ax1.set_ylabel('Biomass', color='r')
ax2.set_ylabel('Glucose', color='b')
ax3.set_ylabel('Acyl CoA Pool', color='g')

