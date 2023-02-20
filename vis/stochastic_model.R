library(tidyverse)
library(plyr)
library(ggpubr)

folder <- dirname(rstudioapi::getSourceEditorContext()$path)
folder <- c("/cloud/project")

full_tables <- file.path(folder, 'data', 'stochastic')

#get a list of all files in the folder ending in .csv
myfiles = list.files(path=full_tables, pattern="*.csv", full.names=TRUE)
#glimpse(myfiles)
#import data for all files in file list
data = ldply(myfiles, read_csv)

#data = data[data$inter_cell_site_distance == 14000,]

data$environment = factor(data$environment, levels=c("rural"),
                          labels=c("Rural"))

data$generation = factor(data$generation, levels=c("5G"),
                         labels=c("5G (4x4 MIMO)"
                         ))

data$frequecy = factor(data$frequecy, 
                            levels=c(700,3800),
                            labels=c("700 MHZ","3800 MHZ"))

#data = data[complete.cases(data),]

#glimpse(data)
#subset the data for plotting
data = select(data, environment, generation, frequecy, sinr,capacity_Mbps,
              distance_m, spectral_efficiency)

test = data

test$distance_m <- 
  cut(test$distance_m, 
      breaks = c(0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000),
      labels = c("<1 km", "1-2 km", "2-3 km", "3-4 km", "4-5 km", "5-6 km", "6-7 km", "7-8 km", "8-9 km", "9-10 km", "10-11 km"),
      include.lowest = TRUE)

sinr_dB = ggplot(test, aes(x=distance_m, y=sinr, colour=factor(frequecy))) + 
  geom_boxplot() + 
  theme(legend.position="bottom") + guides(colour=guide_legend(ncol=5)) +
  labs(title = '(a) SINR vs User Distance From the Cell Site', 
       #subtitle = 'Results reported by settlement type and cellular generation (10 km ISD)',
       x = 'Distance (km)', y='SINR (dB)', colour='Frequency') +
  facet_grid(generation~environment) + theme(text=element_text(family="Times",size=12)) + scale_color_manual(values=c('#E69F00',"#56B4E9"))+
  theme(plot.title=element_text(family="Times",size=12))

capacity = ggplot(test, aes(x=distance_m, y=capacity_Mbps, colour=factor(frequecy))) + 
  geom_boxplot() + 
  theme(legend.position="bottom") + guides(colour=guide_legend(ncol=5)) +
  labs(title = '(c) Capacity (Mbps) vs User Distance From the Cell Site', 
       #subtitle = 'Results reported by settlement type and cellular generation (10 km ISD)',
       x = 'Distance (km)', y='Capacity (Mbps)', colour='Frequency') +
  facet_grid(generation~environment) + theme(text=element_text(family="Times",size=12)) + scale_color_manual(values=c('#E69F00',"#56B4E9"))+
  theme(plot.title=element_text(family="Times", size=12))

spectral_efficiency = ggplot(test, 
                             aes(x=distance_m, y=spectral_efficiency, colour=factor(frequecy))) + 
  geom_boxplot() + 
  # scale_x_continuous(expand = c(0, 0)) + scale_y_continuous(expand = c(0, 0)) +
  theme(legend.position="bottom") + guides(colour=guide_legend(ncol=7)) +
  labs(title = '(b) Spectral Efficiency vs User Distance From the Cell Site', 
       #subtitle = 'Results reported by settlement type and cellular generation (10 km ISD)',
       x = 'Distance (km)', y='Spectral Efficiency (Bps/Hz)', colour='Frequency') +
  facet_grid(generation~environment) + theme(text=element_text(family="Times",size=12)) + scale_color_manual(values=c('#E69F00',"#56B4E9")) +
  theme(plot.title=element_text(family="Times", size=12))
combined <- ggarrange(sinr_dB, spectral_efficiency,capacity,
                      ncol = 1, nrow = 3,
                      common.legend = TRUE, 
                      legend='bottom' 
                      # heights=c(3.5, 5)
)

path = file.path(folder, 'figures', 'tukey.png')
ggsave(path, units="in", width=8, height=10, dpi=300)
print(combined)
dev.off()