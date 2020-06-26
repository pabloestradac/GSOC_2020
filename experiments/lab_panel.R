setwd("~/OneDrive - ufmg.br/Academico/GeoDaCenter/soci40217")

install.packages(c("data.table","splm"))
library(splm)
library(data.table)

db <- st_read('NAT.shp')
st_crs(db) <- "+proj=onglat +datum=WGS84"
st_crs(db)
plot(st_geometry(db))
summary(db)

queen1 <- poly2nb(db)
summary(queen1)
W <- nb2listw(queen1)
summary(W)

db_reg <- melt(setDT(db), id="FIPSNO", 
               measure=patterns("^HR", "^RD", "^PS", "^UE"),
               value.name = c("HR", "RD", "PS", "UE"), variable.name="YEAR")
summary(db_reg)

#1st test: H0: lambda=0 (no spatial correlation) and sigma_mu2 = 0 (no regional random effect)
bsktest(HR ~ RD + PS + UE, db_reg, listw=W, test="LMH")

#2nd test: H0: sigma_mu2 = 0 (no regional random effect), assuming that lambda=0
bsktest(HR ~ RD + PS + UE, db_reg, listw=W, test="LM1")

#3rd test: H0: lambda=0 (no spatial correlation), assuming that sigma_mu2 = 0 (no regional random effect)
bsktest(HR ~ RD + PS + UE, db_reg, listw=W, test="LM2")

#4th test: H0: sigma_mu2 = 0 (no regional random effect), assuming that |lambda|>=0
bsktest(HR ~ RD + PS + UE, db_reg, listw=W, test="CLMmu")

#5th test: H0: lambda=0 (no spatial correlation), assuming that sigma_mu2 >=0
bsktest(HR ~ RD + PS + UE, db_reg, listw=W, test="CLMlambda")

#Spatial Hausman test
sphtest(HR ~ RD + PS + UE, db_reg, listw=W, spatial.model = "lag", method = "GM")

fixed_lag <- spgm(HR ~ RD + PS + UE, db_reg, index=c('FIPSNO','YEAR'),
                  listw = W, model = "within",
                  lag=TRUE,spatial.error = FALSE)
summary(fixed_lag)


fixed_lag = spml(HR ~ RD + PS + UE, data=db_reg,index=c('FIPSNO','YEAR'), listw=W, model="within",
                spatial.error="none", lag=TRUE)
summary(fixed_lag)

eff = effects(fixed_lag)
#eff$SETable[1:10,]
eff

#Pooled
pooled_lag = spml(HR ~ RD + PS + UE, data=db_reg,index=c('FIPSNO','YEAR'), listw=W, model="pooling",
                  spatial.error="none", lag=TRUE)
summary(pooled_lag)

#Fixed Error

fixed_erro <- spgm(HR ~ RD + PS + UE, data=db_reg,index=c('FIPSNO','YEAR'), listw=W, model="within")
summary(fixed_erro)


fixed_erro <- spml(HR ~ RD + PS + UE, data=db_reg,index=c('FIPSNO','YEAR'), listw=W, model="within")
summary(fixed_erro)


#Random
rand_erro_kkp = spgm(HR ~ RD + PS + UE, data=db_reg,index=c('FIPSNO','YEAR'), 
                      moments="weights", listw=W, model="random",spatial.error=TRUE)
summary(rand_erro_kkp)
rand_erro_kkp[["rho"]]

rand_lag = spml(HR ~ RD + PS + UE, data=db_reg,index=c('FIPSNO','YEAR'), listw=W, model="random",
                 spatial.error="none", lag=TRUE)
summary(rand_lag)

rand_erro = spml(HR ~ RD + PS + UE, data=db_reg,index=c('FIPSNO','YEAR'), listw=W, model="random")
summary(rand_erro)

#Save data for use in GSpace
write.csv(db_reg,"NAT_pooled.csv")

