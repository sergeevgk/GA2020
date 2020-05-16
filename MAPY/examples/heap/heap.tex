\documentclass[12pt, a4paper]{article}

\usepackage[left = 1.5cm, right = 1.5cm, top = 1.5cm, bottom = 1.5cm]{geometry}

\usepackage{cmap}

\usepackage[T2A]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}

\usepackage{xcolor}

\usepackage{amsmath}
\usepackage{amssymb}

\begin{document}


$ $

$heap = \text{\color{blue} \textbf{struct }}\{arr\ :\ \text{\color{blue} \textbf{array }}[1..n]\text{\color{blue} \textbf{ of }}\text{\color{blue} \textbf{real}}\text{\color{blue} \textbf{; }}len\ :\ \text{\color{blue} \textbf{int}}\}$

$ $

$\text{\color{gray} {// Восстановление свойства кучи}} $

$\text{{\textbf{Вход:} куча }} {{A,}} \text{{ индекс }} {{i.}} $

$\text{{\textbf{Выход:} восстанавливается свойство кучи в поддереве с корнем }} {{A[i],}} \text{{ причём левое и правое поддеревья имеют свойства кучи}} {{.}} $

$\text{\color{blue} \textbf{func }}Heapify(A\ :\ \text{\color{blue} \textbf{heap}},\ i\ :\ \text{\color{blue} \textbf{int}}) $

$\quad l := 2\ *\ i;\ r := 2\ *\ i\ +\ 1;\ m := i\ \text{\color{gray} {//инициализация}} $

$\quad \text{\color{blue} \textbf{if }}(l\ \leq\ A.len)\ \&\ (A.arr[l]\ >\ A.arr[i])\text{\color{blue} \textbf{ then }}$

$\quad \quad m := l\ $

$\quad \text{\color{blue} \textbf{end }}\text{\color{blue} \textbf{if }}$

$\quad \text{\color{blue} \textbf{if }}(r\ \leq\ A.len)\ \&\ (A.arr[r]\ >\ A.arr[m])\text{\color{blue} \textbf{ then }}$

$\quad \quad m := r\ $

$\quad \text{\color{blue} \textbf{end }}\text{\color{blue} \textbf{if }}$

$\quad \text{\color{blue} \textbf{if }}i\ \neq\ m\text{\color{blue} \textbf{ then }}$

$\quad \quad A.arr[i] \leftrightarrow A.arr[m]\ \text{\color{gray} {//транспозиция элементов массива}} $

$\quad \quad Heapify(A,\ m)\ $

$\quad \text{\color{blue} \textbf{end }}\text{\color{blue} \textbf{if }}$

$\text{\color{blue} \textbf{end func }}$

$ $

$ $

$\text{\color{gray} {// Построение кучи}} $

$\text{{\textbf{Вход:} куча }} {{A}} $

$\text{{\textbf{Выход:} устанавливается свойство кучи в дереве}} {{,}} \text{{ заданным массивом }} {{A.arr}} $

$\text{\color{blue} \textbf{func }}MakeHeap(A\ :\ \text{\color{blue} \textbf{heap}}) $

$\quad \text{\color{blue} \textbf{for }}i\text{\color{blue} \textbf{ from }}\lfloor A.len\ /\ 2 \rfloor\text{\color{blue} \textbf{ downto }}1\text{\color{blue} \textbf{ do }}Heapify(A,\ i)\ \text{\color{blue} \textbf{end for}}$

$\text{\color{blue} \textbf{end func }}$

$ $

$ $

$\text{\color{gray} {// Изменение значения элемента кучи}} $

$\text{{\textbf{Вход:} куча }} {{A,}} \text{{ индекс изменяемого элемента }} {{i,}} \text{{ новое значение }} {{k.}} $

$\text{{\textbf{Выход:} значение элемента с индексом }} {{i}} \text{{ изменяется на }} {{k}} \text{{ без нарушения свойств двоичной кучи}} {{.}} $

$\text{\color{blue} \textbf{func }}IncElt(A\ :\ \text{\color{blue} \textbf{heap}},\ i\ :\ \text{\color{blue} \textbf{int}},\ k\ :\ \text{\color{blue} \textbf{real}}) $

$\quad \text{\color{blue} \textbf{if }}k\ <\ A.arr[i]\text{\color{blue} \textbf{ then }}$

$\quad \quad \text{\color{blue} \textbf{return}}\ \text{\color{blue} \textbf{fail}}\ \text{\color{gray} {//новое значение не должно быть меньше}} $

$\quad \text{\color{blue} \textbf{end }}\text{\color{blue} \textbf{if }}$

$\quad A.arr[i] := k\ $

$\quad \text{\color{blue} \textbf{while }}(i\ >\ 1)\ \&\ (A.arr[\lfloor i\ /\ 2 \rfloor]\ <\ A.arr[i])\text{\color{blue} \textbf{ do }}$

$\quad \quad A.arr[i] \leftrightarrow A.arr[\lfloor i\ /\ 2 \rfloor]\ \text{\color{gray} {//транспозиция элементов}} $

$\quad \quad i := \lfloor i\ /\ 2 \rfloor\ $

$\quad \text{\color{blue} \textbf{end while}}$

$\text{\color{blue} \textbf{end func }}$

$ $

$ $

$\text{\color{gray} {// Вставка нового элемента в кучу}} $

$\text{{\textbf{Вход:} куча }} {{A,}} \text{{ новый элемент }} {{k.}} $

$\text{{\textbf{Выход:} в кучу добавляется элемент со значением }} {{k}} \text{{ без нарушения свойств двоичной кучи}} {{.}} $

$\text{\color{blue} \textbf{func }}InsElt(A\ :\ \text{\color{blue} \textbf{heap}},\ k\ :\ \text{\color{blue} \textbf{real}}) $

$\quad \text{\color{blue} \textbf{if }}A.len\ =\ |A.arr|\text{\color{blue} \textbf{ then }}$

$\quad \quad \text{\color{blue} \textbf{return}}\ \text{\color{blue} \textbf{fail}}\ \text{\color{gray} {// весь массив заполнен}} $

$\quad \text{\color{blue} \textbf{end }}\text{\color{blue} \textbf{if }}$

$\quad A.len := A.len\ +\ 1\ $

$\quad A.arr[A.len] := -\infty\ $

$\quad IncElt(A,\ A.len,\ k)\ $

$\text{\color{blue} \textbf{end func }}$

$ $

$ $

$\text{\color{gray} {// Извлечение максимального элемента из кучи}} $

$\text{{\textbf{Вход:} куча }} {{A}} $

$\text{{\textbf{Выход:} извлечение максимального элемента из кучи с сохранением свойств двоичной кучи}} $

$\text{\color{blue} \textbf{func }}GetMax(A\ :\ \text{\color{blue} \textbf{heap}}) :\ \text{\color{blue} \textbf{real}}$

$\quad \text{\color{blue} \textbf{if }}A.len\ =\ 0\text{\color{blue} \textbf{ then }}\text{\color{blue} \textbf{return}}\ \text{\color{blue} \textbf{fail}}\ \text{\color{blue} \textbf{end }}\text{\color{blue} \textbf{if }} \text{\color{gray} {//куча пуста}} $

$\quad m := A.arr[1]\ \text{\color{gray} {//сохранение значения корневого элемента}} $

$\quad A.arr[1] := A.arr[A.len]\ \text{\color{gray} {//копирование последнего элемента в корень дерева}} $

$\quad A.len := A.len\ -\ 1\ \text{\color{gray} {//уменьшение длины массива}} $

$\quad Heapify(A,\ 1)\ $

$\quad \text{\color{blue} \textbf{return}}\ m\ $

$\text{\color{blue} \textbf{end func }}$

$ $

\end{document}
