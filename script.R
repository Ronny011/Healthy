# installation
install.packages('pacman')
# loading
# require(pacman)
# installing and loading required packages
pacman::p_load(pacman, dplyr, ggplot2, lubridate, ggthemes, 
                plotly, rio, stringr, tidyr, lme4, arm)
# base packages
library(datasets)
# clear console
cat('\014')
getwd()
data<-read.csv('Dataset.csv', stringsAsFactors = TRUE)
model.1 <- lmer(HR ~ ADS + Inc + TOD + Activity + Weight + Height + Age + (1|ID), data=data)
display(model.1)
summary(model.1)
