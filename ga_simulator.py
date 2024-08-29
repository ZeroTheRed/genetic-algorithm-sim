import dearpygui.dearpygui as dpg
import genetic_algorithm as ga
import random
import numpy as np
from matplotlib import cm
import constants as const

dpg.create_context()

def simulate_genetic_algorithm():
    population_size = dpg.get_value("pop_size")
    lower_bound = dpg.get_value("lbound")
    upper_bound = dpg.get_value("ubound")
    mutation_rate = dpg.get_value("mut_rate")
    tournament_size = dpg.get_value("tour_size")
    no_of_generations = dpg.get_value("num_gens")

    best_soln, final_populn, best_ind, best_pfers, ga_table = ga.genetic_algorithm(
        population_size,
        lower_bound,
        upper_bound,
        no_of_generations,
        mutation_rate,
        tournament_size
    )

    for a in range(3):
        dpg.set_value(f"Final population {a}", [list(range(len(final_populn))), [x[a] for x in final_populn]])
        dpg.set_value(f"Best individual {a}", [[final_populn.index(best_ind)], [best_ind[a]]])
        dpg.fit_axis_data(f"Population Y Axis {a}")

    dpg.delete_item(f"Curves")
    for i in range(len(best_pfers)):
        dpg.delete_item(f"Curve {i}")

    colormap = cm.get_cmap('viridis')
    colours = [colormap(i / no_of_generations) for i in range(no_of_generations)]

    colours_rgb = [(int(r*255), int(g*255), int(b*255), 255) for r,g,b,_ in colours]

    for b, (best_i, best_fit) in enumerate(best_pfers):
        coeff_a, coeff_b, coeff_c = best_i
        xrange = np.linspace(lower_bound, upper_bound, 400)
        yrange = coeff_a * (xrange ** 2) + coeff_b * xrange + coeff_c

        with dpg.theme() as series_theme: 
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line, colours_rgb[b], category=dpg.mvThemeCat_Plots)

        dpg.add_line_series(list(xrange), list(yrange), parent="Quad function Y", label=f"Curve {b+1}", tag=f"Curve {b}")
        dpg.bind_item_theme(dpg.last_item(), series_theme)

    generations_list = list(range(1, len(best_pfers) + 1))
    dpg.delete_item("lines")

    for i in range(3):
        dpg.delete_item(f"ga_line_{i}")
        dpg.fit_axis_data(f"ga_params")
        dpg.fit_axis_data("gens")

        with dpg.theme() as lines_theme:
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line, const.SCATTER_COLORS[i], category=dpg.mvThemeCat_Plots)

        dpg.add_line_series(generations_list,
                            [idx[0][i] for idx in best_pfers],
                            parent="ga_params",
                            label=const.COEFF_LABELS[i],
                            tag=f"ga_line_{i}")
        dpg.bind_item_theme(dpg.last_item(), lines_theme)

    update_table(ga_table)

def update_table(table):
    table.border = False
    table.header = False

    for i in range(0, 20):
        dpg.set_value(f"cell_{i}0", i + 1)
        dpg.set_value(f"cell_{i}1", float(table[i].get_string(fields=["a"]).strip()))
        dpg.set_value(f"cell_{i}2", float(table[i].get_string(fields=["b"]).strip()))
        dpg.set_value(f"cell_{i}3", float(table[i].get_string(fields=["c"]).strip()))
        dpg.set_value(f"cell_{i}4", float(table[i].get_string(fields=["Fitness"]).strip()))

# Main Window
def main():
    with dpg.window(tag="Primary Window"):
        # Themes for the final population scatter-plots
        for i in range(3):
            with dpg.theme(tag=f"Final population scatter theme {i}"):
                with dpg.theme_component(dpg.mvScatterSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, const.SCATTER_COLORS[i], category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, const.SCATTER_COLORS[i], category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, const.MARKER_STYLES[i], category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, const.SCATTER_MARKER_SIZE, category=dpg.mvThemeCat_Plots)

            with dpg.theme(tag=f"Best individual theme {i}"):
                with dpg.theme_component(dpg.mvScatterSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, const.BEST_INDIVIDUAL_COLORS[i], category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, const.BEST_INDIVIDUAL_COLORS[i], category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Circle, category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, const.BEST_INDIVIDUAL_MARKER_SIZE, category=dpg.mvThemeCat_Plots)

        # Input - population size
        dpg.add_input_int(label="Population size", width=const.FIELD_WIDTH, tag="pop_size")

        # Input - bounds
        with dpg.group(horizontal=True):
            dpg.add_input_float(label="Lower bound", width=const.FIELD_WIDTH, tag="lbound")
            dpg.add_input_float(label="Upper bound", width=const.FIELD_WIDTH, tag="ubound")

        # Input - no. of generations
        dpg.add_input_int(label="No. of generations", width=const.FIELD_WIDTH, tag="num_gens")

        # Input - mutation rate and tournament selection size
        with dpg.group(horizontal=True):
            dpg.add_input_float(label="Mutation rate", width=const.FIELD_WIDTH, tag="mut_rate")
            dpg.add_input_int(label="Tournament size", width=const.FIELD_WIDTH, tag="tour_size")

        # Plots
        with dpg.group(horizontal=True):
            # Final population and best individual scatter-plot
            with dpg.subplots(const.NUM_PLOTS, 1, label="Final Populations", width=const.PLOT_WIDTH, height=const.PLOT_HEIGHT):
                for i in range(3):
                    with dpg.plot():
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, label="Individual Index")
                        with dpg.plot_axis(dpg.mvYAxis, label=const.COEFF_LABELS[i], tag=f"Population Y Axis {i}"):
                            dpg.set_axis_limits_auto(f"Population Y Axis {i}")

                            dpg.add_scatter_series(list(range(100)),
                                                   [random.random() for _ in range(100)],
                                                   label=f"{const.COEFF_LABELS[i]}",
                                                   tag=f"Final population {i}")
                            dpg.add_scatter_series([i*20],
                                                   [random.random()],
                                                   label=f"Best individual {const.COEFF_LABELS[i]}",
                                                   tag=f"Best individual {i}")

                            dpg.bind_item_theme(f"Final population {i}", f"Final population scatter theme {i}")
                            dpg.bind_item_theme(f"Best individual {i}", f"Best individual theme {i}")

            # Quadratic function curve plot
            with dpg.plot(label="Quadratic Function", width=const.PLOT_WIDTH, height=const.PLOT_HEIGHT):
                dpg.add_plot_axis(dpg.mvXAxis, label="X")
                dpg.add_plot_axis(dpg.mvYAxis, label="Y", tag="Quad function Y")
                dpg.add_plot_legend(location=dpg.mvPlot_Location_North)

                curve_x_range = np.linspace(-50, 50, 400)
                curve_y_range = 2*(curve_x_range**2) + 3*curve_x_range + 4

                dpg.add_line_series(list(curve_x_range), list(curve_y_range), parent="Quad function Y", label="test", tag="Curves")

            # Plot of parameter change over generations
            with dpg.plot(label="Parameter change over generations", width=const.PLOT_WIDTH, height=const.PLOT_HEIGHT):
                dpg.add_plot_axis(dpg.mvXAxis, label="Generations", tag="gens")
                dpg.add_plot_axis(dpg.mvYAxis, label="Parameters", tag="ga_params")
                dpg.add_plot_legend()

                dpg.add_line_series([1, 2], [1, 2], parent="ga_params", tag="lines")

        with dpg.theme() as best_solution_theme:
            with dpg.theme_component(dpg.mvTableRow):
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (0, 200, 0, 255), category=dpg.mvThemeCat_Core)

        # Table - Coefficients and fitness values over generations
        with dpg.table(header_row=True, row_background=True,
                       borders_innerH=True, borders_outerH=True, borders_innerV=True,
                       borders_outerV=True, tag="params_table"):

            dpg.add_table_column(label="Generation")
            dpg.add_table_column(label="a")
            dpg.add_table_column(label="b")
            dpg.add_table_column(label="c")
            dpg.add_table_column(label="Best Fitness")

            for i in range(0, 20):
                with dpg.table_row():
                    for j in range(0, 5):
                        dpg.add_text("0", tag=f"cell_{i}{j}")

            dpg.bind_item_theme(f"")

        dpg.add_button(label="Simulate", callback=simulate_genetic_algorithm)

    dpg.create_viewport(title="Genetic Algorithm Simulator")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()