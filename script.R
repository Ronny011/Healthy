# installation
install.packages('pacman')
# installing and loading required packages
pacman::p_load(pacman, dplyr, ggplot2, ggthemes, 
                plotly, rio, stringr, tidyr, lme4, arm, caret, MLmetrics, 
                  splitTools, ranger, Metrics, leaps, data.table, mltools)

# clear console
cat('\014')
getwd()
# loading data
data<-read.csv('C:/Users/sylum/PycharmProjects/Healthy/Dataset.csv', stringsAsFactors = TRUE)
data[,'ID'] <- as.factor(data[,'ID'])

#analysis - mean HR and variance of HR values
sqrt(var(data[,9]))
mean(data[,9])

# model 1 - trained with full data, no split. prediction made on the training data
model.1 <- lmer(HR ~ ADS + Inc + TOD + Activity + Weight + Height + Age + (1|ID), data=data)
display(model.1)
summary(model.1)
x.test.1 <- data[,1:8]
y.test.1 <- data[,9]
predictions.1<-predict(model.1, x.test.1)
MSE(predictions.1, y.test.1)


# splitting to train (70%) and test (30%) sets 
set.seed(123)
dt = sort(sample(nrow(data), nrow(data)*.7))
train <- data[dt,]
test <- data[-dt,]

# stratified splitting by 'ID' column
set.seed(123)
dts <- partition(data$ID, p = c(train.s = 0.7, test.s = 0.3))
train.s <- data[dts$train.s, ]
test.s <- data[dts$test.s, ]

# bar plots
barplot(table(train.s$ID), main="Stratified train data",
              xlab="User ID")
barplot(table(test.s$ID), main="Stratified test data",
        xlab="User ID")

# ratio
table(test.s$ID)/table(data$ID)

# model 2 with train / test split 
model.2 <- lmer(HR ~ ADS + Inc + TOD + Activity + Weight + Height + Age + (1|ID), data=train)
# make predictions - we exclude the dependent variable and save it
# for later comparison with our predictions
x.test.2 <- test[,1:8]
y.test.2 <- test[,9]
predictions.2 <- predict(model.2, x.test.2)
MSE(predictions.2, y.test.2)

# model 3 - same as model 2 but with stratification
model.3 <- lmer(HR ~ ADS + Inc + TOD + Activity + Weight + Height + Age + (1|ID), data=train.s)
x.test.3 <- test.s[,1:8]
y.test.3 <- test.s[,9]
predictions.3 <- predict(model.3, x.test.3)
MSE(predictions.3, y.test.3)

# k-fold cross validation
data$group <- sample(5, size = nrow(data), replace = TRUE)

mse.sum <- 0

for(i in 1:5) 
  {
    test.kf <- filter(data, group == i)
    model.kf <- lmer(HR ~ ADS + Inc + TOD + Activity + Weight + Height + Age + (1|ID), data = filter(data, group != i))
    x.kf <- test.kf[,1:8]
    y.kf <- test.kf[,9]
    predictions.kf <- predict(model.kf, x.kf)
    mse.sum <<- mse.sum + MSE(predictions.kf, y.kf)
}

mse.mean <- mse.sum/5
mse.mean

# feature selection
subset.models <- regsubsets(HR ~ ADS + Inc + TOD + Activity + Weight + Height + Age, data = data, nvmax = 26, method = "seqrep")
summary(subset.models)
summary(subset.models)$rsq
max(summary(subset.models)$rsq)
plot(subset.models)

# data conversion to one-hot encoding
data.onehot <- setDF(one_hot(as.data.table(data[,2:9])))
data.onehot$ID <- data[,'ID']
names(data.onehot)[names(data.onehot) == "Activity_m-light"] <- "Activity_m_light"
names(data.onehot)[names(data.onehot) == "Activity_m-medium"] <- "Activity_m_medium"
names(data.onehot)[names(data.onehot) == "Activity_su-small"] <- "Activity_su_small"
data.onehot <- data.onehot[c("ID", "Inc_nan", "Inc_Standing", "Activity_m_light", "Activity_m_medium", "Activity_sitting", "Activity_sleeping", "Activity_su_small", "Weight", "Age", "HR")]

#final model :)
model.final <- lmer(HR ~ Inc_nan + Inc_Standing + Activity_m_light + Activity_m_medium + Activity_sitting + Activity_sleeping + Activity_su_small + Weight + Age + (1|ID), data = data.onehot)

# k-fold cross validation - final model
data.onehot$group <- sample(5, size = nrow(data.onehot), replace = TRUE)

mse.sum.final <- 0

for(i in 1:5) 
{
  test.kf <- filter(data.onehot, group == i)
  model.kf <- lmer(HR ~ Inc_nan + Inc_Standing + Activity_m_light + Activity_m_medium + Activity_sitting + Activity_sleeping + Activity_su_small + Weight + Age + (1|ID), data = filter(data.onehot, group != i))
  x.kf <- test.kf[,1:10]
  y.kf <- test.kf[,11]
  predictions.kf <- predict(model.kf, x.kf)
  mse.sum.final <<- mse.sum.final + MSE(predictions.kf, y.kf)
}

mse.mean.final <- mse.sum.final/5
mse.mean.final
sqrt(mse.mean.final)

# k-fold cross validation - linear regression model
data.onehot$group <- sample(5, size = nrow(data.onehot), replace = TRUE)

mse.sum.final <- 0

for(i in 1:5) 
{
  test.kf <- filter(data.onehot, group == i)
  model.kf <- lm(HR ~ Inc_nan + Inc_Standing + Activity_m_light + Activity_m_medium + Activity_sitting + Activity_sleeping + Activity_su_small + Weight + Age, data = filter(data.onehot, group != i))
  x.kf <- test.kf[,1:10]
  y.kf <- test.kf[,11]
  predictions.kf <- predict(model.kf, x.kf)
  mse.sum.final <<- mse.sum.final + MSE(predictions.kf, y.kf)
}

mse.mean.final <- mse.sum.final/5
mse.mean.final
sqrt(mse.mean.final)

# SHT

# final model creation
set.seed(321)
dts.final <- partition(data.onehot$ID, p = c(train.f = 0.7, test.f = 0.3))
train.f <- data.onehot[dts.final$train.f, ]
test.f <- data.onehot[dts.final$test.f, ]

model.final <- lmer(HR ~ Inc_nan + Inc_Standing + Activity_m_light + Activity_m_medium + Activity_sitting + Activity_sleeping + Activity_su_small + Weight + Age + (1|ID), data = train.f)

x.test.f <- test.f[,1:10]
y.test.f <- test.f[,11]
predictions.f <- predict(model.final, x.test.f)
MSE(predictions.f, y.test.f)

# overfitted testing
predictions.of <- predict(model.final, train.f[,1:10])
MSE(predictions.of, train.f[,11])

# results
results <- cbind.data.frame(x.test.f$ID, y.test.f, predictions.f, predictions.of)
names(results)[names(results) == "x.test.f$ID"] <- "ID"
names(results)[names(results) == "y.test.f"] <- "actual.HR"
names(results)[names(results) == "predictions.f"] <- "predicted.HR.test"

results$delta <- abs(results$predicted.HR.test - results$actual.HR)
results$RMSE <- 0

for(i in 1:22) 
{
  train.temp <- filter(train.f, ID == i)
  predictions.temp <- predict(model.final, train.temp[,1:10])
  results[results$ID == i,]$RMSE <- RMSE(predictions.temp, train.temp[,11])
}

results$note <- ifelse(results$delta > 2 * results$RMSE, 'irregular HR', '')
results$predicted.HR.test <- round(results$predicted.HR.test, 2)
results$delta <- round(results$delta, 2)
results$RMSE <- round(results$RMSE, 2)

write.csv(results,'C:/Users/sylum/Desktop/results.csv', row.names = FALSE)
