#include<iostream>
#include <cstdlib>
#include <ctime>
#include <string>

using namespace std;

class Bull_and_cow {
private:
    int n1, n2, n3, n4;
public:
    Bull_and_cow(int n1, int n2, int n3, int n4);
    int num1() { return this->n1; };
    int num2() { return this->n2; };
    int num3() { return this->n3; };
    int num4() { return this->n4; };
};

Bull_and_cow::Bull_and_cow(int n1, int n2, int n3, int n4) {
    this->n1 = n1;
    this->n2 = n2;
    this->n3 = n3;
    this->n4 = n4;
}

bool all_digits_different(int a, int b, int c, int d) {
    return a != b && a != c && a != d &&
        b != c && b != d &&
        c != d;
}

int main() {
    // Инициализация игры
    int n1, n2, n3, n4;
    srand(time(0));
    
    // Компьютер загадывает число
    do {
        n1 = rand() % 10;
        n2 = rand() % 10;
        n3 = rand() % 10;
        n4 = rand() % 10;
    } while (!all_digits_different(n1, n2, n3, n4));
    
    Bull_and_cow play(n1, n2, n3, n4);
    
    // Переменные для состояния игры
    static int current_n1 = 1, current_n2 = 2, current_n3 = 3, current_n4 = 4;
    static int best_n1 = 1, best_n2 = 2, best_n3 = 3, best_n4 = 4;
    static int best_bull = 0, best_cow = 0;
    static int return_to_best_count = 0;
    static bool first_computer_turn = true;
    static bool game_over = false;
    static bool player_won = false;
    static bool computer_won = false;
    
    // Получаем данные из формы
    char* query_string = getenv("QUERY_STRING");
    int guess_n1 = -1, guess_n2 = -1, guess_n3 = -1, guess_n4 = -1;
    int bull_players = -1, cow_players = -1;
    
    if (query_string != nullptr) {
        string query = query_string;
        
        // Парсим ввод игрока
        size_t pos = query.find("guess1=");
        if (pos != string::npos) {
            guess_n1 = stoi(query.substr(pos + 7, 1));
            pos = query.find("guess2=");
            if (pos != string::npos) guess_n2 = stoi(query.substr(pos + 7, 1));
            pos = query.find("guess3=");
            if (pos != string::npos) guess_n3 = stoi(query.substr(pos + 7, 1));
            pos = query.find("guess4=");
            if (pos != string::npos) guess_n4 = stoi(query.substr(pos + 7, 1));
        }
        
        // Парсим ответ на ход компьютера
        pos = query.find("bulls=");
        if (pos != string::npos) {
            bull_players = stoi(query.substr(pos + 6, 1));
            pos = query.find("cows=");
            if (pos != string::npos) cow_players = stoi(query.substr(pos + 5, 1));
        }
    }
    
    // Стили
    cout << "<style>";
    cout << ".game-area { background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.2); margin: 20px 0; }";
    cout << ".player-turn, .computer-turn { margin: 20px 0; padding: 15px; border-radius: 10px; }";
    cout << ".player-turn { background: rgba(0, 150, 255, 0.2); }";
    cout << ".computer-turn { background: rgba(0, 255, 136, 0.2); }";
    cout << ".input-form { margin: 15px 0; }";
    cout << ".number-input { width: 50px; height: 50px; text-align: center; font-size: 1.2em; margin: 5px; border: 2px solid #00ff88; border-radius: 8px; background: rgba(255, 255, 255, 0.1); color: white; }";
    cout << ".btn { background: linear-gradient(135deg, #00ff88 0%, #00a8ff 100%); color: #1a1a2e; border: none; padding: 12px 24px; border-radius: 25px; font-size: 1.1em; font-weight: bold; cursor: pointer; margin: 10px; }";
    cout << ".result { background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0; }";
    cout << ".bull { color: #ff6b6b; font-weight: bold; font-size: 1.2em; }";
    cout << ".cow { color: #ffd700; font-weight: bold; font-size: 1.2em; }";
    cout << ".status { font-size: 1.2em; font-weight: bold; padding: 10px; border-radius: 8px; text-align: center; }";
    cout << ".game-won { background: rgba(0, 255, 0, 0.3); color: #51ff00; }";
    cout << ".game-over { background: rgba(255, 0, 0, 0.3); color: #ff6b6b; }";
    cout << ".guess-display { font-size: 1.3em; font-weight: bold; margin: 10px 0; }";
    cout << ".response-input { width: 40px; height: 40px; text-align: center; margin: 0 5px; border: 1px solid #00a8ff; border-radius: 5px; background: rgba(255, 255, 255, 0.1); color: white; }";
    cout << ".computer-info { background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 5px; margin: 5px 0; font-size: 0.9em; }";
    cout << "</style>";
    
    cout << "<div class='game-area'>";
    
    // Обработка хода игрока
    if (guess_n1 != -1 && guess_n2 != -1 && guess_n3 != -1 && guess_n4 != -1) {
        int bull = 0, cow = 0;
        
        if (play.num1() == guess_n1) bull += 1;
        else if (play.num1() == guess_n2 || play.num1() == guess_n3 || play.num1() == guess_n4) cow += 1;
        if (play.num2() == guess_n2) bull += 1;
        else if (play.num2() == guess_n1 || play.num2() == guess_n3 || play.num2() == guess_n4) cow += 1;
        if (play.num3() == guess_n3) bull += 1;
        else if (play.num3() == guess_n2 || play.num3() == guess_n1 || play.num3() == guess_n4) cow += 1;
        if (play.num4() == guess_n4) bull += 1;
        else if (play.num4() == guess_n2 || play.num4() == guess_n3 || play.num4() == guess_n1) cow += 1;
        
        cout << "<div class='player-turn'>";
        cout << "<h3>🎮 Ваш ход:</h3>";
        cout << "<div class='result'>";
        cout << "<p>Вы ввели: <strong>" << guess_n1 << " " << guess_n2 << " " << guess_n3 << " " << guess_n4 << "</strong></p>";
        cout << "<p><span class='bull'>Быки: " << bull << "</span> | <span class='cow'>Коровы: " << cow << "</span></p>";
        
        if (bull == 4) {
            cout << "<div class='status game-won'>🎉 Поздравляем! Вы угадали число компьютера!</div>";
            player_won = true;
            game_over = true;
        }
        cout << "</div>";
        cout << "</div>";
    }
    
    // Логика компьютера
    if (!first_computer_turn && bull_players != -1 && cow_players != -1) {
        // Проверяем, не стал ли текущий результат ХУЖЕ лучшего
        int current_total = bull_players + cow_players;
        int best_total = best_bull + best_cow;
        
        if (current_total < best_total || (current_total == best_total && bull_players < best_bull)) {
            // Результат ухудшился - возвращаемся к ЛУЧШЕЙ комбинации
            current_n1 = best_n1;
            current_n2 = best_n2;
            current_n3 = best_n3;
            current_n4 = best_n4;
            return_to_best_count++;
            
            if (return_to_best_count >= 2) {
                // Радикально новая комбинация
                do {
                    current_n1 = rand() % 10;
                    current_n2 = rand() % 10;
                    current_n3 = rand() % 10;
                    current_n4 = rand() % 10;
                } while (!all_digits_different(current_n1, current_n2, current_n3, current_n4));
                return_to_best_count = 0;
            } else {
                // Случайная перестановка лучшей комбинации
                int digits[4] = { current_n1, current_n2, current_n3, current_n4 };
                for (int i = 3; i > 0; i--) {
                    int j = rand() % (i + 1);
                    int temp = digits[i];
                    digits[i] = digits[j];
                    digits[j] = temp;
                }
                current_n1 = digits[0];
                current_n2 = digits[1];
                current_n3 = digits[2];
                current_n4 = digits[3];
            }
        } else {
            return_to_best_count = 0;
        }
        
        // Обновляем лучший результат
        if (current_total > best_total || (current_total == best_total && bull_players > best_bull)) {
            best_n1 = current_n1;
            best_n2 = current_n2;
            best_n3 = current_n3;
            best_n4 = current_n4;
            best_bull = bull_players;
            best_cow = cow_players;
            return_to_best_count = 0;
        }
        
        // Проверяем победу компьютера
        if (bull_players == 4) {
            computer_won = true;
            game_over = true;
        }
    }
    
    // Форма для ввода игрока (если игра не окончена)
    if (!game_over) {
        cout << "<div class='player-turn'>";
        cout << "<h3>🔢 Ваш следующий ход:</h3>";
        cout << "<form method='get' class='input-form'>";
        if (bull_players != -1 && cow_players != -1) {
            cout << "<input type='hidden' name='bulls' value='" << bull_players << "'>";
            cout << "<input type='hidden' name='cows' value='" << cow_players << "'>";
        }
        cout << "<input type='number' class='number-input' name='guess1' min='0' max='9' required>";
        cout << "<input type='number' class='number-input' name='guess2' min='0' max='9' required>";
        cout << "<input type='number' class='number-input' name='guess3' min='0' max='9' required>";
        cout << "<input type='number' class='number-input' name='guess4' min='0' max='9' required>";
        cout << "<br>";
        cout << "<button type='submit' class='btn'>Сделать ход</button>";
        cout << "</form>";
        cout << "</div>";
    }
    
    // Ход компьютера (если игра не окончена)
    if (!game_over) {
        cout << "<div class='computer-turn'>";
        cout << "<h3>🤖 Ход компьютера:</h3>";
        cout << "<div class='guess-display'>";
        cout << "Компьютер предполагает: <strong>" << current_n1 << " " << current_n2 << " " << current_n3 << " " << current_n4 << "</strong>";
        cout << "</div>";
        
        if (!first_computer_turn) {
            cout << "<div class='computer-info'>";
            cout << "Лучший результат: " << best_bull << " быков, " << best_cow << " коров";
            cout << "</div>";
        }
        
        cout << "<form method='get' class='input-form'>";
        if (guess_n1 != -1) {
            cout << "<input type='hidden' name='guess1' value='" << guess_n1 << "'>";
            cout << "<input type='hidden' name='guess2' value='" << guess_n2 << "'>";
            cout << "<input type='hidden' name='guess3' value='" << guess_n3 << "'>";
            cout << "<input type='hidden' name='guess4' value='" << guess_n4 << "'>";
        }
        cout << "Быки: <input type='number' class='response-input' name='bulls' min='0' max='4' required> ";
        cout << "Коровы: <input type='number' class='response-input' name='cows' min='0' max='4' required>";
        cout << "<br>";
        cout << "<button type='submit' class='btn'>Отправить ответ</button>";
        cout << "</form>";
        cout << "</div>";
    }
    
    // Сообщения о результате игры
    if (game_over) {
        cout << "<div class='status'>";
        if (player_won) {
            cout << "<div class='game-won'>🎉 Игра окончена! Вы победили!</div>";
        } else if (computer_won) {
            cout << "<div class='game-over'>💥 Игра окончена! Компьютер победил!</div>";
        }
        cout << "<br><a href='?' class='btn'>Новая игра</a>";
        cout << "</div>";
    }
    
    first_computer_turn = false;
    
    cout << "</div>";
    return 0;
}