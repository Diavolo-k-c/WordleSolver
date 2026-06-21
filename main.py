import random
import enchant

wordle = [""] * 5
word = input("Известные буквы (Введи > 5 для жёлтой): ")
ban = list(input("Буквы для бана: "))
iters = int(input("Итераций(для перестановки букв с неизвестной позицией): "))
repetitions = int(input("Раз генерации слова (Рек.: > 200): "))
unknown = [""] * 5

#Возвращает рандомный индекс к букве
def random_index(wordle):
    free_index = [i for j, char in enumerate(wordle) if char == ""]
    return random.choice(free_index)

#Для каждой введённой буквы
for i in range(len(word)):
    indx = int(input(f"На каком месте находится '{word[i]}'?: "))
    indx -= 1 #Чтобы вводить место буквы, а не её индекс
    if 0 <= indx < 5:
        wordle[indx] = word[i]
    else:
        indx = random_index(wordle)
        unknown[indx] = word[i]

# Удаление пустых строк для работы с буквами
unknown = [x for x in unknown if x != ""]

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

available_letters = [letter for letter in letters if letter not in ban and letter not in unknown]

# Поиск пустых слотов
empty_word = [i for i, x in enumerate(wordle) if x == ""] #Принимает пустой слот
possible_words = set()  # Сет для того, чтобы использовать add

#Проверка на существование слова
def is_english_word(word):
    d = enchant.Dict("en_US")
    return d.check(word)

for i in range(iters):
    # Перемешивание неизвестных букв
    unknown_letters = unknown.copy()
    random.shuffle(unknown_letters)

    #Создание слов (По количеству)
    for j in range(repetitions):
        #Добавляет сырое слово в wordle
        temp_word = wordle[:]

        # Если есть неизвестные буквы и свободные слоты
        if unknown_letters and empty_word:
            #Копирует пустые слоты и перемешивает их для дальнейшей работы
            shuffled_positions = empty_word.copy()

            # Очищение позиций неизвестных букв для работы со списком
            for pos in empty_word:
                temp_word[pos] = ""

            # Неизвестные буквы вставляются в список
            for k, letter in enumerate(unknown_letters):
                if k < len(shuffled_positions):
                    temp_word[shuffled_positions[k]] = letter

            # Поиск оставшихся пустых позиций
            remaining_empty = [i for i, x in enumerate(temp_word) if x == ""]
        else:
            #Если нет - создаётся новый такой же список (Чтобы в любом случае использовать его)
            remaining_empty = empty_word

        # Оставшиеся пустые места заполняются случайными буквами
        for idx in remaining_empty:
            temp_word[idx] = random.choice(available_letters)

        #Добавляет сгенерированную букву к списку
        generated_word = "".join(temp_word)

        # Проверяем, что все буквы из unknown использованы по одному разу, чтобы не путать цикл
        if unknown:
            valid = True
            for letter in unknown:
                #Проверка на количество использованных букв с неизвестной позицией
                if generated_word.count(letter) != 1:
                    valid = False
                    break
            #Если буква с неизвестной позицией используется 1 раз и длина сгенерированного слова 5
            if valid and len(generated_word) == 5:
                # Проверяет, является ли слово английским и добавляет в конечный список
                if is_english_word(generated_word):
                    possible_words.add(generated_word)
        else:
            #Если нет буквы с неизвестной позицией
            if len(generated_word) == 5 and is_english_word(generated_word):
                possible_words.add(generated_word)

for word in possible_words:
    if len(word) == 5:
        print(word)