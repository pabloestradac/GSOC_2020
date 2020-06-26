# install.packages(c("data.table", "splm"), dependencies = TRUE)
library(splm)
library(data.table)

setwd("C:\\Users\\pablo\\OneDrive - Escuela Superior Politécnica del Litoral\\2 MECE\\Others\\GSoC\\GSOC2020\\scripts\\natregimes")
db <- st_read('natregimes.shp')
queen1 <- poly2nb(db)
W <- nb2listw(queen1)

db_reg <- melt(setDT(db), id="FIPSNO", 
               measure=patterns("^HR", "^RD", "^PS", "^UE"),
               value.name = c("HR", "RD", "PS", "UE"), variable.name="YEAR")

fixed_lag = spml(HR ~ RD + PS, data=db_reg,index=c('FIPSNO','YEAR'), 
                 listw=W, model="within", spatial.error="none", lag=TRUE)

summary(fixed_lag)