# Практика 2. Rest Service

## Программирование. Rest Service. Часть I

### Задание А (3 балла)
Создайте простой REST сервис, в котором используются HTTP операции GET, POST, PUT и DELETE.
Предположим, что это сервис для будущего интернет-магазина, который пока что умеет 
работать только со списком продуктов. У каждого продукта есть поля: `id` (уникальный идентификатор),
`name` и `description`. 

Таким образом, json-схема продукта (обозначим её `<product-json>`):

```json
{
  "id": 0,
  "name": "string",
  "description": "string"
}
```

Данные продукта от клиента к серверу должны слаться в теле запроса в виде json-а, **не** в параметрах запроса.

Ваш сервис должен поддерживать следующие операции:
1. Добавить новый продукт. При этом его `id` должен сгенерироваться автоматически
   - `POST /product`
   - Схема запроса:
     ```json
     {
       "name": "string",
       "description": "string"
     }
     ```
   - Схема ответа: `<product-json>` (созданный продукт)
2. Получить продукт по его id
   - `GET /product/{product_id}`
   - Схема ответа: `<product-json>`
3. Обновить существующий продукт (обновляются только те поля продукта, которые были переданы в теле запроса)
   - `PUT /product/{product_id}`
   - Схема запроса: `<product-json>` (некоторые поля могут быть опущены)
   - Схема ответа: `<product-json>` (обновлённый продукт)
4. Удалить продукт по его id
   - `DELETE /product/{product_id}`
   - Схема ответа: `<product-json>` (удалённый продукт)
5. Получить список всех продуктов 
   - `GET /products`  
   - Схема ответа:
     ```
     [ 
       <product-json-1>,
       <product-json-2>, 
       ... 
     ]
     ```

Предусмотрите возвращение ошибок (например, если запрашиваемого продукта не существует).

Вы можете положить код сервиса в отдельную директорию рядом с этим документом.

### Задание Б (3 балла)
Продемонстрируйте работоспособность сервиса с помощью программы Postman
(https://www.postman.com/downloads) и приложите соответствующие скрины, на которых указаны
запросы и ответы со стороны сервиса для **всех** его операций.

#### Демонстрация работы
1) Добавление продукта
    ```json
     {
        "name": "мед",
        "description": "супер вкусный мед"
     }
     ```
   ![](./images/1.png)
2) Проверка метода GET
   ![](./images/2.png)
3) Меняем описание у продукта с id=1 на "супер мега вкусный мед!!!!!"
   ![](./images/3.png)
4) Добавляем еще два продукта
   ```json
    {
        "name": "чернослив",
        "description": "черный как арабская ночь"
    }
     ```
   ```json
    {
        "name": "яблоки карамелька",
        "description": "очень сладкие"
    }
     ```
5) Проверяем список всех продуктов 
   ![](./images/4.png)
6) Удаляем чернослив с id=2
   ![](./images/5.png)
7) Проверяем список всех продуктов 
   ![](./images/6.png)
8) Получаем ошибку, если запросили продукт, которого нет
   ![](./images/7.png)

### Задание В (4 балла)
Пусть ваш продукт также имеет иконку (небольшую картинку). Формат иконки (картинки) может
быть любым на ваш выбор. Для простоты будем считать, что у каждого продукта картинка одна.

Добавьте две новые операции:
1. Загрузить иконку:
   - `POST product/{product_id}/image`
   - Запрос содержит бинарный файл — изображение  
     <img src="images/post-image.png" width=500 />
2. Получить иконку:
   - `GET product/{product_id}/image`
   - В ответе передаётся только сама иконка  
     <img src="images/get-image.png" width=500 />

Измените операции в Задании А так, чтобы теперь схема продукта содержала сведения о загруженной иконке, например, имя файла или путь:
```json
"icon": "string"
```

#### Демонстрация работы
Добавляем продукт мед, добавляем ему картинку, потом получаем эту же картинку.
![](./images/C1.png)
![](./images/C2.png)
![](./images/C3.png)
![](./images/C4.png)

---

_(*) В последующих домашних заданиях вам будет предложено расширить функционал данного сервиса._

## Задачи

### Задача 1 (2 балла)
Общая (сквозная) задержка прохождения для одного пакета от источника к приемнику по пути,
состоящему из $N$ соединений, имеющих каждый скорость $R$ (то есть между источником и
приемником $N - 1$ маршрутизатор), равна $d_{\text{сквозная}} = N \dfrac{L}{R}$
Обобщите данную формулу для случая пересылки количества пакетов, равного $P$.

#### Решение
По сути задержка равна времени через сколько 
последний пакет окажется в месте назначения. Эта велечина состоит из двух: 
- времени ожидания пока остальные пакеты освободят первое соединение $ = (P - 1) \dfrac{L}{R}$
- задержка прохождения этого пакета от источника к приемнику  $ = d_{\text{сквозная}} = N \dfrac{L}{R}$

**Ответ** $$ (P - 1 + N) \frac{L}{R} .$$ 

### Задача 2 (2 балла)
Допустим, мы хотим коммутацией пакетов отправить файл с хоста A на хост Б. Между хостами установлены три
последовательных канала соединения со следующими скоростями передачи данных:
$R_1 = 200$ Кбит/с, $R_2 = 3$ Мбит/с и $R_3 = 2$ Мбит/с.
Сколько времени приблизительно займет передача на хост Б файла размером $5$ мегабайт?
Как это время зависит от размера пакета?

#### Решение
Задержка аддитивна по каналам. Если не учитывать задержку обработки, ожидания и распространения:

$$L\sum\frac{1}{R_i} = 40000 \left(\frac{1}{200} + \frac{1}{3000} + \frac{1}{2000}\right) \approx 233,33$$
, все переведено в килобиты.

**Ответ** 233,33. 

### Задача 3 (2 балла)
Предположим, что пользователи делят канал с пропускной способностью $2$ Мбит/с. Каждому
пользователю для передачи данных необходима скорость $100$ Кбит/с, но передает он данные
только в течение $20$ процентов времени использования канала. Предположим, что в сети всего $60$
пользователей. А также предполагается, что используется сеть с коммутацией пакетов. Найдите
вероятность одновременной передачи данных $12$ или более пользователями.

#### Решение
Будем считать, что человек в каждый момент использует канал с вероятностью 0.2 и что люди независимы.
Рассмотрим конкретный момент, вероятность того, что сумма 60 Бернуллевских величин хотя бы $12 = \mathbb{E}\sum B_i(0.2)$ по ЦПТ около $\frac{1}{2}$.

**Ответ** 0,5. 

### Задача 4 (2 балла)
Пусть файл размером $X$ бит отправляется с хоста А на хост Б, между которыми три линии связи и
два коммутатора. Хост А разбивает файл на сегменты по $S$ бит каждый и добавляет к ним
заголовки размером $80$ бит, формируя тем самым пакеты длиной $L = 80 + S$ бит. Скорость
передачи данных по каждой линии составляет $R$ бит/с. Загрузка линий мала, и очередей пакетов
нет. При каком значении $S$ задержка передачи файла между хостами А и Б будет минимальной?
Задержкой распространения сигнала пренебречь.

#### Решение
Нужно минимизировать по $S$ выражение из 1 задания, где $P = \frac{X}{S}$ пакетов, $N = 3$ соединений и $L = 80 + S$.
$$
(P - 1 + N) \frac{L}{R} = 
\left(\frac{X}{S} + 2\right) \frac{S + 80}{R} \sim
X + \frac{80X}{S} + 2S + 160.
$$
Минимум $\frac{80X}{S} + 2S$ достигается при $S = \sqrt{40x}$ по неравенству о средних.

**Ответ** $\sqrt{40X}$.

### Задание 5 (2 балла)
Рассмотрим задержку ожидания в буфере маршрутизатора. Обозначим через $I$ интенсивность
трафика, то есть $I = \dfrac{L a}{R}$.
Предположим, что для $I < 1$ задержка ожидания вычисляется как $\dfrac{I \cdot L}{R (1 – I)}$. 
1. Напишите формулу для общей задержки, то есть суммы задержек ожидания и передачи.
2. Опишите зависимость величины общей задержки от значения $\dfrac{L}{R}$.

#### Решение
1. $d = \dfrac{I \cdot L}{R (1 – I)} + \dfrac{L}{R} = \dfrac{L}{R(1 - I)}$.
2. Видно, что $d$ зависит линейно от $\dfrac{L}{R}$. При этом коэффициент зависит от близости интенсивности к 1.
