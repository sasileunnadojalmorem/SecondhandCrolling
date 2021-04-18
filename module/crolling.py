import pandas as pd
from secoundhand_selenium import start
from define import today, thing

df = start()

# 중복된 데이터 삭제
df.drop_duplicates(['제목'], inplace=True)

# 가격이 비이상적인 데이터 삭제하기
# q1 = df['가격'].quantile(0.25)
# q3 = df['가격'].quantile(0.75)
# iqr = q3 - q1
# condition = (df['가격'] > q3 + 1.5 * iqr) | (df['가격'] < q1 - 1.5 * iqr)
# df.drop(df[condition].index, inplace=True)

# 제목에 '삽니다' 라는 말이 있으면 삭제
condition_buy = df['제목'].str.contains('삽니다')
df.drop(df[condition_buy].index, inplace=True)

# 가격이 낮은 순서대로 정렬하기
# df = df.sort_values('가격')

# 만들어진 df를 엑셀에 저장하기
writer = pd.ExcelWriter(f'중고나라 {today}{thing} 매물.xlsx')
df.to_excel(writer, f'{today}')
writer.save()

# pandas 소수 출력값을 소수 아래 0 자리까지 표시하도록 설정
pd.set_option('display.float_format', lambda x: '%.f' % x)

# 가격 칼럼에 대한 요약 출력
print(df['가격'].describe())