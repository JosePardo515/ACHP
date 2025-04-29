import CoolProp.CoolProp as CP
from FinCorrelations import FinInputs
from Condenser import CondenserClass

def SampleCondenser(AS,T):
    Fins=FinInputs()
    Fins.Tubes.NTubes_per_bank=48       #number of tubes per bank or row
    Fins.Tubes.Nbank=3                  #number of banks or rows
    Fins.Tubes.Ncircuits=24             #number of circuits
    Fins.Tubes.Ltube=2.000              #one tube length
    Fins.Tubes.OD=0.00837
    Fins.Tubes.ID=0.00781
    Fins.Tubes.Pl=0.01905               #distance between center of tubes in flow direction                                                
    Fins.Tubes.Pt=0.0254                #distance between center of tubes orthogonal to flow direction
    Fins.Tubes.kw=385                   #Wall thermal conductivity
    
    Fins.Fins.FPI=16                    #Number of fins per inch
    Fins.Fins.Pd=0.001                  #2* amplitude of wavy fin
    Fins.Fins.xf=0.001                  #1/2 period of fin
    Fins.Fins.t=0.00011                 #Thickness of fin material
    Fins.Fins.k_fin=237                 #Thermal conductivity of fin material
    
    Fins.Air.Vdot_ha=5.5556             #rated volumetric flowrate
    Fins.Air.Tmean=308.15   
    Fins.Air.Tdb=308.15                 #Dry Bulb Temperature
    Fins.Air.p=101325                   #Air pressure in Pa
    Fins.Air.RH=0.51                    #Relative Humidity
    Fins.Air.RHmean=0.51
    Fins.Air.FanPower=1200    
    
    params={
        'AS': AS, #Abstract State
        'mdot_r': 0.0708,
        'Tin_r': T+20+273.15,
        'psat_r': CP.PropsSI('P','T',T+273.15,'Q',1.0,'R410A'),
        'Fins': Fins,
        'FinsType': 'HerringboneFins',  #Choose fin Type: 'WavyLouveredFins' or 'HerringboneFins'or 'PlainFins'
        'Verbosity':0,
        'h_a_tuning':1,
        'h_tp_tuning':1,
        'DP_tuning':1,
    }
    Cond=CondenserClass(**params)
    Cond.Calculate()
    return Cond

if __name__=='__main__':
    # This runs if you run this file directly
    Ref = 'R410A'
    Backend = 'HEOS' #choose between: 'HEOS','TTSE&HEOS','BICUBIC&HEOS','REFPROP','SRK','PR'
    AS = CP.AbstractState(Backend, Ref) #Abstract State
    Cond=SampleCondenser(AS,50)
    print (Cond.OutputList())
    
    print ('Heat transfer rate in condenser is', Cond.Q,'W')
    print ('Heat transfer rate in condenser (superheat section) is',Cond.Q_superheat,'W')
    print ('Heat transfer rate in condenser (twophase section) is',Cond.Q_2phase,'W')
    print ('Heat transfer rate in condenser (subcooled section) is',Cond.Q_subcool,'W')
    print ('Fraction of circuit length in superheated section is',Cond.w_superheat)
    print ('Fraction of circuit length in twophase section is',Cond.w_2phase)
    print ('Fraction of circuit length in subcooled section is',Cond.w_subcool) 
    print ()