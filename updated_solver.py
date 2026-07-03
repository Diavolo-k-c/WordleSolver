from logging import exception

wordle = [""] * 5
ban = []
unknown = []
matches = []

try:
    word = str(input("Известные буквы: "))
    banned = str(input("Буквы для бана: "))
except exception as e:
    print(e)
    exit()

for b in banned:
    if b.isalpha():
        ban.append(b.lower())

for i in range(len(word)):
    try:
        a = input(f"Буква '{word[i]}' жёлтая? (y/n)").lower()
        if a == "y":
            unknown.append(word[i])
        else:
            indx = int(input(f"Позиция буквы '{word[i]}': "))
            indx -= 1
            if 0 <= indx < 5:
                wordle[indx] = word[i]
            else:
                print("Ошибка: Неверная позиция: ")
                break
    except ValueError:
        print("Ошибка: Нужно ввести число")

with open("Words", "r") as file:
    words = file.read().split("\n")

# Список для хранения слов с их вероятностью
word_scores = []

for word in words:

    green_match = True
    yellow_match = True
    banned_match = True

    for i in range(5):
        if wordle[i] and wordle[i] != word[i]:
            green_match = False
            break
    if not green_match:
        continue

    for letter in unknown:
        if letter not in word:
            yellow_match = False
            break
    if not yellow_match:
        continue

    for letter in ban:
        if letter in word:
            banned_match = False
            break
    if not banned_match:
        continue

    # Вероятность
    score = 0

    for i in range(5):
        if wordle[i] and wordle[i] == word[i]:
            score += 5

    rare_letters = ['q', 'x', 'z', 'j', 'v', 'k']
    for letter in word:
        if letter in rare_letters:
            score -= 1

    popular_letters = ['e', 'a', 'r', 'o', 'i', 'l', 's', 't']
    for letter in word:
        if letter in popular_letters:
            score += 1

    word_scores.append((word, score))

# Сортировка по убыванию вероятности
word_scores.sort(key=lambda x: x[1], reverse=True)

print("\nНаиболее вероятные слова: ")
top_count = min(10, len(word_scores))
for i in range(top_count):
    word, score = word_scores[i]
    print(f"{word} (Вероятность: {score})")

# Если нужно показать все слова
if len(word_scores) > 10:
    show_all = input(f"\nПоказать все {len(word_scores)} слов? (y/n): ").lower()
    if show_all == "y":
        for i in range(len(word_scores)):
            word, score = word_scores[i]
            print(f"{word} ({score})")