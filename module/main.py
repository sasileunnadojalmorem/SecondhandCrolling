
from selenium_crolling import start
from data_cleaning import cleaning
import matplotlib.pyplot as plt
import seaborn as sns

# 크롤링 모듈에서 start 함수의 리턴으로 데이터프레임을 가져옴
df = start()

# cleaning 함수 실행
df_cleaned = cleaning(df)

# 데이터프레임 저장하기
df_cleaned.to_csv('/Users/choewonjun/PycharmProjects/study/secondhand/crolling_result.csv', index=False, encoding='utf-8-sig')

# boxplot 그래프 출력하기
sns.boxplot(y='price', data=df)
plt.show()