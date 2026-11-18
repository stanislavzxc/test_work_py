import sys
import time
import requests

def measure_speed(url, num_requests=10):
    total_time = 0.0
    total_bytes = 0
    
    print(f"Замер скорости для: {url}")
    print(f"Количество запросов: {num_requests}\n")

    # Прогреваем соединение (первый запрос часто медленнее из-за handshake)
    # Но по условию задачи делаем ровно 10 запросов, поэтому просто идем по циклу.
    
    for i in range(1, num_requests + 1):
        try:
            start_time = time.time()
            
            # stream=True позволяет скачивать данные кусками (chunks), а не держать всё в памяти
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status() # Вызовет ошибку, если статус 4xx или 5xx
            
            # Ждем полной загрузки ответа
            content = response.content 
            
            end_time = time.time()
            
            time_taken = end_time - start_time
            bytes_downloaded = len(content)
            
            total_time += time_taken
            total_bytes += bytes_downloaded
            
            # Вывод в консоль для каждого запроса (опционально)
            # print(f"Запрос {i}: {time_taken:.2f} сек, {bytes_downloaded / 1024 / 1024:.2f} МБ")
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {i}: {e}")

    if total_time == 0:
        print("Не удалось выполнить ни одного запроса.")
        return

    # Расчеты
    avg_time = total_time / num_requests
    avg_bytes = total_bytes / num_requests
    total_mb = total_bytes / (1024 * 1024)
    
    # Скорость в Мегабитах в секунду (Mbps)
    # Формула: (Байты * 8) / (Секунды * 1024 * 1024)
    speed_mbps = (total_bytes * 8) / (total_time * 1024 * 1024)

    print("\n--- ИТОГИ ---")
    print(f"Среднее время запроса: {avg_time:.2f} сек")
    print(f"Средний размер: {avg_bytes / 1024 / 1024:.2f} МБ")
    print(f"Общий скачанный объём: {total_mb:.2f} МБ")
    print(f"Скорость скачивания: {speed_mbps:.2f} Мбит/с (Mbps)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python speed_test.py <URL>")
        print("Пример: python speed_test.py https://example.com/image.jpg")
    else:
        target_url = sys.argv[1]
        measure_speed(target_url)