#! python3
# coding: latin-1

from bs4 import BeautifulSoup
import requests, re, os, time, ctypes
import pandas as pd
from datetime import date

# Date
today = date.today()
d1 = today.strftime("%d%m%Y")

# Get HTML from site
link = "https://www.pciconcursos.com.br/concursos/"
r  = requests.get(link)
data = r.text
soup = BeautifulSoup(data, "html.parser") # complete html source code

# ---------- CONCURSOS NACIONAIS --------------------------------
source_nacional=str(soup)
nacional=source_nacional[source_nacional.find('<h2>NACIONAL</h2>')+len('<h2>NACIONAL</h2>'):source_nacional.find('<h2>REGI�O SUDESTE</h2>')+len('<h2>REGI�O SUDESTE</h2>')]
extract_nacional=BeautifulSoup(nacional,"html.parser")

name=[]
vagas=[]
nivel=[]
salario=[]
inscricao=[]
combinacao_nacional=[]

for line in extract_nacional.findAll(class_='ca'):
    name.append(line.find('a').text.strip()) # get name of institution
    vagas.append(re.findall('(\d*) vaga', str(line.find(class_='cd')))[0]) # get number of available job's
    nivel.append('/'.join(re.findall('Superior|M�dio', str(line.find(class_='cd'))))) # level
    salario.append(''.join(re.findall('R\$ *\d*\.*\d*\,*\d*', str(line.find(class_='cd'))))) # salary
    inscricao.append(''.join(re.findall('\d+/\d+/\d+', str(line.find(class_='ce')))))
    
# ---------- CONCURSOS CEAR� --------------------------------
ceara=source_nacional[source_nacional.find('<div class="uf">CEAR�</div>')+len('<div class="uf">CEAR�</div>'):source_nacional.find('<div class="uf">MARANH�O</div>')+len('<div class="uf">MARANH�O</div>')]
extract_ceara=BeautifulSoup(ceara,"html.parser")

for line in extract_ceara.findAll(class_='ca'):
    name.append(line.find('a').text.strip()) # get name of institution
    vagas.append(''.join(re.findall('(\d*) vaga', str(line.find(class_='cd'))))) # get number of available job's
    nivel.append('/'.join(re.findall('Superior|M�dio', str(line.find(class_='cd'))))) # level
    salario.append(''.join(re.findall('R\$ *\d*\.*\d*\,*\d*', str(line.find(class_='cd'))))) # salary
    inscricao.append(''.join(re.findall('\d+/\d+/\d+', str(line.find(class_='ce')))))

for i in range(0,len(name)):
    combinacao_nacional=[name[i],vagas[i],nivel[i],salario[i],inscricao[i]]
    df=pd.DataFrame(combinacao_nacional)
    with open('ConcursosAtivos'+d1+'.csv', 'a', encoding='utf-16', newline='') as f:
        df.transpose().to_csv(f, encoding='iso-8859-1', header=False, sep = "\t")

# Conferindo se h� algum concurso novo        
try:
    tamanho_arquivo_original=os.path.getsize('ConcursosAtivos.csv')
    tamanho_arquivo_temp=os.path.getsize('ConcursosAtivos'+d1+'.csv') 
    if tamanho_arquivo_original!=tamanho_arquivo_temp:
        ctypes.windll.user32.MessageBoxW(0, "Novo concurso!", "Aviso", 1)
        os.remove('ConcursosAtivos.csv')
        os.rename('ConcursosAtivos'+d1+'.csv','ConcursosAtivos.csv')
    else:
        os.remove('ConcursosAtivos'+d1+'.csv')
except:
    os.rename('ConcursosAtivos'+d1+'.csv','ConcursosAtivos.csv')