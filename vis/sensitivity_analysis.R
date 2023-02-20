library(ggplot2)
#install.packages("tidyr")
library(tidyr)
#install.packages("plyr")
library(plyr)
library(dplyr)
#install.packages("tidyverse")
library(readr)
library(tidyverse)
library(sensemakr)
#install.packages("devtools")
library(devtools)
folder <- dirname(rstudioapi::getSourceEditorContext()$path)
data <- read_csv("Dataset_sensitivityanalysis.csv")
data$Type <- factor(data$Type, 
                    levels=c("Solo", "Passive", "Active", "NHN5G"),
                    labels=c("(a) Baseline (No Sharing)", 
                             "(b) Passive Infrastructure Sharing", 
                             "(c) Active Infrastructure Sharing", 
                             "(d) 5G Neutral Host Network")
)
glimpse(data)

data$Scenario <- factor(data$Scenario,
                        levels = c("4Minus60", "3Minus40", "2Minus20", "1Minus10", "zero", "1Plus10", "2Plus20", "3Plus40", "6Plus60" ),
                        labels = c("Change -60%", "Change -40%", "Change -20%", "Change -10%", "Baseline", "Change +10%","Change +20%","Change +40%", "Change +60%"))
data$category <- factor(data$category,
                    levels = c("5Population", "6ARPU", "7Existing towers", "2OPEX",
                                "3InfraUpgrade","9Spectrum","1Backhaul", "8DemandGrowth",
                               "4Badloans"),
                    labels = c("Population", "ARPU", "Existing Towers", "OPEX",
                               "Infra Upgrade", "Spectrum","Backhaul", "Demand Growth", 
                               "Debt Repayment"))
glimpse(data)

fig = ggplot(data, aes(x = category, y = ChangeNPV/1e6)) + 
    geom_line( color="grey") +
  geom_point(aes(color = Scenario, shape = Scenario)) + 
  geom_vline(xintercept = 0) + 
  scale_color_manual(
    values=c('#E69F00',"#56B4E9",'#E66101', '#998999', "#000000","#B2B200", '#0571B0', "#E69F00", "#C7B4E9", "#009E73",'#5E3C99'))+
  scale_shape_manual(values=c(3, 16, 17, 1, 23, 4, 10, 6, 7, 20))+ 
  labs(
    x = "Input parameter", y = "Change in NPV in million $") +
  scale_y_continuous(expand = c(0, 0)) + 
  #theme(legend.position="bottom") +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=.5)) +
  facet_wrap(~Type,  ncol = 2) + coord_flip() +
  theme(text=element_text(family="Times",size=12)) 
  
fig
#create folder
dir.create(file.path(folder, 'figures'), showWarnings = FALSE) #creates a folder called figures if it doesn't already exist
path = file.path(folder, 'figures', 'decile_panel_sensitivity.png') #set the path to export the image to
png(path, units="in", width=8, height=7, res=300) #set up the .tiff in terms of width/height and resolution
print(fig) #print the figigure to the .tiff
dev.off() #end the operation
