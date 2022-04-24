library(dplyr)
library(BSDA)


# import the trip data 
tripdata =  read.csv("C:/Users/HP/Desktop/Projects/Trip purpose/Travel Pattern Identification/distanced_trip_data.csv")


# standardize the trip length distribution 
tripdata['standard_distance'] =  NA
tripdata$standard_distance = (tripdata$trip_distance - mean(tripdata$trip_distance)) / sd(tripdata$trip_distance)

# sample and population distribution comparison (one sample test )
z_value_vector = c()
p_value_vector = c()

trip_purposes = c('education','work','residential', 'personal','transit', 'medical', 'shopping','recreational','dining')
 
z.test(x=tripdata$standard_distance, sigma.x=1, conf.level=.95)

for(purpose in trip_purposes){
  
  # select the dataframe for purpose 
  dataframe = tripdata %>% filter(Trip.purpose == purpose)
  
  #perform one sample z-test and take the z value and p value 
  z_value = z.test(x=dataframe$standard_distance, sigma.x=1, conf.level=.95)[['statistic']][['z']]
  p_value = z.test(x=dataframe$standard_distance, sigma.x=1, conf.level=.95)['p.value']
  
  
  # append the value to the vector 
  z_value_vector = append(p_value_vector,z_value)
  p_value_vector = append(z_value_vector,p_value)

}

names(z_value_vector) = trip_purposes

# sample wise distribution comparision (two sample test)
z_value_matrix = matrix(, nrow = 9, ncol = 9, dimnames =  list(trip_purposes ,
                                                               trip_purposes ))

p_value_matrix = matrix(, nrow = 9, ncol = 9, dimnames =  list(trip_purposes ,
                                                               trip_purposes ))

for (purpose1 in trip_purposes){
  
  dataframe1 = tripdata %>% filter(Trip.purpose == purpose1)
  
  for (purpose2 in trip_purposes){
    
    dataframe2 = tripdata %>% filter(Trip.purpose == purpose2)
    
    p_value = z.test(x=dataframe1$standard_distance, y = dataframe2$standard_distance, sigma.x=1, sigma.y=1, conf.level=.95)['p.value']
    z_value = z.test(x=dataframe1$standard_distance, y = dataframe2$standard_distance, sigma.x=1, sigma.y=1, conf.level=.95)[['statistic']][['z']]
    
    
    p_value_matrix[purpose1,purpose2] = p_value[[1]]
    z_value_matrix[purpose1,purpose2] = z_value
    
  }
}

# determine the mean trip length for each activity 
mean_distance_vector = c()

for(purpose in trip_purposes){
  
  # select the dataframe for purpose 
  dataframe = tripdata %>% filter(Trip.purpose == purpose)
  
  #perform one sample z-test and take the z value and p value 
  mean_value = mean(dataframe$trip_distance)
    
  # append the value to the vector 
  mean_distance_vector  = append(mean_distance_vector,mean_value)

}

names(mean_distance_vector) = trip_purposes

# save the results as dataframes 
two_sample_df = data.frame(z_value_matrix)
two_sample_df_p = data.frame(p_value_matrix)
write.csv(two_sample_df,"C:/Users/HP/Desktop/Projects/Trip purpose/Travel Pattern Identification/two_sample_z_value.csv")
write.csv(two_sample_df_p,"C:/Users/HP/Desktop/Projects/Trip purpose/Travel Pattern Identification/two_sample_p_value.csv")

one_sample_df = data.frame(z_value_vector)
one_sample_df_p = data.frame(p_value_matrix)
write.csv(one_sample_df,"C:/Users/HP/Desktop/Projects/Trip purpose/Travel Pattern Identification/one_sample_z_value.csv")
write.csv(one_sample_df_p,"C:/Users/HP/Desktop/Projects/Trip purpose/Travel Pattern Identification/one_sample_p_value.csv")

