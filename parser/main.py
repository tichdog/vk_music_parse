from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def enhanced_vk_parser():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        print("1. Войдите в VK в открывшемся браузере")
        print("2. Перейдите на страницу аудиозаписей")
        print("Вид URL должен быть: https://vk.com/audios*********?section=all")
        print("3. После загрузки страницы нажмите Enter здесь в консоли")
        input("Готовы? Нажмите Enter...")

        tracks = []
        no_new_tracks_count = 0
        max_scrolls = 100  # Максимум прокруток

        print("Начинаем сбор треков...")

        for scroll_attempt in range(max_scrolls):
            print(f"\nИтерация {scroll_attempt + 1}")
            # Даем время на загрузку
            time.sleep(2.5)

            # Прокручиваем немного вверх и вниз
            if scroll_attempt > 0:
                driver.execute_script("window.scrollTo(0, window.scrollY - 300);")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # Ждем появления треков
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".audio_row._audio_row"))
                )
            except:
                print("Треки не загрузились, продолжаем...")

            # Ищем все элементы с треками
            track_elements = driver.find_elements(By.CSS_SELECTOR, ".audio_row._audio_row")
            print(f"Найдено элементов: {len(track_elements)}")

            current_batch = 0

            # Берем каждый трек
            for i, element in enumerate(track_elements):
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(0.1)  # Минимальная задержка
                    artist_elem = element.find_element(By.CSS_SELECTOR, ".audio_row__performers")
                    title_elem = element.find_element(By.CSS_SELECTOR, ".audio_row__title_inner")
                    artist = artist_elem.text.strip()
                    title = title_elem.text.strip()

                    if artist and title:
                        track_key = f"{artist}|{title}"
                        existing_keys = [f"{t['artist']}|{t['title']}" for t in tracks]

                        if track_key not in existing_keys:
                            try:
                                duration_elem = element.find_element(By.CSS_SELECTOR, ".audio_row__duration")
                                duration = duration_elem.text.strip()
                            except:
                                duration = "?:??"

                            tracks.append({
                                'artist': artist,
                                'title': title,
                                'duration': duration
                            })
                            current_batch += 1

                            # Выводим прогресс
                            if len(tracks) % 10 == 0:
                                print(f"Достигнуто {len(tracks)} треков...")

                except Exception as e:
                    continue

            # Статистика
            if current_batch > 0:
                print(f"Добавлено: {current_batch} новых треков")
                no_new_tracks_count = 0
            else:
                print("Новых треков не найдено")
                no_new_tracks_count += 1

            print(f"Всего уникальных: {len(tracks)}")

            # Проверяем разные условия остановки
            if no_new_tracks_count >= 1:
                print("Вероятно все треки загружены!")
                # Финальная попытка - прокрутим еще раз медленно
                print("Финальная проверка...")
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)
                for pos in range(0, 5):
                    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {pos / 4});")
                    time.sleep(1)

                # Последняя проверка треков
                final_elements = driver.find_elements(By.CSS_SELECTOR, ".audio_row._audio_row")
                print(f"После финальной прокрутки: {len(final_elements)} элементов")
                break

            # Прокручиваем вниз для следующей итерации
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Финальный сбор всех видимых треков
        print("\nФинальный сбор всех треков...")
        all_elements = driver.find_elements(By.CSS_SELECTOR, ".audio_row._audio_row")

        for element in all_elements:
            try:
                artist = element.find_element(By.CSS_SELECTOR, ".audio_row__performers").text.strip()
                title = element.find_element(By.CSS_SELECTOR, ".audio_row__title_inner").text.strip()

                if artist and title:
                    track_key = f"{artist}|{title}"
                    existing_keys = [f"{t['artist']}|{t['title']}" for t in tracks]

                    if track_key not in existing_keys:
                        try:
                            duration = element.find_element(By.CSS_SELECTOR, ".audio_row__duration").text.strip()
                        except:
                            duration = "?:??"

                        tracks.append({
                            'artist': artist,
                            'title': title,
                            'duration': duration
                        })
            except:
                continue

        print(f"ФИНАЛЬНЫЙ РЕЗУЛЬТАТ: {len(tracks)} уникальных треков")

        return tracks

    except Exception as e:
        print(f"Ошибка: {e}")
        return [], 0
    finally:
        driver.quit()


def save_results(tracks):
    if not tracks:
        print("Нет треков для сохранения")
        return
    tracks_sorted = sorted(tracks, key=lambda x: x['artist'])
    # Основной файл
    filename = f'vk_music_complete.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for i, track in enumerate(tracks_sorted, 1):
            f.write(f"{track['artist']} - {track['title']} ({track['duration']})\n")


# Запуск
if __name__ == "__main__":
    tracks = enhanced_vk_parser()
    save_results(tracks)