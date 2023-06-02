import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely import wkt

plt.rcParams['font.family'] = 'NanumGothic'

def 지점과동네_시각화(data_file, boundary_file, store_locations):
    # 데이터 불러오기
    data = pd.read_csv(data_file, encoding='euc-kr')

    # 경도와 위도 데이터를 포함하는 딕셔너리 생성
    store_locations = {
        '식사준비 고덕자이점': (37.55344, 127.16912),
        '담꾹 앙원역점': (37.60705, 127.10677),
        '담꾹 고덕점': (37.55925, 127.15304),
        '식사준비 화랑대역점': (37.62081, 127.08384),
        '더잇24 강남자곡점': (37.47457, 127.10411)
    }

    # 위도와 경도를 Point 객체로 변환하여 Geopandas DataFrame에 추가
    for store_name, (lat, lon) in store_locations.items():
        point = Point(lon, lat)
        data = data.append({'temp1': store_name, 'geometry': point.wkt}, ignore_index=True)

    # geometry 열의 POLYGON 문자열을 Shapely의 Polygon 객체로 변환
    data['geometry'] = data['geometry'].apply(lambda polygon_string: wkt.loads(polygon_string))

    # 변환된 데이터를 GeoDataFrame으로 변환
    gdf = gpd.GeoDataFrame(data, geometry='geometry')

    # 선택할 동네 목록
    target_dongs = ['인헌동', '보라매동']

    # 선택한 동네만 필터링
    filtered_data = gdf[gdf['temp1'].isin(target_dongs)]

    # 행정동 경계 데이터 불러오기 (GeoJSON 파일)
    seoul_boundary = gpd.read_file(boundary_file)

    # 서울특별시에 해당하는 데이터 선택
    seoul_boundary = seoul_boundary[seoul_boundary['sidonm'] == '서울특별시']

    # 동 단위로 데이터 그룹화
    grouped_data = filtered_data.groupby('temp1')

    # 서울시 경계와 선택한 동네 내부를 겹쳐서 그리기
    fig, ax = plt.subplots(figsize=(10, 10))
    seoul_boundary.plot(ax=ax, edgecolor='#000000', facecolor='none')
    for dong, group in grouped_data:
        group.plot(ax=ax, facecolor='#00FF00', edgecolor='#000000')

    # 매장 위치 표시
    store_data = gdf[gdf['temp1'].isin(store_locations.keys())]
    store_data.plot(ax=ax, color='red', marker='o', markersize=10)

    plt.title('선택한 동네와 매장 위치', fontdict={'fontsize': '14', 'fontweight': 'bold'})
    plt.show()


data_file = '필요한파일5.csv'
boundary_file = 'HangJeongDong_ver20230401.geojson'
store_locations = {
    '식사준비 고덕자이점': (37.55344, 127.16912),
    '담꾹 앙원역점': (37.60705, 127.10677),
    '담꾹 고덕점': (37.55925, 127.15304),
    '식사준비 화랑대역점': (37.62081, 127.08384),
    '더잇24 강남자곡점': (37.47457, 127.10411)
}

지점과동네_시각화(data_file, boundary_file, store_locations)