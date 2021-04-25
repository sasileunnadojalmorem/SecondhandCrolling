import pandas as pd
from t_selenium_crolling import start
from data_cleaning import cleaning_duplicates, cleaning_Outlier
import matplotlib.pyplot as plt
import seaborn as sns

# 크롤링 모듈에서 start 함수의 리턴으로 데이터프레임을 가져옴
df, df_yet = start()

# price 칼럼을 object에서 int로 바꾸기
df['price'] = df['price'].apply(pd.to_numeric)

# cleaning_duplicates 함수 실행
df_no_duplicate = cleaning_duplicates(df)

# cleaning_Outlier 함수 실행
df_no_outer = cleaning_Outlier(df)

# 데이터프레임 저장하기
df_no_duplicate.to_csv('/Users/choewonjun/PycharmProjects/study/secondhand/df_result.csv', index=False, encoding='utf-8-sig')
df_yet.to_csv('/Users/choewonjun/PycharmProjects/study/secondhand/df_yet_result.csv', index=False, encoding='utf-8-sig')


# boxplot 그래프 출력하기로
sns.boxplot(y='price', data=df_no_outer)
plt.show()