import os
base_directory = 'C:\\Users\\GaboM'
uni_directory = 'C:\\Meine Dateien\\Uni'

def create_directory(end_directory, latex_directory, delete = False):
  
    os.chdir(end_directory)
    print(os.getcwd())

    # Erstellt hauptverzeichnis
    try:
        os.mkdir(latex_directory)
    except FileExistsError:
        if delete == False:
            print('Verzeichnis existiert bereits')
        else:
            try:
                os.rmdir(latex_directory)
                os.mkdir(latex_directory)
            except OSError:
                print('Verzechnis ist nicht leer')

    # Erstellt Unterverzeichnisse
    os.chdir(latex_directory)
    os.mkdir('figs')
    os.mkdir('unterdateien')

    # Erstellt main.tex und restliche dateien
    maintext = "\documentclass[ngerman]{scrreprt}\n\\usepackage{standard_pakete}\n%\\usepackage{math_commands}"\
    '\n%\\usepackage{physics_commands}\n\n\\title{title}\n\\author{author}\n\\date{\\today}\n\n\\begin{document}\n\n\\maketitle\n\n\\end{document}'

    with open('main.tex','w') as file:
        file.write(maintext)

    standard_pakete = '\\RequirePackage[utf8]{inputenc}\n\\RequirePackage{amsmath, amssymb}\n\\RequirePackage{lastpage}\n\\RequirePackage[ngerman]{babel}'\
        '\n\\RequirePackage[T1]{fontenc}\n\\RequirePackage[autostyle=true]{csquotes}\n\\RequirePackage{newtxtext, fancyvrb, xcolor,newtxtmath}'\
        '\n\\RequirePackage{siunitx}\n\\sisetup{locale = DE,sticky-per,\nrange-phrase = -,range-units= single}\n\\RequirePackage{booktabs, wrapfig}'\
        '\n\\RequirePackage{mathtools}\n%\\RequirePackage{tikz, tcolorbox} \n\\RequirePackage{graphicx, subfig}\n\\graphicspath{\n{figs/}\n}'\
        '\n%\RequirePackage{url}\n\\RequirePackage[pdfborder={0 0 0}]{hyperref}\n\\hypersetup{\n    pdfauthor = Gabriel Remiszewski,'\
        '\n    pdftitle = title\n    colorlinks = true,\n    linkcolor = blue,\n    urlcolor = blue,\n    citecolor = black\n}'\
        '\n\\RequirePackage[all]{hypcap}\n%\\RequirePackage[backend=biber,style=alphabetic]{biblatex}\n%\\addbibresource{bibtest.bib}  '\
        '\n%\\RequirePackage{fancyhdr}\n%\\RequirePackage[acronym,nomain]{glossaries}\n%\\RequirePackage[nomain, acronym]{glossaries-extra}'\
        '\n%\\setabbreviationstyle[acronym]{long-short}\n%\\glsdisablehyper\n%\\newacronym{rel}{RT}{Relativitätstheorie}\n%\\makeglossaries'\
        '\n\n\\KOMAoptions{parskip = half} \n\\KOMAoptions{listof=totoc}\n\\tcbset{colback=white!7!white,colframe=red!65!black,sharp corners} '
    with open('standard_pakete.sty','w') as file:
        file.write(standard_pakete)

    math_commands = '\\newcommand{\\im}[0]{\\ensuremath{\\mathrm{i}}}\n\\newcommand{\\e}[0]{\\ensuremath{\\mathrm{e}}}'
    with open('math_commands.sty', 'w') as file:
        file.write(math_commands)

    physics_commands = '%-----------Das Paket siunitx wird benötigt---------------------\n'\
        '\\newcommand{\\daylength}[3]{\\qty{#1}{\\hour}  \\qty{#2}{\\min}  \\qty{#3}{\\second}} % tageslänge in Stunden,Minuten,Sekunden\n\n'\
        '%-----------Konstanten---------------------------------------------\n'\
        '\\newcommand{\\h}[0]{\\ensuremath{\\mathrm{h}}}\n\\newcommand{\\lspeed}[0]{\\ensuremath{\\mathrm{c}}}\n'\
        '%------SI-Unit---------------------\n'\
        '\\DeclareSIPower\\quartic\\tothefourth{4}\n\\DeclareSIPower\\cubic\\tothethird{3}\n\\DeclareSIPower\\six\\tothesixth{6}\n'\
        '\\DeclareSIUnit\\radiant{\\text{rad}}\n\\DeclareSIUnit\\parsec{{pc}}\n\\DeclareSIUnit\\pc{{pc}}\n'\
        '\\DeclareSIUnit\\steradiant{{sr}}\n\\DeclareSIUnit\\au{{AU}}\n\\DeclareSIUnit\\arcmin{{\'}}\n\\DeclareSIUnit\\arcsec{{\'\'}}\n'\
        '\\DeclareSIUnit\\jansky{{Jy}}'

    with open('physics_commands.sty', 'w') as file:
        file.write(physics_commands)
