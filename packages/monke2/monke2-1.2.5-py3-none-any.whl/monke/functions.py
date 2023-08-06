import numpy as np
import math

def roundup(x,r=2):
        a = x*10**r
        a = np.ceil(a)
        a = a*10**(-r)

        if type(x) == float or type(x) == int or type(x) == np.float64:
            if a == 0 :
                a=10**(-r)
        else:
            try:                                           # rundet mehrdimensionale arrays
                for i,j in enumerate(a):
                    for k,l in enumerate(j):
                        if i == 0:  
                            i=10**(-r)
            except:                                        # rundet eindimensionale arrays
                for i,j in enumerate(a):
                    if i == 0:  
                        i=10**(-r)
                    
        return np.around(a,r)

# def varianz_xy(x,x_mean,y,y_mean):
#         return (1/len(x))*((x-x_mean)*(y-y_mean)).sum()

# def varianz_x(x,x_mean):
#     return (1/len(x))*((x-x_mean)**2).sum()
    
def varianz_xy(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    return (1/len(x))*((x-x_mean)*(y-y_mean)).sum()

def varianz_x(x):
    x_mean = np.mean(x)
    return (1/len(x))*((x-x_mean)**2).sum()

def mittel_varianzgewichtet(val,val_err):
    return (val/(val_err**2)).sum()/(1/(val_err**2)).sum()


# Groeßter gemeinsamer Teiler
def gcd(a, b):
    
    k = 0
    while a != int(a) or b != int(b):
        k += 1
        a, b = a*1e1, b*1e1
    a, b = int(a), int(b)
    
    if isinstance(a, int) and isinstance(b, int):
        result = math.gcd(a,b)*10**(-k)
    return result

# Groeßter gemeinsamer Teiler für arrays
def gcd_array(array):

    ggt = []
    n = len(array)
    for i in range(n):
        for j in range(n):
            ggt.append(gcd(array[i],array[j]))
            
    ggt = np.asarray(ggt)
    return min(ggt)

# Passt die Rundung von Werten an die Fehler an, erzeugt strings fertig für tabellen--üBERFLÜSSIG! WURDE ERSETZT DURCH error_round
def errorRound(x, xerr):
    print('veraltet: benutze stattdessen error_round()')
    new_x = [0]*len(x)
    new_x_err = [0]*len(x)
    err_str = [0]*len(x)
    if len(x) == len(xerr):
        for i in range(len(x)):
            floatxerr = xerr.astype(np.float64)                             # ändert type zu float64, weil roundup funktion nicht mit int funktioniert
            errstring = np.format_float_positional(xerr[i])                 # Fehler als String

            #-- rundet Fehler ---
            k = 0
            while (errstring[k] != '.'):
                k += 1
            if (errstring[0] == '1' or errstring[0] == '0'):
                k -= 1
            if errstring[0] == '1' and k == 0:

                new_x_err[i] = roundup(floatxerr[i],1)      # rundet einstelligen Zahlen

                if int(new_x_err[i]) == new_x_err[i]:
                    new_x_err[i] = int(new_x_err[i])   # falls ganzzahlig wird zu int konvertiert
                else:
                    k += 1

            elif (k != 0):
                k = -k
                new_x_err[i] = int(roundup(floatxerr[i],k+1))   # rundet alle Zahlen > 1 auf
                if errstring[0] == '1' and str(new_x_err[i])[0] != '1':
                    k -= 1

            else:
                #print('float',new_x_err[i])
                k = 2                                          # rundet fließkommazahlen < 1
                
                while errstring[k] == '0':
                    k += 1
                k -= 1
                if errstring[k+1] == '1' and round(xerr[i],k) != xerr[i]:
                    new_x_err[i] = roundup(floatxerr[i],k+1)
                    k += 1
                else:
                    new_x_err[i] = roundup(floatxerr[i],k)
                
                errstring = np.format_float_positional(new_x_err[i])
                k = len(errstring) - 2
               
                if new_x_err[i] == int(new_x_err[i]):
                    k = 0                                      # setzt rundungsstelle auf 0, wenn fehler auf 1 gerundet wird
            err_str[i] = np.format_float_positional(new_x_err[i])  
            
            if new_x_err[i] == int(new_x_err[i]):
                err_str[i] = str(int(new_x_err[i]))
                new_x_err[i] = int(new_x_err[i])

            #print(k)
            #--passt nachkommastelle der werte an fehler
            errstring = np.format_float_positional(new_x_err[i])     
            
            if k >= 0:
                new_x[i] = round(x[i],k)
                numformat = '{:.'+str(k)+'f}'
                new_x[i] = numformat.format(new_x[i])
            else:
                new_x[i] = round(x[i],k+1)
                numformat = '{:.'+str(0)+'f}'
                new_x[i] = str(int(new_x[i]))
        
    else:
        print('errorRound: arrays must have same length')

    return new_x, err_str

def error_round(x, xerr, error_mode = 'plus-minus', get_float = False):

    if isinstance(x, (int, float)):
        x = [x]
    if isinstance(xerr, (int, float)):
        xerr = [xerr]
    
    if len(x) != len(xerr):
        print('error_round: beide arrays benötigen dieselbe Länge')
        return 
    
    xerr_sci = [0]*len(x)
    new_xerr = [0]*len(x)
    xerr_str = ['']*len(x)         # gerundete werte als string
    new_x = [0]*len(x)
    x_str = ['']*len(x)

    for i, j in enumerate(xerr):
        xerr_sci[i] = np.format_float_scientific(j)
        this = xerr_sci[i]
        K = ''               # gibt Rundungsstellen an
        last = len(this) -1  # letzer index
        K = this[last-2:]
        K = -int(K)
        if this[0] == '1':
            K +=1
        
        new_xerr[i] = roundup(xerr[i],K)
        xerr_str[i] = np.format_float_positional(new_xerr[i])
        if new_xerr[i] == int(new_xerr[i]):           
            new_xerr[i] = int(new_xerr[i])                  # transformier ganzzahlige floats in ints
            xerr_str[i] = str(new_xerr[i])


        # definiere neues K bei gerundeten Fehlern
        xerr_sci[i] = np.format_float_scientific(new_xerr[i])
        this = xerr_sci[i]
        K = ''               # gibt Rundungsstellen an
        last = len(this) -1  # letzer index
        K = this[last-2:]
        K = -int(K)
        if this[0] == '1' and (this[2] != 'e'):
            K +=1

        # Runde Messwerte
        new_x[i] = round(x[i],K)
        if K >= 0:
            numformat = '{:.'+str(K)+'f}'
            x_str[i] = numformat.format(new_x[i])
        else:
            x_str[i] = str(int(new_x[i]))

        if x_str[i][0] == '-' and new_x[i] == 0:                # entfernt bei -0.0 das minuszeichen
            new_x[i] = -new_x[i]
            x_str[i] = x_str[i][1:]

    if error_mode == 'plus-minus':
        if get_float == False:
            if len(x) != 1:
                return x_str, xerr_str
            else:
                return x_str[0], xerr_str[0]
        else:
            if len(x) != 1:
                return  [float(i) for i in x_str], [float(i) for i in xerr_str]
            else:
                return float(x_str[0]), float(xerr_str[0])
    elif error_mode == 'parenthesis':
        result = []
        for j, i in enumerate(xerr_str):

            error = i.replace('.', '')
            while error[0] == '0':
                error = error[1:]
            result.append(f'{x_str[j]}({error})')
        if len(x) != 1:
            return result
        else:
            return result[0]
        
    elif error_mode == 'scientific':
        res = []
        e_list = []   # Liste aller Potenzen
        for i, j in enumerate(x_str):
            value = float(x_str[i])
            error = xerr_str[i]
            val_str = x_str[i] # wert als string

            e = 0                       # die Potenz
            result = None              # Der Endwert, der ausgegeben wird
            
            first = 0                                   # erste Stelle, die eine Zahl ist
            minus = ''   # fügt ein minus hinzu, falls negativ
            if value < 0:
                first = 1
                minus = '-'
            
            if value != 0:
                while val_str[first] == '0' or val_str[first] == '.':   # macht aus dem Wert eine Zahl der Form #1.01234#
                    first += 1
            else:
                pass
            #print(val_str, len(val_str), first)
            result = f'{minus}{val_str[first]}.'                                                      
            
            for number in val_str[first+1:]:
                if number != '.':
                    result += number
            if result[-1] == '.':
                result = result[:-1]
            #print(result)

            # bestimmt die Potenz
            if abs(value) < 10 and value != 0:
                while abs(value) < 1:
                    e -= 1
                    value = value *1e1
                     #error = error * 1e1
            elif abs(value) >= 10:
                while abs(value) >= 10:
                    e += 1
                    value = value *1e-1
                    
            e_list.append(e) 

            # mache aus dem Fehler einen integer
            error = error.replace('.', '')
            while error[0] == '0':
                error = error[1:]

            if e != 0:
                res.append(f'{result}({error})e{e}')
            else:
                res.append(f'{result}({error})')
        if len(x) != 1:
            return res, e_list
        else:
            return res[0], e_list[0]#
            
        
# Erstellt Wertetabellen, die in LaTeX eingefügt werden können
def make_table(array,header ='',align = '', caption = None, latex=True, transpose = False, error_mode = 'plus-minus'):
    try:
        from texttable import Texttable
        from latextable import draw_latex
    except:
        print('error: für make_table müssen die Pakete texttable und latextable installiert werden')

    num = len(array)                        # Anzahl der Spalten

    try:
        length = np.shape(array[0])[1]                 # Anzahl der Reihen, falls erstes Element 2d ist
    except:
        length = len(array[0])                          # Anzahl der Reihen, falls erstes Element 1d ist
        
    if align == '':                                                     
        align = ['c'] * num
    if header == '':
        list = [0] * num
        for i in range (num):
            list[i] = str(i+1)
        header = list
    
    if len(align) != len(header) or len(header) != len(array):                                  # kontroliiert die Dimensionen der Listen
        print('error: align und header und array benötigen die selben Dimensionen')
        return
    

    k = np.zeros(num)
    #arg = [[0]*num, ['False']*num]
    for i,j in enumerate(array):             # gibt k = 2, wenn as Array 2-dim ist, k = 1 für 1-dim arrays
        try:
            k[i] = np.shape(j)[1]
            k[i] = 2
            
        except IndexError:
            k[i] = 1

    for i in range(num):
        if k[i] == 2:
            array[i][0], array[i][1] = error_round(array[i][0], array[i][1])
    

    table = Texttable()
    
    if transpose is True:
        
        table.set_cols_align(['c'] * (length+1))
        table.set_cols_dtype(['t'] * (length+1))
        for i in range(num):
            list = []
            list.append(header[i])
            for l in range(length):
                if k[i] == 1:
                    list.append(array[i][l])
                elif k[i] == 2:
                    list.append(f'${array[i][0][l]}\\pm {array[i][1][l]}  $')
            table.add_row(list)

    else:
        table.header(header)
        table.set_cols_align(align)
        table.set_cols_dtype(['t']*num)
        for i in range(length):
            list = [0]*num
            for l,m in enumerate(k):
                if m == 1:

                    list[l] = array[l][i]

                elif m == 2 and error_mode == 'plus-minus':

                    list[l] = '$' + array[l][0][i] + '\\pm ' + array[l][1][i] + '$'

                elif m == 2 and error_mode == 'parenthesis':
                    value = float(array[l][0][i])
                    error = array[l][1][i]
                    error = error.replace('.', '')

                    while error[0] == '0':
                        error = error[1:]
                    list[l] = f'${array[l][0][i]}({error})$'

                elif m == 2 and error_mode == 'scientific':

                    value = float(array[l][0][i])
                    error = float(array[l][1][i])
                    
                    res, e = error_round(value, error, error_mode='scientific')
                    
                    while 'e' in res:
                        res = res[:-1]
                    if e != 0:
                        list[l] = f'${res}\\times 10^\u007b{e}\u007d$'
                    else:
                        list[l] = f'${res}$'
                    
                
            table.add_row(list)
    if latex == True:
        if caption:
            text = draw_latex(table, caption = caption)
        else:
            text = draw_latex(table)
        if transpose == True:                                   # entfernt bei transponierter tabelle die erste Leere Zeile
            to_delete = '\n\t\t\t\\hline\n\t\t\t \\\\'
            text = text.replace(to_delete,'')

        with open('data.tex','a') as file:
            file.write(f'{text}\n')

    else:
        print(table.draw())

    return 

def write_csv(values, header='',name='data'):
    import csv 
    
    column = len(values)

    try:
        rows = np.shape(values)[1]
    except:
        rows = len(values)


    name = name + '.csv'

    with open(name,'w',newline='') as csvfile:

        writer = csv.writer(csvfile,delimiter=',')

        # Mache erste Zeile mit bezeichnungen
        if header =='':
            firstrow = np.asarray(range(column))+1
        else:
            firstrow = header
        writer.writerow(firstrow)

        for row in range(rows):
        
            list = [0]*column

            for col in range(column):
                list[col] = values[col][row]

            writer.writerow(list)

    
    print(f'Datei {name} wurde gespeichert')

# passe die Nachkommastellen in einem array an
def round_align(list):
    n = 0    # die Anzahl der Arrays
    num = 0  # Anzahl der Elemnte pro Array
    try:
        num = np.shape(list)[1]
        n = np.shape(list)[0]
    except:
        n = 1
        num = np.shape(list)[0]
        list = [list]
        
    list_sci = [0]*n
    for i in range(n):
        dummy = [0]*num
        last = 100                  # Anzahl der wenigsten nachkommastellen im Array
        for j in range(num):
            dummy[j] = np.format_float_positional(list[i][j])          
            this = dummy[j]
            k = len(this) 
            decimals = 0                                   

            while this[k-1] != '.':
                decimals += 1
                k -= 1

            if last > decimals:
                last = decimals
        numformat = '{:.'+str(last)+'f}'

        for j in range(num):
            dummy[j] = numformat.format(list[i][j])
        list_sci[i] = dummy
        
    if n == 1:
        return list_sci[0]
    else:
        return list_sci
        

# erstellt nötige Dateien, um Plots und Tabellen in latex einfügen zu können
def create_tex():
    with open('standard_pakete.sty','w') as file:
        text1 = '\\RequirePackage[utf8]{inputenc}\n\\RequirePackage{amsmath}\n\\RequirePackage{amssymb}\n\\RequirePackage[ngerman]{babel}'
        text2 = '\n\\RequirePackage[T1]{fontenc}\n\\RequirePackage{newtxtext,newtxmath,siunitx}'
        text3 = '\n\\sisetup{locale = DE,sticky-per,\nrange-phrase = -,range-units= single}\n\\RequirePackage{mathtools,graphicx}\n\\usepackage[margin=.5cm]{geometry}'
        file.write(text1+text2+text3)

    with open('data.tex','w') as file:
        file.write('')

    with open('main.tex','w') as main:
        text1 = '\\documentclass[ngerman]{scrartcl}\n\\usepackage{standard_pakete}\n\n\\title{Titel}\n\\author{author}\n'
        text2 = '\\begin{document}\n\n\\include{data.tex}\n\n\\end{document}'
        main.write(text1 + text2)

    
def display_value(name, value, value_err, unit, display_style = 'plus-minus'):

    if all([isinstance(i, (float, int)) for i in [value, value_err]]):
        x, y = error_round(value, value_err)
        result = None

        if display_style == 'plus-minus':
            result = f'({x} +- {y})'
        elif display_style == 'parenthesis':
            result = error_round(value, value_err, 'parenthesis')

        try:
            percentage = round(float(y)/float(x)*1e2,2)
            print(f'{name}: {result} {unit} {percentage}% Fehler')
        except ZeroDivisionError:
            print(f'{name}: {result} {unit}')
    else:
        print('display_value: value und value_err müssen floats oder ints sein, keine Arrays')