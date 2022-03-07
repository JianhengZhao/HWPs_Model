##########################################################
# In-use Harvested Wood Products Carbon Stock            #
# In-use HWPs-Stock                                      #
# Developed by Xinyuan Wei                               #
# Updated 2021/12/11                                     #
# Version 1.0                                            #
##########################################################

import pandas as pd 
import os 
import _Construction as CS
import _Home_Application as HA
import _Paper as PP

#%% 
##########################################################
# Read harvested wood carbon data.                       #
##########################################################

# Scenario file.
sc='Scenario_1'
directory=os.getcwd()+chr(92)+sc
#print(directory)

# Read the wood products file.
HW_filename=directory+chr(92)+'HWPs_Data.csv'
HW_data=pd.read_csv(HW_filename, sep=',')

# Read the disposal parameter file.
paras_file=directory+chr(92)+'HWPs_Paras.csv'
paras=pd.read_csv(paras_file, sep=',')

#%% 
##########################################################
# Analyzed time period infomation.                       #
##########################################################

# Print the year information.
Year_list=HW_data.Year.unique()
total_yr=len(HW_data)
sy=HW_data['Year'].at[0]
ey=HW_data['Year'].at[total_yr-1]
print('The time period is ', sy,'-',ey,'.')
print(total_yr, 'years in total.')
print('')

#%% 
##########################################################
# Read parameters.                                       #
##########################################################
                                                        
# Construction parameters (building and exterior).
con_dp1=paras.loc[paras['Para_Name']=='con_dp1']['Value'].tolist()[0]
con_dp2=paras.loc[paras['Para_Name']=='con_dp2']['Value'].tolist()[0]
con_dp3=paras.loc[paras['Para_Name']=='con_dp3']['Value'].tolist()[0]

# Home application parameters.
hma_dp1=paras.loc[paras['Para_Name']=='hma_dp1']['Value'].tolist()[0]
hma_dp2=paras.loc[paras['Para_Name']=='hma_dp2']['Value'].tolist()[0]
hma_dp3=paras.loc[paras['Para_Name']=='hma_dp3']['Value'].tolist()[0]

# Paper parameters.
nwp_dp1=paras.loc[paras['Para_Name']=='nwp_dp1']['Value'].tolist()[0]
nwp_dp2=paras.loc[paras['Para_Name']=='nwp_dp2']['Value'].tolist()[0]
nwp_dp3=paras.loc[paras['Para_Name']=='nwp_dp3']['Value'].tolist()[0]

pwp_dp1=paras.loc[paras['Para_Name']=='pwp_dp1']['Value'].tolist()[0]
pwp_dp2=paras.loc[paras['Para_Name']=='pwp_dp2']['Value'].tolist()[0]
pwp_dp3=paras.loc[paras['Para_Name']=='pwp_dp3']['Value'].tolist()[0]

otp_dp1=paras.loc[paras['Para_Name']=='otp_dp1']['Value'].tolist()[0]
otp_dp2=paras.loc[paras['Para_Name']=='otp_dp2']['Value'].tolist()[0]
otp_dp3=paras.loc[paras['Para_Name']=='otp_dp3']['Value'].tolist()[0]

#%% 
##########################################################
# Main function.                                         #
##########################################################

# Wood products.
con_C=HW_data['Construction']   
hma_C=HW_data['Home_Application']
nwp_C=HW_data['Newsprint_Paper']
pwp_C=HW_data['Printing_Writing_Paper']
otp_C=HW_data['Other_Paper']

def Main_Estimate ():
       
    results=[]
    
    # Construction.
    result_con=CS.Construction_C(total_yr,con_C,con_dp1,con_dp2,con_dp3)

    # Home Application.
    result_hma=HA.HomeA_C(total_yr,hma_C,hma_dp1,hma_dp2,hma_dp3)
    
    # Paper
    result_nwp=PP.Paper_C(total_yr,nwp_C,nwp_dp1,nwp_dp2,nwp_dp3)
    result_pwp=PP.Paper_C(total_yr,pwp_C,pwp_dp1,pwp_dp2,pwp_dp3)
    result_otp=PP.Paper_C(total_yr,otp_C,otp_dp1,otp_dp2,otp_dp3)
    
    for i in range (total_yr):
        temp=[]
        
        # Year.
        temp.append(HW_data['Year'].at[i])
        
        temp.append(round(result_con[0][i]))
        temp.append(round(result_con[1][i]))
        
        temp.append(round(result_hma[0][i]))
        temp.append(round(result_hma[1][i]))
        
        temp.append(round(result_nwp[0][i]))
        temp.append(round(result_nwp[1][i]))
        temp.append(round(result_pwp[0][i]))
        temp.append(round(result_pwp[1][i]))
        temp.append(round(result_otp[0][i]))
        temp.append(round(result_otp[1][i]))

                
        header=['Year',
                'Construction_A','Construction_D',
                'Home_Application_A','Home_Application_D',
                'Newsprint_A','Newsprint_D',
                'Printing_Writing_A','Printing_Writing_D',
                'Other_A','Other_D']
        
        results.append(temp)
    
    df=pd.DataFrame(data=results)
    df.to_csv(directory+chr(92)+'Results_Carbon.csv',index=False,header=header)    

Main_Estimate ()