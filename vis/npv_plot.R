library(readr)
# install.packages("dplyr")
library(dplyr)
# install.packages("ggplot2")
library(ggplot2)

# # install.packages("devtools")
folder <- dirname(rstudioapi::getSourceEditorContext()$path)

#data <-  read_csv("NPV_Upgrade_12Aug.csv")
data <-  read_csv("NPV_Upgrade_Dataset7Nov.csv")
data$Type <- factor(data$Type, 
                    levels=c("NPV2ARPU","NPV10ARPU", "NPV20ARPU", "NPV30ARPU", 
                             "NPV40ARPU", "NPV50ARPU", "NPV60ARPU"),
                    labels=c("-93% Revenue", "-66% Revenue", "-33% Revenue", "Baseline Revenue", 
                             "+33% Revenue", "+66% Revenue", "+100% Revenue"))

data$Scenario <- factor(data$Scenario, 
                        levels=c("Solo", "Passive", "Active", "NHN5G"),
                        labels=c("(a) Baseline (No Sharing)", 
                                 "(b) Passive Infrastructure Sharing", 
                                 "(c) Active Infrastructure Sharing", 
                                 "(d) 5G Neutral Host Network")
)

data$Year <- factor(data$Year, 
                    levels=c(2023,2024,2025,2026,2027,2028,2029,2030,2031,2032),
                    labels=c(2023,2024,2025,2026,2027,2028,2029,2030,2031,2032)
)
colnames(data)[3] <- "Strategy"
glimpse(data)
fig = ggplot(data, aes(x=Year, y=Cost/1e6, group=Strategy)) + 
  geom_line(aes(linetype=Strategy, color=Strategy, size=Strategy)) +
  scale_linetype_manual(
    values=c("dashed","longdash", "dotted", "solid", "dotted", "longdash", "dashed"))+
  scale_color_manual(
    values=c('#E69F00',"#56B4E9",'#E66101', '#999999','#92C5DE', '#0571B0','#5E3C99'))+
  scale_size_manual(values=c(.75,.75,.9,1,.9,.75,.75)) +
  labs(
    x = "Year", y = "NPV per Year (US$ Millions)") +
  scale_y_continuous(expand = c(0, 0), limits=c(-1.5,2)) +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=.5)) +
  #theme(legend.position="bottom") +
  guides(linetype = guide_legend(reverse = TRUE), 
         color = guide_legend(reverse = TRUE), 
         size = guide_legend(reverse = TRUE)) +
  facet_wrap(~Scenario,  ncol = 2)  +theme(text=element_text(family="Times",size=12))
fig
##create folder
#create folder
dir.create(file.path(folder, 'figures'), showWarnings = FALSE) #creates a folder called figures if it doesn't already exist
path = file.path(folder, 'figures', 'decile_panel_NPV.tiff') #set the path to export the image to
path = file.path(folder, 'figures', 'decile_panel_NPV.png') #set the path to export the image to
tiff(path, units="in", width=8, height=5, res=300) #set up the .tiff in terms of width/height and resolution
png(path, units="in", width=8, height=5, res=300)
print(fig) #print the figigure to the .tiff
dev.off() #end the operation


# 
#   install.packages('sensemakr')
#   library('sensemakr')
# 
#   data("darfur")
#   View(darfur)
#   # runs regression model
#   model <- lm(peacefactor ~ directlyharmed + age + farmer_dar + herder_dar +
#                 pastvoted + hhsize_darfur + female + village, data = darfur)
#   
#   # runs sensemakr for sensitivity analysis
#   sensitivity <- sensemakr(model, treatment = "directlyharmed",
#                            benchmark_covariates = "female",
#                            kd = 1:3)
#   # short description of results
#   sensitivity
#   
#   # long description of results
#   summary(sensitivity)
#   
#   # plot bias contour of point estimate
#   plot(sensitivity)
#   
#   # plot bias contour of t-value
#   plot(sensitivity, sensitivity.of = "t-value")
#   
#   
#   # plot extreme scenario
#   plot(sensitivity, type = "extreme")
#   
#   # latex code for sensitivity table
#   ovb_minimal_reporting(sensitivity)
#   
#   