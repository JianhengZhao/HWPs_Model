##########################################################
# Construction carbon module.                            #
# Xinyuan Wei                                            #
# 2021/12/11                                             #
##########################################################
import scipy.integrate as integrate
import math

#%%
##########################################################
# Construction carbon module.                            #
##########################################################

def Construction_C (ty,con_C,dp1,dp2,dp3):

    # ty:      total years
    # co_C:    annual construction carbon
    # dp1:     consctruction disposal rate parameter 1
    # dp2:     consctruction disposal rate parameter 2
    # dp3:     consctruction disposal rate parameter 3
    
    co_yrA=[] # Current year, the accumulated construction carbon.
    co_yrD=[] # Annual construction carbon disposed.

    # Construction disposal rate.
    def co_dr(yr):
        part1=dp1/math.sqrt(2*math.pi)
        part2=math.exp((-dp2*math.pow((yr-dp3),2))/dp3)
        return(part1*part2) 
    
    # Accumulated construction carbon.
    for i in range (ty): 
        # Current year, the accumulated construction carbon.
        acc_A=0
            
        if i<=dp3:
            for j in range (i+1):
                temp_A=0
                yr_C=con_C.at[j]
                lfr=integrate.quad(co_dr,0,i+1-j)[0]
                temp_A=temp_A+yr_C*(1-lfr)
                acc_A=acc_A+temp_A
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=con_C.at[int(i-dp3+j)]
               lfr=integrate.quad(co_dr,0,dp3-j)[0]
               temp_A=temp_A+yr_C*(1-lfr)
               acc_A=acc_A+temp_A      
        
        co_yrA.append(acc_A)       
    
    # Construction carbon disposed.
    for i in range (ty):
        acc_D=0
    
        if i<=dp3:
            for j in range (i+1):
                temp_D=0
                yr_C=con_C.at[j]
                dfr=co_dr(i-j+1)
                temp_D=yr_C*dfr
                acc_D=acc_D+temp_D
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=con_C.at[int(i-dp3+j)]
               dfr=co_dr(dp3-j+1)
               temp_D=yr_C*dfr
               acc_D=acc_D+temp_D
   
        co_yrD.append(acc_D)

    # Return:
    # accumulated construction carbon
    # disposed construction carbon
    
    return(co_yrA,co_yrD)