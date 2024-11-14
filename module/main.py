import pandas as pd
from t_selenium_crolling import start
from data_cleaning import cleaning_duplicates, cleaning_Outlier
import matplotlib.pyplot as plt
import seaborn as sns
from define import thing, save_path

def op():
    # 크롤링 모듈에서 start 함수의 리턴으로 데이터프레임을 가져옴
    df, df_yet = start()

    # price 칼럼을 object에서 int로 바꾸기
    df['price'] = df['price'].apply(pd.to_numeric)

    # 중복값 삭제하기
    df_no_duplicate = cleaning_duplicates(df)

    # 이상점 삭제하기

    df_no_outer = cleaning_Outlier(df_no_duplicate)
    df_final = pd.concat([df_no_outer])

    
    # 가격정보 없던 게시글에 가격 정보 추가하기

    # 두 데이터 프레임 합치기

    # 데이터프레임 저장하기
    df_final.to_csv(f'{save_path}/{thing}.csv', index=False, encoding='utf-8-sig')

    # boxplot 그래프 출력하기로
    sns.boxplot(y='price', data=df_no_outer)
    plt.show()

if __name__ == '__main__':
    op()