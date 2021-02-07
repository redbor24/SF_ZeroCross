# SkillFactory
# Итоговое задание блока B5 - игра "Крестики-нолики"
import os
from random import randint
# import algorithm as al

# declare section
# Словарь настроек и динамических данных игровой сессии
config = {
    # Настройки
    "board_size": (3),  # Размеры игрового поля. Т.к. игровое поле у нас квадратное, то и переменная одна
                        # Сделал кортежем, чтобы защитить от случайного изменения в коде
    "step_type": ("X", "0"),  # Возможные варианты фишек
    "player_type": ("I", "C"),  # Возможные варианты выбора первоочередного хода
    "session_state": ("SE", "X", "0", "DRAW"),  # Варианты состояния партии:
                                                  # можно сделать следующий ход, выиграл человек, выиграл компьютер, ничья
    "cell_nums": list(range(10)),  # Набор допустимых номеров клеток:
                                   # 1-9 сами номера ячеек
                                   # 0 используется для выхода из игры
#    "prefix"
    # -------------------------------
    # Параметры игровой сессии
    "player_step_type": None,  # чем играет человек - индекс в config["step_type"]
    "computer_step_type": None,  # чем играет компьютер - индекс в config["step_type"]
    # Номер клетки хода - индекс из "cell_nums"
    "player_step_cell": None,  # человека
    "computer_step_cell": None,  # компьютера
    "first_step": None,  # Кто ходит первым: индекс в config["player_type"]
    "last_step": None,  # Чей был последний ход: индекс в config["player_type"]
    "break_session": False  # Признак прерывания партии
}
board = []  # Игровое поле - список списков (матрица)
print_data = []  # данные для отображения на экране


# Очистка консоли
def clear():
    os.system('cls')


# Возвращает чем занята клетка
def check_cell(cell_number):
    x = get_cell_coord(cell_number)
    return board[x[0]][x[1]]


# Выводит игровое поле
def print_board():
    print('\033[2J')  # clear()
    print("")
    print("\u001b[0m-------- Табло --------\u001b[38;5;4m")
    print(*print_data, sep="\n")
    print("\u001b[0m-------- Табло --------\u001b[0m")

    for i in range(1, len(board) + 1):
        for j in range(1, len(board) + 1):
            s = "\u001b[38;5;<brd_c>m(\u001b[38;5;<step_c>m<step_type>\u001b[38;5;<brd_c>m)\u001b[0m"
            s2 = str(board[i - 1][j - 1])
            # Зададим саму фишку
            s = s.replace("<step_type>", s2)
            # Зададим цвет фишки
            if s2 == "X":
                s = s.replace("<step_c>", "14")  # Яркий светло-голубой
            elif s2 == "0":
                s = s.replace("<step_c>", "11")  # Ярко-жёлтый
            else:
                s = s.replace("<step_c>", "7")  # Серый

            # Зададим цвет границ
            s = s.replace("<brd_c>", "8")  # Тускло-серый
            print(s, end="")
        print("")


# Инициализация игрового поля
def init_board():
    z = [[" " for j in range(config["board_size"])] for i in range(config["board_size"])]
    for i in range(config["board_size"]**2):
        y = get_cell_coord(i + 1)
        z[y[0]][y[1]] = str(i + 1)
    return z


# Спросим у игрока чем он хочет играть - крестиками или ноликами?
def ask_step_type():
    while True:
        s = str.upper(input(f"Выберите крестик или нолик ({', '.join(config['step_type'])}):"))
        if s not in config["step_type"]:
            print("Неверный выбор!")
        else:
            if s == config["step_type"][0]:
                config["player_step_type"] = 0
                config["computer_step_type"] = 1
            else:
                config["player_step_type"] = 1
                config["computer_step_type"] = 0  # config["step_type"][0]
            print_data.append(f'Ваша фишка - "{config["step_type"][config["player_step_type"]]}"')
            print_data.append(f'Фишка компьютера - "{config["step_type"][config["computer_step_type"]]}"')
            break


# Спросим у игрока чей будет первый ход его или компьютера?
def ask_human_first_step():
    while True:
        s = input('Кто будет ходить первым - вы или компьютер? Введите "I" или "C":').strip().upper()
        if s not in config["player_type"]:
            print("Ошибка!")
            continue
        config["first_step"] = config["player_type"].index(s)
        print_data.append(f'Первым ходит {"игрок" if s == config["player_type"][0] else "компьютер"}')
        break


def get_cell_coord(
        cell_num  # номер ячейки на игровом поле
                   ):
    if cell_num == 7:
        return 0, 0
    elif cell_num == 8:
        return 0, 1
    elif cell_num == 9:
        return 0, 2
    elif cell_num == 4:
        return 1, 0
    elif cell_num == 5:
        return 1, 1
    elif cell_num == 6:
        return 1, 2
    elif cell_num == 1:
        return 2, 0
    elif cell_num == 2:
        return 2, 1
    elif cell_num == 3:
        return 2, 2


# Запросим у пользователя номер клетки
def do_human_step():
    # Пока не будет введён верный номер клетки
    while True:
        s = input(f"Ваш ход (введите номер клетки, 0 - завершение игры): ")
        if not s.strip().isalnum():
            print("Ошибка! Нужно вводить только цифры!")
            continue
        z = int(s)
        if z not in config["cell_nums"]:
            print(f'Ошибка! Номер клетки должен быть от 1 до {len(config["cell_nums"]) - 1}')
            continue
        # завершение программы
        if z == 0:
            print(z)
            return -1
        # Клетка должна быть свободной
        x = get_cell_coord(z)
        if board[x[0]][x[1]] in config["step_type"]:
            print(f"Ошибка! Клетка номер {z} занята!")
            continue
        config["player_step_cell"] = z
        x = get_cell_coord(z)
        board[x[0]][x[1]] = config["step_type"][config["player_step_type"]]
        config["last_step"] = 0
        print_board()
        break
    return z


# анализ состояния партии
def analyze_board():
    # Проверим заполненность линий
    x = check_lines()
    if x == "X":
        return config["session_state"][1]  # Выиграли крестики
    elif x == "0":
        return config["session_state"][2]  # Выиграли нолики

    # Есть ли свободные клетки
    free_cell_count = 0
    for i in range(config["board_size"]**2):
        y = get_cell_coord(i + 1)
        if not board[y[0]][y[1]].isalpha():
            if 1 <= int(board[y[0]][y[1]]) <= 9:
                free_cell_count += 1
    if not free_cell_count:
        return config["session_state"][3]  # свободных клеток нет - ничья

    return config["session_state"][0]  # ещё есть ходы


# проверяет наличие в матрице заполненных линий. При обнаружении возвращает фишку, из которой состоит найденная линия
def check_lines():
    s = "X"
    # Одна из трёх горизонтальных строк
    # Один из трёх столбцов
    # Одна из двух диагоналей
    if board[0][0] == s and board[0][1] == s and board[0][2] == s or \
        board[1][0] == s and board[1][1] == s and board[1][2] == s or \
        board[2][0] == s and board[2][1] == s and board[2][2] == s or \
        board[0][0] == s and board[1][0] == s and board[2][0] == s or \
        board[0][1] == s and board[1][1] == s and board[2][1] == s or \
        board[0][2] == s and board[1][2] == s and board[2][2] == s or \
        board[0][0] == s and board[1][1] == s and board[2][2] == s or \
        board[0][2] == s and board[1][1] == s and board[2][0] == s:
        return s
    s = "0"
    if board[0][0] == s and board[0][1] == s and board[0][2] == s or \
        board[1][0] == s and board[1][1] == s and board[1][2] == s or \
        board[2][0] == s and board[2][1] == s and board[2][2] == s or \
        board[0][0] == s and board[1][0] == s and board[2][0] == s or \
        board[0][1] == s and board[1][1] == s and board[2][1] == s or \
        board[0][2] == s and board[1][2] == s and board[2][2] == s or \
        board[0][0] == s and board[1][1] == s and board[2][2] == s or \
        board[0][2] == s and board[1][1] == s and board[2][0] == s:
        return s
    return ""

# В цикле, пока есть пустые поля:
#     if (есть линия с двумя "фишками" противника)
#         { ход на свободное поле в этой линии }
#     elif (есть линия с двумя своими "фишками" и пустым полем)
#         { завершаем выигрышем }  # противник ошибся
#         else
#             { ставим фишку в любое свободное поле }
#             проверяем позицию на предмет выигрыша одной из сторон

# ход компа
def do_comp_step():
    z = randint(1, config["board_size"]**2)
    while True:
        xx = check_cell(z)
        if xx in config["step_type"]:
            z = randint(1, config["board_size"] ** 2)
        else:
            break
    config["computer_step_cell"] = z
    x = get_cell_coord(z)
    board[x[0]][x[1]] = config["step_type"][config["computer_step_type"]]
    config["last_step"] = 1
    print_board()


# делаем ход
def do_step():
    if config["last_step"] == 1:  # первым ходит человек
        if do_human_step() == -1:  # если человек прервал игру
            config["break_session"] = True
    else:
        do_comp_step()


# Вывод состяния партии
def session_state():
    x = analyze_board()
    if x == config["session_state"][0]:  # есть ход
        s = "Партия незавершена"
    elif x == config["session_state"][1]:  # выиграли крестики
        s = "Выиграли крестики! :)))"
    elif x == config["session_state"][2]:  # выиграли нолики
        s = "Выиграли нолики! :((("
    elif x == config["session_state"][3]:  # ничья
        s = "Ничья! :|||"
    print("\u001b[38;5;9m" + s + "\u001b[0m")


# тело программы
board = init_board()
# print_board()
# exit()
# запрос конфигурации
ask_step_type()
ask_human_first_step()
print_board()

# цикл по ходам
sess_state = None
if config["first_step"] == 0:  # первым ходит человек
    config["last_step"] = 1  # то запишем, что предыдущий ход был сделан компом

while True:
    do_step()
    if config["break_session"]:
        session_state()
        break

    sess_state = analyze_board()
    # Если нет свободных клеток - игра закончена
    if sess_state != config["session_state"][0]:
        session_state()
        break


