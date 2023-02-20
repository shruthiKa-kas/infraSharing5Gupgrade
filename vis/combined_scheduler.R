library(ggplot2)
library(grid)
library(ggpubr)
# # install.packages("devtools")

folder <- dirname(rstudioapi::getSourceEditorContext()$path)
folder <- c("/cloud/project")

data <-  read_csv("SchedulerResultsRefined.csv")
glimpse(data)
data$User_behavior <- factor(data$User_behavior, 
                    levels=c("short_user", "mid_user","long_user"),
                    labels=c('Short User (20 sec)', 'Mid User (60 sec)', 'Long User (300 sec)')
)
#data <- data %>% rename("User_behavior" = "User_behavior")
colnames(data)[2] <- "Behavior"
glimpse(data)

Datascheduler = ggplot(data, aes(x=Subscribers, y=DataScheduler, colour=factor(Behavior))) + 
  geom_line(aes(linetype=Behavior, color=Behavior)) + 
  theme(legend.position="bottom",legend.title=element_blank()) + guides(colour=guide_legend(ncol=3)) +
  labs(title = '(a) Data Scheduler', 
       x = 'Subscribers', y='Quantity of Data Scheduling\n Session Requests', colour='Behavior') +
  scale_fill_discrete(name=NULL)+
  theme(text=element_text(family="Times",size=12)) + scale_color_manual(values=c('#E69F00',"#56B4E9",'#E66101'))+
  theme(plot.title=element_text(family="Times", size=12))

#Datascheduler
Voicescheduler = ggplot(data, aes(x=Subscribers, y=VoiceScheduler, colour=factor(Behavior))) + 
  geom_line(aes(linetype=Behavior, color=Behavior)) + 
  theme(legend.position="bottom",legend.title=element_blank()) + guides(colour=guide_legend(ncol=3)) +
  labs(title = '(b) Voice Scheduler', 
       x = 'Subscribers', y='Quantity of Voice Scheduling\n Session Requests', colour='Behavior') +
  scale_fill_discrete(name=NULL)+
  theme(text=element_text(family="Times",size=12)) + scale_color_manual(values=c('#E69F00',"#56B4E9",'#E66101'))+
  theme(plot.title=element_text(family="Times", size=12))
#colnames(data)[2] <- "User behavior"


combined <- ggarrange(Datascheduler, Voicescheduler,
                      ncol = 2, nrow = 1,
                      common.legend = TRUE, 
                      legend='bottom' 
                      # heights=c(3.5, 5)
)
combined
dir.create(file.path(folder, 'figures'), showWarnings = FALSE) #creates a folder called figures if it doesn't already exist
path = file.path(folder, 'figures', 'SchedulerNew.png') #set the path to export the image to
png(path, units="in", width=6, height=3, res=300) #set up the .tiff in terms of width/height and resolution
print(combined) #print the figigure to the .tiff
dev.off() #end the operation
