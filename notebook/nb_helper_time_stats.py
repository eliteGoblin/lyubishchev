import matplotlib.pyplot as plt

def time_stat_to_pie_chart_data(time_stat: dict[str, int]) -> dict[str, int]:
    """
    cherry-pick data from timestats, and return a dict for pie chart
    """

    res = {
        "sleep": time_stat["sleep_all"],
        "work": time_stat["work"],
        "exercise": time_stat["exercise"],
        "self_improving": time_stat["self_improving"],
        "sex": time_stat["sex"],
    }

    res["other"] = time_stat["total"] - sum(res.values())

    return res

def show_time_stat_as_piechart(report_time_stat: dict[str, int]) -> None:
    """
    show time stat as a pie chart
    """
    piechart_data = time_stat_to_pie_chart_data(report_time_stat)

    fig, ax = plt.subplots()
    ax.pie(piechart_data.values(), labels=piechart_data.keys(), autopct='%1.1f%%')
    ax.set_title("Pie Chart of Data")
    plt.show()