
def cleaning_duplicates(dataframe):
    # 중복되는 게시글 삭제
    dataframe.drop_duplicates(['제목', '판매자'], inplace=True)

    # 제목에 '삽니다' 라는 말이 있으면 삭제
    condition_buy = dataframe['제목'].str.contains('삽니다')
    dataframe.drop(dataframe[condition_buy].index, inplace=True)

    return dataframe

def cleaning_Outlier(dataframe):

    q1 = dataframe['price'].quantile(0.25)
    q3 = dataframe['price'].quantile(0.75)
    iqr = q3 - q1
    condition = (dataframe['price'] > q3 + 1.5 * iqr) | (dataframe['price'] < q1 - 1.5 * iqr)
    dataframe.drop(dataframe[condition].index, inplace=True)

    return dataframe


def no_price_data(dataframe):
    price_int_list = []
    df_app = dataframe[dataframe['제목'].str.startswith('[')].copy()

    title_spl_list = df_app['제목'].str.split('[')

    for i in title_spl_list:
        p = i[-1]  # 가격이 포함된 문자열
        p_str = p[:-2]  # 가격만 추출
        price_int_list.append(int(p_str.replace(',', '')))  # 가격을 숫자로 바꿈

    df_app['price'] = price_int_list

    return df_app