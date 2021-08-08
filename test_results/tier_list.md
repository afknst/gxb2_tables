# GxB2 PvP Simple Tier List

**Aug. 2021, by Aforest**  
[English](https://github.com/afknst/gxb2_tables/blob/master/test_results/tier_list.md),
[中文](https://github.com/afknst/gxb2_tables/blob/master/test_results/tier_list.cn.md)

>**D**: Damage source  
**S**: Support (buffer/healer)  
**C**: Control, mark, or skill effect (debuffer)  
**T**: Tank  
**M**: Multiple copies required/recommended  
**?**: Temporary

**T1**: In most cases **all** of the girls below are necessary to build a decent team  
Angelica (DC)    
Holly (TC)  

**T2**: **Some** of the girls below are necessary  to build a decent team   
Apate (CD)  
Kassy (SD)  
Skye (SC)  
Teresa (TCD)  
Vivian (SCD)  

**T3**: **In rare cases** few girls below might be used in a decent team  
Frexie (CD)  
Izanami (SC)  
Joan (DC)  
Von Helsing (DCM)  

**T4**: Guardians of **sub teams**  
Mika (CTD)  
Nephilim (DC)  
Psychic (SC)  
Raphael (S)  
Vera (SCD)  

---
**Additional Notes**  
Let `G` be the set of girls, and let `T` be the set of teams (i.e. `T = G^6`). The set of meta teams `MT` is defined as below:  
```
MT_(0) = T,
MT_(N+1) = {t in MT_(N) | the average win rate of t against all teams in MT_(N) is greater than or equal to 50%}.

If MT_(N) converges to a nonempty set as N goes to infinity, its limit is then called MT.
If MT_(N) converges to the empty set, the last set that is nonempty is then called MT.
```  
And the definitions of `T1` and `T2` are given by:  
```
T1 = {g in G | for all t in MT, g in t},
T2 = {g in G\T1 | there exists t in MT, g in t}.
```
