# MAPY

DSL для перевода псевдокода в LaTeX и Python.

## Что полезного делает DSL во внешнем мире?

![Диаграмма использования](http://www.plantuml.com/plantuml/svg/dP0nIiH058RxESKhJJ4vm23B7i32mi9sSMVTm9g1-2o4BIGBMhg5bI0s7Y2kYGpHv0p_tCWVj12qKQPwytt_6-QVdkkiqekpbLdvXOe6gOhJfSgygFo95g4q3ayvjZaUSYVMhYVYiCKkrHZJbJFV1s8xaJqyfWsUyOQ87aswHaotWeONBw36iSOxHkooNzDtH7tQKEama4L6AAF1m3EY4-frkg7oYXQK4D5bvjz9sLzRouVlgRIPAOFwhnB2uY-_4IS7ioD__6F3vsBYmqjTij6fB-Ti_0C0)

## Как называется DSL?

![MAPY = Mathematics Algorithm PYthon](https://latex.codecogs.com/svg.latex?\mathtt{MAPY}%20\quad%20=%20\quad%20\mathtt{M}\mathrm{athematics}%20\quad%20\mathtt{A}\mathrm{lgorithm}%20\quad%20\mathtt{PY}\mathrm{thon})

## Результаты

Скоро...

## Получение кода
```cmd
git clone https://github.com/...
```

## Установка зависимостей
Нужно установить все зависимости:
```cmd
pip install -r requirements.txt
```

## Компиляция грамматики

### Подготовка для работы с ANTLR
- Windows  

  ```cmd
  antlr4env.bat
  ```
  
- PyCharm IDE
  
  1. Установить плагин `ANTLR v4 grammar plugin`
  2. Настроить параметры компиляции грамматики:
     * ПКМ по файлу `MAPY.g4` и нажать на `Configure ANTLR...`
     * В поле `Output directory where all output is generated` прописать дерикторию с проектом
     * В поле `Language` прописать `Python3`
     * Поставить галочку `generate parse tree visitor`
     * Нажать `OK`

### Получение файлов грамматики в виде Python файлов
- Windows  
  
  ```cmd
  antlr4py3 MAPY.g4
  ```
  
- PyCharm IDE

  ПКМ по файлу `MAPY.g4` и нажать на `Generate ANTLR Recognizer`  

## Запуск трансляции

- Перевод MAPY в LaTeX
  
    Выполнить команду
    
    ```cmd
    python mapy2latex.py [-h] -i INPUT_MAPY [-o OUTPUT_LATEX]
    ```
  
    * `-i`, `--input_mapy` - путь к файлу с кодом на языке MAPY, который нужно транслировать в LaTeX
    * `-o`, `--output_latex` - путь к файлу, в который запишется результат трансляции в LaTeX. По умолчанию `out.tex`

- Перевод MAPY в Python
  
    Выполнить команду
    
    ```cmd
    python mapy2py.py [-h] -i INPUT_MAPY [-o OUTPUT_PY]
    ```
  
    * `-i`, `--input_mapy` - путь к файлу с кодом на языке MAPY, который нужно транслировать в Python
    * `-o`, `--output_py` - путь к файлу, в который запишется результат трансляции в Python. По умолчанию `out.py`
