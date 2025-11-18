import re
from collections import defaultdict


def count_artists_tracks(file_path):
    # Словарь для хранения количества треков по исполнителям
    artist_tracks = defaultdict(int)

    # Регулярное выражение для поиска фитов и совместных исполнителей
    # Ищем конструкции с feat., feat, &, и просто запятые между исполнителями
    feat_pattern = re.compile(r'(?:\s+feat\.?|\s+&|,)\s+', re.IGNORECASE)

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # Пропускаем пустые строки и строки с комментариями
            if not line or line.startswith('#'):
                continue

            # Разделяем строку на исполнителя и трек
            if ' - ' in line:
                artist_part, track_part = line.split(' - ', 1)

                # Обрабатываем исполнителей
                artists = []

                # Разделяем основного исполнителя и фиты
                main_artist_match = re.split(feat_pattern, artist_part)
                if main_artist_match:
                    # Первый элемент - основной исполнитель
                    main_artist = main_artist_match[0].strip()
                    artists.append(main_artist)

                    # Остальные - участники фитов
                    for feat_artist in main_artist_match[1:]:
                        feat_artist = feat_artist.strip()
                        if feat_artist:
                            artists.append(feat_artist)

                # Добавляем +1 трек каждому исполнителю
                for artist in artists:
                    artist_tracks[artist] += 1

    return artist_tracks


def save_results(artist_tracks, output_file):
    # Сортируем по количеству треков (по убыванию)
    sorted_artists = sorted(artist_tracks.items(), key=lambda x: x[1], reverse=True)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("Исполнитель | Количество треков\n")
        file.write("-" * 40 + "\n")

        for artist, count in sorted_artists:
            file.write(f"{artist} | {count}\n")


def main():
    input_file = "vk_music_complete.txt"
    output_file = "artist_tracks_count.txt"

    print("Подсчет количества треков по исполнителям...")
    artist_tracks = count_artists_tracks(input_file)

    print(f"Найдено {len(artist_tracks)} уникальных исполнителей")

    # Сохраняем результаты
    save_results(artist_tracks, output_file)
    print(f"Результаты сохранены в файл: {output_file}")

    # Выводим топ-10 исполнителей
    print("\nТоп-10 исполнителей по количеству треков:")
    sorted_artists = sorted(artist_tracks.items(), key=lambda x: x[1], reverse=True)
    for i, (artist, count) in enumerate(sorted_artists[:10], 1):
        print(f"{i}. {artist}: {count} треков")


if __name__ == "__main__":
    main()