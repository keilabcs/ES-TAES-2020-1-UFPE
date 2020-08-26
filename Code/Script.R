#Carregar os pacotes que serão usados

library(dplyr)                                  
library(rstatix)                                
library(readxl)

#Read Data
Survey<- read_excel("~/ES-TAES-2020-1/Base/new_results2.xlsx")  # Carregamento do Arquivo xlsx
glimpse(Survey)                                                 # Visualização de um resumo dos dados
head(Survey)

# Realização do teste de Mann-Whitney
wilcox.test(build ~ candidate, data = Survey)
wilcox.test(mismanaging ~ candidate, data = Survey)
wilcox.test(rework ~ candidate, data = Survey)