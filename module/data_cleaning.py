
def cleaning(dataframe):
    # 중복되는 게시글 삭제
    dataframe.drop_duplicates(['제목', '판매자'], inplace=True)

    # 제목에 '삽니다' 라는 말이 있으면 삭제
    condition_buy = dataframe['제목'].str.contains('삽니다')
    dataframe.drop(dataframe[condition_buy].index, inplace=True)

    # #price이 비이상적인 데이터 삭제하기
    # q1 = dataframe['price'].quantile(0.25)
    # q3 = dataframe['price'].quantile(0.75)
    # iqr = q3 - q1
    # condition = (dataframe['price'] > q3 + 1.5 * iqr) | (dataframe['price'] < q1 - 1.5 * iqr)
    # dataframe.drop(dataframe[condition].index, inplace=True)

    return dataframe