from pyecharts import *
from pyecharts.constants import DEFAULT_HOST
from flask import Flask, render_template
from datatoaster import *
import collections
import datetime
import time

data = collections.OrderedDict()


class Item:
    def __init__(self, api_version, date, time, username, action, version, os):
        self.api_version, self.date, self.time, self.username, self.action, self.version, self.os = api_version, date, time, username, action, version, os

    def __repr__(self):
        return repr(self.__dict__)


# import data
def import_data(file_name):
    all_data = []
    with open(file_name) as file:
        for line in file:
            parts = line.split(" ")
            if len(parts) == 3:  # old version: 2017-09-24 10:00:00 'xxxxxxxx'
                api_version = "1.0"
                date = parts[0]
                time = parts[1]
                username = parts[2].replace("'", "").replace("\n", "")
                action = "unknown"
                version = "1.0.x"
                os = "unknown"
            elif len(parts) == 4:  # updated api: 1.0 2017-09-24 10:00:00 'xxxxxxxx'
                api_version = parts[0]
                date = parts[1]
                time = parts[2]
                username = parts[3].replace("'", "").replace("\n", "")
                action = "unknown"
                version = "1.1_beta"
                os = "unknown"
            elif len(parts) == 7:  # latest api: 2.0 2017-09-24 18:01:49 xxxxxxxx pull_data 1.1 android
                api_version = parts[0]
                date = parts[1]
                time = parts[2]
                username = parts[3]
                version = parts[4]
                action = parts[5]
                os = parts[6].replace("\n", "")
            else:
                print("[Warning] Skipped a line: ", line)
                continue
            if action == "login(failed)":continue
            all_data.append(Item(api_version, date, time, username, action, version, os))
    return all_data


app = Flask(__name__)

Width, Height, Curve = 700, 500, 0.5

all_data = import_data("/var/www/html/api/usage.log.py")


def standardized(data):
    all_keys = set()
    for _, value in data.items():
        for k, _ in value.items():
            all_keys.add(k)
    for key, value in data.items():
        arr = []
        for k in all_keys:
            arr.append(value.get(k, 0))
        data[key] = arr
    return data, list(all_keys)


def get_peak(data):
    peak = 0
    peak_date = "n/a"
    for date, num in data.items():
        if num > peak:
            peak = num
            peak_date = date
    return peak, peak_date


line_chart_args = {"is_label_show": True, "is_datazoom_show": True, "line_curve": Curve, "is_smooth": True, "is_fill":True, "area_opacity":0.3}


@app.route("/dashboard/")
def index():
    time_start = time.time()

    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    yesterday_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

    unique_data = (datatoaster.DataSet(all_data)
                   .set_x(lambda i: i.username)
                   .set_y(lambda li: li[-1])
                   .get_result())
    unique_data_array = []
    for _, info in unique_data.items():
        unique_data_array.append(info)

    number_chart_data = (datatoaster.DataSet(all_data)
                         .set_x(lambda i: i.date)
                         .set_y(lambda li: len(set([i.username for i in li])))
                         .ordered_by(lambda i: i[0])
                         .get_result())
    number_chart = Line("User Numbers", width=Width, height=Height)
    number_chart.add("", list(number_chart_data.keys()), list(number_chart_data.values()), **line_chart_args)

    number_usage_chart_data = (datatoaster.DataSet(all_data)
                               .set_x(lambda i: i.date)
                               .set_y(lambda li: len(li))
                               .ordered_by(lambda i: i[0])
                               .get_result())
    number_usage_chart = Line("User Usage Numbers", width=Width, height=Height)
    number_usage_chart.add("", list(number_usage_chart_data.keys()), list(number_usage_chart_data.values()),
                           **line_chart_args)

    today_user, today_usage = number_chart_data.get(today_date, 0), number_usage_chart_data.get(today_date, 0)
    diff_user, diff_usage = today_user - number_chart_data.get(yesterday_date, 0), \
                            today_usage - number_usage_chart_data.get(yesterday_date, 0)

    nu_set = datatoaster.DataSet(all_data)
    number_usage_today_chart_data, nu_series = standardized(nu_set
                                                            .set_x(lambda i: i.time[:2]+":00")
                                                            .set_y(nu_set.NumberOfAppearance(lambda i: i.action))
                                                            .add_constraint(lambda i: i.date == today_date)
                                                            .ordered_by(lambda i: i[0])
                                                            .get_result())
    number_usage_today_chart = Line("User Usage\nNumbers (Today) By Requests", width=Width, height=Height)
    for i in range(0, len(next(iter(number_usage_today_chart_data.values())))):
        number_usage_today_chart.add(nu_series[i], list(number_usage_today_chart_data.keys()),
                                     [j[i] for j in list(number_usage_today_chart_data.values())], **line_chart_args,
                                     is_stack=True)

    user_peak, user_peak_date = get_peak(number_chart_data)
    usage_peak, usage_peak_date = get_peak(number_usage_chart_data)

    os_time_chart_data_set = datatoaster.DataSet(unique_data_array)
    os_time_chart_data_set_data, os_time_series = standardized(os_time_chart_data_set
                                                       .set_x(lambda i: i.date)
                                                       .set_y(os_time_chart_data_set.NumberOfAppearance(lambda i: i.os))
                                                       .ordered_by(lambda i: i[0])
                                                       .get_result())
    os_time_chart = Line("", width=Width, height=Height)
    for i in range(0, len(next(iter(os_time_chart_data_set_data.values())))):
        os_time_chart.add(os_time_series[i], list(os_time_chart_data_set_data.keys()),
                          [j[i] for j in list(os_time_chart_data_set_data.values())], **line_chart_args)

    os_chart_data_set = datatoaster.DataSet(unique_data_array)
    os_chart_data = (os_chart_data_set
                     .set_x(lambda i: i.os)
                     .set_y(os_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                     .add_constraint(lambda i: i.date == today_date)
                     .get_result())
    os_chart = Pie("Percentage of OS", width=Width, height=Height)
    os_chart.add("", list(os_chart_data.keys()), list(os_chart_data.values()), is_label_show=True)

    version_ios_chart_data_set = datatoaster.DataSet(unique_data_array)
    version_ios_chart_data = (version_ios_chart_data_set
                              .set_x(lambda i: i.version)
                              .set_y(version_ios_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                              .add_constraint(lambda i: i.date == today_date and i.os == "ios")
                              .get_result())
    version_ios_chart = Pie("Percentage of\nVersions (iOS)", width=Width, height=Height)
    version_ios_chart.add("", list(version_ios_chart_data.keys()), list(version_ios_chart_data.values()),
                          is_label_show=True)

    version_android_chart_data_set = datatoaster.DataSet(unique_data_array)
    version_android_chart_data = (version_android_chart_data_set
                                  .set_x(lambda i: i.version)
                                  .set_y(version_android_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                                  .add_constraint(lambda i: i.date == today_date and i.os == "android")
                                  .get_result())
    version_android_chart = Pie("Percentage of\nVersions (Android)", width=Width, height=Height)
    version_android_chart.add("", list(version_android_chart_data.keys()), list(version_android_chart_data.values()),
                              is_label_show=True)

    action_chart_data_set = datatoaster.DataSet(all_data)
    action_chart_data = (action_chart_data_set
                         .set_x(lambda i: i.action)
                         .set_y(action_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                         .add_constraint(lambda i: i.date == today_date)
                         .get_result())
    action_chart = Pie("Percentage of\nActions", width=Width, height=Height)
    action_chart.add("", list(action_chart_data.keys()), list(action_chart_data.values()), is_label_show=True)

    district_chart_data_set = datatoaster.DataSet(unique_data_array)
    district_chart_data = (district_chart_data_set
                           .set_x(lambda i: i.username[2:4] if i.username[:4] != "2017" else i.username[4:6])
                           .set_y(district_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                           .add_constraint(lambda i: i.username[:8].isdigit() and i.api_version!="1.0" and i.api_version!="unknown" and (i.username[0]=="1" or i.username[1]=="2") and len(i.username)>=8)
                           .get_result())
    district_chart = Pie("Percentage of\nDistrict Code", width=Width, height=Height)
    district_chart.add("", list(district_chart_data.keys()), list(district_chart_data.values()), is_label_show=True)

    grade_chart_data_set = datatoaster.DataSet(unique_data_array)
    grade_chart_data = (grade_chart_data_set
                        .set_x(lambda i: i.username[0:2] if i.username[:4] != "2017" else i.username[0:4])
                        .set_y(grade_chart_data_set.NumberOfAppearance(datatoaster.XValue))
                        .add_constraint(lambda i: i.username[:8].isdigit() and i.api_version!="1.0" and i.api_version!="unknown" and (i.username[0]=="1" or i.username[0]=="2") and len(i.username)>=8)
                        .get_result())
    grade_chart = Pie("Percentage of\nGrades", width=Width, height=Height)
    grade_chart.add("", list(grade_chart_data.keys()), list(grade_chart_data.values()), is_label_show=True)

    return render_template('index.html',
                           os_chart=os_chart.render_embed(),
                           number_chart=number_chart.render_embed(),
                           version_android_chart=version_android_chart.render_embed(),
                           version_ios_chart=version_ios_chart.render_embed(),
                           number_usage_chart=number_usage_chart.render_embed(),
                           number_today_chart=number_usage_today_chart.render_embed(),
                           action_chart=action_chart.render_embed(),
                           district_chart=district_chart.render_embed(),
                           grade_chart=grade_chart.render_embed(),
                           os_time_chart=os_time_chart.render_embed(),
                           user_peak=user_peak,
                           user_peak_date=user_peak_date,
                           usage_peak=usage_peak,
                           usage_peak_date=usage_peak_date,
                           time_used=round((time.time() - time_start) * 1000, 2),
                           total_users=len(set([i.username for i in all_data])),
                           total_requests=len(all_data),
                           today_user=today_user,
                           today_usage=today_usage,
                           diff_user=("+" if diff_user > 0 else "") + str(diff_user),
                           diff_usage=("+" if diff_user > 0 else "") + str(diff_usage),
                           host=DEFAULT_HOST,
                           script_list=os_chart.get_js_dependencies())


if __name__ == '__main__':
    app.run(host="0.0.0.0")
