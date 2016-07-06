from django.shortcuts import render

# Create your views here.

from markupApp.models import TextIn
from markupApp.forms import TextInForm
import os
# making a change to a file
# write the latex file header
header= '''
\\documentclass{report}
\usepackage{geometry}
\usepackage[dvipsnames]{xcolor}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{float}
\usepackage{amsmath}
\usepackage{subcaption}
\usepackage{caption}
\usepackage{mathtools}
\usepackage{listings}

\graphicspath{ {images/}}
\hypersetup{
colorlinks=true,
linktoc=all,
linkcolor=blue!60,
}
\\geometry{legalpaper, portrait, margin=0.5in}
\\lstdefinestyle{custom}{
  basicstyle=\\small\\ttfamily,
  columns=flexible,
  breaklines=true,
  frame=single,
  language=Python ,
  keepspaces=true,
  backgroundcolor=\\color{gray!20},
  keywordstyle=\\bfseries\\color{purple!70!black},
  identifierstyle=\color{black},
  stringstyle=\color{orange},
  commentstyle=\\color{green!40!black}
}

\\lstset{style=custom}

\\title{Default Title}
\\author{Matt McNichols}
\\date{\\today}

\\DeclarePairedDelimiter\\floor{\\lfloor}{\\rfloor}



\\begin{document}
\\maketitle
\\tableofcontents
\\listoffigures
'''
str_rep = '''
\\b{ --> \\begin{
\\e{ --> \\end{
\\s{ --> \\section{
i_z --> itemize
d_n --> description
|{ --> \\item{
'''

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.
def index(request):
 # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    TextBlocks = TextIn.objects.order_by('-id').reverse()
    block_dict = {'blocks': TextBlocks}

    # put blocks together into a file
    fTexName = os.path.join(BASE_DIR,'static/markupApp/fOut.tex')
    print 'tex file location: ',fTexName
    fTex = open(fTexName,'w')
    # loop through text blocks
    for block in TextBlocks:
        if block.slugId != 'str-repl':
            print 'block: ',block, 'lang: ',block.is_lang();
            fTex.write(block.data)
    # file has now been writen
    fTex.close();

    # now compile tex file into pdf
    os.chdir('static/markupApp/');
    os.system('pdflatex fOut.tex')
    os.chdir('../../');
    os.system('pwd')

    # Render the response and send it back!
    return render(request, 'markupApp/index.html', block_dict)

def add_block(request):
    # still display the other blocks
    TextBlocks = TextIn.objects.order_by('-id').reverse()
    block_dict = {'blocks': TextBlocks}
    # A HTTP POST?
    if request.method == 'POST':
        print 'method was a post'
        form = TextInForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print 'the form was not valid'
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = TextInForm()
    # pass the block info and the form
    block_dict['form'] = form
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'markupApp/add_block.html', block_dict)
