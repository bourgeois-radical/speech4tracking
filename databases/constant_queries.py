# bp_hr_aff = blood_pressure_heart_rate_affect
CREATE_BP_HR_AFF_TABLE = """
CREATE TABLE IF NOT EXISTS bp_hr_aff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time DATATIME DEFAULT CURRENT_TIMESTAMP,
    sys NUMERIC(5, 2) NOT NULL,
    dia NUMERIC(5, 2) NOT NULL,
    hr NUMERIC(5, 2) NOT NULL,
    affect TEXT NOT NULL
);
"""
# CURRENT_TIMESTAMP = Coordinated Universal Time

# add a row to bp_hr_aff
INSERT_ROW_TO_BP_HR_AFF = """
INSERT INTO bp_hr_aff (sys, dia, hr, affect)
VALUES(?, ?, ?, ?);
"""

# check last row
CHECK_LAST_ROW = """
SELECT * FROM bp_hr_aff;
"""

# the sys, dia and hr values in these db were actually taken from my personal measurements done in the years 2022/2023
# sys_rates.append(int(randint(109, 121)))
# dia_rates.append(int(randint(56, 68)))
# h_rates.append(int(randint(50, 60)))
# all_affect.append('no_affect')

# sys_rates_coffee.append(int(randint(115, 132)))
# dia_rates_coffee.append(int(randint(62, 75)))
# h_rates_coffee.append(int(randint(56, 70)))
# all_affect_coffee.append('coffee')


CREATE_DEMO_BP_HR_AFF_DB = """
CREATE TABLE IF NOT EXISTS demo_bp_hr_aff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time DATATIME DEFAULT CURRENT_TIMESTAMP,
    sys NUMERIC(5, 2) NOT NULL,
    dia NUMERIC(5, 2) NOT NULL,
    hr NUMERIC(5, 2) NOT NULL,
    affect TEXT NOT NULL
);
"""

INITIALIZE_FAKE_MEASUREMENTS_IN_DEMO_BP_HR_AFF_TABLE = """
INSERT INTO demo_bp_hr_aff (sys, dia, hr, affect)
VALUES (111, 65, 51, 'no_affect'),
(113, 57, 57, 'no_affect'),
(121, 63, 57, 'no_affect'),
(119, 62, 53, 'no_affect'),
(110, 63, 50, 'no_affect'),
(115, 62, 59, 'no_affect'),
(121, 68, 50, 'no_affect'),
(120, 63, 54, 'no_affect'),
(120, 68, 53, 'no_affect'),
(118, 57, 55, 'no_affect'),
(109, 56, 50, 'no_affect'),
(119, 64, 50, 'no_affect'),
(115, 66, 53, 'no_affect'),
(115, 67, 50, 'no_affect'),
(117, 59, 57, 'no_affect'),
(116, 64, 53, 'no_affect'),
(114, 59, 60, 'no_affect'),
(112, 68, 57, 'no_affect'),
(113, 56, 56, 'no_affect'),
(117, 66, 51, 'no_affect'),
(111, 66, 54, 'no_affect'),
(110, 67, 55, 'no_affect'),
(120, 67, 58, 'no_affect'),
(115, 64, 60, 'no_affect'),
(112, 60, 54, 'no_affect'),
(118, 63, 58, 'no_affect'),
(115, 65, 50, 'no_affect'),
(116, 59, 56, 'no_affect'),
(115, 66, 52, 'no_affect'),
(114, 64, 60, 'no_affect'),
(120, 61, 51, 'no_affect'),
(116, 66, 58, 'no_affect'),
(110, 68, 52, 'no_affect'),
(117, 62, 55, 'no_affect'),
(116, 67, 50, 'no_affect'),
(116, 56, 54, 'no_affect'),
(120, 65, 59, 'no_affect'),
(118, 62, 60, 'no_affect'),
(111, 58, 58, 'no_affect'),
(112, 56, 53, 'no_affect'),
(131, 69, 59, 'coffee'),
(131, 72, 56, 'coffee'),
(127, 72, 65, 'coffee'),
(125, 72, 66, 'coffee'),
(128, 62, 67, 'coffee'),
(124, 64, 59, 'coffee'),
(116, 66, 57, 'coffee'),
(117, 66, 70, 'coffee'),
(124, 73, 58, 'coffee'),
(128, 71, 60, 'coffee'),
(119, 62, 64, 'coffee'),
(116, 71, 69, 'coffee'),
(121, 71, 63, 'coffee'),
(120, 75, 69, 'coffee'),
(131, 62, 62, 'coffee'),
(121, 67, 57, 'coffee'),
(121, 71, 66, 'coffee'),
(128, 71, 59, 'coffee'),
(130, 63, 66, 'coffee'),
(127, 66, 64, 'coffee'),
(130, 62, 61, 'coffee'),
(127, 66, 56, 'coffee'),
(120, 65, 69, 'coffee'),
(125, 74, 65, 'coffee'),
(119, 67, 62, 'coffee'),
(121, 66, 66, 'coffee'),
(118, 75, 62, 'coffee'),
(132, 67, 70, 'coffee'),
(132, 69, 68, 'coffee'),
(132, 65, 57, 'coffee'),
(116, 63, 58, 'coffee'),
(120, 64, 70, 'coffee'),
(132, 65, 60, 'coffee'),
(125, 71, 64, 'coffee'),
(123, 67, 61, 'coffee'),
(125, 63, 60, 'coffee'),
(122, 75, 65, 'coffee'),
(130, 64, 65, 'coffee'),
(132, 74, 57, 'coffee'),
(125, 62, 62, 'coffee');
"""
