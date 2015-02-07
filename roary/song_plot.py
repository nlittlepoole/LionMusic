from nvd3 import scatterChart

def make_plot(xdata, ydata):
    output_file = open('../templates/roary/scatterChart.html', 'w')

    type = "scatterChart"
    chart = scatterChart(name=type, height=350, width=550, x_is_date=False)

    kwargs1 = {'shape': 'circle', 'size': '1'}

    extra_serie = {"tooltip": {"y_start": "", "y_end": " calls"}}
    chart.add_serie(name="songs", y=ydata, x=xdata, extra=extra_serie, **kwargs1)

    chart.buildhtml()
    chart.htmlcontent = chart.htmlcontent.replace('./bower', './static/js/bower')
    output_file.write(chart.htmlcontent)
    output_file.close()
