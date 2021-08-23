# GxB2 PvP Simple Tier List

**Aug. 2021, by Aforest**  
[English](https://github.com/afknst/gxb2_tables/blob/master/test_results/tier_list.md),
[中文](https://github.com/afknst/gxb2_tables/blob/master/test_results/tier_list.cn.md)

## Role
>**D**: Damage source  
**S**: Support (buffer/healer)  
**C**: Control, mark, or skill effect (debuffer)  
**T**: Tank  
**M**: Multiple copies required/recommended  
**?**: Temporary

## Equipment
>**SPD**: 3?332, Speed core, Deception, Speed excursion  
**HP**: 1?312, HP/HP, Eternal Dawn, HP excursion  
**ENERGY**: **SPD** but with energy antique  
**HP/CRIT**: **HP** but with Crit core  

## T1

In most cases **all** of the girls below are necessary to build a decent team  

>Angelica / 后羿 (DC): **HP/CRIT** or **ENERGY**     
Holly / 槲寄生 (TC): **HP**   

## T2

**Some** of the girls below are necessary  to build a decent team   

>Apate / 阿帕忒 (CD): **ENERGY** or **SPD**  
Kassy / 凱茜 (SD): **ENERGY**, **SPD**, or **HP**   
Skye / 稀風 (SC): **ENERGY**, **SPD**, or **HP**   
Teresa / 特蕾莎 (TCD): **SPD**  
Vivian / 薇薇安 (SCD): **HP**   

## T3

**In rare cases** few girls below might be used in a decent team  

>Frexie / 菲斯納 (CD): **HP** or **SPD**   
Izanami / 伊邪那美 (SC): **HP**   
Joan / 劉備 (DC): **HP/CRIT** or **HP**   
Von Helsing / 凡赫辛 (DCM): **ENERGY** or **SPD**   

## T4

Guardians of **sub teams**  

>Mika / 雲母 (CTD): **HP**  
Nephilim / 路西菲爾 (DC): **HP**  
Psychic / 黃月英 (SC): **HP**   
Raphael / 華佗 (S): **HP**  
Vera / 薇拉 (SCD): **HP**   

---
**Additional Notes**  

The current meta has no best team, but a few good teams that counter each other:

TEAM1:
 - 3-4 VH
 - 2-3 (Kassy and Skye)

TEAM2:   
 - 2 Angie
 - Kassy or Skye
 - Three girls in [Angie, Frexie, VH, Apate, Kassy, Skye, Holly, etc.]

TEAM3:  
 - Apate, Holly, Teresa, Vivian, Angelica
 - One girl in [Angie, Apate, Izanami, Vivian, etc.]

And: TEAM1 > TEAM2 > TEAM3 > TEAM1.

To counter TEAM1, TEAM2 can
1. use 2 Apate (and they have higher Atk than Angie), or
1. make Skye's Atk the highest.
1. use Joan (not recommended since the opponent can just add a Holly).

To counter TEAM2, TEAM3 can
1. use Izanami, and
1. equip with 2+ pink3 ED.
1. do nothing if the opponent uses Frexie.

To counter TEAM3, TEAM1 can
1. do nothing and just gives up.

**Definitions**

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
