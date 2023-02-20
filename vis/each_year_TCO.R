library(ggplot2)
#install.packages("tidyr")
library(tidyr)
#install.packages("plyr")
library(plyr)
library(dplyr)
#install.packages("tidyverse")
library(readr)
library(tidyverse)
#library(sensemakr)
#install.packages("devtools")
library(devtools)

#install.packages("devtools")
folder <- c("/cloud/project")
data <- read_csv("CombinedCost11Sept.csv")
data$Type <- factor(data$Type, 
                    levels=c("InfrasUpgrade", "OPEX", "BadLoans"),
                    labels=c("CAPEX", "OPEX", "Debt Payment"),
)
data$Scenario <- factor(data$Scenario, 
                        levels=c("Solo", "Passive", "Active", "NHN5G"),
                        labels=c("(a) Baseline (No Sharing)", 
                                 "(b) Passive Infrastructure Sharing", 
                                 "(c) Active Infrastructure Sharing", 
                                 "(d) 5G Neutral Host Network")
)
glimpse(data)
data$Year <- factor(data$Year, 
                    levels=c(2023,2024,2025,2026,2027,2028,2029,2030,2031,2032),
                    labels=c(2023,2024,2025,2026,2027,2028,2029,2030,2031,2032)
)
glimpse(data)
totals <- data %>%
  group_by(Year, Scenario) %>%
  summarize(total = round(
    sum(Cost)/1e6,2)
  )

fig = ggplot(data, aes(Year, Cost/1e6, fill = Type)) +
  geom_col() + 
  #scale_fill_viridis_d() +
  geom_text(
    aes(label = round(after_stat(y),2), group = Year), 
    stat = 'summary', fun = sum, vjust = -1, size=2.5) + 
  labs(
    # title = "Add title...", subtitle="Add subtitle",
    x = "Year", y = "Cost (US$ Millions)") +
  scale_y_continuous(expand = c(0, 0), limits=c(0,0.225)) +
  scale_fill_manual(
    values=c('#E69F00',"#56B4E9",'#E66101'))+
  guides(fill=guide_legend(title="Cost type")) +
  #theme(legend.position="bottom") +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=.5)) +
  theme(text=element_text(family="Times",size=12)) +
  facet_wrap(~Scenario,  ncol = 2) +theme(text=element_text(size=12))
fig
#create folder
dir.create(file.path(folder, 'figures'), showWarnings = FALSE) #creates a folder called figures if it doesn't already exist
path = file.path(folder, 'figures', 'decile_panel_TCO.png') #set the path to export the image to
png(path, units="in", width=8, height=5, res=300) #set up the .tiff in terms of width/height and resolution
print(fig) #print the figigure to the .tiff
dev.off() #end the operation
