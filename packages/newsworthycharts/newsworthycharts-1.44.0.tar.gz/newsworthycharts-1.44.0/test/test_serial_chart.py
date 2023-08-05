from newsworthycharts import SerialChart
from newsworthycharts.storage import DictStorage, LocalStorage
import pytest

# store test charts to this folder for visual verfication
OUTPUT_DIR = "test/rendered_charts"
local_storage = LocalStorage(OUTPUT_DIR)


def test_color_function():
    container = {}
    ds = DictStorage(container)

    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2016-01-01", -4],
                ["2017-01-01", 4],
                ["2018-01-01", None],
                ["2019-01-01", -1]
            ]
        ],
        "type": "bars",
        "color_fn": "positive_negative",
        "highlight": "2019-01-01",
    }
    c = SerialChart.init_from(chart_obj, storage=ds)
    c.render("test", "png")

    neutral_color = c._nwc_style["neutral_color"]
    pos_color = c._nwc_style["positive_color"]
    neg_color = c._nwc_style["negative_color"]
    bar_colors = [bar.get_facecolor() for bar in c.ax.patches]
    assert bar_colors[0] == neg_color
    assert bar_colors[1] == pos_color
    assert bar_colors[2] == neutral_color
    assert bar_colors[3] == neg_color

    chart_obj["color_fn"] = "warm_cold"
    c = SerialChart.init_from(chart_obj, storage=ds)
    c.render("test", "png")

    warm_color = c._nwc_style["warm_color"]
    cold_color = c._nwc_style["cold_color"]
    bar_colors = [bar.get_facecolor() for bar in c.ax.patches]

    assert bar_colors[0] == cold_color
    assert bar_colors[1] == warm_color
    assert bar_colors[2] == neutral_color
    assert bar_colors[3] == cold_color


def test_type_property():
    container = {}
    ds = DictStorage(container)

    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2016-01-01", -4],
                ["2017-01-01", 4],
                ["2018-01-01", 1],
                ["2019-01-01", -1]
            ]
        ],
        "type": "bars",
    }
    # when type="bars"...
    c = SerialChart.init_from(chart_obj, storage=ds)
    c.render("test", "png")
    bars = c.ax.patches
    # ...4 bars should be rendered
    assert len(bars) == 4

    # while a type=line...
    chart_obj["type"] = "line"
    c = SerialChart.init_from(chart_obj, storage=ds)
    c.render("test", "png")
    # lines = c.ax.patches
    # ... should only render one element
    # assert(len(lines) == 1)


def test_stacked_bar_chart():
    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2016-01-01", 1],
                ["2017-01-01", 4],
                ["2018-01-01", None],
                ["2019-01-01", 2]
            ],
            [
                ["2016-01-01", 3],
                ["2017-01-01", 12],
                ["2018-01-01", 1],
                ["2019-01-01", None]
            ]
        ],
        "labels": ["the good", "the bad"],
        "type": "bars",
    }
    # when type="bars"...
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("stacked_bar_chart_basic", "png")
    bars = c.ax.patches
    assert len(bars) == 8

    # Should color with qualitative colors by default
    qualitative_colors = c._nwc_style["qualitative_colors"]
    bar_colors = [bar.get_facecolor() for bar in c.ax.patches]
    assert bar_colors[0] == qualitative_colors[0]
    assert bar_colors[-1] == qualitative_colors[1]

    # specify colors
    chart_obj["colors"] = ["red", "green"]
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("stacked_bar_chart_spec_colors", "png")
    bar_colors = [bar.get_facecolor() for bar in c.ax.patches]
    assert bar_colors[0] == (1.0, 0.0, 0.0, 1.0)  # red


def test_bar_chart_with_ymax():
    # all negative values with fixed ymax to 0
    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2016-01-01", -4],
                ["2017-01-01", -6],
                ["2018-01-01", -3],
                ["2019-01-01", -2]
            ]
        ],
        "title": "Stating at zero",
        "ymax": 0,
        "type": "bars",
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("bar_chart_with_ymax1", "png")
    assert c.ax.get_ylim()[1] == 0

    # when ymax < actual max value in data
    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2016-01-01", .94],
                ["2017-01-01", .96],
                ["2018-01-01", .93],
                ["2019-01-01", .99],
            ]
        ],
        "title": "Make sure I start at 100 %",
        "ymax": 1,
        "type": "line",
        "units": "percent",
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("serial_chart_with_ymax", "png")
    # max_value = max([x[1] for x in chart_obj["data"][0]])
    assert c.ax.get_ylim()[1] == 1.0


def test_serial_chart_with_axis_labels():
    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2016-01-01", 12],
                ["2017-01-01", 14],
                ["2018-01-01", 8],
                ["2019-01-01", 2]
            ]
        ],
        "title": "Make sure the ylabel fits",
        "xlabel": "Point in time",
        "ylabel": "Number of cats",
        "note": "Read this also",
        "caption": "Source: Truth",
        "type": "line",
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    # visually make sure quay and x labels are visible
    c.render("serial_chart_with_axis_labels", "png")


def test_chart_with_long_y_ticks():
    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2016-01-01", 4e6],
                ["2017-01-01", 6e6],
                ["2018-01-01", 3e6],
                ["2019-01-01", 2e6]
            ]
        ],
        "title": "Look how large numbers!",
        "type": "bars",
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    # visually make sure tick labels are visible
    c.render("serial_bar_chart_with_long_y_ticks", "png")


def test_chart_with_negative_values():
    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2016-01-01", 2],
                ["2017-01-01", 3],
                ["2018-01-01", -1],
                ["2019-01-01", -3]
            ]
        ],
        "ymin": 0,
        "title": "Look  at the negative values",
        "type": "bars",
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    # visually make sure tick labels are visible
    c.render("serial_bar_chart_with_negative_values", "png")


def test_weekly_chart():
    # all negative values with fixed ymax to 0
    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2020-06-22", 0.391],
                ["2020-06-29", 0.346],
                ["2020-07-06", 0.297],
                ["2020-07-13", 0.317],
                ["2020-07-20", 0.197],
                ["2020-07-27", 0.417],
            ]
        ],
        "type": "bars",
        "units": "percent",
        "interval": "weekly",
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("serial_chart_weekly", "png")


def test_multi_color_lines():
    colors = ["red", "green", "blue"]

    chart_obj = {
        "width": 800,
        "height": 600,
        "data": [
            [
                ["2017-01-01", -6],
                ["2018-01-01", -3],
                ["2019-01-01", -2]
            ], [
                ["2017-01-01", -3],
                ["2018-01-01", -1],
                ["2019-01-01", 4]
            ], [
                ["2017-01-01", 2],
                ["2018-01-01", 5],
                ["2019-01-01", -3]
            ]

        ],
        "labels": colors,
        "colors": colors,
        "ymax": 0,
        "type": "line",
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("serial_chart_multi_color", "png")
    for i, color in enumerate(colors):
        assert c.ax.get_lines()[i].get_color() == color


def test_value_labeling():
    chart_obj = {
        "width": 600,
        "height": 300,
        "data": [
            [
                ["2017-01-01", -.6],
                ["2018-01-01", .1],
                ["2019-01-01", .32]
            ],
            [
                ["2017-01-01", -.6],
                ["2018-01-01", -.1],
                ["2019-01-01", .4]
            ],
        ],
        "labels": ["Region A", "Region B"],
        "label_placement": "line",
        "value_labels": True,
        "decimals": 1,
        "units": "percent",
        "type": "line",
        # "highlight": "2019-01-01",
        "title": "Look at those value labels",
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("serial_chart_value_labeling", "png")


def test_line_labeling():
    chart_obj = {
        "width": 600,
        "height": 300,
        "data": [
            [
                ["2017-01-01", -6],
                ["2018-01-01", -3],
                ["2019-01-01", 3.2]
            ],
            [
                ["2017-01-01", -3],
                ["2018-01-01", -1],
                ["2019-01-01", 4]
            ],
        ],
        "labels": ["Region A", "Region B"],
        "label_placement": "line",
        "decimals": 1,
        "ymin": 0,
        "type": "line",
        "highlight": "2019-01-01",
        "title": "Look at those labels",
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("serial_chart_line_labeling", "png")

    # real world example
    chart_obj = {
        'data': [
            [
                ['2008-01-01', 0.048],
                ['2008-02-01', 0.048],
                ['2008-03-01', 0.046],
                ['2008-04-01', 0.042],
                ['2008-05-01', 0.041],
                ['2008-06-01', 0.042],
                ['2008-07-01', 0.045],
                ['2008-08-01', 0.045],
                ['2008-09-01', 0.047],
                ['2008-10-01', 0.048],
                ['2008-11-01', 0.052],
                ['2008-12-01', 0.058],
                ['2009-01-01', 0.062],
                ['2009-02-01', 0.065],
                ['2009-03-01', 0.066],
                ['2009-04-01', 0.066], ['2009-05-01', 0.066], ['2009-06-01', 0.069], ['2009-07-01', 0.07], ['2009-08-01', 0.072], ['2009-09-01', 0.072], ['2009-10-01', 0.073], ['2009-11-01', 0.078], ['2009-12-01', 0.085], ['2010-01-01', 0.089], ['2010-02-01', 0.09], ['2010-03-01', 0.088], ['2010-04-01', 0.085], ['2010-05-01', 0.081], ['2010-06-01', 0.083], ['2010-07-01', 0.084], ['2010-08-01', 0.082], ['2010-09-01', 0.08], ['2010-10-01', 0.081], ['2010-11-01', 0.082], ['2010-12-01', 0.086], ['2011-01-01', 0.088], ['2011-02-01', 0.086], ['2011-03-01', 0.082], ['2011-04-01', 0.077], ['2011-05-01', 0.075], ['2011-06-01', 0.077], ['2011-07-01', 0.08], ['2011-08-01', 0.079], ['2011-09-01', 0.078], ['2011-10-01', 0.081], ['2011-11-01', 0.081], ['2011-12-01', 0.085], ['2012-01-01', 0.085], ['2012-02-01', 0.084], ['2012-03-01', 0.082], ['2012-04-01', 0.079], ['2012-05-01', 0.077], ['2012-06-01', 0.081], ['2012-07-01', 0.08], ['2012-08-01', 0.079], ['2012-09-01', 0.079], ['2012-10-01', 0.081], ['2012-11-01', 0.081], ['2012-12-01', 0.084], ['2013-01-01', 0.082], ['2013-02-01', 0.08], ['2013-03-01', 0.077], ['2013-04-01', 0.072], ['2013-05-01', 0.069], ['2013-06-01', 0.071], ['2013-07-01', 0.073], ['2013-08-01', 0.074], ['2013-09-01', 0.074], ['2013-10-01', 0.075], ['2013-11-01', 0.076], ['2013-12-01', 0.08], ['2014-01-01', 0.081], ['2014-02-01', 0.08], ['2014-03-01', 0.074], ['2014-04-01', 0.069], ['2014-05-01', 0.067], ['2014-06-01', 0.07], ['2014-07-01', 0.07], ['2014-08-01', 0.071], ['2014-09-01', 0.072], ['2014-10-01', 0.073], ['2014-11-01', 0.075], ['2014-12-01', 0.079], ['2015-01-01', 0.079], ['2015-02-01', 0.078], ['2015-03-01', 0.074], ['2015-04-01', 0.069], ['2015-05-01', 0.068], ['2015-06-01', 0.068], ['2015-07-01', 0.068], ['2015-08-01', 0.069], ['2015-09-01', 0.07], ['2015-10-01', 0.07], ['2015-11-01', 0.071], ['2015-12-01', 0.074], ['2016-01-01', 0.077], ['2016-02-01', 0.074], ['2016-03-01', 0.067], ['2016-04-01', 0.065], ['2016-05-01', 0.062], ['2016-06-01', 0.06], ['2016-07-01', 0.062], ['2016-08-01', 0.062], ['2016-09-01', 0.064], ['2016-10-01', 0.065], ['2016-11-01', 0.066], ['2016-12-01', 0.07], ['2017-01-01', 0.07], ['2017-02-01', 0.069], ['2017-03-01', 0.065], ['2017-04-01', 0.061], ['2017-05-01', 0.059], ['2017-06-01', 0.06], ['2017-07-01', 0.061], ['2017-08-01', 0.06], ['2017-09-01', 0.062], ['2017-10-01', 0.062], ['2017-11-01', 0.064], ['2017-12-01', 0.068], ['2018-01-01', 0.067], ['2018-02-01', 0.067], ['2018-03-01', 0.063], ['2018-04-01', 0.059], ['2018-05-01', 0.056], ['2018-06-01', 0.055], ['2018-07-01', 0.056], ['2018-08-01', 0.057], ['2018-09-01', 0.057], ['2018-10-01', 0.056], ['2018-11-01', 0.057], ['2018-12-01', 0.059], ['2019-01-01', 0.059], ['2019-02-01', 0.058], ['2019-03-01', 0.056], ['2019-04-01', 0.054], ['2019-05-01', 0.052], ['2019-06-01', 0.052], ['2019-07-01', 0.053], ['2019-08-01', 0.054], ['2019-09-01', 0.054], ['2019-10-01', 0.055], ['2019-11-01', 0.057], ['2019-12-01', 0.06], ['2020-01-01', 0.063], ['2020-02-01', 0.062], ['2020-03-01', 0.063], ['2020-04-01', 0.066], ['2020-05-01', 0.069], ['2020-06-01', 0.072], ['2020-07-01', 0.073], ['2020-08-01', 0.071], ['2020-09-01', 0.069], ['2020-10-01', 0.066], ['2020-11-01', 0.066], ['2020-12-01', 0.069], ['2021-01-01', 0.07], ['2021-02-01', 0.068], ['2021-03-01', 0.065], ['2021-04-01', 0.061], ['2021-05-01', 0.059], ['2021-06-01', 0.058], ['2021-07-01', 0.059], ['2021-08-01', 0.057], ['2021-09-01', 0.057], ['2021-10-01', 0.055], ['2021-11-01', 0.095]
            ], [
                ['2008-01-01', 0.056],
                ['2008-02-01', 0.055],
                ['2008-03-01', 0.053],
                ['2008-04-01', 0.051],
                ['2008-05-01', 0.049], ['2008-06-01', 0.052], ['2008-07-01', 0.053], ['2008-08-01', 0.054], ['2008-09-01', 0.055], ['2008-10-01', 0.057], ['2008-11-01', 0.06], ['2008-12-01', 0.066], ['2009-01-01', 0.071], ['2009-02-01', 0.074], ['2009-03-01', 0.076], ['2009-04-01', 0.076], ['2009-05-01', 0.077], ['2009-06-01', 0.082], ['2009-07-01', 0.085], ['2009-08-01', 0.087], ['2009-09-01', 0.087], ['2009-10-01', 0.089], ['2009-11-01', 0.091], ['2009-12-01', 0.095], ['2010-01-01', 0.099], ['2010-02-01', 0.1], ['2010-03-01', 0.099], ['2010-04-01', 0.096], ['2010-05-01', 0.093], ['2010-06-01', 0.096], ['2010-07-01', 0.098], ['2010-08-01', 0.097], ['2010-09-01', 0.096], ['2010-10-01', 0.096], ['2010-11-01', 0.096], ['2010-12-01', 0.099], ['2011-01-01', 0.102], ['2011-02-01', 0.101], ['2011-03-01', 0.098], ['2011-04-01', 0.095], ['2011-05-01', 0.093], ['2011-06-01', 0.096], ['2011-07-01', 0.097], ['2011-08-01', 0.097], ['2011-09-01', 0.097], ['2011-10-01', 0.097], ['2011-11-01', 0.098], ['2011-12-01', 0.103], ['2012-01-01', 0.102], ['2012-02-01', 0.102], ['2012-03-01', 0.1], ['2012-04-01', 0.098], ['2012-05-01', 0.095], ['2012-06-01', 0.099], ['2012-07-01', 0.1], ['2012-08-01', 0.101], ['2012-09-01', 0.101], ['2012-10-01', 0.102], ['2012-11-01', 0.103], ['2012-12-01', 0.106], ['2013-01-01', 0.106], ['2013-02-01', 0.105], ['2013-03-01', 0.104], ['2013-04-01', 0.101], ['2013-05-01', 0.099], ['2013-06-01', 0.102], ['2013-07-01', 0.103], ['2013-08-01', 0.104], ['2013-09-01', 0.104], ['2013-10-01', 0.104], ['2013-11-01', 0.104], ['2013-12-01', 0.107], ['2014-01-01', 0.107], ['2014-02-01', 0.106], ['2014-03-01', 0.103], ['2014-04-01', 0.099], ['2014-05-01', 0.097], ['2014-06-01', 0.099], ['2014-07-01', 0.1], ['2014-08-01', 0.101], ['2014-09-01', 0.1], ['2014-10-01', 0.1], ['2014-11-01', 0.1], ['2014-12-01', 0.103], ['2015-01-01', 0.104], ['2015-02-01', 0.103], ['2015-03-01', 0.101], ['2015-04-01', 0.098], ['2015-05-01', 0.096], ['2015-06-01', 0.098], ['2015-07-01', 0.099], ['2015-08-01', 0.1], ['2015-09-01', 0.1], ['2015-10-01', 0.101], ['2015-11-01', 0.101], ['2015-12-01', 0.103], ['2016-01-01', 0.104], ['2016-02-01', 0.103], ['2016-03-01', 0.1], ['2016-04-01', 0.098], ['2016-05-01', 0.096], ['2016-06-01', 0.096], ['2016-07-01', 0.096], ['2016-08-01', 0.097], ['2016-09-01', 0.097], ['2016-10-01', 0.098], ['2016-11-01', 0.098], ['2016-12-01', 0.101], ['2017-01-01', 0.101], ['2017-02-01', 0.101], ['2017-03-01', 0.1], ['2017-04-01', 0.098], ['2017-05-01', 0.096], ['2017-06-01', 0.097], ['2017-07-01', 0.099], ['2017-08-01', 0.099], ['2017-09-01', 0.099], ['2017-10-01', 0.099], ['2017-11-01', 0.099], ['2017-12-01', 0.1], ['2018-01-01', 0.099], ['2018-02-01', 0.098], ['2018-03-01', 0.096], ['2018-04-01', 0.093], ['2018-05-01', 0.091], ['2018-06-01', 0.092], ['2018-07-01', 0.093], ['2018-08-01', 0.093], ['2018-09-01', 0.093], ['2018-10-01', 0.093], ['2018-11-01', 0.092], ['2018-12-01', 0.094], ['2019-01-01', 0.093], ['2019-02-01', 0.093], ['2019-03-01', 0.092], ['2019-04-01', 0.09], ['2019-05-01', 0.089], ['2019-06-01', 0.091], ['2019-07-01', 0.092], ['2019-08-01', 0.093], ['2019-09-01', 0.093], ['2019-10-01', 0.094], ['2019-11-01', 0.095], ['2019-12-01', 0.098], ['2020-01-01', 0.098], ['2020-02-01', 0.097], ['2020-03-01', 0.098], ['2020-04-01', 0.103], ['2020-05-01', 0.107], ['2020-06-01', 0.113], ['2020-07-01', 0.115], ['2020-08-01', 0.114], ['2020-09-01', 0.111], ['2020-10-01', 0.109], ['2020-11-01', 0.109], ['2020-12-01', 0.111], ['2021-01-01', 0.11], ['2021-02-01', 0.109], ['2021-03-01', 0.106], ['2021-04-01', 0.102], ['2021-05-01', 0.099], ['2021-06-01', 0.099], ['2021-07-01', 0.099], ['2021-08-01', 0.097], ['2021-09-01', 0.095], ['2021-10-01', 0.094], ['2021-11-01', 0.092]
            ]
        ],
        'labels': ['Ängelholm', 'Skåne län'],
        'type': 'line',
        'units': 'percent',
        'width': 900,
        'height': 474,
        'ymin': 0,
        'periodicity': 'monthly',
        'label_placement': 'line', 'highlight': '2021-11-01',
        'title': 'Lägre arbetslöshet i Ängelholm än i Skåne',
        'subtitle': 'Arbetssökande som andel av den registerbaserade arbetskraften månad för månad.'
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("serial_chart_line_labeling2", "png")


def test_inline_labeling():
    # real world example
    chart_obj = {
        'data': [
            [
                ['2008-01-01', 0.048],
                ['2008-02-01', 0.048],
                ['2008-03-01', 0.046],
                ['2008-04-01', 0.042],
                ['2008-05-01', 0.041],
                ['2008-06-01', 0.042],
                ['2008-07-01', 0.045],
                ['2008-08-01', 0.045],
                ['2008-09-01', 0.047],
                ['2008-10-01', 0.048],
                ['2008-11-01', 0.052],
                ['2008-12-01', 0.058],
                ['2009-01-01', 0.062], ['2009-02-01', 0.065], ['2009-03-01', 0.066], ['2009-04-01', 0.066], ['2009-05-01', 0.066], ['2009-06-01', 0.069], ['2009-07-01', 0.07], ['2009-08-01', 0.072], ['2009-09-01', 0.072], ['2009-10-01', 0.073], ['2009-11-01', 0.078], ['2009-12-01', 0.085], ['2010-01-01', 0.089], ['2010-02-01', 0.09], ['2010-03-01', 0.088], ['2010-04-01', 0.085], ['2010-05-01', 0.081], ['2010-06-01', 0.083], ['2010-07-01', 0.084], ['2010-08-01', 0.082], ['2010-09-01', 0.08], ['2010-10-01', 0.081], ['2010-11-01', 0.082], ['2010-12-01', 0.086], ['2011-01-01', 0.088], ['2011-02-01', 0.086], ['2011-03-01', 0.082], ['2011-04-01', 0.077], ['2011-05-01', 0.075], ['2011-06-01', 0.077], ['2011-07-01', 0.08], ['2011-08-01', 0.079], ['2011-09-01', 0.078], ['2011-10-01', 0.081], ['2011-11-01', 0.081], ['2011-12-01', 0.085], ['2012-01-01', 0.085], ['2012-02-01', 0.084], ['2012-03-01', 0.082], ['2012-04-01', 0.079], ['2012-05-01', 0.077], ['2012-06-01', 0.081], ['2012-07-01', 0.08], ['2012-08-01', 0.079], ['2012-09-01', 0.079], ['2012-10-01', 0.081], ['2012-11-01', 0.081], ['2012-12-01', 0.084], ['2013-01-01', 0.082], ['2013-02-01', 0.08], ['2013-03-01', 0.077], ['2013-04-01', 0.072], ['2013-05-01', 0.069], ['2013-06-01', 0.071], ['2013-07-01', 0.073], ['2013-08-01', 0.074], ['2013-09-01', 0.074], ['2013-10-01', 0.075], ['2013-11-01', 0.076], ['2013-12-01', 0.08], ['2014-01-01', 0.081], ['2014-02-01', 0.08], ['2014-03-01', 0.074], ['2014-04-01', 0.069], ['2014-05-01', 0.067], ['2014-06-01', 0.07], ['2014-07-01', 0.07], ['2014-08-01', 0.071], ['2014-09-01', 0.072], ['2014-10-01', 0.073], ['2014-11-01', 0.075], ['2014-12-01', 0.079], ['2015-01-01', 0.079], ['2015-02-01', 0.078], ['2015-03-01', 0.074], ['2015-04-01', 0.069], ['2015-05-01', 0.068], ['2015-06-01', 0.068], ['2015-07-01', 0.068], ['2015-08-01', 0.069], ['2015-09-01', 0.07], ['2015-10-01', 0.07], ['2015-11-01', 0.071], ['2015-12-01', 0.074], ['2016-01-01', 0.077], ['2016-02-01', 0.074], ['2016-03-01', 0.067], ['2016-04-01', 0.065], ['2016-05-01', 0.062], ['2016-06-01', 0.06], ['2016-07-01', 0.062], ['2016-08-01', 0.062], ['2016-09-01', 0.064], ['2016-10-01', 0.065], ['2016-11-01', 0.066], ['2016-12-01', 0.07], ['2017-01-01', 0.07], ['2017-02-01', 0.069], ['2017-03-01', 0.065], ['2017-04-01', 0.061], ['2017-05-01', 0.059], ['2017-06-01', 0.06], ['2017-07-01', 0.061], ['2017-08-01', 0.06], ['2017-09-01', 0.062], ['2017-10-01', 0.062], ['2017-11-01', 0.064], ['2017-12-01', 0.068], ['2018-01-01', 0.067], ['2018-02-01', 0.067], ['2018-03-01', 0.063], ['2018-04-01', 0.059], ['2018-05-01', 0.056], ['2018-06-01', 0.055], ['2018-07-01', 0.056], ['2018-08-01', 0.057], ['2018-09-01', 0.057], ['2018-10-01', 0.056], ['2018-11-01', 0.057], ['2018-12-01', 0.059], ['2019-01-01', 0.059], ['2019-02-01', 0.058], ['2019-03-01', 0.056], ['2019-04-01', 0.054], ['2019-05-01', 0.052], ['2019-06-01', 0.052], ['2019-07-01', 0.053], ['2019-08-01', 0.054], ['2019-09-01', 0.054], ['2019-10-01', 0.055], ['2019-11-01', 0.057], ['2019-12-01', 0.06], ['2020-01-01', 0.063], ['2020-02-01', 0.062], ['2020-03-01', 0.063], ['2020-04-01', 0.066], ['2020-05-01', 0.069], ['2020-06-01', 0.072], ['2020-07-01', 0.073], ['2020-08-01', 0.071], ['2020-09-01', 0.069], ['2020-10-01', 0.066], ['2020-11-01', 0.066], ['2020-12-01', 0.069], ['2021-01-01', 0.07], ['2021-02-01', 0.068], ['2021-03-01', 0.065], ['2021-04-01', 0.061], ['2021-05-01', 0.059], ['2021-06-01', 0.058], ['2021-07-01', 0.059], ['2021-08-01', 0.057], ['2021-09-01', None], ['2021-10-01', 0.055], ['2021-11-01', 0.055]
            ], [
                ['2008-01-01', 0.056],
                ['2008-02-01', 0.055],
                ['2008-03-01', 0.053],
                ['2008-04-01', 0.051],
                ['2008-05-01', 0.049],
                ['2008-06-01', 0.052],
                ['2008-07-01', 0.053],
                ['2008-08-01', 0.054],
                ['2008-09-01', 0.055],
                ['2008-10-01', 0.057],
                ['2008-11-01', 0.06],
                ['2008-12-01', 0.066],
                ['2009-01-01', 0.071],
                ['2009-02-01', 0.074],
                ['2009-03-01', 0.076],
                ['2009-04-01', 0.076],
                ['2009-05-01', 0.077],
                ['2009-06-01', 0.082],
                ['2009-07-01', 0.085],
                ['2009-08-01', 0.087],
                ['2009-09-01', 0.087],
                ['2009-10-01', 0.089],
                ['2009-11-01', 0.091],
                ['2009-12-01', 0.095],
                ['2010-01-01', 0.099],
                ['2010-02-01', 0.1],
                ['2010-03-01', 0.099],
                ['2010-04-01', 0.096],
                ['2010-05-01', 0.093],
                ['2010-06-01', 0.096],
                ['2010-07-01', 0.098],
                ['2010-08-01', 0.097],
                ['2010-09-01', 0.096],
                ['2010-10-01', 0.096],
                ['2010-11-01', 0.096],
                ['2010-12-01', 0.099],
                ['2011-01-01', 0.102],
                ['2011-02-01', 0.101],
                ['2011-03-01', 0.098],
                ['2011-04-01', 0.095],
                ['2011-05-01', 0.093],
                ['2011-06-01', 0.096],
                ['2011-07-01', 0.097],
                ['2011-08-01', 0.097],
                ['2011-09-01', 0.097],
                ['2011-10-01', 0.097],
                ['2011-11-01', 0.098],
                ['2011-12-01', 0.103],
                ['2012-01-01', 0.102], ['2012-02-01', 0.102], ['2012-03-01', 0.1], ['2012-04-01', 0.098], ['2012-05-01', 0.095], ['2012-06-01', 0.099], ['2012-07-01', 0.1], ['2012-08-01', 0.101], ['2012-09-01', 0.101], ['2012-10-01', 0.102], ['2012-11-01', 0.103], ['2012-12-01', 0.106], ['2013-01-01', 0.106], ['2013-02-01', 0.105], ['2013-03-01', 0.104], ['2013-04-01', 0.101], ['2013-05-01', 0.099], ['2013-06-01', 0.102], ['2013-07-01', 0.103], ['2013-08-01', 0.104], ['2013-09-01', 0.104], ['2013-10-01', 0.104], ['2013-11-01', 0.104], ['2013-12-01', 0.107], ['2014-01-01', 0.107], ['2014-02-01', 0.106], ['2014-03-01', 0.103], ['2014-04-01', 0.099], ['2014-05-01', 0.097], ['2014-06-01', 0.099], ['2014-07-01', 0.1], ['2014-08-01', 0.101], ['2014-09-01', 0.1], ['2014-10-01', 0.1], ['2014-11-01', 0.1], ['2014-12-01', 0.103], ['2015-01-01', 0.104], ['2015-02-01', 0.103], ['2015-03-01', 0.101], ['2015-04-01', 0.098], ['2015-05-01', 0.096], ['2015-06-01', 0.098], ['2015-07-01', 0.099], ['2015-08-01', 0.1], ['2015-09-01', 0.1], ['2015-10-01', 0.101], ['2015-11-01', 0.101], ['2015-12-01', 0.103], ['2016-01-01', 0.104], ['2016-02-01', 0.103], ['2016-03-01', 0.1], ['2016-04-01', 0.098], ['2016-05-01', 0.096], ['2016-06-01', 0.096], ['2016-07-01', 0.096], ['2016-08-01', 0.097], ['2016-09-01', 0.097], ['2016-10-01', 0.098], ['2016-11-01', 0.098], ['2016-12-01', 0.101], ['2017-01-01', 0.101], ['2017-02-01', 0.101], ['2017-03-01', 0.1], ['2017-04-01', 0.098], ['2017-05-01', 0.096], ['2017-06-01', 0.097], ['2017-07-01', 0.099], ['2017-08-01', 0.099], ['2017-09-01', 0.099], ['2017-10-01', 0.099], ['2017-11-01', 0.099], ['2017-12-01', 0.1], ['2018-01-01', 0.099], ['2018-02-01', 0.098], ['2018-03-01', 0.096], ['2018-04-01', 0.093], ['2018-05-01', 0.091], ['2018-06-01', 0.092], ['2018-07-01', 0.093], ['2018-08-01', 0.093], ['2018-09-01', 0.093], ['2018-10-01', 0.093], ['2018-11-01', 0.092], ['2018-12-01', 0.094], ['2019-01-01', 0.093], ['2019-02-01', 0.093], ['2019-03-01', 0.092], ['2019-04-01', 0.09], ['2019-05-01', 0.089], ['2019-06-01', 0.091], ['2019-07-01', 0.092], ['2019-08-01', 0.093], ['2019-09-01', 0.093], ['2019-10-01', 0.094], ['2019-11-01', 0.095], ['2019-12-01', 0.098], ['2020-01-01', 0.098], ['2020-02-01', 0.097], ['2020-03-01', 0.098], ['2020-04-01', 0.103], ['2020-05-01', 0.107], ['2020-06-01', 0.113], ['2020-07-01', 0.115], ['2020-08-01', 0.114], ['2020-09-01', 0.111], ['2020-10-01', 0.109], ['2020-11-01', 0.109], ['2020-12-01', 0.111], ['2021-01-01', 0.11], ['2021-02-01', 0.109], ['2021-03-01', 0.106], ['2021-04-01', 0.102], ['2021-05-01', 0.099], ['2021-06-01', 0.099], ['2021-07-01', 0.099], ['2021-08-01', 0.097], ['2021-09-01', 0.095], ['2021-10-01', 0.094], ['2021-11-01', 0.092],
            ]
        ],
        'labels': ['Ängelholm', 'Skåne län'],
        'type': 'line',
        'units': 'percent',
        'width': 900,
        'height': 474,
        'decimals': 1,
        'periodicity': 'monthly',
        'label_placement': 'inline',
        'highlight': '2021-11-01',
        'title': 'Lägre arbetslöshet i Ängelholm än i Skåne',
        'subtitle': 'Arbetssökande som andel av den registerbaserade arbetskraften månad för månad.'
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("serial_chart_inline_labeling", "png")


def test_serial_chart_with_highlighted_area():
    import json
    with open("test/data/elpriser.json") as f:
        series = json.load(f)
    data = series

    chart_obj = {
        'width': 960,
        'height': 600,
        'title': 'Rekordpris i bidding area SE1',
        'subtitle': 'Spotpris på el på Nordpool',
        'note': 'Källa: Nordpool',
        'data': data,
        'type': 'line',
        'line_width': 1,
        "ticks": [
            ("2021-09-07", "Samma dag\ni fjol"),
            ("2022-01-01", "2022"),
            ("2022-04-01", "Apr"),
            ("2022-07-01", "Jul"),
            ("2022-09-07", "I dag"),
        ],
        'highlighted_x_ranges': [
            ['2022-08-09', '2022-09-07'],
            ['2021-08-09', '2021-09-07'],
        ],
        'label_placement': 'line',
        'labels': ['Dagens högsta\ntimpris: 536 kr'],
        'ymin': 0
    }
    c = SerialChart.init_from(chart_obj, storage=local_storage)
    c.render("serial_chart_with_highlighted_area", "png")


def test_duplicated_timepoint():
    chart_obj = {
        'colors': ['#00a39a', '#DBAD58'],
        'data': [
            [
                ('2020', 1294),
                ('2021', 2038),
                ('2022', 2176),
                ('2022', 2178),  # <= duplicated!
            ]
        ],
        'height': 552.0,
        'type': 'bars',
        'width': 920,
    }
    with pytest.raises(ValueError):
        c = SerialChart.init_from(chart_obj, storage=local_storage)
        c.render("serial_barchart", "png")
