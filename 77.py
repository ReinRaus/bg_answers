data = {
    "colors": [ "Красный", "Зеленый", "Белый", "Желтый", "Синий" ],
    "pets": [ "Собака", "Птица", "Кошка", "Лошадь", "Рыбка" ],
    "nation": [ "Англичанин", "Швед", "Датчанин", "Норвежец", "Немец" ],
    "cigare": [ "Pall Mall", "Dunhill", "Blend", "Bluemaster", "Prince" ],
    "napit": [ "Чай", "Кофе", "Молоко", "Пиво", "Вода" ],
    "order": [ 1, 2, 3, 4, 5 ]
}
# 4-ёх мерный массив с доступом по: graph[category1][value1][category2][value2], содержит True при инициализации
graph = { i: { j: { k: { m:True for m in data[k] } for k in data if not k==i } for j in data[i] } for i in data }

def printer( isFinal = False):
    if not isFinal: print( '            colors pets   nation cigare napit  order' )
    if not isFinal: print( '            КЗБЖС  СПКЛР  АШДНН  PDBBP  ЧКМПВ  12345\n' )
    for i in graph:
        for j in graph[i]:
            print( str(j), ' '*(11-len(str(j))),end = '' )
            for k in data:
                if k == i:
                    if isFinal: print( ' '*12, end = '' )
                    else: print( '     ', end='' )
                else:
                    mark = 'O' if len( getLinks( graph[i][j][k] )[1] )==1 else 'X'
                    for l in graph[i][j][k]:
                        if graph[i][j][k][l]:
                            if isFinal: print( str(l), ' '*(11-len(str(l))),end = '' )
                            else: print( mark, end='' )
                        elif not isFinal: print( ' ', end='' )
                print( '  ', end='' )
            print()
        print()
    if not isFinal: print( '            КЗБЖС  СПКЛР  АШДНН  PDBBP  ЧКМПВ  12345' )
    if not isFinal: print( '            colors pets   nation cigare napit  order' )

def getLinks( cat ):
    return [
        [k for k in cat if not cat[k] ],
        [k for k in cat if cat[k] ]
    ]

# одно значение ставим в True, остальные в False
def positiveLink( cat, val, cat2, val2 ):
    changed = False
    for i in graph[cat][val][cat2]:
        v = i==val2
        if not graph[cat][val][cat2][i] == v:
            graph[cat][val][cat2][i] = v
            changed = True
    for i in graph[cat2][val2][cat]:
        v = i==val
        if not graph[cat2][val2][cat][i] == v:
            graph[cat2][val2][cat][i] = v
            changed = True
    return changed

def negativeLink( cat1, val1, cat2, val2 ):
    if graph[cat1][val1][cat2][val2] or graph[cat2][val2][cat1][val1]:
        graph[cat1][val1][cat2][val2] = False
        graph[cat2][val2][cat1][val1] = False
        return True
                        
# Если Англичанин не живёт в Жёлтом доме, то в Жёлтом доме живет не Англичанин
def ruleMirrors( cat1, val1, cat2, val2 ):
    if not graph[cat1][val1][cat2][val2] and graph[cat2][val2][cat1][val1]:
        graph[cat2][val2][cat1][val1] = False
        return True

# Если Англичанин живёт в Красном доме, и не держит Собаку, то жилец Красного дома не держит Собаку
def rulePositiveSumm( cat1, val1, cat2 ):
    links = getLinks( graph[cat1][val1][cat2] )
    if len( links[True] ) == 1:
        val2 = links[True][0]
        changed = False
        for i in graph[cat1][val1]:
            for j in graph[cat1][val1][i]:
                if not graph[cat1][val1][i][j] and not i == cat2 and graph[cat2][val2][i][j]:
                    changed = changed or negativeLink( cat2, val2, i, j )
        return changed
    
# проверяет, допустимо ли соседство
def ruleSosedi( cat1, val1, cat2, val2 ):
    changed = negativeLink( cat1, val1, cat2, val2 )
    cat = [cat1, cat2]
    val = [val1, val2]
    for i in range( 0, 1 ):
        j = not i
        sosedIn = set()
        for k in graph[cat[i]][val[i]]['order']:
            if graph[cat[i]][val[i]]['order'][k]:
                left = k - 1
                right = k + 1
                # если рассматриваемый объект может жить в текущем доме, то допустимые левые и правые дома кидаем в сет
                if left > 0 and graph[cat[j]][val[j]]['order'][left]: sosedIn.add(left)
                if right < 6 and graph[cat[j]][val[j]]['order'][right]: sosedIn.add(right)
                # если рассматриваемый объект может жить в текущем доме, но сосед не может жить слева или справа, то исключаем
                if (left > 0 and not graph[cat[j]][val[j]]['order'][left]) and (right < 6 and not graph[cat[j]][val[j]]['order'][right]):
                    changed = changed or negativeLink( cat[i], val[i], 'order', k )
        # если оказалось, что сосед может быть только в одном доме
        if len( sosedIn ) == 1:
            changed = changed or positiveLink( cat[j], val[j], 'order', list(sosedIn)[0] )
    return changed

#rule 4 Зеленый дом находится слева от белого, а белый справа от зеленого, val1 слева от val2
def ruleLeft(cat1, val1, cat2, val2 ):
    changed = negativeLink( cat1, val1, 'order', 5 )
    changed = changed or negativeLink( cat2, val2, 'order', 1 )
    for i in graph[cat1][val1]['order']:
        if graph[cat1][val1]['order'][i]:
            sos = i + 1
            if sos < 6 and not graph[cat2][val2]['order'][sos]:
                changed = changed or negativeLink( cat1, val1, 'order', i )
    for i in graph[cat2][val2]['order']:
        if graph[cat2][val2]['order'][i]:
            sos = i - 1
            if sos > 0 and not graph[cat1][val1]['order'][sos]:
                changed = changed or negativeLink( cat2, val2, 'order', i )
    return changed

positiveLink( "nation", "Англичанин", "colors", "Красный" )    # rule 1
positiveLink( "nation", "Швед",       "pets",   "Собака" )     # rule 2
positiveLink( "nation", "Датчанин",   "napit",  "Чай" )        # rule 3
positiveLink( "colors", "Зеленый",    "napit",  "Кофе" )       # rule 5
positiveLink( "cigare", "Pall Mall",  "pets",   "Птица" )      # rule 6
positiveLink( "colors", "Желтый",     "cigare", "Dunhill" )    # rule 7
positiveLink( "order",  3,            "napit",  "Молоко" )     # rule 8
positiveLink( "nation", "Норвежец",   "order",  1 )            # rule 9
positiveLink( "napit",  "Пиво",       "cigare", "Bluemaster" ) # rule 12
positiveLink( "nation", "Немец",      "cigare", "Prince" )     # rule 13

def process():
    changed = False
    for cat1 in graph:
        for val1 in graph[cat1]:
            for cat2 in graph[cat1][val1]:
                changed = changed or rulePositiveSumm( cat1, val1, cat2 )
                for val2 in graph[cat1][val1][cat2]:
                    changed = changed or ruleMirrors(cat1, val1, cat2, val2)
    changed = changed or ruleLeft(   'colors', 'Зеленый',  'colors', 'Белый'  ) # rule 4
    changed = changed or ruleSosedi( 'cigare', 'Blend',    'pets',   'Кошка'  ) # rule 10
    changed = changed or ruleSosedi( 'cigare', 'Dunhill',  'pets',   'Лошадь' ) # rule 11
    changed = changed or ruleSosedi( 'nation', 'Норвежец', 'colors', 'Синий'  ) # rule 14
    changed = changed or ruleSosedi( 'cigare', 'Blend',    'napit',  'Вода'   ) # rule 15
    return changed

iters = 0
while process():
    iters+= 1
print( 'Iterations:', iters )
    
printer( 1 )
