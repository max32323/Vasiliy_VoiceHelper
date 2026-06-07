import string

syms = '!@#$%^&*()-—_=+№%[]{},.<>?;:"\\|\\\\`~–'
nums = '1234567890'
end_syms = string.ascii_lowercase + string.ascii_uppercase
dumb_passwords = [
    "password", "123456", "123456"[::-1], "qwerty", "111111", "abc123",
    "monkey", "letmein", "abcdef", "abcdef"[::-1], "iloveyou", "admin",
    "welcome", "1234", "password1", "qwerty123", "123123", "123123"[::-1],
    "sunshine", "charlie", "aa123456", "1q2w3e4r", "password123",
    "dragon", "qwertyuiop", "princess", "azerty", "trustno1",
    "football", "123321", "1q2w3e", "1qaz2wsx", "loveyou",
    "1qazxsw2", "123qwe", "qwert", "ilovepassword", "12345678", "12345678"[::-1],
    "superman", "welcome1", "qazwsx", "asdfgh", "qwerty1234",
    "password0", "12345", "12345"[::-1], "mysecurepassword", "1qaz2wsx3edc", "qwerty12345",
    "letmein123", "1234567890", "hello", "welcome123", "passw0rd", '123', "1234567890"[::-1]
]


# while True:
#     password = input('Введите ваш пароль(без пробелов): ').strip()
#     if len(password) != 0 and len(password) > 2:
#         break
#     print('Пожалуйста введите нормальный пароль!')

def check(password):
    global dumb_passwords
    global syms
    global nums
    global end_syms
    b_nums = False
    b_syms = False
    b_end_syms = False
    len_syms = {}
    for i in password:
        len_syms[i] = password.count(i)
        if i in nums:
            b_nums = True
        elif i in syms:
            b_syms = True
        elif i in end_syms:
            b_end_syms = True
        if b_syms and b_nums:
            break
    len_syms = max(len_syms.values())  # Сколько макс. повторений символа

    if password.lower() in dumb_passwords:
        return False

    # Лёгкий
    elif ((password.islower() or password.isupper()) or ((not b_nums or not b_syms) or (b_nums or b_syms))) and (
            3 <= len(password) <= 5):
        if (b_nums and b_syms) and not (password.islower() or password.isupper()) and (len_syms < 2):
            return True
        elif (b_nums and b_syms) and (len_syms < 2):
            return True
        elif b_nums or b_syms:
            return False

        else:
            return False

    # Средняк
    elif ((b_nums and not b_syms) or (not b_nums and b_syms) or (b_nums or b_syms)) and (5 <= len(password) <= 13):
        if len_syms < 4 and b_end_syms:
            return True
        else:
            return False
    # Шик
    elif (b_nums and b_syms) and (13 <= len(password) <= 20):
        if len_syms < 8 and b_end_syms:
            return True
        else:
            return False
    else:
        if ((password.islower() or password.isupper()) or (not b_nums or not b_syms)) and (5 <= len(password) <= 20):
            return False
        else:
            return False

# print(check_password(password))