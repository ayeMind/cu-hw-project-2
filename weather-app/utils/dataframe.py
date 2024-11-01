from pandas import DataFrame

def create_dataframe(weather_cities: list) -> DataFrame:
    """
    Возвращает Pandas датафрейм с данными о погоде
    """
    if len(weather_cities) == 0:
        return DataFrame({
            "date": [],
            "city": [],
            "temperature": [],
            "humidity": [],
            "precipitation": [],
            "wind_speed": [],
            "cloud_cover": [],
            "result": []
        })
        
    all_data = []
    for city_data in weather_cities:
        all_data.extend(city_data)
            
    result_df = DataFrame(all_data)
    return result_df
