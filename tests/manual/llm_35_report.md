# Live-LLM transcript — qwen/qwen3-32b (max_completion_tokens=2048, reasoning=raw/default)

35 questions · budget 2800 tok · pace 60.0s

## [1] CORE · mp=OFF · 2.7s

`billed: prompt=2926 completion=734 total=3660 · finish=stop` · ctx 2769 tok

**Q:** If a Battle-shocked unit that is below half-strength Falls Back, what tests does it take and can it still shoot or charge that turn?

<details><summary>reasoning trace (2033 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about a Battle-shocked unit that's below half-strength and Falls Back. They want to know what tests it takes and whether it can shoot or charge that turn.

First, I need to check the rules provided. Let's start with the Battle-shock rules. From [1], when a unit is Battle-shocked, it can't use Stratagems, has OC 0, and if it Falls Back, it must take Desperate Escape tests for every model. Also, Battle-shocked units can't shoot or declare a charge in the same turn they Fell Back. Wait, the Shooting Phase [3] says units that Fell Back can't shoot. Similarly, the Charge Phase [9] probably has a similar restriction. 

Looking at the Fall Back Moves [2], it states that units that Fall Back cannot shoot or declare a charge in the same turn. So regardless of being Battle-shocked, Falling Back alone makes them ineligible to shoot or charge. But since the unit is also Battle-shocked, there's an additional requirement for Desperate Escape tests for every model when they Fall Back. 

So, when the unit Falls Back, they take Desperate Escape tests for all models (because they're Battle-shocked, per [2]). Then, because they Fell Back, they can't shoot or charge that turn, as per [3] and [9]. The fact that they're below half-strength might have caused the Battle-shock in the first place, but the key points here are the effects of being Battle-shocked and Falling Back. 

I need to make sure there's no other rule that affects this. The Below Half-strength rule [4] just defines when a unit is considered Below Half-strength, which triggers Battle-shock tests. The main interactions here are between Battle-shock and Fall Back. 

So the ruling is: The unit must take Desperate Escape tests for all models when Falling Back (due to being Battle-shocked). Additionally, because they Fell Back, they cannot shoot or charge that turn. The relevant rules are [1] for Battle-shock effects, [2] for Fall Back mechanics, and [3] for the Shooting Phase restriction.
</think>

[Ruling]  
A Battle-shocked unit that Falls Back must take **Desperate Escape tests for every model in the unit** (due to being Battle-shocked). Additionally, the unit **cannot shoot or declare a charge in the same turn** it Fell Back.  

[Rule Citations]  
- **Desperate Escape tests**: [2. Fall Back Moves] → "If a unit is Battle-shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved."  
- **Cannot shoot/charge**: [3. Shooting Phase] → "A unit is eligible to shoot unless [...] that unit Fell Back this turn." + [9. Charge Phase] (implied by core rule: units that Fall Back cannot declare charges in the same turn).  

[Reasoning]  
1. **Desperate Escape Tests**: The unit is Battle-shocked (per [1. Battle-shock]), so Falling Back triggers a Desperate Escape test for **every model** (as stated in [2. Fall Back Moves]).  
2. **Shooting/Charging Restrictions**: Falling Back inherently disqualifies a unit from shooting (per [3. Shooting Phase]) or declaring charges (per standard rules) in the same turn, regardless of Battle-shock status.
```

</details>

**A:** [Ruling]  
A Battle-shocked unit that Falls Back must take **Desperate Escape tests for every model in the unit** (due to being Battle-shocked). Additionally, the unit **cannot shoot or declare a charge in the same turn** it Fell Back.  

[Rule Citations]  
- **Desperate Escape tests**: [2. Fall Back Moves] → "If a unit is Battle-shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved."  
- **Cannot shoot/charge**: [3. Shooting Phase] → "A unit is eligible to shoot unless [...] that unit Fell Back this turn." + [9. Charge Phase] (implied by core rule: units that Fall Back cannot declare charges in the same turn).  

[Reasoning]  
1. **Desperate Escape Tests**: The unit is Battle-shocked (per [1. Battle-shock]), so Falling Back triggers a Desperate Escape test for **every model** (as stated in [2. Fall Back Moves]).  
2. **Shooting/Charging Restrictions**: Falling Back inherently disqualifies a unit from shooting (per [3. Shooting Phase]) or declaring charges (per standard rules) in the same turn, regardless of Battle-shock status.

---

## [2] CORE · mp=OFF · 1.9s

`billed: prompt=2760 completion=620 total=3380 · finish=stop` · ctx 2714 tok

**Q:** If I set up a unit using Deep Strike from Strategic Reserves, how far from enemy models must it arrive and can it charge that same turn?

<details><summary>reasoning trace (1688 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about setting up a unit using Deep Strike from Strategic Reserves and wants to know two things: the required distance from enemy models and whether the unit can charge that same turn.

First, I need to look at the Deep Strike rules. From the provided context, rule [1] says that when a unit with Deep Strike arrives from Reserves, it can be set up more than 9" horizontally away from all enemy models. That's the key distance here. So the answer to the first part is 9 inches.

Next, the question about charging the same turn. The Deep Strike rule mentions that when a unit arrives from Strategic Reserves, it's set up using either Strategic Reserves rules or Deep Strike. But the main point is whether the unit can charge after arriving. Looking at rule [5], which covers Reinforcements, it states that Reserves units count as having made a Normal move in the turn they are set up. The Core Rules (rule [3] and [4]) say that units that Advance or Fall Back can't charge that turn, but Normal move isn't restricted in the same way. However, the key here is that the unit is set up as a Normal move. Rule [5] says they can act normally that turn, which includes declaring a charge. So if the unit is set up via Deep Strike (a Normal move), they can charge that same turn. 

Wait, but I should check if there's any other rule that might restrict this. The Deep Strike rule itself doesn't mention any restrictions on actions after setup. Rule [5] explicitly says that Reserves units can act normally, so shooting, charging, etc., are allowed. Therefore, the unit can charge in the same turn they arrive via Deep Strike.
</think>

[Ruling] A unit set up using Deep Strike from Strategic Reserves must be placed more than 9" horizontally away from all enemy models. It **can** declare a charge in the same turn it arrives.  

[Rule Citation]  
- **Distance Requirement:** Deep Strike (Core Rules) → "set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models."  
- **Charge Eligibility:** Reinforcements (Core Rules) → "Reserves units always count as having made a Normal move in the turn they are set up on the battlefield, and so cannot move further during this phase. Otherwise, units set up in this way can act normally this turn (shoot, declare a charge, fight, etc.)."  

[Reasoning]  
1. **Distance Requirement:** The Deep Strike rule explicitly requires units arriving from Reserves to be placed more than 9" horizontally from all enemies.  
2. **Charge Eligibility:** While Reserves units count as having made a Normal move (preventing further movement), they are not restricted from declaring a charge in the same turn, as per the Reinforcements rule. Charging does not require additional movement beyond the initial setup.
```

</details>

**A:** [Ruling] A unit set up using Deep Strike from Strategic Reserves must be placed more than 9" horizontally away from all enemy models. It **can** declare a charge in the same turn it arrives.  

[Rule Citation]  
- **Distance Requirement:** Deep Strike (Core Rules) → "set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models."  
- **Charge Eligibility:** Reinforcements (Core Rules) → "Reserves units always count as having made a Normal move in the turn they are set up on the battlefield, and so cannot move further during this phase. Otherwise, units set up in this way can act normally this turn (shoot, declare a charge, fight, etc.)."  

[Reasoning]  
1. **Distance Requirement:** The Deep Strike rule explicitly requires units arriving from Reserves to be placed more than 9" horizontally from all enemies.  
2. **Charge Eligibility:** While Reserves units count as having made a Normal move (preventing further movement), they are not restricted from declaring a charge in the same turn, as per the Reinforcements rule. Charging does not require additional movement beyond the initial setup.

---

## [3] CORE · mp=OFF · 2.8s

`billed: prompt=2915 completion=1054 total=3969 · finish=stop` · ctx 2780 tok

**Q:** When my unit makes a charge move over a barricade, can it end in Engagement Range with an enemy on the floor above, and does the barricade affect the move?

<details><summary>reasoning trace (3548 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking if their unit can charge over a barricade and end in Engagement Range with an enemy on the floor above, and whether the barricade affects the move.

First, I need to look at the rules related to barricades. From the provided context, [1] Barricades and Fuel Pipes says that models can move up, over, and down the terrain feature but cannot set up or end any move on top of it. So moving over is allowed, but ending on top isn't. 

Next, the charge move rules from [3] Charging with a Unit state that a charge must end within Engagement Range of the target. The question is whether moving over the barricade allows ending in Engagement Range with an enemy on the other side. The barricade's rule under Engagement Range says that if an enemy is within 1" of the barricade, a charging unit on the opposite side can charge them if they end within 2" of the enemy. Wait, that's in the Charge phase. So during a charge, if the enemy is within 1" of the barricade, the charging unit can charge them even if they're on the other side, provided they end within 2" of the enemy. 

But the user is asking about ending in Engagement Range. Engagement Range is typically 1", so if the barricade allows the charge to end within 2" of the enemy, does that count as Engagement Range? The barricade's Engagement Range rule says that during the Charge phase, if the enemy is within 1" of the barricade, the charging unit can charge them and end within 2". However, the standard Engagement Range is 1", so maybe the barricade allows an exception here. 

But the main question is about ending in Engagement Range. The barricade's rule says that models can move over it but can't end on top. So if the unit charges over the barricade and ends in base-to-base contact with an enemy on the other side, that's allowed as long as they end within Engagement Range. However, the barricade's rule allows the charge to end within 2" of the enemy if the enemy is within 1" of the barricade. So if the enemy is right next to the barricade, the charging unit can end within 2" of them, which might not be Engagement Range. But during the Fight phase, the barricade allows units to fight if they're on opposite sides within 2". 

Wait, the user is asking about a Charge move. The barricade's Engagement Range rule for the Charge phase says that if the enemy is within 1" of the barricade, the charging unit can charge them and end within 2" of the enemy. So in that case, the charge would end within 2", which is not Engagement Range (which is 1"). But the rule says that the charge can still be made. However, the standard charge requires ending within Engagement Range (1"). So there's a conflict here. 

But the barricade's specific rule overrides the normal charge rules. The rule says that during the Charge phase, if the enemy is within 1" of the barricade, the charging unit can charge them and end within 2". So in this case, the barricade allows the charge to end within 2", which is not Engagement Range, but the rule allows it. Therefore, the barricade affects the charge move by allowing the charge to end within 2" of the enemy, even though normally it would need to be within 1". 

So the answer is that yes, the unit can charge over the barricade and end in Engagement Range (as modified by the barricade's rule) with the enemy on the other side, provided they end within 2" of the enemy if the enemy is within 1" of the barricade. The barricade does affect the move by allowing this exception.
</think>

[Ruling] Yes, a unit can make a Charge move over a barricade and end in Engagement Range with an enemy on the opposite side, provided the enemy is within 1" of the barricade. The barricade allows the charging unit to end its Charge move within 2" of the enemy unit (instead of the standard Engagement Range of 1") if the enemy is within 1" of the barricade. However, the barricade itself does not block the movement—models can move over it, but cannot end a move on top of it.  

[Rule Citation] **Barricades and Fuel Pipes (Engagement Range)** → [1]  
[Reasoning] The barricade’s Engagement Range rule explicitly allows a charging unit to end its Charge move as close as possible to the barricade and within 2" of an enemy unit on the opposite side, provided the enemy is within 1" of the barricade. This overrides the standard Engagement Range requirement (1") for the purpose of this specific terrain feature. Additionally, the barricade’s general movement rule permits models to move over it, but they cannot end a move on top of it.
```

</details>

**A:** [Ruling] Yes, a unit can make a Charge move over a barricade and end in Engagement Range with an enemy on the opposite side, provided the enemy is within 1" of the barricade. The barricade allows the charging unit to end its Charge move within 2" of the enemy unit (instead of the standard Engagement Range of 1") if the enemy is within 1" of the barricade. However, the barricade itself does not block the movement—models can move over it, but cannot end a move on top of it.  

[Rule Citation] **Barricades and Fuel Pipes (Engagement Range)** → [1]  
[Reasoning] The barricade’s Engagement Range rule explicitly allows a charging unit to end its Charge move as close as possible to the barricade and within 2" of an enemy unit on the opposite side, provided the enemy is within 1" of the barricade. This overrides the standard Engagement Range requirement (1") for the purpose of this specific terrain feature. Additionally, the barricade’s general movement rule permits models to move over it, but they cannot end a move on top of it.

---

## [4] CORE · mp=OFF · 1.9s

`billed: prompt=2676 completion=558 total=3234 · finish=stop` · ctx 2759 tok

**Q:** How does Big Guns Never Tire let a Monster or Vehicle shoot while within Engagement Range, and what penalty applies to those ranged attacks?

<details><summary>reasoning trace (1819 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking how the "Big Guns Never Tire" rule allows Monsters and Vehicles to shoot while in Engagement Range and what penalties apply to their ranged attacks.

First, I need to recall the relevant rules from the provided context. The user provided several sections, but the key one here is [1] Big Guns Never Tire. Let me check that again.

From [1], it says that MONSTER and VEHICLE units can shoot in their controlling player's Shooting phase even if they're within Engagement Range of enemies. That's the main point. Also, when they make ranged attacks while in Engagement Range, unless the attack is with a Pistol, subtract 1 from the Hit roll. Additionally, if they target an enemy MONSTER or VEHICLE that's within Engagement Range of friendly units, the same -1 penalty applies unless it's a Pistol.

So the answer should state that Monsters and Vehicles can shoot even in Engagement Range, and the penalty is -1 to Hit rolls for non-Pistol attacks. The source is Big Guns Never Tire from Core Rules.

I need to make sure there's no other rule conflicting. The Make Ranged Attacks section [2] mentions that normally units can't shoot if in Engagement Range, but Monsters and Vehicles are exceptions as per Big Guns. The Pistol rule [3] allows units with Pistols to shoot in Engagement Range, but that's a separate case. The question is about Monsters and Vehicles, so the Pistol part isn't directly relevant here except to note that Pistols don't get the penalty.

So the ruling is that Monsters and Vehicles can shoot while in Engagement Range, and their non-Pistol attacks have a -1 to Hit. The penalty applies both when they attack and when they are attacked by other units. The key is the Big Guns Never Tire rule overrides the normal restriction.
</think>

[Ruling] MONSTER and VEHICLE units can shoot in their controlling player's Shooting phase even while within Engagement Range of enemy units. When making ranged attacks under these conditions, subtract 1 from the Hit roll for each attack unless the attack is made with a Pistol. This penalty applies both when the MONSTER/VEHICLE is attacking and when other units are targeting them.  

[Rule Citation] Big Guns Never Tire (Core Rules) → Wahapedia_Core_Rules  

[Reasoning] The Big Guns Never Tire rule explicitly grants MONSTER and VEHICLE units the ability to shoot while in Engagement Range, overriding the standard restriction in Make Ranged Attacks (Core Rules). The penalty (-1 to Hit rolls for non-Pistol attacks) is detailed in the same rule, applying to both offensive and defensive ranged attacks involving MONSTER/VEHICLE units under these conditions.
```

</details>

**A:** [Ruling] MONSTER and VEHICLE units can shoot in their controlling player's Shooting phase even while within Engagement Range of enemy units. When making ranged attacks under these conditions, subtract 1 from the Hit roll for each attack unless the attack is made with a Pistol. This penalty applies both when the MONSTER/VEHICLE is attacking and when other units are targeting them.  

[Rule Citation] Big Guns Never Tire (Core Rules) → Wahapedia_Core_Rules  

[Reasoning] The Big Guns Never Tire rule explicitly grants MONSTER and VEHICLE units the ability to shoot while in Engagement Range, overriding the standard restriction in Make Ranged Attacks (Core Rules). The penalty (-1 to Hit rolls for non-Pistol attacks) is detailed in the same rule, applying to both offensive and defensive ranged attacks involving MONSTER/VEHICLE units under these conditions.

---

## [5] CORE · mp=OFF · 2.4s

`billed: prompt=2752 completion=372 total=3124 · finish=stop` · ctx 2689 tok

**Q:** If I shoot with an Indirect Fire weapon at a target I cannot see, what modifier applies to my hit rolls and does the target get the Benefit of Cover?

<details><summary>reasoning trace (813 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about using an Indirect Fire weapon when the target isn't visible. I need to check the rules provided.

Looking at the Indirect Fire entry (Rule 1), it says that if no models in the target unit are visible, then each attack with an Indirect Fire weapon subtracts 1 from the Hit roll. Also, an unmodified Hit roll of 1-3 always fails, and the target gets the Benefit of Cover. 

So the key points here are the -1 modifier to Hit rolls and the Benefit of Cover. The user is specifically asking about the modifiers and cover, which are both covered in the Indirect Fire rule. The other rules like Rapid Fire or Big Guns Never Tire don't seem relevant here. The answer should reference Rule 1 and confirm both the modifier and the cover benefit.
</think>

[Ruling] When using an Indirect Fire weapon against a target where no models are visible, subtract 1 from your Hit rolls, unmodified Hit rolls of 1–3 always fail, and the target gains the **Benefit of Cover** against the attack.  
[Rule Citation] **Indirect Fire** (Core Rules) → "If no models in a target unit are visible to the attacking unit when you select that target, then each time a model in the attacking unit makes an attack against that target using an Indirect Fire weapon, subtract 1 from that attack's Hit roll, an unmodified Hit roll of 1–3 always fails, and the target has the Benefit of Cover against that attack."  
[Reasoning] The rules explicitly state the penalties for targeting invisible units with Indirect Fire weapons, including the -1 modifier, automatic failure for low rolls, and cover benefits. No other rules override this scenario.
```

</details>

**A:** [Ruling] When using an Indirect Fire weapon against a target where no models are visible, subtract 1 from your Hit rolls, unmodified Hit rolls of 1–3 always fail, and the target gains the **Benefit of Cover** against the attack.  
[Rule Citation] **Indirect Fire** (Core Rules) → "If no models in a target unit are visible to the attacking unit when you select that target, then each time a model in the attacking unit makes an attack against that target using an Indirect Fire weapon, subtract 1 from that attack's Hit roll, an unmodified Hit roll of 1–3 always fails, and the target has the Benefit of Cover against that attack."  
[Reasoning] The rules explicitly state the penalties for targeting invisible units with Indirect Fire weapons, including the -1 modifier, automatic failure for low rolls, and cover benefits. No other rules override this scenario.

---

## [6] CORE · mp=OFF · 3.5s

`billed: prompt=2697 completion=845 total=3542 · finish=stop` · ctx 2608 tok

**Q:** How do Devastating Wounds interact with invulnerable saves and Feel No Pain — which of those can still be used against the damage?

<details><summary>reasoning trace (2704 chars, billed)</summary>

```
<think>
Okay, let's tackle this question about Devastating Wounds and their interaction with invulnerable saves and Feel No Pain. The user wants to know which of these abilities can still be used against the damage caused by Devastating Wounds.

First, I need to recall the rules provided. From the context, Devastating Wounds are a type of weapon that, when a Critical Wound is scored (which is an unmodified Wound roll of 6), the attack bypasses all saving throws, including invulnerable ones. The Devastating Wounds rule (1) states that no saving throw of any kind can be made against such attacks. So, invulnerable saves are out of the question here because the rule explicitly says they can't be used.

Next, looking at Feel No Pain (2), which allows a model to ignore wounds based on a D6 roll. The question is whether Feel No Pain can be used against the mortal wounds caused by Devastating Wounds. The Mortal Wounds rule (3) mentions that if the mortal wounds are from Devastating Wounds, then when a model is destroyed by those wounds, the remaining wounds are lost. However, the key part here is that Feel No Pain is about ignoring wounds when they are suffered. Since Devastating Wounds cause mortal wounds, and mortal wounds are a form of damage that is applied after normal damage. 

But according to the Devastating Wounds rule (1), when a Critical Wound is scored, the attack inflicts mortal wounds equal to the weapon's Damage characteristic. The Mortal Wounds rule (3) says that no saving throws can be made against mortal wounds. However, Feel No Pain is not a saving throw; it's an ability that allows a model to ignore wounds when they would be lost. The Feel No Pain rule (2) applies when a model suffers damage and would lose a wound. Since the mortal wounds from Devastating Wounds are still damage that causes wounds to be lost, Feel No Pain could be used here. 

Wait, but the Devastating Wounds rule says that no saving throws can be made, but Feel No Pain isn't a saving throw. The Core Rules differentiate between saving throws (like armour or invulnerable saves) and abilities like Feel No Pain. Since Feel No Pain is an ability that's applied after the damage is inflicted, it's not a saving throw. Therefore, even though Devastating Wounds prevent saving throws, Feel No Pain can still be used because it's a separate mechanic.

So putting it all together: Devastating Wounds negate invulnerable saves and all other saving throws, but Feel No Pain can still be used against the resulting mortal wounds because it's not a saving throw. The answer should reference the Devastating Wounds rule for invulnerable saves and the Feel No Pain rule for its applicability.
</think>

[Ruling] Devastating Wounds completely bypass **invulnerable saves** and **all other saving throws**, but **Feel No Pain** can still be used against the mortal wounds they inflict.  
[Rule Citation]  
- **Devastating Wounds** (1): "No saving throw of any kind can be made against that attack (including invulnerable saving throws)."  
- **Feel No Pain** (2): "Each time a model with this ability suffers damage and so would lose a wound [...] roll one D6: if the result equals or exceeds 'x', that wound is ignored and is not lost."  
[Reasoning]  
Devastating Wounds explicitly negate all saving throws (including invulnerable saves) when a Critical Wound is scored. However, **Feel No Pain** is not a saving throw—it is an ability that allows a model to ignore wounds after damage is applied. Since mortal wounds from Devastating Wounds still cause models to "suffer damage and so would lose a wound," Feel No Pain can be used to potentially ignore those wounds. The Devastating Wounds rule does not override Feel No Pain, as the latter operates at a different stage of the attack sequence (post-damage allocation).
```

</details>

**A:** [Ruling] Devastating Wounds completely bypass **invulnerable saves** and **all other saving throws**, but **Feel No Pain** can still be used against the mortal wounds they inflict.  
[Rule Citation]  
- **Devastating Wounds** (1): "No saving throw of any kind can be made against that attack (including invulnerable saving throws)."  
- **Feel No Pain** (2): "Each time a model with this ability suffers damage and so would lose a wound [...] roll one D6: if the result equals or exceeds 'x', that wound is ignored and is not lost."  
[Reasoning]  
Devastating Wounds explicitly negate all saving throws (including invulnerable saves) when a Critical Wound is scored. However, **Feel No Pain** is not a saving throw—it is an ability that allows a model to ignore wounds after damage is applied. Since mortal wounds from Devastating Wounds still cause models to "suffer damage and so would lose a wound," Feel No Pain can be used to potentially ignore those wounds. The Devastating Wounds rule does not override Feel No Pain, as the latter operates at a different stage of the attack sequence (post-damage allocation).

---

## [7] CORE · mp=OFF · 2.2s

`billed: prompt=2529 completion=696 total=3225 · finish=stop` · ctx 2416 tok

**Q:** When a Transport is destroyed with units still embarked, how do the passengers disembark and can they take damage?

<details><summary>reasoning trace (2140 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about what happens when a Transport is destroyed with units still inside. They want to know how the passengers disembark and if they can take damage.

First, I need to look at the rules provided. The main rule here is [1] Destroyed Transports. That section says that if a Transport is destroyed, any embarked units must disembark immediately. The process involves rolling a D6 for each disembarking model. If you roll a 1, the unit suffers a mortal wound. Also, the unit becomes Battle-shocked until the start of the next Command phase and can't charge for the rest of the turn. 

Then there's the Emergency Disembarkation part. If the unit can't be set up within 3" of the Transport, they have to do an emergency disembark. In that case, they set up within 6" and the mortal wound chance increases to 1-3. If they still can't be placed, the models are destroyed. 

So, the key points are: when the Transport is destroyed, the units must disembark. They roll for damage, get Battle-shocked, and can't charge. If they can't set up properly, emergency rules apply with higher damage and possible destruction.

I should check if there's any other relevant rules. The [4] Deadly Demise rule might come into play if the Transport has that ability. But the question doesn't mention Deadly Demise, so maybe it's not applicable here unless the Transport has it. The user's question is general, so the answer should focus on the standard destroyed Transport rules unless specified otherwise.

Also, the [7] Persisting Effects rule mentions that effects continue if a unit disembarks, but that's more about ongoing effects, not the disembarkation from destruction. So probably not relevant here.

Putting it all together: When a Transport is destroyed, embarked units disembark immediately. They roll D6 each for possible mortal wounds (1 for normal, 1-3 for emergency). They become Battle-shocked and can't charge. If they can't set up in the required range, emergency rules apply. The answer should reference the Destroyed Transports rule and explain the process step by step.
</think>

[Ruling] When a TRANSPORT is destroyed with units embarked, those units must immediately disembark. They roll one D6 per model for mortal wounds (1 = 1 mortal wound), become Battle-shocked until the start of their controlling player's next Command phase, and cannot declare a charge until the end of the turn. If they cannot be set up wholly within 3" of the destroyed TRANSPORT and not in Engagement Range of enemies, Emergency Disembarkation applies (6" range, 1-3 = mortal wound, and models that still cannot be set up are destroyed).  

[Rule Citation] → [1] Destroyed Transports (Wahapedia_Core_Rules)  
[Reasoning] The core rule explicitly states that destroyed TRANSPORTs force embarked units to disembark, with the associated mortal wound rolls, Battle-shocked status, and movement restrictions. Emergency Disembarkation is triggered if standard disembarkation is impossible, increasing the mortal wound threshold and setup range. No other rules override this process unless the TRANSPORT has a specific ability (e.g., Deadly Demise, not mentioned here).
```

</details>

**A:** [Ruling] When a TRANSPORT is destroyed with units embarked, those units must immediately disembark. They roll one D6 per model for mortal wounds (1 = 1 mortal wound), become Battle-shocked until the start of their controlling player's next Command phase, and cannot declare a charge until the end of the turn. If they cannot be set up wholly within 3" of the destroyed TRANSPORT and not in Engagement Range of enemies, Emergency Disembarkation applies (6" range, 1-3 = mortal wound, and models that still cannot be set up are destroyed).  

[Rule Citation] → [1] Destroyed Transports (Wahapedia_Core_Rules)  
[Reasoning] The core rule explicitly states that destroyed TRANSPORTs force embarked units to disembark, with the associated mortal wound rolls, Battle-shocked status, and movement restrictions. Emergency Disembarkation is triggered if standard disembarkation is impossible, increasing the mortal wound threshold and setup range. No other rules override this process unless the TRANSPORT has a specific ability (e.g., Deadly Demise, not mentioned here).

---

## [8] CORE · mp=OFF · 3.2s

`billed: prompt=2839 completion=461 total=3300 · finish=stop` · ctx 2796 tok

**Q:** Can a unit that Advanced still shoot Assault weapons, and is it allowed to declare a charge in the same turn?

<details><summary>reasoning trace (1346 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking if a unit that Advanced can still shoot Assault weapons and if they can declare a charge in the same turn. 

First, I need to check the rules provided. Let's start with the Assault weapons rule. From rule [1], it says that units that Advanced this turn can still shoot in the Shooting phase if they have Assault weapons. The key part here is that when a unit Advances, they can shoot in the Shooting phase but only with Assault weapons. So that answers the first part about shooting Assault weapons.

Next, the second part is about declaring a charge. Looking at rule [3], which covers Advance moves, there's a line that says "A unit cannot shoot or declare a charge in the same turn that it Advanced." So that directly states that if a unit Advanced, they can't declare a charge in that turn. 

Wait, but I should check the Charge phase rules too. Rule [4] mentions eligibility for charging, and one of the conditions is that the unit can't have Advanced or Fell Back. So even if the unit didn't shoot, if they Advanced, they can't charge. So combining both rules [3] and [4], the answer is clear: Advanced units can't charge.

So putting it all together: Yes, they can shoot Assault weapons (due to rule [1]) but no, they can't declare a charge (due to rules [3] and [4]).
</think>

[Ruling] A unit that Advanced can shoot Assault weapons in the Shooting phase but cannot declare a charge in the same turn.  
[Rule Citation]  
- Assault weapons: [1] "If a unit that Advanced this turn contains any models equipped with Assault weapons, it is still eligible to shoot in this turn's Shooting phase."  
- Charge restriction: [3] "A unit cannot shoot or declare a charge in the same turn that it Advanced."  

[Reasoning]  
The Assault weapon rule explicitly allows units that Advanced to shoot in the Shooting phase, but only with Assault weapons. The Advance move rule explicitly prohibits units that Advanced from declaring a charge in the same turn. The Charge phase eligibility rules ([4]) further reinforce this by excluding units that Advanced from charging.
```

</details>

**A:** [Ruling] A unit that Advanced can shoot Assault weapons in the Shooting phase but cannot declare a charge in the same turn.  
[Rule Citation]  
- Assault weapons: [1] "If a unit that Advanced this turn contains any models equipped with Assault weapons, it is still eligible to shoot in this turn's Shooting phase."  
- Charge restriction: [3] "A unit cannot shoot or declare a charge in the same turn that it Advanced."  

[Reasoning]  
The Assault weapon rule explicitly allows units that Advanced to shoot in the Shooting phase, but only with Assault weapons. The Advance move rule explicitly prohibits units that Advanced from declaring a charge in the same turn. The Charge phase eligibility rules ([4]) further reinforce this by excluding units that Advanced from charging.

---

## [9] CORE · mp=OFF · 2.1s

`billed: prompt=1921 completion=708 total=2629 · finish=stop` · ctx 1750 tok

**Q:** In the Fight phase, when both players have units in combat and one unit has Fights First, what is the order in which units fight?

<details><summary>reasoning trace (2049 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about the order of units fighting in the Fight phase when both players have units in combat and one unit has the Fights First ability.

First, I need to recall the core rules provided. From the context, the Fight phase is divided into two steps: 1. Fights First and 2. Remaining Combats. 

Looking at rule [1], the Fight phase starts with units that can Fight First. These units go first. Then, the remaining eligible units fight in the Remaining Combats step. The key here is that during the Fights First step, only units with the Fights First ability fight. After that, any remaining units, including those that became eligible later (like after a Consolidation move), fight in the Remaining Combats step.

Rule [3] specifies that in the Fights First step, all eligible units with the Fights First ability fight. It also mentions that units that made a Charge move this turn and have a Charge bonus are included. So, if a unit has Fights First, they fight in the first step.

Rule [2] then covers the Remaining Combats step, where all other eligible units fight. This includes any units that weren't eligible at the start of the Fight phase but became eligible later, such as after a Consolidation move.

So, the order would be: first, all units with Fights First fight in the Fights First step. Then, in the Remaining Combats step, the remaining eligible units (those without Fights First or those that became eligible later) fight. The players alternate selecting units, starting with the non-turn player, as per rule [1]. Also, note that each unit can only fight once in the phase.

The user's scenario has both players with units in combat, and one unit has Fights First. So, during the Fights First step, the unit with Fights First (assuming it's eligible) would fight first. Then, the Remaining Combats step would handle the rest. The exact order depends on which player's turn it is and the selection order, but the key is the two-step process with Fights First first.
</think>

[Ruling] In the Fight phase, units with the **Fights First** ability fight during the **Fights First step**, followed by all remaining eligible units during the **Remaining Combats step**. If both players have eligible units, they alternate selecting units to fight, starting with the player whose turn is **not** currently taking place. Units with Fights First must fight first in their step, and no unit can fight more than once.  

[Rule Citation]  
- **Fights First step**: Units with the *Fights First* ability fight first (Core Rules 1. Fights First).  
- **Remaining Combats step**: All other eligible units fight afterward (Core Rules 2. Remaining Combats).  
- **Selection order**: Players alternate selecting units to fight, starting with the non-turn player (Core Rules 1. FIGHT PHASE).  

[Reasoning]  
The Fight phase is explicitly split into two steps. Units with *Fights First* resolve their combat in the first step, ensuring they strike before others. Afterward, the Remaining Combats step handles all other eligible units. The selection order (non-turn player first) ensures fairness, and no unit may fight twice. This applies even if both players have units in combat.
```

</details>

**A:** [Ruling] In the Fight phase, units with the **Fights First** ability fight during the **Fights First step**, followed by all remaining eligible units during the **Remaining Combats step**. If both players have eligible units, they alternate selecting units to fight, starting with the player whose turn is **not** currently taking place. Units with Fights First must fight first in their step, and no unit can fight more than once.  

[Rule Citation]  
- **Fights First step**: Units with the *Fights First* ability fight first (Core Rules 1. Fights First).  
- **Remaining Combats step**: All other eligible units fight afterward (Core Rules 2. Remaining Combats).  
- **Selection order**: Players alternate selecting units to fight, starting with the non-turn player (Core Rules 1. FIGHT PHASE).  

[Reasoning]  
The Fight phase is explicitly split into two steps. Units with *Fights First* resolve their combat in the first step, ensuring they strike before others. Afterward, the Remaining Combats step handles all other eligible units. The selection order (non-turn player first) ensures fairness, and no unit may fight twice. This applies even if both players have units in combat.

---

## [10] CORE · mp=OFF · 2.7s

`billed: prompt=2754 completion=821 total=3575 · finish=stop` · ctx 2754 tok

**Q:** Does a Battle-shocked unit still control objective markers, and how does being below half-strength affect that unit?

<details><summary>reasoning trace (2382 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking whether a Battle-shocked unit still controls objective markers and how being below half-strength affects that unit.

First, I need to recall the relevant rules from the provided context. Let's start with Battle-shock. From rule [1], when a unit is Battle-shocked, one of the effects is that the Objective Control (OC) characteristic of all its models becomes 0. Objective Control is crucial for controlling markers because, as per rule [4], the Level of Control is determined by summing the OC of all models within range. If a unit's OC is 0, their contribution to the Level of Control would be nothing. So, Battle-shocked units can't contribute to controlling objective markers because their OC is zero.

Next, the question also asks about being Below Half-strength. Rule [2] defines Below Half-strength: a unit is Below Half-strength if the number of models is less than half its Starting Strength. However, being Below Half-strength triggers Battle-shock tests, but the actual effect on Objective Control comes from the Battle-shock result, not just being Below Half-strength. So, unless the unit fails the Battle-shock test and becomes Battle-shocked, its OC remains normal. If it's Below Half-strength but passes the Battle-shock test, it's not Battle-shocked, so its OC is unaffected. But if it fails, then OC drops to 0 as per Battle-shock rules.

So putting it together: Battle-shocked units have OC 0, so they don't contribute to controlling markers. Being Below Half-strength leads to Battle-shock tests, which if failed, result in Battle-shock and thus loss of OC. But being Below Half-strength alone doesn't directly affect OC unless the Battle-shock test is failed.

I need to check if there's any other rule that might affect this. Rule [4] mentions OC is based on models' characteristics. Rule [1] explicitly sets OC to 0 when Battle-shocked. There's no mention of Below Half-strength affecting OC directly. So the answer hinges on the Battle-shock status, not just being Below Half-strength.

Therefore, the ruling is that Battle-shocked units cannot control objective markers because their OC is 0. Being Below Half-strength leads to Battle-shock tests, which if failed, cause the unit to be Battle-shocked, thereby losing OC. If the test is passed, the unit remains unaffected in terms of OC.
</think>

[Ruling] A Battle-shocked unit **does not control objective markers** because its models' Objective Control (OC) is set to 0 while Battle-shocked. Being **Below Half-strength** triggers a Battle-shock test, but only failing that test (not merely being Below Half-strength) causes the unit to lose OC.  

[Rule Citation]  
- **Battle-shock (Core Rules)**: "While a unit is Battle-shocked: [...] The Objective Control characteristic of all of its models is 0."  
- **Below Half-strength (Core Rules)**: Defines when a unit is Below Half-strength, which triggers Battle-shock tests.  
- **Objective Markers (Core Rules)**: "To determine a player's Level of Control over an objective marker, add together the OC characteristics of all the models [...] within range."  

[Reasoning]  
1. **Battle-shocked units**: Their OC is explicitly set to 0, so they cannot contribute to controlling objective markers.  
2. **Below Half-strength**: This condition triggers a Battle-shock test (per rule [1]), but only failing that test results in Battle-shock (and thus OC = 0). If the test is passed, the unit retains its OC and can control markers.  
3. **Objective Control**: OC is calculated based on models' characteristics, which are nullified by Battle-shock but not by merely being Below Half-strength.
```

</details>

**A:** [Ruling] A Battle-shocked unit **does not control objective markers** because its models' Objective Control (OC) is set to 0 while Battle-shocked. Being **Below Half-strength** triggers a Battle-shock test, but only failing that test (not merely being Below Half-strength) causes the unit to lose OC.  

[Rule Citation]  
- **Battle-shock (Core Rules)**: "While a unit is Battle-shocked: [...] The Objective Control characteristic of all of its models is 0."  
- **Below Half-strength (Core Rules)**: Defines when a unit is Below Half-strength, which triggers Battle-shock tests.  
- **Objective Markers (Core Rules)**: "To determine a player's Level of Control over an objective marker, add together the OC characteristics of all the models [...] within range."  

[Reasoning]  
1. **Battle-shocked units**: Their OC is explicitly set to 0, so they cannot contribute to controlling objective markers.  
2. **Below Half-strength**: This condition triggers a Battle-shock test (per rule [1]), but only failing that test results in Battle-shock (and thus OC = 0). If the test is passed, the unit retains its OC and can control markers.  
3. **Objective Control**: OC is calculated based on models' characteristics, which are nullified by Battle-shock but not by merely being Below Half-strength.

---

## [11] LEVIATHAN · mp=ON · 2.5s

`billed: prompt=2053 completion=748 total=2801 · finish=stop` · ctx 2040 tok

**Q:** Using Tactical Missions in Leviathan, how does the Assassination Secondary Mission score when I destroy enemy Characters, and does a resurrected Character count?

<details><summary>reasoning trace (2498 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about the Assassination Secondary Mission in Leviathan when using Tactical Missions. They want to know how it scores when destroying enemy Characters and whether a resurrected Character counts.

First, I need to look at the provided rules context. Let's check the Assassination Secondary Mission description. From entry [1], under Tactical Missions, the Secondary Mission is achieved if either condition is met: one or more enemy CHARACTER units destroyed during the turn, or all CHARACTER units from the opponent's Army Roster destroyed. The note says that even if a unit is destroyed and then resurrected, the mission is still achieved. So, for Tactical Missions, scoring 5VP if either condition is met, and the resurrection doesn't negate it.

Now, the user is using Tactical Missions, so the relevant part is the Tactical Missions condition. Each time an enemy CHARACTER model is destroyed, they score VP. But wait, the description says "each time an enemy CHARACTER model is destroyed, you score 4VP." Wait, no, looking again: under Fixed Missions, it's 4VP per destroyed CHARACTER model. But under Tactical Missions, it's different. For Tactical Missions, at the end of the turn, if either condition is satisfied, you score 5VP. The note clarifies that even if destroyed and resurrected, it counts. So the key here is that for Tactical Missions, the mission is achieved if any CHARACTER is destroyed during the turn, regardless of resurrection. The VP scored is 5VP if achieved, not per model. Wait, no, the Fixed Missions part says "each time an enemy CHARACTER model is destroyed, you score 4VP." But for Tactical Missions, it's a one-time 5VP if the conditions are met. The note says VP are scored even if the model is destroyed and resurrected. So, if a CHARACTER is destroyed once, even if it comes back, the mission is achieved. Also, if multiple CHARACTERS are destroyed, does that matter? The Tactical Missions condition is met if any one or more are destroyed. So even one destroyed CHARACTER would trigger the 5VP. Also, if all the opponent's CHARACTERs are destroyed, same thing. The note says that even if destroyed and resurrected, it counts. So the answer is that for Tactical Missions, the Assassination Secondary Mission gives 5VP if either condition is met during the turn, and resurrection doesn't affect it. The citation is from the Assassination Secondary Mission description in the context provided.
</think>

[Ruling] When using Tactical Missions, the **Assassination** Secondary Mission scores 5VP at the end of the turn if either of its conditions are met (destroying one or more enemy CHARACTER units, or destroying all of your opponent’s CHARACTER units from their Army Roster). Resurrected CHARACTER models still count toward this mission.  

[Rule Citation] **ASSASSINATION** (Secondary Mission deck [1]) → "If you are using Tactical Missions, then at the end of the turn, if either of the conditions below are satisfied, this Secondary Mission is achieved and you score 5VP... Note that if you are using Tactical Missions, this Secondary Mission is achieved even if such a unit was destroyed and then subsequently resurrected for any reason."  

[Reasoning] The mission explicitly states that resurrection does not invalidate the VP gain. For Tactical Missions, the mission is achieved if the conditions are met during the turn, regardless of subsequent resurrection. The 5VP is awarded once per turn if the mission is achieved.
```

</details>

**A:** [Ruling] When using Tactical Missions, the **Assassination** Secondary Mission scores 5VP at the end of the turn if either of its conditions are met (destroying one or more enemy CHARACTER units, or destroying all of your opponent’s CHARACTER units from their Army Roster). Resurrected CHARACTER models still count toward this mission.  

[Rule Citation] **ASSASSINATION** (Secondary Mission deck [1]) → "If you are using Tactical Missions, then at the end of the turn, if either of the conditions below are satisfied, this Secondary Mission is achieved and you score 5VP... Note that if you are using Tactical Missions, this Secondary Mission is achieved even if such a unit was destroyed and then subsequently resurrected for any reason."  

[Reasoning] The mission explicitly states that resurrection does not invalidate the VP gain. For Tactical Missions, the mission is achieved if the conditions are met during the turn, regardless of subsequent resurrection. The 5VP is awarded once per turn if the mission is achieved.

---

## [12] LEVIATHAN · mp=ON · 2.5s

`billed: prompt=2067 completion=1058 total=3125 · finish=stop` · ctx 1951 tok

**Q:** Under Bring It Down with Tactical Missions, how many VP for destroying a 20-wound Monster, and what is the maximum I can score from it?

<details><summary>reasoning trace (2955 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about the Bring It Down secondary mission under Tactical Missions, specifically how many VP they get for destroying a 20-wound monster and the maximum they can score from it.

First, I need to look at the Bring It Down rules. From the provided context, Bring It Down says that each time an enemy MONSTER or VEHICLE is destroyed, you score 2VP plus extra 1VP for each condition met. The conditions are based on the Wounds characteristic: 10+, 15+, and 20+. So for a 20-wound model, all three conditions are met. That would be 2VP base plus 3 extra VP (1 for each condition), totaling 5VP per destruction.

But wait, the user mentioned using Tactical Missions. The note says that if you score any VP from this mission during a turn, the mission is achieved at the end of the turn. Also, under Tactical Missions, you can't score more than 8VP total from this mission. However, each instance of destroying a model gives 5VP. But the maximum total is capped at 8VP. So if you destroy one model, you get 5VP. If you destroy another, you'd add another 5VP, but the total can't exceed 8. Therefore, the maximum you can get from this mission is 8VP, even if you destroy multiple models. But the question is about destroying a single 20-wound monster. So that one destruction gives 5VP, and since 5 is less than 8, that's the amount scored. The maximum possible from this mission is 8VP, but you can only achieve that by destroying two models (5 + 5 would be 10, but capped at 8). Wait, no—if you destroy one model, you get 5VP. If you destroy another, you add another 5VP, but the total is capped at 8VP. So the first destruction gives 5VP, and the second would add 3VP to reach 8. But the rules state that if you score any VP during a turn, the mission is achieved. Once achieved, you can't score more from it. Wait, no—the mission is achieved when you score any VP during a turn. So once you score VP in a turn, the mission is achieved at the end of that turn. But under Tactical Missions, you can't score more than 8VP total from this mission. So if you destroy one model for 5VP, that's part of the 8VP cap. If you destroy another model in the same turn, you can only add up to 8VP total. But the mission is achieved once you score any VP in a turn, so after the first destruction, the mission is achieved, and you can't score more VP from it in that turn. However, if you destroy another model in a different turn, you can score again. But the total across all turns is capped at 8VP. So the maximum you can get from this mission is 8VP. For a single 20-wound monster, it's 5VP. The maximum possible from this mission is 8VP, which could be achieved by destroying one model (5VP) and then another (adding 3VP to reach 8). But the user is asking specifically about destroying a 20-wound monster. So the answer is 5VP for that destruction, and the maximum possible from the mission is 8VP.
</think>

[Ruling] Destroying a 20-wound MONSTER under **Bring It Down** with Tactical Missions scores **5VP** (2VP base + 1VP for 10+ Wounds + 1VP for 15+ Wounds + 1VP for 20+ Wounds). The **maximum total VP** you can score from this mission is **8VP** (capped by the "maximum of 8VP" rule for Tactical Missions).  

[Rule Citation] **Bring It Down** (Secondary Mission deck [1]) → "each time an enemy MONSTER or VEHICLE model is destroyed, you score 2VP and an extra 1VP for each of the conditions [...] The destroyed model had a Wounds characteristic of 10+/15+/20+." **Determine Victor** ([4]) → "a maximum of 40VP from Secondary Missions [...] if you are using Tactical Missions, you cannot score more than 8VP in total from this Secondary Mission."  

[Reasoning] The 20-wound model satisfies all three Wounds thresholds (10+, 15+, 20+), adding 3VP to the base 2VP. However, Tactical Missions limit this mission’s total VP to 8VP. Destroying one such model gives 5VP, and no further VP can be added beyond 8VP (e.g., destroying a second model would only add 3VP to reach the cap).
```

</details>

**A:** [Ruling] Destroying a 20-wound MONSTER under **Bring It Down** with Tactical Missions scores **5VP** (2VP base + 1VP for 10+ Wounds + 1VP for 15+ Wounds + 1VP for 20+ Wounds). The **maximum total VP** you can score from this mission is **8VP** (capped by the "maximum of 8VP" rule for Tactical Missions).  

[Rule Citation] **Bring It Down** (Secondary Mission deck [1]) → "each time an enemy MONSTER or VEHICLE model is destroyed, you score 2VP and an extra 1VP for each of the conditions [...] The destroyed model had a Wounds characteristic of 10+/15+/20+." **Determine Victor** ([4]) → "a maximum of 40VP from Secondary Missions [...] if you are using Tactical Missions, you cannot score more than 8VP in total from this Secondary Mission."  

[Reasoning] The 20-wound model satisfies all three Wounds thresholds (10+, 15+, 20+), adding 3VP to the base 2VP. However, Tactical Missions limit this mission’s total VP to 8VP. Destroying one such model gives 5VP, and no further VP can be added beyond 8VP (e.g., destroying a second model would only add 3VP to reach the cap).

---

## [13] LEVIATHAN · mp=ON · 1.9s

`billed: prompt=2269 completion=654 total=2923 · finish=stop` · ctx 2210 tok

**Q:** On the Take and Hold primary mission, how does VP scoring work in the second to fourth battle rounds versus the fifth battle round?

<details><summary>reasoning trace (1836 chars, billed)</summary>

```
<think>
Okay, let's tackle this question about the Take and Hold primary mission. The user wants to know how VP scoring works in the second to fourth battle rounds compared to the fifth. 

First, I need to look at the provided rules for Take and Hold. From the context given, the mission says that in the second, third, and fourth battle rounds, at the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control, up to 15VP per turn. 

Then, in the fifth battle round, the rules change slightly. The player who has the first turn scores VP as described above. The player with the second turn also scores VP but does so at the end of their turn instead of at the end of their Command phase. 

So the key differences are the timing of VP scoring in the fifth round. For the first player in the fifth round, it's still at the end of their Command phase, but the second player does it at the end of their turn. The VP amount per objective marker remains 5VP, same as before. The maximum per turn is still 15VP, which would be if they control 3 objective markers (assuming there are three), since 3x5=15.

I need to make sure there's no other rule in the context that affects this. The other missions don't seem relevant here. The answer should clearly state the VP scoring for each battle round, highlighting the difference in timing for the fifth round. Also, mention the maximum VP per turn. 

I should structure the answer with the ruling first, then cite the rule, and explain the reasoning. Since the user provided the exact text, I can reference the Take and Hold mission directly. Make sure to note that in the fifth round, the second player's VP is scored at the end of their turn instead of the Command phase. That's the main distinction between the fourth and fifth rounds.
</think>

[Ruling] In the **second, third, and fourth battle rounds**, the player whose turn it is scores **5VP per controlled objective marker** at the end of their Command phase (up to 15VP per turn). In the **fifth battle round**, the **first-turn player** scores VP as above at the end of their Command phase, while the **second-turn player** scores VP at the end of their **turn** instead of the Command phase.  

[Rule Citation] *Take and Hold (Primary Mission)* → "In the second, third and fourth battle rounds: At the end of each Command phase... scores 5VP for each objective marker they control (up to 15VP per turn). In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase."  

[Reasoning] The mission explicitly differentiates between the timing of VP scoring in the fifth battle round for the second-turn player, shifting it from the Command phase to the end of their full turn. All other VP values and conditions remain unchanged.
```

</details>

**A:** [Ruling] In the **second, third, and fourth battle rounds**, the player whose turn it is scores **5VP per controlled objective marker** at the end of their Command phase (up to 15VP per turn). In the **fifth battle round**, the **first-turn player** scores VP as above at the end of their Command phase, while the **second-turn player** scores VP at the end of their **turn** instead of the Command phase.  

[Rule Citation] *Take and Hold (Primary Mission)* → "In the second, third and fourth battle rounds: At the end of each Command phase... scores 5VP for each objective marker they control (up to 15VP per turn). In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase."  

[Reasoning] The mission explicitly differentiates between the timing of VP scoring in the fifth battle round for the second-turn player, shifting it from the Command phase to the end of their full turn. All other VP values and conditions remain unchanged.

---

## [14] LEVIATHAN · mp=ON · 3.4s

`billed: prompt=1940 completion=874 total=2814 · finish=stop` · ctx 1868 tok

**Q:** How are the attacker and defender determined in a Leviathan mission, and how does that affect deployment and the first turn?

<details><summary>reasoning trace (3354 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking how the attacker and defender are determined in a Leviathan mission and how that affects deployment and the first turn. 

First, I need to look at the provided rules context. Let me start by checking the "Determine Attacker and Defender" section (Rule 1). It says that players consult the Deployment card drawn for the mission to agree on which battlefield edge is the Attacker's and Defender's. Then they roll off, and the winner decides who is the Attacker and who is the Defender. This determines which deployment zone each uses.

Next, for deployment, Rule 4 "Deploy Armies" states that players alternate setting up their remaining units, starting with the Defender. The Defender goes first in deploying their units, followed by the Attacker. Each player's models must be within their respective deployment zones.

Now, regarding the first turn. The question also asks how the attacker and defender affect the first turn. Looking at Rule 5 "Redeployments" under Core Rules, it mentions that redeployments are resolved after the Deploy Armies step and before the Determine First Turn step. However, the user's question is about how the attacker/defender status affects the first turn. The Core Rules mention that after deployment and redeployments, the Determine First Turn step occurs. But in the provided Leviathan rules, there's no specific mention of how attacker/defender status affects who gets the first turn. The Core Rules might have a standard roll-off for first turn unless specified otherwise. However, in the provided context, Rule 6 "Resolve Pre-battle Rules" says players alternate resolving pre-battle rules starting with the player who takes the first turn. But the determination of who has the first turn isn't covered in the given Leviathan rules. 

Wait, the user's question is about how the attacker/defender status affects the first turn. The answer might be that the first turn is determined by a roll-off, as per standard 10th edition rules, unless modified by a mission rule. However, in the provided context, there's no Leviathan rule that changes this. The Core Rules mention that after deployment, redeployments, and pre-battle rules, the Determine First Turn step is handled. Since the provided Leviathan rules don't specify a change here, the standard Core Rule applies: players roll off, and the winner takes the first turn. However, the user's question is whether the attacker/defender status directly affects the first turn. The answer is no, unless a specific rule says so. The provided rules don't indicate that the attacker/defender status affects the first turn determination. The first turn is determined separately via a roll-off. 

So, putting it all together: The attacker and defender are determined by the Deployment card and a roll-off, which sets their deployment zones. Deployment starts with the Defender. The first turn is determined by a separate roll-off, not directly by being attacker or defender. The provided rules don't link attacker/defender status to the first turn. Therefore, the answer should state that the attacker and defender are determined as per Rule 1, deployment order is Defender first (Rule 4), and the first turn is determined by a roll-off as per Core Rules, not specified in the provided Leviathan context.
</think>

[Ruling] The Attacker and Defender are determined by rolling off after consulting the Deployment card, with the winner choosing roles. Deployment starts with the Defender placing units first, and the first turn is determined separately via a roll-off (not directly tied to attacker/defender status).  

[Rule Citations]  
- Determine Attacker and Defender (Leviathan) → [1]  
- Deploy Armies (Leviathan) → [4]  
- Core Rules: Determine First Turn (implied by Core Rules structure, not explicitly in provided Leviathan context).  

[Reasoning]  
The Deployment card defines battlefield edges, and the roll-off winner assigns roles ([1]). Deployment proceeds with the Defender first ([4]). The first turn is determined by a separate roll-off per Core Rules (not detailed in provided Leviathan text), as Leviathan rules do not link attacker/defender status to turn order.
```

</details>

**A:** [Ruling] The Attacker and Defender are determined by rolling off after consulting the Deployment card, with the winner choosing roles. Deployment starts with the Defender placing units first, and the first turn is determined separately via a roll-off (not directly tied to attacker/defender status).  

[Rule Citations]  
- Determine Attacker and Defender (Leviathan) → [1]  
- Deploy Armies (Leviathan) → [4]  
- Core Rules: Determine First Turn (implied by Core Rules structure, not explicitly in provided Leviathan context).  

[Reasoning]  
The Deployment card defines battlefield edges, and the roll-off winner assigns roles ([1]). Deployment proceeds with the Defender first ([4]). The first turn is determined by a separate roll-off per Core Rules (not detailed in provided Leviathan text), as Leviathan rules do not link attacker/defender status to turn order.

---

## [15] LEVIATHAN · mp=ON · 2.1s

`billed: prompt=2090 completion=612 total=2702 · finish=stop` · ctx 1983 tok

**Q:** What is the Scorched Earth primary mission and how does burning an objective marker score VP at the end of the battle?

<details><summary>reasoning trace (1892 chars, billed)</summary>

```
<think>
Okay, let's tackle this question about the Scorched Earth primary mission. The user wants to know what the mission is and how burning an objective marker scores VP at the end of the battle.

First, I need to look at the provided rules context. The user mentioned [1] as the Scorched Earth mission. Let me check that entry. 

Looking at [1], the description says that starting from the second battle round, in each player's Shooting phase, they can select a unit to shoot, but that unit can't shoot or charge until the end of the turn. Then, if that unit is within 1" of an objective marker controlled by the player whose turn it is, the marker is burned and removed. 

Then, in the second, third, and fourth battle rounds, at the end of each Command phase, the player scores 5VP per controlled objective marker, up to 10VP per turn. In the fifth round, the first player scores as before, and the second does so at the end of their turn. 

The end of the battle VP: Each player scores 5VP if any No Man's Land markers were burned by their units, and 10VP if the opponent's deployment zone marker was burned. 

So the user is asking specifically about how burning an objective marker scores VP at the end of the battle. The answer should focus on the end-of-battle VP from burning markers. The key part is the last paragraph under [1], which details the 5VP and 10VP for burning markers in specific locations. 

I need to make sure I'm not mixing in other VP scoring from the same mission. The question is about the end-of-battle VP from burning, not the VP scored during the battle rounds. 

So the ruling is that burning an objective marker gives 5VP if it's in No Man's Land and 10VP if it's in the opponent's deployment zone. The rule citation is from [1] under Scorched Earth. The reasoning is that the end-of-battle VP is based on where the burned markers were located.
</think>

[Ruling] The **Scorched Earth** Primary Mission allows players to burn objective markers by having a unit within 1" of them during their next Command phase. At the end of the battle, players score **5VP for each objective marker in No Man's Land burned by their units** and **10VP if the objective marker in their opponent's deployment zone was burned**.  

[Rule Citation] This is detailed in the **Scorched Earth** Primary Mission description (Rule [1]).  

[Reasoning] The mission explicitly states that burning objective markers (removing them by meeting the conditions) grants VP based on their location at the end of the battle. The 5VP/10VP rewards are tied to markers burned in No Man's Land vs. the opponent's deployment zone, as outlined in the final paragraph of the rule.
```

</details>

**A:** [Ruling] The **Scorched Earth** Primary Mission allows players to burn objective markers by having a unit within 1" of them during their next Command phase. At the end of the battle, players score **5VP for each objective marker in No Man's Land burned by their units** and **10VP if the objective marker in their opponent's deployment zone was burned**.  

[Rule Citation] This is detailed in the **Scorched Earth** Primary Mission description (Rule [1]).  

[Reasoning] The mission explicitly states that burning objective markers (removing them by meeting the conditions) grants VP based on their location at the end of the battle. The 5VP/10VP rewards are tied to markers burned in No Man's Land vs. the opponent's deployment zone, as outlined in the final paragraph of the rule.

---

## [16] LEVIATHAN · mp=ON · 2.2s

`billed: prompt=2026 completion=877 total=2903 · finish=stop` · ctx 1872 tok

**Q:** In Leviathan, how do ruins affect movement and visibility, and can a unit end its move inside a ruin's walls?

<details><summary>reasoning trace (1907 chars, billed)</summary>

```
<think>
Okay, let's tackle this question about how ruins affect movement and visibility in Leviathan, and whether a unit can end its move inside a ruin's walls. 

First, I need to look at the provided rules context. The user mentioned Leviathan, so I should check both the Leviathan-specific rules and the Core Rules since Leviathan might override some Core Rules.

Looking at the Core Rules entry for Ruins (Rule 3), there's a section on Movement. It says that INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models can move through Ruins as if they weren't there. But they can't end a move within a wall, floor, etc. Then, other models (like non-INFANTRY) can only be on the ground floor. So movement through Ruins depends on the model type.

For visibility, the Core Rules state that models can't see over or through Ruins except for AIRCRAFT. So line of sight is blocked by Ruins unless you're an aircraft. Also, models inside Ruins can see out normally, and vice versa.

Now, the Leviathan rules don't have a specific entry about Ruins beyond the general Use of Ruins (Rule 1), which mentions they block line of sight and provide cover. But since the Core Rules are the base, and Leviathan doesn't override the Ruins mechanics here, the Core Rules apply.

The question also asks if a unit can end its move inside a ruin's walls. According to Core Rule 3 (Ruins), under MOVEMENT, it says a model cannot end a move within a wall, floor, etc. So even if a model can move through Ruins, they can't end their move inside the walls. They can be on a floor level, but not inside the structure itself.

So putting it all together: Movement through Ruins is allowed for certain models, visibility is blocked except for aircraft, and units can't end their move inside walls but can be on floors. The answer should reference the Core Rules for Ruins and note that Leviathan doesn't change this.
</think>

[Ruling]  
In Warhammer 40,000 Leviathan, **Ruins affect movement and visibility as per Core Rules**, with no Leviathan-specific overrides provided in the context.  

- **Movement**:  
  - INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models can move through Ruins (walls, floors, ceilings, etc.) as if they are not there. However, **no model may end a move within a wall, floor, or structural element** of the Ruins.  
  - INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, BEASTS, and FLY models can be set up or end a move on any floor level of the Ruins (if their base does not overhang the floor). All other models are restricted to the ground floor.  

- **Visibility**:  
  - Models **cannot see over or through Ruins** (e.g., a unit outside cannot target a unit on the other side of the Ruins, even through open windows/doors).  
  - AIRCRAFT models are exceptions and can see through Ruins normally.  
  - Models **within Ruins can see out** normally, and vice versa.  

- **Ending a Move Inside Ruins**:  
  - A unit **cannot end its move inside a Ruin’s walls, floors, or structural elements**. Models may only occupy floor levels (as per the MOVEMENT section of the Core Rules).  

**Rule Citations**:  
- Movement and visibility rules are defined in **Core Rules → Ruins** (Rule 3).  
- Leviathan’s **Use of Ruins** (Rule 1) confirms Ruins are used for line-of-sight and cover but does not alter Core Rules mechanics.  

**Reasoning**:  
The Core Rules explicitly state movement and visibility rules for Ruins, and no Leviathan rule in the provided context contradicts or modifies these. The restriction on ending a move within structural elements (walls, floors) is non-negotiable per the Core Rules.
```

</details>

**A:** [Ruling]  
In Warhammer 40,000 Leviathan, **Ruins affect movement and visibility as per Core Rules**, with no Leviathan-specific overrides provided in the context.  

- **Movement**:  
  - INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models can move through Ruins (walls, floors, ceilings, etc.) as if they are not there. However, **no model may end a move within a wall, floor, or structural element** of the Ruins.  
  - INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, BEASTS, and FLY models can be set up or end a move on any floor level of the Ruins (if their base does not overhang the floor). All other models are restricted to the ground floor.  

- **Visibility**:  
  - Models **cannot see over or through Ruins** (e.g., a unit outside cannot target a unit on the other side of the Ruins, even through open windows/doors).  
  - AIRCRAFT models are exceptions and can see through Ruins normally.  
  - Models **within Ruins can see out** normally, and vice versa.  

- **Ending a Move Inside Ruins**:  
  - A unit **cannot end its move inside a Ruin’s walls, floors, or structural elements**. Models may only occupy floor levels (as per the MOVEMENT section of the Core Rules).  

**Rule Citations**:  
- Movement and visibility rules are defined in **Core Rules → Ruins** (Rule 3).  
- Leviathan’s **Use of Ruins** (Rule 1) confirms Ruins are used for line-of-sight and cover but does not alter Core Rules mechanics.  

**Reasoning**:  
The Core Rules explicitly state movement and visibility rules for Ruins, and no Leviathan rule in the provided context contradicts or modifies these. The restriction on ending a move within structural elements (walls, floors) is non-negotiable per the Core Rules.

---

## [17] LEVIATHAN · mp=ON · 2.5s

`billed: prompt=2160 completion=896 total=3056 · finish=stop` · ctx 2158 tok

**Q:** When are objective markers placed in a Leviathan mission, and how is control of an objective determined?

<details><summary>reasoning trace (2795 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking when objective markers are placed in a Leviathan mission and how control is determined. 

First, I need to look at the provided rules. From the context, there are several entries about objective markers. Let's start with placement. 

Looking at rule [1], it says that in Leviathan, players set up objective markers based on the Deployment card's map. Each Deployment card specifies the number and placement. Also, the Designer's Note mentions that in Leviathan, objective markers are treated as flat markers that don't impede movement, unlike the Core Rules where models can't end their move on them. 

Rule [5] talks about the "Chosen Battlefield" mission rule. Here, instead of using the Deployment card's setup, players roll off and alternate placing markers. Specific placement rules include being in deployment zones and No Man's Land, with distances from edges and other markers. This seems to override the standard Deployment card setup for this mission.

Now, for control determination. Rule [4] from Core Rules states that control is based on the sum of Objective Control (OC) characteristics of models within range (3" horizontally, 5" vertically). The player with the higher total controls the marker. If tied, it's contested. However, Leviathan's rule [1] mentions that in their missions, models can end any type of move on top of an objective marker. But does that affect control? The Core Rules still define control via OC, unless Leviathan changes that. 

Looking at the Leviathan rules provided, there's no mention of changing how control is determined. Rule [3] "Sweep and Clear" affects control by allowing a player to keep control even if models are out of range after their Command phase. But that's a specific mission rule. The general rule would still be the Core Rules unless Leviathan states otherwise. 

So, combining these, in a standard Leviathan mission, objective markers are placed as per the Deployment card's instructions (rule [1]), unless a mission rule like "Chosen Battlefield" (rule [5]) changes the setup. Control is determined by OC values as per Core Rules (rule [4]), unless a mission rule like "Sweep and Clear" modifies it. 

Wait, but the user is asking about Leviathan missions in general. The answer should mention that placement depends on the specific mission's rules. For example, some missions might use Deployment cards, others might use different rules. But the default is rule [1], and mission-specific rules can alter that. 

For control, unless a mission rule changes it (like "Sweep and Clear"), the Core Rules apply. So the answer should state that control is determined by OC values and range, as per Core Rules, unless a Leviathan mission rule specifies otherwise.
</think>

[Ruling] Objective markers in a Leviathan mission are placed according to the specific Deployment card’s instructions (e.g., number and location) during the **Place Objective Markers step**. Control of objective markers is determined by **Objective Control (OC) values** of models within range (3" horizontally, 5" vertically), as per Core Rules, unless modified by a mission rule (e.g., *Sweep and Clear*).  

[Rule Citation]  
- Placement: **Leviathan** → *Place Objective Markers* (Wahapedia_Leviathan [1]) → "Players now set up objective markers on the battlefield. Each Deployment card's deployment map will show players how many objective markers to set up and where each should be placed."  
- Control: **Core Rules** → *Objective Markers* (Wahapedia_Core_Rules [4]) → "To determine a player's Level of Control over it, add together the OC characteristics of all the models from that player's army that are within range of that objective marker."  

[Reasoning]  
Leviathan missions retain the Core Rules’ OC-based control system unless a mission rule (e.g., *Sweep and Clear* [3]) alters it. Placement is mission-dependent (e.g., standard Deployment cards [1] or mission-specific rules like *Chosen Battlefield* [5]). The Leviathan rule allowing models to end moves on objective markers ([1]) does not affect control mechanics, which remain tied to OC values and range.
```

</details>

**A:** [Ruling] Objective markers in a Leviathan mission are placed according to the specific Deployment card’s instructions (e.g., number and location) during the **Place Objective Markers step**. Control of objective markers is determined by **Objective Control (OC) values** of models within range (3" horizontally, 5" vertically), as per Core Rules, unless modified by a mission rule (e.g., *Sweep and Clear*).  

[Rule Citation]  
- Placement: **Leviathan** → *Place Objective Markers* (Wahapedia_Leviathan [1]) → "Players now set up objective markers on the battlefield. Each Deployment card's deployment map will show players how many objective markers to set up and where each should be placed."  
- Control: **Core Rules** → *Objective Markers* (Wahapedia_Core_Rules [4]) → "To determine a player's Level of Control over it, add together the OC characteristics of all the models from that player's army that are within range of that objective marker."  

[Reasoning]  
Leviathan missions retain the Core Rules’ OC-based control system unless a mission rule (e.g., *Sweep and Clear* [3]) alters it. Placement is mission-dependent (e.g., standard Deployment cards [1] or mission-specific rules like *Chosen Battlefield* [5]). The Leviathan rule allowing models to end moves on objective markers ([1]) does not affect control mechanics, which remain tied to OC values and range.

---

## [18] LEVIATHAN · mp=ON · 1.8s

`billed: prompt=2042 completion=667 total=2709 · finish=stop` · ctx 1927 tok

**Q:** What does the Engage on All Fronts secondary require across table quarters, and how do Battle-shocked units affect whether it is achieved?

<details><summary>reasoning trace (2018 chars, billed)</summary>

```
<think>
Okay, let's tackle this question about the "Engage on All Fronts" secondary mission. The user wants to know two things: what the mission requires across table quarters and how Battle-shocked units affect its achievement.

First, I need to look at the provided rules for "Engage on All Fronts." From the context given, the mission states that at the end of your turn, if you have one or more qualifying units from your army wholly within three or more different table quarters, and those units are all more than 3" away from any other table quarter, then the mission is achieved. The VP is 4 if in four quarters, 2 if in three. Also, Battle-shocked units are not qualifying units. 

So, the requirements are: units must be in different table quarters (at least three), each unit must be wholly within a quarter, and each must be more than 3" from any other quarter. Wait, the phrasing says "more than 3" away from any other table quarter." So each unit has to be in a separate quarter and not too close to the edges of the table that separate quarters. 

Now, Battle-shocked units are explicitly excluded as qualifying. So if a unit is Battle-shocked, it doesn't count towards meeting the requirement. The user is asking how Battle-shocked units affect the mission. The answer is that they can't be used to fulfill the requirement because they're not qualifying units. 

I need to check if there's any other rule that might affect this. The Battle-shock rules (rule 3) mention that Battle-shocked units have their Objective Control at 0 and can't be affected by Stratagems, but that's probably not relevant here. The key part is that Battle-shocked units aren't qualifying for this mission. 

So putting it all together: the mission requires units in three or four different table quarters, each more than 3" from other quarters. Battle-shocked units can't be used. The answer should reference the specific rule in the mission description and the part about Battle-shocked units not being qualifying.
</think>

[Ruling] The **Engage on All Fronts** Secondary Mission requires one or more qualifying units from your army to be **wholly within three or more different table quarters**, with each unit **more than 3" away from any other table quarter**. Battle-shocked units are explicitly **not qualifying units** for this mission.  

[Rule Citation]  
- **Engage on All Fronts** (Secondary Mission deck [1]) → "At the end of your turn, if you have one or more qualifying units [...] wholly within three or more different table quarters [...] and those units are all more than 3" away from any other table quarter, this Secondary Mission is achieved."  
- **Engage on All Fronts** (Secondary Mission deck [1]) → "While a unit is Battle-shocked, it is not a qualifying unit."  

[Reasoning]  
The mission’s success hinges on units meeting two spatial conditions: occupying distinct table quarters and maintaining distance from other quarters. Battle-shocked units are excluded entirely from consideration as "qualifying units," meaning they cannot contribute to fulfilling the mission’s requirements.
```

</details>

**A:** [Ruling] The **Engage on All Fronts** Secondary Mission requires one or more qualifying units from your army to be **wholly within three or more different table quarters**, with each unit **more than 3" away from any other table quarter**. Battle-shocked units are explicitly **not qualifying units** for this mission.  

[Rule Citation]  
- **Engage on All Fronts** (Secondary Mission deck [1]) → "At the end of your turn, if you have one or more qualifying units [...] wholly within three or more different table quarters [...] and those units are all more than 3" away from any other table quarter, this Secondary Mission is achieved."  
- **Engage on All Fronts** (Secondary Mission deck [1]) → "While a unit is Battle-shocked, it is not a qualifying unit."  

[Reasoning]  
The mission’s success hinges on units meeting two spatial conditions: occupying distinct table quarters and maintaining distance from other quarters. Battle-shocked units are excluded entirely from consideration as "qualifying units," meaning they cannot contribute to fulfilling the mission’s requirements.

---

## [19] LEVIATHAN · mp=ON · 1.3s

`billed: prompt=1952 completion=399 total=2351 · finish=stop` · ctx 1814 tok

**Q:** In the Secure No Man's Land secondary, how many VP do I score for controlling one versus two objective markers in No Man's Land?

<details><summary>reasoning trace (1235 chars, billed)</summary>

```
<think>
Okay, let's see. The user is asking about the Secure No Man's Land secondary mission and how many VP they score for controlling one versus two objective markers in No Man's Land.

First, I need to look at the provided rules context for that specific mission. The user provided [1] which is the Secure No Man's Land Secondary Mission. Let me check that again.

The description says: At the end of your turn, if you control two or more objective markers in No Man's Land, this Secondary Mission is achieved and you score 5VP. If, at the end of your turn, you only control one objective marker in No Man's Land, this Secondary Mission is still achieved, but you score 2VP instead of 5VP.

So, the answer is straightforward. Controlling two or more gives 5VP, and controlling one gives 2VP. The key points here are the conditions for achieving the mission and the VP differences based on the number of markers controlled. I need to make sure there's no other rule in the context that might affect this, but since the question is specifically about Secure No Man's Land, and the other missions don't interfere with this one, the answer is clear. The user just needs to know the VP for each scenario as stated in the rule.
</think>

[Ruling]  
- Controlling **two or more** objective markers in No Man's Land at the end of your turn scores **5VP**.  
- Controlling **one** objective marker in No Man's Land at the end of your turn scores **2VP**.  

[Rule Citation]  
**Secure No Man's Land (Secondary Mission)** → [1]  

[Reasoning]  
The mission explicitly states the VP rewards based on the number of objective markers controlled. Controlling two or more grants 5VP, while controlling one grants 2VP. No other rules in the provided context modify this outcome.
```

</details>

**A:** [Ruling]  
- Controlling **two or more** objective markers in No Man's Land at the end of your turn scores **5VP**.  
- Controlling **one** objective marker in No Man's Land at the end of your turn scores **2VP**.  

[Rule Citation]  
**Secure No Man's Land (Secondary Mission)** → [1]  

[Reasoning]  
The mission explicitly states the VP rewards based on the number of objective markers controlled. Controlling two or more grants 5VP, while controlling one grants 2VP. No other rules in the provided context modify this outcome.

---

## [20] LEVIATHAN · mp=ON · 1.5s

`billed: prompt=1654 completion=543 total=2197 · finish=stop` · ctx 1539 tok

**Q:** How do Gambits work in a Leviathan game and when can I use one?

<details><summary>reasoning trace (1396 chars, billed)</summary>

```
<think>
Okay, let's tackle this question about Gambits in Leviathan. The user wants to know how they work and when they can be used.

First, I need to look through the provided rules context. Let me check each entry. 

Looking at [1] Begin the Battle, it mentions that at the end of each player's turn, if using Tactical Missions, they can discard Secondary Mission cards and gain CP. Also, at the end of the third battle round, players generate Gambits. So Gambits are generated after the third round.

Next, [3] Determine Attacker and Defender mentions that Secondary Mission and Gambit decks are set aside and later used. [5] Determine Victor says players can score VP from Gambits, with a max of 50VP from Primary Missions and/or Gambits. But the actual use of Gambits isn't detailed here.

The user is asking when to use Gambits. The rules in the context don't explicitly explain how Gambits are used beyond generating them at the end of the third round. The context doesn't provide details on activation, effects, or timing beyond their generation. 

Since the provided rules don't have specific information on using Gambits beyond their generation, I can't infer more. The answer should state that Gambits are generated at the end of the third round and that their use isn't detailed here. The user might need to refer to other sources or the full Leviathan rules for specifics.
</think>

The provided rules do not clearly address how Gambits function beyond their generation. Specifically:  
- **Gambits are generated at the end of the third battle round** ([1] Begin the Battle).  
- Players receive Gambit decks during setup ([3] Determine Attacker and Defender), and Gambits contribute to VP scoring (capped at 50VP total with Primary Missions) ([5] Determine Victor).  

However, **no explicit rules are provided in the context about how Gambits are used, activated, or resolved during the game**. For details on Gambit mechanics (e.g., when they can be played, their effects, or how they interact with other rules), you would need to consult the full Leviathan rules or the Leviathan Tournament Companion.  

**Ruling**: Gambits are generated at the end of the third battle round and contribute to VP, but their exact use is not detailed in the provided rules.  
**Rule Citation**: [1] Begin the Battle, [3] Determine Attacker and Defender, [5] Determine Victor.  
**Reasoning**: The context only mentions Gambit generation and VP contribution, not their gameplay mechanics.
```

</details>

**A:** The provided rules do not clearly address how Gambits function beyond their generation. Specifically:  
- **Gambits are generated at the end of the third battle round** ([1] Begin the Battle).  
- Players receive Gambit decks during setup ([3] Determine Attacker and Defender), and Gambits contribute to VP scoring (capped at 50VP total with Primary Missions) ([5] Determine Victor).  

However, **no explicit rules are provided in the context about how Gambits are used, activated, or resolved during the game**. For details on Gambit mechanics (e.g., when they can be played, their effects, or how they interact with other rules), you would need to consult the full Leviathan rules or the Leviathan Tournament Companion.  

**Ruling**: Gambits are generated at the end of the third battle round and contribute to VP, but their exact use is not detailed in the provided rules.  
**Rule Citation**: [1] Begin the Battle, [3] Determine Attacker and Defender, [5] Determine Victor.  
**Reasoning**: The context only mentions Gambit generation and VP contribution, not their gameplay mechanics.

---

## [21] UNITS · mp=OFF · 2.7s

`billed: prompt=3138 completion=905 total=4043 · finish=stop` · ctx 2795 tok

**Q:** When Abaddon the Despoiler fights the Aberrants in melee, how do Abaddon's Devastating Wounds interact with the Aberrants' Feel No Pain?

<details><summary>reasoning trace (2687 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking how Abaddon's Devastating Wounds interact with the Aberrants' Feel No Pain when they fight in melee.

First, I need to recall the rules for both abilities. From the provided context:

Abaddon's weapon, Drach’nyen, has the Devastating Wounds ability. The rule for Devastating Wounds isn't explicitly listed here, but based on standard Warhammer 40k rules, Devastating Wounds typically mean that if the wound roll is a 6, the target doesn't get a save. However, since the user provided context might have specific details, I need to check if there's any mention of Devastating Wounds in the given data.

Looking at the provided data for Abaddon's weapons, the Drach’nyen has "devastating wounds" noted, but there's no specific rule text here. The core rules for Devastating Wounds would apply unless there's an errata or specific rule in the context. Since there's no additional info here, I'll assume the standard rule applies: a wound roll of 6 bypasses the target's save.

Now, the Aberrants have Feel No Pain 5+. The rule for Feel No Pain is in the Core Abilities section of the Aberrants' entry. It states that each time they would lose a wound, roll a D6; if it's equal to or exceeds 5, the wound is ignored.

The interaction here is between Devastating Wounds (which removes the save) and Feel No Pain (which affects wound loss). The key is the order of resolution. Normally, when an attack is resolved, you determine if it wounds, then the target applies saves, and then any Feel No Pain. However, Devastating Wounds would negate the save if the wound roll is a 6. So, if the wound is a 6, the Aberrants can't use their save, but they can still use Feel No Pain on the resulting wound.

Wait, but the question is about how they interact. Let me break it down step by step:

1. Attack is made against Aberrants.
2. Wound roll is made. If it's a 6, Devastating Wounds apply, so no save can be taken.
3. If the wound is successful (after any saves, or bypassing saves via Devastating Wounds), then Feel No Pain is applied. The Aberrants roll a D6; on a 5 or 6, they ignore the wound.

So, Devastating Wounds don't affect the Feel No Pain ability itself. Feel No Pain is applied after the wound is determined, regardless of whether a save was possible or not. Therefore, even if the wound is a 6 and bypasses the save, the Aberrants can still use Feel No Pain to potentially ignore the wound.

Therefore, the ruling is that Devastating Wounds remove the save, but Feel No Pain is still applied to the resulting wounds. The answer should reference the relevant rules for both abilities as per the provided context.
</think>

[Ruling] When Abaddon the Despoiler’s weapon with **Devastating Wounds** scores a wound roll of 6, the Aberrants cannot take a save. However, the Aberrants can still use their **Feel No Pain 5+** ability to potentially ignore the wound after the save is bypassed.  

[Rule Citations]  
- **Devastating Wounds**: Implied by the weapon’s stated ability (Drach’nyen, Abaddon’s datasheet). Standard rule: A wound roll of 6 bypasses the target’s save.  
- **Feel No Pain 5+**: Explicitly detailed in the Aberrants’ Core Abilities (unnamed rule under their entry).  

[Reasoning]  
1. **Devastating Wounds** remove the target’s save only if the wound roll is a 6.  
2. **Feel No Pain** applies after the wound is determined (post-save or post-bypass). The Aberrants roll a D6 for each wound they would lose; on a 5+, the wound is ignored.  
3. These abilities operate sequentially: Devastating Wounds negate the save, but Feel No Pain remains unaffected and resolves afterward.
```

</details>

**A:** [Ruling] When Abaddon the Despoiler’s weapon with **Devastating Wounds** scores a wound roll of 6, the Aberrants cannot take a save. However, the Aberrants can still use their **Feel No Pain 5+** ability to potentially ignore the wound after the save is bypassed.  

[Rule Citations]  
- **Devastating Wounds**: Implied by the weapon’s stated ability (Drach’nyen, Abaddon’s datasheet). Standard rule: A wound roll of 6 bypasses the target’s save.  
- **Feel No Pain 5+**: Explicitly detailed in the Aberrants’ Core Abilities (unnamed rule under their entry).  

[Reasoning]  
1. **Devastating Wounds** remove the target’s save only if the wound roll is a 6.  
2. **Feel No Pain** applies after the wound is determined (post-save or post-bypass). The Aberrants roll a D6 for each wound they would lose; on a 5+, the wound is ignored.  
3. These abilities operate sequentially: Devastating Wounds negate the save, but Feel No Pain remains unaffected and resolves afterward.

---

## [22] UNITS · mp=OFF · 2.4s

`billed: prompt=3078 completion=801 total=3879 · finish=stop` · ctx 2764 tok

**Q:** When An'ggrath the Unbound is destroyed next to an Ork mob led by a Painboy, can the Painboy's Feel No Pain save against the Deadly Demise mortal wounds?

<details><summary>reasoning trace (2373 chars, billed)</summary>

```
<think>
Okay, let's tackle this question step by step. The user is asking whether the Painboy's Feel No Pain (FNP) ability can save against the Deadly Demise mortal wounds when An'ggrath the Unbound is destroyed next to an Ork mob led by a Painboy.

First, I need to recall the relevant rules. From the provided context, there are a few key points to consider:

1. **Deadly Demise (Rule 5):** When a model with Deadly Demise is destroyed, you roll a D6. On a 6, each unit within 6" suffers mortal wounds. This is a specific ability that triggers when the model is destroyed.

2. **Feel No Pain (Rule 6):** Models with FNP can roll to ignore wounds. The Painboy has Dok’s Toolz, which gives FNP 5+ to his unit. So, when the unit suffers wounds, including mortal wounds, they can use this save.

3. **Interaction Between Abilities:** The question is whether FNP applies to the mortal wounds from Deadly Demise. Since FNP applies whenever a model would lose a wound, including from mortal wounds, it should work here unless there's an exception.

4. **Attached Units (Rule 3 and 4):** The Painboy is a Leader attached to his Ork mob. The rules state that when attacks are allocated, they use the Bodyguard's Toughness. However, for FNP, since it's a model's own ability, the Leader's FNP should apply to the entire Attached unit. The note in Rule 3 says that when attacks are made against an Attached unit, the Toughness used is the Bodyguard's, but FNP is about saving wounds, not Toughness. Therefore, the Painboy's FNP should still apply to the entire unit, including the Bodyguard models.

5. **No Specific Exceptions:** There's no mention in the provided rules that Deadly Demise's mortal wounds bypass FNP. The general rule is that FNP applies to any wound, including mortal ones, unless stated otherwise. Since the context doesn't indicate any such exception, the FNP should work as normal.

Putting it all together: When An'ggrath is destroyed, his Deadly Demise triggers, causing mortal wounds. The Ork mob, being an Attached unit led by the Painboy, has FNP 5+ from Dok’s Toolz. Therefore, each model in the unit can use their FNP to potentially ignore those mortal wounds. The key is that the FNP is part of the unit's abilities due to the Painboy's leadership, and there's no rule here that excludes it from applying to mortal wounds from Deadly Demise.
</think>

[Ruling] Yes, the Painboy's Feel No Pain 5+ (from Dok’s Toolz) applies to the mortal wounds caused by An’ggrath’s Deadly Demise.  
[Rule Citation] **Feel No Pain** (Core Rules 5. Inflict Damage — Feel No Pain) and **Dok’s Toolz** (Painboy’s Datasheet Abilities).  
[Reasoning]  
- **Feel No Pain** applies to all wounds, including mortal wounds, unless explicitly excluded. The Painboy’s **Dok’s Toolz** grants Feel No Pain 5+ to the entire Attached unit (the Ork mob).  
- **Deadly Demise** (Core Rules 5. Inflict Damage — Deadly Demise) inflicts mortal wounds when An’ggrath is destroyed. Since the Ork mob is an Attached unit, the Feel No Pain 5+ applies to all models in the unit, including the Bodyguard models.  
- No rule in the provided context excludes Feel No Pain from interacting with Deadly Demise. The Attached unit rules do not override or restrict the application of Feel No Pain.
```

</details>

**A:** [Ruling] Yes, the Painboy's Feel No Pain 5+ (from Dok’s Toolz) applies to the mortal wounds caused by An’ggrath’s Deadly Demise.  
[Rule Citation] **Feel No Pain** (Core Rules 5. Inflict Damage — Feel No Pain) and **Dok’s Toolz** (Painboy’s Datasheet Abilities).  
[Reasoning]  
- **Feel No Pain** applies to all wounds, including mortal wounds, unless explicitly excluded. The Painboy’s **Dok’s Toolz** grants Feel No Pain 5+ to the entire Attached unit (the Ork mob).  
- **Deadly Demise** (Core Rules 5. Inflict Damage — Deadly Demise) inflicts mortal wounds when An’ggrath is destroyed. Since the Ork mob is an Attached unit, the Feel No Pain 5+ applies to all models in the unit, including the Bodyguard models.  
- No rule in the provided context excludes Feel No Pain from interacting with Deadly Demise. The Attached unit rules do not override or restrict the application of Feel No Pain.

---

## [23] UNITS · mp=OFF · 1.9s

`billed: prompt=2097 completion=751 total=2848 · finish=stop` · ctx 1931 tok

**Q:** Compare the transport capacity of a Battlewagon and a Trukk, and what kinds of models each one is allowed to carry.

<details><summary>reasoning trace (1940 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user wants to compare the transport capacity of a Battlewagon and a Trukk, and what models each can carry. Let me start by looking at the provided rules context.

First, I'll check the Battlewagon's entry. From [1], the Battlewagon has a transport capacity of 22 Orks Infantry models. If it's equipped with a killkannon, that capacity drops to 12. Also, each Mega Armour or Jump Pack model takes up 2 spaces, and Ghazghkull Thraka takes 4. So, the Battlewagon can carry those specific models but with space penalties.

Now, the Trukk's entry in [2] says it can carry 12 Orks Infantry models. Each Mega Armour model takes 2 spaces here. Importantly, the Trukk cannot transport Jump Pack models or Ghazghkull Thraka. So, the Trukk's restrictions are stricter than the Battlewagon's in that it can't carry those two types at all, even with space adjustments.

Comparing the two, the Battlewagon has a higher base capacity (22 vs. 12) but when a killkannon is equipped, it's lower (12). The Trukk's capacity is lower but without the option to equip a killkannon. Both handle Mega Armour models by taking up double space, but the Trukk outright bans Jump Pack and Ghazghkull Thraka, while the Battlewagon allows them with space penalties.

I need to make sure I'm citing the correct rules. The Battlewagon's info is from [1], Trukk from [2], and the general transport capacity rules from [3]. The key differences are in their capacities and the allowed models. Also, the Trukk's restrictions are explicit in [2], while the Battlewagon's are in [1]. 

No other rules seem relevant here. The answer should highlight the capacity numbers, the effects of killkannon, and the specific models each can carry. I should structure the answer to first state the Battlewagon's capacity and restrictions, then the Trukk's, making sure to note the differences in allowed models and space calculations.
</think>

[Ruling]  
The **Battlewagon** (Orks) has a transport capacity of **22 Orks Infantry models** (or **12** if equipped with a killkannon). It can carry **Mega Armour** or **Jump Pack** models (each taking 2 spaces) and **Ghazghkull Thraka** (taking 4 spaces). The **Trukk** (Orks) has a transport capacity of **12 Orks Infantry models**, but **cannot** carry **Jump Pack** or **Ghazghkull Thraka** models. **Mega Armour** models in the Trukk take 2 spaces.  

[Rule Citations]  
- Battlewagon: [1] *Battlewagon (Orks)*.  
- Trukk: [2] *Trukk (Orks)*.  
- Transport Capacity: [3] *Transport Capacity (Core Rules)*.  

[Reasoning]  
The Battlewagon’s higher base capacity and flexibility to carry Jump Pack/Ghazghkull Thraka (with space penalties) contrast with the Trukk’s lower capacity and explicit bans on those models. Both handle Mega Armour similarly (2 spaces per model), but the Trukk’s restrictions are stricter. The Battlewagon’s killkannon reduces its capacity, while the Trukk has no such conditional reduction.
```

</details>

**A:** [Ruling]  
The **Battlewagon** (Orks) has a transport capacity of **22 Orks Infantry models** (or **12** if equipped with a killkannon). It can carry **Mega Armour** or **Jump Pack** models (each taking 2 spaces) and **Ghazghkull Thraka** (taking 4 spaces). The **Trukk** (Orks) has a transport capacity of **12 Orks Infantry models**, but **cannot** carry **Jump Pack** or **Ghazghkull Thraka** models. **Mega Armour** models in the Trukk take 2 spaces.  

[Rule Citations]  
- Battlewagon: [1] *Battlewagon (Orks)*.  
- Trukk: [2] *Trukk (Orks)*.  
- Transport Capacity: [3] *Transport Capacity (Core Rules)*.  

[Reasoning]  
The Battlewagon’s higher base capacity and flexibility to carry Jump Pack/Ghazghkull Thraka (with space penalties) contrast with the Trukk’s lower capacity and explicit bans on those models. Both handle Mega Armour similarly (2 spaces per model), but the Trukk’s restrictions are stricter. The Battlewagon’s killkannon reduces its capacity, while the Trukk has no such conditional reduction.

---

## [24] UNITS · mp=OFF · 2.5s

`billed: prompt=2196 completion=1014 total=3210 · finish=stop` · ctx 2160 tok

**Q:** If a Callidus Assassin and Boss Snikrot both deploy using Infiltrators, how close to the enemy can each of them be set up?

<details><summary>reasoning trace (3204 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about the deployment distances for a Callidus Assassin and Boss Snikrot when both use the Infiltrators ability. 

First, I need to check the rules provided. The Callidus Assassin has the Infiltrators keyword, which is covered in rule [3]. Rule [3] states that units with Infiltrators can be set up more than 9" away from the enemy deployment zone and all enemy models. So the Callidus Assassin can be placed more than 9" away from all enemy models.

Now, Boss Snikrot's ability is listed in rule [4]. His ability, Kunnin’ Infiltrator, allows him to remove and redeploy during his Movement phase, but the question is about deployment. The user is asking about initial deployment using Infiltrators. However, Boss Snikrot's own rules don't mention Infiltrators. Wait, the user says both deploy using Infiltrators. But does Boss Snikrot have the Infiltrators keyword? Let me check the provided rules. 

Looking at rule [4], Boss Snikrot's ability is a one-time redeploy in his Movement phase, but there's no mention of Infiltrators. Unless there's another rule giving him Infiltrators. The user might be assuming that Boss Snikrot has Infiltrators, but based on the provided context, there's no rule stating that Boss Snikrot has the Infiltrators keyword. Therefore, the initial deployment using Infiltrators for Boss Snikrot isn't covered here. 

Wait, the user's question says both deploy using Infiltrators. But according to the given rules, only the Callidus Assassin has Infiltrators (rule [3]). Boss Snikrot's ability is different. So maybe the user is mistaken, or there's an external rule not provided here. Since I can only use the provided context, I must go by what's given. 

Therefore, the Callidus Assassin can be set up more than 9" away from all enemy models due to Infiltrators (rule [3]). Boss Snikrot, lacking the Infiltrators keyword in the provided rules, doesn't have that deployment option. However, the user's question states that both deploy using Infiltrators, which might be an error. But since I have to answer based on the given context, I need to clarify that Boss Snikrot doesn't have Infiltrators here. 

Wait, maybe the user is referring to Boss Snikrot's own redeploy ability. His ability allows him to set up more than 9" away from all enemy models once per battle. But that's during his Movement phase, not initial deployment. The initial deployment for Boss Snikrot would follow standard rules unless he has Infiltrators. Since he doesn't have Infiltrators in the provided rules, his initial deployment would be subject to normal deployment rules, which typically require being within 6" of the enemy deployment zone. 

So the answer would be that the Callidus Assassin can be set up more than 9" away from all enemy models (Infiltrators), while Boss Snikrot, without Infiltrators, must be deployed normally, likely within 6" of the enemy deployment zone. However, the user's question states that both use Infiltrators, which might be incorrect based on the provided rules. Therefore, I need to point out that Boss Snikrot doesn't have the Infiltrators ability here, so his deployment is different.
</think>

[Ruling] The Callidus Assassin can be set up more than 9" horizontally away from all enemy models due to the **Infiltrators** ability (rule [3]). Boss Snikrot does **not** have the Infiltrators keyword in the provided rules, so he cannot use this deployment rule. Instead, his **Kunnin’ Infiltrator** ability (rule [4]) allows him to redeploy once per battle during his Movement phase, but this does not apply to initial deployment. For initial deployment, Boss Snikrot must follow standard deployment rules (e.g., within 6" of the enemy deployment zone unless otherwise stated).  

[Rule Citation]  
- Callidus Assassin: **Deployment Abilities — Infiltrators** [3].  
- Boss Snikrot: **Kunnin’ Infiltrator** [4] (does not grant Infiltrators for initial deployment).  

[Reasoning]  
The Callidus Assassin explicitly gains the Infiltrators ability (rule [3]), allowing it to bypass the 6" deployment rule. Boss Snikrot’s ability (rule [4]) is a **redeployment** tool, not a deployment rule, and does not grant Infiltrators. Since no rule in the provided context grants Boss Snikrot the Infiltrators keyword, he cannot use it for initial setup.
```

</details>

**A:** [Ruling] The Callidus Assassin can be set up more than 9" horizontally away from all enemy models due to the **Infiltrators** ability (rule [3]). Boss Snikrot does **not** have the Infiltrators keyword in the provided rules, so he cannot use this deployment rule. Instead, his **Kunnin’ Infiltrator** ability (rule [4]) allows him to redeploy once per battle during his Movement phase, but this does not apply to initial deployment. For initial deployment, Boss Snikrot must follow standard deployment rules (e.g., within 6" of the enemy deployment zone unless otherwise stated).  

[Rule Citation]  
- Callidus Assassin: **Deployment Abilities — Infiltrators** [3].  
- Boss Snikrot: **Kunnin’ Infiltrator** [4] (does not grant Infiltrators for initial deployment).  

[Reasoning]  
The Callidus Assassin explicitly gains the Infiltrators ability (rule [3]), allowing it to bypass the 6" deployment rule. Boss Snikrot’s ability (rule [4]) is a **redeployment** tool, not a deployment rule, and does not grant Infiltrators. Since no rule in the provided context grants Boss Snikrot the Infiltrators keyword, he cannot use it for initial setup.

---

## [25] UNITS · mp=OFF · 1.6s

`billed: prompt=2914 completion=538 total=3452 · finish=stop` · ctx 2756 tok

**Q:** What melee weapons does Abaddon the Despoiler have on his datasheet, and what does his Dark Destiny ability do?

<details><summary>reasoning trace (1479 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about Abaddon the Despoiler's melee weapons and his Dark Destiny ability. 

First, I need to look at the provided rules context. From the first entry under [1], there's a section for Wargear with his weapons. The table lists two weapons: Talon of Horus and Drach’nyen. The Talon of Horus has both a ranged and a melee profile. The Drach’nyen is a melee weapon. So, his melee weapons are the Talon of Horus (melee) and Drach’nyen. 

Next, the Dark Destiny ability is covered in [2]. The ability states that each time his unit makes a Dark Pact and doesn't fail the Leadership test, if the result is 7+, you gain 1CP. I need to make sure there's no other mention of Dark Destiny elsewhere that might modify this, but in the given context, [2] is the only source. 

I should check if there are any other relevant rules. The Core Rules about weapons in [3] and [5] explain how weapons are selected and used, but since the question is specifically about Abaddon's weapons and his ability, those aren't directly needed here. 

So, the answer should list both melee weapons and explain the Dark Destiny ability with the correct citation. Need to ensure that the Talon of Horus (melee) is included even though it also has a ranged profile. The user might be confused if they think he only has one weapon, but the datasheet shows two separate entries. Also, confirm that the Dark Destiny is correctly cited from [2].
</think>

[Ruling]  
Abaddon the Despoiler has two melee weapons on his datasheet: **Talon of Horus (Melee)** and **Drach’nyen**. His **Dark Destiny** ability grants 1CP each time his unit makes a Dark Pact, passes the Leadership test, and achieves a result of 7+ on that test.  

[Rule Citations]  
- **Melee Weapons**: [1] Abaddon The Despoiler (Chaos Space Marines) → Wargear table.  
- **Dark Destiny**: [2] Abaddon The Despoiler (Chaos Space Marines) → Ability: Dark Destiny.  

[Reasoning]  
The Wargear table in [1] explicitly lists both melee weapons. The Dark Destiny ability in [2] is a standalone rule tied to Abaddon’s unit, overriding general Core Rules for CP generation when its conditions are met.
```

</details>

**A:** [Ruling]  
Abaddon the Despoiler has two melee weapons on his datasheet: **Talon of Horus (Melee)** and **Drach’nyen**. His **Dark Destiny** ability grants 1CP each time his unit makes a Dark Pact, passes the Leadership test, and achieves a result of 7+ on that test.  

[Rule Citations]  
- **Melee Weapons**: [1] Abaddon The Despoiler (Chaos Space Marines) → Wargear table.  
- **Dark Destiny**: [2] Abaddon The Despoiler (Chaos Space Marines) → Ability: Dark Destiny.  

[Reasoning]  
The Wargear table in [1] explicitly lists both melee weapons. The Dark Destiny ability in [2] is a standalone rule tied to Abaddon’s unit, overriding general Core Rules for CP generation when its conditions are met.

---

## [26] UNITS · mp=OFF · 1.7s

`billed: prompt=1697 completion=604 total=2301 · finish=stop` · ctx 1496 tok

**Q:** What is the Battlewagon's transport capacity, and separately what does its 'Ard Case ability do?

<details><summary>reasoning trace (1502 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about the Battlewagon's transport capacity and the effect of its 'Ard Case ability. 

First, I need to look at the rules provided. The Battlewagon is an Ork unit. Let me check the entries related to it. 

Looking at entry [2], under "Battlewagon — Transport," it states the transport capacity. The first part says it can carry 22 Orks Infantry models. But if it's equipped with a killkannon, the capacity drops to 12. Also, Mega Armour or Jump Pack models take up 2 spaces each, and Ghazghkull Thraka takes 4. So the transport capacity depends on whether it has a killkannon and the types of models inside.

Next, the 'Ard Case ability is in entry [1]. It adds 2 to the Toughness characteristic but removes the Firing Deck ability. The Firing Deck is mentioned in entry [3], which allows embarked models to shoot through the transport. Since 'Ard Case removes that, the Battlewagon can't use the Firing Deck when this ability is active.

I need to make sure there's no other rule affecting this. The core rules about transports in [3] and [4] don't override the specific Battlewagon entries. Also, the 'Ard Case ability is specific to the Battlewagon, so it's straightforward. 

So the answer should state the transport capacity based on the presence of a killkannon and the space taken by certain models. For the 'Ard Case, it's adding Toughness and removing Firing Deck. I need to cite the exact rules from the context provided.
</think>

[Ruling]  
The **Battlewagon** has a transport capacity of **22 Orks Infantry models** unless equipped with a **killkannon**, in which case it can carry **12 Orks Infantry models**. Each **Mega Armour** or **Jump Pack** model occupies 2 spaces, and the **Ghazghkull Thraka** model occupies 4 spaces.  

The **'Ard Case** ability adds **+2 to the Battlewagon’s Toughness characteristic** but removes its **Firing Deck ability** (preventing it from allowing embarked models to shoot via the Firing Deck rules).  

[Rule Citations]  
- Transport capacity: [2] *Battlewagon — Transport*  
- 'Ard Case ability: [1] *Battlewagon (Orks)*  
- Firing Deck rules: [3] *Transport Capacity*  

[Reasoning]  
The transport capacity is explicitly defined in [2], with modifiers for killkannon and model types. The 'Ard Case ability’s effects are directly stated in [1], overriding the Firing Deck ability (see [3] for the standard Firing Deck rules). No other rules in the context modify these specifics.
```

</details>

**A:** [Ruling]  
The **Battlewagon** has a transport capacity of **22 Orks Infantry models** unless equipped with a **killkannon**, in which case it can carry **12 Orks Infantry models**. Each **Mega Armour** or **Jump Pack** model occupies 2 spaces, and the **Ghazghkull Thraka** model occupies 4 spaces.  

The **'Ard Case** ability adds **+2 to the Battlewagon’s Toughness characteristic** but removes its **Firing Deck ability** (preventing it from allowing embarked models to shoot via the Firing Deck rules).  

[Rule Citations]  
- Transport capacity: [2] *Battlewagon — Transport*  
- 'Ard Case ability: [1] *Battlewagon (Orks)*  
- Firing Deck rules: [3] *Transport Capacity*  

[Reasoning]  
The transport capacity is explicitly defined in [2], with modifiers for killkannon and model types. The 'Ard Case ability’s effects are directly stated in [1], overriding the Firing Deck ability (see [3] for the standard Firing Deck rules). No other rules in the context modify these specifics.

---

## [27] UNITS · mp=OFF · 1.9s

`billed: prompt=2911 completion=637 total=3548 · finish=stop` · ctx 2590 tok

**Q:** What is the Callidus Assassin's Movement characteristic, and what does her Acrobatic Escape ability do?

<details><summary>reasoning trace (1715 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about the Callidus Assassin's Movement characteristic and the details of her Acrobatic Escape ability.

First, I need to check the provided rules context. Let's start with the Movement characteristic. Looking through the datasheet in entry [8], under the Stats section, the Callidus Assassin has a Movement (M) value of 7". That's straightforward.

Next, the Acrobatic Escape ability. There's information in both [1] and [8]. In [1], the ability is described as allowing a Fall Back move of up to D6" at the end of the Fight phase if she's in Engagement Range. Also, at the end of the opponent's turn, if she's not within 3" of enemies, she can be removed and then set up again more than 9" away during the next Movement phase. If the battle ends and she's not on the board, she's destroyed. Entry [8] repeats the same details under the Datasheet Abilities section, confirming the same information.

I need to make sure there's no conflicting information. The Movement characteristic is clearly stated as 7", and the Acrobatic Escape ability is fully detailed in both sections. No other rules in the context seem to affect this. The Fall Back move is covered under Core Rules in [3], but since the ability specifies the D6" move, that's the key part here. Also, since the Callidus Assassin isn't flying or a Titan, the Desperate Escape tests would apply if she moves through enemies, but the question isn't asking about that.

So, the answer should state the Movement is 7" and outline the two parts of Acrobatic Escape as per the given rules. No need to reference other rules unless they override, but here the provided context is sufficient.
</think>

[Ruling] The Callidus Assassin has a Movement (M) characteristic of **7"**. Her **Acrobatic Escape** ability allows two actions:  
1. At the end of the Fight phase, if within Engagement Range of one or more enemy units, she can make a **Fall Back move of up to D6"**.  
2. At the end of her opponent’s turn, if she is **not within 3" of any enemy units**, she can be **removed from the battlefield** and **reappear during the Reinforcements step of the player’s next Movement phase**, set up **more than 9" horizontally away from all enemy models**. If the battle ends while she is off the battlefield, she is destroyed.  

[Rule Citations]  
- Movement characteristic: [8] Callidus Assassin (Stats table).  
- Acrobatic Escape: [1] Callidus Assassin (Ability) and [8] Callidus Assassin (Datasheet Abilities).  

[Reasoning] The Movement value is explicitly stated in her datasheet. The Acrobatic Escape ability is detailed in both her unit profile and datasheet, with no conflicting rules in the provided context overriding its functionality.
```

</details>

**A:** [Ruling] The Callidus Assassin has a Movement (M) characteristic of **7"**. Her **Acrobatic Escape** ability allows two actions:  
1. At the end of the Fight phase, if within Engagement Range of one or more enemy units, she can make a **Fall Back move of up to D6"**.  
2. At the end of her opponent’s turn, if she is **not within 3" of any enemy units**, she can be **removed from the battlefield** and **reappear during the Reinforcements step of the player’s next Movement phase**, set up **more than 9" horizontally away from all enemy models**. If the battle ends while she is off the battlefield, she is destroyed.  

[Rule Citations]  
- Movement characteristic: [8] Callidus Assassin (Stats table).  
- Acrobatic Escape: [1] Callidus Assassin (Ability) and [8] Callidus Assassin (Datasheet Abilities).  

[Reasoning] The Movement value is explicitly stated in her datasheet. The Acrobatic Escape ability is detailed in both her unit profile and datasheet, with no conflicting rules in the provided context overriding its functionality.

---

## [28] UNITS · mp=OFF · 1.7s

`billed: prompt=2499 completion=629 total=3128 · finish=stop` · ctx 2197 tok

**Q:** What is the Trukk's transport capacity, and what does its Grot Riggers ability do?

<details><summary>reasoning trace (1600 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking about the Trukk's transport capacity and the Grot Riggers ability. 

First, I need to check the rules provided. Looking at the context, there are several entries related to the Trukk. 

Starting with the transport capacity. In the rules, under [1] Trukk (Orks), it says the Trukk has a transport capacity of 12 Orks Infantry models. Also, each Mega Armour model takes up the space of 2 models. It can't transport Jump Pack or Ghazghkull Thraka models. There's another mention in [8] under the Transport section that repeats the same info. So the transport capacity is definitely 12 Orks Infantry, with the exceptions noted.

Next, the Grot Riggers ability. In [2] Trukk (Orks), the ability is described as regaining 1 lost wound at the start of the Command phase. Also, in [8], under Datasheet Abilities, Grot Riggers is the same. So the ability is straightforward: at the start of the Command phase, the Trukk regains 1 lost wound.

I need to make sure there's no conflicting information. The transport capacity is consistent across the rules provided. The Grot Riggers ability is only mentioned in the Trukk's specific rules, so no other general rules override it. 

No other sections mention exceptions or additional effects for these. The user didn't ask about any other abilities, so I don't need to check further. 

So the answer should state the transport capacity with the specifics about Mega Armour and prohibited models, and the Grot Riggers effect with when it triggers. Cite the relevant rule numbers for each part.
</think>

[**Ruling**]  
The Trukk has a transport capacity of **12 Orks Infantry models**, with each **Mega Armour** model occupying the space of 2 models. It **cannot transport** **Jump Pack** or **Ghazghkull Thraka** models.  

The **Grot Riggers** ability allows the Trukk to **regain 1 lost wound** at the **start of your Command phase**.  

[**Rule Citations**]  
- Transport capacity: [1] Trukk (Orks) → "This model has a transport capacity of 12 Orks Infantry models. Each Mega Armour model takes up the space of 2 models. It cannot transport Jump Pack or Ghazghkull Thraka models."  
- Grot Riggers: [2] Trukk (Orks) → "At the start of your Command phase, this model regains 1 lost wound."  

[**Reasoning**]  
The transport capacity and restrictions are explicitly stated in the Trukk’s unit profile. The Grot Riggers ability is a dedicated model-specific effect with no additional conditions or interactions beyond its stated trigger. No conflicting rules override these details in the provided context.
```

</details>

**A:** [**Ruling**]  
The Trukk has a transport capacity of **12 Orks Infantry models**, with each **Mega Armour** model occupying the space of 2 models. It **cannot transport** **Jump Pack** or **Ghazghkull Thraka** models.  

The **Grot Riggers** ability allows the Trukk to **regain 1 lost wound** at the **start of your Command phase**.  

[**Rule Citations**]  
- Transport capacity: [1] Trukk (Orks) → "This model has a transport capacity of 12 Orks Infantry models. Each Mega Armour model takes up the space of 2 models. It cannot transport Jump Pack or Ghazghkull Thraka models."  
- Grot Riggers: [2] Trukk (Orks) → "At the start of your Command phase, this model regains 1 lost wound."  

[**Reasoning**]  
The transport capacity and restrictions are explicitly stated in the Trukk’s unit profile. The Grot Riggers ability is a dedicated model-specific effect with no additional conditions or interactions beyond its stated trigger. No conflicting rules override these details in the provided context.

---

## [29] UNITS · mp=OFF · 1.9s

`billed: prompt=1519 completion=624 total=2143 · finish=stop` · ctx 1229 tok

**Q:** Chief Librarian Mephiston has Fights First. If he is in combat with an enemy unit that also has Fights First, who fights first?

<details><summary>reasoning trace (2022 chars, billed)</summary>

```
<think>
Okay, let's see. The user is asking about who fights first when both Chief Librarian Mephiston and an enemy unit with Fights First are in combat. 

First, I need to check the rules provided. The Chief Librarian Mephiston has the Fights First ability, as mentioned in his keywords. The enemy unit also has Fights First. 

Looking at the core rules, specifically the Fights First section (rule 2), it says that units with Fights First fight in the Fights First step. The Fight phase is split into two steps: Fights First and Remaining Combats. In the Fights First step, all eligible units with that ability fight. 

But the question is about two units both having Fights First. The rules don't mention any priority between them. The Fights First step includes all eligible units, regardless of which side they're on. Both players alternate selecting units to fight, starting with the player whose turn is not active. However, the user's question is about who goes first when both are in combat.

Wait, the rules state that in both steps of the Fight phase, players alternate selecting eligible units from their army, one at a time, starting with the player whose turn is not taking place. So if it's the active player's turn, the non-active player goes first in selecting their Fights First units. But if both units are eligible, they would alternate. However, the question is about who "fights first" between the two units. 

The rules don't specify that one unit goes before another if both have Fights First. They just alternate selection. So if both units are eligible, they both fight in the Fights First step, with the players taking turns selecting. The order depends on whose turn it is. 

So the answer would be that both units fight in the Fights First step, with the players alternating selection starting with the non-active player. There's no rule that one Fights First unit overrides another. Therefore, both get to fight in that step, but the order of selection depends on whose turn it is.
</think>

[Ruling] Both units with the Fights First ability will fight in the Fights First step of the Fight phase. Players alternate selecting their eligible units to fight, starting with the player whose turn is not currently taking place. If both units are eligible, they will both fight in this step, with the order of selection determined by turn order.  

[Rule Citation] **Fights First** (Core Rules 1. Fights First) and **Fight Phase** (Core Rules 4. Fight Phase).  

[Reasoning] The Fights First step includes all units with the Fights First ability, regardless of faction. Players alternate selecting units to fight in this step, starting with the non-active player. Since both units meet the criteria, they both fight in the Fights First step, but the order of selection depends on whose turn it is. No rule prioritizes one Fights First unit over another in this context.
```

</details>

**A:** [Ruling] Both units with the Fights First ability will fight in the Fights First step of the Fight phase. Players alternate selecting their eligible units to fight, starting with the player whose turn is not currently taking place. If both units are eligible, they will both fight in this step, with the order of selection determined by turn order.  

[Rule Citation] **Fights First** (Core Rules 1. Fights First) and **Fight Phase** (Core Rules 4. Fight Phase).  

[Reasoning] The Fights First step includes all units with the Fights First ability, regardless of faction. Players alternate selecting units to fight in this step, starting with the non-active player. Since both units meet the criteria, they both fight in the Fights First step, but the order of selection depends on whose turn it is. No rule prioritizes one Fights First unit over another in this context.

---

## [30] UNITS · mp=OFF · 2.6s

`billed: prompt=1461 completion=1015 total=2476 · finish=stop` · ctx 1236 tok

**Q:** How does the Aegis Defence Line fortification give units the Benefit of Cover, and how do models interact with it?

<details><summary>reasoning trace (2818 chars, billed)</summary>

```
<think>
Okay, let's tackle this question about the Aegis Defence Line fortification. The user wants to know how it grants the Benefit of Cover and how models interact with it.

First, I need to look at the provided rules. The Aegis Defence Line has two abilities: Reinforced Cover and Defence Line. 

Starting with Reinforced Cover (rule 1), it says that each time a ranged attack is allocated to a model, if the model isn't fully visible to every model in the attacking unit because of the fortification, then the model has the Benefit of Cover. So the key here is visibility being blocked by the Aegis Defence Line itself. This is different from other terrain features like Barricades or Rubble, which might have different conditions. 

Then, the Defence Line ability (rule 2) states that while an Astra Militarum Infantry model has the Benefit of Cover from this terrain, they get a 4+ invulnerable save. So this is an additional benefit on top of the standard Benefit of Cover rules.

Looking at the general Benefit of Cover rules (rule 3), it adds +1 to armor saves against ranged attacks, but not for models with a 3+ save against AP 0. Also, multiple instances don't stack. So the Aegis Defence Line's Benefit of Cover would follow these core rules, but with the specific condition of visibility being blocked by the fortification.

Other terrain features like Barricades (rule 4) and Rubble (rule 6) have their own conditions for granting Benefit of Cover. For example, Barricades require being within 3", and Rubble requires being on top. The Aegis Defence Line's condition is purely based on visibility being blocked by the fortification itself, regardless of distance or position, as long as the attacker can't see the model fully because of the fortification.

Also, there's a mention in rule 7 and 8 about other fortifications (like the Aegis with Weapon Emplacement and Wall Of Martyrs) giving invulnerable saves, but those are for different units. The Aegis Defence Line specifically applies to Astra Militarum Infantry.

So putting it all together: The Aegis Defence Line grants Benefit of Cover when an attack can't fully see the model due to the fortification. This triggers the core Benefit of Cover rules, adding +1 to saves, and for Astra Militarum Infantry, gives a 4+ invulnerable save. Models must be positioned such that the fortification blocks visibility from the attacker. Movement rules for the fortification aren't specified here, but since it's a fortification, it's likely immobile and can't be set up or moved during the game unless stated otherwise. Also, the fortification's setup requires parts to be within 1" of each other (rule 7), but that's for the version with the weapon emplacement. The standard Aegis Defence Line might not have that setup rule unless specified.
</think>

[Ruling] The **Aegis Defence Line** grants the **Benefit of Cover** to models when a ranged attack is allocated to them, and the model is **not fully visible to every model in the attacking unit because of the fortification**. This triggers the core Benefit of Cover rules (add +1 to armour saves against ranged attacks, excluding invulnerable saves). Additionally, **Astra Militarum Infantry models** with this Benefit of Cover gain a **4+ invulnerable save**.  

[Rule Citation]  
- **Reinforced Cover** (Aegis Defence Line, rule 1): Grants Benefit of Cover if visibility is blocked by the fortification.  
- **Defence Line** (Aegis Defence Line, rule 2): Grants a 4+ invulnerable save to Astra Militarum Infantry with Benefit of Cover from this fortification.  
- **Benefit of Cover** (Core Rules, rule 3): Defines the mechanics of the Benefit of Cover (add +1 to saves, stacking restrictions).  

[Reasoning]  
The Aegis Defence Line’s **Reinforced Cover** ability explicitly ties the Benefit of Cover to visibility being blocked by the fortification itself. This differs from terrain features like **Barricades** (rule 4) or **Craters** (rule 6), which require proximity or positioning. Once a model gains the Benefit of Cover via this rule, the core rules apply (e.g., +1 to saves). The **Defence Line** ability then adds a 4+ invulnerable save **only for Astra Militarum Infantry**, stacking with the core Benefit of Cover rules.  

No movement or setup restrictions are specified for the Aegis Defence Line beyond its **Fortification** keyword (rule 7), which requires parts to be within 1" of each other when set up (but this applies to the "With Weapon Emplacement" variant, not the base Aegis Defence Line).
```

</details>

**A:** [Ruling] The **Aegis Defence Line** grants the **Benefit of Cover** to models when a ranged attack is allocated to them, and the model is **not fully visible to every model in the attacking unit because of the fortification**. This triggers the core Benefit of Cover rules (add +1 to armour saves against ranged attacks, excluding invulnerable saves). Additionally, **Astra Militarum Infantry models** with this Benefit of Cover gain a **4+ invulnerable save**.  

[Rule Citation]  
- **Reinforced Cover** (Aegis Defence Line, rule 1): Grants Benefit of Cover if visibility is blocked by the fortification.  
- **Defence Line** (Aegis Defence Line, rule 2): Grants a 4+ invulnerable save to Astra Militarum Infantry with Benefit of Cover from this fortification.  
- **Benefit of Cover** (Core Rules, rule 3): Defines the mechanics of the Benefit of Cover (add +1 to saves, stacking restrictions).  

[Reasoning]  
The Aegis Defence Line’s **Reinforced Cover** ability explicitly ties the Benefit of Cover to visibility being blocked by the fortification itself. This differs from terrain features like **Barricades** (rule 4) or **Craters** (rule 6), which require proximity or positioning. Once a model gains the Benefit of Cover via this rule, the core rules apply (e.g., +1 to saves). The **Defence Line** ability then adds a 4+ invulnerable save **only for Astra Militarum Infantry**, stacking with the core Benefit of Cover rules.  

No movement or setup restrictions are specified for the Aegis Defence Line beyond its **Fortification** keyword (rule 7), which requires parts to be within 1" of each other when set up (but this applies to the "With Weapon Emplacement" variant, not the base Aegis Defence Line).

---

## [31] ILLEGAL · mp=OFF · 1.4s

`billed: prompt=2082 completion=446 total=2528 · finish=stop` · ctx 1877 tok

**Q:** Can a 5-model Terminator Squad embark inside a Rhino transport?

<details><summary>reasoning trace (1396 chars, billed)</summary>

```
<think>
Okay, let's tackle this question. The user is asking if a 5-model Terminator Squad can embark inside a Rhino transport. Let me check the rules provided.

First, I need to look at the transport capacities of the Rhino. There are two entries for Rhino transports: one for Grey Knights and one for Space Marines. The Grey Knights Rhino can carry 12 Grey Knights Infantry models but not Terminators. The Space Marines Rhino can carry 12 Adeptus Astartes Infantry models but explicitly states it cannot transport Terminator models, along with others like Jump Pack, Wulfen, etc. 

So, regardless of which Rhino we're talking about, the Terminator Squad is not allowed. The key point here is the "cannot transport Terminator models" clause in both cases. The user's Terminator Squad is part of the Space Marines, so the Space Marines Rhino's rules apply. Since the Rhino's transport capacity excludes Terminators, even if the unit size is within the 12 model limit, they can't be embarked. 

Also, the Core Rules about Embark and Transport Capacity don't override the specific model's transport restrictions. The Core Rule says units can embark if they meet the transport's capacity, but the Rhino's specific entry takes precedence here. 

So the answer is no. The Terminator Squad can't embark in a Rhino because the Rhino's transport capacity explicitly excludes Terminator models.
</think>

[Ruling] No, a 5-model Terminator Squad cannot embark inside a Rhino transport.  
[Rule Citation] **Rhino (Space Marines)** → "This model has a transport capacity of 12 ADEPTUS ASTARTES INFANTRY models. It cannot transport JUMP PACK, WULFEN, PHOBOS, GRAVIS, CENTURION, TERMINATOR or TACTICUS models..."  
[Reasoning] The Space Marines Rhino explicitly prohibits transporting Terminator models, regardless of unit size. While the Terminator Squad is an Adeptus Astartes Infantry unit, the "TERMINATOR" keyword disqualifies it from being embarked due to the Rhino’s stated restriction. Core Rules on Embark and Transport Capacity do not override this specific exclusion.
```

</details>

**A:** [Ruling] No, a 5-model Terminator Squad cannot embark inside a Rhino transport.  
[Rule Citation] **Rhino (Space Marines)** → "This model has a transport capacity of 12 ADEPTUS ASTARTES INFANTRY models. It cannot transport JUMP PACK, WULFEN, PHOBOS, GRAVIS, CENTURION, TERMINATOR or TACTICUS models..."  
[Reasoning] The Space Marines Rhino explicitly prohibits transporting Terminator models, regardless of unit size. While the Terminator Squad is an Adeptus Astartes Infantry unit, the "TERMINATOR" keyword disqualifies it from being embarked due to the Rhino’s stated restriction. Core Rules on Embark and Transport Capacity do not override this specific exclusion.

---

## [32] ILLEGAL · mp=OFF · 1.5s

`billed: prompt=1776 completion=438 total=2214 · finish=stop` · ctx 1634 tok

**Q:** Can I set up a unit using Deep Strike just 3 inches away from an enemy unit?

<details><summary>reasoning trace (1348 chars, billed)</summary>

```
<think>
Okay, let's see. The user is asking if they can set up a unit using Deep Strike just 3 inches away from an enemy unit. I need to check the rules provided to answer this.

First, looking at the Deep Strike rule in the context. Rule [1] says that when a unit with Deep Strike arrives from Strategic Reserves, it can be set up more than 9" horizontally away from all enemy models. So the minimum distance is 9 inches. 

Then there's rule [3] about stratagems that allow a closer set up range. It mentions that if a stratagem allows setting up more than 3" away, it's changed to 6". But this applies to stratagems, not the Deep Strike ability itself. The question is about using Deep Strike, not a stratagem. So rule [3] doesn't override the Deep Strike requirement here.

Also, rule [4] talks about Strategic Reserve units, but Deep Strike is an alternative to Strategic Reserves. The Deep Strike setup is separate from the Strategic Reserve setup rules. The user is specifically asking about Deep Strike, so the 9" minimum from rule [1] applies.

Therefore, the answer should be no. The unit must be set up more than 9" away from enemies when using Deep Strike. The 3" distance is too close and doesn't meet the requirement. There's no mention of any exception or stratagem being used here, so the standard Deep Strike rule stands.
</think>

[Ruling] No, a unit using Deep Strike must be set up more than 9" horizontally away from all enemy models.  
[Rule Citation] Deployment Abilities — Deep Strike (Core Rules)  
[Reasoning] The Deep Strike rule explicitly requires units to be set up "more than 9" horizontally away from all enemy models" when arriving via this ability. Rule [3] (Stratagems That Allow a Closer Set Up Range) only modifies effects from stratagems (e.g., Cosmic Precision), not the Deep Strike ability itself. No rule in the provided context allows reducing this distance below 9".
```

</details>

**A:** [Ruling] No, a unit using Deep Strike must be set up more than 9" horizontally away from all enemy models.  
[Rule Citation] Deployment Abilities — Deep Strike (Core Rules)  
[Reasoning] The Deep Strike rule explicitly requires units to be set up "more than 9" horizontally away from all enemy models" when arriving via this ability. Rule [3] (Stratagems That Allow a Closer Set Up Range) only modifies effects from stratagems (e.g., Cosmic Precision), not the Deep Strike ability itself. No rule in the provided context allows reducing this distance below 9".

---

## [33] ILLEGAL · mp=OFF · 1.4s

`billed: prompt=2894 completion=329 total=3223 · finish=stop` · ctx 2786 tok

**Q:** My unit Fell Back this turn — can that same unit then declare a charge this turn?

<details><summary>reasoning trace (978 chars, billed)</summary>

```
<think>
Okay, let's see. The user is asking if a unit that Fell Back this turn can declare a charge in the same turn. I need to check the rules provided.

Looking at the Fall Back Moves rule (1), it says that a unit that Falls Back cannot shoot or declare a charge in the same turn. So right there, that seems to answer it. But wait, maybe there's another rule that could affect this?

Then checking the Charge Phase (2), the eligibility for charging includes that a unit cannot charge if it Advanced or Fell Back this turn. So both rules are pointing to the same conclusion. The unit is ineligible to charge after Falling Back.

Also, the Disembark rule (3) mentions that units disembarking after a transport that Fell Back can't charge, but that's a different scenario. The key points are in the Fall Back and Charge Phase rules. There's no mention of any exceptions here. So the answer should be no, citing both the Fall Back rule and the Charge Phase eligibility.
</think>

[Ruling] No, a unit that Fell Back this turn cannot declare a charge in the same turn.  
[Rule Citation] **Fall Back Moves** (Core Rules) and **Charge Phase** (Core Rules).  
[Reasoning]  
1. **Fall Back Moves** explicitly states: "Units that Fall Back cannot shoot or declare a charge in the same turn."  
2. **Charge Phase** confirms: A unit is ineligible to charge if "that unit Advanced or Fell Back this turn."  

Both rules independently prohibit the unit from declaring a charge after Falling Back.
```

</details>

**A:** [Ruling] No, a unit that Fell Back this turn cannot declare a charge in the same turn.  
[Rule Citation] **Fall Back Moves** (Core Rules) and **Charge Phase** (Core Rules).  
[Reasoning]  
1. **Fall Back Moves** explicitly states: "Units that Fall Back cannot shoot or declare a charge in the same turn."  
2. **Charge Phase** confirms: A unit is ineligible to charge if "that unit Advanced or Fell Back this turn."  

Both rules independently prohibit the unit from declaring a charge after Falling Back.

---

## [34] ILLEGAL · mp=OFF · 1.1s

`billed: prompt=1455 completion=339 total=1794 · finish=stop` · ctx 1231 tok

**Q:** Can my Space Marine unit embark inside an enemy Ork Trukk?

<details><summary>reasoning trace (1021 chars, billed)</summary>

```
<think>
Okay, let's see. The user is asking if their Space Marine unit can embark inside an enemy Ork Trukk. Hmm. First, I need to check the rules provided.

Looking at the Embark rule (4), it says that a unit can embark within a friendly TRANSPORT model. The key word here is "friendly." The Trukk is an Ork model, so it's an enemy unit. The Space Marines are on the opposing side, so the Trukk isn't friendly to them. 

Also, the Transport rules (7) mention that TRANSPORT keyword models are used by their own units. There's no mention of being able to use enemy transports. The Rapid Embarkation stratagem (8) allows a Space Marine unit to embark in a friendly Heavy Transport, but again, the Trukk is enemy. 

Additionally, the Trukk's entry (3) specifies its transport capacity for Orks, but even if there was space, the Space Marines aren't Orks. The rules don't allow units to embark in enemy transports. So the answer should be no, citing the Embark rule's requirement for the transport to be friendly.
</think>

[Ruling] No, your Space Marine unit cannot embark inside an enemy Ork Trukk.  
[Rule Citation] **Embark (Core Rules)** → "A unit can embark within a friendly TRANSPORT model..."  
[Reasoning] The Trukk is an enemy unit (Orks faction), and the "friendly" requirement explicitly restricts embarking to allied TRANSPORT models. No rules in the provided context allow embarking in enemy transports.
```

</details>

**A:** [Ruling] No, your Space Marine unit cannot embark inside an enemy Ork Trukk.  
[Rule Citation] **Embark (Core Rules)** → "A unit can embark within a friendly TRANSPORT model..."  
[Reasoning] The Trukk is an enemy unit (Orks faction), and the "friendly" requirement explicitly restricts embarking to allied TRANSPORT models. No rules in the provided context allow embarking in enemy transports.

---

## [35] ILLEGAL · mp=OFF · 2.1s

`billed: prompt=2849 completion=679 total=3528 · finish=stop` · ctx 2710 tok

**Q:** Can a single model in my 10-model unit end its move 4 inches away from every other model in that unit?

<details><summary>reasoning trace (2092 chars, billed)</summary>

```
<think>
Okay, let's see. The user is asking if a single model in their 10-model unit can end its move 4 inches away from every other model. Hmm.

First, I need to check the Unit Coherency rules. From the provided context, [1] says that units with more than one model must be set up and end moves as a group, with all models within 2" horizontally and 5" vertically of at least one other model. For units with 7+ models, they need to be within 2" of two other models.

So, the user's unit has 10 models. According to rule [1], each model must be within 2" of at least two others. If one model is 4 inches away from all others, that's way beyond the 2" requirement. That model wouldn't be within 2" of any other model, let alone two. Therefore, the entire unit would fail the coherency check.

The rules also mention that if a unit can't end a move in coherency, the move is invalid, and models are returned to previous positions. Additionally, at the end of each turn, any unit not in coherency must have models removed until coherency is restored. So, in this case, the unit would have to remove models until the remaining ones meet the coherency requirements. The single model that's too far away would be considered out of coherency and would need to be removed, but since it's just one model, maybe they remove that one? Wait, the rule says to remove models one at a time until only a single group remains. But if the unit is split into two groups, they remove models from the smaller group first? Or just remove models until the entire unit is in one coherent group.

But the question is about ending a move with one model out of position. The answer is no, because the unit must end the move in coherency. If they can't, the move is invalid. So the ruling is that the model cannot end the move 4 inches away from others because it violates unit coherency. The specific rule is [1] Unit Coherency, which requires all models in a 7+ unit to be within 2" of two others. The model being 4 inches away breaks that, so the move is invalid, and the unit must adjust or remove models.
</think>

[Ruling] No. A unit with 10 models must end its move with all models within 2" horizontally of **two** other models (per Unit Coherency rules for 7+ models). A single model 4" away from all others violates this requirement, causing the entire unit to fail Unit Coherency. The move would be invalid, and the unit would need to remove models until coherency is restored.  

[Rule Citation] **Unit Coherency** → Core_Rules (Wahapedia_Core_Rules)  
[Reasoning] Rule [1] explicitly states that units with 7+ models must have all models within 2" horizontally of **two** other models. A model 4" away from all others cannot satisfy this requirement, breaking coherency. The unit cannot legally end the move in this configuration.
```

</details>

**A:** [Ruling] No. A unit with 10 models must end its move with all models within 2" horizontally of **two** other models (per Unit Coherency rules for 7+ models). A single model 4" away from all others violates this requirement, causing the entire unit to fail Unit Coherency. The move would be invalid, and the unit would need to remove models until coherency is restored.  

[Rule Citation] **Unit Coherency** → Core_Rules (Wahapedia_Core_Rules)  
[Reasoning] Rule [1] explicitly states that units with 7+ models must have all models within 2" horizontally of **two** other models. A model 4" away from all others cannot satisfy this requirement, breaking coherency. The unit cannot legally end the move in this configuration.

---

