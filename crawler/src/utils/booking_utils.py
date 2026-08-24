from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re


DEPARTURE_DATE_KEY = "querydeparturedate"
DEPARTURE_TIME_KEY = "querydeparture"
ARRIVAL_TIME_KEY = "queryarrival"
TRAIN_NO_KEY = "querycode"
ESTIMATED_TIME_KEY = "queryestimatedtime"


def parse_train_schedules(html: str) -> List[Dict]:
    """
    解析高鐵訂票網站返回的列車時刻表
    
    Args:
        html: 網頁HTML內容
        
    Returns:
        訂票列車資訊列表
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find(id="BookingS2Form_TrainQueryDataViewPanel")
        
        if not table:
            return []
        
        schedules = table.find('div', class_="result-listing")
        
        if not schedules:
            return []
        
        train_schedules = []
        for item in schedules.find_all('label', class_="result-item"):
            train_radio = item.find('input', class_='uk-radio')
            
            if not train_radio:
                continue
            
            early_bird_element = item.find('p', class_='type early-bird')
            early_bird = early_bird_element.get_text() if early_bird_element else ''
            
            dict_data = {
                DEPARTURE_DATE_KEY: train_radio.get(DEPARTURE_DATE_KEY),
                DEPARTURE_TIME_KEY: train_radio.get(DEPARTURE_TIME_KEY),
                ARRIVAL_TIME_KEY: train_radio.get(ARRIVAL_TIME_KEY),
                TRAIN_NO_KEY: train_radio.get(TRAIN_NO_KEY),
                ESTIMATED_TIME_KEY: train_radio.get(ESTIMATED_TIME_KEY),
                'EARLY_BIRD': early_bird
            }
            
            train_schedules.append(dict_data)
        
        return train_schedules
    except Exception as e:
        print(f"解析列車時刻表失敗: {str(e)}")
        return []


def find_best_train(schedules: List[Dict], target_time: str, is_early_bird: bool = False) -> Optional[Dict]:
    """
    從列車時刻表中選擇最佳車次
    
    Args:
        schedules: 訂票列車資訊列表
        target_time: 目標出發時間
        is_early_bird: 是否為早鳥票
        
    Returns:
        最佳車次資訊
    """
    if not schedules:
        return None
    
    if is_early_bird:
        # 優先選擇有早鳥票的車次
        early_bird_trains = [s for s in schedules if s.get('EARLY_BIRD')]
        if early_bird_trains:
            return _get_closest_time_train(early_bird_trains, target_time)
    else:
        # 選擇沒有早鳥票的車次
        no_early_bird_trains = [s for s in schedules if not s.get('EARLY_BIRD')]
        if no_early_bird_trains:
            return _get_closest_time_train(no_early_bird_trains, target_time)
    
    # 默認選擇最接近目標時間的車次
    return _get_closest_time_train(schedules, target_time)


def _get_closest_time_train(schedules: List[Dict], target_time: str) -> Optional[Dict]:
    """
    獲取最接近目標時間的列車
    
    Args:
        schedules: 訂票列車資訊列表
        target_time: 目標出發時間 (格式: HH:MM)
        
    Returns:
        最接近時間的車次資訊
    """
    try:
        target_minutes = _time_to_minutes(target_time)
        
        closest_train = None
        min_diff = float('inf')
        
        for train in schedules:
            train_time = train.get(DEPARTURE_TIME_KEY)
            if train_time:
                train_minutes = _time_to_minutes(train_time)
                diff = abs(train_minutes - target_minutes)
                
                if diff < min_diff:
                    min_diff = diff
                    closest_train = train
        
        return closest_train
    except Exception as e:
        print(f"選擇最接近時間的列車失敗: {str(e)}")
        return schedules[0] if schedules else None


def _time_to_minutes(time_str: str) -> int:
    """
    將時間字符串轉換為分鐘數
    
    Args:
        time_str: 時間字符串 (格式: HH:MM)
        
    Returns:
        分鐘數
    """
    parts = time_str.split(':')
    if len(parts) >= 2:
        hours = int(parts[0])
        minutes = int(parts[1])
        return hours * 60 + minutes
    return 0


def extract_pnr_code(html: str) -> Optional[str]:
    """
    從訂票成功頁面中提取訂單代號
    
    Args:
        html: 網頁HTML內容
        
    Returns:
        訂單代號
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        pnr_element = soup.find(class_="pnr-code")
        
        if pnr_element:
            span = pnr_element.find('span')
            if span:
                return span.get_text().strip()
    except Exception as e:
        print(f"提取訂單代號失敗: {str(e)}")
    
    return None
