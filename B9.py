from datetime import date, timedelta
import holidays

FIRST_DAY = date(2024, 9, 9)
TIME_LIST = [['08:00', '08:45'], ['08:55', '09:40'], ['10:00', '10:45'],
             ['10:55', '11:40'], ['14:30', '15:15'], ['15:15', '16:00'],
             ['16:10', '16:55'], ['16:55', '17:40'], ['19:00', '19:45'],
             ['19:55', '20:40'], ['20:50', '21:35']]
LOCATION_LIST = {'综': '湖南大学综合教学楼', '研': '湖南大学研究生院楼',
                 '复': '复临舍教学楼', '中': '湖南大学教学中楼', '北': '湖南大学北楼教学楼',
                 '东': '湖南大学东楼教学楼', '水': '水上教学楼', '梯': '湖南大学阶梯教学楼',
                 '二': '湖南大学第二教学楼', '电': '湖南大学电子教学楼'}
DAY_SHIFT = {}


def get_date(week, day):
    global FIRST_DAY
    return FIRST_DAY + timedelta(days=7 * (week - 1) + day - 1)


def get_time(c_time):
    global TIME_LIST
    time_collect = []
    for i in range(len(c_time) // 2):
        temp = c_time[2 * i] + c_time[2 * i + 1]
        time_collect.append(TIME_LIST[int(temp) - 1])
    return [time_collect[0][0], time_collect[-1][-1]]


def read_week(s: str):
    t = s.split(',')
    result = []
    for x in t:
        if '-' in x:
            starr, end = tuple([int(c) for c in x.split('-')])
            for j in range(starr, end + 1):
                result.append(j)
        else:
            result.append(int(x))
    return result


def main(s: str):
    f1, f2 = tuple(s.split('('))
    d = f1[0]
    f1 = f1[1:]
    f2 = f2[:-2]
    t = get_time(f1)
    wk = read_week(f2)
    c = [get_date(w, int(d)) for w in wk if not is_holiday(get_date(w, int(d)))]
    return c, t


error_count = 0


def detect_location(s: str):
    global LOCATION_LIST, error_count
    try:
        return LOCATION_LIST[s[0]] + ' ' + s[1:]
    except (KeyError, IndexError):
        error_count += 1
        return s


def pure_name(s: str):
    if '(' in s:
        s = s.split('(')
        if s[0][-1] == '*':
            return s[0][:-1], s[1][:-1]
        return s[0], s[1][:-1]
    if s[-1] == '*':
        return s[:-1], ''
    return s, ''


cn_holidays = holidays.China()


def is_holiday(date_):
    """
    判断某个日期是否是中国大陆的节假日
    :param date_: datetime.date 对象或字符串（格式为 YYYY-MM-DD）
    :return: 如果是节假日，返回 True；否则返回 False
    """
    if isinstance(date_, str):
        from datetime import datetime
        date_ = datetime.strptime(date_, "%Y-%m-%d").date()

    return date_ in cn_holidays


if __name__ == '__main__':
    print(read_week('1-4,7-18'))
    print(read_week('12-18'))
    print(is_holiday('2025-1-4'))
