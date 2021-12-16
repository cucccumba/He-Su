# He-Su

## Поэтапное описание протокола He-Su

![image](https://user-images.githubusercontent.com/95577144/146212949-5f28fa79-0978-4440-9c13-c25146547d45.png)

## Описание кода реализации протокола

### He-Su/src/utils/hesugen.py 

================================
##### def generate_large_prime(keysize=1024)

Генерирует большое простое число размером в keysize битов.

Aргументы:
1. keysize - параметр размера генерируемого простого числа.

Возвращаемое значение: простое число.

================================
##### def generate_keys(key_size)

Генерирует два ключа из простых чисел размером в keysize битов: public_key = (n, e), private_key = (n, d) - открытый b закрытый с помощью алгоритма RSA для пользователя.
Шаг протокола: 1.1

Aргументы:
1. keysize - параметр размера генерируемых ключей.

Возвращаемое значение: два ключа RSA public_key, private_key.

================================
##### def get_mask_factor()

Генерирует случайное число (маскирующий множитель)
Шаг протокола: 1.2

Возвращаемое значение: маскирующий множитель.

================================

### He-Su/src/utils/hesuutils.py 

================================
##### def huhash(x)

Вычисляет hash-функцию hash(x) % 200. hash(x) - функция из стандартной библиотеки.

Возвращаемое значение: hash(x) % 200.

================================

##### def mod_exp(base, exponent, modulus)

Вычисляет base^exponent % modulus - модульное возведение в степерь.
http://en.wikipedia.org/wiki/Modular_exponentiation#Right-to-left_binary_method

Aргументы:
1. base - число, возводимое в степень exponent.
2. exponent - степень возведения.
3. modulus - модуль.

Возвращаемое значение: число - результат возведения.

================================
##### def egcd(a, b)

Реализация расишренного алгоритма евклида - находит целые числа HOД(a,b), c, d: HOД(a,b) = ca + bd

Aргументы:
1. a,b - натуральные числа.

Возвращаемое значение: HOД(a,b), c, d

================================
##### def mmi(a, m)
Возвращает a^-1 по модулю m ??????????????

Aргументы:
1. a,m - натуральные числа.

Возвращаемое значение: a^-1 - число

================================
##### def gcd(a, b)

НЕ ИСПОЛЬЗУЕТСЯ
Считает НОД(a,b)

Aргументы:
1. a,b - натуральные числа.

Возвращаемое значение: HOД(a,b)

================================
##### def find_mod_inverse(a, m)

НЕ ИСПОЛЬЗУЕТСЯ
Возвращает a^-1 по модулю m

Aргументы:
1. a,m - натуральные числа.

Возвращаемое значение: a^-1 - число

================================

##### def rabin_miller(num)

Вероятностный тест Миллера-Рабина, проверяющий число на простоту

Aргументы:
1. num - натуральное число.

Возвращаемое значение: true если простое, false - иначе 

================================

##### def is_prime(num)

Проверяет число на простоту. Если num < 1000, ищет в списке простых до 1000, иначе использует вероятностный тест Миллера-Рабина

Aргументы:
1. num - натуральное число.

Возвращаемое значение: true если простое, false - иначе 

================================

### He-Su/src/hesu/hesuadmin.py  

#### class Admin(object)

Класс, описывающий администратора.

Поля класса:
1. public_key - открытый RSA ключ администратора
2. private_key - закрытый RSA ключ администатора
3. auth_voters - массив зарегистрированных голосующих

================================
##### def sign(self, auth, name)

Проверяет приемлимость избирателя, подписывает принятое сообщение избирателя, отправляет результат избирателю
Шаги протокола: 2.1 - 2.3

Aргументы:
1. self - поля класса
2. auth - значение сообщения избирателя (пункт 1.3)
3. name - имя избирателя

Возвращаемое значение: подписанное принятое сообщение для избирателя

================================

### He-Su/src/hesu/hesuvoter.py  

#### class Voter(object)

Класс, описывающий избирателя.

Поля класса:
1. name
2. public_key - открытый RSA ключ администратора
3. private_key - закрытый RSA ключ администатора
4. mask_factor - маскирующий множитель
5. public_adm_key - публичный ключ администратора
6. signed_public_key - подписанный администратором публичный ключ избирателя
7. hash_key - huhash(self.public_key)
8. secret_key - секретный ключ избирателя

================================
##### def authorization(self)

Авторизация избирателя - генерация и отправка первого сообщения администратору
Шаги протокола: 1.3, 1.4

Aргументы:
1. self - поля класса

Возвращаемое значение: авторизационное сообщение для администратора

================================
##### def get_signed_key(self, sign)

Вычисляет подписанный self.signed_public_key ключ администратора, убирает маскирующий множитель, проверяет все на правильность. 
Отправляет открытый ключ self.public_key избирателя и подписанный ключ администратора счетчику
Шаги протокола: 3-4

Aргументы:
1. self - поля класса

Возвращаемое значение: self.public_key, self.signed_public_key

================================
##### def make_vote(self, vote, secret_key)

Вычисляет и послылает счетчику подписанный бюллетень, зашифрованный бюллетень, также посылает ему открытый ключ избирателя 
Шаги протокола: 3-4

Aргументы:
1. self - поля класса
2. vote - бюллетень
3. secret key - секретный ключ избирателя

Возвращаемое значение: self.public_key, encrypt_vote, sign_vote

================================
##### def confirm_vote(self)

Вычисляет sign - подпись, позволяющую счетчику вычислить и учесть бюллетень. Отправляет счетчику открытый и секретный ключи избирателя и sign.
Шаги протокола: 9

Aргументы:
1. self - поля класса

Возвращаемое значение: self.public_key, self.secret_key, sign

### He-Su/src/hesu/hesucounter.py

#### class Counter(object)

Класс, описывающий счетчик голосов.

Поля класса:
1. public_adm_key - открытый ключ администратора
2. auth_keys - список ключей зарегистрированных избирателей
3. secret_key - секретный ключ
4. votes - список голосов

================================
##### def registrate(self, pair)

Проверяет подписанный ключ избирателя, регистрирует голосующуего избирателя
Шаги протокола: 5

Aргументы:
1. self - поля класса
2. pair - открытый ключ и подписанный администратором ключи избирателя

Возвращаемое значение: 1, если избиратель зарегистрирован

================================
##### def generate_secret_key(self)

Генирирует секретный ключ для симметричного шифрования с избирателем

Aргументы:
1. self - поля класса

Возвращаемое значение: секретный ключ

================================
##### def public_vote(self, vote)

Проверяет ключ избирателя, голос избирателя, если все ок - заносит запись о голосе избитрателя в лист голосов, чтобы избиратель мог ее проверить.
Шаги протокола: 7

Aргументы:
1. self - поля класса
2. vote - открытый ключ и зашифрованная бюллетень, подписанная бюллетень 

Возвращаемое значение: 1, если голос занесен

================================
##### def public_final_vote(self, confirm)

Проверяет, что бюллетень можно получить, если все ок - находит бюллетень и публикует.
Шаги протокола: 7

Aргументы:
1. self - поля класса
2. сonfirm - открытый ключ и секретный ключ, подписанный секретный ключ избирателя 

Возвращаемое значение: 1, если голос занесен

================================



## Описание кода для тестировки протокола

### He-Su/src/hesuuser.py 

#### class VotingController(object)

Класс, контролирующий голосование.

Поля класса:
1. key_gen_num - размер ключей
2. admin_keys - ключи админа
3. admin - экземпляр класса Admin - администратор голосования
4. voter_count - количество проголосовавших
5. counter - экземпляр класса Counter - счетчик голосования

================================
##### def vote(self, voter_name, test_type = 'normal')

НЕАКТУАЛЬНАЯ ФУНКЦИЯ
Проводит всю процедуру голосования для voter_name голосующуго

Aргументы:
1. self - поля класса
2. voter_name - имя голосующуго
3. test_type - тип теста 
 test_types = [NORMAL_TEST_TYPE, VOTER_ALREADY_REGISTERED_TEST_TYPE, VOTER_KEY_FAILED_TEST_TYPE,
              REGISTRATION_FAILED_TEST_TYPE, PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_TEST_TYPE,
              PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_TEST_TYPE, FINAL_VOTE_FAILED_TEST_TYPE]

Возвращаемое значение: Response - класс boolean значений, говорящий, какие этапы прошли успешно и несущий сообщение об ошибке, если оно есть:

class Response(object):
    is_admin_sign_ok = False
    is_registration_ok = False
    is_public_vote_ok = False
    is_final_vote_ok = False
    is_voter_key_signed_ok = False
    err = ''

================================
##### def main_block(self, test_type, voter, voter_name)

Проводит всю процедуру голосования для voter c voter_name избирателя

Aргументы:
1. self - поля класса
2. voter - экземпляр класса Voter - избиратель
3. voter_name - имя голосующуго
4. test_type - тип теста 
 test_types = [NORMAL_TEST_TYPE, VOTER_ALREADY_REGISTERED_TEST_TYPE, VOTER_KEY_FAILED_TEST_TYPE,
              REGISTRATION_FAILED_TEST_TYPE, PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_TEST_TYPE,
              PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_TEST_TYPE, FINAL_VOTE_FAILED_TEST_TYPE]

Возвращаемое значение: Response - класс boolean значений, говорящий, какие этапы прошли успешно и несущий сообщение об ошибке, если оно есть:

class Response(object):
    is_admin_sign_ok = False
    is_registration_ok = False
    is_public_vote_ok = False
    is_final_vote_ok = False
    is_voter_key_signed_ok = False
    err = ''

================================
##### def test_all(self)

Генерирует по voter для каждого теста, проводит все тесты.

Функции тестов
1. def test_normal(self, voter_name)
2. def test_voter_already_registered(self, voter_name)
3. def test_voter_key_failed(self, voter_name)
4. def test_registration_failed(self, voter_name)
5. def test_public_vote_auth_key_hash_failed(self, voter_name)
6. def test_public_vote_auth_key_not_present(self, voter_name)
7. def test_final_vote_failed(self, voter_name)

Соответствующие типы исключений:
exception_types = [NO_EXCEPTION, 
                   VOTER_ALREADY_REGISTERED_EXCEPTION, 
                   VOTER_KEY_FAILED_EXCEPTION,
                   REGISTRATION_FAILED_EXCEPTION, 
                   PUBLIC_VOTE_AUTH_KEY_HASH_FAILED_EXCEPTION,
                   PUBLIC_VOTE_AUTH_KEY_NOT_PRESENT_EXCEPTION, 
                   FINAL_VOTE_FAILED_EXCEPTION]
                   
Возвращаемого значения нет, только exception или print в случае ошибок

================================

### He-Su/src/test/test.py 

##### def load_test(test_num = 100)

Генерирует test_num голосов и замеряет время работы протокола при их учете.

Aргументы:
1. test_num - количество голосов для замера времени

Возвращаемое значение: отсутствует
Печатает время работы.
