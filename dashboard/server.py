from pyecharts import *
from pyecharts.constants import DEFAULT_HOST
from flask import Flask, render_template
from datatoaster import *
import collections
import datetime

data = collections.OrderedDict()


class Item:
    def __init__(self, api_version, date, username, action, version, os):
        self.api_version, self.date, self.username, self.action, self.version, self.os = api_version, date, username, action, version, os

    def __repr__(self):
        return repr(self.__dict__)


all_data = []

# import data
with open("/var/www/html/api/usage.log.py") as file:
    for line in file:
        parts = line.split(" ")
        if len(parts) == 3:  # old version: 2017-09-24 10:00:00 'xxxxxxxx'
            api_version = "1.0"
            date = parts[0]
            username = parts[2].replace("'", "").replace("\n", "")
            action = "unknown"
            version = "1.0.x"
            os = "unknown"
        elif len(parts) == 4:  # updated api: 1.0 2017-09-24 10:00:00 'xxxxxxxx'
            api_version = parts[0]
            date = parts[1]
            username = parts[3].replace("'", "").replace("\n", "")
            action = "unknown"
            version = "1.1_beta"
            os = "unknown"
        elif len(parts) == 7:  # latest api: 2.0 2017-09-24 18:01:49 xxxxxxxx pull_data 1.1 android
            api_version = parts[0]
            date = parts[1]
            username = parts[3]
            version = parts[4]
            action = parts[5]
            os = parts[6].replace("\n", "")
        else:
            print("[Warning] Skipped a line: ", line)
            continue
        all_data.append(Item(api_version, date, username, action, version, os))

app = Flask(__name__)

Width, Height = 700, 500


@app.route("/dashboard/")
def index():
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')

    unique_data_today = (datatoaster.DataSet(all_data)
                         .set_x(lambda i: i.username)
                         .set_y(lambda li: li[-1])
                         .add_constraint(lambda i: i.date == today_date)
                         .get_result())
    unique_data_today_array = []
    for username, info in unique_data_today:
        unique_data_today_array.append(Item(info['api_version'],info['date'],username,info['action'],info['version'],info['os']))

    number_chart_data = (datatoaster.DataSet(all_data)
                         .set_x(lambda i: i.date)
                         .set_y(lambda li: len(set([i.username for i in li])))
                         .ordered_by(lambda i: i[0])
                         .get_result())
    number_chart = Line("User Numbers", width=Width, height=Height)
    number_chart.add("", list(number_chart_data.keys()), list(number_chart_data.values()), is_label_show=True)

    number_usage_chart_data = (datatoaster.DataSet(all_data)
                               .set_x(lambda i: i.date)
                               .set_y(lambda li: len(li))
                               .ordered_by(lambda i: i[0])
                               .get_result())
    number_usage_chart = Line("User Usage Numbers", width=Width, height=Height)
    number_usage_chart.add("", list(number_usage_chart_data.keys()), list(number_usage_chart_data.values()),
                           is_label_show=True)

    os_chart_data_set = datatoaster.DataSet(all_data)
    os_chart_data = (os_chart_data_set
                     .set_x(lambda i: i.os)
                     .set_y(os_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                     .add_constraint(lambda i: i.date == today_date)
                     .get_result())
    os_chart = Pie("Percentage of OS", width=Width, height=Height)
    os_chart.add("", list(os_chart_data.keys()), list(os_chart_data.values()), is_label_show=True)

    version_ios_chart_data_set = datatoaster.DataSet(unique_data_today_array)
    version_ios_chart_data = (version_ios_chart_data_set
                              .set_x(lambda i: i.version)
                              .set_y(version_ios_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                              .add_constraint(lambda i: i.date == today_date and i.os == "ios")
                              .get_result())
    version_ios_chart = Pie("Percentage of Versions (iOS)", width=Width, height=Height)
    version_ios_chart.add("", list(version_ios_chart_data.keys()), list(version_ios_chart_data.values()),
                          is_label_show=True)

    version_android_chart_data_set = datatoaster.DataSet(unique_data_today_array)
    version_android_chart_data = (version_android_chart_data_set
                                  .set_x(lambda i: i.version)
                                  .set_y(version_android_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                                  .add_constraint(lambda i: i.date == today_date and i.os == "android")
                                  .get_result())
    version_android_chart = Pie("Percentage of Versions (Android)", width=Width, height=Height)
    version_android_chart.add("", list(version_android_chart_data.keys()), list(version_android_chart_data.values()),
                              is_label_show=True)

    action_chart_data_set = datatoaster.DataSet(unique_data_today_array)
    action_chart_data = (action_chart_data_set
                         .set_x(lambda i: i.action)
                         .set_y(action_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                         .add_constraint(lambda i: i.date == today_date)
                         .get_result())
    action_chart = Pie("Percentage of Versions (Android)", width=Width, height=Height)
    action_chart.add("", list(action_chart_data.keys()), list(action_chart_data.values()),
                     is_label_show=True)

    return render_template('index.html',
                           os_chart=os_chart.render_embed(),
                           number_chart=number_chart.render_embed(),
                           version_android_chart=version_android_chart.render_embed(),
                           version_ios_chart=version_ios_chart.render_embed(),
                           number_usage_chart=number_usage_chart.render_embed(),
                           action_chart=action_chart.render_embed(),
                           host=DEFAULT_HOST,
                           script_list=os_chart.get_js_dependencies())


if __name__ == '__main__':
    app.run(host="0.0.0.0")
