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
**T1**  
Angelica (DC)  
Apate (CD)  
Holly (TS?)  

<!-- [cn] -->
**T1**  
后羿 (DC)  
阿帕忒 (CD)  
槲寄生 (TS?)  

<!-- [en] -->
**T2**  
Joan (DC)  
Kassy (SD?)  
Teresa (TCD)  
Vivian (SCD)  

<!-- [cn] -->
**T2**  
劉備 (DC)  
凱茜 (SD?)  
特蕾莎 (TCD)  
薇薇安 (SCD)  

<!-- [en] -->
**T3**  
Izanami (SC)  
Mika (CTD)  
Nephilim (DC)  
Skye (SC)  

<!-- [cn] -->
**T3**  
伊邪那美 (SC)  
雲母 (CTD)  
路西菲爾 (DC)  
稀風 (SC)  

<!-- [en] -->
**T4**  
Psychic (SC)  
Raphael (S)  
Vera (SCD)  

<!-- [cn] -->
**T4**  
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