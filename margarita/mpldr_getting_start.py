import matplotlib.pyplot as plt
import mpld3

my_plot = plt.plot([3, 1, 4, 1, 5], 'ks-', mec='w', mew=5, ms=20)
# mpld3.show()
# plt.savefig('mpld3_fig1.svg')


html_str = mpld3.fig_to_html(my_plot[0].figure, )

print(html_str)
