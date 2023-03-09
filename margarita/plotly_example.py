import plotly.express as px
import plotly.io as pio
fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
# fig.write_html('first_figure.html', auto_open=True, full_html=False)

html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
print(html)
