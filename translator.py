import os
import shutil
from deep_translator import GoogleTranslator
import sys
import time

if not os.path.isfile("mod-info.txt"):
    print("ОШИБКА: Файл 'mod-info.txt' не найден в этой папке.\nЭто не корневая папка мода")
    time.sleep(10)
    sys.exit()

TARGET_KEY = "displayDescription:"

SOURCE_LANG = 'en'
TARGET_LANG = 'ru'
backup = 0
print("Переводчик модов для игры Rusted Warfare\nСоздатель: t.me/KPAKOB\nУсловие:\n-Поместить transl.exe в папку с модо\n\nКак определить что нужная папка?\n- Наличие в папке файла mod-info.txt\n\n")
check = input("Создавать резервные копии файлов?\nОтвет(yes/no): ")
if check == 'yes':
    backup = 1

def translate_text(text):
    """
    Функция для перевода текста.
    Сохраняет переносы строк \n.
    """
    try:
        translator = GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"    [!] Ошибка перевода: {e}")
        return None

def process_ini_file(file_path):
    """
    Обрабатывает один .ini файл: ищет нужные строки, переводит и заменяет их.
    """
    print(f"\n--- Проверяем файл: {file_path} ---")
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"  [!] Не удалось прочитать файл: {e}")
        return

    new_lines = []
    was_modified = False

    for line in lines:
        if line.strip().startswith(TARGET_KEY):
            parts = line.split(':', 1)
            if len(parts) == 2:
                key_part = parts[0]
                text_to_translate = parts[1].strip()

                log_text = text_to_translate.replace('\\n', ' ')
                print(f"  [+] Найдена строка для перевода: {log_text}")
                
                translated_text = translate_text(text_to_translate.replace('\\n', '\n'))

                if translated_text:
                    final_translated_text = translated_text.replace('\n', '\\n')
                    
                    log_translated_text = final_translated_text.replace('\\n', ' ')
                    print(f"  [->] Результат перевода: {log_translated_text}")

                    indentation = line[:line.find(key_part)]
                    new_line = f"{indentation}{key_part}: {final_translated_text}\n"
                    new_lines.append(new_line)
                    was_modified = True
                else:
                    print("  [!] Перевод не удался, оставляем оригинал.")
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if was_modified:
        try:
            if backup == 1:
                backup_path = file_path + '.bak'
                print(f"  [*] Создаю резервную копию: {backup_path}")
                shutil.copy2(file_path, backup_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"  [OK] Файл успешно обновлен!")
        except Exception as e:
            print(f"  [!] Не удалось записать изменения в файл: {e}")
    else:
        print("  [*] Изменений не найдено, файл пропущен.")


def main():
    try:
        start_path = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        start_path = os.getcwd()
        
    print(f"Запускаю поиск .ini файлов в папке: {start_path} и всех ее подпапках...")

    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in ['__pycache__']]
        
        for filename in files:
            if filename.endswith('.ini'):
                file_path = os.path.join(root, filename)
                process_ini_file(file_path)
    
    print("\n====================")
    print("Работа скрипта завершена.")

# Запуск основной функции
if __name__ == "__main__":
    main()
