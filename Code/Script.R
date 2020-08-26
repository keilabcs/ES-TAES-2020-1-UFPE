#Carregar os pacotes que serão usados

library(dplyr)                                  
library(rstatix)                                
library(readxl)

#Read Data
Survey<- read_excel("~/ES-TAES-2020-1/Base/rank.xlsx")  # Carregamento do Arquivo xlsx
glimpse(Survey)                                         # Visualização de um resumo dos dados
head(Survey)

#Filtrando por categoria
Build1 <- Survey %>%
  select(waste, rank, candidate) %>%
  filter(waste %in% c('build', 'mismanaging'))
head(Build1)

Build2 <- Survey %>%
  select(waste, rank, candidate) %>%
  filter(waste %in% c('build', 'rework'))

Build3 <- Survey %>%
  select(waste, rank, candidate) %>%
  filter(waste %in% c('build', 'unnecessarily'))


# Realização do teste de Mann-Whitney
wilcox.test(rank ~ waste, data = Build1)
wilcox.test(rank ~ waste, data = Build2)
wilcox.test(rank ~ waste, data = Build3)

#Análise descritiva dos dados
dados %>% group_by(rank) %>% 
  get_summary_stats(rank, rank, rank, type = "median_iqr")

# Visualização da distribuição
par(mfrow=c(1,2))
hist(rank[Build1$waste == "build"],
     ylab="Frequência", xlab="Rank", main="Grupo Build")
hist(rank[Build1$waste == "mismanaging"],
     ylab="Frequência", xlab="Rank", main="Grupo Mismanaging")
