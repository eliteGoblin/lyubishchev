import plotly.graph_objs as go
from arrow import Arrow

from lyubishchev.data_model import TimeInterval
from lyubishchev.report import get_time_interval_aggregation_dict_tree
from time_report_notebook.nb_helper_util import dict_tree_to_parent_tree, m2h


def sunburst_time_intervals(
    wakeup_timestamp: Arrow, time_intervals: list[TimeInterval]
) -> None:
    aggregation_dict_tree = get_time_interval_aggregation_dict_tree(
        wakeup_timestamp=wakeup_timestamp,
        time_intervals=time_intervals,
    )
    labels, parents, values = dict_tree_to_parent_tree(aggregation_dict_tree)
    fig = go.Figure(
        go.Sunburst(
            labels=labels,
            parents=parents,
            values=m2h(values),
            textinfo="label+percent entry",
            # maxdepth=3,
        )
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.show()
