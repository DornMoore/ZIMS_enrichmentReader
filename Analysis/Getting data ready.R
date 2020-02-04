library(readxl)
library(ggplot2)
library(dplyr)
library(scales)

# Import our dataset
output <- read_excel("C:/Code/ZIMS_enrichmentReader/output.xlsx", col_types = c("numeric", "text", "text", "text", "text", "text", "text", "text","text", "text", "text", "text", "text", "text", "date", "text", "text", "text", "text", "text"))

# Set up some values as factors
output$individual<-factor(output$individual)
output$preferredID<-factor(output$preferredID)
output$species<-factor(output$species)
output$birth_type<-factor(output$birth_type)
output$localId<-factor(output$localId)
output$enrichmentType<-factor(output$enrichmentType)
output$reaction<-factor(output$reaction)

#rating is special becasue the factor is ranked - set up the ranking
output$rating <- factor(output$rating, levels=c("Highly Unsuccessful", "Moderately Unsuccessful", "No Reaction", "Moderately Successful", "Highly Successful"))


# Create a subset to plot out rating by bird
plot_data <- output %>% filter(!is.na(rating)) %>%
  count(preferredID, rating) %>% 
  group_by(preferredID) %>% 
  mutate(percent = n/sum(n))

# plott rating by bird
ggplot(plot_data, aes(x=preferredID, y = percent, fill = rating)) + 
  geom_col(position = "fill") + 
  coord_flip()
