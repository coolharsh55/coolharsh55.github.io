"""common scaled ratings for harshp_com"""

from collections import namedtuple

Rating_5to1 = namedtuple('Rating_5to1', 'score label')
# scale 5 to 1
# 5 is highest, 1 is lowest
scale_5to1 = (
    Rating_5to1(5, 'SCORE-5'), Rating_5to1(4, 'SCORE-4'),
    Rating_5to1(3, 'SCORE-3'), Rating_5to1(2, 'SCORE-2'),
    Rating_5to1(1, 'SCORE-1'), Rating_5to1(0, 'NONE'))

scale_5to1_lowest = scale_5to1[-1]
scale_5to1_highest = scale_5to1[0]
