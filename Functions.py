import database
import numpy as np

def remove_dominated_strategies(matrix, weak=True):
    """
    Удаляет строго и слабо доминируемые стратегии.
    Параметр weak=True включает удаление слабого доминирования.
    """
    player1_matrix, player2_matrix = parse_bimatrix(matrix)

    while True:
        removed = False

        # Поиск доминируемых строк для первого игрока
        dominated_rows = set()
        for i in range(player1_matrix.shape[0]):
            for k in range(player1_matrix.shape[0]):
                if i != k:
                    if weak:
                        # Слабое доминирование: одна строка не лучше другой и хотя бы раз хуже
                        if np.all(player1_matrix[i, :] <= player1_matrix[k, :]) and np.any(player1_matrix[i, :] < player1_matrix[k, :]):
                            dominated_rows.add(i)
                    else:
                        # Строгое доминирование: одна строка всегда хуже другой
                        if np.all(player1_matrix[i, :] < player1_matrix[k, :]):
                            dominated_rows.add(i)

        # Удаляем доминируемые строки
        if dominated_rows:
            player1_matrix = np.delete(player1_matrix, list(dominated_rows), axis=0)
            player2_matrix = np.delete(player2_matrix, list(dominated_rows), axis=0)
            removed = True

        # После удаления строк, ищем и удаляем доминируемые столбцы для второго игрока
        dominated_cols = set()
        for j in range(player2_matrix.shape[1]):
            for m in range(player2_matrix.shape[1]):
                if j != m:
                    if weak:
                        # Слабое доминирование
                        if np.all(player2_matrix[:, j] <= player2_matrix[:, m]) and np.any(player2_matrix[:, j] < player2_matrix[:, m]):
                            dominated_cols.add(j)
                    else:
                        # Строгое доминирование
                        if np.all(player2_matrix[:, j] < player2_matrix[:, m]):
                            dominated_cols.add(j)

        # Удаляем доминируемые столбцы
        if dominated_cols:
            player1_matrix = np.delete(player1_matrix, list(dominated_cols), axis=1)
            player2_matrix = np.delete(player2_matrix, list(dominated_cols), axis=1)
            removed = True

        # Если нечего удалять — выходим
        if not removed:
            break

    return player1_matrix, player2_matrix

def save_csv_to_db(username, csv_data):
    conn, cursor = database.get_db_connection()

    # Проверяем, существует ли пользователь с таким username
    cursor.execute('''SELECT id FROM users WHERE username = ?''', (username,))
    user = cursor.fetchone()

    if user:
        # Если пользователь существует, обновляем его CSV
        cursor.execute('''UPDATE users SET csv_file = ? WHERE username = ?''', (csv_data, username))
    else:
        # Если пользователя нет, вставляем новый
        cursor.execute('''INSERT INTO users (username, password, csv_file)
                          VALUES (?, ?, ?)''', (username, "user_password", csv_data))
    
    conn.commit()
    conn.close()
    
def parse_bimatrix(matrix):
    """
    Преобразует матрицу строковых значений ("(a;b)") в два массива выигрышей для каждого игрока.
    """
    rows, cols = len(matrix), len(matrix[0])
    player1_matrix = np.zeros((rows, cols))
    player2_matrix = np.zeros((rows, cols))
    
    for i in range(rows):
        for j in range(cols):
            value = matrix[i][j].strip("()").split(";")
            player1_matrix[i, j] = int(value[0])
            player2_matrix[i, j] = int(value[1])
    
    return player1_matrix, player2_matrix

def minimax_bimatrix(matrix):
    """
    Рассчитывает минимаксную стратегию для обоих игроков в биматричной игре.
    """
    player1_matrix, player2_matrix = parse_bimatrix(matrix)
    
    # Минимакс для первого игрока
    min_in_rows = np.min(player1_matrix, axis=1)
    maximin_p1 = np.max(min_in_rows)
    
    # Минимакс для второго игрока
    min_in_cols = np.min(player2_matrix, axis=0)
    maximin_p2 = np.max(min_in_cols)
    
    return maximin_p1, maximin_p2

def nash_equilibria(matrix):
    """
    Находит равновесия Нэша в биматричной игре.
    """
    player1_matrix, player2_matrix = parse_bimatrix(matrix)
    rows, cols = player1_matrix.shape
    equilibria = []
    
    for i in range(rows):
        for j in range(cols):
            p1_payoff = player1_matrix[i, j]
            p2_payoff = player2_matrix[i, j]
            
            best_response_p1 = p1_payoff == np.max(player1_matrix[:, j])
            best_response_p2 = p2_payoff == np.max(player2_matrix[i, :])
            
            if best_response_p1 and best_response_p2:
                equilibria.append((i, j))
    
    return equilibria