import unittest
from datetime import datetime, time, timedelta

class Sky:
    index_map = {}

    def __init__(self, idx, chinese, korean):
        self.idx = idx
        self.chinese = chinese
        self.korean = korean
        Sky.index_map[idx] = self

    def get_idx(self):
        return self.idx

    @staticmethod
    def from_chinese(chinese):
        for sky in Sky.index_map.values():
            if sky.chinese == chinese:
                return sky
        return None

    @staticmethod
    def from_korean(korean):
        for sky in Sky.index_map.values():
            if sky.korean == korean:
                return sky
        return None


class Ground:
    index_map = {}

    def __init__(self, idx, chinese, korean):
        self.idx = idx
        self.chinese = chinese
        self.korean = korean
        Ground.index_map[idx] = self

    def get_idx(self):
        return self.idx

    @staticmethod
    def from_chinese(chinese):
        for ground in Ground.index_map.values():
            if ground.chinese == chinese:
                return ground
        return None

    @staticmethod
    def from_korean(korean):
        for ground in Ground.index_map.values():
            if ground.korean == korean:
                return ground
        return None


# Initialize Sky and Ground objects (Example, you can extend this)
Sky(1, "甲", "갑")
Sky(2, "乙", "을")
Sky(3, "丙", "병")
Sky(4, "丁", "정")
Sky(5, "戊", "무")
Sky(6, "己", "기")
Sky(7, "庚", "경")
Sky(8, "辛", "신")
Sky(9, "壬", "임")
Sky(10, "癸", "계")

Ground(1, "子", "자")
Ground(2, "丑", "축")
Ground(3, "寅", "인")
Ground(4, "卯", "묘")
Ground(5, "辰", "진")
Ground(6, "巳", "사")
Ground(7, "午", "오")
Ground(8, "未", "미")
Ground(9, "申", "신")
Ground(10, "酉", "유")
Ground(11, "戌", "술")
Ground(12, "亥", "해")


def calculate_time_sky(day_sky, ground_time):
    day_sky_index = day_sky.get_idx()
    ground_time_index = ground_time.get_idx()

    dx = day_sky_index if day_sky_index <= 5 else day_sky_index - 5
    idx = ground_time_index + ((dx - 1) * 2)
    idx = idx - 10 if idx > 10 else idx

    return Sky.index_map.get(idx)


def find_ground(time_str):
    tim_div = time_str.split(":")
    input_time = time(int(tim_div[0]), int(tim_div[1]))

    ground_times = [
        ("23:30", "01:30", "자"),
        ("01:30", "03:30", "축"),
        ("03:30", "05:30", "인"),
        ("05:30", "07:30", "묘"),
        ("07:30", "09:30", "진"),
        ("09:30", "11:30", "사"),
        ("11:30", "13:30", "오"),
        ("13:30", "15:30", "미"),
        ("15:30", "17:30", "신"),
        ("17:30", "19:30", "유"),
        ("19:30", "21:30", "술"),
        ("21:30", "23:30", "해"),
    ]

    for start, end, ground in ground_times:
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()

        if start_time <= end_time:  # not over midnight
            if start_time <= input_time < end_time:
                return Ground.from_korean(ground)
        else:  # over midnight
            if input_time >= start_time or input_time < end_time:
                return Ground.from_korean(ground)

    return Ground.index_map[1]  # 기본적으로 자시


def get_heavenly_stem(year):
    heavenly_stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    return Sky.from_korean(heavenly_stems[(year - 4) % 10])


def get_earthly_branch(year):
    earthly_branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    return Ground.from_korean(earthly_branches[(year - 4) % 12])


def get_month_gan_zhi(year, month):
    heavenly_stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    earthly_branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    
    month_stem_base = {'갑': 2, '을': 4, '병': 6, '정': 8, '무': 0, '기': 2, '경': 4, '신': 6, '임': 8, '계': 0}
    year_stem = heavenly_stems[(year - 4) % 10]
    month_stem_index = (month_stem_base[year_stem] + month - 1) % 10
    month_stem = heavenly_stems[month_stem_index]
    month_branch = earthly_branches[(month + 1) % 12]
    return Sky.from_korean(month_stem), Ground.from_korean(month_branch)


def get_day_gan_zhi(base_date, target_date):
    heavenly_stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    earthly_branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    
    diff_days = (target_date - base_date).days
    day_stem = heavenly_stems[diff_days % 10]
    day_branch = earthly_branches[diff_days % 12]
    return Sky.from_korean(day_stem), Ground.from_korean(day_branch)


def get_hour_gan_zhi(day_gan, hour):
    heavenly_stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    hour_branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    hour_stem_base = {'갑': 0, '을': 2, '병': 4, '정': 6, '무': 8, '기': 0, '경': 2, '신': 4, '임': 6, '계': 8}
    hour_stem_index = (hour_stem_base[day_gan.korean] + hour // 2) % 10
    hour_stem = heavenly_stems[hour_stem_index]
    hour_branch = hour_branches[hour // 2]
    return Sky.from_korean(hour_stem), Ground.from_korean(hour_branch)


def calculate_bazi(birth_date, birth_time):
    birth_datetime = datetime.combine(birth_date, birth_time)
    
    year_sky = get_heavenly_stem(birth_date.year)
    year_ground = get_earthly_branch(birth_date.year)
    
    month_sky, month_ground = get_month_gan_zhi(birth_date.year, birth_date.month)
    
    base_date = datetime(1900, 1, 31)
    day_sky, day_ground = get_day_gan_zhi(base_date, birth_datetime)
    
    hour_sky, hour_ground = get_hour_gan_zhi(day_sky, birth_datetime.hour)
    
    return {
        "year_sky": year_sky.korean,
        "year_ground": year_ground.korean,
        "month_sky": month_sky.korean,
        "month_ground": month_ground.korean,
        "day_sky": day_sky.korean,
        "day_ground": day_ground.korean,
        "hour_sky": hour_sky.korean,
        "hour_ground": hour_ground.korean,
    }


# Example usage:
birth_date = datetime(1990, 5, 5)
birth_time = datetime.strptime("05:30", "%H:%M").time()
bazi = calculate_bazi(birth_date, birth_time)
print(bazi)

class TestCalculateBazi(unittest.TestCase):
    def test_calculate_bazi(self):
        birth_date = datetime(1990, 5, 5)
        birth_time = datetime.strptime("05:30", "%H:%M").time()
        bazi = calculate_bazi(birth_date, birth_time)
        self.assertEqual(bazi['year_sky'], '경')
        self.assertEqual(bazi['year_ground'], '오')
        self.assertEqual(bazi['month_sky'], '임')
        self.assertEqual(bazi['month_ground'], '오')
        self.assertEqual(bazi['day_sky'], '경')
        self.assertEqual(bazi['day_ground'], '인')
        self.assertEqual(bazi['hour_sky'], '무')
        self.assertEqual(bazi['hour_ground'], '인')

if __name__ == "__main__":
    unittest.main()
