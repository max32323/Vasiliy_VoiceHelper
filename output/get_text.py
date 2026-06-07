import g4f
import string

def russian():
    russian_letters = ''.join(chr(i) for i in range(1040, 1104))  # А-Я, а-я

    digits = string.digits
    a = "'"
    special_characters = '1234567890!@#$%^&*()-—_=+№%[]{},.<>?;:"\\|\\\\`~–' + a + ' ' + 'ё' + 'ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba•'
    result_string = russian_letters + digits + special_characters
    return result_string

b = True

def GPT_answer(text: str):
    global b
    while True:
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": (
                f"Ты помощник который даёт чёткие ответы, делай ответ от 1-ого лица. Главное чтобы твой ответ не превышал 300 символов, а также был на русском языке и быз лишних пробелов! Также сделай ответ от 1-ого лица, без подробностей!")},
                      {"role": "user", "content": f'Чёткий ответ для слайда презентации до 300 символом только по теме на русском языке, без доп символов и описания количества слов: {text}'}],
        )
        if str(response) == '' or str(response) == '流量异常,请尝试更换网络环境' or str(response) == 'Model not found or too long input. Or any other error (xD)' or response == 'Too many messages in a row' or response == 'Request ended with status code 404' or response == 'No message received':
            pass
        elif str(response) == 'sorry, 您的ip已由于触发防滥用检测而被封禁,本服务网址是https://chat18.aichatos8.com 或者 https://cat.chatavx.com/ 如果你不在本网站，请前往本网站使用即可 如需合作接口调用请联系微信kelemm220 或者前往 https://binjie09.shop 自助购买key, 认为是误封需要解封的请前往https://www.ip.cn/ 查询ip信息,并发送信息至邮件 gpt33@binjie.site ，站长会定期看邮件并处理解封和合作问题，如需调用接口请见接口文档https://apifox.com/apidoc/shared-803d9df6-a071-4b3e-9d69-ea1281614d82，如需合作接口调用请联系微信chatkf123 或者前往 https://cat.chatavx.com/  注册使用（可付费使用gpt4 注册可免费使用3.5）' or "sorry" in response:
            pass
        elif len(str(response))>=350:
            pass
        else:
            return response

#print(GPT_answer('Виды цветов'))







# import g4f
# import string
#
# def russian():
#     russian_letters = ''.join(chr(i) for i in range(1040, 1104))  # А-Я, а-я
#
#     digits = string.digits
#     a = "'"
#     special_characters = '1234567890!@#$%^&*()-—_=+№%[]{},.<>?;:"\\|\\\\`~–' + a + ' ' + 'ё' + 'ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba•'
#     result_string = russian_letters + digits + special_characters
#     return result_string
#
# b = True
#
# def GPT_answer(text: str):
#     global b
#     while True:
#         response = g4f.ChatCompletion.create(
#             model="gpt-4",
#             messages=[{"role": "system", "content": (
#                 f"Ты помощник который даёт чёткие ответы, делай ответ от 1-ого лица. Главное чтобы твой ответ не превышал 300 символов, а также был на русском языке и быз лишних пробелов! Также сделай ответ от 1-ого лица, без подробностей!")},
#                       {"role": "user", "content": f'Чёткий ответ до 300 символом только по теме на русском языке: {text}'}],
#         )
#         if str(response) == '' or str(response) == '流量异常,请尝试更换网络环境' or str(response) == 'Model not found or too long input. Or any other error (xD)' or response == 'Too many messages in a row' or response == 'Request ended with status code 404' or response == 'No message received':
#             pass
#         elif str(response) == 'sorry, 您的ip已由于触发防滥用检测而被封禁,本服务网址是https://chat18.aichatos8.com 或者 https://cat.chatavx.com/ 如果你不在本网站，请前往本网站使用即可 如需合作接口调用请联系微信kelemm220 或者前往 https://binjie09.shop 自助购买key, 认为是误封需要解封的请前往https://www.ip.cn/ 查询ip信息,并发送信息至邮件 gpt33@binjie.site ，站长会定期看邮件并处理解封和合作问题，如需调用接口请见接口文档https://apifox.com/apidoc/shared-803d9df6-a071-4b3e-9d69-ea1281614d82，如需合作接口调用请联系微信chatkf123 或者前往 https://cat.chatavx.com/  注册使用（可付费使用gpt4 注册可免费使用3.5）' or "sorry" in response:
#             pass
#         elif len(str(response))>=350:
#             pass
#         else:
#             print('Прошёл 1 этап')
#             r = russian()
#             t = ''
#             for i in response:
#                 if i == '#' or i == '*':
#                     pass
#                 else:
#                     t += i
#             print(response)
#             for i in t[:-1]:
#                 if i in r:
#                     b = True
#                 else:
#                     print(i)
#                     b = False
#                     break
#             print(f'Прошёл 2 этап {b}')
#             if b:
#                 if 'Извините' in t.capitalize() or 'Простите' in t.capitalize() or 'Прости' in t.capitalize() or 'Извини' in t.capitalize():
#                     pass
#                 else:
#                     return t
#             else:
#                 pass
#
# #print(GPT_answer('Виды цветов'))