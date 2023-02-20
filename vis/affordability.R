library(readr)
library(dplyr)
library(ggplot2)
library(grid)

folder <- dirname(rstudioapi::getSourceEditorContext()$path)
folder <- c("/cloud/project")

data <-  read_csv("Dataset_affordability.csv")

data$Type <- factor(data$Type, 
                         levels=c("Solo", "Passive", "Active", "NHN"),
                         labels=c("(a) Baseline (No Sharing)", 
                                  "(b) Passive Infrastructure Sharing", 
                                  "(c) Active Infrastructure Sharing", 
                                  "(d) 5G Neutral Host Network")
)

glimpse(data)


fig = ggplot(data, aes(x=Subscribers, y=ARPU, group=Type, color=Type)) + 
  geom_point() +
  geom_line()+
  scale_linetype_manual(
    values=c("dashed","longdash", "dotted", "solid", "dotted"))+
  scale_color_manual(name = "Infrastructure Sharing Strategy",
    values=c('#E69F00',"#56B4E9",'#E66101', '#999999'))+
  scale_size_manual(values=c(.75,.9,1,.9)) +
  labs(
    x = "Number of Subscribers at Year 0", y = "ARPU $ (USD)") +
  scale_y_continuous(expand = c(0, 0), limits = c(0,60))  + 
  scale_x_continuous(limits = c(0, 10000))+
  theme(axis.text.x = element_text(angle = 0, vjust = 0.5, hjust=.5)) +
  theme(text=element_text(family="Times",size=12)) +
  #theme(legend.position="bottom") +
  guides(linetype = guide_legend(reverse = FALSE), 
         color = guide_legend(reverse = FALSE), 
         size = guide_legend(reverse = FALSE)) 


dir.create(file.path(folder, 'figures'), showWarnings = FALSE) 
path = file.path(folder, 'figures', 'affordarpu.png') 
png(path, units="in", width=8, height=5, res=300) 
print(fig) 
dev.off()
