import requests
from tqdm.notebook import tqdm_notebook as tqdm_
import time

import ipywidgets as widgets
from IPython import display as dsp

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def work(progress):
  print('Выбор бонуса')
  total = 100
  for i in range(total):
      time.sleep(0.05)
      progress.value = float(i+1)/total

def Start_levels(idx):
    dsp.clear_output(wait=True)
    url='https://d5dttm7ipl4ef12lussv.apigw.yandexcloud.net'
    res_url='/numbers'    
    res_save= '/save'
    res = requests.get(f'{url}{res_url}', params={'idx': idx})
    progress = widgets.FloatProgress(value=0.0, min=0.0, max=1.0)
    presents=['']
    cost=0
    if idx==-1:
        presents = ['5 zoom консультаций',
                    '10 zoom консультаций',
                    '20 zoom консультаций',
                    '1 стажировка (3 месяца)',
                    '2 стажировки (6 месяцев)',
                    '4 стажировки (12 месяцев)',
                    'Курс по трейдингу (6 занятий) + стажировка',
                    'Курс по обработке данных и алгоритмам (14 занятий)',
                    'Курс по PyTorch (10 занятий)',
                    'Выкуп стоимости обучения',
                    'Скидка 5.000 рублей',
                    'Скидка 10.000 рублей',
                    'Скидка 20.000 рублей',]
        cost = [9500, 14900, 29800, 14900, 24900, 39900, 39900, 39900, 39900, 39900, 5000, 10000, 20000]    
    elif idx==0:
        presents = ['Выкуп стоимости',
                    '5 zoom консультаци',
                    '10 zoom консультации',
                    'Бонусы - 5.000р',
                    'Бонусы - 10.000р',
                    '1 стажировка',]
        cost = [39900, 9500, 14900, 5000, 10000, 14900]    
    elif idx==1:
        presents = ['Курс на выбор',
                    'Выкуп стоимости',
                    '5 zoom консультаци',
                    '10 zoom консультации',
                    '20 zoom консультации',
                    'Бонусы - 5.000р',
                    'Бонусы - 10.000р',
                    'Бонусы - 20.000р',
                    '1 стажировка',
                    '2 стажировки',]
        cost = [39900, 39900, 9500, 14900, 29800, 5000, 10000, 20000, 14900, 24900]
    elif idx==2:
        presents = ['Курс на выбор',                    
                    '5 zoom консультаци',
                    '10 zoom консультации',
                    '20 zoom консультации',
                    'Бонусы - 5.000р',
                    'Бонусы - 10.000р',
                    'Бонусы - 20.000р',
                    '1 стажировка',
                    '2 стажировки',]
        cost = [39900, 9500, 14900, 29800, 5000, 10000, 20000, 14900, 24900]

    current_variant =  [int(value)  for value in res.json().values()]
    bonuses = []
    num_bonus = 1
    print(f'{bcolors.BOLD}Готовимся выбирать бонусы...{bcolors.ENDC}')
    time.sleep(1)
    current_cost = 0
    for i, elem in enumerate(current_variant):
        if elem:          
          #for _ in tqdm_(range(60), desc=f'Выбор бонуса №{num_bonus}', ncols=500):
          #    time.sleep(0.05)
          dsp.display(progress)
          work(progress)
          num_bonus+=1
          current_cost += cost[i]
          current_present = f'{bcolors.OKBLUE}Бонус:{bcolors.ENDC} {presents[i]} ({cost[i]} руб.)'
          print(current_present)
          time.sleep(1)
          dsp.clear_output(wait=True)
          bonuses.append(f'{presents[i]} ({cost[i]} руб)')
          print(f'{bcolors.BOLD}Готовимся выбирать бонусы...{bcolors.ENDC}')
          print(f'{bcolors.OKGREEN}{bcolors.BOLD}Поздравляем!', end=' ')
          print(f'Ваш список бонусов:{bcolors.ENDC}')
          for b in bonuses:    
              print(f'- {b}')
    print()
    print(f'{bcolors.UNDERLINE}Вам выпало бонусов на {current_cost} руб.{bcolors.ENDC}')
    print()
    print()
    print(f'Вам нравится такой бонус?')
    print(f'Напиши {bcolors.BOLD}Забронировать{bcolors.ENDC}, чтобы сохранить бонусы за собой')
    print(f'Напиши {bcolors.BOLD}Заново{bcolors.ENDC}, чтобы запустить {bcolors.UNDERLINE}{bcolors.OKBLUE}колесо удачи{bcolors.ENDC} снова')
    ans = input()
    while 1:      
      if ans.lower() == 'забронировать':
        dsp.clear_output(wait=True)
        print(f'{bcolors.OKGREEN}{bcolors.BOLD}Поздравляем!', end=' ')
        print(f'Ваш список бонусов:{bcolors.ENDC}')
        for b in bonuses:    
            print(f'- {b}')
        print()
        print(f'{bcolors.UNDERLINE}Вам выпало бонусов на {current_cost} руб.{bcolors.ENDC}')
        res_save= '/save'
        url='https://d5dttm7ipl4ef12lussv.apigw.yandexcloud.net'
        print('\nВведите, пожалуйста, свои данные:')
        name = input('Имя:')
        mail = input('e-mail:')
        phone = input('Телефон:')
        res = requests.post(f'{url}{res_save}', params={'idx':idx,'email': mail, 'name':name, 'phone': phone, 'bonus': "• "+ "\n• ".join(bonuses)})
        print()
        if res.status_code==200:    
          print(f'{bcolors.HEADER}Отлично, эти подарки теперь забронированы за вами!')
          print('Скоро мы вам позвоним :)')
        else:
          res = requests.post(f'{url}{res_save}', params={'idx':idx, 'email': mail, 'name':name, 'phone': phone, 'bonus': "• "+ "\n• ".join(bonuses)})
          if res.status_code==200:    
            print(f'{bcolors.HEADER}Отлично, эти подарки теперь забронированы за вами!')
            print('Скоро мы вам позвоним :)')
          else:
            res = requests.post(f'{url}{res_save}', params={'idx':idx, 'email': mail, 'name':name, 'phone': phone, 'bonus': "• "+ "\n• ".join(bonuses)})
            if res.status_code==200:    
              print(f'{bcolors.HEADER}Отлично, эти подарки теперь забронированы за вами!')
              print('Скоро мы вам позвоним :)')
            else:
              print(f'{bcolors.FAIL}Ошибка сервера! Обратитесь, пожалуйста, к менеджерам УИИ')
        return
      elif ans.lower()=='заново':
        Start_levels(idx)
        return
      else:
        ans = input('Ответ не распознан. введите Забронировать или Заново\n')