def add_dynamic_bounds(yali, y):
    """Use external concentrations to bound the uptake flux of glucose."""
    biomass, glucose = y  # expand the boundary species
#    glucose_max_import = -10 * glucose / (5 + glucose)
#    yali.reactions.y001714.lower_bound = glucose_max_import


def dynamic_system(t, y):
    """Calculate the time derivative of external species."""

    biomass, glucose = y  # expand the boundary species

    # Calculate the specific exchanges fluxes at the given external concentrations.
    with yali:
        add_dynamic_bounds(yali, y)

        cobra.util.add_lp_feasibility(yali)
        feasibility = cobra.util.fix_objective_as_constraint(yali)
        lex_constraints = cobra.util.add_lexicographic_constraints(
            yali, ['xBIOMASS', 'y001714'], ['max', 'max'])

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