'''
    Сформировать последовательность Фиббоначи, количество значений в которой
    лимитировано вводимым натруральным числом N.
'''

def fib_rec(N=7, f=[]):

    count = 1
    if N > count:
        fib_rec(N-1)
    if N <= 2:
        f.append(1)
    else:
        f.append(f[N-3] + f[N-2])

    return f
    

def fib_rec2(N=7, f=[]):

    f.append(f[-1] + f[-2]) if len(f) > 1 else f.append(1)
    return f if len(f) == N else fib_rec2(N, f)




def fib_rec3(N=7, f=[1, 1]):
    if len(f) < N:
        f.append(f[-1] + f[-2])
        fib_rec3(N, f)

    return f


'''
    Имеется следующий многомерный список: d = [1, 2, [True, False], ["Москва", "Уфа", [100, 101], ['True', [-2, -1]]], 7.89]
    С помощью рекурсивной функции get_line_list создать на его основе одномерный список из значений элементов списка d. 
    Функция должна возвращать новый созданный одномерный список.
'''

d = [1, 2, [True, False], ["Москва", "Уфа", [100, 101], ['True', [-2, -1]]], 7.89]

def get_line_list(d,a=[]):
    for item in d:
        if isinstance(item, list):
            get_line_list(item)
        else:
            a.append(item)
    return a

f = get_line_list(d)


'''
    Лягушка прыгает вперед и может скакнуть либо на одно деление, либо сразу на два. 
    Наша задача определить количество вариантов маршрутов, которыми лягушка может достичь риски под номером N (натуральное число N вводится с клавиатуры).
    Решать задачу следует с применением рекурсивной функции. Назовем ее get_path. Алгоритм решения будет следующий. Рассмотрим, например, риску под номером 4. 
    Очевидно, в нее лягушка может скакнуть либо с риски номер 2, либо с риски номер 3. Значит, общее число вариантов перемещений лягушки можно определить как:
    get_path(4) = get_path(3) + get_path(2)

    Аналогично будет справедливо и для любой риски N:
    get_path(N) = get_path(N-1) + get_path(N-2)

    А начальные условия задачи, следующие:
    get_path(1) = 1
    get_path(2) = 2

    Реализуйте такую рекурсивную функцию, которая должна возвращать количество вариантов перемещений лягушки для риски под номером N.
'''


def get_path(n=6):

    if n in (1, 2):
        return n
    else:
        return get_path(n-1) + get_path(n-2)

    # just another form of writing as above.
    # return n if n in (1, 2) else get_path(n - 1) + get_path(n - 2)    


print(get_path())
