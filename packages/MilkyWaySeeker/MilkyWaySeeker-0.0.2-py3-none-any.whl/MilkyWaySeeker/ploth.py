import matplotlib.pyplot as plt
from laspec.mpl import set_cham
set_cham(latex=True)

def ploth_scatter(x_plot, y_plot, x_sub_list, y_sub_list, fmt_list, label_list, plot_range,
                  x_label="X", ylabel="Y",
                  show_legend=False, figsize=None, fn_save=None):
    if figsize is not None:
        fig = plt.figure(figsize=figsize)
    else:
        fig = plt.figure(figsize=(6,4))
    ax = fig.add_axes(plot_range)
    plt.plot(x_plot, y_plot,'.', color="gray", ms=1)
    for x_sub_tmp, y_sub_tmp, fmt_tmp, label_tmp in zip(x_sub_list, y_sub_list):
        plt.plot(x_sub_tmp, y_sub_tmp, fmt_tmp, label=label_tmp)

    if show_legend:
        plt.legend(fontsize=14)
