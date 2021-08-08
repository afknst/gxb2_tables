<!---------------------------->
<!-- multilingual suffix: en, cn -->
<!-- no suffix: en -->
<!---------------------------->

<!-- [common] -->
# GxB2 PvP Simple Tier List

**Aug. 2021, by Aforest**  
[English](https://github.com/afknst/gxb2_tables/blob/master/test_results/tier_list.md),
[中文](https://github.com/afknst/gxb2_tables/blob/master/test_results/tier_list.cn.md)

<!-- [en] -->
>**D**: Damage source  
**S**: Support (buffer/healer)  
**C**: Control, mark, or skill effect (debuffer)  
**T**: Tank  
**M**: Multiple copies required/recommended  
**?**: Temporary

<!-- [cn] -->
>**D**: 输出  
**S**: 辅助 (加成/治疗)  
**C**: 控制, 印记, 或 技能效果 (减益)  
**T**: 坦克  
**M**: 需要/推荐 多个相同角色   
**?**: 临时

<!-- [en] -->
**T1**: In most cases **all** of the girls below are necessary to build a decent team  
Angelica (DC)    
Holly (TC)  

<!-- [cn] -->
**T1**: 强队通常需要以下**所有**角色   
后羿 (DC)  
槲寄生 (TC)  

<!-- [en] -->
**T2**: **Some** of the girls below are necessary  to build a decent team   
Apate (CD)  
Kassy (SD)  
Skye (SC)  
Teresa (TCD)  
Vivian (SCD)  

<!-- [cn] -->
**T2**: 强队需要其中**部分**角色  
阿帕忒 (CD)  
凱茜 (SD)  
稀風 (SC)  
特蕾莎 (TCD)  
薇薇安 (SCD)  

<!-- [en] -->
**T3**: **In rare cases** few girls below might be used in a decent team  
Frexie (CD)  
Izanami (SC)  
Joan (DC)  
Von Helsing (DCM)  

<!-- [cn] -->
**T3**: 强队**偶尔**需要其中某些角色    
菲斯納 (CD)  
伊邪那美 (SC)  
劉備 (DC)  
凡赫辛 (DCM)  

<!-- [en] -->
**T4**: Guardians of **sub teams**  
Mika (CTD)  
Nephilim (DC)  
Psychic (SC)  
Raphael (S)  
Vera (SCD)  

<!-- [cn] -->
**T4**: **二三队**守卫者  
雲母 (CTD)  
路西菲爾 (DC)  
黃月英 (SC)  
華佗 (S)  
薇拉 (SCD)  

<!-- [en] -->
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
