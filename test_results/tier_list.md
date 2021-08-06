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

**T1**  
Angelica (DC)  
Apate (CD)  
Holly (TC?)  

**T2**  
Joan (DC)  
Kassy (SD?)  
Teresa (TCD)  
Vivian (SCD)  

**T3**  
Izanami (SC)  
Mika (CTD)  
Nephilim (DC)  
Skye (SC)  

**T4**  
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
