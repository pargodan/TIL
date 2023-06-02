import geopandas as gpd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'

# GeoJSON 파일 불러오기
geojson_file = 'HangJeongDong_ver20230401.geojson'
geo_data = gpd.read_file(geojson_file)

# CSV 파일 불러오기
csv_file = "내가씀.csv"
csv_data = pd.read_csv(csv_file, encoding='euc-kr')

# 필요한 열 선택
csv_data = csv_data[['매장명', '경도', '위도', '행정동', '총인구', '30~59세 인구']]

# 행정동 주소를 기준으로 데이터 병합
merged_data = seoul_geo_data.merge(csv_data, left_on='adm_nm', right_on='행정동')

# 'sidonm' 열이 '서울특별시'인 데이터만 선택
seoul_geo_data = geo_data[geo_data['sidonm'] == '서울특별시']

# 구 단위로 데이터 그룹화
grouped_data = seoul_geo_data.dissolve(by='sggnm', aggfunc='sum')

# 서울시 경계 그리기
fig, ax = plt.subplots(figsize=(10, 10))

# 연하늘색으로 바탕색 설정
ax.set_facecolor('white')

# 구 단위 경계 그리기 (약한 연하늘색)
grouped_data.boundary.plot(ax=ax, color=None, edgecolor='#B3C7D9', linewidth=1.5)

# 매장 위치 표시 (빨간 점)
store_locations = {
    '담꾹 길음점': (37.6066, 127.02152),  # '담꾹 길음점'의 위치 데이터 (위도, 경도)
    'NBM 신정역점': (37.52497, 126.85483),  # 'NBM 신정역점'의 위치 데이터 (위도, 경도)
}


# 담꾹 길음점과 NBM 신정역점 표시 (빨간 점)
for store_name, location in store_locations.items():
    plt.plot(location[1], location[0], 'ro', markersize=5)  # 빨간 점으로 표시

# '내가씀.csv' 파일에서 매장명, 경도, 위도 데이터 불러오기
#data_file = '내가씀.csv'
#df = pd.read_csv(data_file)
#csv_data
# 나머지 매장 표시 (회색 점)
for i, row in csv_data.iterrows():
    store_name = row['매장명']
    latitude = row['경도']
    longitude = row['위도']
    if store_name not in store_locations:
        plt.plot(longitude, latitude, 'o', color='gray', markersize=5)  # 회색 점으로 표시

ax.set_title('서울시 매장', fontdict={'fontsize': '14', 'fontweight': 'bold'})

plt.show()