import datetime as dt
# Вопрос уже к тому кто будет проверять меня: пункт из требований про Docstrings про то что они обязательны для функций?
# Или про то что если и писать комментарии к функциям, то в таком виде?
# Для первого случая:
# К почти всем функциям отсутствуют комментарии. Оформлять их стоит в виде Docstrings. Почитать про это можно вот тут:
# https://peps.python.org/pep-0257/
# Для второго случая:
# Комментарии к функциям это хорошо: def get_calories_remained(self):  # Получает остаток калорий на сегодня
# Но лучше оформлять из в виде Docstrings. Почитать про это можно вот тут:
# https://peps.python.org/pep-0257/
# Ну и раз уж написали комментарий к функции, get_calories_remained, то мне кажется логичным написать комментарий к
# похожей функции get_today_cash_remained


class Record:
    # Когда предполагается, что date может не быть вообще, то лучше задать его как date=None
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # if not date неявная проверка, которой стоит избегать, с учетом предыдущей рекомендации стоит написать
        # if date is None
        # И мне кажется более понятным такое форматирование кода
        # self.date = (
        #     dt.datetime.now().date() if date is None
        #     else dt.datetime.strptime(date, '%d.%m.%Y').date()
        # )
        #
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment

# Можно оптимизировать методы get_today_stats и get_week_stats, внеся так же изменения в метод add_record.
# Если при добавлении записи проверять дату записи, и располагать объекты Record в списке records по возрастанию даты,
# то это немного замедлит добавление данных. Но позволит существенно повысить скорость работы метода get_today_stats
# таким образом: проходиться по списку records надо будет с конца к началу
# for record in self.records[::-1]
# и как только record.date будет меньше сегодняшней даты для метода get_today_stats или меньше сегодняшней даты - 7 для
# метода get_week_stats, то можно будет выходить из цикла и не рассматривать записи, которые не подходят по дате.
# предыдущее изменение add_record будет гарантировать, что никакие данные не будут пропущены
# текущая реализация проверяет каждую запись на то подходит она по дате, или нет.
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Имя переменной следует писать с маленькой буквы: record.
        for Record in self.records:
            # Нарушена консистентность
            # В этом и следующем методе отличается подход в таком моменте:
            # Здесь dt.datetime.now().date() создается при каждой проверке
            # В методе get_week_stats() использована переменная today = dt.datetime.now().date()
            # Второй вариант лучше по скорости выполнения, так как в первом создается объект при каждом сравнении,
            # во втором варианте создается единожды и используется для всех проверок.
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Можно сократить до if 7 > (today - record.date).days >= 0:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Бэкслеш ('\') лучше не использовать для переноса
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Хорошие были времена.. :)
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    # Хорошая идея дать возможность использовать нестандартный курс.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Эта строка не делат ничего, так как проверяет равно ли cash_remained единице все условного оператора
            # Видимо, хотелось написать cash_remained /= 1.00, чтобы выглядело одинаково, но это, пожалуй, лишнее
            cash_remained == 1.00
            currency_type = 'руб'
        # Здесь можно вставить пустую строку, чтобы логически разделить два блока кода с условиями, и они не сливались
        # между собой
        if cash_remained > 0:
            # в f-строках лучше не использовать функции, а только подставлять переменные. Округлить следовало заранее
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Нарушена консистентность
            # Использованы разные способы подстановки переменных. До этого f-строка, а тут функция format.
            # Так же разные способы округления. Первый был математический, а этот просто отрезает лишние цифры.
            # Бэкслеш ('\') лучше не использовать для переноса
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Этот метод излишен, так как просто вызывает метод родительского класса.
    def get_week_stats(self):
        super().get_week_stats()
