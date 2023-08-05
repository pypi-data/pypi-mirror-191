from .chart import Chart
from .lib.locator import get_best_locator, get_year_ticks
from .lib.utils import to_float, to_date
from .lib.formatter import Formatter

import numpy as np
from math import inf
from matplotlib.dates import DateFormatter, num2date
from dateutil.relativedelta import relativedelta
from adjustText import adjust_text
from labellines import labelLines


class SerialChart(Chart):
    """Plot a timeseries, as a line or bar plot.

    Data should be a list of iterables of (value, date string) tuples, eg:
    `[ [("2010-01-01", 2), ("2010-02-01", 2.3)] ]`
    """
    _uses_categorical_data = False

    def __init__(self, *args, **kwargs):
        super(SerialChart, self).__init__(*args, **kwargs)
        self.type = "bars"
        self.bar_width = 0.9

        self.allow_broken_y_axis = kwargs.get("allow_broken_y_axis", True)
        # draw bars and cut ay axis from this line
        self.baseline = kwargs.get("baseline", 0)
        self.baseline_annotation = kwargs.get("baseline_annotation", None)

        self.color_labels = kwargs.get("color_labels", None)

        # Set with of lines explicitly (otherwise determined by style file)
        self.line_width = None

        # Percent of period. 0.85 means a bar in a chart with yearly data will
        # be around 310 or 311 days wide.
        self.max_ticks = 5

        # Manually set tick locations and labels? Provide a list of tuples:
        # [(2013-01-01, "-13"), (2014-01-01, "-14"), (2015-01-01, "-15")]
        self.ticks = None
        self._ymin = None
        self._ymax = None

        # Optional: specify a list of colors (one color for each dataset)
        self.colors = None

        # Optional: where to place series label
        self.label_placement = "legend"  # legend|inline|outside

        # Optional: annotate each point with a value label
        self.value_labels = False

        # Optional: Adds background color to part of charts
        self.highlighted_x_ranges = []

    @property
    def ymin(self):
        # WIP
        return self._ymin

    @ymin.setter
    def ymin(self, val):
        self._ymin = val

    @property
    def ymax(self):
        return self._ymax

    @ymax.setter
    def ymax(self, val):
        self._ymax = val

    def _days_in(self, interval, d=None):
        """Return number of days in a given period.

        If only interval is given, use a typical number of days.
        >>>> _days_in(monthly)
        30
        >>>> _days_in(monthly, datetime(2004, 02, 05))
        29
        """
        if d is None:
            return {
                'yearly': 365,
                'quarterly': 91,
                'monthly': 30,
                'weekly': 7,
                'daily': 1,
            }[interval]
        else:
            # https://stackoverflow.com/questions/4938429/how-do-we-determine-the-number-of-days-for-a-given-month-in-python

            if interval == "yearly":
                return (
                    (d + relativedelta(years=1)).replace(day=1, month=1) - d.replace(day=1, month=1)
                ).days
            elif interval == "quarterly":
                return (
                    (d + relativedelta(months=3)).replace(day=1) - d.replace(day=1)
                ).days
            elif interval == "monthly":
                return (
                    (d + relativedelta(months=1)).replace(day=1) - d.replace(day=1)
                ).days
            elif interval == "weekly":
                # Assuming ISO 8601 here
                return 7
            elif interval == "daily":
                return 1

    def _guess_interval(self):
        """Return a probable interval, e.g. "montly", given current data."""
        interval = "yearly"
        for serie in self.data:
            dates = [to_date(x[0]) for x in serie]
            dates_str = [x[0] for x in serie]
            years = [x.year for x in dates]
            months = [x.month for x in dates]
            yearmonths = [x.strftime("%Y-%m") for x in dates]
            weeks = [str(x.year) + str(x.isocalendar()[1]) for x in dates]
            if len(years) > len(set(years)):
                # there are years with more than one point
                unique_months = sorted(list(set(months)))
                if len(unique_months) == 4 \
                   and unique_months[0] + 3 == unique_months[1] \
                   and unique_months[1] + 3 == unique_months[2] \
                   and unique_months[2] + 3 == unique_months[3]:
                    # all in all four months, and they are non-conscutive
                    interval = "quarterly"
                else:
                    interval = "monthly"
                    if len(yearmonths) > len(set(yearmonths)):
                        interval = "weekly"
                    if len(weeks) > len(set(weeks)):
                        interval = "daily"
        return interval

    def _get_annotation_direction(self, index, values):
        """ Given an index and series of values, provide the estimated best
        direction for an annotation. This will be an educated guess, and the
        annotation is not guaranteed to be free from overlapping,
        """
        num_vals = len(values)
        if num_vals < 2:
            return "up"
        if index == 0:
            if values[0] < values[1]:
                return "down"
            else:
                return "up"
        if index == num_vals - 1:
            # get previous non-None value
            latest_not_null = [x for x in values[:-1] if x is not None][-1]
            if latest_not_null <= values[-1]:
                return "up"
            else:
                return "down"
        val = values[index]
        if val == max(values[index - 1:index + 2]):
            return "up"
        if val == min(values[index - 1:index + 2]):
            return "down"
        return "up"

    def _add_data(self):

        series = self.data

        # For backwards compatibility: Convert type = "line" -> type = ["line"]
        if type(self.type) == str:
            self.type = [self.type] * len(series)
        is_stacked = (len(series) > 1) and all([t == "bars" for t in self.type])

        # parse values
        serie_values = []
        for i, serie in enumerate(series):
            # make sure all timepoints are unique
            _timepoints = [x[0] for x in serie]
            if len(_timepoints) > len(set(_timepoints)):
                raise ValueError(f"Duplicated timepoints: {_timepoints}")
            _values = [to_float(x[1]) for x in serie]
            if self.type[i] == "bars":
                # Replace None values with 0's to be able to plot bars
                _values = [self.baseline if v is None else v for v in _values]
            serie_values.append(_values)

        #  Select a date to highlight
        highlight_date = None
        if self.highlight is not None:
            try:
                highlight_date = to_date(self.highlight)
            except ValueError:
                # in case we are highlighting something else (like a whole serie)
                highlight_date = None

        # Make an educated guess about the interval of the data
        if self.interval is None:
            self.interval = self._guess_interval()

        # Formatters for axis and annotations
        y_formatter = self._get_value_axis_formatter()
        a_formatter = self._get_annotation_formatter()

        # Number of days on x axis (Matplotlib will use days as unit here)
        xmin, xmax = to_date(self.data.x_points[0]), to_date(self.data.x_points[-1])
        delta = xmax - xmin

        # Store y values while we are looping the data, to adjust axis,
        # and highlight diff
        highlight_diff = {
            'y0': inf,
            'y1': -inf
        }
        highlight_values = []

        # For storing elements for later position adjustment
        line_label_elems = []
        value_label_elems = []

        for i, serie in enumerate(series):

            values = np.array(serie_values[i], dtype=float)
            dates = [to_date(x[0]) for x in serie]
            dates_str = [x[0] for x in serie]

            highlight_value = None
            if self.highlight:
                try:
                    highlight_value = values[dates.index(highlight_date)]
                    highlight_values.append(highlight_value)
                except ValueError:
                    # If this date is not in series, silently ignore
                    pass

            if self.highlight and (highlight_value is not None):
                highlight_diff['y0'] = min(highlight_diff['y0'],
                                           highlight_value)
                highlight_diff['y1'] = max(highlight_diff['y1'],
                                           highlight_value)
            if self.type[i] == "line":
                # Put first series on top
                zo = 2 + (i == 0)

                if self.line_width is None:
                    lw = self._nwc_style.get("lines.linewidth", 2)
                else:
                    lw = self.line_width

                if self.colors is not None:
                    color = self.colors[i]
                elif i == 0:
                    color = self._nwc_style["strong_color"]
                else:
                    color = self._nwc_style["neutral_color"]

                line, = self.ax.plot(dates, values,
                                     color=color,
                                     zorder=zo,
                                     lw=lw)
                # Add single, orphaned data points as markers
                # None, 1, None, 1, 1, 1 =>  . ---
                num_values = len(values)
                if num_values == 1:
                    self.ax.plot(dates[0], values[0],
                                 c=color,
                                 marker='.',
                                 zorder=2)
                elif num_values > 1:
                    for j, v in enumerate(values):
                        def nullish(val):
                            return val is None or np.isnan(val)
                        plot_me = False
                        if not nullish(v):
                            if j == 0 and nullish(values[1]):
                                plot_me = True
                            elif j == num_values - 1 and nullish(values[j - 1]):
                                plot_me = True
                            elif nullish(values[j - 1]) and nullish(values[j + 1]):
                                plot_me = True
                        if plot_me:
                            self.ax.plot(dates[j], v,
                                         c=color,
                                         marker='.',
                                         zorder=2)

                if len(self.labels) > i:
                    line.set_label(self.labels[i])

                if self.label_placement == "line":
                    # TODO: Offset should be dynamic
                    lbl = self._annotate_point(
                        self.labels[i],
                        (dates[-1], values[-1]),
                        "right",
                        offset=15,
                        color=color,
                        va="center"
                    )
                    # store labels to check for overlap later
                    line_label_elems.append(lbl)

                # add highlight marker
                if highlight_value:
                    self.ax.plot(highlight_date, highlight_value,
                                 c=color,
                                 marker='o',
                                 markersize=5,
                                 zorder=zo)

            elif self.type[i] == "bars":
                # Put first series on top, if mixed types
                zo = 2 + (i == 0)

                # Create colors
                colors = None
                if self.color_fn:
                    # Custom function has priority
                    # TODO: These functions probably want to know
                    # about stacking and highlighting, but we have
                    # no such usecase yet
                    colors = [
                        self._color_by(v, baseline=self.baseline) for v in values
                    ]
                elif self.colors:
                    colors = [self.colors[i]] * len(values)
                elif i == 0 and self.highlight:
                    base_color_for_series = self._nwc_style["neutral_color"]
                    hl_color_for_series = self._nwc_style["strong_color"]
                elif i == 0:
                    base_color_for_series = self._nwc_style["strong_color"]
                elif is_stacked:
                    hl_color_for_series = self._nwc_style["strong_color"]
                    base_color_for_series = self._nwc_style["qualitative_colors"][i]
                else:
                    """ i > 0 in mixed mode charts. Use secondary hl color """
                    base_color_for_series = self._nwc_style["neutral_color"]
                    hl_color_for_series = self._nwc_style["qualitative_colors"][i]

                if not colors:
                    print(self.highlight, dates_str)
                    if self.highlight in dates_str:
                        colors = []
                        for v in dates_str:
                            if v == self.highlight:
                                colors.append(hl_color_for_series)
                            else:
                                colors.append(base_color_for_series)
                    else:
                        colors = [base_color_for_series] * len(values)
                # Set bar width, based on interval
                """
                if self.interval == "monthly":
                    # Keep all months the same width, to make it look cleaner
                    bar_widths_ = [self._days_in(self.interval) for d in dates]
                else:
                    bar_widths_ = [self._days_in(self.interval, d) for d in dates]
                """
                bar_widths_ = [self._days_in(self.interval, d) for d in dates]

                # Put whitespace betw bars, unless there are a lot of bars
                bbox = self.ax.get_window_extent()
                if (sum(bar_widths_) * 2 / len(dates)) > bbox.width:
                    bar_widths = bar_widths_
                else:
                    bar_widths = [round(w * 0.85) for w in bar_widths_]

                bar_kwargs = dict(
                    color=colors,
                    width=bar_widths,
                    zorder=zo,
                )
                if len(dates) < 100:
                    # FIXME: This complements the bar_width hack above
                    # For some charts edges give better results (n_bars ~50?)
                    # This should be better tested, and implemented in a
                    # more robust way
                    bar_kwargs["edgecolor"] = "white"
                    bar_kwargs["linewidth"] = 1

                if is_stacked and i > 0:
                    if self.baseline != 0:
                        raise Exception("Setting a baseline is not supported for stacked bars")
                    # To make stacked bars we need to set bottom value
                    # aggregate values for stacked bar chart
                    cum_values = np.cumsum(serie_values, axis=0).tolist()
                    bar_kwargs["bottom"] = cum_values[i - 1]
                    # But only do this if both values have the same sign!
                    # We want to be able to have opposing (+/-) bars
                    for j, x in enumerate(values):
                        last_serie = serie_values[i - 1]
                        if np.sign(x) != np.sign(last_serie[j]):
                            # assert cum_values[i][j] == 0
                            bar_kwargs["bottom"][j] = 0
                else:
                    bar_kwargs["bottom"] = self.baseline

                bars = self.ax.bar(dates, values, **bar_kwargs)

                if len(self.labels) > i:
                    bars.set_label(self.labels[i])

            if self.value_labels:
                for date, value in zip(dates, values):
                    dir = "up"
                    value_label = a_formatter(value)
                    xy = (date, value)
                    elem = self._annotate_point(value_label, xy, direction=dir, color=color)
                    value_label_elems.append(elem)
            if self.color_labels:
                import matplotlib.patches as mpatches
                patches = []
                for color, label in self.color_labels.items():
                    # A bit of an hack:
                    # Check if this corresponds to one of our predefined
                    # color names:
                    if f"{color}_color" in self._nwc_style:
                        color = self._nwc_style[f"{color}_color"]
                    patch = mpatches.Patch(color=color, label=label)
                    patches.append(patch)
                self.ax.legend(handles=patches)

        # Annotate highlighted points/bars
        for hv in highlight_values:
            value_label = a_formatter(hv)
            xy = (highlight_date, hv)
            if self.type[i] == "bars":
                if hv >= self.baseline:
                    dir = "up"
                else:
                    dir = "down"
            if self.type[i] == "line":
                if len(highlight_values) > 1:
                    # When highlighting two values on the same point,
                    # put them in opposite direction
                    if hv == max(highlight_values):
                        dir = "up"
                    elif hv == min(highlight_values):
                        dir = "down"
                    else:
                        dir = "left"  # To the right we have diff annotation
                else:
                    # Otherwise, use what works best with the line shape
                    if highlight_date in dates:
                        i = dates.index(highlight_date)
                        dir = self._get_annotation_direction(i, values)
                    else:
                        # This highlight is probably out of range for this dataset
                        # Could happen if we have two or more lines,
                        # with different start and end points.
                        continue
            self._annotate_point(value_label, xy, direction=dir)

        # Add background highlights
        for (x0, x1) in self.highlighted_x_ranges:
            x0 = to_date(x0)
            x1 = to_date(x1)
            self.ax.axvspan(x0, x1, alpha=.4, color="lightgrey", lw=0)

        # Accentuate y=0 || y=baseline
        if (self.data.min_val < self.baseline) or self.baseline_annotation:
            self.ax.axhline(
                y=self.baseline,
                linewidth=1,
                color="#444444",
                zorder=3,
                linestyle="--" if self.baseline else "-"
            )
            if self.baseline_annotation:
                xy = (to_date(self.data.outer_min_x), self.baseline)
                # We only allow baseline to be set for single series bar charts
                first_val = self.data.values[0][0]
                self._annotate_point(
                    self.baseline_annotation,
                    xy,
                    direction="down" if first_val >= self.baseline else "up",
                    color=self._nwc_style["neutral_color"],
                )

        # Shade area between lines if there are exactly 2 series
        # and both are lines
        # For more series, the chart will get messy with shading
        if len(series) == 2 and self.type[0] == "line" and self.type[0] == "bars":
            # Fill any gaps in series
            filled_values = self.data.filled_values
            min_x = self.data.inner_min_x
            max_x = self.data.inner_max_x
            self.ax.fill_between([to_date(x) for x in self.data.x_points],
                                 filled_values[0],  # already a float1w
                                 filled_values[1],
                                 where=[(x >= min_x and x <= max_x)
                                        for x in self.data.x_points],
                                 facecolor=self._nwc_style["fill_between_color"],
                                 alpha=self._nwc_style["fill_between_alpha"])

        # Y axis formatting
        padding_bottom = 0
        if self.ymin is not None:
            # Override ymin if the smallest value is smaller than the suggested ymin
            # For example bar charts with negative values wants a forced ymin=0 if
            # all values are positive, but also show negatives
            ymin = min(self.ymin, self.data.min_val)
            padding_bottom = abs(ymin * 0.15)
        elif self.data.min_val > 0 and self.allow_broken_y_axis:
            # Boken y axis?
            if (self.data.max_val - self.data.min_val) < self.data.min_val:
                # Only break y axis if data variation is less than distance from ymin to 0
                ymin = self.data.min_val
                padding_bottom = abs(self.data.min_val * 0.15)
            else:
                ymin = self.baseline
                padding_bottom = abs(self.baseline * 0.15)
        elif self.data.min_val < 0:
            ymin = self.baseline + self.data.min_val
            padding_bottom = abs(-ymin * 0.15)
        else:
            ymin = self.baseline
            padding_bottom = abs(self.baseline * 0.15)

        if self.ymax is not None:
            ymax = self.ymax
            padding_top = 0
        else:
            if is_stacked:
                ymax = self.data.stacked_max_val
            else:
                ymax = self.data.max_val + self.baseline

            padding_top = ymax * 0.15

        self.ax.set_ylim(ymin=ymin - padding_bottom,
                         ymax=ymax + padding_top)

        self.ax.yaxis.set_major_formatter(y_formatter)
        self.ax.yaxis.grid(True)

        if ymin > self.baseline and self.allow_broken_y_axis:
            self._mark_broken_axis()

        # X ticks and formatter
        if self.ticks:
            self.ax.set_xticks([x[0] for x in self.ticks])
            self.ax.set_xticklabels([x[1] for x in self.ticks])

        elif delta.days > 500:
            ticks = get_year_ticks(xmin, xmax, max_ticks=self.max_ticks)
            self.ax.set_xticks(ticks)
            self.ax.xaxis.set_major_formatter(DateFormatter('%Y'))

        else:
            loc = get_best_locator(delta, len(dates), self.interval)
            self.ax.xaxis.set_major_locator(loc)
            formatter = Formatter(self._language)

            # if isinstance(loc, WeekdayLocator):
            if self.interval == "weekly":
                # We consider dates to be more informative than week numbers
                def fmt(x, pos):
                    if pos > len(self.data.x_points):
                        return None
                    try:
                        return formatter.date(self.data.x_points[pos], "d MMM")
                    except IndexError:
                        return None
                # fmt = DateFormatter('%-d %b')
            # elif isinstance(loc, MonthLocator):
            elif self.interval in ["monthly", "quarterly"]:
                def fmt(x, pos):
                    d = num2date(x).isoformat()[:10]
                    if d not in self.data.x_points:
                        return None
                    if pos > len(self.data.x_points):
                        return None
                    if len(self.data.x_points) > 12 and d[5:7] == "01":
                        return formatter.date(d, "MMM\ny")
                    else:
                        return formatter.date(d, "MMM")
                # fmt = DateFormatter('%b')

            # elif isinstance(loc, DayLocator):
            elif self.interval == "daily":
                def fmt(x, pos):
                    if pos > len(self.data.x_points):
                        return None
                    try:
                        if len(self.data.x_points) > 7:
                            return formatter.date(self.data.x_points[pos], "d MMM")
                        elif pos == 0:
                            return formatter.date(self.data.x_points[pos], "EE d/M")
                        else:
                            return formatter.date(self.data.x_points[pos], "EEE")
                    except IndexError:
                        return None
                # fmt = DateFormatter('%-d %b')
            else:
                NotImplementedError("Unable to determine tick formatter")

            self.ax.xaxis.set_major_formatter(fmt)

        # Add labels in legend if there are multiple series, otherwise
        # title is assumed to self-explanatory
        if len(self.labels) > 1:
            if self.label_placement == "legend":
                self.ax.legend(loc="best")
            elif self.label_placement == "outside":
                self.ax.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower right")
            elif self.label_placement == "inline":
                labelLines(self.ax.get_lines(), align=False, zorder=3, outline_width=4, fontweight="bold")

        # Trend/change line
        # Will use first serie
        if self.trendline:
            # Check if we have a list of single (x-) values, or data points
            if all(len(x) == 2 for x in self.trendline):
                # data points
                dates = [to_date(x[0]) for x in self.trendline]
                values = [to_float(x[1]) for x in self.trendline]
                marker = "_"
            else:
                # timepoints, get values from first series
                dates = [to_date(x) for x in self.trendline]
                alldates = [to_date(x[0]) for x in self.data[0]]
                values = [self.data[0][alldates.index(d)][1] for d in dates]
                marker = 'o'

            self.ax.plot(dates, values,
                         color=self._nwc_style["strong_color"], zorder=4,
                         marker=marker, linestyle='dashed')

            # Annotate points in trendline
            if self.annotate_trend:
                for i, date in enumerate(dates):
                    xy = (date, values[i])
                    dir = self._get_annotation_direction(i, values)
                    self._annotate_point(a_formatter(values[i]), xy,
                                         color=self._nwc_style["strong_color"],
                                         direction=dir)

            # x = [a.xy[0] for a in self._annotations]
            # y = [a.xy[1] for a in self._annotations]
            # adjust_text(self._annotations,
            #             x=x, y=y)

        if len(line_label_elems) > 1:
            self._adust_texts_vertically(line_label_elems)

        if len(value_label_elems) > 1:
            self._adust_texts_vertically(value_label_elems, ha="center")

    def _adust_texts_vertically(self, elements, ha="left"):
        if len(elements) == 2:
            # Hack: check for overlap and adjust labels only
            # if such overlap exist.
            # `adjust_text` tended to offset labels unnecessarily
            # but it might just be that I haven't worked out how to use it properly
            from adjustText import get_bboxes
            bb1, bb2 = get_bboxes(elements, self._fig.canvas.renderer, (1.0, 1.0), self.ax)
            print(bb1.y0, bb2.y0)
            if (
                # first label is above
                (bb1.y0 < bb2.y0) and (bb1.y1 > bb2.y0)
                # first label is below
                or (bb1.y0 > bb2.y0) and (bb1.y0 < bb2.y1)
            ):
                adjust_text(elements, autoalign="y", ha=ha)

        else:
            adjust_text(elements, autoalign="y", ha=ha)
