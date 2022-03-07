##########################################################
# Paper carbon module                                    #
# Xinyuan Wei                                            #
# 2021/12/11                                             #
##########################################################
import scipy.integrate as integrate
import math

##########################################################
# Paper carbon module.                                   #
##########################################################

def Paper_C (ty,pap_C,dp1,dp2,dp3):
    
    # ty:      total years
    # pap_C:   annual paper production
    # dp1:     paper disposal rate parameter 1
    # dp2:     paper disposal rate parameter 2
    # dp3:     paper disposal rate parameter 3 (service life)
    
    paper_yrA=[]     # Current year, the accumulated paper carbon.
    paper_yrD=[]     # Annual paper carbon disposed.
    
    # Paper disposal rate.
    # TSD: time since production
    def pap_dr(TSP):
        part1=dp1/math.sqrt(2*math.pi)
        part2=math.exp(-dp2*math.pow((TSP-dp3),2)/dp3)
        return(part1*part2)
             
    # Accumulated paper carbon.
    for i in range (ty): 
        # Current year, the accumulated paper carbon (Carbon Pool).
        acc_A=0
            
        if i<=dp3:
            for j in range (i+1):
                temp_A=0
                yr_C=pap_C[j]
                lfr=integrate.quad(pap_dr,0,i+1-j)[0]
                temp_A=temp_A+yr_C*(1-lfr)
                acc_A=acc_A+temp_A
        
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=pap_C[int(i-dp3+j)]
               lfr=integrate.quad(pap_dr,0,dp3-j)[0]
               temp_A=temp_A+yr_C*(1-lfr)
               acc_A=acc_A+temp_A
 
        paper_yrA.append(acc_A)       
    
    # Paper carbon disposed.
    for i in range (ty):
        acc_D=0
    
        if i<=dp3:
            for j in range (i+1):
                temp_D=0
                yr_C=pap_C[j]
                dfr=pap_dr(i-j+1)
                temp_D=yr_C*dfr
                acc_D=acc_D+temp_D
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_D=0
               yr_C=pap_C[int(i-dp3+j)]
               dfr=pap_dr(dp3-j+1)
               temp_D=yr_C*dfr
               acc_D=acc_D+temp_D
            
        paper_yrD.append(acc_D)
    
    # Return:
    # accumulated paper carbon
    # disposed paper carbon
    
    return(paper_yrA,paper_yrD)
