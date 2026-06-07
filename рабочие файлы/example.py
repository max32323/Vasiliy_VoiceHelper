import subprocess
import os

def revert_local_changes():
    """
    Отменяет все несохраненные локальные изменения в Git-репозитории,
    возвращая файлы к состоянию последнего коммита.
    """
    # Проверяем, находимся ли мы в Git-репозитории
    if not os.path.isdir(".git"):
        print("Ошибка: Текущая директория не является Git-репозиторием.")
        return

    try:
        # Команда 'git checkout .' сбрасывает все локальные изменения
        # в текущем каталоге и его подкаталогах, возвращая их к последнему коммиту.
        # Важно: Это действие необратимо для несохраненных изменений.
        process = subprocess.run(
            ["git", "checkout", "."],
            capture_output=True,
            text=True,
            check=True # Вызовет исключение, если команда завершится с ошибкой
        )
        print("Все несохраненные локальные изменения успешно отменены.")
        if process.stdout:
            print("Вывод команды:\n", process.stdout)
        if process.stderr:
            print("Ошибки (если есть):\n", process.stderr)

        # Дополнительно можно проверить статус, чтобы убедиться, что все чисто
        status_process = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        if not status_process.stdout:
            print("Git статус: Рабочий каталог чист.")
        else:
            print("Git статус (остались изменения?):\n", status_process.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Произошла ошибка при отмене изменений: {e}")
        print(f"Stderr:\n{e.stderr}")
    except FileNotFoundError:
        print("Ошибка: Команда 'git' не найдена. Убедитесь, что Git установлен и доступен в PATH.")

# Пример вызова функции:
# revert_local_changes()
