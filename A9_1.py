from datetime import datetime
import uuid
import re
import pandas as pd
import B9
import math

file = r"请更改为您的课表文件路径.xlsx"
if file == r"请更改为您的课表文件路径.xlsx":
    raise ValueError("请更改为您的课表文件路径.xlsx 为您的课表文件路径")


def turn_jieci_to_course_num(jieci):
    if jieci == 1:
        return [1, 2]
    elif jieci == 2:
        return [3, 4]
    elif jieci == 3:
        return [5, 6]
    elif jieci == 4:
        return [7, 8]
    elif jieci == 5:
        return [9, 11]


def turn_num_to_time(num):
    print(B9.TIME_LIST[num[0] - 1])
    begin = B9.TIME_LIST[num[0] - 1][0]
    end = B9.TIME_LIST[num[-1] - 1][1]
    return f'{begin}-{end}'


class single_course:
    def __init__(self, name, teacher_name, date, weekday_of_the_class, time_of_class, location, other):
        self.name = name
        self.teacher = teacher_name
        self.date = date
        self.weekday_of_the_class = weekday_of_the_class
        self.time_of_class = time_of_class
        self.location = location
        self.other = other

    def __str__(self):
        num = turn_jieci_to_course_num(self.time_of_class)
        CLASStime = turn_num_to_time(num)
        return f"课程: {self.name}, 教师{self.teacher}, 日期: {B9.get_date(self.date, self.time_of_class)}, 节次: {self.time_of_class},时间:{CLASStime} 地点: {self.location}, 其他: {self.other}"

    def turn_to_ics_format(self):
        num = turn_jieci_to_course_num(self.time_of_class)
        CLASStime = turn_num_to_time(num)
        x = (
            str(datetime.now())
            .replace(" ", "")
            .replace("-", "")
            .replace(":", "")
            .replace(".", "")[:-6]
        )
        matches = re.findall(r"\((.*?)\)", self.location)
        if matches:
            matches = matches[0]
        else:
            matches = ''
        return f"""BEGIN:VEVENT
UID:{str(uuid.uuid4())}
DTSTAMP:{x[:8]}T{x[8:]}
DTSTART:{str(B9.get_date(self.date, self.weekday_of_the_class)).replace('-', '')}T{CLASStime.split('-')[0].replace(':', '')}00
DTEND:{str(B9.get_date(self.date, self.weekday_of_the_class)).replace('-', '')}T{CLASStime.split('-')[1].replace(':', '')}00
SUMMARY:{self.name}
DESCRIPTION:{self.location}   {self.teacher}   {self.other}
LOCATION:{B9.detect_location(matches)}
END:VEVENT
"""


def get_course_time(row, col):
    time = row - 4
    day = {'B': 7, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6}[col]
    return time, day


def process_a_cell(value):
    if value is None:
        return []
    try:
        # 处理 float('nan') 的情况
        if isinstance(value, float) and math.isnan(value):
            return []
    except:
        pass

    value = str(value)
    if value.lower() == 'nan':  # 处理字符串 'nan'
        return []

    # 按换行切分并去掉空字符串
    results = [x for x in value.split('\n') if x.strip() != '']
    if len(results) <= 3:
        return [results]
    else:
        grouped = []
        for i in range(0, len(results), 3):
            grouped.append(results[i:i + 3])
        return grouped


df = pd.read_excel(file)
subset = df.iloc[2:7, 1:8]

course_list = []
single_course_list = []

for row_idx in range(subset.shape[0]):  # 遍历行
    for col_idx in range(subset.shape[1]):  # 遍历列
        value = subset.iat[row_idx, col_idx]  # 获取单元格内容
        t, d = get_course_time(row_idx + 4, chr(66 + col_idx))
        print(f"周{d}，第{t + 1}大节 : {process_a_cell(value)}")
        if process_a_cell(value):
            course_list.append([t, process_a_cell(value), d])
print(course_list)

for course_collection in course_list:
    t, course_collection, d = tuple(course_collection)
    if len(course_collection[0]) == 3:
        course_name, data, other = tuple(course_collection[0])
        result_split = data.split(';')
        teacher = result_split[0]
        week_data = B9.read_week(result_split[1].replace('周', ''))
        location = result_split[2] if len(result_split) > 2 else ''
        for week in week_data:
            single_course_list.append(single_course(course_name, teacher, week, d, t + 1, location, other))
    else:
        print('Its length is not 3:', course_collection)

for single_c in single_course_list:
    print(single_c)

with open('my_schedule.ics', 'w', encoding='utf-8') as f:
    f.write(
        """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
"""
    )
    for single_c in single_course_list:
        if not B9.is_holiday(B9.get_date(single_c.date, single_c.weekday_of_the_class)):
            f.write(single_c.turn_to_ics_format())
    f.write("END:VCALENDAR\n")
