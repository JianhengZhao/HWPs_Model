##########################################################
# Home application carbon module.                        #
# Xinyuan Wei                                            #
# 2021/05/11                                             #
##########################################################
import scipy.integrate as integrate
import math

#%%
##########################################################
# Home application carbon module.                        #
##########################################################

def HomeA_C (ty,hma_C,dp1,dp2,dp3):
    
    # ty:      total years
    # hma_C:   annual home application carbon
    # dp1:     home application disposal rate parameter 1 
    # dp2:     home application disposal rate parameter 2 
    # dp3:     home application disposal rate parameter 3 (service life)

    hma_yrA=[] # Current year, the accumulated home application carbon.
    hma_yrD=[] # Annual home application carbon disposed.
    
    # Home application disposal rate.
    # TSD: time since production
    def hma_dr(TSP):
        part1=dp1/math.sqrt(2*math.pi)
        part2=math.exp((-dp2*math.pow((TSP-dp3),2))/dp3)
        return(part1*part2)
             
    # Accumulated home application carbon.
    for i in range (ty): 
        # Current year, the accumulated home application carbon (Carbon Pool).
        acc_A=0
            
        if i<=dp3:
            for j in range (i+1):
                temp_A=0
                yr_C=hma_C.at[j]
                lfr=integrate.quad(hma_dr,0,i+1-j)[0]
                temp_A=temp_A+yr_C*(1-lfr)
                acc_A=acc_A+temp_A
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=hma_C.at[int(i-dp3+j)]
               lfr=integrate.quad(hma_dr,0,dp3-j)[0]
               temp_A=temp_A+yr_C*(1-lfr)
               acc_A=acc_A+temp_A      
        
        hma_yrA.append(acc_A)       
    
    # Home application carbon disposed.
    for i in range (ty):
        acc_D=0
    
        if i<=dp3:
            for j in range (i+1):
                temp_D=0
                yr_C=hma_C.at[j]
                dfr=hma_dr(i-j+1)
                temp_D=yr_C*dfr
                acc_D=acc_D+temp_D

        if i>dp3:
           for j in range (int(dp3)):
               temp_D=0
               yr_C=hma_C.at[int(i-dp3+j)]
               dfr=hma_dr(dp3-j+1)
               temp_D=yr_C*dfr
               acc_D=acc_D+temp_D

        hma_yrD.append(acc_D)
             
    # Return:
    # accumulated home application carbon
    # disposed home application carbon
    return(hma_yrA,hma_yrD)