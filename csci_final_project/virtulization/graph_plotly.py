import plotly.graph_objs as go
import plotly.offline as offline
from csci_final_project.dataloader import filehandler


def plot_csv_result(df, title, filename, file_path):
    traces = []
    trace = go.Scatter(x=df['start_date'], y=df['pnl'].cumsum(), name='PnL')
    traces.append(trace)
    layout = go.Layout(
        title=title,
        xaxis=dict(showgrid=False, zerolinecolor='black'),
        yaxis=dict(title='', showline=True),
    )
    fig = go.Figure(data=traces, layout=layout)
    offline.plot(fig, filename=file_path + filename + '.html', auto_open=False)


def read_csv_file_and_plot(filename, file_path, graph_title='PnL Curve'):
    df = filehandler.loadCSV(filename, file_path)
    plot_csv_result(df, graph_title, filename.split('.')[0] + '_graph', file_path)

# read_csv_file_and_plot('sample.csv', 'data/')
# read_csv_file_and_plot('best_trades.csv', 'data/')