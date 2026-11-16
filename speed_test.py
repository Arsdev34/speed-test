import time
import sys
import json
import requests

def measure_speed(url, num_requests=10):
    print(f"Замер скорости для: {url}")
    print(f"Количество запросов: {num_requests}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    total_time = 0.0
    total_bytes = 0
    results = []
    
    for i in range(1, num_requests + 1):
        try:
            start_time = time.time()
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            end_time = time.time()
            
            request_time = end_time - start_time
            data_size = len(response.content)
            
            total_time += request_time
            total_bytes += data_size
            
            results.append({
                "request": i,
                "time_sec": round(request_time, 3),
                "size_kb": round(data_size / 1024, 2)
            })
            
            print(f"Запрос {i}: {request_time:.3f} сек, {data_size / 1024:.2f} KB")
            
        except Exception as e:
            print(f"\nОшибка в запросе {i}: {e}")
            sys.exit(1)
            
    avg_time = total_time / num_requests
    avg_speed_kbps = (total_bytes / 1024) / avg_time
    avg_speed_mbps = (total_bytes * 8) / (avg_time * 1_000_000)
    
    # Формируем итоговый отчет
    report = {
        "url": url,
        "num_requests": num_requests,
        "avg_time_sec": round(avg_time, 3),
        "total_data_kb": round(total_bytes / 1024, 2),
        "avg_speed_kbps": round(avg_speed_kbps, 2),
        "avg_speed_mbps": round(avg_speed_mbps, 2),
        "details": results
    }
    
    # Сохраняем в JSON
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    
    print(f"\n--- Результаты ---")
    print(f"Среднее время запроса: {avg_time:.3f} сек")
    print(f"Общий объём скачанных данных: {total_bytes / 1024:.2f} KB")
    print(f"Средняя скорость скачивания: {avg_speed_kbps:.2f} KB/s ({avg_speed_mbps:.2f} Mbps)")
    print(f"\nДетальный отчет сохранен в result.json")

if __name__ == "__main__":
    # Парсим аргументы: python speed_test.py <url> <num_requests>
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://httpbin.org/image/jpeg"
        
    num_requests = 10
    if len(sys.argv) > 2:
        try:
            num_requests = int(sys.argv[2])
        except ValueError:
            print("Ошибка: количество запросов должно быть числом.")
            sys.exit(1)
            
    measure_speed(url, num_requests)
