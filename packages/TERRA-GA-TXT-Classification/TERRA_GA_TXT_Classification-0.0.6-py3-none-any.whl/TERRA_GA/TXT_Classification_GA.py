def TXT_create_Conv_Net(text_train, text_test, WIN_SIZE = 1000, WIN_HOP = 100, CLASS_COUNT = 6, vocab_size_list = [1000, 5000], embedding_subsets = False, BoW_subsets = True,
                        ep=10, verb = 1, n = 20, nsurv = 10, epohs = 5, times_for_popul = 3, best_models_num = 3, BATCH_SIZE = 128, Bow_or_Embedding0 = 0,  Bow_or_Embedding1=0,
                        link = '/content/drive/MyDrive/GA_folder', first_dense_size_low = 2, first_dense_size_high = 9, activation_list = ['softmax','sigmoid','linear','relu','tanh'],
                        final_activation_list = ['softmax','sigmoid'], embedding_size_low = 20, embedding_size_high = 100, layers_list = ["Conv1D", "LSTM", "Bidirectional", "Dense"], 
                        ConvSize_low = 2, ConvSize_high = 8, Kernel_size_low= 2, Kernel_size_high= 5, paddingType_list = ["same", "valid"], LSTM_units_low = 2, LSTM_units_high = 9, 
                        if_second_after_emb = 0, if_third_after_emb = 0, flatten_layers_list = ["Flatten", "GlobalMaxPooling1D", "GlobalAveragePooling1D", "LSTM"], denseSize_after_emb_low = 2,
                        denseSize_after_emb_high = 9, if_second_dense_after_BoW = 1, if_third_dense_after_BoW = 1, if_first_second_layer_after_emb = 1, if_first_third_layer_after_emb = 1, 
                        if_second_second_layer_after_emb = 1, if_second_third_layer_after_emb = 1, if_third_second_layer_after_emb = 1, if_third_third_layer_after_emb = 1, mut = 0.01):

  import random as random                          # Генератор рандомных чисел
  from google.colab import files                   # Для загрузки своей картинки
  import numpy as np                               # Библиотека работы с массивами
  import time                                      # Для подсчета времени
  from statistics import mean                      # Для подсчета среднего значения
  import gdown                                     # Подключение модуля для загрузки данных из облака
  import tensorflow
  import pandas as pd
  from tensorflow.keras.layers import Dense, Dropout, SpatialDropout1D, BatchNormalization, Embedding, Flatten, Activation
  from tensorflow.keras.layers import LSTM, Bidirectional, Conv1D, MaxPooling1D, GlobalMaxPooling1D, SpatialDropout1D, GlobalAveragePooling1D
  # Токенизатор для преобразование текстов в последовательности
  from tensorflow.keras.preprocessing.text import Tokenizer
  # Функции операционной системы
  import os
  # Регулярные выражения
  import re
  # Вывод объектов в ячейке colab
  from sklearn.model_selection import train_test_split
  from tensorflow.keras.models import Sequential   # Сеть прямого распространения
  from keras.utils.vis_utils import plot_model
  from tensorflow.keras import utils               # Используем для to_categorical
  import matplotlib.pyplot as plt                  # Для отрисовки графиков


  # функция по созданию выборки для обучения на эмбеддингах
  # данная функция подготавливает выборки для обучения на эмбеддингах. В нее подаются тексты, а на выходе мы получаем тренировочную
  # и тестовую выборки, разделенные окном WIN_SIZE с шагом WIN_HOP
  def create_sequence_for_embedding(text_train, text_test, VOCAB_SIZE):
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, filters='!"#$%&()*+,-–—./…:;<=>?@[\\]^_`{|}~«»\t\n\xa0\ufeff', lower=True, split=' ', oov_token='неизвестное_слово', char_level=False)
      # Построение частотного словаря по обучающим текстам
    tokenizer.fit_on_texts(text_train)
      # Построение словаря в виде пар слово - индекс
    items = list(tokenizer.word_index.items())
      # Преобразование обучающих и проверочных текстов текст в последовательности индексов согласно частотному словарю
    seq_train = tokenizer.texts_to_sequences(text_train)
    seq_test = tokenizer.texts_to_sequences(text_test)
      # Функция разбиения последовательности на отрезки скользящим окном
      # На входе - последовательность индексов, размер окна, шаг окна
    def split_sequence(sequence, win_size, hop):
      # Последовательность разбивается на части до последнего полного окна
      return [sequence[i:i + win_size] for i in range(0, len(sequence) - win_size + 1, hop)]
    # Функция формирования выборок из последовательностей индексов
    # формирует выборку отрезков и соответствующих им меток классов в виде one hot encoding
    def vectorize_sequence(seq_list, win_size, hop):
      # В списке последовательности следуют в порядке их классов
      # Всего последовательностей в списке ровно столько, сколько классов
      class_count = len(seq_list)

      # Списки для исходных векторов и категориальных меток класса
      x, y = [], []
      # Для каждого класса:
      for cls in range(class_count):
          # Разбиение последовательности класса cls на отрезки
          vectors = split_sequence(seq_list[cls], win_size, hop)
          # Добавление отрезков в выборку
          x += vectors
          if class_count == 2:
              y += [cls] * len(vectors)
          # Для всех отрезков класса cls добавление меток класса в виде OHE
          else:
            y += [utils.to_categorical(cls, class_count)] * len(vectors)


      # Возврат результатов как numpy-массивов
      return np.array(x), np.array(y)
    # Формирование обучающей выборки
    x_train_emb, y_train = vectorize_sequence(seq_train, WIN_SIZE, WIN_HOP) 
      # Формирование тестовой выборки
    x_test_emb, y_test = vectorize_sequence(seq_test, WIN_SIZE, WIN_HOP)
    return x_train_emb, y_train, x_test_emb, y_test

  # функция по созданию выборки для обучения на BAG OF WORDS.
  def create_sequence_for_BoW(text_train, text_test, VOCAB_SIZE):
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, filters='!"#$%&()*+,-–—./…:;<=>?@[\\]^_`{|}~«»\t\n\xa0\ufeff', lower=True, split=' ', oov_token='неизвестное_слово', char_level=False)
    tokenizer.fit_on_texts(text_train)
      # Построение словаря в виде пар слово - индекс
    items = list(tokenizer.word_index.items())
      # Преобразование обучающих и проверочных текстов текст в последовательности индексов согласно частотному словарю
    seq_train = tokenizer.texts_to_sequences(text_train)
    seq_test = tokenizer.texts_to_sequences(text_test)
      # Функция разбиения последовательности на отрезки скользящим окном
      # На входе - последовательность индексов, размер окна, шаг окна
    def split_sequence(sequence, win_size, hop):
      # Последовательность разбивается на части до последнего полного окна
      return [sequence[i:i + win_size] for i in range(0, len(sequence) - win_size + 1, hop)]
    # Функция формирования выборок из последовательностей индексов
    # формирует выборку отрезков и соответствующих им меток классов в виде one hot encoding
    def vectorize_sequence(seq_list, win_size, hop):
      # В списке последовательности следуют в порядке их классов
      # Всего последовательностей в списке ровно столько, сколько классов
      class_count = len(seq_list)
      # Списки для исходных векторов и категориальных меток класса
      x, y = [], []
      # Для каждого класса:
      for cls in range(class_count):
          # Разбиение последовательности класса cls на отрезки
          vectors = split_sequence(seq_list[cls], win_size, hop)
          # Добавление отрезков в выборку
          x += vectors
          if class_count == 2:
              y += [cls] * len(vectors)
          # Для всех отрезков класса cls добавление меток класса в виде OHE
          else:
            y += [utils.to_categorical(cls, class_count)] * len(vectors)


      # Возврат результатов как numpy-массивов
      return np.array(x), np.array(y)
    # Формирование обучающей выборки
    x_train_emb, y_train = vectorize_sequence(seq_train, WIN_SIZE, WIN_HOP) 
      # Формирование тестовой выборки
    x_test_emb, y_test = vectorize_sequence(seq_test, WIN_SIZE, WIN_HOP)
    x_train_BoW = tokenizer.sequences_to_matrix(x_train_emb.tolist())
    x_test_BoW = tokenizer.sequences_to_matrix(x_test_emb.tolist())
    return x_train_BoW, y_train, x_test_BoW, y_test

  # если нужны заранее приготовленные выборки для обучения на эмбеддингах:
  if embedding_subsets == True:
    # создаем выборки по разному размеру словаря - vocab_size_list - для обучения на эмбеддингах
    emb_seq_list = []
    for v_size in vocab_size_list:
      emb_seq_list.append(create_sequence_for_embedding(text_train, text_test, VOCAB_SIZE=v_size))

  # если нужны заранее приготовленные выборки для обучения на BoW:
  if BoW_subsets == True:
    # создаем выборки по разному размеру словаря - vocab_size_list - для обучения на эмбеддингах
    BoW_seq_list = []
    for v_size in vocab_size_list:
      BoW_seq_list.append(create_sequence_for_BoW(text_train, text_test, VOCAB_SIZE=v_size))
  
  def createRandomNet():
  
    net = []
    net.append(random.randint(Bow_or_Embedding0,Bow_or_Embedding1))     # Используем Bag of words или Embedding             net[0] 0 - BoW, 1 - embedding
    net.append(random.randint(first_dense_size_low, first_dense_size_high))  # Количество нейронов в 1 dense блоке               net[1]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации Dense слоя первого блока        net[2]
    net.append(random.randint(0,1))                                     # Делаем ли Dropout в первом блоке                  net[3]
    net.append(random.randint(0,4))                                     # Процент Dropout в первом слое 1 блока             net[4]
    net.append(random.randint(0,1))                                     # Делаем ли нормализацию в первом блоке             net[5]

    net.append(random.randint(0,if_second_dense_after_BoW))             # Делаем ли второй Dense блок                       net[6]
    net.append(random.randint(first_dense_size_low, first_dense_size_high))  # Количество нейронов во 2 dense блоке              net[7]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации Dense слоя второго блока        net[8]
    net.append(random.randint(0,1))                                     # Делаем ли Dropout во 2 блоке                      net[9]
    net.append(random.randint(0,4))                                     # Процент Dropout во 2 блоке                        net[10]
    net.append(random.randint(0,1))                                     # Делаем ли нормализацию в 2 блоке                  net[11]

    net.append(random.randint(0,if_third_dense_after_BoW))              # Делаем ли третий Dense блок                       net[12]
    net.append(random.randint(first_dense_size_low, first_dense_size_high)) # Количество нейронов в 3 dense блоке               net[13]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации Dense слоя третьего блока       net[14]
    net.append(random.randint(0,1))                                     # Делаем ли Dropout в 3 блоке                       net[15]
    net.append(random.randint(0,4))                                     # Процент Dropout в 3 блоке                         net[16]
    net.append(random.randint(0,1))                                     # Делаем ли нормализацию в 3 блоке                  net[17]
    net.append(random.randint(0,(len(final_activation_list)-1)))        # Функция активации выходного слоя                  net[18]

    net.append(random.randint(embedding_size_low, embedding_size_high)) # Размер вектора для эмбеддинга                     net[19]
    net.append(random.randint(0,1))                                     # Делаем ли Spatialdropout после слоя Embedding     net[20]
    net.append(random.randint(0,1))                                     # Добавляем ли Batchnorm после слоя Embedding       net[21]

    net.append(random.randint(0,(len(layers_list)-1)))                  # Какой из слоев из списка layers_list добавляем  в первом блоке net[22]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров первого Conv1D в первом блоке      net[23]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size первого свёрточного слоя в первом блоке      net[24]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для первого слоя первого блока       net[25]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого слоя первого блока      net[26]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров второго Conv1D в первом блоке      net[27]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size второго свёрточного слоя в первом блоке      net[28]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для второго слоя первого блока       net[29]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго слоя первого блока      net[30]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров третьего Conv1D в первом блоке     net[31]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size третьего свёрточного слоя в первом блоке     net[32]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для третьего слоя первого блока      net[33]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего слоя первого блока     net[34]

    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 1 слое LSTM 1 блока         net[35]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов во 2 слое LSTM 1 блока        net[36]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 3 слое LSTM 1 блока         net[37]
    net.append(random.randint(0,4))                                     # размер spatialDropout после Embedding             net[38]
    net.append(random.randint(0,1))                                     # Делаем ли Maxpooling в 1 блоке                    net[39]
    net.append(random.randint(2,4))                                     # Pool_size для Maxpooling1D в 1 блоке              net[40]

    net.append(random.randint(0,if_second_after_emb))                   # Делаем ли второй блок после Embedding             net[41]
    net.append(random.randint(0,(len(layers_list)-1)))                  # Какой из слоев из списка layers_list добавляем  во втором блоке net[42]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров первого Conv1D во втором блоке     net[43]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size первого свёрточного слоя во втором блоке     net[44]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для первого слоя во втором блоке     net[45]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого слоя во втором блоке    net[46] 

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров второго Conv1D во втором блоке     net[47]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size второго свёрточного слоя во втором блоке     net[48]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для второго слоя во втором блоке     net[49]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго слоя во втором блоке    net[50]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров третьего Conv1D во втором блоке    net[51]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size третьего свёрточного слоя во втором блоке    net[52]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для третьего слоя во втором блоке    net[53]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего слоя во втором блоке   net[54]

    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 1 слое LSTM во втором блоке net[55]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов во 2 слое LSTM во втором блоке net[56]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 3 слое LSTM во втором блоке net[57]

    net.append(random.randint(0,1))                                     # Делаем ли maxpooling для второго блока            net[58]
    net.append(random.randint(2,4))                                     # Размер MaxPooling для второго блока               net[59]

    net.append(random.randint(0,if_third_after_emb))                    # Делаем ли третий блок после Embedding             net[60]
    net.append(random.randint(0,(len(layers_list)-1)))                  # Какой из слоев из списка layers_list добавляем  в третьем блоке net[61]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров первого Conv1D в третьем блоке     net[62]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size первого свёрточного слоя в третьем блоке     net[63]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для первого слоя в третьем блоке     net[64]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого слоя в третьем блоке    net[65] 

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров второго Conv1D в третьем блоке     net[66]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size второго свёрточного слоя в третьем блоке     net[67]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для второго слоя в третьем блоке     net[68]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго слоя в третьем блоке    net[69]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров третьего Conv1D в третьем блоке    net[70]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size третьего свёрточного слоя в третьем блоке    net[71]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для третьего слоя в третьем блоке    net[72]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего слоя в третьем блоке   net[73]

    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 1 слое LSTM в третьем блоке net[74]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов во 2 слое LSTM в третьем блоке net[75]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 3 слое LSTM в третьем блоке net[76]

    net.append(random.randint(0,1))                                     # Делаем ли maxpooling для третьего блока            net[77]
    net.append(random.randint(2,4))                                     # Размер MaxPooling для третьего блока               net[78]
    
    net.append(random.randint(0,(len(flatten_layers_list)-1)))          # Тип выравнивающего слоя Flatten, GlobalMax, GlobalAverage или LSTM  net[79]
    net.append(random.randint(0,(len(vocab_size_list)-1)))              # Какую выборку подаем сети (должно соответствовать vocab_size_list) net[80]

    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units первого Dense слоя в первом блоке (степень числа 2)            net[81]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого Dense слоя в первом блоке net[82]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units второго Dense слоя в первом блоке (степень числа 2)           net[83]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго Dense слоя в первом блоке net[84]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units третьего Dense слоя в первом блоке (степень числа 2)           net[85]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего Dense слоя в первом блоке net[86]

    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units первого Dense слоя во втором блоке (степень числа 2)           net[87]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого Dense слоя во втором блоке net[88]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units второго Dense слоя во втором блоке (степень числа 2)            net[89]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго Dense слоя во втором блоке net[90]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units третьего Dense слоя во втором блоке (степень числа 2)           net[91]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего Dense слоя во втором блоке net[92]

    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units первого Dense слоя в третьем блоке (степень числа 2)           net[93]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого Dense слоя в третьем блоке net[94]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units второго Dense слоя в третьем блоке (степень числа 2)           net[95]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго Dense слоя в третьем блоке net[96]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units третьего Dense слоя в третьем блоке (степень числа 2)           net[97]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего Dense слоя в третьем блоке net[98]

    net.append(random.randint(0,0))                                     # запускаем алгоритм при уже созданных датасетах или создаем в боте net[99]
    net.append(random.randint(0,if_first_second_layer_after_emb))       # Добавляем ли второй слой в первый блок при эмбеддингах    net[100] 
    net.append(random.randint(0,if_first_third_layer_after_emb))        # Добавляем ли третий слой в первый блок при эмбеддингах    net[101] 
    net.append(random.randint(0,if_second_second_layer_after_emb))      # Добавляем ли второй слой во второй блок при эмбеддингах    net[102] 
    net.append(random.randint(0,if_second_third_layer_after_emb))       # Добавляем ли третий слой во второй блок при эмбеддингах    net[103] 
    net.append(random.randint(0,if_third_second_layer_after_emb))       # Добавляем ли второй слой в третий блок при эмбеддингах    net[104] 
    net.append(random.randint(0,if_third_third_layer_after_emb))        # Добавляем ли третий слой в третий блок при эмбеддингах    net[105] 

    return net

  # Создаём сеть (net - список параметров - бот)

  def createConvNet(net):

    model = Sequential()             # Создаем модель Sequential
    
    BoW_or_Embedding = net[0]         # Используем Bag of words или Embedding. '0'- Bag of words, '1'- Embedding
    first_dense_size = 2 **net[1]     # Количество нейронов в dense слое 1 блока
    first_dense_activation = net[2]   # Функция активации первого слоя первого блока
    if_first_dropout = net[3]         # Делаем ли Dropout в первом блоке
    first_dropout_size = net[4]       # Процент Dropout в 1 блоке
    if_first_batchnorm = net[5]       # Делаем ли нормализацию в первом блоке

    if_second_dense = net[6]          # Делаем ли второй Dense блок                     
    second_dense_size = 2 **net[7]    # Количество нейронов в dense слое 2 блока
    second_dense_activation = net[8]  # Функция активации второго dense блока
    if_second_dropout = net[9]        # Делаем ли Dropout во втором блоке
    second_dropout_size = net[10]     # Процент Dropout во 2 блоке
    if_second_batchnorm = net[11]     # Делаем ли нормализацию во втором блоке

    if_third_dense = net[12]          # Делаем ли третий Dense блок
    third_dense_size = 2 **net[13]    # Количество нейронов в dense слое 3 блока
    third_dense_activation = net[14]  # Функция активации третьего dense блока
    if_third_dropout = net[15]        # Делаем ли Dropout в третьем блоке
    third_dropout_size = net[16]      # Процент Dropout в 3 блоке
    if_third_batchnorm = net[17]      # Делаем ли нормализацию в третьем блоке    
    last_activation = net[18]         # Функция активации выходного слоя  

    embedding_size = net[19]          # Размер вектора эмбеддинг    
    if_spatialdropout = net[20]       # Делаем ли Spatialdropout после слоя Embedding
    embedding_batchnorm = net[21]     # Добавляем ли нормализацию по батчу после слоя Embedding
    first_layer_type = net[22]        # Какой из слоев из списка layers_list добавляем в первом блоке

    firstConvSize0 = 2 ** net[23]     # Количество фильтров первого Conv1D в первом блоке
    firstConvKernel0 = net[24]        # kernel_size первого свёрточного слоя в первом блоке
    firstPaddingType0 = net[25]       # Тип паддинга для первого слоя первого блока
    firstActivation0 = net[26]        # Функция активации первого слоя первого блока

    firstDenseSize0 = 2 ** net[81]    # Размер первого Dense слоя в первом блоке
    firstDenseActivation0 = net[82]   # Функция активации первого Dense слоя в первом блоке

    firstConvSize1 = 2 ** net[27]     # Количество фильтров второго Conv1D в первом блоке
    firstConvKernel1 = net[28]        # kernel_size второго свёрточного слоя в первом блоке
    firstPaddingType1 = net[29]       # Тип паддинга для второго слоя первого блока
    firstActivation1 = net[30]        # Функция активации второго слоя первого блока

    firstDenseSize1 = 2 ** net[83]    # Размер первого Dense слоя в первом блоке
    firstDenseActivation1 = net[84]   # Функция активации первого Dense слоя в первом блоке

    firstConvSize2 = 2 ** net[31]     # Количество фильтров третьего Conv1D в первом блоке
    firstConvKernel2 = net[32]        # kernel_size третьего свёрточного слоя в первом блоке
    firstPaddingType2 = net[33]       # Тип паддинга для третьего слоя первого блока
    firstActivation2 = net[34]        # Функция активации третьего слоя первого блока

    firstDenseSize2 = 2 ** net[85]    # Размер первого Dense слоя в первом блоке
    firstDenseActivation2 = net[86]   # Функция активации первого Dense слоя в первом блоке

    first_LSTM_size_0 = 2 ** net[35]  # Количество нейронов в 1 слое LSTM 1 блока
    first_LSTM_size_1 = 2 ** net[36]  # Количество нейронов во 2 слое LSTM 1 блока
    first_LSTM_size_2 = 2 ** net[37]  # Количество нейронов в 3 слое LSTM 1 блока

    spatialDropout_size = net[38]     # размер spatialDropout после Embedding
    makeMaxPooling0 = net[39]         # Делаем ли maxpooling для первого блока
    maxPoolingSize0 = net[40]         # Размер MaxPooling для первого блока

    if_second_block = net[41]         # Делаем ли второй блок после Embedding
    second_layer_type = net[42]       # Какой из слоев из списка layers_list добавляем в первом блоке

    secondConvSize0 = 2 ** net[43]     # Размер свертки первого Conv1D во втором блоке
    secondConvKernel0 = net[44]        # Ядро первого свёрточного слоя во втором блоке
    secondPaddingType0 = net[45]       # Тип паддинга для первого слоя во втором блоке
    secondActivation0 = net[46]        # Функция активации первого слоя во втором блоке

    secondDenseSize0 = 2 ** net[87]    # Размер первого Dense слоя во втором блоке
    secondDenseActivation0 = net[88]   # Функция активации первого Dense слоя во втором блоке

    secondConvSize1 = 2 ** net[47]     # Размер свертки второго Conv1D во втором блоке
    secondConvKernel1 = net[48]        # Ядро второго свёрточного слоя во втором блоке
    secondPaddingType1 = net[49]       # Тип паддинга для второго слоя во втором блоке
    secondActivation1 = net[50]        # Функция активации второго слоя во втором блоке

    secondDenseSize1 = 2 ** net[89]    # Размер второго Dense слоя во втором блоке
    secondDenseActivation1 = net[90]   # Функция активации второго Dense слоя во втором блоке

    secondConvSize2 = 2 ** net[51]     # Размер свертки третьего Conv1D во втором блоке
    secondConvKernel2 = net[52]        # Ядро третьего свёрточного слоя во втором блоке
    secondPaddingType2 = net[53]       # Тип паддинга для третьего слоя во втором блоке
    secondActivation2 = net[54]        # Функция активации третьего слоя во втором блоке

    secondDenseSize2 = 2 ** net[91]    # Размер третьего Dense слоя во втором блоке
    secondDenseActivation2 = net[92]   # Функция активации третьего Dense слоя во втором блоке

    second_LSTM_size_0 = 2 ** net[55]  # Количество нейронов в 1 слое LSTM во втором блоке
    second_LSTM_size_1 = 2 ** net[56]  # Количество нейронов во 2 слое LSTM во втором блоке
    second_LSTM_size_2 = 2 ** net[57]  # Количество нейронов в 3 слое LSTM во втором блоке

    makeMaxPooling1 = net[58]         # Делаем ли maxpooling для второго блока
    maxPoolingSize1 = net[59]         # Размер MaxPooling для второго блока


    if_third_block = net[60]         # Делаем ли третий блок после Embedding
    third_layer_type = net[61]       # Какой из слоев из списка layers_list добавляем в третьем блоке

    thirdConvSize0 = 2 ** net[62]     # Размер свертки первого Conv1D в третьем блоке
    thirdConvKernel0 = net[63]        # Ядро первого свёрточного слоя в третьем блоке
    thirdPaddingType0 = net[64]       # Тип паддинга для первого слоя в третьем блоке
    thirdActivation0 = net[65]        # Функция активации первого слоя в третьем блоке

    thirdDenseSize0 = 2 ** net[93]    # Размер первого Dense слоя в третьем блоке
    thirdDenseActivation0 = net[94]   # Функция активации первого Dense слоя в третьем блоке

    thirdConvSize1 = 2 ** net[66]     # Размер свертки второго Conv1D в третьем блоке
    thirdConvKernel1 = net[67]        # Ядро второго свёрточного слоя в третьем блоке
    thirdPaddingType1 = net[68]       # Тип паддинга для второго слоя в третьем блоке
    thirdActivation1 = net[69]        # Функция активации второго слоя в третьем блоке

    thirdDenseSize1 = 2 ** net[95]    # Размер второго Dense слоя в третьем блоке
    thirdDenseActivation1 = net[96]   # Функция активации второго Dense слоя в третьем блоке

    thirdConvSize2 = 2 ** net[70]     # Размер свертки третьего Conv1D в третьем блоке
    thirdConvKernel2 = net[71]        # Ядро третьего свёрточного слоя в третьем блоке
    thirdPaddingType2 = net[72]       # Тип паддинга для третьего слоя в третьем блоке
    thirdActivation2 = net[73]        # Функция активации третьего слоя в третьем блоке

    thirdDenseSize2 = 2 ** net[97]    # Размер третьего Dense слоя в третьем блоке
    thirdDenseActivation2 = net[98]   # Функция активации третьего Dense слоя в третьем блоке

    third_LSTM_size_0 = 2 ** net[74]  # Количество нейронов в 1 слое LSTM в третьем блоке
    third_LSTM_size_1 = 2 ** net[75]  # Количество нейронов во 2 слое LSTM в третьем блоке
    third_LSTM_size_2 = 2 ** net[76]  # Количество нейронов в 3 слое LSTM в третьем блоке

    makeMaxPooling2 = net[77]         # Делаем ли maxpooling для третьего блока
    maxPoolingSize2 = net[78]         # Размер MaxPooling для третьего блока

    flatten_globalmax_globalaver_lstm_choise  = net[79]         # тип выравнивающего слоя
    vocab_size_choise = net[80]       # Выборку с каким объемом словаря используем при обучении (1000, 5000, 10000 слов) должно соответствовать vocab_size_list
    if_create_dataset = net[99]       # Запускаем алгоритм при уже созданных датасетах или создаем в боте. 0 - на уже созданных выборках
    if_first_second_layer = net[100]  # Добавляем ли второй слой в первый блок при эмбеддингах    net[100] 
    if_first_third_layer = net[101]   # Добавляем ли третий слой в первый блок при эмбеддингах    net[101] 
    if_second_second_layer = net[102] # Добавляем ли второй слой во второй блок при эмбеддингах    net[102] 
    if_second_third_layer = net[103]  # Добавляем ли третий слой во второй блок при эмбеддингах    net[103] 
    if_third_second_layer = net[104]  # Добавляем ли второй слой в третий блок при эмбеддингах    net[104] 
    if_third_third_layer = net[105]   # Добавляем ли третий слой в третий блок при эмбеддингах    net[105] 
    

    #activation_list = ['softmax','sigmoid','linear','relu','tanh']  # какие функции активации тестируем в полносвязных слоях 
    #final_activation_list = ['softmax','sigmoid']                   # какие функции активации тестируем в полносвязных слоях
    dropout_list = [0.05, 0.1, 0.3, 0.4, 0.5]
    #layers_list = ["Conv1D", "LSTM", "Bidirectional", "Dense"]               # какие слои используем в блоках после Embedding
    #paddingType_list = ["same", "valid"]                            # какие типы паддингов тестируем в сверточных блоках
    #flatten_globalmax_globalaver_lstm = ["Flatten", "GlobalMaxPooling1D", "GlobalAveragePooling1D", "LSTM"] # тестируем Flatten, GlobalMaxPooling1D, GlobalAveragePooling1D или LSTM
    # Если используем Bag of words:
    if (BoW_or_Embedding!=1):   
      # первый полносвязный блок
      model.add(Dense(first_dense_size, input_dim=vocab_size_list[vocab_size_choise], activation=activation_list[first_dense_activation])) 
      if (if_first_dropout!=0):
        model.add(Dropout(dropout_list[first_dropout_size]))
      if (if_first_batchnorm!=0):
        model.add(BatchNormalization())
      # второй полносвязный блок
      if (if_second_dense!=0):
        model.add(Dense(second_dense_size, activation=activation_list[second_dense_activation]))
        if (if_second_dropout!=0):
          model.add(Dropout(dropout_list[second_dropout_size]))
        if (if_second_batchnorm!=0):
          model.add(BatchNormalization())
      # третий полносвязный блок
      if (if_third_dense!=0):
        model.add(Dense(third_dense_size, activation=activation_list[third_dense_activation]))
        if (if_third_dropout!=0):
          model.add(Dropout(dropout_list[third_dropout_size]))
        if (if_third_batchnorm!=0):
          model.add(BatchNormalization())
    else:
      model.add(Embedding(vocab_size_list[vocab_size_choise], embedding_size, input_length=WIN_SIZE)) # Добавим эмбеддинг
      if (if_spatialdropout!=0):
        model.add(SpatialDropout1D(dropout_list[spatialDropout_size])) # Добавим дропаут для целых векторов в эмбеддинг пространстве
      if (embedding_batchnorm!=0):
        model.add(BatchNormalization())                             # Добавим нормализацию по батчу
      # формируем первый блок из 3-х слоев на выбор сети: Conv1D, LSTM, BidirectionalLSTM, Dense
      if (layers_list[first_layer_type]) == "Conv1D":
        model.add(Conv1D(firstConvSize0, firstConvKernel0, activation=activation_list[firstActivation0], padding=paddingType_list[firstPaddingType0]))
        if (if_first_second_layer!=0):
          model.add(Conv1D(firstConvSize1, firstConvKernel1, activation=activation_list[firstActivation1], padding=paddingType_list[firstPaddingType1]))
        if (if_first_third_layer!=0):
          model.add(Conv1D(firstConvSize2, firstConvKernel2, activation=activation_list[firstActivation2], padding=paddingType_list[firstPaddingType2]))
      if (layers_list[first_layer_type]) == "LSTM":
        model.add(LSTM(first_LSTM_size_0, return_sequences=1))
        if (if_first_second_layer!=0):
          model.add(LSTM(first_LSTM_size_1, return_sequences=1))
        if (if_first_third_layer!=0):
          model.add(LSTM(first_LSTM_size_2, return_sequences=1))
      if (layers_list[first_layer_type]) == "Bidirectional":
        model.add(Bidirectional(LSTM(first_LSTM_size_0, return_sequences=True)))
        if (if_first_second_layer!=0):
          model.add(Bidirectional(LSTM(first_LSTM_size_1, return_sequences=True)))
        if (if_first_third_layer!=0):  
          model.add(Bidirectional(LSTM(first_LSTM_size_2, return_sequences=True)))
      if (layers_list[first_layer_type]) == "Dense":
        model.add(Dense(firstDenseSize0, activation=activation_list[firstDenseActivation0]))
        if (if_first_second_layer!=0):
          model.add(Dense(firstDenseSize1, activation=activation_list[firstDenseActivation1]))
        if (if_first_third_layer!=0):
          model.add(Dense(firstDenseSize2, activation=activation_list[firstDenseActivation2]))
      if (makeMaxPooling0!=0):
        model.add(MaxPooling1D(maxPoolingSize0))
      if (if_first_dropout!=0):
        model.add(Dropout(dropout_list[first_dropout_size]))
      if (if_first_batchnorm!=0):
        model.add(BatchNormalization()) 

      # если делаем второй блок после Embedding
      if (if_second_block!=0):
        if (layers_list[second_layer_type]) == "Conv1D":
          model.add(Conv1D(secondConvSize0, secondConvKernel0, activation=activation_list[secondActivation0], padding=paddingType_list[secondPaddingType0]))
          if (if_second_second_layer!=0):
            model.add(Conv1D(secondConvSize1, secondConvKernel1, activation=activation_list[secondActivation1], padding=paddingType_list[secondPaddingType1]))
          if (if_second_third_layer!=0):  
            model.add(Conv1D(secondConvSize2, secondConvKernel2, activation=activation_list[secondActivation2], padding=paddingType_list[secondPaddingType2]))
        if (layers_list[second_layer_type]) == "LSTM":
          model.add(LSTM(second_LSTM_size_0, return_sequences=1))
          if (if_second_second_layer!=0):
            model.add(LSTM(second_LSTM_size_1, return_sequences=1))
          if (if_second_third_layer!=0):
            model.add(LSTM(second_LSTM_size_2, return_sequences=1))
        if (layers_list[second_layer_type]) == "Bidirectional":
          model.add(Bidirectional(LSTM(second_LSTM_size_0, return_sequences=True)))
          if (if_second_second_layer!=0):
            model.add(Bidirectional(LSTM(second_LSTM_size_1, return_sequences=True)))
          if (if_second_third_layer!=0):
            model.add(Bidirectional(LSTM(second_LSTM_size_2, return_sequences=True))) 
        if (layers_list[first_layer_type]) == "Dense":
          model.add(Dense(secondDenseSize0, activation=activation_list[secondDenseActivation0]))
          if (if_second_second_layer!=0):
            model.add(Dense(secondDenseSize1, activation=activation_list[secondDenseActivation1]))
          if (if_second_third_layer!=0):
            model.add(Dense(secondDenseSize2, activation=activation_list[secondDenseActivation2]))
        if (makeMaxPooling1!=0):
          model.add(MaxPooling1D(maxPoolingSize1))
        if (if_second_dropout!=0):
          model.add(Dropout(dropout_list[second_dropout_size]))
        if (if_second_batchnorm!=0):
          model.add(BatchNormalization()) 

      # если делаем третий блок после Embedding
      if (if_third_block!=0):
        if (layers_list[third_layer_type]) == "Conv1D":
          model.add(Conv1D(thirdConvSize0, thirdConvKernel0, activation=activation_list[thirdActivation0], padding=paddingType_list[thirdPaddingType0]))
          if (if_third_second_layer!=0):
            model.add(Conv1D(thirdConvSize1, thirdConvKernel1, activation=activation_list[thirdActivation1], padding=paddingType_list[thirdPaddingType1]))
          if (if_third_third_layer!=0):
            model.add(Conv1D(thirdConvSize2, thirdConvKernel2, activation=activation_list[thirdActivation2], padding=paddingType_list[thirdPaddingType2]))
        if (layers_list[third_layer_type]) == "LSTM":
          model.add(LSTM(third_LSTM_size_0, return_sequences=1))
          if (if_third_second_layer!=0):
            model.add(LSTM(third_LSTM_size_1, return_sequences=1))
          if (if_third_third_layer  !=0):
            model.add(LSTM(third_LSTM_size_2, return_sequences=1))
        if (layers_list[third_layer_type]) == "Bidirectional":
          model.add(Bidirectional(LSTM(third_LSTM_size_0, return_sequences=True)))
          if (if_third_second_layer!=0):
            model.add(Bidirectional(LSTM(third_LSTM_size_1, return_sequences=True)))
          if (if_third_third_layer  !=0):
            model.add(Bidirectional(LSTM(third_LSTM_size_2, return_sequences=True))) 
        if (layers_list[first_layer_type]) == "Dense":
          model.add(Dense(thirdDenseSize0, activation=activation_list[thirdDenseActivation0]))
          if (if_third_second_layer!=0):
            model.add(Dense(thirdDenseSize1, activation=activation_list[thirdDenseActivation1]))
          if (if_third_third_layer  !=0):
            model.add(Dense(thirdDenseSize2, activation=activation_list[thirdDenseActivation2]))
        if (makeMaxPooling2!=0):
          model.add(MaxPooling1D(maxPoolingSize2))
        if (if_second_dropout!=0):
          model.add(Dropout(dropout_list[third_dropout_size]))
        if (if_third_batchnorm!=0):
          model.add(BatchNormalization()) 
      if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="Flatten"):
        model.add(Flatten())   
      if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="GlobalMaxPooling1D"):
        model.add(GlobalMaxPooling1D()) 
      if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="GlobalAveragePooling1D"):
        model.add(GlobalAveragePooling1D())   
      if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="LSTM"):
        model.add(LSTM(4))  
    if CLASS_COUNT == 2:
      cl_count=1
    else:
      cl_count=CLASS_COUNT
    model.add(Dense(cl_count, activation=final_activation_list[last_activation]))
    return model

  def evaluateNet(net):
    if CLASS_COUNT>2:
      LOSS='categorical_crossentropy'
    else:
      LOSS='binary_crossentropy'
    val = 0
    time.time()
    model = createConvNet(net) # Создаем модель createConvNet
    # если выборки НЕ создаются в боте:
    if (net[99]==0):
      # если обучаем на BoW:
      if net[0]==0:
        x_train = BoW_seq_list[net[80]][0]
        x_test = BoW_seq_list[net[80]][2]
        y_train = BoW_seq_list[net[80]][1]
        y_test = BoW_seq_list[net[80]][3]
      else:
        x_train = emb_seq_list[net[80]][0]
        x_test = emb_seq_list[net[80]][2]
        y_train = emb_seq_list[net[80]][1]
        y_test = emb_seq_list[net[80]][3]
    # если выборки создаются в боте:
    else:
      # если обучаем на BoW:
      if net[0]==0:
        x_train, y_train, x_test, y_test = create_sequence_for_BoW(text_train, text_test, VOCAB_SIZE=vocab_size_list[net[80]])
      else:
        x_train, y_train, x_test, y_test = create_sequence_for_embedding(text_train, text_test, VOCAB_SIZE=vocab_size_list[net[80]])
    # Компилируем сеть
    model.compile(loss=LOSS, optimizer='rmsprop', metrics=['accuracy'])

    # Обучаем сеть на датасете 
    history = model.fit(x_train, 
                        y_train, 
                        batch_size=BATCH_SIZE, 
                        epochs=ep,
                        validation_data=(x_test, y_test),
                        verbose=1)
      
    val = history.history["val_accuracy"][-1] # Возвращаем точность на проверочной выборке с последней эпохи
    return val, model                         # Возвращаем точность и модель
  
  nnew = n - nsurv    # Количество новых (столько новых ботов создается)
  l = 106              # Размер бота
  #epohs = 3           # Количество запусков генетики
  #times_for_popul = 2 # Количество запусков одной популяции
  #mut = 0.01          # Коэффициент мутаций
  #best_models_num = 3 # Сколько лучших моделей мы хотим получить по итогам всех запусков
  #worst_models_num = 3# Сколько худших моделей мы хотим получить по итогам всех запусков
  popul = []          # Массив популяции
  val = []            # Одномерный массив значений точности этих ботов
  mean_val = []       # Массив со средними точностями по запускам
  max_val = []        # Массив с лучшими точностями по запускам
  best_models  =[]    # 3 лучших модели по итогам всех запусков
  #worst_models = []   # 3 худших модели по итогам всех запусков

  from google.colab import drive
  import os.path
  from os import path
  drive.mount('/content/drive')
  link = '/content/drive/MyDrive/GA_folder'
  if path.exists(link) == False:
    os.mkdir(link)
  # Создаём случайных ботов
  for i in range(n):
    popul.append(createRandomNet())
    
  for it in range(epohs):                 # Пробегаем по всем запускам генетики
    #val = []                             # список с точностями ботов на проверочной выборке с последней эпохи
    curr_time = time.time()
    curr_models=[[] for _ in range(n)]    # список с моделями из данного запуска
    bots_accuracy_list = [[] for _ in range(n)] # создаем список с n пустыми списками под точности бота

    # для каждого бота создается список, в который будут добавляться точности на каждом запуске:
    
    for j in range(times_for_popul):
      for i in range(n):                    # Пробегаем в цикле по всем ботам 
        bot = popul[i]                      # Берем очередного бота
        f, model_sum = evaluateNet(bot) # Вычисляем точность текущего бота на последней эпохе и получаем обученную модель
        #val.append(f)                       # Добавляем полученное значение в список val
        bots_accuracy_list[i].append(f)
        curr_models[i].append(model_sum)       # Добавляем текущую модель в список с моделями curr_models
    best_bots_accuracy_list = []            # список из лучших точностей по каждому боту
    for acc in bots_accuracy_list:
      best_bots_accuracy_list.append(max(acc))

    #best_curr_models = []
    sval = sorted(best_bots_accuracy_list, reverse=1)         # Сортируем best_bots_accuracy_list по убыванию точности

    # Получаем индексы ботов из списка по убыванию точности в данном запуске генетики sval:
    indexes_best = []
    for i in range(len(sval)):
      indexes_best.append(best_bots_accuracy_list.index(sval[i]))

    # Получаем список моделей по ботам
    models_curr_list = []
    for i in curr_models:
      models_curr_list.append(i[0])

    # Получаем отсортированный список моделей по убыванию точности
    best_models = []
    for i in indexes_best:
      best_models.append(models_curr_list[i])

    ind_best = indexes_best[0]                                # Индекс лучшего бота в популяции
    ind_worst = indexes_best[-1]                              # Индекс худшего бота в популяции
    worst_val = sorted(best_bots_accuracy_list, reverse=0)    # Сортируем best_bots_accuracy_list по возрастанию точности
    
    current_mean_val = mean(best_bots_accuracy_list)          # Средняя точность ботов на каждом запуске по кол-ву запусков
    current_max_val = max(best_bots_accuracy_list)            # Лучшая из лучших точностей ботов на каждом запуске по кол-ву запусков
    mean_val.append(current_mean_val)
    max_val.append(current_max_val)
    # сохраняем текущую популяцию ботов и их лучшую аккураси по итогам всех запусков одной популяции на гугл драйв
    bots_accuracy_df = pd.DataFrame(
      {'bots': popul,
      'accuracy': best_bots_accuracy_list
      })
    base_filename = 'bots_accuracy_df.csv'
    os.path.join(link, base_filename)
    bots_accuracy_df.to_csv(os.path.join(link, base_filename), index=False)
    
    # Выводим точность 
    print("запуск номер ", (int(it)+1), " Секунд на запуск: ", int(time.time() - curr_time), " лучший бот - ", popul[ind_best]) 
    print(" Средняя точность ботов на последней эпохе ", current_mean_val,  "худший бот в данном запуске: ", popul[ind_worst])
    print(" Лучшая точность ботов на последней эпохе ", current_max_val)
    print("model_summary лучшей модели ", best_models[0].summary()) 
    
    newpopul = []                         # Создаем пустой список под новую популяцию
    for i in range(nsurv):                # Пробегаем по всем выжившим ботам
      index = best_bots_accuracy_list.index(sval[i])          # Получаем индекс очередного бота из списка лучших в списке val
      newpopul.append(popul[index])       # Добавляем в новую популяцию бота из popul с индексом index
      
    for i in range(nnew):                 # Проходимся в цикле nnew-раз  
      indexp1 = random.randint(0,nsurv-1) # Случайный индекс первого родителя в диапазоне от 0 до nsurv - 1
      indexp2 = random.randint(0,nsurv-1) # Случайный индекс первого родителя в диапазоне от 0 до nsurv - 1
      botp1 = newpopul[indexp1]           # Получаем первого бота-родителя по indexp1
      botp2 = newpopul[indexp2]           # Получаем второго бота-родителя по indexp2    
      newbot = []                         # Создаем пустой список под значения нового бота    
      net4Mut = createRandomNet()         # Создаем случайную сеть для мутаций
      for j in range(l):                  # Пробегаем по всей длине размерности (84)      
        x = 0      
        pindex = random.random()          # Получаем случайное число в диапазоне от 0 до 1

        # Если pindex меньше 0.5, то берем значения от первого бота, иначе от второго
        if pindex < 0.5:
          x = botp1[j]
        else:
          x = botp2[j]
        
        # С вероятностью mut устанавливаем значение бота из net4Mut
        if (random.random() < mut):
          x = net4Mut[j]
          
        newbot.append(x)                  # Добавляем очередное значение в нового бота      
      newpopul.append(newbot)             # Добавляем бота в новую популяцию      
    popul = newpopul                      # Записываем в popul новую посчитанную популяцию

  final_best_models = []
  for i in range(best_models_num):        # Пробегаем по всем моделям из последнего запуска
    index = best_bots_accuracy_list.index(sval[i])            # Получаем индекс модели из списка лучших в списке best_bots_accuracy_list
    final_best_models.append(best_models[index])# Добавляем в best_models модель с индексом index
  best_bot = popul[ind_best]
  return best_models, mean_val, max_val, best_bot
  
def visualize_mean_accuracy(mean_val, max_val):
  import matplotlib.pyplot as plt
  # Создание полотна для рисунка
  plt.figure(1, figsize=(8, 10))

  plt.plot(mean_val, label='Среднее значение точности на проверочной выборке')
  plt.plot(max_val, label='Лучшее значение точности на проверочной выборке')
  # Задание подписей осей 
  plt.xlabel('Эпоха обучения')
  plt.ylabel('Значение точности')
  plt.legend()

  # Фиксация графиков и рисование всей картинки
  plt.show()


def Recovery_Conv_Net(text_train, text_test, WIN_SIZE = 1000, WIN_HOP = 100, CLASS_COUNT = 6, vocab_size_list = [1000, 5000], embedding_subsets = False, BoW_subsets = True,
                      ep=10, verb = 1, n = 20, nsurv = 10, epohs = 5, times_for_popul = 3, best_models_num = 3, BATCH_SIZE = 128, Bow_or_Embedding0 = 0,  Bow_or_Embedding1=0,
                      link = '/content/drive/MyDrive/GA_folder', first_dense_size_low = 2, first_dense_size_high = 9, activation_list = ['softmax','sigmoid','linear','relu','tanh'],
                      final_activation_list = ['softmax','sigmoid'], embedding_size_low = 20, embedding_size_high = 100, layers_list = ["Conv1D", "LSTM", "Bidirectional", "Dense"], 
                      ConvSize_low = 2, ConvSize_high = 8, Kernel_size_low= 2, Kernel_size_high= 5, paddingType_list = ["same", "valid"], LSTM_units_low = 2, LSTM_units_high = 9, 
                      if_second_after_emb = 0, if_third_after_emb = 0, flatten_layers_list = ["Flatten", "GlobalMaxPooling1D", "GlobalAveragePooling1D", "LSTM"], denseSize_after_emb_low = 2,
                      denseSize_after_emb_high = 9, if_second_dense_after_BoW = 1, if_third_dense_after_BoW = 1, if_first_second_layer_after_emb = 1, if_first_third_layer_after_emb = 1, 
                      if_second_second_layer_after_emb = 1, if_second_third_layer_after_emb = 1, if_third_second_layer_after_emb = 1, if_third_third_layer_after_emb = 1, mut = 0.01):

  import random as random                          # Генератор рандомных чисел
  from google.colab import files                   # Для загрузки своей картинки
  import numpy as np                               # Библиотека работы с массивами
  import time                                      # Для подсчета времени
  from statistics import mean                      # Для подсчета среднего значения
  import gdown                                     # Подключение модуля для загрузки данных из облака
  import tensorflow
  import pandas as pd
  from tensorflow.keras.layers import Dense, Dropout, SpatialDropout1D, BatchNormalization, Embedding, Flatten, Activation
  from tensorflow.keras.layers import LSTM, Bidirectional, Conv1D, MaxPooling1D, GlobalMaxPooling1D, SpatialDropout1D, GlobalAveragePooling1D
  # Токенизатор для преобразование текстов в последовательности
  from tensorflow.keras.preprocessing.text import Tokenizer
  # Функции операционной системы
  import os
  # Регулярные выражения
  import re
  # Вывод объектов в ячейке colab
  from sklearn.model_selection import train_test_split
  from tensorflow.keras.models import Sequential   # Сеть прямого распространения
  from keras.utils.vis_utils import plot_model
  from tensorflow.keras import utils               # Используем для to_categorical
  import matplotlib.pyplot as plt                  # Для отрисовки графиков

  # функция по созданию выборки для обучения на эмбеддингах
  # данная функция подготавливает выборки для обучения на эмбеддингах. В нее подаются тексты, а на выходе мы получаем тренировочную
  # и тестовую выборки, разделенные окном WIN_SIZE с шагом WIN_HOP
  def create_sequence_for_embedding(text_train, text_test, VOCAB_SIZE):
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, filters='!"#$%&()*+,-–—./…:;<=>?@[\\]^_`{|}~«»\t\n\xa0\ufeff', lower=True, split=' ', oov_token='неизвестное_слово', char_level=False)
      # Построение частотного словаря по обучающим текстам
    tokenizer.fit_on_texts(text_train)
      # Построение словаря в виде пар слово - индекс
    items = list(tokenizer.word_index.items())
      # Преобразование обучающих и проверочных текстов текст в последовательности индексов согласно частотному словарю
    seq_train = tokenizer.texts_to_sequences(text_train)
    seq_test = tokenizer.texts_to_sequences(text_test)
      # Функция разбиения последовательности на отрезки скользящим окном
      # На входе - последовательность индексов, размер окна, шаг окна
    def split_sequence(sequence, win_size, hop):
      # Последовательность разбивается на части до последнего полного окна
      return [sequence[i:i + win_size] for i in range(0, len(sequence) - win_size + 1, hop)]
    # Функция формирования выборок из последовательностей индексов
    # формирует выборку отрезков и соответствующих им меток классов в виде one hot encoding
    def vectorize_sequence(seq_list, win_size, hop):
      # В списке последовательности следуют в порядке их классов
      # Всего последовательностей в списке ровно столько, сколько классов
      class_count = len(seq_list)

      # Списки для исходных векторов и категориальных меток класса
      x, y = [], []
      # Для каждого класса:
      for cls in range(class_count):
          # Разбиение последовательности класса cls на отрезки
          vectors = split_sequence(seq_list[cls], win_size, hop)
          # Добавление отрезков в выборку
          x += vectors
          if class_count == 2:
              y += [cls] * len(vectors)
          # Для всех отрезков класса cls добавление меток класса в виде OHE
          else:
            y += [utils.to_categorical(cls, class_count)] * len(vectors)


      # Возврат результатов как numpy-массивов
      return np.array(x), np.array(y)
    # Формирование обучающей выборки
    x_train_emb, y_train = vectorize_sequence(seq_train, WIN_SIZE, WIN_HOP) 
      # Формирование тестовой выборки
    x_test_emb, y_test = vectorize_sequence(seq_test, WIN_SIZE, WIN_HOP)
    return x_train_emb, y_train, x_test_emb, y_test

  # функция по созданию выборки для обучения на BAG OF WORDS.
  def create_sequence_for_BoW(text_train, text_test, VOCAB_SIZE):
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, filters='!"#$%&()*+,-–—./…:;<=>?@[\\]^_`{|}~«»\t\n\xa0\ufeff', lower=True, split=' ', oov_token='неизвестное_слово', char_level=False)
    tokenizer.fit_on_texts(text_train)
      # Построение словаря в виде пар слово - индекс
    items = list(tokenizer.word_index.items())
      # Преобразование обучающих и проверочных текстов текст в последовательности индексов согласно частотному словарю
    seq_train = tokenizer.texts_to_sequences(text_train)
    seq_test = tokenizer.texts_to_sequences(text_test)
      # Функция разбиения последовательности на отрезки скользящим окном
      # На входе - последовательность индексов, размер окна, шаг окна
    def split_sequence(sequence, win_size, hop):
      # Последовательность разбивается на части до последнего полного окна
      return [sequence[i:i + win_size] for i in range(0, len(sequence) - win_size + 1, hop)]
    # Функция формирования выборок из последовательностей индексов
    # формирует выборку отрезков и соответствующих им меток классов в виде one hot encoding
    def vectorize_sequence(seq_list, win_size, hop):
      # В списке последовательности следуют в порядке их классов
      # Всего последовательностей в списке ровно столько, сколько классов
      class_count = len(seq_list)
      # Списки для исходных векторов и категориальных меток класса
      x, y = [], []
      # Для каждого класса:
      for cls in range(class_count):
          # Разбиение последовательности класса cls на отрезки
          vectors = split_sequence(seq_list[cls], win_size, hop)
          # Добавление отрезков в выборку
          x += vectors
          if class_count == 2:
              y += [cls] * len(vectors)
          # Для всех отрезков класса cls добавление меток класса в виде OHE
          else:
            y += [utils.to_categorical(cls, class_count)] * len(vectors)


      # Возврат результатов как numpy-массивов
      return np.array(x), np.array(y)
    # Формирование обучающей выборки
    x_train_emb, y_train = vectorize_sequence(seq_train, WIN_SIZE, WIN_HOP) 
      # Формирование тестовой выборки
    x_test_emb, y_test = vectorize_sequence(seq_test, WIN_SIZE, WIN_HOP)
    x_train_BoW = tokenizer.sequences_to_matrix(x_train_emb.tolist())
    x_test_BoW = tokenizer.sequences_to_matrix(x_test_emb.tolist())
    return x_train_BoW, y_train, x_test_BoW, y_test

  # если нужны заранее приготовленные выборки для обучения на эмбеддингах:
  if embedding_subsets == True:
    # создаем выборки по разному размеру словаря - vocab_size_list - для обучения на эмбеддингах
    emb_seq_list = []
    for v_size in vocab_size_list:
      emb_seq_list.append(create_sequence_for_embedding(text_train, text_test, VOCAB_SIZE=v_size))

  # если нужны заранее приготовленные выборки для обучения на BoW:
  if BoW_subsets == True:
    # создаем выборки по разному размеру словаря - vocab_size_list - для обучения на эмбеддингах
    BoW_seq_list = []
    for v_size in vocab_size_list:
      BoW_seq_list.append(create_sequence_for_BoW(text_train, text_test, VOCAB_SIZE=v_size))
  
  def createRandomNet():
  
    net = []
    net.append(random.randint(Bow_or_Embedding0,Bow_or_Embedding1))     # Используем Bag of words или Embedding             net[0] 0 - BoW, 1 - embedding
    net.append(random.randint(first_dense_size_low, first_dense_size_high))  # Количество нейронов в 1 dense блоке               net[1]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации Dense слоя первого блока        net[2]
    net.append(random.randint(0,1))                                     # Делаем ли Dropout в первом блоке                  net[3]
    net.append(random.randint(0,4))                                     # Процент Dropout в первом слое 1 блока             net[4]
    net.append(random.randint(0,1))                                     # Делаем ли нормализацию в первом блоке             net[5]

    net.append(random.randint(0,if_second_dense_after_BoW))             # Делаем ли второй Dense блок                       net[6]
    net.append(random.randint(first_dense_size_low, first_dense_size_high))  # Количество нейронов во 2 dense блоке              net[7]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации Dense слоя второго блока        net[8]
    net.append(random.randint(0,1))                                     # Делаем ли Dropout во 2 блоке                      net[9]
    net.append(random.randint(0,4))                                     # Процент Dropout во 2 блоке                        net[10]
    net.append(random.randint(0,1))                                     # Делаем ли нормализацию в 2 блоке                  net[11]

    net.append(random.randint(0,if_third_dense_after_BoW))              # Делаем ли третий Dense блок                       net[12]
    net.append(random.randint(first_dense_size_low, first_dense_size_high)) # Количество нейронов в 3 dense блоке               net[13]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации Dense слоя третьего блока       net[14]
    net.append(random.randint(0,1))                                     # Делаем ли Dropout в 3 блоке                       net[15]
    net.append(random.randint(0,4))                                     # Процент Dropout в 3 блоке                         net[16]
    net.append(random.randint(0,1))                                     # Делаем ли нормализацию в 3 блоке                  net[17]
    net.append(random.randint(0,(len(final_activation_list)-1)))        # Функция активации выходного слоя                  net[18]

    net.append(random.randint(embedding_size_low, embedding_size_high)) # Размер вектора для эмбеддинга                     net[19]
    net.append(random.randint(0,1))                                     # Делаем ли Spatialdropout после слоя Embedding     net[20]
    net.append(random.randint(0,1))                                     # Добавляем ли Batchnorm после слоя Embedding       net[21]

    net.append(random.randint(0,(len(layers_list)-1)))                  # Какой из слоев из списка layers_list добавляем  в первом блоке net[22]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров первого Conv1D в первом блоке      net[23]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size первого свёрточного слоя в первом блоке      net[24]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для первого слоя первого блока       net[25]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого слоя первого блока      net[26]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров второго Conv1D в первом блоке      net[27]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size второго свёрточного слоя в первом блоке      net[28]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для второго слоя первого блока       net[29]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго слоя первого блока      net[30]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров третьего Conv1D в первом блоке     net[31]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size третьего свёрточного слоя в первом блоке     net[32]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для третьего слоя первого блока      net[33]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего слоя первого блока     net[34]

    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 1 слое LSTM 1 блока         net[35]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов во 2 слое LSTM 1 блока        net[36]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 3 слое LSTM 1 блока         net[37]
    net.append(random.randint(0,4))                                     # размер spatialDropout после Embedding             net[38]
    net.append(random.randint(0,1))                                     # Делаем ли Maxpooling в 1 блоке                    net[39]
    net.append(random.randint(2,4))                                     # Pool_size для Maxpooling1D в 1 блоке              net[40]

    net.append(random.randint(0,if_second_after_emb))                   # Делаем ли второй блок после Embedding             net[41]
    net.append(random.randint(0,(len(layers_list)-1)))                  # Какой из слоев из списка layers_list добавляем  во втором блоке net[42]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров первого Conv1D во втором блоке     net[43]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size первого свёрточного слоя во втором блоке     net[44]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для первого слоя во втором блоке     net[45]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого слоя во втором блоке    net[46] 

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров второго Conv1D во втором блоке     net[47]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size второго свёрточного слоя во втором блоке     net[48]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для второго слоя во втором блоке     net[49]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго слоя во втором блоке    net[50]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров третьего Conv1D во втором блоке    net[51]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size третьего свёрточного слоя во втором блоке    net[52]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для третьего слоя во втором блоке    net[53]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего слоя во втором блоке   net[54]

    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 1 слое LSTM во втором блоке net[55]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов во 2 слое LSTM во втором блоке net[56]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 3 слое LSTM во втором блоке net[57]

    net.append(random.randint(0,1))                                     # Делаем ли maxpooling для второго блока            net[58]
    net.append(random.randint(2,4))                                     # Размер MaxPooling для второго блока               net[59]

    net.append(random.randint(0,if_third_after_emb))                    # Делаем ли третий блок после Embedding             net[60]
    net.append(random.randint(0,(len(layers_list)-1)))                  # Какой из слоев из списка layers_list добавляем  в третьем блоке net[61]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров первого Conv1D в третьем блоке     net[62]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size первого свёрточного слоя в третьем блоке     net[63]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для первого слоя в третьем блоке     net[64]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого слоя в третьем блоке    net[65] 

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров второго Conv1D в третьем блоке     net[66]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size второго свёрточного слоя в третьем блоке     net[67]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для второго слоя в третьем блоке     net[68]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго слоя в третьем блоке    net[69]

    net.append(random.randint(ConvSize_low, ConvSize_high))             # Количество фильтров третьего Conv1D в третьем блоке    net[70]
    net.append(random.randint(Kernel_size_low, Kernel_size_high))       # Kernel_size третьего свёрточного слоя в третьем блоке    net[71]
    net.append(random.randint(0,(len(paddingType_list)-1)))             # Тип паддинга для третьего слоя в третьем блоке    net[72]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего слоя в третьем блоке   net[73]

    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 1 слое LSTM в третьем блоке net[74]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов во 2 слое LSTM в третьем блоке net[75]
    net.append(random.randint(LSTM_units_low, LSTM_units_high))         # Количество нейронов в 3 слое LSTM в третьем блоке net[76]

    net.append(random.randint(0,1))                                     # Делаем ли maxpooling для третьего блока            net[77]
    net.append(random.randint(2,4))                                     # Размер MaxPooling для третьего блока               net[78]
    
    net.append(random.randint(0,(len(flatten_layers_list)-1)))          # Тип выравнивающего слоя Flatten, GlobalMax, GlobalAverage или LSTM  net[79]
    net.append(random.randint(0,(len(vocab_size_list)-1)))              # Какую выборку подаем сети (должно соответствовать vocab_size_list) net[80]

    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units первого Dense слоя в первом блоке (степень числа 2)            net[81]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого Dense слоя в первом блоке net[82]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units второго Dense слоя в первом блоке (степень числа 2)           net[83]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго Dense слоя в первом блоке net[84]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units третьего Dense слоя в первом блоке (степень числа 2)           net[85]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего Dense слоя в первом блоке net[86]

    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units первого Dense слоя во втором блоке (степень числа 2)           net[87]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого Dense слоя во втором блоке net[88]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units второго Dense слоя во втором блоке (степень числа 2)            net[89]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго Dense слоя во втором блоке net[90]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units третьего Dense слоя во втором блоке (степень числа 2)           net[91]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего Dense слоя во втором блоке net[92]

    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units первого Dense слоя в третьем блоке (степень числа 2)           net[93]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации первого Dense слоя в третьем блоке net[94]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units второго Dense слоя в третьем блоке (степень числа 2)           net[95]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации второго Dense слоя в третьем блоке net[96]
    net.append(random.randint(denseSize_after_emb_low, denseSize_after_emb_high)) # Параметр units третьего Dense слоя в третьем блоке (степень числа 2)           net[97]
    net.append(random.randint(0,(len(activation_list)-1)))              # Функция активации третьего Dense слоя в третьем блоке net[98]

    net.append(random.randint(0,0))                                     # запускаем алгоритм при уже созданных датасетах или создаем в боте net[99]
    net.append(random.randint(0,if_first_second_layer_after_emb))       # Добавляем ли второй слой в первый блок при эмбеддингах    net[100] 
    net.append(random.randint(0,if_first_third_layer_after_emb))        # Добавляем ли третий слой в первый блок при эмбеддингах    net[101] 
    net.append(random.randint(0,if_second_second_layer_after_emb))      # Добавляем ли второй слой во второй блок при эмбеддингах    net[102] 
    net.append(random.randint(0,if_second_third_layer_after_emb))       # Добавляем ли третий слой во второй блок при эмбеддингах    net[103] 
    net.append(random.randint(0,if_third_second_layer_after_emb))       # Добавляем ли второй слой в третий блок при эмбеддингах    net[104] 
    net.append(random.randint(0,if_third_third_layer_after_emb))        # Добавляем ли третий слой в третий блок при эмбеддингах    net[105] 

    return net

  # Создаём сеть (net - список параметров - бот)

  def createConvNet(net):

    model = Sequential()             # Создаем модель Sequential
    
    BoW_or_Embedding = net[0]         # Используем Bag of words или Embedding. '0'- Bag of words, '1'- Embedding
    first_dense_size = 2 **net[1]     # Количество нейронов в dense слое 1 блока
    first_dense_activation = net[2]   # Функция активации первого слоя первого блока
    if_first_dropout = net[3]         # Делаем ли Dropout в первом блоке
    first_dropout_size = net[4]       # Процент Dropout в 1 блоке
    if_first_batchnorm = net[5]       # Делаем ли нормализацию в первом блоке

    if_second_dense = net[6]          # Делаем ли второй Dense блок                     
    second_dense_size = 2 **net[7]    # Количество нейронов в dense слое 2 блока
    second_dense_activation = net[8]  # Функция активации второго dense блока
    if_second_dropout = net[9]        # Делаем ли Dropout во втором блоке
    second_dropout_size = net[10]     # Процент Dropout во 2 блоке
    if_second_batchnorm = net[11]     # Делаем ли нормализацию во втором блоке

    if_third_dense = net[12]          # Делаем ли третий Dense блок
    third_dense_size = 2 **net[13]    # Количество нейронов в dense слое 3 блока
    third_dense_activation = net[14]  # Функция активации третьего dense блока
    if_third_dropout = net[15]        # Делаем ли Dropout в третьем блоке
    third_dropout_size = net[16]      # Процент Dropout в 3 блоке
    if_third_batchnorm = net[17]      # Делаем ли нормализацию в третьем блоке    
    last_activation = net[18]         # Функция активации выходного слоя  

    embedding_size = net[19]          # Размер вектора эмбеддинг    
    if_spatialdropout = net[20]       # Делаем ли Spatialdropout после слоя Embedding
    embedding_batchnorm = net[21]     # Добавляем ли нормализацию по батчу после слоя Embedding
    first_layer_type = net[22]        # Какой из слоев из списка layers_list добавляем в первом блоке

    firstConvSize0 = 2 ** net[23]     # Количество фильтров первого Conv1D в первом блоке
    firstConvKernel0 = net[24]        # kernel_size первого свёрточного слоя в первом блоке
    firstPaddingType0 = net[25]       # Тип паддинга для первого слоя первого блока
    firstActivation0 = net[26]        # Функция активации первого слоя первого блока

    firstDenseSize0 = 2 ** net[81]    # Размер первого Dense слоя в первом блоке
    firstDenseActivation0 = net[82]   # Функция активации первого Dense слоя в первом блоке

    firstConvSize1 = 2 ** net[27]     # Количество фильтров второго Conv1D в первом блоке
    firstConvKernel1 = net[28]        # kernel_size второго свёрточного слоя в первом блоке
    firstPaddingType1 = net[29]       # Тип паддинга для второго слоя первого блока
    firstActivation1 = net[30]        # Функция активации второго слоя первого блока

    firstDenseSize1 = 2 ** net[83]    # Размер первого Dense слоя в первом блоке
    firstDenseActivation1 = net[84]   # Функция активации первого Dense слоя в первом блоке

    firstConvSize2 = 2 ** net[31]     # Количество фильтров третьего Conv1D в первом блоке
    firstConvKernel2 = net[32]        # kernel_size третьего свёрточного слоя в первом блоке
    firstPaddingType2 = net[33]       # Тип паддинга для третьего слоя первого блока
    firstActivation2 = net[34]        # Функция активации третьего слоя первого блока

    firstDenseSize2 = 2 ** net[85]    # Размер первого Dense слоя в первом блоке
    firstDenseActivation2 = net[86]   # Функция активации первого Dense слоя в первом блоке

    first_LSTM_size_0 = 2 ** net[35]  # Количество нейронов в 1 слое LSTM 1 блока
    first_LSTM_size_1 = 2 ** net[36]  # Количество нейронов во 2 слое LSTM 1 блока
    first_LSTM_size_2 = 2 ** net[37]  # Количество нейронов в 3 слое LSTM 1 блока

    spatialDropout_size = net[38]     # размер spatialDropout после Embedding
    makeMaxPooling0 = net[39]         # Делаем ли maxpooling для первого блока
    maxPoolingSize0 = net[40]         # Размер MaxPooling для первого блока

    if_second_block = net[41]         # Делаем ли второй блок после Embedding
    second_layer_type = net[42]       # Какой из слоев из списка layers_list добавляем в первом блоке

    secondConvSize0 = 2 ** net[43]     # Размер свертки первого Conv1D во втором блоке
    secondConvKernel0 = net[44]        # Ядро первого свёрточного слоя во втором блоке
    secondPaddingType0 = net[45]       # Тип паддинга для первого слоя во втором блоке
    secondActivation0 = net[46]        # Функция активации первого слоя во втором блоке

    secondDenseSize0 = 2 ** net[87]    # Размер первого Dense слоя во втором блоке
    secondDenseActivation0 = net[88]   # Функция активации первого Dense слоя во втором блоке

    secondConvSize1 = 2 ** net[47]     # Размер свертки второго Conv1D во втором блоке
    secondConvKernel1 = net[48]        # Ядро второго свёрточного слоя во втором блоке
    secondPaddingType1 = net[49]       # Тип паддинга для второго слоя во втором блоке
    secondActivation1 = net[50]        # Функция активации второго слоя во втором блоке

    secondDenseSize1 = 2 ** net[89]    # Размер второго Dense слоя во втором блоке
    secondDenseActivation1 = net[90]   # Функция активации второго Dense слоя во втором блоке

    secondConvSize2 = 2 ** net[51]     # Размер свертки третьего Conv1D во втором блоке
    secondConvKernel2 = net[52]        # Ядро третьего свёрточного слоя во втором блоке
    secondPaddingType2 = net[53]       # Тип паддинга для третьего слоя во втором блоке
    secondActivation2 = net[54]        # Функция активации третьего слоя во втором блоке

    secondDenseSize2 = 2 ** net[91]    # Размер третьего Dense слоя во втором блоке
    secondDenseActivation2 = net[92]   # Функция активации третьего Dense слоя во втором блоке

    second_LSTM_size_0 = 2 ** net[55]  # Количество нейронов в 1 слое LSTM во втором блоке
    second_LSTM_size_1 = 2 ** net[56]  # Количество нейронов во 2 слое LSTM во втором блоке
    second_LSTM_size_2 = 2 ** net[57]  # Количество нейронов в 3 слое LSTM во втором блоке

    makeMaxPooling1 = net[58]         # Делаем ли maxpooling для второго блока
    maxPoolingSize1 = net[59]         # Размер MaxPooling для второго блока


    if_third_block = net[60]         # Делаем ли третий блок после Embedding
    third_layer_type = net[61]       # Какой из слоев из списка layers_list добавляем в третьем блоке

    thirdConvSize0 = 2 ** net[62]     # Размер свертки первого Conv1D в третьем блоке
    thirdConvKernel0 = net[63]        # Ядро первого свёрточного слоя в третьем блоке
    thirdPaddingType0 = net[64]       # Тип паддинга для первого слоя в третьем блоке
    thirdActivation0 = net[65]        # Функция активации первого слоя в третьем блоке

    thirdDenseSize0 = 2 ** net[93]    # Размер первого Dense слоя в третьем блоке
    thirdDenseActivation0 = net[94]   # Функция активации первого Dense слоя в третьем блоке

    thirdConvSize1 = 2 ** net[66]     # Размер свертки второго Conv1D в третьем блоке
    thirdConvKernel1 = net[67]        # Ядро второго свёрточного слоя в третьем блоке
    thirdPaddingType1 = net[68]       # Тип паддинга для второго слоя в третьем блоке
    thirdActivation1 = net[69]        # Функция активации второго слоя в третьем блоке

    thirdDenseSize1 = 2 ** net[95]    # Размер второго Dense слоя в третьем блоке
    thirdDenseActivation1 = net[96]   # Функция активации второго Dense слоя в третьем блоке

    thirdConvSize2 = 2 ** net[70]     # Размер свертки третьего Conv1D в третьем блоке
    thirdConvKernel2 = net[71]        # Ядро третьего свёрточного слоя в третьем блоке
    thirdPaddingType2 = net[72]       # Тип паддинга для третьего слоя в третьем блоке
    thirdActivation2 = net[73]        # Функция активации третьего слоя в третьем блоке

    thirdDenseSize2 = 2 ** net[97]    # Размер третьего Dense слоя в третьем блоке
    thirdDenseActivation2 = net[98]   # Функция активации третьего Dense слоя в третьем блоке

    third_LSTM_size_0 = 2 ** net[74]  # Количество нейронов в 1 слое LSTM в третьем блоке
    third_LSTM_size_1 = 2 ** net[75]  # Количество нейронов во 2 слое LSTM в третьем блоке
    third_LSTM_size_2 = 2 ** net[76]  # Количество нейронов в 3 слое LSTM в третьем блоке

    makeMaxPooling2 = net[77]         # Делаем ли maxpooling для третьего блока
    maxPoolingSize2 = net[78]         # Размер MaxPooling для третьего блока

    flatten_globalmax_globalaver_lstm_choise  = net[79]         # тип выравнивающего слоя
    vocab_size_choise = net[80]       # Выборку с каким объемом словаря используем при обучении (1000, 5000, 10000 слов) должно соответствовать vocab_size_list
    if_create_dataset = net[99]       # Запускаем алгоритм при уже созданных датасетах или создаем в боте. 0 - на уже созданных выборках
    if_first_second_layer = net[100]  # Добавляем ли второй слой в первый блок при эмбеддингах    net[100] 
    if_first_third_layer = net[101]   # Добавляем ли третий слой в первый блок при эмбеддингах    net[101] 
    if_second_second_layer = net[102] # Добавляем ли второй слой во второй блок при эмбеддингах    net[102] 
    if_second_third_layer = net[103]  # Добавляем ли третий слой во второй блок при эмбеддингах    net[103] 
    if_third_second_layer = net[104]  # Добавляем ли второй слой в третий блок при эмбеддингах    net[104] 
    if_third_third_layer = net[105]   # Добавляем ли третий слой в третий блок при эмбеддингах    net[105] 
    

    #activation_list = ['softmax','sigmoid','linear','relu','tanh']  # какие функции активации тестируем в полносвязных слоях 
    #final_activation_list = ['softmax','sigmoid']                   # какие функции активации тестируем в полносвязных слоях
    dropout_list = [0.05, 0.1, 0.3, 0.4, 0.5]
    #layers_list = ["Conv1D", "LSTM", "Bidirectional", "Dense"]               # какие слои используем в блоках после Embedding
    #paddingType_list = ["same", "valid"]                            # какие типы паддингов тестируем в сверточных блоках
    #flatten_globalmax_globalaver_lstm = ["Flatten", "GlobalMaxPooling1D", "GlobalAveragePooling1D", "LSTM"] # тестируем Flatten, GlobalMaxPooling1D, GlobalAveragePooling1D или LSTM
    # Если используем Bag of words:
    if (BoW_or_Embedding!=1):   
      # первый полносвязный блок
      model.add(Dense(first_dense_size, input_dim=vocab_size_list[vocab_size_choise], activation=activation_list[first_dense_activation])) 
      if (if_first_dropout!=0):
        model.add(Dropout(dropout_list[first_dropout_size]))
      if (if_first_batchnorm!=0):
        model.add(BatchNormalization())
      # второй полносвязный блок
      if (if_second_dense!=0):
        model.add(Dense(second_dense_size, activation=activation_list[second_dense_activation]))
        if (if_second_dropout!=0):
          model.add(Dropout(dropout_list[second_dropout_size]))
        if (if_second_batchnorm!=0):
          model.add(BatchNormalization())
      # третий полносвязный блок
      if (if_third_dense!=0):
        model.add(Dense(third_dense_size, activation=activation_list[third_dense_activation]))
        if (if_third_dropout!=0):
          model.add(Dropout(dropout_list[third_dropout_size]))
        if (if_third_batchnorm!=0):
          model.add(BatchNormalization())
    else:
      model.add(Embedding(vocab_size_list[vocab_size_choise], embedding_size, input_length=WIN_SIZE)) # Добавим эмбеддинг
      if (if_spatialdropout!=0):
        model.add(SpatialDropout1D(dropout_list[spatialDropout_size])) # Добавим дропаут для целых векторов в эмбеддинг пространстве
      if (embedding_batchnorm!=0):
        model.add(BatchNormalization())                             # Добавим нормализацию по батчу
      # формируем первый блок из 3-х слоев на выбор сети: Conv1D, LSTM, BidirectionalLSTM, Dense
      if (layers_list[first_layer_type]) == "Conv1D":
        model.add(Conv1D(firstConvSize0, firstConvKernel0, activation=activation_list[firstActivation0], padding=paddingType_list[firstPaddingType0]))
        if (if_first_second_layer!=0):
          model.add(Conv1D(firstConvSize1, firstConvKernel1, activation=activation_list[firstActivation1], padding=paddingType_list[firstPaddingType1]))
        if (if_first_third_layer!=0):
          model.add(Conv1D(firstConvSize2, firstConvKernel2, activation=activation_list[firstActivation2], padding=paddingType_list[firstPaddingType2]))
      if (layers_list[first_layer_type]) == "LSTM":
        model.add(LSTM(first_LSTM_size_0, return_sequences=1))
        if (if_first_second_layer!=0):
          model.add(LSTM(first_LSTM_size_1, return_sequences=1))
        if (if_first_third_layer!=0):
          model.add(LSTM(first_LSTM_size_2, return_sequences=1))
      if (layers_list[first_layer_type]) == "Bidirectional":
        model.add(Bidirectional(LSTM(first_LSTM_size_0, return_sequences=True)))
        if (if_first_second_layer!=0):
          model.add(Bidirectional(LSTM(first_LSTM_size_1, return_sequences=True)))
        if (if_first_third_layer!=0):  
          model.add(Bidirectional(LSTM(first_LSTM_size_2, return_sequences=True)))
      if (layers_list[first_layer_type]) == "Dense":
        model.add(Dense(firstDenseSize0, activation=activation_list[firstDenseActivation0]))
        if (if_first_second_layer!=0):
          model.add(Dense(firstDenseSize1, activation=activation_list[firstDenseActivation1]))
        if (if_first_third_layer!=0):
          model.add(Dense(firstDenseSize2, activation=activation_list[firstDenseActivation2]))
      if (makeMaxPooling0!=0):
        model.add(MaxPooling1D(maxPoolingSize0))
      if (if_first_dropout!=0):
        model.add(Dropout(dropout_list[first_dropout_size]))
      if (if_first_batchnorm!=0):
        model.add(BatchNormalization()) 

      # если делаем второй блок после Embedding
      if (if_second_block!=0):
        if (layers_list[second_layer_type]) == "Conv1D":
          model.add(Conv1D(secondConvSize0, secondConvKernel0, activation=activation_list[secondActivation0], padding=paddingType_list[secondPaddingType0]))
          if (if_second_second_layer!=0):
            model.add(Conv1D(secondConvSize1, secondConvKernel1, activation=activation_list[secondActivation1], padding=paddingType_list[secondPaddingType1]))
          if (if_second_third_layer!=0):  
            model.add(Conv1D(secondConvSize2, secondConvKernel2, activation=activation_list[secondActivation2], padding=paddingType_list[secondPaddingType2]))
        if (layers_list[second_layer_type]) == "LSTM":
          model.add(LSTM(second_LSTM_size_0, return_sequences=1))
          if (if_second_second_layer!=0):
            model.add(LSTM(second_LSTM_size_1, return_sequences=1))
          if (if_second_third_layer!=0):
            model.add(LSTM(second_LSTM_size_2, return_sequences=1))
        if (layers_list[second_layer_type]) == "Bidirectional":
          model.add(Bidirectional(LSTM(second_LSTM_size_0, return_sequences=True)))
          if (if_second_second_layer!=0):
            model.add(Bidirectional(LSTM(second_LSTM_size_1, return_sequences=True)))
          if (if_second_third_layer!=0):
            model.add(Bidirectional(LSTM(second_LSTM_size_2, return_sequences=True))) 
        if (layers_list[first_layer_type]) == "Dense":
          model.add(Dense(secondDenseSize0, activation=activation_list[secondDenseActivation0]))
          if (if_second_second_layer!=0):
            model.add(Dense(secondDenseSize1, activation=activation_list[secondDenseActivation1]))
          if (if_second_third_layer!=0):
            model.add(Dense(secondDenseSize2, activation=activation_list[secondDenseActivation2]))
        if (makeMaxPooling1!=0):
          model.add(MaxPooling1D(maxPoolingSize1))
        if (if_second_dropout!=0):
          model.add(Dropout(dropout_list[second_dropout_size]))
        if (if_second_batchnorm!=0):
          model.add(BatchNormalization()) 

      # если делаем третий блок после Embedding
      if (if_third_block!=0):
        if (layers_list[third_layer_type]) == "Conv1D":
          model.add(Conv1D(thirdConvSize0, thirdConvKernel0, activation=activation_list[thirdActivation0], padding=paddingType_list[thirdPaddingType0]))
          if (if_third_second_layer!=0):
            model.add(Conv1D(thirdConvSize1, thirdConvKernel1, activation=activation_list[thirdActivation1], padding=paddingType_list[thirdPaddingType1]))
          if (if_third_third_layer!=0):
            model.add(Conv1D(thirdConvSize2, thirdConvKernel2, activation=activation_list[thirdActivation2], padding=paddingType_list[thirdPaddingType2]))
        if (layers_list[third_layer_type]) == "LSTM":
          model.add(LSTM(third_LSTM_size_0, return_sequences=1))
          if (if_third_second_layer!=0):
            model.add(LSTM(third_LSTM_size_1, return_sequences=1))
          if (if_third_third_layer  !=0):
            model.add(LSTM(third_LSTM_size_2, return_sequences=1))
        if (layers_list[third_layer_type]) == "Bidirectional":
          model.add(Bidirectional(LSTM(third_LSTM_size_0, return_sequences=True)))
          if (if_third_second_layer!=0):
            model.add(Bidirectional(LSTM(third_LSTM_size_1, return_sequences=True)))
          if (if_third_third_layer  !=0):
            model.add(Bidirectional(LSTM(third_LSTM_size_2, return_sequences=True))) 
        if (layers_list[first_layer_type]) == "Dense":
          model.add(Dense(thirdDenseSize0, activation=activation_list[thirdDenseActivation0]))
          if (if_third_second_layer!=0):
            model.add(Dense(thirdDenseSize1, activation=activation_list[thirdDenseActivation1]))
          if (if_third_third_layer  !=0):
            model.add(Dense(thirdDenseSize2, activation=activation_list[thirdDenseActivation2]))
        if (makeMaxPooling2!=0):
          model.add(MaxPooling1D(maxPoolingSize2))
        if (if_second_dropout!=0):
          model.add(Dropout(dropout_list[third_dropout_size]))
        if (if_third_batchnorm!=0):
          model.add(BatchNormalization()) 
      if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="Flatten"):
        model.add(Flatten())   
      if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="GlobalMaxPooling1D"):
        model.add(GlobalMaxPooling1D()) 
      if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="GlobalAveragePooling1D"):
        model.add(GlobalAveragePooling1D())   
      if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="LSTM"):
        model.add(LSTM(4))  
    if CLASS_COUNT == 2:
      cl_count=1
    else:
      cl_count=CLASS_COUNT
    model.add(Dense(cl_count, activation=final_activation_list[last_activation]))
    return model

  def evaluateNet(net):
    if CLASS_COUNT>2:
      LOSS='categorical_crossentropy'
    else:
      LOSS='binary_crossentropy'
    val = 0
    time.time()
    model = createConvNet(net) # Создаем модель createConvNet
    # если выборки НЕ создаются в боте:
    if (net[99]==0):
      # если обучаем на BoW:
      if net[0]==0:
        x_train = BoW_seq_list[net[80]][0]
        x_test = BoW_seq_list[net[80]][2]
        y_train = BoW_seq_list[net[80]][1]
        y_test = BoW_seq_list[net[80]][3]
      else:
        x_train = emb_seq_list[net[80]][0]
        x_test = emb_seq_list[net[80]][2]
        y_train = emb_seq_list[net[80]][1]
        y_test = emb_seq_list[net[80]][3]
    # если выборки создаются в боте:
    else:
      # если обучаем на BoW:
      if net[0]==0:
        x_train, y_train, x_test, y_test = create_sequence_for_BoW(text_train, text_test, VOCAB_SIZE=vocab_size_list[net[80]])
      else:
        x_train, y_train, x_test, y_test = create_sequence_for_embedding(text_train, text_test, VOCAB_SIZE=vocab_size_list[net[80]])
    # Компилируем сеть
    model.compile(loss=LOSS, optimizer='rmsprop', metrics=['accuracy'])

    # Обучаем сеть на датасете 
    history = model.fit(x_train, 
                        y_train, 
                        batch_size=BATCH_SIZE, 
                        epochs=ep,
                        validation_data=(x_test, y_test),
                        verbose=1)
      
    val = history.history["val_accuracy"][-1] # Возвращаем точность на проверочной выборке с последней эпохи
    return val, model                         # Возвращаем точность и модель
  nnew = n - nsurv    # Количество новых (столько новых ботов создается)
  l = 106              # Размер бота
  #epohs = 3           # Количество запусков генетики
  #times_for_popul = 2 # Количество запусков одной популяции
  #mut = 0.01          # Коэффициент мутаций
  #best_models_num = 3 # Сколько лучших моделей мы хотим получить по итогам всех запусков
  #worst_models_num = 3# Сколько худших моделей мы хотим получить по итогам всех запусков
  popul = []          # Массив популяции
  val = []            # Одномерный массив значений точности этих ботов
  mean_val = []       # Массив со средними точностями по запускам
  max_val = []        # Массив с лучшими точностями по запускам
  best_models  =[]    # 3 лучших модели по итогам всех запусков

  from google.colab import drive
  import os.path
  from os import path
  import pandas as pd
  import ast

  drive.mount('/content/drive')
  base_filename = 'bots_accuracy_df.csv'

  df=pd.read_csv(os.path.join(link, base_filename))

  popul_col = df['bots'].tolist()
  new_bots_list = []
  for i in popul_col:
    new_bots_list.append(ast.literal_eval(i))

  accuracy_col = df['accuracy'].tolist()
  popul = new_bots_list
  best_bots_accuracy_list = accuracy_col

  sval = sorted(best_bots_accuracy_list, reverse=1)         # Сортируем best_bots_accuracy_list по убыванию точности

  # Получаем индексы ботов из списка по убыванию точности в данном запуске генетики sval:
  indexes_best = []
  for i in range(len(sval)):
    indexes_best.append(best_bots_accuracy_list.index(sval[i]))

  worst_val = sorted(best_bots_accuracy_list, reverse=0)    # Сортируем best_bots_accuracy_list по возрастанию точности
  current_mean_val = mean(best_bots_accuracy_list)          # Средняя точность ботов на каждом запуске по кол-ву запусков
  current_max_val = max(best_bots_accuracy_list)            # Лучшая из лучших точностей ботов на каждом запуске по кол-ву запусков
  mean_val.append(current_mean_val)
  max_val.append(current_max_val)

  newpopul = []                         # Создаем пустой список под новую популяцию
  for i in range(nsurv):                # Пробегаем по всем выжившим ботам
    index = best_bots_accuracy_list.index(sval[i])          # Получаем индекс очередного бота из списка лучших в списке val
    newpopul.append(popul[index])       # Добавляем в новую популяцию бота из popul с индексом index
      
  for i in range(nnew):                 # Проходимся в цикле nnew-раз  
    indexp1 = random.randint(0,nsurv-1) # Случайный индекс первого родителя в диапазоне от 0 до nsurv - 1
    indexp2 = random.randint(0,nsurv-1) # Случайный индекс первого родителя в диапазоне от 0 до nsurv - 1
    botp1 = newpopul[indexp1]           # Получаем первого бота-родителя по indexp1
    botp2 = newpopul[indexp2]           # Получаем второго бота-родителя по indexp2    
    newbot = []                         # Создаем пустой список под значения нового бота    
    net4Mut = createRandomNet()         # Создаем случайную сеть для мутаций
    for j in range(l):                  # Пробегаем по всей длине размерности (84)      
      x = 0      
      pindex = random.random()          # Получаем случайное число в диапазоне от 0 до 1

      # Если pindex меньше 0.5, то берем значения от первого бота, иначе от второго
      if pindex < 0.5:
        x = botp1[j]
      else:
        x = botp2[j]
        
        # С вероятностью mut устанавливаем значение бота из net4Mut
      if (random.random() < mut):
        x = net4Mut[j]
          
      newbot.append(x)                  # Добавляем очередное значение в нового бота      
    newpopul.append(newbot)             # Добавляем бота в новую популяцию      
  popul = newpopul                      # Записываем в popul новую посчитанную популяцию

  for it in range(epohs):                 # Пробегаем по всем запускам генетики
    #val = []                             # список с точностями ботов на проверочной выборке с последней эпохи
    curr_time = time.time()
    curr_models=[[] for _ in range(n)]    # список с моделями из данного запуска
    bots_accuracy_list = [[] for _ in range(n)] # создаем список с n пустыми списками под точности бота

    # для каждого бота создается список, в который будут добавляться точности на каждом запуске:
    
    for j in range(times_for_popul):
      for i in range(n):                    # Пробегаем в цикле по всем ботам 
        bot = popul[i]                      # Берем очередного бота
        f, model_sum = evaluateNet(bot) # Вычисляем точность текущего бота на последней эпохе и получаем обученную модель
        #val.append(f)                       # Добавляем полученное значение в список val
        bots_accuracy_list[i].append(f)
        curr_models[i].append(model_sum)       # Добавляем текущую модель в список с моделями curr_models
    best_bots_accuracy_list = []            # список из лучших точностей по каждому боту
    for acc in bots_accuracy_list:
      best_bots_accuracy_list.append(max(acc))

    #best_curr_models = []
    sval = sorted(best_bots_accuracy_list, reverse=1)         # Сортируем best_bots_accuracy_list по убыванию точности

    # Получаем индексы ботов из списка по убыванию точности в данном запуске генетики sval:
    indexes_best = []
    for i in range(len(sval)):
      indexes_best.append(best_bots_accuracy_list.index(sval[i]))

    # Получаем список моделей по ботам
    models_curr_list = []
    for i in curr_models:
      models_curr_list.append(i[0])

    # Получаем отсортированный список моделей по убыванию точности
    best_models = []
    for i in indexes_best:
      best_models.append(models_curr_list[i])

    ind_best = indexes_best[0]                                # Индекс лучшего бота в популяции
    ind_worst = indexes_best[-1]                              # Индекс худшего бота в популяции
    worst_val = sorted(best_bots_accuracy_list, reverse=0)    # Сортируем best_bots_accuracy_list по возрастанию точности
    
    current_mean_val = mean(best_bots_accuracy_list)          # Средняя точность ботов на каждом запуске по кол-ву запусков
    current_max_val = max(best_bots_accuracy_list)            # Лучшая из лучших точностей ботов на каждом запуске по кол-ву запусков
    mean_val.append(current_mean_val)
    max_val.append(current_max_val)
    # сохраняем текущую популяцию ботов и их лучшую аккураси по итогам всех запусков одной популяции на гугл драйв
    bots_accuracy_df = pd.DataFrame(
      {'bots': popul,
      'accuracy': best_bots_accuracy_list
      })
    base_filename = 'bots_accuracy_df.csv'
    os.path.join(link, base_filename)
    bots_accuracy_df.to_csv(os.path.join(link, base_filename), index=False)
    
    # Выводим точность 
    print("запуск номер ", (int(it)+1), " Секунд на запуск: ", int(time.time() - curr_time), " лучший бот - ", popul[ind_best]) 
    print(" Средняя точность ботов на последней эпохе ", current_mean_val,  "худший бот в данном запуске: ", popul[ind_worst])
    print(" Лучшая точность ботов на последней эпохе ", current_max_val)
    print("model_summary лучшей модели ", best_models[0].summary(), "model_summary худшей модели ", best_models[-1].summary()) 
    best_bot = popul[ind_best]
    
    newpopul = []                         # Создаем пустой список под новую популяцию
    for i in range(nsurv):                # Пробегаем по всем выжившим ботам
      index = best_bots_accuracy_list.index(sval[i])          # Получаем индекс очередного бота из списка лучших в списке val
      newpopul.append(popul[index])       # Добавляем в новую популяцию бота из popul с индексом index
      
    for i in range(nnew):                 # Проходимся в цикле nnew-раз  
      indexp1 = random.randint(0,nsurv-1) # Случайный индекс первого родителя в диапазоне от 0 до nsurv - 1
      indexp2 = random.randint(0,nsurv-1) # Случайный индекс первого родителя в диапазоне от 0 до nsurv - 1
      botp1 = newpopul[indexp1]           # Получаем первого бота-родителя по indexp1
      botp2 = newpopul[indexp2]           # Получаем второго бота-родителя по indexp2    
      newbot = []                         # Создаем пустой список под значения нового бота    
      net4Mut = createRandomNet()         # Создаем случайную сеть для мутаций
      for j in range(l):                  # Пробегаем по всей длине размерности (84)      
        x = 0      
        pindex = random.random()          # Получаем случайное число в диапазоне от 0 до 1

        # Если pindex меньше 0.5, то берем значения от первого бота, иначе от второго
        if pindex < 0.5:
          x = botp1[j]
        else:
          x = botp2[j]
        
        # С вероятностью mut устанавливаем значение бота из net4Mut
        if (random.random() < mut):
          x = net4Mut[j]
          
        newbot.append(x)                  # Добавляем очередное значение в нового бота      
      newpopul.append(newbot)             # Добавляем бота в новую популяцию      
    popul = newpopul                      # Записываем в popul новую посчитанную популяцию

  final_best_models = []
  for i in range(best_models_num):        # Пробегаем по всем моделям из последнего запуска
    index = best_bots_accuracy_list.index(sval[i])            # Получаем индекс модели из списка лучших в списке best_bots_accuracy_list
    final_best_models.append(best_models[index])# Добавляем в best_models модель с индексом index


  return best_models, mean_val, max_val, best_bot            # Функция возвращает 3 лучшие и 3 худшие модели, массив со средними и лучшими точностями по запускам

'''
Функция расшифровки значений бота 
'''
def best_bot_decoding(net, activation_list = ['softmax','sigmoid','linear','relu','tanh'], paddingType_list = ["same", "valid"], 
                      dropout_list = [0.05, 0.1, 0.3, 0.4, 0.5], CLASS_COUNT=6, WIN_SIZE=1000, 
                      flatten_layers_list = ["Flatten", "GlobalMaxPooling1D", "GlobalAveragePooling1D", "LSTM"],
                      layers_list = ["Conv1D", "LSTM", "Bidirectional", "Dense"], final_activation_list = ['softmax','sigmoid'], vocab_size_list = [1000, 5000]):
  
  print("model = Sequential()")             
  BoW_or_Embedding = net[0]         # Используем Bag of words или Embedding. '0'- Bag of words, '1'- Embedding
  first_dense_size = 2 **net[1]     # Количество нейронов в dense слое 1 блока
  first_dense_activation = net[2]   # Функция активации первого слоя первого блока
  if_first_dropout = net[3]         # Делаем ли Dropout в первом блоке
  first_dropout_size = net[4]       # Процент Dropout в 1 блоке
  if_first_batchnorm = net[5]       # Делаем ли нормализацию в первом блоке

  if_second_dense = net[6]          # Делаем ли второй Dense блок                     
  second_dense_size = 2 **net[7]    # Количество нейронов в dense слое 2 блока
  second_dense_activation = net[8]  # Функция активации второго dense блока
  if_second_dropout = net[9]        # Делаем ли Dropout во втором блоке
  second_dropout_size = net[10]     # Процент Dropout во 2 блоке
  if_second_batchnorm = net[11]     # Делаем ли нормализацию во втором блоке

  if_third_dense = net[12]          # Делаем ли третий Dense блок
  third_dense_size = 2 **net[13]    # Количество нейронов в dense слое 3 блока
  third_dense_activation = net[14]  # Функция активации третьего dense блока
  if_third_dropout = net[15]        # Делаем ли Dropout в третьем блоке
  third_dropout_size = net[16]      # Процент Dropout в 3 блоке
  if_third_batchnorm = net[17]      # Делаем ли нормализацию в третьем блоке    
  last_activation = net[18]         # Функция активации выходного слоя  

  embedding_size = net[19]          # Размер вектора эмбеддинг    
  if_spatialdropout = net[20]       # Делаем ли Spatialdropout после слоя Embedding
  embedding_batchnorm = net[21]     # Добавляем ли нормализацию по батчу после слоя Embedding
  first_layer_type = net[22]        # Какой из слоев из списка layers_list добавляем в первом блоке

  firstConvSize0 = 2 ** net[23]     # Количество фильтров первого Conv1D в первом блоке
  firstConvKernel0 = net[24]        # kernel_size первого свёрточного слоя в первом блоке
  firstPaddingType0 = net[25]       # Тип паддинга для первого слоя первого блока
  firstActivation0 = net[26]        # Функция активации первого слоя первого блока

  firstDenseSize0 = 2 ** net[81]    # Размер первого Dense слоя в первом блоке
  firstDenseActivation0 = net[82]   # Функция активации первого Dense слоя в первом блоке

  firstConvSize1 = 2 ** net[27]     # Количество фильтров второго Conv1D в первом блоке
  firstConvKernel1 = net[28]        # kernel_size второго свёрточного слоя в первом блоке
  firstPaddingType1 = net[29]       # Тип паддинга для второго слоя первого блока
  firstActivation1 = net[30]        # Функция активации второго слоя первого блока

  firstDenseSize1 = 2 ** net[83]    # Размер первого Dense слоя в первом блоке
  firstDenseActivation1 = net[84]   # Функция активации первого Dense слоя в первом блоке

  firstConvSize2 = 2 ** net[31]     # Количество фильтров третьего Conv1D в первом блоке
  firstConvKernel2 = net[32]        # kernel_size третьего свёрточного слоя в первом блоке
  firstPaddingType2 = net[33]       # Тип паддинга для третьего слоя первого блока
  firstActivation2 = net[34]        # Функция активации третьего слоя первого блока

  firstDenseSize2 = 2 ** net[85]    # Размер первого Dense слоя в первом блоке
  firstDenseActivation2 = net[86]   # Функция активации первого Dense слоя в первом блоке

  first_LSTM_size_0 = 2 ** net[35]  # Количество нейронов в 1 слое LSTM 1 блока
  first_LSTM_size_1 = 2 ** net[36]  # Количество нейронов во 2 слое LSTM 1 блока
  first_LSTM_size_2 = 2 ** net[37]  # Количество нейронов в 3 слое LSTM 1 блока

  spatialDropout_size = net[38]     # размер spatialDropout после Embedding
  makeMaxPooling0 = net[39]         # Делаем ли maxpooling для первого блока
  maxPoolingSize0 = net[40]         # Размер MaxPooling для первого блока

  if_second_block = net[41]         # Делаем ли второй блок после Embedding
  second_layer_type = net[42]       # Какой из слоев из списка layers_list добавляем в первом блоке

  secondConvSize0 = 2 ** net[43]     # Размер свертки первого Conv1D во втором блоке
  secondConvKernel0 = net[44]        # Ядро первого свёрточного слоя во втором блоке
  secondPaddingType0 = net[45]       # Тип паддинга для первого слоя во втором блоке
  secondActivation0 = net[46]        # Функция активации первого слоя во втором блоке

  secondDenseSize0 = 2 ** net[87]    # Размер первого Dense слоя во втором блоке
  secondDenseActivation0 = net[88]   # Функция активации первого Dense слоя во втором блоке

  secondConvSize1 = 2 ** net[47]     # Размер свертки второго Conv1D во втором блоке
  secondConvKernel1 = net[48]        # Ядро второго свёрточного слоя во втором блоке
  secondPaddingType1 = net[49]       # Тип паддинга для второго слоя во втором блоке
  secondActivation1 = net[50]        # Функция активации второго слоя во втором блоке

  secondDenseSize1 = 2 ** net[89]    # Размер второго Dense слоя во втором блоке
  secondDenseActivation1 = net[90]   # Функция активации второго Dense слоя во втором блоке

  secondConvSize2 = 2 ** net[51]     # Размер свертки третьего Conv1D во втором блоке
  secondConvKernel2 = net[52]        # Ядро третьего свёрточного слоя во втором блоке
  secondPaddingType2 = net[53]       # Тип паддинга для третьего слоя во втором блоке
  secondActivation2 = net[54]        # Функция активации третьего слоя во втором блоке

  secondDenseSize2 = 2 ** net[91]    # Размер третьего Dense слоя во втором блоке
  secondDenseActivation2 = net[92]   # Функция активации третьего Dense слоя во втором блоке

  second_LSTM_size_0 = 2 ** net[55]  # Количество нейронов в 1 слое LSTM во втором блоке
  second_LSTM_size_1 = 2 ** net[56]  # Количество нейронов во 2 слое LSTM во втором блоке
  second_LSTM_size_2 = 2 ** net[57]  # Количество нейронов в 3 слое LSTM во втором блоке

  makeMaxPooling1 = net[58]         # Делаем ли maxpooling для второго блока
  maxPoolingSize1 = net[59]         # Размер MaxPooling для второго блока


  if_third_block = net[60]         # Делаем ли третий блок после Embedding
  third_layer_type = net[61]       # Какой из слоев из списка layers_list добавляем в третьем блоке

  thirdConvSize0 = 2 ** net[62]     # Размер свертки первого Conv1D в третьем блоке
  thirdConvKernel0 = net[63]        # Ядро первого свёрточного слоя в третьем блоке
  thirdPaddingType0 = net[64]       # Тип паддинга для первого слоя в третьем блоке
  thirdActivation0 = net[65]        # Функция активации первого слоя в третьем блоке

  thirdDenseSize0 = 2 ** net[93]    # Размер первого Dense слоя в третьем блоке
  thirdDenseActivation0 = net[94]   # Функция активации первого Dense слоя в третьем блоке

  thirdConvSize1 = 2 ** net[66]     # Размер свертки второго Conv1D в третьем блоке
  thirdConvKernel1 = net[67]        # Ядро второго свёрточного слоя в третьем блоке
  thirdPaddingType1 = net[68]       # Тип паддинга для второго слоя в третьем блоке
  thirdActivation1 = net[69]        # Функция активации второго слоя в третьем блоке

  thirdDenseSize1 = 2 ** net[95]    # Размер второго Dense слоя в третьем блоке
  thirdDenseActivation1 = net[96]   # Функция активации второго Dense слоя в третьем блоке

  thirdConvSize2 = 2 ** net[70]     # Размер свертки третьего Conv1D в третьем блоке
  thirdConvKernel2 = net[71]        # Ядро третьего свёрточного слоя в третьем блоке
  thirdPaddingType2 = net[72]       # Тип паддинга для третьего слоя в третьем блоке
  thirdActivation2 = net[73]        # Функция активации третьего слоя в третьем блоке

  thirdDenseSize2 = 2 ** net[97]    # Размер третьего Dense слоя в третьем блоке
  thirdDenseActivation2 = net[98]   # Функция активации третьего Dense слоя в третьем блоке

  third_LSTM_size_0 = 2 ** net[74]  # Количество нейронов в 1 слое LSTM в третьем блоке
  third_LSTM_size_1 = 2 ** net[75]  # Количество нейронов во 2 слое LSTM в третьем блоке
  third_LSTM_size_2 = 2 ** net[76]  # Количество нейронов в 3 слое LSTM в третьем блоке

  makeMaxPooling2 = net[77]         # Делаем ли maxpooling для третьего блока
  maxPoolingSize2 = net[78]         # Размер MaxPooling для третьего блока

  flatten_globalmax_globalaver_lstm_choise  = net[79]         # тип выравнивающего слоя
  vocab_size_choise = net[80]       # Выборку с каким объемом словаря используем при обучении (1000, 5000, 10000 слов) должно соответствовать vocab_size_list
  if_create_dataset = net[99]       # Запускаем алгоритм при уже созданных датасетах или создаем в боте. 0 - на уже созданных выборках
  if_first_second_layer = net[100]  # Добавляем ли второй слой в первый блок при эмбеддингах    net[100] 
  if_first_third_layer = net[101]   # Добавляем ли третий слой в первый блок при эмбеддингах    net[101] 
  if_second_second_layer = net[102] # Добавляем ли второй слой во второй блок при эмбеддингах    net[102] 
  if_second_third_layer = net[103]  # Добавляем ли третий слой во второй блок при эмбеддингах    net[103] 
  if_third_second_layer = net[104]  # Добавляем ли второй слой в третий блок при эмбеддингах    net[104] 
  if_third_third_layer = net[105]   # Добавляем ли третий слой в третий блок при эмбеддингах    net[105] 

  if (BoW_or_Embedding!=1):   
    # первый полносвязный блок
    print(f"model.add(Dense({first_dense_size}, input_dim={vocab_size_list[vocab_size_choise]}, activation={activation_list[first_dense_activation]}))") 
    if (if_first_dropout!=0):
      print(f"model.add(Dropout({dropout_list[first_dropout_size]}))")
    if (if_first_batchnorm!=0):
      print(f"model.add(BatchNormalization())")
    # второй полносвязный блок
    if (if_second_dense!=0):
      print(f"model.add(Dense({second_dense_size}, activation={activation_list[second_dense_activation]}))")
      if (if_second_dropout!=0):
        print(f"model.add(Dropout({dropout_list[second_dropout_size]}))")
      if (if_second_batchnorm!=0):
        print(f"model.add(BatchNormalization())")
    # третий полносвязный блок
    if (if_third_dense!=0):
      print(f"model.add(Dense({third_dense_size}, activation={activation_list[third_dense_activation]}))")
      if (if_third_dropout!=0):
        print(f"model.add(Dropout({dropout_list[third_dropout_size]}))")
      if (if_third_batchnorm!=0):
        print(f"model.add(BatchNormalization())")
  else:
    print(f"model.add(Embedding({vocab_size_list[vocab_size_choise]}, {embedding_size}, input_length={WIN_SIZE}))") # Добавим эмбеддинг
    if (if_spatialdropout!=0):
      print(f"model.add(SpatialDropout1D({dropout_list[spatialDropout_size]}))") # Добавим дропаут для целых векторов в эмбеддинг пространстве
    if (embedding_batchnorm!=0):
      print(f"model.add(BatchNormalization())")                            # Добавим нормализацию по батчу
    # формируем первый блок из 3-х слоев на выбор сети: Conv1D, LSTM, BidirectionalLSTM, Dense
    if (layers_list[first_layer_type]) == "Conv1D":
      print(f"model.add(Conv1D({firstConvSize0}, {firstConvKernel0}, activation={activation_list[firstActivation0]}, padding={paddingType_list[firstPaddingType0]}))")
      if (if_first_second_layer!=0):
        print(f"model.add(Conv1D({firstConvSize1}, {firstConvKernel1}, activation={activation_list[firstActivation1]}, padding={paddingType_list[firstPaddingType1]}))")
      if (if_first_third_layer!=0):
        print(f"model.add(Conv1D({firstConvSize2}, {firstConvKernel2}, activation={activation_list[firstActivation2]}, padding={paddingType_list[firstPaddingType2]}))")
    if (layers_list[first_layer_type]) == "LSTM":
      print(f"model.add(LSTM({first_LSTM_size_0}, return_sequences=1))")
      if (if_first_second_layer!=0):
        print(f"model.add(LSTM({first_LSTM_size_1}, return_sequences=1))")
      if (if_first_third_layer!=0):
        print(f"model.add(LSTM({first_LSTM_size_2}, return_sequences=1))")
    if (layers_list[first_layer_type]) == "Bidirectional":
      print(f"model.add(Bidirectional(LSTM({first_LSTM_size_0}, return_sequences=True)))")
      if (if_first_second_layer!=0):
        print(f"model.add(Bidirectional(LSTM({first_LSTM_size_1}, return_sequences=True)))")
      if (if_first_third_layer!=0):
        print(f"model.add(Bidirectional(LSTM({first_LSTM_size_2}, return_sequences=True)))")
    if (layers_list[first_layer_type]) == "Dense":
      print(f"model.add(Dense({firstDenseSize0}, activation={activation_list[firstDenseActivation0]}))")
      if (if_first_second_layer!=0):
        print(f"model.add(Dense({firstDenseSize1}, activation={activation_list[firstDenseActivation1]}))")
      if (if_first_third_layer!=0):
        print(f"model.add(Dense({firstDenseSize2}, activation={activation_list[firstDenseActivation2]}))")
    if (makeMaxPooling0!=0):
      print(f"model.add(MaxPooling1D({maxPoolingSize0}))")
    if (if_first_dropout!=0):
      print(f"model.add(Dropout({dropout_list[first_dropout_size]}))")
    if (if_first_batchnorm!=0):
      print(f"model.add(BatchNormalization())")

    # если делаем второй блок после Embedding
    if (if_second_block!=0):
      if (layers_list[second_layer_type]) == "Conv1D":
        print(f"model.add(Conv1D({secondConvSize0}, {secondConvKernel0}, activation={activation_list[secondActivation0]}, padding={paddingType_list[secondPaddingType0]}))")
        if (if_second_second_layer!=0):
          print(f"model.add(Conv1D({secondConvSize1}, {secondConvKernel1}, activation={activation_list[secondActivation1]}, padding={paddingType_list[secondPaddingType1]}))")
        if (if_second_third_layer!=0):
          print(f"model.add(Conv1D({secondConvSize2}, {secondConvKernel2}, activation={activation_list[secondActivation2]}, padding={paddingType_list[secondPaddingType2]}))")
      if (layers_list[second_layer_type]) == "LSTM":
        print(f"model.add(LSTM({second_LSTM_size_0}, return_sequences=1))")
        if (if_second_second_layer!=0):
          print(f"model.add(LSTM({second_LSTM_size_1}, return_sequences=1))")
        if (if_second_third_layer!=0):
          print(f"model.add(LSTM({second_LSTM_size_2}, return_sequences=1))")
      if (layers_list[second_layer_type]) == "Bidirectional":
        print(f"model.add(Bidirectional(LSTM({second_LSTM_size_0}, return_sequences=True)))")
        if (if_second_second_layer!=0):
          print(f"model.add(Bidirectional(LSTM({second_LSTM_size_1}, return_sequences=True)))")
        if (if_second_third_layer!=0):
          print(f"model.add(Bidirectional(LSTM({second_LSTM_size_2}, return_sequences=True)))")
      if (layers_list[first_layer_type]) == "Dense":
        print(f"model.add(Dense({secondDenseSize0}, activation={activation_list[secondDenseActivation0]}))")
        if (if_second_second_layer!=0):
          print(f"model.add(Dense({secondDenseSize1}, activation={activation_list[secondDenseActivation1]}))")
        if (if_second_third_layer!=0):
          print(f"model.add(Dense({secondDenseSize2}, activation={activation_list[secondDenseActivation2]}))")
      if (makeMaxPooling1!=0):
        print(f"model.add(MaxPooling1D({maxPoolingSize1}))")
      if (if_second_dropout!=0):
        print(f"model.add(Dropout({dropout_list[second_dropout_size]}))")
      if (if_second_batchnorm!=0):
        print(f"model.add(BatchNormalization())")
    # если делаем третий блок после Embedding
    if (if_third_block!=0):
      if (layers_list[third_layer_type]) == "Conv1D":
        print(f"model.add(Conv1D({thirdConvSize0}, {thirdConvKernel0}, activation={activation_list[thirdActivation0]}, padding={paddingType_list[thirdPaddingType0]}))")
        if (if_third_second_layer!=0):
          print(f"model.add(Conv1D({thirdConvSize1}, {thirdConvKernel1}, activation={activation_list[thirdActivation1]}, padding={paddingType_list[thirdPaddingType1]}))")
        if (if_third_third_layer!=0):
          print(f"model.add(Conv1D({thirdConvSize2}, {thirdConvKernel2}, activation={activation_list[thirdActivation2]}, padding={paddingType_list[thirdPaddingType2]}))")
      if (layers_list[third_layer_type]) == "LSTM":
        print(f"model.add(LSTM({third_LSTM_size_0}, return_sequences=1))")
        if (if_third_second_layer!=0):
          print(f"model.add(LSTM({third_LSTM_size_1}, return_sequences=1))")
        if (if_third_third_layer!=0):
          print(f"model.add(LSTM({third_LSTM_size_2}, return_sequences=1))")
      if (layers_list[third_layer_type]) == "Bidirectional":
        print(f"model.add(Bidirectional(LSTM({third_LSTM_size_0}, return_sequences=True)))")
        if (if_third_second_layer!=0):
          print(f"model.add(Bidirectional(LSTM({third_LSTM_size_1}, return_sequences=True)))")
        if (if_third_third_layer!=0):
          print(f"model.add(Bidirectional(LSTM({third_LSTM_size_2}, return_sequences=True)))")
      if (layers_list[first_layer_type]) == "Dense":
        print(f"model.add(Dense({thirdDenseSize0}, activation={activation_list[thirdDenseActivation0]}))")
        if (if_third_second_layer!=0):
          print(f"model.add(Dense({thirdDenseSize1}, activation={activation_list[thirdDenseActivation1]}))")
        if (if_third_third_layer!=0):
          print(f"model.add(Dense({thirdDenseSize2}, activation={activation_list[thirdDenseActivation2]}))")
      if (makeMaxPooling2!=0):
        print(f"model.add(MaxPooling1D({maxPoolingSize2}))")
      if (if_second_dropout!=0):
        print(f"model.add(Dropout({dropout_list[third_dropout_size]}))")
      if (if_third_batchnorm!=0):
        print(f"model.add(BatchNormalization())")
    if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="Flatten"):
      print(f"model.add(Flatten())")   
    if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="GlobalMaxPooling1D"):
      print(f"model.add(GlobalMaxPooling1D())") 
    if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="GlobalAveragePooling1D"):
      print(f"model.add(GlobalAveragePooling1D())")  
    if (flatten_layers_list[flatten_globalmax_globalaver_lstm_choise]=="LSTM"):
      print(f"model.add(LSTM(4))")
  if CLASS_COUNT == 2:
    cl_count=1
  else:
    cl_count=CLASS_COUNT
  print(f"model.add(Dense({cl_count}, activation={final_activation_list[last_activation]}))")

    
  if CLASS_COUNT == 2:
    print(f"model.compile(loss=tf.keras.losses.BinaryCrossentropy, optimizer=tf.keras.optimizers.rmsprop(), metrics=['accuracy'])")
  else:
    print(f"model.compile(loss=tf.keras.losses.CategoricalCrossentropy, optimizer=tf.keras.optimizers.rmsprop(), metrics=['accuracy'])")