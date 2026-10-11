# Model answer collection — 8 models

> **⚠️ STATUS (2026-07-21):** `qwen/qwen3-32b` (listed below) was **RETIRED — Groq closed it on the
> free tier.** Production is now **`openai/gpt-oss-120b`** (co-best here at 43/43). qwen3-32b's answers
> below are a historical record only; it is no longer a selectable model.

Groq models: qwen/qwen3-32b, qwen/qwen3.6-27b, llama-3.3-70b-versatile, llama-3.1-8b-instant, meta-llama/llama-4-scout-17b-16e-instruct, openai/gpt-oss-120b, openai/gpt-oss-20b, allam-2-7b

Pipeline: retrieval.build_context → serving.build_messages (budget 2800 tok). cap_mode=tpm (per-model TPM-sized: qwen3-32b=2560, llama-3.1-8b-instant=2560, allam-2-7b=2560, qwen3.6-27b=4096, gpt-oss-120b=4096, gpt-oss-20b=4096, llama-3.3-70b-versatile=8192, llama-4-scout-17b-16e-instruct=8192), temperature=0.1. Reasoning `<think>` stripped from answers.

⚠ groq/compound[-mini] are agentic (may use tools/web), not pure grounded Q&A.


====================================================================================================
## [1] CORE · mp=OFF · ctx 2265 tok

**Q:** If a Battle-shocked unit that is below half-strength Falls Back, what tests does it take and can it still shoot or charge that turn?

**Expected concepts (ground-truth anchors):** [['desperate escape', 'fall back'], ['battle-shock'], ['half-strength']]

<details><summary>rules context sent to every model</summary>

```
[1] 2. Battle-shock ()
# 2. Battle-shock
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In this step, you must take a Battle-shock test for each of your units on the battlefield that is Below Half-strength. To do so, roll 2D6: if the result is greater than or equal to the best Leadership characteristic in that unit, the test is passed; otherwise, the test is failed and, until the start of your next Command phase, that unit is Battle-shocked. While a unit is Battle-shocked:
- The Objective Control characteristic of all of its models is 0.
- If it Falls Back, you must take a Desperate Escape test for every model in that unit.
- Its controlling player cannot use Stratagems to affect that unit.
Once you have taken Battle-shock tests for all of your units that require them, your Command phase ends and you progress to your Movement phase. In this step, if for any reason a unit is forced to take a Battle-shock test for being below its Starting Strength, unless otherwise stated, that unit does not also have to take a Battle-shock test for being Below Half-strength. While a unit is Battle-shocked, all models in that unit are also Battle-shocked.
Take a Battle-shock test for each unit from your army on the battlefield that is Below Half-strength. Roll 2D6: if the result is greater than or equal to the unit's Leadership, the test is passed. Otherwise, the unit is Battle-shocked until the start of your next Command phase. Battle-shocked units have an OC of 0 and their controlling player cannot use Stratagems to affect them. Battle-shocked units must take Desperate Escape tests if they Fall Back.

---

[2] Fall Back Moves ()
# Fall Back Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Falls Back, each model in that unit can make a Fall Back move by moving a distance in inches less than or equal to its Move characteristic, and when doing so you can move it within Engagement Range of enemy models, provided it does not end that move within Engagement Range of any enemy models - if this is not possible, that unit cannot Fall Back. A unit cannot shoot or declare a charge in the same turn that it Fell Back. Desperate Escape Tests Unlike when making other types of move, models can move over enemy models when making a Fall Back move as if those enemy models were not there, but you must take a Desperate Escape test for each model that will do so (excluding models that are TITANIC or can FLY) before any models in that unit are moved. In addition, if a unit is Battle-shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved. Each time you take a Desperate Escape test for a model, roll one D6. For each roll of 1-2, one model from the unit that is Falling Back is destroyed (selected by you). The same model can only ever trigger one Desperate Escape test per phase. Fall Back Move: Models move up to M". Units that Fall Back cannot shoot or declare a charge in the same turn. Models can move over enemy models when Falling Back, but you must take Desperate Escape tests for them before they do so (excluding models that are TITANIC or can FLY). If a Battle-shocked unit is selected to Fall Back, take a Desperate Escape test for every model in that unit. Desperate Escape Test: Roll one D6. On a 1-2, one model from that unit is destroyed. A The Sternguard Veterans are selected to make a Fall Back move, but to do so they must move through enemy models, so Desperate Escape tests are required. B The controlling player rolls one D6 for each model that moves through an enemy unit, resulting in a 1, 2, 4, 4 and 6. Two models are therefore destroyed.

---

[3] CHARGE PHASE ()
# CHARGE PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Use the following sequence to charge with your units.
1. SELECT ELIGIBLE UNIT
2. SELECT TARGETS
3. MAKE CHARGE ROLL
4. MAKE CHARGE MOVE
5. REPEAT FOR NEXT ELIGIBLE UNIT
In your Charge phase, if you have any eligible units from your army on the battlefield that you want to charge into close combat, you can select those units, one at a time, to declare a charge. Each can only be selected once per phase. Once all of these charges (if any) have been resolved, progress to the Fight phase. A unit is eligible to charge if it is within 12" of one or more enemy units in your Charge phase, unless any of the following apply:
- That unit Advanced or Fell Back this turn.
- That unit is within Engagement Range of any enemy models.
- That unit is an AIRCRAFT unit.
Warriors hurl themselves into battle to slay with blade, hammer and claw. Strident war cries and frantic screams echo through the whirling smoke as the moment of cataclysmic violence draws near.

---

[4] Below Half-strength ()
# Below Half-strength
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some rules will refer to a unit being Below Half-strength.
- If a unit has a Starting Strength of 1, then it is said to be Below Half-strength while its remaining number of wounds is less than half of its Wounds characteristic.
- For any other unit, while the number of models in that unit is less than half of its Starting Strength, that unit is said to be Below Half-strength.

---

[5] Gaining Command Points ()
# Gaining Command Points
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Outside of the 1CP players gain at the start of the Command phase, each player can only gain a total of 1CP per battle round, regardless of the source (this includes other CP gained at the start of the Command phase). Starting Strength The number of models a unit contains when it is added to your army is known as its Starting Strength. Below Half-strength Some rules will refer to a unit being Below Half-strength. If a unit has a Starting Strength of 1, then it is said to be Below Half-strength while its remaining number of wounds is less than half of its Wounds characteristic. For any other unit, while the number of models in that unit is less than half of its Starting Strength, that unit is said to be Below Half-strength. Destroyed Throughout a battle, models will suffer damage and be destroyed. When a model is destroyed, it is removed from the battlefield. When every model in a unit has been destroyed, that unit is destroyed. Attached Units Some CHARACTER units have the Leader ability, which lets them merge with other units (known as Bodyguard units) to form an Attached unit. The Starting Strength of an Attached unit is equal to the combined Starting Strengths of all of its units (i.e. the number of models in the Leader unit added to the number of models in the Bodyguard unit). If either the Leader unit or the Bodyguard unit in an Attached unit is destroyed, the Starting Strength of the remaining unit is changed to be equal to its original Starting Strength. Example: A Primaris Captain (Starting Strength 1) is attached to a unit of Intercessors (Starting Strength 5). This Attached unit has a Starting Strength of 6. If all the Intercessors are destroyed, the remaining Primaris Captain would revert to having a Starting Strength of 1. For the purposes of rules that are triggered when a unit is destroyed, such rules are still triggered when one of the individual units that made up an Attached unit is destroyed (the Leader or the Bodyguard unit). Example: If a rule awards you with 1VP each time an enemy unit is destroyed, and you target an Attached unit, you would gain 1VP if the Bodyguard unit is destroyed and 1VP if the Leader unit is destroyed (for a total of 2VP).

---

[6] COMMAND PHASE ()
# COMMAND PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Your Command phase is split into two steps. In the first, both players gain 1 Command point (CP) and you resolve any other Command phase rules; in the second, you test to see if any of your units are Battle-shocked.
1. COMMAND
2. BATTLE-SHOCK
Commanders gauge the flow of the battle, consolidating their objectives b
```
</details>


### qwen/qwen3-32b
`finish=stop · 746 compl tok · 2.3s`

[Ruling]  
A Battle-shocked unit that Falls Back must take **Desperate Escape tests for every model in the unit** (due to being Battle-shocked). Additionally, the unit **cannot shoot or declare a charge in the same turn** because it Fell Back.  

[Rule Citations]  
- **Desperate Escape tests**: [2] *Fall Back Moves* → "If a unit is Battle-shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved."  
- **Restrictions on shooting/charging**: [2] *Fall Back Moves* → "Units that Fall Back cannot shoot or declare a charge in the same turn."  

[Reasoning]  
The unit’s Battle-shocked status triggers the mandatory Desperate Escape tests for all models during the Fall Back move (per [2]). Falling Back itself independently prohibits shooting or charging (per [2] and [3] *Charge Phase*), regardless of Battle-shocked status. No additional tests are required beyond the Desperate Escape tests, as the unit’s Below Half-strength status only triggered the initial Battle-shock test (resolved in the Command phase, per [1]).

### qwen/qwen3.6-27b
`finish=stop · 1794 compl tok · 4.3s`

[Ruling] The unit must take a Desperate Escape test for every model in the unit before any models are moved, and it cannot shoot or declare a charge in the same turn.

[Rule Citation] Fall Back Moves (Wahapedia_Core_Rules) & Battle-shock (Wahapedia_Core_Rules)

[Reasoning] The Fall Back Moves rule explicitly states that "if a unit is Battle-shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved." It further specifies that "A unit cannot shoot or declare a charge in the same turn that it Fell Back." The Battle-shock rule corroborates this by noting that if a Battle-shocked unit Falls Back, "you must take a Desperate Escape test for every model in that unit." The Below Half-strength condition does not impose any additional tests or restrictions on Falling Back, shooting, or charging beyond those already stated in the provided rules.

### llama-3.3-70b-versatile
`finish=stop · 226 compl tok · 1.7s`

[Ruling] → [Rule Citation] → [Reasoning]

A Battle-shocked unit that Falls Back must take Desperate Escape tests for every model in that unit, as stated in the "Fall Back Moves" rule (**Source:** Wahapedia_Core_Rules). Additionally, since the unit is Battle-shocked, its Objective Control characteristic is 0, and its controlling player cannot use Stratagems to affect that unit, as stated in the "Battle-shock" rule (**Source:** Wahapedia_Core_Rules).

According to the "Fall Back Moves" rule, a unit that Falls Back cannot shoot or declare a charge in the same turn. Therefore, the Battle-shocked unit that Falls Back cannot shoot or charge that turn.

To summarize:

- The unit must take Desperate Escape tests for every model in that unit (**Fall Back Moves** rule).
- The unit's Objective Control characteristic is 0, and its controlling player cannot use Stratagems to affect that unit (**Battle-shock** rule).
- The unit cannot shoot or declare a charge in the same turn (**Fall Back Moves** rule).

### llama-3.1-8b-instant
`finish=stop · 91 compl tok · 1.3s`

[Ruling] → [2. Fall Back Moves] → [Reasoning]

A Battle-shocked unit that is below half-strength must take a Desperate Escape test for every model in that unit before any are moved when it Falls Back. 

According to [2. Fall Back Moves], a unit cannot shoot or declare a charge in the same turn that it Fell Back. Therefore, the Battle-shocked unit cannot shoot or charge that turn.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 215 compl tok · 1.8s`

[Ruling] → A Battle-shocked unit that is below half-strength and Falls Back must take a Desperate Escape test for every model in that unit. 

→ [Battle-shock] → A unit that is Battle-shocked has its Objective Control characteristic set to 0 and its controlling player cannot use Stratagems to affect that unit.

→ [Fall Back Moves] → When a unit Falls Back, it cannot shoot or declare a charge in the same turn that it Fell Back.

→ [Reasoning] The provided rules state that a Battle-shocked unit has specific restrictions, including not being able to be affected by Stratagems and having an Objective Control characteristic of 0. When such a unit Falls Back, it must take a Desperate Escape test for every model. Additionally, a unit that Falls Back cannot shoot or declare a charge in the same turn. 

Therefore, a Battle-shocked unit that is below half-strength and Falls Back must take Desperate Escape tests for all its models and cannot shoot or declare a charge that turn.

### openai/gpt-oss-120b
`finish=stop · 715 compl tok · 2.5s`

**Ruling**  
When a Battle‑shocked unit that is Below Half‑strength is selected to Fall Back, you must take a Desperate Escape test for every model in that unit. After it Falls Back, the unit may not shoot or declare a charge in the same turn.

**Rule Citations**  
- **Battle‑shock** – “If it Falls Back, you must take a Desperate Escape test for every model in that unit.” (Rule 2)  
- **Fall Back Moves** – “A unit cannot shoot or declare a charge in the same turn that it Fell Back.” (Rule 2)  
- **Fall Back Moves** – “If a unit is Battle‑shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved.” (Rule 2)

**Reasoning**  
The Battle‑shock rule explicitly adds a requirement that any Battle‑shocked unit taking a Fall Back must roll a Desperate Escape test for each of its models. The Fall Back Moves rule also repeats this requirement for Battle‑shocked units, confirming that the same test applies (no additional or different test is required).  

The Fall Back Moves rule further states that a unit which has Fallen Back cannot shoot or declare a charge in that turn, regardless of its Battle‑shocked status. Therefore, after the unit completes its Fall Back (and any required Desperate Escape tests), it is prohibited from shooting or charging for the remainder of the turn.

### openai/gpt-oss-20b
`finish=stop · 866 compl tok · 1.9s`

**Ruling**  
A Battle‑shocked unit that falls back must take a Desperate Escape test for every model in that unit before any of them move, and it may not shoot or declare a charge during that turn.

**Rule Citations**  
1. **Fall Back Moves** – “When a unit Falls Back … you must take a Desperate Escape test for every model in that unit before any are moved.” (Rule 2)  
2. **Fall Back Moves** – “A unit cannot shoot or declare a charge in the same turn that it Fell Back.” (Rule 2)  
3. **Battle‑shock** – “If it Falls Back, you must take a Desperate Escape test for every model in that unit.” (Rule 1)

**Reasoning**  
- The Fall Back Moves rule explicitly requires a Desperate Escape test for each model when a unit falls back, and it also prohibits shooting or charging in the same turn.  
- The Battle‑shock rule reinforces that a Battle‑shocked unit must also take Desperate Escape tests when falling back.  
- No other rule in the provided context overrides or modifies these requirements. Therefore, the unit must perform the Desperate Escape tests and is barred from shooting or charging that turn.

### allam-2-7b
`finish=stop · 1090 compl tok · 1.1s`






































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































====================================================================================================
## [2] CORE · mp=OFF · ctx 2715 tok

**Q:** If I set up a unit using Deep Strike from Strategic Reserves, how far from enemy models must it arrive and can it charge that same turn?

**Expected concepts (ground-truth anchors):** [['deep strike'], ['strategic reserve']]

<details><summary>rules context sent to every model</summary>

```
[1] Deployment Abilities ()
# Deployment Abilities — Deep Strike
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

DEEP STRIKE Some units make their way to battle via tunnelling, teleportation, high-altitude descent or other extraordinary means that allow them to appear suddenly in the thick of the fighting. During the Declare Battle Formations step, if every model in a unit has this ability, you can set it up in Reserves instead of setting it up on the battlefield. If you do, in the Reinforcements step of one of your Movement phases you can set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models. If a unit with the Deep Strike ability arrives from Strategic Reserves, the controlling player can choose for that unit to be set up either using the rules for Strategic Reserves or using the Deep Strike ability. Unit can be set up in Reserves instead of on the battlefield. Unit can be set up in your Reinforcements step, more than 9" horizontally away from all enemy models.

---

[2] Advance Moves ()
# Advance Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Advances, make an Advance roll for that unit by rolling one D6. Add the result in inches to the Move characteristic of each model in that unit until the end of the phase. Each model in that unit can then make an Advance move by moving a distance in inches less than or equal to this total, but no model can be moved within Engagement Range of enemy models. A unit cannot shoot or declare a charge in the same turn that it Advanced.
Advance Move: Models move up to M+D6". Cannot move within Engagement Range of any enemy models. Units that Advance cannot shoot or charge this turn.

---

[3] Fall Back Moves ()
# Fall Back Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Falls Back, each model in that unit can make a Fall Back move by moving a distance in inches less than or equal to its Move characteristic, and when doing so you can move it within Engagement Range of enemy models, provided it does not end that move within Engagement Range of any enemy models - if this is not possible, that unit cannot Fall Back. A unit cannot shoot or declare a charge in the same turn that it Fell Back. Desperate Escape Tests Unlike when making other types of move, models can move over enemy models when making a Fall Back move as if those enemy models were not there, but you must take a Desperate Escape test for each model that will do so (excluding models that are TITANIC or can FLY) before any models in that unit are moved. In addition, if a unit is Battle-shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved. Each time you take a Desperate Escape test for a model, roll one D6. For each roll of 1-2, one model from the unit that is Falling Back is destroyed (selected by you). The same model can only ever trigger one Desperate Escape test per phase. Fall Back Move: Models move up to M". Units that Fall Back cannot shoot or declare a charge in the same turn. Models can move over enemy models when Falling Back, but you must take Desperate Escape tests for them before they do so (excluding models that are TITANIC or can FLY). If a Battle-shocked unit is selected to Fall Back, take a Desperate Escape test for every model in that unit. Desperate Escape Test: Roll one D6. On a 1-2, one model from that unit is destroyed. A The Sternguard Veterans are selected to make a Fall Back move, but to do so they must move through enemy models, so Desperate Escape tests are required. B The controlling player rolls one D6 for each model that moves through an enemy unit, resulting in a 1, 2, 4, 4 and 6. Two models are therefore destroyed.

---

[4] Charging with a Unit ()
# Charging with a Unit
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Once you have selected an eligible unit to declare a charge, you must select one or more enemy units within 12" of it as the targets of that charge. The targets of a charge do not need to be visible to the charging unit. You then make a Charge roll for the charging unit by rolling 2D6. The result is the maximum number of inches each model in that unit can be moved if a Charge move is possible. For a Charge move to be possible, the Charge roll must be sufficient to enable the charging unit to end that move:
- Within Engagement Range of every unit that you selected as a target of the charge.
- Without moving within Engagement Range of any enemy units that were not a target of the charge.
- In Unit Coherency.
If any of these conditions cannot be met, the charge fails and no models in the charging unit move this phase. Otherwise, the charge is successful and the models in the charging unit make a Charge move - move each model a distance in inches up to the result of the Charge roll. When doing so, each model in the charging unit must end its Charge move closer to one of the units selected as a target of its charge. If you can also move a charging model so that it ends its Charge move in base-to-base contact with one or more enemy models while still enabling the charging unit to end its move satisfying all of the conditions above, you must do so. The controlling player chooses the order in which to move their models.
Charge Roll: 2D6". Targets of a charge must be within 12" but do not need to be visible. If the distance rolled is insufficient to move within Engagement Range of all targets while maintaining Unit Coherency, the charge fails. Cannot move within Engagement Range of any unit that was not a target of the charge. If the charge is successful, each model makes a Charge move less than or equal to the Charge roll, and must move into base-to-base contact with an enemy model if possible.

---

[5] 2. Reinforcements ()
# 2. Reinforcements
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some units have a rule that allows them to start the battle in Reserves, such as Deep Strike. Such units will arrive later in the battle and are known as Reserves units. Any Reserves units that have not been set up on the battlefield when the battle ends count as having been destroyed. In the Reinforcements step of your Movement phase, if you have any Reserves units in your army, you can select one or more of them and set them up on the battlefield, one at a time. Once all your Reserves units that you wish to set up this turn have been set up, your Movement phase ends and you progress to your Shooting phase. Details of how to set up Reserves units are described in the same rules that enabled the unit to be set up in Reserves. These rules will typically specify a distance away from all enemy models; whenever such a distance is specified, it always applies to the horizontal distance, even though normally you measure to and from the closest part of a model's base. Reserves units always count as having made a Normal move in the turn they are set up on the battlefield, and so cannot move further during this phase. Otherwise, units set up in this way can act normally this turn (shoot, declare a charge, fight, etc.).
Reserves Unit: A unit that starts the battle in a location other than the battlefield. Always count as having made a Normal move in the turn they are set up on the battlefield. Any specified distance from enemy models applies to horizontal distance. Any Reserves unit not set up on the battlefield by the end of the battle counts as destroyed.

---

[6] Setting Up Strategic Reserve Units ()
# Setting Up Strategic Reserve Units
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Where on the battlefield a Strategic Reserves unit can be set up when it arrives depends on the battle round, as follows:
- During the second battle round, Strategic Reserves units that arrive must be set up wholly within 6" of any battlefield edge, but no model in those units can be set up within the enemy depl
```
</details>


### qwen/qwen3-32b
`finish=stop · 953 compl tok · 2.5s`

[Ruling]  
The unit must be set up more than 9" horizontally from all enemy models. It can charge in the same turn it arrives.  

[Rule Citations]  
- **Distance from enemies:** [1] Deployment Abilities — Deep Strike ("more than 9" horizontally away from all enemy models").  
- **Charge eligibility:** [5] 2. Reinforcements ("Reserves units always count as having made a Normal move in the turn they are set up on the battlefield, and so cannot move further during this phase. Otherwise, units set up in this way can act normally this turn (shoot, declare a charge, etc.)").  

[Reasoning]  
Deep Strike allows setup more than 9" from enemies ([1]). While arriving via Reserves counts as a Normal move ([5]), this does not restrict the unit from declaring a charge in the same turn (unlike Advance or Fall Back moves, which explicitly prohibit charging [2][3]). The unit can charge if it meets all charge conditions (e.g., targets within 12", sufficient movement, etc.).

### qwen/qwen3.6-27b
`finish=stop · 1875 compl tok · 23.2s`

[Ruling] The unit must be set up more than 9" horizontally away from all enemy models, and yes, it can declare a charge in the same turn it arrives.

[Rule Citation] Deep Strike (Wahapedia_Core_Rules), Reinforcements (Wahapedia_Core_Rules), Strategic Reserves (Wahapedia_Core_Rules)

[Reasoning] The Deep Strike rule explicitly states that when using the Deep Strike ability to set up a unit, it must be placed "more than 9" horizontally away from all enemy models." The Strategic Reserves rule reinforces this, noting that "Strategic Reserves units cannot be set up within 9" horizontally of any enemy models." Regarding post-setup actions, the Reinforcements rule clarifies that "Reserves units always count as having made a Normal move in the turn they are set up on the battlefield, and so cannot move further during this phase. Otherwise, units set up in this way can act normally this turn (shoot, declare a charge, fight, etc.)." Since Deep Strike units are classified as Reserves units, they count as having made a Normal move upon arrival but retain full permission to declare a charge that same turn.

### llama-3.3-70b-versatile
`finish=stop · 260 compl tok · 44.4s`

[Ruling] → [Rule Citation] → [Reasoning]

A unit set up using Deep Strike from Strategic Reserves must arrive more than 9" horizontally away from all enemy models, as stated in the Deep Strike ability (**[1] Deployment Abilities — Deep Strike**). 

Regarding charging, according to **[5] 2. Reinforcements**, units set up in Reserves, including those using Deep Strike, count as having made a Normal move in the turn they are set up on the battlefield. However, it does not explicitly state they cannot declare a charge. But, considering **[4] Charging with a Unit**, which does not restrict charging based on the type of move made previously (Normal, Advance, etc.) but rather on the unit's current state (e.g., not having Advanced or Fallen Back), and given that a unit set up via Deep Strike has not Advanced or Fallen Back but has made a Normal move, it should be eligible to charge.

Therefore, a unit set up using Deep Strike from Strategic Reserves can potentially charge in the same turn it arrives, provided it meets the conditions for declaring a charge as outlined in **[4] Charging with a Unit**, such as being within 12" of an enemy unit and successfully making a Charge roll.

### llama-3.1-8b-instant
`finish=stop · 227 compl tok · 16.3s`

[Ruling] → [Rule Citation] → [Reasoning]

A unit set up using Deep Strike from Strategic Reserves can be set up anywhere on the battlefield that is more than 9" horizontally away from all enemy models.

→ [Rule Citation: Deep Strike, #1] → [Reasoning]
The Deep Strike ability allows a unit to be set up in Reserves instead of on the battlefield, and in the Reinforcements step of one of your Movement phases, you can set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models.

A unit set up using Deep Strike from Strategic Reserves can charge the same turn.

→ [Rule Citation: Reinforcements, #5] → [Reasoning]
Reserves units always count as having made a Normal move in the turn they are set up on the battlefield, and so cannot move further during this phase. However, they can act normally this turn (shoot, declare a charge, fight, etc.). Since the unit has already made a Normal move by being set up, it can declare a charge in the same turn.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 246 compl tok · 1.4s`

[Ruling] → A unit setting up using Deep Strike from Strategic Reserves must be set up more than 9" horizontally away from all enemy models. It counts as having made a Normal move in the turn it is set up on the battlefield and can act normally this turn, which includes declaring a charge.

→ [Deep Strike, Wahapedia_Core_Rules] → The unit can be set up in Reserves instead of on the battlefield. Unit can be set up in your Reinforcements step, more than 9" horizontally away from all enemy models.

→ [Reserves, Wahapedia_Core_Rules] → Reserves units always count as having made a Normal move in the turn they are set up on the battlefield, and so can move further during this phase, shoot, declare a charge, fight, etc.

→ [5. 2. Reinforcements, Wahapedia_Core_Rules] → Details of how to set up Reserves units are described in the same rules that enabled the unit to be set up in Reserves. 

Note that the specific distance requirement for Strategic Reserves units (6" of a battlefield edge) does not apply when using Deep Strike, as Deep Strike provides its own setup rules.

### openai/gpt-oss-120b
`finish=stop · 949 compl tok · 13.6s`

**Ruling**  
When you bring a Deep‑Strike unit onto the battlefield from Strategic Reserves you must set it up **more than 9 inches horizontally away from all enemy models**, and the unit **may declare a charge in the same turn it arrives**.

**Rule Citations**  

1. **Deep Strike** – “If a unit with the Deep Strike ability arrives from Strategic Reserves, the controlling player can choose for that unit to be set up either using the rules for Strategic Reserves or using the Deep Strike ability. … you can set up this unit anywhere on the battlefield that is **more than 9" horizontally away from all enemy models**.” [Source: Deep Strike, Wahapedia_Core_Rules]  

2. **Reserves Units (Reinforcements)** – “Reserves units always count as having made a **Normal move** in the turn they are set up on the battlefield, and so **cannot move further during this phase**. **Otherwise, units set up in this way can act normally this turn (shoot, declare a charge, fight, etc.)**.” [Source: 2. Reinforcements, Wahapedia_Core_Rules]

**Reasoning**  

- Because you elect to use the Deep‑Strike option when the unit arrives from Strategic Reserves, the placement rule from Deep Strike applies, requiring the unit to be placed **more than 9 inches** away (horizontal measurement) from every enemy model. This satisfies the distance requirement; the separate Strategic‑Reserves placement restrictions are not used in this case.  

- Upon arrival, the unit is treated as a Reserves unit that has just been set up. By rule 2, it is considered to have already made its Normal move for the phase, so it cannot move again (i.e., it cannot Advance, Fall Back, or make another Normal move). However, the same rule explicitly states that such a unit may still **shoot, declare a charge, fight, etc.,** in that turn. Therefore, the Deep‑Strike unit may declare and resolve a charge immediately after being set up.

### openai/gpt-oss-20b
`finish=stop · 1016 compl tok · 13.2s`

**Ruling**  
If you set up a unit using Deep Strike from Strategic Reserves, you must place it more than 9 inches horizontally away from all enemy models, and the unit cannot charge during that same movement phase.

**Rule Citations**  
1. **Deep Strike** – “If you do, in the Reinforcements step of one of your Movement phases you can set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models.” (Rule 1)  
2. **Reserves Unit** – “Reserves units always count as having made a Normal move in the turn they are set up on the battlefield, and so cannot move further during this phase.” (Rule 5)  
3. **Charging** – Charging is a type of move (a Charge move). (Rule 4)

**Reasoning**  
- The Deep Strike ability gives the specific distance requirement of “more than 9" horizontally away from all enemy models” when the unit is set up in the Reinforcements step.  
- When a unit is set up from Reserves (including Deep Strike), the Reserves Unit rule states that it counts as having made a Normal move that turn and “cannot move further during this phase.”  
- Charging is a move action; therefore, because the unit has already made a Normal move by being set up, it is not allowed to move further, which includes charging, during that same movement phase.

### allam-2-7b
`finish=stop · 794 compl tok · 51.0s`






























































































































































































































































































































































































































































































































































































































































































































































































































====================================================================================================
## [3] CORE · mp=OFF · ctx 2307 tok

**Q:** When my unit makes a charge move over a barricade, can it end in Engagement Range with an enemy on the floor above, and does the barricade affect the move?

**Expected concepts (ground-truth anchors):** [['barricade'], ['engagement range']]

<details><summary>rules context sent to every model</summary>

```
[1] Barricades and Fuel Pipes ()
# Barricades and Fuel Pipes
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Fuel pipes and purpose-made defence lines are excellent positions from which to repel the enemy. MOVEMENT Models can move up, over and down this terrain feature, but they cannot be set up or end any kind of move on top of it. VISIBILITY Normal visibility rules apply. ENGAGEMENT RANGE In the Charge phase, if an enemy unit is within 1" of this terrain feature, a charging unit on the opposite side of this terrain feature can still make a Charge move against that enemy unit provided it ends that Charge move as close as possible to this terrain feature and within 2" of that enemy unit. In the Fight phase, units are eligible to fight - and models can make attacks - if their target is on the opposite side of this terrain feature and within 2" of them. BENEFIT OF COVER Each time a ranged attack is allocated to an INFANTRY model that is wholly within 3" of this terrain feature, if that model is not fully visible to every model in the attacking unit because of this terrain feature, that model has the Benefit of Cover against that attack. KEYWORDS: OBSTACLE, BARRICADE

---

[2] Engagement Range ()
# Engagement Range
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Engagement Range represents the zone of threat that models present to their enemies. While a model is within 1" horizontally and 5" vertically of an enemy model, those models - and their units - are within Engagement Range of each other. Models cannot be set up or end a Normal, Advance or Fall Back move within Engagement Range of any enemy models. If for any reason a model cannot meet this condition, that model is destroyed. Engagement Range: Within 1" horizontally and 5" vertically. Models cannot be set up or end a Normal, Advance or Fall Back move within Engagement Range of any enemy models.

---

[3] Advance Moves ()
# Advance Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Advances, make an Advance roll for that unit by rolling one D6. Add the result in inches to the Move characteristic of each model in that unit until the end of the phase. Each model in that unit can then make an Advance move by moving a distance in inches less than or equal to this total, but no model can be moved within Engagement Range of enemy models. A unit cannot shoot or declare a charge in the same turn that it Advanced.
Advance Move: Models move up to M+D6". Cannot move within Engagement Range of any enemy models. Units that Advance cannot shoot or charge this turn.

---

[4] Charging with a Unit ()
# Charging with a Unit
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Once you have selected an eligible unit to declare a charge, you must select one or more enemy units within 12" of it as the targets of that charge. The targets of a charge do not need to be visible to the charging unit. You then make a Charge roll for the charging unit by rolling 2D6. The result is the maximum number of inches each model in that unit can be moved if a Charge move is possible. For a Charge move to be possible, the Charge roll must be sufficient to enable the charging unit to end that move:
- Within Engagement Range of every unit that you selected as a target of the charge.
- Without moving within Engagement Range of any enemy units that were not a target of the charge.
- In Unit Coherency.
If any of these conditions cannot be met, the charge fails and no models in the charging unit move this phase. Otherwise, the charge is successful and the models in the charging unit make a Charge move - move each model a distance in inches up to the result of the Charge roll. When doing so, each model in the charging unit must end its Charge move closer to one of the units selected as a target of its charge. If you can also move a charging model so that it ends its Charge move in base-to-base contact with one or more enemy models while still enabling the charging unit to end its move satisfying all of the conditions above, you must do so. The controlling player chooses the order in which to move their models.
Charge Roll: 2D6". Targets of a charge must be within 12" but do not need to be visible. If the distance rolled is insufficient to move within Engagement Range of all targets while maintaining Unit Coherency, the charge fails. Cannot move within Engagement Range of any unit that was not a target of the charge. If the charge is successful, each model makes a Charge move less than or equal to the Charge roll, and must move into base-to-base contact with an enemy model if possible.

---

[5] 1. Pile In ()
# 1. Pile In
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Piles In, you can move each model in that unit that is not already in base-to-base contact with an enemy model up to 3" - this is a Pile-in move. For a Pile In to be possible, a unit must be able to end these moves within Engagement Range of one or more enemy units and in Unit Coherency. If these conditions cannot be met, no models in the unit can make Pile-in moves this phase and you progress to making melee attacks with that unit. Otherwise, the unit can make Pile-in moves. Each time a model makes a Pile-in move, it must end that move closer to the closest enemy model. If it can also end that move in base-to-base contact with one or more enemy models while still satisfying all of the conditions above, it must do so. The controlling player chooses the order in which to move their models.
Pile-in Move: Up to 3". Every model that moves must end closer to the closest enemy model, and in base-to-base contact with an enemy model if possible. The unit must end in Unit Coherency and within Engagement Range of at least one enemy unit (or no models can Pile In).

---

[6] Aircraft in the Charge and Fight Phases ()
# Aircraft in the Charge and Fight Phases
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

AIRCRAFT units cannot declare a charge, and only units that can FLY can select an AIRCRAFT unit as a target of their charge. Such units can end their Charge move within Engagement Range of one or more enemy AIRCRAFT units. An AIRCRAFT model is only eligible to fight if it is within Engagement Range of one or more enemy units that can FLY, and it can only make melee attacks against units that can FLY. Only models that can FLY can make melee attacks against AIRCRAFT units. AIRCRAFT models cannot make Pile-in or Consolidation moves. Each time a model makes a Pile-in or Consolidation move, unless that model can FLY, AIRCRAFT models are ignored for the purposes of moving closer to the closest enemy model.
Only units that can FLY can charge at or make melee attacks against AIRCRAFT. AIRCRAFT cannot charge, Pile In or Consolidate, and can only make melee attacks against units that can FLY. When a model Piles In or Consolidates, unless it can FLY, ignore AIRCRAFT when determining the closest enemy model.

---

[7] Flying ()
# Flying
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a model can FLY, then when it makes a Normal, Advance or Fall Back move, it can be moved over enemy models as if they were not there, and can be moved within Engagement Range of enemy models when making such a move. Note this also means that MONSTER and VEHICLE models that can FLY can be moved over other MONSTER and VEHICLE models when making such a move. However, models that can FLY cannot end their move on top of any other models or within Engagement Range of any enemy models. When a model that can FLY starts or ends a move on a terrain feature, instead of measuring the path it has moved across the battlefield, you instead measure its path 'through the air', as shown in the diagram below. FLY models can move over enemy models when they make a Normal, Advance or Fall Back move. FLY models that start or end a move on a terrain feature measure distance moved through the air when they make a
```
</details>


### qwen/qwen3-32b
`finish=stop · 711 compl tok · 1.9s`

[Ruling] Yes, a unit can make a Charge move over a Barricade and end within Engagement Range of an enemy unit on a higher floor, provided the vertical distance between the units is ≤5". The Barricade does not block the Charge move itself but must be crossed as part of the movement.  
**Rule Citation**: [1] Barricades and Fuel Pipes → Charge phase clause; [2] Engagement Range → Vertical distance clause; [4] Charging with a Unit → Charge move conditions.  
**Reasoning**:  
1. **Barricade Interaction**: Barricades allow models to move over them (not end on them). During the Charge phase, a charging unit can cross a Barricade to reach an enemy on the opposite side, even if that enemy is elevated (e.g., on a higher floor). The Barricade does not block Engagement Range for Charge purposes if the target is on the opposite side.  
2. **Engagement Range**: Engagement Range is defined as ≤1" horizontally and ≤5" vertically. If the enemy is on a higher floor but within 5" vertical distance, the charging unit can end its Charge move in Engagement Range.  
3. **Charge Conditions**: The Charge must end within Engagement Range of the target(s) and maintain Unit Coherency. The Barricade does not prevent this as long as the vertical distance is valid.  

No rule in the context prohibits crossing a Barricade during a Charge move, and vertical Engagement Range is explicitly allowed.

### qwen/qwen3.6-27b
`finish=stop · 2971 compl tok · 23.2s`

[Ruling] The barricade affects the move by allowing models to move up, over, and down it, but you cannot end the charge move on top of it. Regarding whether the unit can end in Engagement Range with an enemy on a floor above, the provided rules do not clearly address this — I recommend checking the official GW FAQ.

[Rule Citation] Barricades and Fuel Pipes (Movement & Engagement Range), Charging with a Unit, Engagement Range

[Reasoning] The Barricades and Fuel Pipes rule explicitly states that models "can move up, over and down this terrain feature, but they cannot be set up or end any kind of move on top of it." The specific charge exception for barricades only applies to enemies on the "opposite side" of the barricade, allowing the charging unit to end "as close as possible to this terrain feature and within 2" of that enemy unit." While general charge rules require ending within Engagement Range (defined as 1" horizontally and 5" vertically), the provided context contains no specific rules governing vertical charging to a different floor level or how barricades interact with such vertical charges. Therefore, I cannot definitively rule on the floor-above scenario based solely on the provided text.

### llama-3.3-70b-versatile
`finish=stop · 345 compl tok · 43.2s`

[Ruling] → [Rule Citation] → [Reasoning]

[Ruling]: Yes, a unit can end a Charge move in Engagement Range with an enemy on the floor above when moving over a barricade, and the barricade does affect the move in terms of Engagement Range and visibility.

[Rule Citation]: Barricades and Fuel Pipes (1), Engagement Range (2), Charging with a Unit (4)

[Reasoning]: According to Barricades and Fuel Pipes (1), in the Charge phase, if an enemy unit is within 1" of this terrain feature, a charging unit on the opposite side of this terrain feature can still make a Charge move against that enemy unit provided it ends that Charge move as close as possible to this terrain feature and within 2" of that enemy unit. This implies that the barricade does not block the charge move but does influence how the charge can be resolved in terms of proximity to the barricade and the enemy. Engagement Range (2) defines the zone of threat but does not override the specific rule for barricades in the context of charging. Charging with a Unit (4) outlines the conditions for a successful charge, including ending the move within Engagement Range of the target unit, which can be satisfied when moving over a barricade according to the specific rules for barricades. 

Therefore, when making a Charge move over a barricade, the unit can indeed end in Engagement Range with an enemy on the floor above, considering the barricade's effect as outlined in the Barricades and Fuel Pipes rule. The move is still subject to the conditions of a successful charge as defined in Charging with a Unit, adapted by the specific conditions related to barricades.

### llama-3.1-8b-instant
`finish=stop · 326 compl tok · 2.0s`

[Ruling] → [Rule Citation] → [Reasoning]

The unit can make a charge move over the barricade, but it cannot end its move on top of the barricade. → [Rule Citation: Barricades and Fuel Pipes, Core_Rules, Wahapedia_Core_Rules] → [Reasoning] The barricade states that models can move up, over, and down this terrain feature, but they cannot be set up or end any kind of move on top of it.

However, the unit can end its charge move in Engagement Range with an enemy on the floor above, as long as the enemy is within 2" of the barricade and the unit ends its move as close as possible to the barricade. → [Rule Citation: Barricades and Fuel Pipes, Core_Rules, Wahapedia_Core_Rules] → [Reasoning] The barricade states that in the Charge phase, if an enemy unit is within 1" of this terrain feature, a charging unit on the opposite side of this terrain feature can still make a Charge move against that enemy unit provided it ends that Charge move as close as possible to this terrain feature and within 2" of that enemy unit.

The barricade does not affect the move in terms of distance, as the unit can move up to the result of the Charge roll. → [Rule Citation: Charging with a Unit, Core_Rules, Wahapedia_Core_Rules] → [Reasoning] The Charge roll determines the maximum number of inches each model in the charging unit can be moved if a Charge move is possible.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 345 compl tok · 2.6s`

[Ruling] → A unit making a Charge move can end within Engagement Range of an enemy unit on the other side of a Barricade, provided it ends the Charge move as close as possible to the Barricade and within 2" of the enemy unit. The Barricade does not affect the Charge move itself, but it does affect visibility and Engagement Range for units on opposite sides of it.

→ [Charging with a Unit] → The Charge move rules do not explicitly state that the Barricade affects the move, but [Barricades and Fuel Pipes] states that models can move up, over, and down the terrain feature.

→ [Barricades and Fuel Pipes] also states that in the Charge phase, if an enemy unit is within 1" of this terrain feature, a charging unit on the opposite side of this terrain feature can still make a Charge move against that enemy unit provided it ends that Charge move as close as possible to this terrain feature and within 2" of that enemy unit. 

However, [Engagement Range] states that models cannot be set up or end a Normal, Advance or Fall Back move within Engagement Range of any enemy models. But for Charge moves, [Charging with a Unit] allows units to end within Engagement Range of targets.

→ Additionally, [Barricades and Fuel Pipes] affects visibility and Engagement Range, stating that units are eligible to fight if their target is on the opposite side of the Barricade and within 2" of them.

The provided rules do not clearly address a multi-level scenario with a Barricade and an enemy unit on a higher level; I recommend checking the official GW FAQ.

### openai/gpt-oss-120b
`finish=stop · 887 compl tok · 2.6s`

**Ruling**  
A unit may charge over a barricade and finish the charge in Engagement Range with an enemy model that is on the floor above, provided that enemy is one of the charge’s selected targets. The barricade does not impede the charge move itself, but the charging unit may not end its move on top of the barricade.

**Rule Citations**  
1. **Barricades and Fuel Pipes** – “Models can move up, over and down this terrain feature, but they cannot be set up or end any kind of move on top of it.” (Core Rules – Wahapedia)  
2. **Charging with a Unit** – “For a Charge move to be possible, the Charge roll must be sufficient to enable the charging unit to end that move: … Within Engagement Range of every unit that you selected as a target of the charge.” (Core Rules – Wahapedia)  
3. **Engagement Range** – “Models cannot be set up or end a Normal, Advance or Fall Back move within Engagement Range of any enemy models.” (Core Rules – Wahapedia)

**Reasoning**  
- The barricade rule explicitly allows models to move **up, over and down** the feature, so a charging unit may traverse it during its charge. The only restriction is that a move cannot **end on** the barricade; ending elsewhere (e.g., on the floor above) is permitted.  
- The charge rules state that a successful charge must end **within Engagement Range of each target unit** and may not end within Engagement Range of non‑target units. There is no prohibition on ending a charge in Engagement Range; in fact, the rule requires it for the selected targets.  
- The Engagement Range rule restricts only **Normal, Advance, or Fall Back** moves from ending within Engagement Range. Since a charge is a distinct type of move, that restriction does not apply.  

Therefore, the barricade does not block or otherwise affect the charge beyond the “cannot end on it” clause, and the charging unit can legally finish the charge in Engagement Range with the enemy on the floor above, assuming that enemy was chosen as a charge target and all other charge conditions (range, unit coherency, etc.) are met.

### openai/gpt-oss-20b
`finish=stop · 2523 compl tok · 10.1s`

**Ruling**  
Yes – a charging unit can end in Engagement Range with an enemy on the floor above while moving over a barricade, and the barricade does not otherwise alter the charge move except for the requirement that the charging unit must finish as close as possible to the barricade and within 2" of the target unit.

**Rule Citations**  
1. **Barricades and Fuel Pipes** – “MOVEMENT Models can move up, over and down this terrain feature, but they cannot be set up or end any kind of move on top of it.” (Wahapedia_Core_Rules)  
2. **Barricades and Fuel Pipes** – “In the Charge phase, if an enemy unit is within 1" of this terrain feature, a charging unit on the opposite side of this terrain feature can still make a Charge move against that enemy unit provided it ends that Charge move as close as possible to this terrain feature and within 2" of that enemy unit.” (Wahapedia_Core_Rules)  
3. **Charging with a Unit** – “For a Charge move to be possible, the Charge roll must be sufficient to enable the charging unit to end that move: Within Engagement Range of every unit that you selected as a target of the charge.” (Wahapedia_Core_Rules)  
4. **Engagement Range** – “Models cannot be set up or end a Normal, Advance or Fall Back move within Engagement Range of any enemy models.” (Wahapedia_Core_Rules) – (Note: this restriction does not apply to Charge moves, which are governed by the Charging rule.)

**Reasoning**  
- The Barricades rule explicitly allows models to move over the terrain feature, so the charge move can pass over the barricade.  
- The same rule states that a charging unit may still make a charge move against an enemy within 1" of the barricade, provided it ends the move as close as possible to the barricade and within 2" of that enemy.  
- The Charging rule requires that a successful charge ends within Engagement Range of the target units, so ending in Engagement Range with an enemy on the floor above is permitted.  
- The Engagement Range rule only restricts Normal, Advance, and Fall Back moves; it does not forbid ending a Charge move within Engagement Range.  
- Therefore, the barricade does not block or otherwise modify the charge move beyond the stated proximity requirement.

### allam-2-7b
`finish=stop · 20 compl tok · 50.6s`

The provided rules do not clearly address this — I recommend checking the official GW FAQ.


====================================================================================================
## [4] CORE · mp=OFF · ctx 2517 tok

**Q:** How does Big Guns Never Tire let a Monster or Vehicle shoot while within Engagement Range, and what penalty applies to those ranged attacks?

**Expected concepts (ground-truth anchors):** [['big guns never tire'], ['engagement range']]

<details><summary>rules context sent to every model</summary>

```
[1] Big Guns Never Tire ()
# Big Guns Never Tire
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Monsters and war engines can dispense death from afar even as they trample the masses before them. MONSTER and VEHICLE units are eligible to shoot in their controlling player's Shooting phase even while they are within Engagement Range of one or more enemy units. Ranged weapons equipped by MONSTER and VEHICLE units can target one or more of the enemy units they are within Engagement Range of, even if other friendly units are also within Engagement Range of the same enemy unit. Each time a MONSTER or VEHICLE unit makes a ranged attack, if that unit was within Engagement Range of one or more enemy units when it selected its targets, unless that attack is made with a Pistol, subtract 1 from that attack's Hit roll. You can select an enemy MONSTER or VEHICLE unit within Engagement Range of one or more units from your army as a target of ranged weapons. Each time a model from your army makes a ranged attack against such a target, unless that attack is made with a Pistol, subtract 1 from that attack's Hit roll. Designer's Note: A unit that is within Engagement Range of an enemy MONSTER or VEHICLE unit is still not eligible to shoot, and so cannot make ranged attacks against that MONSTER or VEHICLE unit (unless that unit is eligible to shoot even while within Engagement Range of enemy units, e.g. it is itself a MONSTER or VEHICLE unit, or its models are equipped with Pistols). Other units from your army that are eligible to shoot can, however, target and shoot that enemy MONSTER or VEHICLE unit. MONSTERS and VEHICLES can shoot, and be shot at, even while they are within Engagement Range of enemy units. Each time a ranged attack is made by or against such a unit, subtract 1 from that attack's Hit roll (unless shooting with a Pistol).

---

[2] Make Ranged Attacks ()
# Make Ranged Attacks
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The shooting unit's models now make attacks using their ranged weapons. Each time a model shoots with a ranged weapon, it will make a number of attacks equal to the Attacks (A) characteristic in that weapon's profile. You make one Hit roll for each attack being made (see Making Attacks). If you selected more than one target for your unit to shoot at, you must resolve all of the attacks against one target before moving on to the next target. If your unit is shooting more than one ranged weapon at a target, and those weapons have different profiles, then after you have resolved attacks with one of those weapons you must, if any other weapons with the same profile are also being shot at that unit, resolve those attacks before resolving any other attacks against the target. Note that, provided at least one model in the target unit was visible to an attacking model and in range of that attacking model's weapon when that target unit was selected, that weapon's attacks can still be made, even if no models in the target unit remain visible to or in range of it when you come to resolve those attacks (for example, because models in the target unit have already been destroyed by attacks made with other weapons in the attacking model's unit).
When a model shoots a weapon, it makes a number of attacks equal to that weapon's Attacks characteristic. Resolve all attacks against one unit before resolving attacks against any other unit. Resolve all attacks made with the same weapon profile before resolving attacks with any other profile. If a weapon was in range and its target was visible when selected, that weapon's attacks can always be made.
Locked in Combat A unit is not eligible to shoot while it is within Engagement Range of one or more enemy units. While an enemy unit is within Engagement Range of one or more units from your army, you cannot select that enemy unit as a target of ranged weapons. MONSTER and VEHICLE units are exceptions to these rules, as described in the Big Guns Never Tire section. Units cannot shoot while within Engagement Range of enemy units. Units cannot shoot at targets within Engagement Range of friendly units.
STEALTH Some warriors are masters of disguise and concealment. If every model in a unit has this ability, then each time a ranged attack is made against it, subtract 1 from that attack's Hit roll.

---

[3] Pistol ()
# Pistol
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Pistols can be wielded even at point-blank range. Weapons with [PISTOL] in their profile are known as Pistols. If a unit contains any models equipped with Pistols, that unit is eligible to shoot in its controlling player's Shooting phase even while it is within Engagement Range of one or more enemy units. When such a unit is selected to shoot, it can only resolve attacks using its Pistols and can only target one of the enemy units it is within Engagement Range of. In such circumstances, a Pistol can target an enemy unit even if other friendly units are within Engagement Range of the same enemy unit. If a model is equipped with one or more Pistols, unless it is a MONSTER or VEHICLE model, it can either shoot with its Pistols or with all of its other ranged weapons. Declare whether such a model will shoot with its Pistols or its other ranged weapons before selecting targets. Can be shot even if the bearer's unit is within Engagement Range of enemy units, but must target one of those enemy units. Cannot be shot alongside any other non-Pistol weapon (except by a MONSTER or VEHICLE).

---

[4] Weapons ()
# Weapons
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Weapons are described with the following characteristics: Range: How far the weapon can shoot. Weapons with a range of 'Melee' are melee weapons and can only be used in close combat. All other weapons are ranged weapons. For ranged weapons, after all modifiers are applied, this cannot be less than 1". Attacks (A): This tells you how many attacks are made each time that weapon is used. After all modifiers are applied, this cannot be less than 1. Weapon Skill (WS): This reflects the bearer's skill in wielding the relevant melee weapon. After all modifiers are applied, this cannot be 1+ or better. Ballistic Skill (BS): This shows how accurate the bearer is when shooting with the relevant ranged weapon. After all modifiers are applied, this cannot be 1+ or better. Strength (S): How likely the weapon is to wound a foe. After all modifiers are applied, this cannot be less than 1. Armour Penetration (AP): This represents the weapon's ability to cut through the target's defences. After all modifiers are applied, this cannot be worse than 0. Damage (D): The amount of damage inflicted by a successful wound. After all modifiers are applied, this cannot be less than 1. The exception to this is where a rule specifies that you can change the Damage characteristic to 0.

---

[5] Blast ()
# Blast
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

High-explosives can fell several warriors in a single blast, but firing them where your comrades will get caught in the ensuing detonation is simply unwise. Weapons with [BLAST] in their profile are known as Blast weapons, and they make a random number of attacks. Each time you determine how many attacks are made with a Blast weapon, add 1 to the result for every five models that were in the target unit when you selected it as the target (rounding down). Blast weapons can never be used to make attacks against a unit that is within Engagement Range of one or more units from the attacking model's army (including its own unit). Example: If a weapon with the [BLAST] ability and an Attacks characteristic of 2D6 targets a unit that contains 11 models, and the roll to determine how many attacks are made is a 9, a total of 11 attacks would be made against that unit. Add 1 to the Attacks characteristic for every five models in the target unit (rounding down). Can never be used against a target that is w
```
</details>


### qwen/qwen3-32b
`finish=stop · 705 compl tok · 20.7s`

[Ruling] MONSTER and VEHICLE units can shoot in their controlling player's Shooting phase even while within Engagement Range of enemy units. When making ranged attacks under these conditions, subtract 1 from the Hit roll for each attack (unless the attack is made with a Pistol).  

[Rule Citation] **Big Guns Never Tire** (Core Rules) → "MONSTER and VEHICLE units are eligible to shoot [...] even while they are within Engagement Range [...] Each time a MONSTER or VEHICLE unit makes a ranged attack [...] subtract 1 from that attack's Hit roll [...] Designer's Note: [...] subtract 1 from that attack's Hit roll (unless shooting with a Pistol)."  

[Reasoning] The **Big Guns Never Tire** rule explicitly grants MONSTER and VEHICLE units the exception to shoot while in Engagement Range. The penalty (-1 to Hit rolls) applies universally to their ranged attacks in this scenario unless the weapon is a Pistol (which is a separate exception under the **Pistol** rule). This penalty also extends to attacks targeting enemy MONSTER or VEHICLE units within Engagement Range of friendly units.

### qwen/qwen3.6-27b
`finish=stop · 1834 compl tok · 24.0s`

[Ruling] MONSTER and VEHICLE units are eligible to shoot in their Shooting phase even while within Engagement Range of enemy units, and they may target enemy units they are engaged with even if friendly units are also within Engagement Range of those enemies. Each time a ranged attack is made by or against a MONSTER or VEHICLE unit that is within Engagement Range, you must subtract 1 from that attack's Hit roll (unless the attack is made with a Pistol).

[Rule Citation] Big Guns Never Tire (Core Rules)

[Reasoning] The rule explicitly overrides the standard restriction that prevents units from shooting while within Engagement Range, granting this exception specifically to MONSTER and VEHICLE units. It further clarifies that these units can target engaged enemies regardless of friendly unit positions. The penalty is directly stated in the rule text: any ranged attack made by or against such a unit while in Engagement Range suffers a -1 modifier to Hit rolls, with the only exception being attacks made with Pistols.

### llama-3.3-70b-versatile
`finish=stop · 155 compl tok · 3.0s`

[Ruling] → A MONSTER or VEHICLE unit can shoot while within Engagement Range of enemy units, but suffers a penalty of -1 to Hit rolls for ranged attacks made with non-Pistol weapons. 
→ [Rule Citation] Big Guns Never Tire, Core Rules 
→ [Reasoning] According to the Big Guns Never Tire rule, MONSTER and VEHICLE units are eligible to shoot in their controlling player's Shooting phase even while they are within Engagement Range of one or more enemy units. However, each time a MONSTER or VEHICLE unit makes a ranged attack, if that unit was within Engagement Range of one or more enemy units when it selected its targets, unless that attack is made with a Pistol, subtract 1 from that attack's Hit roll.

### llama-3.1-8b-instant
`finish=stop · 145 compl tok · 23.6s`

Big Guns Never Tire → [Big Guns Never Tire] → [Rule Citation: Core_Rules, Wahapedia_Core_Rules]

According to Big Guns Never Tire, MONSTER and VEHICLE units are eligible to shoot in their controlling player's Shooting phase even while they are within Engagement Range of one or more enemy units. 

Big Guns Never Tire → [Big Guns Never Tire] → [Rule Citation: Core_Rules, Wahapedia_Core_Rules]

When a MONSTER or VEHICLE unit makes a ranged attack, if that unit was within Engagement Range of one or more enemy units when it selected its targets, unless that attack is made with a Pistol, subtract 1 from that attack's Hit roll.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 102 compl tok · 19.5s`

Big Guns Never Tire → Core_Rules, Wahapedia_Core_Rules → According to Big Guns Never Tire, MONSTER and VEHICLE units are eligible to shoot in their controlling player's Shooting phase even while they are within Engagement Range of one or more enemy units. However, if a MONSTER or VEHICLE unit makes a ranged attack while within Engagement Range of one or more enemy units, and that attack is not made with a Pistol, subtract 1 from that attack's Hit roll.

### openai/gpt-oss-120b
`finish=stop · 402 compl tok · 3.2s`

**Ruling**  
Monsters and Vehicles are permitted to make ranged attacks even when they are within Engagement Range of enemy units. For each ranged attack they make while in Engagement Range, they suffer a –1 penalty to the Hit roll (i.e., you subtract 1 from the result of each Hit roll).  

**Rule Citation**  
*Big Guns Never Tire* – “MONSTER and VEHICLE units are eligible to shoot in their controlling player's Shooting phase even while they are within Engagement Range of one or more enemy units… Each time a MONSTER or VEHICLE unit makes a ranged attack, if that unit was within Engagement Range of one or more enemy units when it selected its targets, unless that attack is made with a Pistol, **subtract 1 from that attack's Hit roll**.”  

**Reasoning**  
The core rule *Locked in Combat* (in *Make Ranged Attacks*) normally prevents any unit from shooting while in Engagement Range. *Big Guns Never Tire* explicitly creates an exception for MONSTER and VEHICLE units, allowing them to shoot despite the Engagement Range restriction. The same rule then specifies the exact penalty that applies to those attacks: a –1 modifier to each Hit roll, unless the weapon used is a Pistol (which is excluded from the penalty). Thus, the ability both lifts the shooting restriction and imposes the –1 Hit roll penalty.

### openai/gpt-oss-20b
`finish=stop · 1070 compl tok · 8.5s`

**[Ruling]**  
Big Guns Never Tire allows MONSTER and VEHICLE units to shoot during the Shooting phase even while they are within Engagement Range of one or more enemy units.  For each ranged attack made by such a unit, the attacker must subtract 1 from the Hit roll, unless the attack is made with a Pistol.

**[Rule Citation]**  
- **Big Guns Never Tire** – “MONSTER and VEHICLE units are eligible to shoot in their controlling player’s Shooting phase even while they are within Engagement Range of one or more enemy units… Each time a MONSTER or VEHICLE unit makes a ranged attack, if that unit was within Engagement Range of one or more enemy units when it selected its targets, unless that attack is made with a Pistol, subtract 1 from that attack’s Hit roll.”  
- **Make Ranged Attacks** – “Locked in Combat: A unit is not eligible to shoot while it is within Engagement Range of one or more enemy units.” (This general rule is overridden by Big Guns Never Tire for MONSTER and VEHICLE units.)

**[Reasoning]**  
The general rule in *Make Ranged Attacks* prohibits any unit from shooting while within Engagement Range.  *Big Guns Never Tire* explicitly states that MONSTER and VEHICLE units are exceptions to this restriction, granting them the ability to shoot even when within Engagement Range.  The same rule then specifies the penalty: for every ranged attack made by such a unit, subtract 1 from the Hit roll, except when the attack is made with a Pistol.  Thus, a Monster or Vehicle can fire while in Engagement Range, but each of its attacks is penalised by –1 to Hit unless the weapon is a Pistol.

### allam-2-7b
`finish=stop · 964 compl tok · 51.3s`

Big Guns Never Tire


====================================================================================================
## [5] CORE · mp=OFF · ctx 3075 tok

**Q:** If I shoot with an Indirect Fire weapon at a target I cannot see, what modifier applies to my hit rolls and does the target get the Benefit of Cover?

**Expected concepts (ground-truth anchors):** [['indirect fire'], ['benefit of cover', 'cover']]

<details><summary>rules context sent to every model</summary>

```
[1] Indirect Fire ()
# Indirect Fire
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Indirect fire weapons launch munitions over or around intervening obstacles - nowhere is safe from their fury.
Weapons with [INDIRECT FIRE] in their profile are known as Indirect Fire weapons, and attacks can be made with them even if the target is not visible to the attacking model. These attacks can destroy enemy models in a target unit even though none may have been visible to the attacking unit when you selected that target. If no models in a target unit are visible to the attacking unit when you select that target, then each time a model in the attacking unit makes an attack against that target using an Indirect Fire weapon, subtract 1 from that attack's Hit roll, an unmodified Hit roll of 1-3 always fails, and the target has the Benefit of Cover against that attack. Weapons with the [TORRENT] ability cannot be fired using the [INDIRECT FIRE] ability.
Example: An enemy unit is targeted by an attacking model equipped with a weapon with the [INDIRECT FIRE] ability. No models in the target unit are visible to the attacking model, so when resolving the attacks made with that weapon, subtract 1 from that attack's Hit roll an unmodified Hit roll of 1-3 always fails, and each time an attack is allocated to a model in the target unit, it has the Benefit of Cover against that attack.
Can target and make attacks against units that are not visible to the attacking unit. If no models are visible in a target unit when it is selected, then when making an attack against that target with an Indirect Fire weapon, subtract 1 from that attack's Hit roll, an unmodified Hit roll of 1-3 always fails, and the target has the Benefit of Cover against that attack.

---

[2] Rapid Fire ()
# Rapid Fire
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Rapid fire weapons are capable of long-ranged precision shots or controlled bursts at nearby targets.
Weapons with [RAPID FIRE X] in their profile are known as Rapid Fire weapons. Each time such a weapon targets a unit within half that weapon's range, the Attacks characteristic of that weapon is increased by the amount denoted by 'x'.
Example: A model targets a unit that is within half range of a weapon with an Attacks characteristic of 1 and the [RAPID FIRE 1] ability. That weapon therefore makes two attacks at the target, and you make two Hit rolls.
[RAPID FIRE X]: Increase the Attacks by 'x' when targeting units within half range.

---

[3] Make Ranged Attacks ()
# Make Ranged Attacks
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The shooting unit's models now make attacks using their ranged weapons. Each time a model shoots with a ranged weapon, it will make a number of attacks equal to the Attacks (A) characteristic in that weapon's profile. You make one Hit roll for each attack being made (see Making Attacks). If you selected more than one target for your unit to shoot at, you must resolve all of the attacks against one target before moving on to the next target. If your unit is shooting more than one ranged weapon at a target, and those weapons have different profiles, then after you have resolved attacks with one of those weapons you must, if any other weapons with the same profile are also being shot at that unit, resolve those attacks before resolving any other attacks against the target. Note that, provided at least one model in the target unit was visible to an attacking model and in range of that attacking model's weapon when that target unit was selected, that weapon's attacks can still be made, even if no models in the target unit remain visible to or in range of it when you come to resolve those attacks (for example, because models in the target unit have already been destroyed by attacks made with other weapons in the attacking model's unit).
When a model shoots a weapon, it makes a number of attacks equal to that weapon's Attacks characteristic. Resolve all attacks against one unit before resolving attacks against any other unit. Resolve all attacks made with the same weapon profile before resolving attacks with any other profile. If a weapon was in range and its target was visible when selected, that weapon's attacks can always be made.
Locked in Combat A unit is not eligible to shoot while it is within Engagement Range of one or more enemy units. While an enemy unit is within Engagement Range of one or more units from your army, you cannot select that enemy unit as a target of ranged weapons. MONSTER and VEHICLE units are exceptions to these rules, as described in the Big Guns Never Tire section. Units cannot shoot while within Engagement Range of enemy units. Units cannot shoot at targets within Engagement Range of friendly units.
STEALTH Some warriors are masters of disguise and concealment. If every model in a unit has this ability, then each time a ranged attack is made against it, subtract 1 from that attack's Hit roll.

---

[4] Ignores Cover ()
# Ignores Cover
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some weapons are designed to root enemy formations out of entrenched positions.
Weapons with [IGNORES COVER] in their profile are known as Ignores Cover weapons. Each time an attack is made with such a weapon, the target cannot have the Benefit of Cover against that attack.

---

[5] Weapons ()
# Weapons
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Weapons are described with the following characteristics: Range: How far the weapon can shoot. Weapons with a range of 'Melee' are melee weapons and can only be used in close combat. All other weapons are ranged weapons. For ranged weapons, after all modifiers are applied, this cannot be less than 1". Attacks (A): This tells you how many attacks are made each time that weapon is used. After all modifiers are applied, this cannot be less than 1. Weapon Skill (WS): This reflects the bearer's skill in wielding the relevant melee weapon. After all modifiers are applied, this cannot be 1+ or better. Ballistic Skill (BS): This shows how accurate the bearer is when shooting with the relevant ranged weapon. After all modifiers are applied, this cannot be 1+ or better. Strength (S): How likely the weapon is to wound a foe. After all modifiers are applied, this cannot be less than 1. Armour Penetration (AP): This represents the weapon's ability to cut through the target's defences. After all modifiers are applied, this cannot be worse than 0. Damage (D): The amount of damage inflicted by a successful wound. After all modifiers are applied, this cannot be less than 1. The exception to this is where a rule specifies that you can change the Damage characteristic to 0.

---

[6] Benefit of Cover ()
# Benefit of Cover
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Shattered ruins and twisted wreckage afford much-needed shelter from enemy salvoes. Even heavily armoured warriors unfazed by small arms fire are thankful for such cover when foes bring their biggest guns to bear. Models can sometimes gain a measure of protection from terrain features. The rules below detail the conditions under which a terrain feature confers the Benefit of Cover on a model. Each time a ranged attack is allocated to a model that has the Benefit of Cover, add 1 to the saving throw made for that attack (excluding invulnerable saving throws). Models with a Save characteristic of 3+ or better cannot have the Benefit of Cover against attacks with an Armour Penetration characteristic of 0. Multiple instances of the Benefit of Cover are not cumulative - a model cannot benefit from this rule more than once at any one time. Benefit of Cover: Add 1 to armour saving throws against ranged attacks. Does not apply to models with a Save of 3+ or better against attacks with an AP of 0. Multiple instances are not cumulative.

---

[7] Select Targets ()
# Select Targets
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rule
```
</details>


### qwen/qwen3-32b
`finish=stop · 502 compl tok · 21.6s`

[Ruling] When using an Indirect Fire weapon to target a unit where **no models are visible** to the attacking unit, **subtract 1 from each attack’s Hit roll**, **unmodified Hit rolls of 1–3 always fail**, and **the target gains the Benefit of Cover** against the attack.  

[Rule Citation] **Indirect Fire** (Core Rules) → [1] Indirect Fire.  

[Reasoning] The rule explicitly states that if no models in the target unit are visible when the target is selected, attacks with an Indirect Fire weapon suffer a -1 to Hit rolls, unmodified 1–3 Hit rolls fail automatically, and the target gains the Benefit of Cover. This applies regardless of other rules (e.g., Ignores Cover) unless the weapon has conflicting abilities (not the case here).

### qwen/qwen3.6-27b
`finish=stop · 1264 compl tok · 40.1s`

[Ruling] You must subtract 1 from each Hit roll, an unmodified Hit roll of 1–3 always fails, and the target has the Benefit of Cover against those attacks.

[Rule Citation] [1] Indirect Fire (Core Rules)

[Reasoning] The Indirect Fire rule explicitly states that if no models in the target unit are visible to the attacking unit when the target is selected, each attack made with an Indirect Fire weapon against that target suffers a -1 modifier to the Hit roll, unmodified rolls of 1–3 automatically fail, and the target gains the Benefit of Cover against those attacks.

### llama-3.3-70b-versatile
`finish=stop · 181 compl tok · 3.0s`

[Ruling] → [Rule Citation: Indirect Fire, Category: Core_Rules, Source: Wahapedia_Core_Rules] → [Reasoning]: When making an attack with an Indirect Fire weapon against a target that is not visible to the attacking unit, you subtract 1 from the attack's Hit roll, and an unmodified Hit roll of 1-3 always fails. Additionally, the target has the Benefit of Cover against that attack. This is explicitly stated in the Indirect Fire rule: "If no models in a target unit are visible to the attacking unit when you select that target, then each time a model in the attacking unit makes an attack against that target using an Indirect Fire weapon, subtract 1 from that attack's Hit roll, an unmodified Hit roll of 1-3 always fails, and the target has the Benefit of Cover against that attack."

### llama-3.1-8b-instant
`finish=stop · 172 compl tok · 21.1s`

[Ruling] → [Indirect Fire] → [Rule Citation: Indirect Fire, Core_Rules, Wahapedia_Core_Rules]

When shooting with an Indirect Fire weapon at a target you cannot see, you must subtract 1 from that attack's Hit roll, and an unmodified Hit roll of 1-3 always fails. Additionally, the target has the Benefit of Cover against that attack.

[Reasoning]
According to the Indirect Fire rule, when no models in a target unit are visible to the attacking unit when you select that target, then each time a model in the attacking unit makes an attack against that target using an Indirect Fire weapon, subtract 1 from that attack's Hit roll, an unmodified Hit roll of 1-3 always fails, and the target has the Benefit of Cover against that attack.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 153 compl tok · 1.1s`

[Ruling] → When shooting with an Indirect Fire weapon at a target that is not visible to the attacking model, subtract 1 from the attack's Hit roll, and an unmodified Hit roll of 1-3 always fails. Additionally, the target has the Benefit of Cover against that attack.

→ [Indirect Fire] → [Reasoning]: According to the Indirect Fire rule, if no models in the target unit are visible to the attacking unit when the target is selected, then each time a model in the attacking unit makes an attack against that target using an Indirect Fire weapon, subtract 1 from that attack's Hit roll, an unmodified Hit roll of 1-3 always fails, and the target has the Benefit of Cover against that attack.

### openai/gpt-oss-120b
`finish=stop · 452 compl tok · 10.6s`

**Ruling:** When you fire an Indirect Fire weapon at a target that you cannot see, you subtract 1 from each Hit roll (and any unmodified roll of 1‑3 automatically fails), and the target unit does receive the Benefit of Cover against those attacks.

**Rule Citation:** *Indirect Fire* – “If no models in a target unit are visible to the attacking unit when you select that target, then each time a model in the attacking unit makes an attack against that target using an Indirect Fire weapon, **subtract 1 from that attack's Hit roll**, an unmodified Hit roll of 1‑3 always fails, and **the target has the Benefit of Cover** against that attack.” (Source: Wahapedia_Core_Rules, [1] Indirect Fire)

**Reasoning:** The Indirect Fire rule explicitly defines the penalties and benefits that apply when the target is not visible. The –1 modifier to the Hit roll is the required adjustment to the attack roll, and the rule also states that the target gains the Benefit of Cover for those attacks. No other rule overrides this effect, so the stated modifiers and cover benefit apply directly.

### openai/gpt-oss-20b
`finish=stop · 521 compl tok · 10.1s`

**[Ruling]**  
When you fire an Indirect Fire weapon at a target unit that contains no visible models, you must subtract 1 from each Hit roll for that attack, any unmodified Hit roll of 1‑3 automatically fails, and the target unit gains the Benefit of Cover for that attack.

**[Rule Citation]**  
*Indirect Fire* (Wahapedia_Core_Rules, rule 1) – “If no models in a target unit are visible to the attacking unit when you select that target, then each time a model in the attacking unit makes an attack against that target using an Indirect Fire weapon, subtract 1 from that attack’s Hit roll, an unmodified Hit roll of 1‑3 always fails, and the target has the Benefit of Cover against that attack.”

**[Reasoning]**  
The rule explicitly states the two modifiers that apply when the target is not visible: a –1 to the Hit roll and a guaranteed miss on unmodified 1‑3. It also states that the target “has the Benefit of Cover against that attack,” meaning the target’s saving throw will receive the +1 bonus from the Benefit of Cover rule. No other modifiers are mentioned, so only these apply.

### allam-2-7b
`finish=error · ? compl tok · ?s` ⚠ ERROR: Error code: 413 - {'error': {'message': 'Request too large for model `allam-2-7b` in organization `org_01kkppmxccfd1r98zztyme6k5a` service tier `on_demand` on tokens per minute (TPM): Limit 6000, Requ


====================================================================================================
## [6] CORE · mp=OFF · ctx 2673 tok

**Q:** How do Devastating Wounds interact with invulnerable saves and Feel No Pain — which of those can still be used against the damage?

**Expected concepts (ground-truth anchors):** [['devastating wounds'], ['invulnerable save'], ['feel no pain']]

<details><summary>rules context sent to every model</summary>

```
[1] Devastating Wounds ()
# Devastating Wounds
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Weapons with [DEVASTATING WOUNDS] in their profile are known as Devastating Wounds weapons. Each time an attack is made with such a weapon, if that attack scores a Critical Wound, no saving throw of any kind can be made against that attack (including invulnerable saving throws). Such attacks are only allocated to models after all other attacks made by the attacking unit have been allocated and resolved. After that attack is allocated and after any modifiers are applied, it inflicts a number of mortal wounds on the target equal to the Damage characteristic of that attack, instead of inflicting damage normally. Example: An attack made with a Devastating Wounds weapon with a Damage characteristic of 2 scores a Critical Wound. Instead of allocating the attack and making saving throws normally, the target suffers 2 mortal wounds. A Critical Wound inflicts mortal wounds equal to the weapon's Damage characteristic, instead of any normal damage.

---

[2] 5. Inflict Damage ()
# 5. Inflict Damage — Feel No Pain
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

FEEL NO PAIN Some warriors refuse to be laid low, even by what should be fatal wounds. Some models have 'Feel No Pain x+' listed in their abilities. Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6: if the result is greater than or equal to the number denoted by 'x', that wound is ignored and is not lost. If a model has more than one Feel No Pain ability, you can only use one of those abilities each time that model suffers damage and so would lose a wound. Feel No Pain x+: Each time this model would lose a wound, roll one D6: if the result equals or exceeds 'x', that wound is not lost.

---

[3] Mortal Wounds ()
# Mortal Wounds
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some attacks are so powerful that no armour or force field can withstand their fury. Some rules inflict mortal wounds on units. Each time mortal wounds are inflicted on a unit, each of those mortal wounds inflicts one point of damage to that unit, and they are always applied one at a time. Each mortal wound is allocated to a model in the same manner as allocating an attack. Excess damage from mortal wounds is not lost if the damage can be allocated to another model. Instead, keep allocating damage to another model in the target unit until either all the damage has been allocated or the target unit is destroyed. If an attack inflicts mortal wounds in addition to any normal damage, do not make a Wound roll or saving throw (including invulnerable saving throws) against those mortal wounds. If those mortal wounds are inflicted by an attack that has the [PRECISION] ability, the attacking model's controlling player can allocate those mortal wounds to a CHARACTER model in that unit. If mortal wounds are being inflicted as a result of the [HAZARDOUS] ability or by an attack with the [DEVASTATING WOUNDS] ability that scored a Critical Wound, each time those mortal wounds are allocated to a model, if that model is destroyed as a result of those mortal wounds, the remaining mortal wounds from that attack are lost, just as with a normal attack. If, when a unit is selected to shoot or fight, one or more of its attacks can inflict mortal wounds on the target, resolve any normal damage inflicted by the attacking unit's attacks on that target before inflicting any mortal wounds on that target. If an attack inflicts mortal wounds in addition to any normal damage, but the normal damage is subsequently saved, the target unit still suffers those mortal wounds, as described above. Each mortal wound inflicted on a unit causes one model in that unit to lose one wound. Unless the source of the mortal wounds is the [HAZARDOUS] ability or an attack with the [DEVASTATING WOUNDS] ability, damage from mortal wounds is not lost if it can be allocated to another model. No saving throws can be made against mortal wounds. Mortal wounds inflicted by attacks always apply after any normal damage, even if that damage was saved.

---

[4] 5. Inflict Damage ()
# 5. Inflict Damage
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The damage inflicted is equal to the Damage (D) characteristic of the attack. A model loses one wound for each point of damage it suffers. If a model's wounds are reduced to 0 or less, it is destroyed and removed from play. If a model loses several wounds from an attack and is destroyed, any excess damage inflicted by that attack is lost and has no effect. A model loses a number of wounds equal to the attack's Damage characteristic. If a model is destroyed by an attack, any excess damage inflicted by that attack is lost.

---

[5] 4. Saving Throw ()
# 4. Saving Throw
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The player controlling the target unit then makes one saving throw. By default, this will be an armour saving throw using their model's Save (Sv) characteristic, but some models have invulnerable saves that can be used instead (see below). To make an armour saving throw, roll one D6, then modify the result by the Armour Penetration (AP) characteristic of the attack. For example, if the attack has an AP of -1, then 1 is subtracted from the saving throw. If the result is greater than or equal to the Save characteristic of the model the attack was allocated to, then that saving throw is successful and the attack sequence ends. Otherwise, that saving throw fails and that model suffers damage. An unmodified saving throw of 1 always fails. A saving throw can never be improved by more than +1. Saving Throw: Roll one D6 and modify by the attack's AP. If the result is less than the Save of the model being rolled for, the saving throw is failed and that model suffers damage. Otherwise, that attack is saved. An unmodified saving throw of 1 always fails. A saving throw can never be improved by more than +1.

---

[6] Lethal Hits ()
# Lethal Hits
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some weapons can inflict fatal injuries on any foe, no matter their resilience.
Weapons with [LETHAL HITS] in their profile are known as Lethal Hits weapons. Each time an attack is made with such a weapon, a Critical Hit automatically wounds the target.

---

[7] 3. Allocate Attack ()
# 3. Allocate Attack
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If an attack successfully wounds the target unit, the player controlling the target unit allocates that attack to one model in the target unit, as follows. If a model in the target unit has already lost one or more wounds, or has already had attacks allocated to it this phase, that attack must be allocated to that model. Otherwise, that attack can be allocated to any model in the target unit. Note that it does not matter if that model is visible to or within range/ Engagement Range of the attacking model.
If a model in the target unit has already lost any wounds or had other attacks allocated to it this phase, the attack must be allocated to that model.

---

[8] 2. Wound Roll ()
# 2. Wound Roll
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Each time an attack scores a hit against a target unit, make a Wound roll for that attack by rolling one D6 to see if that attack successfully wounds the target unit. The result required is determined by comparing the attack's Strength (S) characteristic with the target's Toughness (T) characteristic, as shown below.
WOUND ROLL
ATTACK'S STRENGTH VS TARGET'S TOUGHNESS | D6 RESULT REQUIRED
Strength is TWICE (or more than twice) the Toughness. | 2+
Strength is GREATER than the Toughness. | 3+
Strength is EQUAL to the Toughness. | 4+
Strength is LESS than the Toughness. | 5+
Strength is HALF (or less than half) the Toughness. | 6+
If the result of the Wound roll is greater than or equ
```
</details>


### qwen/qwen3-32b
`finish=stop · 813 compl tok · 2.1s`

[Ruling] Devastating Wounds completely bypass all saving throws (including invulnerable saves) and are resolved as mortal wounds. However, Feel No Pain can still be used against the mortal wounds they inflict, as Feel No Pain is not a saving throw but a wound-loss mitigation ability.  

[Rule Citations]  
- **Devastating Wounds bypass all saving throws**: [1] Devastating Wounds → "no saving throw of any kind can be made against that attack (including invulnerable saving throws)."  
- **Mortal wounds bypass saving throws**: [3] Mortal Wounds → "No saving throws can be made against mortal wounds."  
- **Feel No Pain applies to mortal wounds**: [2] Feel No Pain → "Each time a model with this ability suffers damage and so would lose a wound [...] roll one D6: if the result equals or exceeds 'x', that wound is not lost." Mortal wounds from Devastating Wounds are "damage" that cause wound loss, so Feel No Pain applies.  

[Reasoning]  
Devastating Wounds prevent saving throws (including invulnerable saves) during the wound resolution phase, but after mortal wounds are allocated, they function as raw damage. Feel No Pain is a separate mechanic that triggers when a model would lose wounds from any source (including mortal wounds), and it is not classified as a "saving throw" in the rules. Thus, it remains usable against Devastating Wounds' mortal wounds.

### qwen/qwen3.6-27b
`finish=stop · 1631 compl tok · 80.9s`

[Ruling] Invulnerable saves cannot be used against a Devastating Wounds attack that scores a Critical Wound, but Feel No Pain can still be used against the resulting damage.

[Rule Citation] Devastating Wounds (Wahapedia_Core_Rules); 5. Inflict Damage — Feel No Pain (Wahapedia_Core_Rules)

[Reasoning] The Devastating Wounds rule explicitly states that if the attack scores a Critical Wound, "no saving throw of any kind can be made against that attack (including invulnerable saving throws)." Instead of inflicting damage normally, the attack inflicts mortal wounds equal to its Damage characteristic. The Feel No Pain rule explicitly triggers "Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds)," allowing the controlling player to roll a D6 to ignore those wounds. Therefore, while all saving throws are completely bypassed, Feel No Pain remains fully applicable to the mortal wounds inflicted by the weapon.

### llama-3.3-70b-versatile
`finish=stop · 212 compl tok · 18.2s`

[Ruling] → [Rule Citation: Devastating Wounds, Feel No Pain, Invulnerable Saves] → [Reasoning]: 
According to the Devastating Wounds rule, "no saving throw of any kind can be made against that attack (including invulnerable saving throws)" when a Devastating Wounds weapon scores a Critical Wound. This means that invulnerable saves cannot be used against the damage inflicted by a Devastating Wounds attack that scores a Critical Wound.

However, the Feel No Pain rule states that it can be used "each time a model suffers damage and so would lose a wound (including wounds lost due to mortal wounds)". Since Devastating Wounds inflict mortal wounds, Feel No Pain can still be used against the damage inflicted by a Devastating Wounds attack. 

Therefore, when a Devastating Wounds attack scores a Critical Wound, the target model cannot use invulnerable saves, but it can still use Feel No Pain to potentially ignore some or all of the mortal wounds inflicted.

### llama-3.1-8b-instant
`finish=stop · 283 compl tok · 10.1s`

[Ruling] → [Rule Citation] → [Reasoning]

**Devastating Wounds and Invulnerable Saves:**
Devastating Wounds do not interact with invulnerable saves in a way that prevents the use of invulnerable saves. → [Invulnerable Saves] → Invulnerable saving throws are never modified by an attack's Armour Penetration characteristic, but otherwise follow the normal rules for saving throws. This means that invulnerable saves can still be used against Devastating Wounds attacks.

**Devastating Wounds and Feel No Pain:**
Feel No Pain can still be used against Devastating Wounds attacks. → [Devastating Wounds] → Each time an attack is made with such a weapon, if that attack scores a Critical Wound, no saving throw of any kind can be made against that attack (including invulnerable saving throws). However, this rule does not prevent the use of Feel No Pain abilities, which are triggered by the model losing wounds, not by making saving throws. → [5. Inflict Damage] → Feel No Pain x+: Each time this model would lose a wound, roll one D6: if the result equals or exceeds 'x', that wound is not lost.

In summary, invulnerable saves can still be used against Devastating Wounds attacks, and Feel No Pain abilities can still be used to prevent wounds from being lost.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 247 compl tok · 127.8s`

Devastating Wounds Interaction → Devastating Wounds [1] → According to the Devastating Wounds rule, when an attack with [DEVASTATING WOUNDS] scores a Critical Wound, no saving throw of any kind can be made against that attack. This includes invulnerable saving throws.

Feel No Pain Interaction → Feel No Pain [2] → The Devastating Wounds rule does not explicitly state that Feel No Pain abilities cannot be used. However, since the attack inflicts mortal wounds directly and does not allow a saving throw, Feel No Pain would not be triggered in the same way as it would for normal damage.

Ruling → Devastating Wounds [1] → When an attack with [DEVASTATING WOUNDS] scores a Critical Wound, the target model cannot make an invulnerable saving throw or use Feel No Pain to ignore the wound. The model directly suffers mortal wounds equal to the weapon's Damage characteristic.

Therefore, against an attack with [DEVASTATING WOUNDS] that scores a Critical Wound, neither invulnerable saves nor Feel No Pain abilities can be used to mitigate the damage. The target model directly suffers mortal wounds as per the weapon's Damage characteristic.

### openai/gpt-oss-120b
`finish=stop · 1031 compl tok · 22.9s`

**Ruling**  
When a Devastating Wounds weapon scores a Critical Wound, **no saving throw of any kind can be made** (so invulnerable saves cannot be used). The attack then inflicts mortal wounds equal to its Damage characteristic. After those mortal wounds are allocated and cause damage, any model that has **Feel No Pain** may attempt to ignore each wound caused by the mortal wounds.

**Rule Citations**  

1. **Devastating Wounds** – “Each time an attack is made with such a weapon, if that attack scores a Critical Wound, **no saving throw of any kind can be made against that attack (including invulnerable saving throws)**… it inflicts a number of mortal wounds on the target equal to the Damage characteristic of that attack, instead of inflicting damage normally.”【1】

2. **Invulnerable Saves** – “Each time an attack is allocated to a model with an invulnerable save, the controlling player must choose to use either that model's Save characteristic or its invulnerable save… Invulnerable saving throws are never modified by an attack's Armour Penetration characteristic…”【10】  
   *The Devastating Wounds rule explicitly overrides any saving throw, so this choice is unavailable.*

3. **Mortal Wounds** – “Each mortal wound inflicts one point of damage to that unit… No saving throws can be made against mortal wounds. … If a model suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6… (Feel No Pain).”【3】

4. **Feel No Pain** – “Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6: if the result is greater than or equal to the number denoted by ‘x’, that wound is ignored and is not lost.”【2】

**Reasoning**  

- The Devastating Wounds rule states that **no saving throw of any kind** can be made when the weapon scores a Critical Wound. This explicitly includes invulnerable saves, so the target cannot attempt an invulnerable save against the attack.  
- The same rule then replaces normal damage with mortal wounds equal to the weapon’s Damage characteristic. Mortal wounds are a form of damage that bypasses saves but still count as “damage suffered” by the model.  
- The Feel No Pain rule triggers **any time a model suffers damage and would lose a wound**, explicitly covering wounds lost from mortal wounds. Therefore, after the mortal wounds are allocated, the model may roll for Feel No Pain to potentially ignore each wound.  

Thus, against a Devastating Wounds attack that scores a Critical Wound, **invulnerable saves cannot be used**, while **Feel No Pain can still be applied** to each wound caused by the resulting mortal wounds.

### openai/gpt-oss-20b
`finish=stop · 1641 compl tok · 2.2s`

**Ruling**  
When a Devastating Wounds attack scores a Critical Wound, no saving throw can be made against it, so an invulnerable save is not available. The mortal wounds that are inflicted still cause damage that can be mitigated by a model’s Feel No Pain ability.

**Rule Citations**  
1. **Devastating Wounds** – “Each time an attack is made with such a weapon, if that attack scores a Critical Wound, no saving throw of any kind can be made against that attack (including invulnerable saving throws).” (Rule [1])  
2. **Invulnerable Saves** – “Each time an attack is allocated to a model with an invulnerable save, the controlling player must choose to use either that model’s Save characteristic or its invulnerable save, but not both.” (Rule [10])  
3. **Mortal Wounds** – “Each mortal wound inflicts one point of damage to that unit … No saving throws can be made against mortal wounds.” (Rule [3])  
4. **Feel No Pain** – “Each time a model with this ability suffers damage and so would lose a wound … roll one D6 … that wound is not lost.” (Rule [2])

**Reasoning**  
- The Devastating Wounds rule explicitly states that *no saving throw of any kind* can be made when a Critical Wound is scored, overriding any other saving‑throw rules, including the invulnerable save.  
- The mortal wounds that replace normal damage are still “damage” that is applied to models (Rule [3]), and the Feel No Pain ability triggers whenever a model would lose a wound from damage (Rule [2]).  
- Because mortal wounds are not subject to saving throws, the only potential mitigation is the Feel No Pain ability, which remains available.  

Thus, invulnerable saves cannot be used against a Devastating Wounds attack that scores a Critical Wound, but Feel No Pain can still be used to ignore a wound lost from the mortal wounds inflicted.

### allam-2-7b
`finish=stop · 726 compl tok · 0.9s`


























































































































































































































































































































































































































































































































































































































































































































































====================================================================================================
## [7] CORE · mp=OFF · ctx 2416 tok

**Q:** When a Transport is destroyed with units still embarked, how do the passengers disembark and can they take damage?

**Expected concepts (ground-truth anchors):** [['transport'], ['disembark'], ['destroyed']]

<details><summary>rules context sent to every model</summary>

```
[1] Destroyed Transports ()
# Destroyed Transports
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a TRANSPORT model is destroyed, any units embarked within that TRANSPORT model must immediately disembark (see below) before that TRANSPORT model is removed from the battlefield. Units that disembark from a destroyed TRANSPORT model are not affected by that model's Deadly Demise ability. Instead, you must roll one D6 for each disembarking model. For each roll of 1, that disembarking model's unit suffers 1 mortal wound. In addition, if a unit disembarks from a destroyed TRANSPORT model:
- Until the start of its controlling player's next Command phase, that unit is Battle-shocked.
- Until the end of the turn, that unit counts as having made a Normal move this turn, and cannot declare a charge this turn.
If a TRANSPORT is destroyed, any embarked units must disembark. Roll one D6 for each model that disembarks: for each 1, that model's unit suffers 1 mortal wound. Until the start of its controlling player's next Command phase, the disembarking unit is Battle-shocked. Until the end of the turn, the disembarking unit counts as having made a Normal move, and cannot declare a charge.
Emergency Disembarkation
If a TRANSPORT model is destroyed and it is not possible to set up a disembarking unit wholly within 3" of that TRANSPORT model and not within Engagement Range of any enemy models, that unit must instead perform an Emergency Disembarkation. This is performed as described for disembarking from a destroyed TRANSPORT model, except that a unit that does so must be set up wholly within 6" of the destroyed TRANSPORT model (instead of wholly within 3") and not within Engagement Range of any enemy models, and when rolling for each disembarking model, that unit suffers 1 mortal wound for each roll of 1-3 (instead of for each roll of 1). If, for any reason, a disembarking model still cannot be set up, that model is destroyed.
Units disembarking a destroyed TRANSPORT that cannot be set up wholly within 3" of it must perform an Emergency Disembarkation: Must be set up wholly within 6" of it instead of wholly within 3". Suffer 1 mortal wound for each roll of 1-3, instead of each roll of 1. Any disembarking model that cannot be set up is destroyed.
The Terminators make an Advance move of 8" - all the models in the unit end that move within 3" of the Land Raider Crusader, and can therefore embark within it.
The Terminators are selected to disembark from the Land Raider Crusader and are set up wholly within 3" of it. The Land Raider Crusader has Remained Stationary, so the Terminators can then make an Advance move.
The Land Raider Crusader is destroyed, forcing the Terminators to disembark wholly within 3". The controlling player then rolls one D6 for each disembarking model, resulting in a 1, 3, 3, 5 and 6. The Terminator unit suffers 1 mortal wound and is now Battle-shocked.

---

[2] Transports ()
# Transports
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some models have the TRANSPORT keyword. The following rules describe how units can embark within and disembark from such models, and how they are used to move these passengers across the battlefield.
Some units can carry others across the battlefield, providing their passengers with greater speed and protection as they are ferried to the front lines or towards vital objectives.

---

[3] Disembark ()
# Disembark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit from your army starts your Movement phase embarked within a TRANSPORT model, that unit can disembark in that phase. When a unit disembarks from a TRANSPORT model, set it up on the battlefield so that it is wholly within 3" of that TRANSPORT model and not within Engagement Range of any enemy models. If, for any reason, a disembarking model cannot be set up, that model's unit cannot disembark. Units that disembark from a TRANSPORT model that either Remained Stationary this phase or has not yet made a Normal, Advance or Fall Back move this phase can then act normally (make a Normal move, Advance, shoot, declare a charge, fight, etc.) in the remainder of the turn. Such a disembarking unit cannot choose to Remain Stationary. Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; they cannot move further during this phase. Such a unit also cannot declare a charge in the same turn, but can otherwise act normally in the remainder of the turn. Units cannot disembark from a TRANSPORT model that either Advanced or Fell Back this turn. Units that start your Movement phase embarked within a TRANSPORT can disembark this phase, provided their TRANSPORT has not Advanced or Fallen Back. If a unit disembarks before its TRANSPORT moves, it can act normally. If a unit disembarks after its TRANSPORT moves, it cannot move or charge this turn, but can otherwise act normally. Disembarking units must be set up wholly within 3" of their TRANSPORT and not within Engagement Range of any enemy models (or the unit cannot disembark). Units that disembark this turn cannot Remain Stationary.

---

[4] Embark ()
# Embark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit makes a Normal, Advance or Fall Back move, and every model in that unit ends that move within 3" of a friendly TRANSPORT model, they can embark within it. A unit cannot embark if it has already disembarked from a TRANSPORT model in the same phase. Remove the unit from the battlefield and place it to one side - it is now embarked within that TRANSPORT model. Unless otherwise stated, units cannot do anything or be affected in any way while they are embarked. A unit can embark within a friendly TRANSPORT if all of its models end a Normal, Advance or Fall Back move within 3" of that TRANSPORT. A unit cannot embark and disembark in the same phase.

---

[5] 5. Inflict Damage ()
# 5. Inflict Damage — Deadly Demise
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

DEADLY DEMISE From detonating ammo stores to corrosive innards or frenzied death throes, some targets are deadly even in defeat. Some models have 'Deadly Demise x' listed in their abilities. When such a model is destroyed, roll one D6 before removing it from play (if such a model is a TRANSPORT, roll before any embarked models disembark). On a 6, each unit within 6" of that model suffers a number of mortal wounds denoted by 'x' (if this is a random number, roll separately for each unit within 6"). Example: A TRANSPORT model with the Deadly Demise D3 ability is destroyed. Before any models disembark and before removing it from play, its controlling player rolls one D6, getting a 6. There are three units within 6" of that destroyed model, so its controlling player rolls one D3 for each of them, inflicting mortal wounds accordingly. Deadly Demise x: When this model is destroyed, roll one D6. On a 6, each unit within 6" suffers 'x' mortal wounds.

---

[6] Transport Capacity ()
# Transport Capacity
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

All TRANSPORT models have a transport capacity listed on their datasheet. This determines the type and maximum number of friendly models that can embark within them. Units can start the battle embarked within a TRANSPORT model instead of being set up separately - declare which units are embarked within a TRANSPORT model before you set it up. FIRING DECK Some transports have firing hatches, ports or platforms from which embarked passengers can shoot. Some TRANSPORT models have 'Firing Deck x' listed in their abilities. Each time such a model is selected to shoot in the Shooting phase, you can select up to 'x' models embarked within it whose units have not already shot this phase. Then, for each of those embarked models, you can select one ranged weapon that embarked model is equipped with (excluding weapons with the [ONE SHOT] ability). Until that TRANSPORT mode
```
</details>


### qwen/qwen3-32b
`finish=stop · 937 compl tok · 7.0s`

[Ruling] When a TRANSPORT is destroyed with units embarked, those units must immediately disembark. During this process, each disembarking model triggers a D6 roll: a roll of 1 inflicts 1 mortal wound on the unit. If setup within 3" of the destroyed TRANSPORT is impossible, Emergency Disembarkation applies (setup within 6", with mortal wounds on 1-3 instead of 1). Units disembarking this way are Battle-shocked until the start of their controlling player’s next Command phase and count as having made a Normal move (cannot charge that turn).  

[Rule Citation] **Destroyed Transports** (Core Rules) → "If a TRANSPORT is destroyed, any units embarked within that TRANSPORT model must immediately disembark... Roll one D6 for each model that disembarks: for each 1, that disembarking model's unit suffers 1 mortal wound... Emergency Disembarkation: ...suffer 1 mortal wound for each roll of 1-3..."  

[Reasoning] The rules explicitly state that destroyed TRANSPORTs force embarked units to disembark, with specific rules for damage rolls and setup. The D6 rolls and their outcomes (mortal wounds, Battle-shocked status, movement restrictions) are directly tied to this process. Emergency Disembarkation modifies setup range and damage thresholds if standard disembarkation is impossible.

### qwen/qwen3.6-27b
`finish=stop · 1864 compl tok · 8.0s`

[Ruling] When a TRANSPORT model is destroyed, embarked units must immediately disembark before the transport is removed. They can take damage during this process via D6 rolls, and they are explicitly not affected by the transport's Deadly Demise ability.

[Rule Citation] Destroyed Transports (Core Rules, Wahapedia_Core_Rules)

[Reasoning] According to the Destroyed Transports rule, units must disembark immediately and be set up wholly within 3" of the destroyed TRANSPORT and not within Engagement Range of any enemy models. For each model that disembarks, you roll one D6; on a roll of 1, that model's unit suffers 1 mortal wound. If it is impossible to set the unit up within 3", it must perform an Emergency Disembarkation, setting up wholly within 6" instead. During an Emergency Disembarkation, the unit suffers 1 mortal wound for each roll of 1-3. Any model that still cannot be set up is destroyed. Additionally, until the start of the controlling player's next Command phase, the disembarking unit is Battle-shocked, and until the end of the turn, it counts as having made a Normal move and cannot declare a charge. The rule explicitly states that units disembarking from a destroyed TRANSPORT are not affected by that model's Deadly Demise ability.

### llama-3.3-70b-versatile
`finish=stop · 204 compl tok · 110.7s`

[Ruling] → [Rule Citation: Destroyed Transports, Source: Wahapedia_Core_Rules] → [Reasoning]: When a TRANSPORT model is destroyed, any units embarked within that TRANSPORT model must immediately disembark. To disembark, the units are set up wholly within 3" of the destroyed TRANSPORT model and not within Engagement Range of any enemy models. For each model that disembarks, the player rolls one D6, and for each roll of 1, that model's unit suffers 1 mortal wound. Additionally, the disembarking unit is Battle-shocked until the start of its controlling player's next Command phase and counts as having made a Normal move, and cannot declare a charge this turn. If it's not possible to set up the unit within 3" of the TRANSPORT, an Emergency Disembarkation is performed, where the unit is set up within 6" instead, and suffers 1 mortal wound for each roll of 1-3.

### llama-3.1-8b-instant
`finish=stop · 259 compl tok · 1.0s`

[Ruling] → [Destroyed Transports] → [Core_Rules] → [Reasoning]

When a Transport is destroyed with units still embarked, the passengers must immediately disembark before the Transport is removed from the battlefield. The disembarking process is described in the Destroyed Transports rule.

According to the rule, units that disembark from a destroyed Transport model are not affected by that model's Deadly Demise ability. Instead, the controlling player must roll one D6 for each disembarking model. For each roll of 1, that disembarking model's unit suffers 1 mortal wound.

Additionally, the disembarking unit is Battle-shocked until the start of its controlling player's next Command phase and counts as having made a Normal move this turn, and cannot declare a charge this turn.

Emergency Disembarkation is triggered if a disembarking unit cannot be set up wholly within 3" of the destroyed Transport model and not within Engagement Range of any enemy models. In this case, the unit must perform an Emergency Disembarkation, which is similar to the standard disembarkation process but with some modifications.

Therefore, the passengers of a destroyed Transport can take damage during the disembarkation process, but they are not affected by the Transport's Deadly Demise ability.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 224 compl tok · 1.0s`

Destroyed Transports → Destroyed Transports [1] → When a TRANSPORT model is destroyed, any units embarked within that TRANSPORT model must immediately disembark before that TRANSPORT model is removed from the battlefield. Units that disembark from a destroyed TRANSPORT model are not affected by that model's Deadly Demise ability. Instead, you must roll one D6 for each disembarking model. For each roll of 1, that disembarking model's unit suffers 1 mortal wound. 

[Ruling] → The units disembark wholly within 3" of the TRANSPORT model and not within Engagement Range of any enemy models, if possible. If not, they perform an Emergency Disembarkation, setting up wholly within 6" of the TRANSPORT model. 

[Reasoning] → According to the Destroyed Transports rule [1], when a TRANSPORT is destroyed, embarked units disembark and may take damage based on a D6 roll. The Emergency Disembarkation clause allows units to disembark within 6" if they cannot be set up within 3".

### openai/gpt-oss-120b
`finish=stop · 787 compl tok · 3.1s`

**Ruling**  
When a TRANSPORT model is destroyed while it still has units embarked, those units must **immediately disembark**. Each model that disembarks is set up **wholly within 3" of the destroyed TRANSPORT** (or, if that is impossible, performs an **Emergency Disembarkation** and is set up wholly within 6") and must not be within Engagement Range of any enemy models. For each disembarking model the controlling player rolls one D6; **each roll of 1 inflicts 1 mortal wound** on that model’s unit. The disembarking units are **not affected by the transport’s Deadly Demise** ability. In addition, the disembarking units are **Battle‑shocked until the start of their controller’s next Command phase**, **count as having made a Normal move for the turn**, and **cannot declare a charge this turn**.

**Rule Citation**  
- *Destroyed Transports* (Core Rules – Wahapedia): “If a TRANSPORT model is destroyed, any units embarked within that TRANSPORT model must immediately disembark … Roll one D6 for each disembarking model. For each roll of 1, that disembarking model's unit suffers 1 mortal wound. … Until the start of its controlling player's next Command phase, that unit is Battle‑shocked. Until the end of the turn, that unit counts as having made a Normal move this turn, and cannot declare a charge this turn.”  
- *Emergency Disembarkation* (same entry): “If it is not possible to set up a disembarking unit wholly within 3" … the unit must instead perform an Emergency Disembarkation … must be set up wholly within 6" … and suffers 1 mortal wound for each roll of 1‑3 (instead of each roll of 1). If a disembarking model still cannot be set up, that model is destroyed.”

**Reasoning**  
The *Destroyed Transports* rule explicitly overrides the normal *Disembark* rule for the case of a destroyed transport. It dictates the required placement (within 3", or 6" for emergency), the mortal‑wound roll (1 on a D6 per model, or 1‑3 on a D6 for emergency), and the subsequent effects (Battle‑shocked, counts as Normal move, cannot charge). It also states that the transport’s Deadly Demise does **not** apply to units disembarking from a destroyed transport, so the only damage they can take at this moment is from the disembarkation roll described above.

### openai/gpt-oss-20b
`finish=stop · 1444 compl tok · 2.3s`

**Ruling**  
When a TRANSPORT model is destroyed while it still has embarked units, those units must disembark immediately before the transport is removed from play. They do so by following the *Destroyed Transports* rule: each disembarking model rolls one D6; for every roll of **1** that model’s unit suffers **1 mortal wound**. The unit is then Battle‑shocked until the start of its controlling player’s next Command phase, counts as having made a Normal move for the rest of the turn, and cannot declare a charge this turn.  

If a unit cannot be set up wholly within 3" of the destroyed transport, it must perform an **Emergency Disembarkation**: it is set up wholly within 6" of the transport and not within Engagement Range of any enemy models, and it rolls one D6 per model but suffers a mortal wound for each roll of **1‑3**. If a model still cannot be set up, it is destroyed.  

The transport’s *Deadly Demise* ability does **not** affect the disembarking units. The Deadly Demise roll (if the transport has it) is made before any units disembark, but the rule explicitly states that “Units that disembark from a destroyed TRANSPORT model are not affected by that model’s Deadly Demise ability.” Therefore the only damage the passengers can take is from the D6 roll(s) described above (or the Emergency Disembarkation rule if applicable).

**Rule Citations**  
- *Destroyed Transports* – “If a TRANSPORT model is destroyed, any units embarked within that TRANSPORT model must immediately disembark … Roll one D6 for each disembarking model. For each roll of 1, that disembarking model’s unit suffers 1 mortal wound …”  
- *Disembark* – “If a unit disembarks from a TRANSPORT model … set it up wholly within 3" of that TRANSPORT model …”  
- *Emergency Disembarkation* – “If a TRANSPORT model is destroyed and it is not possible to set up a disembarking unit wholly within 3" … the unit must instead perform an Emergency Disembarkation … suffer 1 mortal wound for each roll of 1‑3.”  
- *Deadly Demise* – “When such a model is destroyed, roll one D6 before removing it from play … On a 6, each unit within 6" of that model suffers mortal wounds …” (but *Destroyed Transports* overrides this for disembarking units).

### allam-2-7b
`finish=stop · 974 compl tok · 8.2s`

---


====================================================================================================
## [8] CORE · mp=OFF · ctx 2570 tok

**Q:** Can a unit that Advanced still shoot Assault weapons, and is it allowed to declare a charge in the same turn?

**Expected concepts (ground-truth anchors):** [['assault'], ['advance'], ['charge']]

<details><summary>rules context sent to every model</summary>

```
[1] Assault ()
# Assault
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Assault weapons fire so indiscriminately that they can be shot from the hip as warriors dash forward.
Weapons with [ASSAULT] in their profile are known as Assault weapons. If a unit that Advanced this turn contains any models equipped with Assault weapons, it is still eligible to shoot in this turn's Shooting phase. When such a unit is selected to shoot, you can only resolve attacks using Assault weapons its models are equipped with.
Can be shot even if the bearer's unit Advanced.

---

[2] SHOOTING PHASE ()
# SHOOTING PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Use the following sequence when a unit shoots.
1. SELECT ELIGIBLE UNIT
2. SELECT TARGETS
3. MAKE RANGED ATTACKS
4. REPEAT FOR NEXT ELIGIBLE UNIT
In your Shooting phase, if you have one or more eligible units from your army on the battlefield, you can select those units, one at a time, and shoot with them. Each unit can only be selected to shoot once per phase. Once all of the units you selected have shot, progress to your Charge phase. A unit is eligible to shoot unless any of the following apply:
- That unit Advanced this turn.
- That unit Fell Back this turn.
Unless at least one model in a unit has an eligible target for one or more of its ranged weapons, that model's unit cannot be selected to shoot. Designer's Note: This doesn't change the unit's eligibility to shoot, but it does mean that a unit can't be selected to shoot at nothing, and therefore won't qualify for other rules triggers (e.g. GARGOYLES ' Winged Swarm ability and Dark Pacts)
Guns thunder and shrapnel flies through the air. Bursts of muzzle flare and beams of las-fire illuminate the fog of war, and spent ammunition cartridges litter the battlefield.

---

[3] Pistol ()
# Pistol
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Pistols can be wielded even at point-blank range. Weapons with [PISTOL] in their profile are known as Pistols. If a unit contains any models equipped with Pistols, that unit is eligible to shoot in its controlling player's Shooting phase even while it is within Engagement Range of one or more enemy units. When such a unit is selected to shoot, it can only resolve attacks using its Pistols and can only target one of the enemy units it is within Engagement Range of. In such circumstances, a Pistol can target an enemy unit even if other friendly units are within Engagement Range of the same enemy unit. If a model is equipped with one or more Pistols, unless it is a MONSTER or VEHICLE model, it can either shoot with its Pistols or with all of its other ranged weapons. Declare whether such a model will shoot with its Pistols or its other ranged weapons before selecting targets. Can be shot even if the bearer's unit is within Engagement Range of enemy units, but must target one of those enemy units. Cannot be shot alongside any other non-Pistol weapon (except by a MONSTER or VEHICLE).

---

[4] Advance Moves ()
# Advance Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Advances, make an Advance roll for that unit by rolling one D6. Add the result in inches to the Move characteristic of each model in that unit until the end of the phase. Each model in that unit can then make an Advance move by moving a distance in inches less than or equal to this total, but no model can be moved within Engagement Range of enemy models. A unit cannot shoot or declare a charge in the same turn that it Advanced.
Advance Move: Models move up to M+D6". Cannot move within Engagement Range of any enemy models. Units that Advance cannot shoot or charge this turn.

---

[5] Make Ranged Attacks ()
# Make Ranged Attacks
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The shooting unit's models now make attacks using their ranged weapons. Each time a model shoots with a ranged weapon, it will make a number of attacks equal to the Attacks (A) characteristic in that weapon's profile. You make one Hit roll for each attack being made (see Making Attacks). If you selected more than one target for your unit to shoot at, you must resolve all of the attacks against one target before moving on to the next target. If your unit is shooting more than one ranged weapon at a target, and those weapons have different profiles, then after you have resolved attacks with one of those weapons you must, if any other weapons with the same profile are also being shot at that unit, resolve those attacks before resolving any other attacks against the target. Note that, provided at least one model in the target unit was visible to an attacking model and in range of that attacking model's weapon when that target unit was selected, that weapon's attacks can still be made, even if no models in the target unit remain visible to or in range of it when you come to resolve those attacks (for example, because models in the target unit have already been destroyed by attacks made with other weapons in the attacking model's unit).
When a model shoots a weapon, it makes a number of attacks equal to that weapon's Attacks characteristic. Resolve all attacks against one unit before resolving attacks against any other unit. Resolve all attacks made with the same weapon profile before resolving attacks with any other profile. If a weapon was in range and its target was visible when selected, that weapon's attacks can always be made.
Locked in Combat A unit is not eligible to shoot while it is within Engagement Range of one or more enemy units. While an enemy unit is within Engagement Range of one or more units from your army, you cannot select that enemy unit as a target of ranged weapons. MONSTER and VEHICLE units are exceptions to these rules, as described in the Big Guns Never Tire section. Units cannot shoot while within Engagement Range of enemy units. Units cannot shoot at targets within Engagement Range of friendly units.
STEALTH Some warriors are masters of disguise and concealment. If every model in a unit has this ability, then each time a ranged attack is made against it, subtract 1 from that attack's Hit roll.

---

[6] Big Guns Never Tire ()
# Big Guns Never Tire
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Monsters and war engines can dispense death from afar even as they trample the masses before them. MONSTER and VEHICLE units are eligible to shoot in their controlling player's Shooting phase even while they are within Engagement Range of one or more enemy units. Ranged weapons equipped by MONSTER and VEHICLE units can target one or more of the enemy units they are within Engagement Range of, even if other friendly units are also within Engagement Range of the same enemy unit. Each time a MONSTER or VEHICLE unit makes a ranged attack, if that unit was within Engagement Range of one or more enemy units when it selected its targets, unless that attack is made with a Pistol, subtract 1 from that attack's Hit roll. You can select an enemy MONSTER or VEHICLE unit within Engagement Range of one or more units from your army as a target of ranged weapons. Each time a model from your army makes a ranged attack against such a target, unless that attack is made with a Pistol, subtract 1 from that attack's Hit roll. Designer's Note: A unit that is within Engagement Range of an enemy MONSTER or VEHICLE unit is still not eligible to shoot, and so cannot make ranged attacks against that MONSTER or VEHICLE unit (unless that unit is eligible to shoot even while within Engagement Range of enemy units, e.g. it is itself a MONSTER or VEHICLE unit, or its models are equipped with Pistols). Other units from your army that are eligible to shoot can, however, target and shoot that enemy MONSTER or VEHICLE unit. MONSTERS and VEHICLES can shoot, and be shot at, even while they are within Engagement Range of enemy units. Each time a ranged attack is made by or against such a unit, subtract 1 from th
```
</details>


### qwen/qwen3-32b
`finish=stop · 506 compl tok · 1.6s`

[Ruling] A unit that Advanced this turn can still shoot Assault weapons in the Shooting phase but cannot declare a charge in the same turn.  
[Rule Citation 1] **Assault** (Core Rules) → Units with Assault weapons remain eligible to shoot after Advancing.  
[Rule Citation 2] **Advance Moves** (Core Rules) → Units that Advanced "cannot shoot or declare a charge in the same turn."  
[Reasoning] The Assault rule explicitly allows shooting Assault weapons after Advancing, but the Advance Moves rule universally prohibits declaring a charge in the same turn. These rules do not conflict, as Assault weapons are an exception to the general shooting restriction, but the charge prohibition applies regardless of weapon type.

### qwen/qwen3.6-27b
`finish=stop · 1540 compl tok · 3.5s`

[Ruling] Yes, a unit that Advanced can still shoot Assault weapons, but it cannot declare a charge in the same turn.

[Rule Citation] Assault (Wahapedia_Core_Rules); Advance Moves (Wahapedia_Core_Rules); CHARGE PHASE (Wahapedia_Core_Rules)

[Reasoning] The Assault rule explicitly overrides the general Advance restriction for shooting, stating: "If a unit that Advanced this turn contains any models equipped with Assault weapons, it is still eligible to shoot in this turn's Shooting phase. When such a unit is selected to shoot, you can only resolve attacks using Assault weapons its models are equipped with." However, the Advance Moves rule clearly states that "A unit cannot shoot or declare a charge in the same turn that it Advanced," and the CHARGE PHASE rule confirms that a unit is ineligible to charge if "That unit Advanced or Fell Back this turn." Because the Assault keyword only provides a specific exception to the shooting restriction and does not mention charging, the unit remains strictly prohibited from declaring a charge in the same turn it Advanced.

### llama-3.3-70b-versatile
`finish=stop · 136 compl tok · 47.9s`

[Ruling] → A unit that Advanced can still shoot with Assault weapons, but it is not allowed to declare a charge in the same turn.
[Rule Citation] → [1] Assault, [4] Advance Moves, and [7] CHARGE PHASE.
[Reasoning] → According to [1] Assault, a unit that Advanced can still shoot with Assault weapons. However, [4] Advance Moves states that a unit that Advanced cannot declare a charge in the same turn. This is further reinforced by [7] CHARGE PHASE, which lists "That unit Advanced or Fell Back this turn" as a condition that makes a unit ineligible to charge.

### llama-3.1-8b-instant
`finish=stop · 199 compl tok · 0.9s`

[Ruling] → [Advance Moves] → [Reasoning]

A unit that Advanced cannot shoot or declare a charge in the same turn that it Advanced. This is explicitly stated in [Advance Moves] (Source: Wahapedia_Core_Rules).

[Ruling] → [Advance Moves] → [Reasoning]

A unit that Advanced cannot shoot or declare a charge in the same turn that it Advanced. This is explicitly stated in [Advance Moves] (Source: Wahapedia_Core_Rules).

[Ruling] → [Assault] → [Reasoning]

However, a unit that Advanced can still shoot Assault weapons in the same turn, as stated in [Assault] (Source: Wahapedia_Core_Rules). This is an exception to the general rule that a unit cannot shoot or declare a charge in the same turn that it Advanced.

Therefore, the answer is: a unit that Advanced can still shoot Assault weapons, but it cannot declare a charge in the same turn.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 136 compl tok · 2.0s`

A unit that Advanced this turn is not eligible to declare a charge in the same turn → [CHARGE PHASE] → A unit is eligible to charge if it is within 12" of one or more enemy units in your Charge phase, unless any of the following apply: - That unit Advanced or Fell Back this turn.

However, a unit that Advanced this turn can still shoot Assault weapons → [Assault] → If a unit that Advanced this turn contains any models equipped with Assault weapons, it is still eligible to shoot in this turn's Shooting phase. 

So, to summarize: 
- The unit can shoot Assault weapons.
- The unit cannot declare a charge.

### openai/gpt-oss-120b
`finish=stop · 638 compl tok · 2.0s`

**Ruling**  
- A unit that Advanced may still fire its Assault weapons in the same turn.  
- The same unit may **not** declare a charge in that turn.

**Rule Citations**  
1. **Assault** – “If a unit that Advanced this turn contains any models equipped with Assault weapons, it is still eligible to shoot in this turn's Shooting phase… Can be shot even if the bearer's unit Advanced.” (Rule [1])  
2. **Advance Moves** – “A unit cannot shoot or declare a charge in the same turn that it Advanced.” (Rule [4])  

**Reasoning**  
- The general eligibility rule in **Shooting Phase** ([2]) states that a unit that Advanced is *normally* ineligible to shoot. However, the **Assault** rule explicitly overrides this restriction for Assault weapons, granting eligibility to shoot even after advancing. Therefore, the unit may fire its Assault weapons.  
- No rule provides an exception for charging after an Advance. The **Advance Moves** rule unambiguously prohibits both shooting *and* declaring a charge for a unit that Advanced. Since there is no overriding errata or special ability that changes this, the unit cannot declare a charge in the same turn it Advanced.

### openai/gpt-oss-20b
`finish=stop · 589 compl tok · 1.9s`

**Ruling**  
A unit that Advanced can still shoot its Assault weapons, but it cannot declare a charge in the same turn.

**Rule Citations**  
- [1] Assault – “If a unit that Advanced this turn contains any models equipped with Assault weapons, it is still eligible to shoot in this turn’s Shooting phase.”  
- [7] Charge Phase – “A unit is eligible to charge … unless any of the following apply: *That unit Advanced or Fell Back this turn.*”

**Reasoning**  
The Assault rule explicitly overrides the general Shooting Phase rule that normally disqualifies units that Advanced from shooting. Therefore, a unit that Advanced remains eligible to shoot its Assault weapons.  
Conversely, the Charge Phase rule lists “Advanced” as a condition that disqualifies a unit from charging. Since the unit has Advanced, it is not eligible to declare a charge in that turn.

### allam-2-7b
`finish=stop · 854 compl tok · 1.0s`


























































































































































































































































































































































































































































































































































































































































































































































































































































































====================================================================================================
## [9] CORE · mp=OFF · ctx 1407 tok

**Q:** In the Fight phase, when both players have units in combat and one unit has Fights First, what is the order in which units fight?

**Expected concepts (ground-truth anchors):** [['fights first'], ['whose turn is not taking place', 'alternat', 'pile in']]

<details><summary>rules context sent to every model</summary>

```
[1] FIGHT PHASE ()
# FIGHT PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The Fight phase is split into two steps. Units that have the ability to Fight First do so, followed by any remaining eligible units.
1. FIGHTS FIRST
2. Units that can Fight First do so
3. REMAINING COMBATS
4. Remaining units that can fight do so
In both steps of the Fight phase, players alternate selecting eligible units from their army, one at a time, starting with the player whose turn is not taking place, and fighting with them. Note that a player cannot pass or opt not to fight when they have one or more eligible units that could fight - they must select one of them to fight. In both steps, a unit is eligible to fight if either or both of the following apply: It is within Engagement Range of one or more enemy units. It made a Charge move this turn. No unit can fight more than once in the Fight phase. In each step, if all of one player's eligible units that can fight during that step have fought, the opposing player can then fight with all of their remaining eligible units that can fight during that step, one at a time.
Once neither player has any eligible units to fight with during the current step, you progress to the next step. Once all eligible units have fought in every step, the Fight phase ends. The player's turn then ends and, unless the battle ends, the next player's turn begins. Note that after an enemy unit has fought and finished its Consolidation move, it might be that previously ineligible units are now eligible - these units can then be selected to fight during the Remaining Combats step.
Carnage engulfs the battlefield as the warring armies meet head-on. Fangs and claws crunch through bone. Blades ring like hammers on anvils. Blood spurts and flesh tears as hate-filled foes tear one another apart.

---

[2] 2. Remaining Combats ()
# 2. Remaining Combats
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In this step, all remaining eligible units fight. This includes any units with the Fights First ability that were not eligible to fight at the start of the Fight phase, but have since become eligible to fight.

---

[3] 1. Fights First ()
# 1. Fights First
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In this step, all eligible units with the Fights First ability fight. Remember that this will include units that made a Charge move this turn and that have a Charge bonus.
FIGHTS FIRST Some warriors attack with blinding speed, landing their blows before their foes can react. Units with this ability that are eligible to fight do so in the Fights First step, provided every model in the unit has this ability.

---

[4] Declare Battle Formations ()
# Declare Battle Formations
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In the order stated below, both players now secretly note down: Which of their Leader units will start the battle attached (they must specify which Leader unit is attached to which Bodyguard unit). Which of their units will start the battle embarked within TRANSPORT models (they must specify which units are embarked within which models). Which of their units will start the battle in Reserves (including Strategic Reserves). When both players have done so, they declare their selections to their opponent.

---

[5] Fight ()
# Fight
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When you select a unit to fight, it first Piles In, then its models make melee attacks, then the unit Consolidates.
C After the Termagants have made all of their attacks, one enemy model has been destroyed. The Termagants now Consolidate; just like when they Piled In, each model must move up to 3" in order to end closer to the closest enemy model, and in base-to-base contact if they can. Three Termagants are already in base-to-base contact, and so are not moved.
Use the following sequence when a unit fights.
1. PILE IN
2. MAKE MELEE ATTACKS
3. Select weapon
4. Select targets
5. Make attacks
6. CONSOLIDATE

---

[6] COMMAND PHASE ()
# COMMAND PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Your Command phase is split into two steps. In the first, both players gain 1 Command point (CP) and you resolve any other Command phase rules; in the second, you test to see if any of your units are Battle-shocked.
1. COMMAND
2. BATTLE-SHOCK
Commanders gauge the flow of the battle, consolidating their objectives before making alterations to their battle plans and devising new tactics and strategies with which to defeat the foe.

---

[7] Which Models Fight ()
# Which Models Fight
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit makes its melee attacks, only models in that unit that are either within Engagement Range of an enemy unit, or in base-to-base contact with another model from their own unit that is itself in base-to-base contact with an enemy unit, can fight.
A model can fight if it is within Engagement Range of an enemy unit. A model can fight if it is in base-to-base contact with another model from its own unit that is itself in base-to-base contact with an enemy unit.

---

[8] Sequencing ()
# Sequencing
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

While playing Warhammer 40,000, you'll occasionally find that two or more rules are to be resolved at the same time. If this occurs during the battle, the player whose turn it is chooses the order. If this occurs before or after the battle, or at the start or end of a battle round, the players roll off and the winner decides the order in which those rules are resolved.
```
</details>


### qwen/qwen3-32b
`finish=stop · 1260 compl tok · 2.8s`

[Ruling] In the Fight phase, units with the **Fights First** ability fight in the **Fights First step**, followed by all remaining eligible units in the **Remaining Combats step**. If both players have units in combat but only one unit has **Fights First**, that unit fights first in the Fights First step, and the other player’s units (without Fights First) fight in the Remaining Combats step.  

[Rule Citation]  
- **Fights First** (Core Rules, [3]) → Units with this ability fight in the Fights First step.  
- **Remaining Combats** (Core Rules, [2]) → All remaining eligible units fight in this step.  
- **Fight Phase** (Core Rules, [1]) → Units alternate selection starting with the non-turn player, but cannot pass if they have eligible units.  

[Reasoning]  
The Fights First step prioritizes units with the **Fights First** ability. Once these units have fought, the Remaining Combats step handles all other eligible units. Since the question specifies only one unit has Fights First, it resolves first, and the other player’s units resolve afterward in the Remaining Combats step. The exact selection order within each step depends on whose turn it is (non-turn player selects first if they have eligible units), but the key distinction is the two-step sequence: Fights First → Remaining Combats.

### qwen/qwen3.6-27b
`finish=stop · 1741 compl tok · 3.7s`

[Ruling] The Fight phase is resolved in two sequential steps: first, all eligible units with the Fights First ability fight, followed by all remaining eligible units. Within each step, players alternate selecting eligible units one at a time, starting with the player whose turn it is not. If one player exhausts all of their eligible units during a step, the opposing player may then fight with all of their remaining eligible units for that step before the phase progresses.

[Rule Citation] Core Rules: "FIGHT PHASE", "1. Fights First", and "2. Remaining Combats" (Source: Wahapedia_Core_Rules)

[Reasoning] The Fight Phase rules explicitly split the phase into the Fights First step and the Remaining Combats step. In the Fights First step, only eligible units that possess the Fights First ability (including those that made a Charge move) fight. In the Remaining Combats step, all other eligible units fight, which also includes any Fights First units that were ineligible at the start of the phase but became eligible later. During both steps, players must alternate selecting eligible units one at a time, beginning with the non-active player, and cannot pass if they have eligible units. If a player has no eligible units left to select in a given step, the opposing player resolves all of their remaining eligible units for that step. Once neither player has eligible units for the current step, play progresses to the next step.

### llama-3.3-70b-versatile
`finish=stop · 208 compl tok · 48.1s`

[Ruling] → The order in which units fight in the Fight phase is as follows: units with the Fights First ability fight first, followed by the remaining eligible units. 
→ [Rule Citation] This is stated in the FIGHT PHASE rule (**Source:** Wahapedia_Core_Rules), which says: "The Fight phase is split into two steps. Units that have the ability to Fight First do so, followed by any remaining eligible units."
→ [Reasoning] The FIGHT PHASE rule explicitly states that units with the Fights First ability fight in the first step, and then the remaining eligible units fight in the second step. This order is further clarified in the 1. Fights First rule (**Source:** Wahapedia_Core_Rules), which states that units with the Fights First ability fight in the Fights First step, and the 2. Remaining Combats rule (**Source:** Wahapedia_Core_Rules), which states that all remaining eligible units fight in the Remaining Combats step.

### llama-3.1-8b-instant
`finish=stop · 54 compl tok · 0.4s`

→ FIGHT PHASE → [1] Core_Rules, Wahapedia_Core_Rules

In the Fight phase, the order in which units fight is as follows: Units that have the ability to Fight First do so, followed by any remaining eligible units.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 255 compl tok · 1.0s`

The order in which units fight in the Fight phase when both players have units in combat and one unit has Fights First is as follows:

1. **Fights First step**: Units with the Fights First ability that are eligible to fight do so. This includes units that made a Charge move this turn and have a Charge bonus. [1] FIGHT PHASE → [3] 1. Fights First → [Source: Wahapedia_Core_Rules]

2. After the Fights First step, the **Remaining Combats step** begins. In this step, all remaining eligible units fight. This includes any units with the Fights First ability that were not eligible to fight at the start of the Fight phase but have since become eligible to fight. [2] 2. Remaining Combats → [Source: Wahapedia_Core_Rules]

In both steps, players alternate selecting eligible units from their army, one at a time, starting with the player whose turn is not taking place, and fighting with them. A player cannot pass or opt not to fight when they have one or more eligible units that could fight; they must select one of them to fight. [1] FIGHT PHASE → [Source: Wahapedia_Core_Rules]

### openai/gpt-oss-120b
`finish=stop · 818 compl tok · 3.1s`

**Ruling**  
1. The Fight phase is divided into two steps.  
2. In the first step (**Fights First**) only units that have the *Fights First* ability and are eligible to fight may be selected.  
3. Players alternate selecting which eligible unit fights, beginning with the player whose turn is **not** taking place.  
4. Once all eligible *Fights First* units have fought, the phase moves to the second step (**Remaining Combats**).  
5. In the **Remaining Combats** step all other eligible units (including any *Fights First* units that have become eligible later) fight, again alternating selections starting with the non‑active player.  

**Rule Citation**  
- **Fight Phase** – “The Fight phase is split into two steps… In both steps of the Fight phase, players alternate selecting eligible units from their army, one at a time, **starting with the player whose turn is not taking place**… Once neither player has any eligible units to fight with during the current step, you progress to the next step.” [Source: Wahapedia_Core_Rules – Fight Phase]  
- **1. Fights First** – “In this step, all eligible units with the *Fights First* ability fight… provided every model in the unit has this ability.” [Source: Wahapedia_Core_Rules – 1. Fights First]  
- **2. Remaining Combats** – “In this step, all remaining eligible units fight. This includes any units with the *Fights First* ability that were not eligible to fight at the start of the Fight phase, but have since become eligible to fight.” [Source: Wahapedia_Core_Rules – 2. Remaining Combats]  

**Reasoning**  
The Fight phase rules explicitly create a two‑step sequence. The first step is reserved for any unit that possesses the *Fights First* keyword and meets the eligibility criteria (within Engagement Range or having charged). During that step, the turn‑order rule for selecting units applies: the non‑active player selects first, then players alternate until no eligible *Fights First* units remain. After that, the phase proceeds to the **Remaining Combats** step, where the same alternating selection order is used for all other eligible units, including any *Fights First* units that have only just become eligible. Thus, the overall order is:

1. All eligible *Fights First* units fight first, alternating selections starting with the non‑active player.  
2. Then all remaining eligible units fight, again alternating selections starting with the non‑active player.

### openai/gpt-oss-20b
`finish=stop · 1477 compl tok · 2.7s`

**Ruling**  
During the Fight phase, the units that fight are ordered in two distinct steps:

1. **Fights‑First step** – All units that have the *Fights First* ability and are eligible to fight do so first.  
   • Players alternate selecting one of their eligible *Fights First* units, one at a time.  
   • The alternation starts with the player whose turn is **not** currently taking place.  
   • If one player has no remaining eligible *Fights First* units, the other player may then fight with all of their remaining eligible units that can fight during that step, one at a time.

2. **Remaining Combats step** – After every eligible *Fights First* unit has fought, the phase proceeds to the Remaining Combats step.  
   • Again, players alternate selecting one of their remaining eligible units (including any units that gained *Fights First* eligibility during the phase).  
   • The alternation again starts with the player whose turn is not taking place.

Once all eligible units have fought in both steps, the Fight phase ends.

**Rule Citations**  
- *Fight Phase* – “The Fight phase is split into two steps… Units that have the ability to Fight First do so, followed by any remaining eligible units.” (Rule 1)  
- *Fights First* – “In this step, all eligible units with the Fights First ability fight… In both steps, players alternate selecting eligible units from their army, one at a time, starting with the player whose turn is not taking place.” (Rule 3)  
- *Remaining Combats* – “In this step, all remaining eligible units fight… In both steps, players alternate selecting eligible units from their army, one at a time, starting with the player whose turn is not taking place.” (Rule 2)

**Reasoning**  
The *Fight Phase* rule establishes that the phase is divided into a *Fights First* step followed by a *Remaining Combats* step.  
The *Fights First* rule specifies that only units with the ability fight in that step and that players alternate selections, beginning with the non‑turn‑taking player.  
The *Remaining Combats* rule repeats the same alternation for the second step, applying to all remaining eligible units (including those that became eligible during the phase).  
Thus, the order is: first all eligible *Fights First* units, alternating between players starting with the non‑turn‑taking player; then all remaining eligible units, again alternating starting with the non‑turn‑taking player.

### allam-2-7b
`finish=stop · 87 compl tok · 0.4s`

In the Fight phase, when both players have units in combat and one unit has Fights First, the order in which units fight is determined by the player whose turn it is. The player with Fights First chooses the order in which units fight. 

Ruling: [Ruling] → Core_Rules → Sequencing → Players roll off and the winner decides the order in which units fight.


====================================================================================================
## [10] CORE · mp=OFF · ctx 2322 tok

**Q:** Does a Battle-shocked unit still control objective markers, and how does being below half-strength affect that unit?

**Expected concepts (ground-truth anchors):** [['battle-shock'], ['objective control', 'objective marker'], ['half-strength']]

<details><summary>rules context sent to every model</summary>

```
[1] 2. Battle-shock ()
# 2. Battle-shock
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In this step, you must take a Battle-shock test for each of your units on the battlefield that is Below Half-strength. To do so, roll 2D6: if the result is greater than or equal to the best Leadership characteristic in that unit, the test is passed; otherwise, the test is failed and, until the start of your next Command phase, that unit is Battle-shocked. While a unit is Battle-shocked:
- The Objective Control characteristic of all of its models is 0.
- If it Falls Back, you must take a Desperate Escape test for every model in that unit.
- Its controlling player cannot use Stratagems to affect that unit.
Once you have taken Battle-shock tests for all of your units that require them, your Command phase ends and you progress to your Movement phase. In this step, if for any reason a unit is forced to take a Battle-shock test for being below its Starting Strength, unless otherwise stated, that unit does not also have to take a Battle-shock test for being Below Half-strength. While a unit is Battle-shocked, all models in that unit are also Battle-shocked.
Take a Battle-shock test for each unit from your army on the battlefield that is Below Half-strength. Roll 2D6: if the result is greater than or equal to the unit's Leadership, the test is passed. Otherwise, the unit is Battle-shocked until the start of your next Command phase. Battle-shocked units have an OC of 0 and their controlling player cannot use Stratagems to affect them. Battle-shocked units must take Desperate Escape tests if they Fall Back.

---

[2] Below Half-strength ()
# Below Half-strength
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some rules will refer to a unit being Below Half-strength.
- If a unit has a Starting Strength of 1, then it is said to be Below Half-strength while its remaining number of wounds is less than half of its Wounds characteristic.
- For any other unit, while the number of models in that unit is less than half of its Starting Strength, that unit is said to be Below Half-strength.

---

[3] Objective Markers ()
# Objective Markers
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Objective markers represent objects of tactical or strategic import that both sides are attempting to secure, such as valuable artefacts, vital supplies or communications nodes. If a mission uses objective markers, it will state where they are located on the battlefield. These can be represented using any suitable marker, but we recommend using round markers that are 40mm in diameter. When setting objective markers up on the battlefield, place them so they are centred on the point specified by the mission. When measuring distances to and from objective markers, measure to and from the closest part of them. Models can move over objective markers as if they were not there, but they cannot end a move on top of an objective marker. At the start of the battle, each objective marker on the battlefield is said to be contested, and so is not controlled by either player. To control an objective marker, a player will first need to move models within range of it. A model is within range of an objective marker if it is within 3" horizontally and 5" vertically of that objective marker. Every model has an Objective Control (OC) characteristic listed on its datasheet. To determine a player's Level of Control over an objective marker, add together the OC characteristics of all the models from that player's army that are within range of that objective marker. A player will control an objective marker at the end of any phase or turn if their Level of Control over it is greater than their opponent's. If both players have the same Level of Control over an objective marker, that objective marker is contested.
A model is within range of an objective marker if within 3" horizontally and 5" vertically. Level of Control: Add together the OC characteristics of all of a player's models within range of the objective marker. An objective marker is controlled by the player with the highest Level of Control over it (in a tie, it is contested). Models cannot end a move on top of an objective marker.

---

[4] Gaining Command Points ()
# Gaining Command Points
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Outside of the 1CP players gain at the start of the Command phase, each player can only gain a total of 1CP per battle round, regardless of the source (this includes other CP gained at the start of the Command phase). Starting Strength The number of models a unit contains when it is added to your army is known as its Starting Strength. Below Half-strength Some rules will refer to a unit being Below Half-strength. If a unit has a Starting Strength of 1, then it is said to be Below Half-strength while its remaining number of wounds is less than half of its Wounds characteristic. For any other unit, while the number of models in that unit is less than half of its Starting Strength, that unit is said to be Below Half-strength. Destroyed Throughout a battle, models will suffer damage and be destroyed. When a model is destroyed, it is removed from the battlefield. When every model in a unit has been destroyed, that unit is destroyed. Attached Units Some CHARACTER units have the Leader ability, which lets them merge with other units (known as Bodyguard units) to form an Attached unit. The Starting Strength of an Attached unit is equal to the combined Starting Strengths of all of its units (i.e. the number of models in the Leader unit added to the number of models in the Bodyguard unit). If either the Leader unit or the Bodyguard unit in an Attached unit is destroyed, the Starting Strength of the remaining unit is changed to be equal to its original Starting Strength. Example: A Primaris Captain (Starting Strength 1) is attached to a unit of Intercessors (Starting Strength 5). This Attached unit has a Starting Strength of 6. If all the Intercessors are destroyed, the remaining Primaris Captain would revert to having a Starting Strength of 1. For the purposes of rules that are triggered when a unit is destroyed, such rules are still triggered when one of the individual units that made up an Attached unit is destroyed (the Leader or the Bodyguard unit). Example: If a rule awards you with 1VP each time an enemy unit is destroyed, and you target an Attached unit, you would gain 1VP if the Bodyguard unit is destroyed and 1VP if the Leader unit is destroyed (for a total of 2VP).

---

[5] COMMAND PHASE ()
# COMMAND PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Your Command phase is split into two steps. In the first, both players gain 1 Command point (CP) and you resolve any other Command phase rules; in the second, you test to see if any of your units are Battle-shocked.
1. COMMAND
2. BATTLE-SHOCK
Commanders gauge the flow of the battle, consolidating their objectives before making alterations to their battle plans and devising new tactics and strategies with which to defeat the foe.

---

[6] 'Surge' Moves ()
# 'Surge' Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some rules enable units to make out-of-phase 'surge' moves when a certain trigger occurs (e.g. Khorne Berzerkers ' Blood Surge ability, triggered after one or more of their models are destroyed by enemy ranged attacks). Unless otherwise stated, the following restrictions apply to all such moves:
- Each unit can only make one 'surge' move per phase.
- A unit cannot make a 'surge' move while it is Battle-shocked.
- A unit cannot make a 'surge' move while it is within Engagement Range of one or more enemy units.

---

[7] CHARGE PHASE ()
# CHARGE PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Use the following sequence to charge with your units.
1. SELECT ELIGIBLE UNIT
2. SELECT TARGETS
3. MAKE CHARGE ROLL
4. MAKE CHARGE MOVE
5. REPEAT FOR NEXT ELIGIBLE UNI
```
</details>


### qwen/qwen3-32b
`finish=stop · 594 compl tok · 4.0s`

[Ruling] A Battle-shocked unit cannot control objective markers because all models in the unit have their Objective Control (OC) characteristic set to 0. Being Below Half-strength triggers a Battle-shock test, which may result in the unit becoming Battle-shocked and losing OC contributions.  

[Rule Citation]  
- **Battle-shock (Core Rules)**: "While a unit is Battle-shocked: [...] The Objective Control characteristic of all of its models is 0."  
- **Objective Markers (Core Rules)**: "To determine a player's Level of Control over an objective marker, add together the OC characteristics of all the models from that player's army that are within range of that objective marker."  

[Reasoning]  
1. **Battle-shocked units lose OC**: The explicit rule in the Battle-shock step states that all models in a Battle-shocked unit have their OC set to 0. This directly prevents them from contributing to objective control.  
2. **Below Half-strength triggers Battle-shock**: A unit Below Half-strength must take a Battle-shock test. If it fails, it becomes Battle-shocked (and thus loses OC contributions). If it passes, its OC remains unaffected. The connection between Below Half-strength and Battle-shock is defined in the Battle-shock rule.  

No other rules in the provided context override this interaction.

### qwen/qwen3.6-27b
`finish=stop · 1882 compl tok · 8.0s`

[Ruling] A Battle-shocked unit does not contribute to controlling objective markers, as its models' Objective Control (OC) characteristic is reduced to 0. Being Below Half-strength forces the unit to take a mandatory Battle-shock test in the Command phase.

[Rule Citation] Battle-shock (Core Rules), Objective Markers (Core Rules), Below Half-strength (Core Rules)

[Reasoning] The Battle-shock rule explicitly states: "While a unit is Battle-shocked: The Objective Control characteristic of all of its models is 0." Since the Objective Markers rule dictates that a player's Level of Control is determined by adding together the OC characteristics of all models within range of the marker, a Battle-shocked unit contributes nothing to that total and therefore cannot help control the marker. Regarding Below Half-strength, the Battle-shock rule mandates that "you must take a Battle-shock test for each of your units on the battlefield that is Below Half-strength" during the Command phase. Failing this test causes the unit to become Battle-shocked until the start of your next Command phase, applying the OC 0 penalty and other restrictions listed in the rule.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 187 compl tok · 0.9s`

[Ruling] → [Rule Citation] → [Reasoning]

A Battle-shocked unit does not control objective markers. → [3] Objective Markers → While a unit is Battle-shocked: The Objective Control characteristic of all of its models is 0.

Being below half-strength does not directly affect a unit's ability to control objective markers. However, it does trigger a Battle-shock test, which may result in the unit becoming Battle-shocked. → [2] Below Half-strength → In this step, you must take a Battle-shock test for each of your units on the battlefield that is Below Half-strength. → [1] 2. Battle-shock → While a unit is Battle-shocked: The Objective Control characteristic of all of its models is 0.

Therefore, a unit that is below half-strength may become Battle-shocked, which would prevent it from controlling objective markers.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 240 compl tok · 1.3s`

[Ruling] → A Battle-shocked unit does not control objective markers because its Objective Control (OC) characteristic is 0. Being Below Half-strength does not directly affect a unit's control of objective markers; however, it triggers a Battle-shock test, which can lead to the unit being Battle-shocked and thus losing control.

→ [Battle-shock] → A unit that is Battle-shocked has an OC of 0 [2. Battle-shock].

→ [Objective Markers] → To control an objective marker, add together the OC characteristics of all models from that player's army within range of that objective marker [3. Objective Markers].

→ [Below Half-strength] → A unit is Below Half-strength if it has fewer models than half of its Starting Strength (or, for units with a Starting Strength of 1, if its remaining wounds are less than half of its Wounds characteristic) [2. Below Half-strength].

The provided rules do not explicitly state how being Below Half-strength affects control of objective markers directly, but they do show that a Battle-shocked unit (which can result from being Below Half-strength) loses control due to its OC being 0.

### openai/gpt-oss-120b
`finish=stop · 599 compl tok · 1.6s`

**Ruling**  
A Battle‑shocked unit does **not** contribute any Objective Control (OC) toward controlling objective markers, because while Battle‑shocked “the Objective Control characteristic of all of its models is 0.” Being Below Half‑strength by itself does **not** alter a unit’s OC; only the Battle‑shock condition changes it.

**Rule Citations**  
- **Battle‑shock** (Core Rules – Wahapedia): “While a unit is Battle‑shocked: – The Objective Control characteristic of all of its models is 0.”【1】  
- **Below Half‑strength** (Core Rules – Wahapedia): defines when a unit is considered Below Half‑strength but gives no effect on OC【2】  
- **Objective Markers** (Core Rules – Wahapedia): OC of models is summed to determine Level of Control over a marker【3】

**Reasoning**  
Objective control is calculated by adding the OC values of all models that are “within range” of the marker (Objective Markers rule). The Battle‑shock rule explicitly sets the OC of every model in a Battle‑shocked unit to 0, so those models add nothing to the total, meaning the unit cannot help control the marker while Battle‑shocked. The Below Half‑strength rule merely describes a unit’s size status and does not modify OC or any other characteristic; therefore, being Below Half‑strength alone has no impact on objective control unless the unit also becomes Battle‑shocked, at which point the OC‑zero effect applies.

### openai/gpt-oss-20b
`finish=stop · 867 compl tok · 2.0s`

**Ruling**  
A unit that is Battle‑shocked cannot control objective markers because its models’ Objective Control (OC) characteristic is set to 0.  Being below half‑strength only matters insofar as it triggers the Battle‑shock test; if the unit fails that test it becomes Battle‑shocked and then loses OC, but the state of “below half‑strength” itself does not directly alter OC.

**Rule Citations**  
- **Battle‑shock** – “While a unit is Battle‑shocked: *The Objective Control characteristic of all of its models is 0*.” (Rule 1)  
- **Objective Markers** – “To determine a player's Level of Control over an objective marker, add together the OC characteristics of all the models from that player's army that are within range of that objective marker.” (Rule 3)  
- **Below Half‑strength** – “For any other unit, while the number of models in that unit is less than half of its Starting Strength, that unit is said to be Below Half‑strength.” (Rule 2)  
- **Battle‑shock test** – “Take a Battle‑shock test for each unit from your army on the battlefield that is Below Half‑strength.” (Rule 1)

**Reasoning**  
1. When a unit is Battle‑shocked, its models’ OC is 0 (Rule 1).  
2. The Level of Control for an objective marker is calculated by summing the OC of all models within range (Rule 3).  
3. Therefore, a Battle‑shocked unit contributes 0 to the Level of Control and cannot control the marker.  
4. The “Below Half‑strength” condition (Rule 2) only determines whether a Battle‑shock test must be taken. It does not itself modify OC; only a failed Battle‑shock test (Rule 1) causes the unit to become Battle‑shocked and lose OC.

### allam-2-7b
`finish=stop · 33 compl tok · 0.3s`

The provided rules do not clearly address this question. I recommend checking the official Warhammer 40k_Rules for a more detailed answer.


====================================================================================================
## [11] LEVIATHAN · mp=ON · ctx 1504 tok

**Q:** Using Tactical Missions in Leviathan, how does the Assassination Secondary Mission score when I destroy enemy Characters, and does a resurrected Character count?

**Expected concepts (ground-truth anchors):** [['assassination'], ['character']]

<details><summary>rules context sent to every model</summary>

```
[1] Secondary Mission deck ()
**ASSASSINATION**
*Secondary Mission*
> The enemy looks to their champions for courage. Identify and eliminate them with extreme prejudice.
If you are using Fixed Missions, then while this Secondary Mission is active, each time an enemy CHARACTER model is destroyed, you score 4VP. If you are using Tactical Missions, then at the end of the turn, if either of the conditions below are satisfied, this Secondary Mission is achieved and you score 5VP: One or more enemy CHARACTER units were destroyed during this turn. All CHARACTER units from your opponent's Army Roster have been destroyed during the battle. Note that if you are using Tactical Missions, this Secondary Mission is achieved even if such a unit was destroyed and then subsequently resurrected for any reason.

---

[2] Secondary Mission deck ()
**NO PRISONERS**
*Secondary Mission*
> Exterminate your enemies.
While this Secondary Mission is active, each time an enemy unit is destroyed, you score 2VP (to a maximum of 5VP). Note that VP are scored even if such a unit is destroyed and then subsequently resurrected for any reason. If you score any VP from this Secondary Mission during a turn, then at the end of that turn this Secondary Mission is achieved.

---

[3] Secondary Mission deck ()
**OVERWHELMING FORCE**
*Secondary Mission*
> Scour the enemy from the face of the battlefield.
While this Secondary Mission is active, each time an enemy unit that started the turn within range of an objective marker is destroyed, you score 3VP (to a maximum of 5VP). Note that VP are scored even if such a unit is destroyed and then subsequently resurrected for any reason. If you score any VP from this Secondary Mission during a turn, then at the end of that turn this Secondary Mission is achieved.

---

[4] Secondary Mission deck ()
**BRING IT DOWN**
*Secondary Mission*
> The opposing army contains numerous heavily armoured units. Take any opportunity to bring them down.
While this Secondary Mission is active, each time an enemy MONSTER or VEHICLE model is destroyed, you score 2VP and an extra 1VP for each of the conditions below that are satisfied (all are cumulative): The destroyed model had a Wounds characteristic of 10+. The destroyed model had a Wounds characteristic of 15+. The destroyed model had a Wounds characteristic of 20+. Note that VP are scored even if such a model is destroyed and then subsequently resurrected for any reason. If you score any VP from this Secondary Mission during a turn, then at the end of that turn this Secondary Mission is achieved. If you are using Tactical Missions, then when this Secondary Mission is achieved you score an extra 1VP. However, if you are using Tactical Missions, you cannot score more than 8VP in total from this Secondary Mission.

---

[5] Begin the Battle ()
# Begin the Battle
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

The first battle round begins. Players continue to resolve battle rounds until the battle ends. At the end of each player's turn, if that player is using Tactical Missions, they can discard one or more of their active Secondary Mission cards. If they do, and if it is not the fifth battle round, that player gains 1CP. This represents high command diverting strategic resources that had been allocated to now-obsolete objectives to instead engage new targets of opportunity. At the end of the third battle round, players generate Gambits.

---

[6] Secondary Mission deck ()
**BEHIND ENEMY LINES**
*Secondary Mission*
> Break through the foe's army and cut off their lines of escape.
At the end of your turn, if two or more units from your army (excluding AIRCRAFT) are wholly within your opponent's deployment zone, this Secondary Mission is achieved and you score 4VP (or 5VP if you are using Tactical Missions). If, at the end of your turn, only one unit from your army (excluding AIRCRAFT) is wholly within your opponent's deployment zone, then this Secondary Mission is still achieved, but in this instance you score 3VP instead of 4VP (or instead of 5VP).

---

[7] Secondary Mission deck ()
**ENGAGE ON ALL FRONTS**
*Secondary Mission*
> This area is of extreme importance. You are to lead an immediate all-out assault to capture it and deny it to our enemy for good.
At the end of your turn, if you have one or more qualifying units (see below) from your army wholly within three or more different table quarters, and those units are all more than 3" away from any other table quarter, this Secondary Mission is achieved and you score 4VP if you have qualifying units in four different table quarters, or 2VP if you have qualifying units in three different table quarters. While a unit is Battle-shocked, it is not a qualifying unit. If, when you draw this Secondary Mission card, you only have one or two qualifying units remaining in your army, you can discard this Secondary Mission card and draw a new Secondary Mission card. If you are using Tactical Missions, then when this Secondary Mission is achieved you score an extra 1VP (for a maximum of 5VP).

---

[8] Secondary Mission deck ()
**STORM HOSTILE OBJECTIVE**
*Secondary Mission*
> Dominate the field of battle. Storm every site of tactical import and leave the foe with no place to hide.
At the end of your turn, if either of the below conditions are satisfied, this Secondary Mission is achieved and you score 4VP if you are using Fixed Missions, or 5VP if you are using Tactical Missions: You control one or more objective markers that were controlled by your opponent at the start of your turn. Your opponent did not control any objective markers at the start of your turn and you control one or more objective markers that you did not control at the start of your turn. This Secondary Mission cannot be achieved during the first battle round; if you randomly drew this Secondary Mission card during the first battle round, draw a new Secondary Mission card and shuffle this Secondary Mission card back into your Secondary Mission deck.
```
</details>


### qwen/qwen3-32b
`finish=stop · 584 compl tok · 1.4s`

[Ruling] While using Tactical Missions, the **Assassination** Secondary Mission scores 5VP at the end of the turn if either of its conditions are met (destroying one or more enemy CHARACTER units during the turn, or destroying all of your opponent's CHARACTER units in the battle). Destroyed enemy CHARACTER models that are later resurrected still count for VP purposes.  

[Rule Citation] **ASSASSINATION** (Secondary Mission deck) → "Note that if you are using Tactical Missions, this Secondary Mission is achieved even if such a unit was destroyed and then subsequently resurrected for any reason."  

[Reasoning] The rule explicitly states that resurrection does not negate VP scored for destroying enemy CHARACTER models under Tactical Missions. The mission is achieved at the end of the turn if the destruction occurred during the turn, regardless of later resurrection.

### qwen/qwen3.6-27b
`finish=stop · 1677 compl tok · 3.7s`

[Ruling] When using Tactical Missions, the Assassination Secondary Mission is achieved at the end of your turn if you destroy one or more enemy CHARACTER units during that turn, or if you have destroyed all enemy CHARACTER units from your opponent's Army Roster during the battle. Upon achieving it, you score 5VP. Yes, a resurrected CHARACTER unit still counts toward achieving this mission.

[Rule Citation] ASSASSINATION Secondary Mission (Secondary Mission deck)

[Reasoning] The provided rule explicitly states that for Tactical Missions, you score 5VP at the end of the turn if either of the two listed conditions are satisfied. It further includes a direct clarification: "Note that if you are using Tactical Missions, this Secondary Mission is achieved even if such a unit was destroyed and then subsequently resurrected for any reason." Therefore, the destruction condition is met regardless of subsequent resurrection, and the mission awards 5VP upon achievement.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 146 compl tok · 1.2s`

[Ruling] → [Rule Citation] → [Reasoning]
You score 5VP each time an enemy CHARACTER model is destroyed. → [ASSASSINATION, Secondary Mission deck ()] → This rule specifies that if you are using Tactical Missions, then at the end of the turn, if either of the conditions below are satisfied, this Secondary Mission is achieved and you score 5VP: One or more enemy CHARACTER units were destroyed during this turn. 

A resurrected Character counts as it was destroyed during the turn. → [ASSASSINATION, Secondary Mission deck ()] → This rule explicitly states that if a unit was destroyed and then subsequently resurrected for any reason, it still counts towards the Secondary Mission.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 252 compl tok · 1.2s`

[Ruling] → The Assassination Secondary Mission scores 5VP at the end of the turn if one or more enemy CHARACTER units were destroyed during that turn or if all CHARACTER units from your opponent's Army Roster have been destroyed during the battle.

→ [Assassination, Secondary Mission deck ()] → 

[Reasoning] According to the provided rule, if you are using Tactical Missions, the Assassination Secondary Mission is achieved and scores 5VP at the end of the turn if either of two conditions are met: 

1. One or more enemy CHARACTER units were destroyed during this turn.
2. All CHARACTER units from your opponent's Army Roster have been destroyed during the battle.

The rule also specifies that this Secondary Mission is achieved even if a unit was destroyed and then subsequently resurrected for any reason. However, this does not affect scoring for destroyed units; it only ensures the mission can still be achieved even if Characters are brought back.

Therefore, destroying enemy Characters counts toward achieving the mission and scoring 5VP. A resurrected Character does count as having been destroyed for the purpose of achieving the mission, but VP are scored only for Characters destroyed during the turn, not for Characters that were resurrected.

### openai/gpt-oss-120b
`finish=stop · 693 compl tok · 1.8s`

**Ruling**  
When playing with Tactical Missions, the Assassination Secondary Mission does **not** award VP each time a CHARACTER model is destroyed. Instead, at the end of your turn you check the listed conditions; if either is met you achieve the mission and score **5 VP**. A CHARACTER that was destroyed and later resurrected still satisfies the “character destroyed” condition.

**Rule Citation**  
- **ASSASSINATION – Secondary Mission (Tactical Missions)** – *Rule [1]*:  
  > “If you are using Tactical Missions, then at the end of the turn, if either of the conditions below are satisfied, this Secondary Mission is achieved and you score 5VP:  
  > 1️⃣ One or more enemy CHARACTER units were destroyed during this turn.  
  > 2️⃣ All CHARACTER units from your opponent's Army Roster have been destroyed during the battle.  
  > Note that if you are using Tactical Missions, this Secondary Mission is achieved even if such a unit was destroyed and then subsequently resurrected for any reason.”

**Reasoning**  
- The rule explicitly changes the scoring method for Tactical Missions: VP are awarded **once per turn** (5 VP) when the end‑of‑turn condition is satisfied, rather than per model destroyed.  
- The “one or more enemy CHARACTER units were destroyed during this turn” clause is satisfied by any destruction of a CHARACTER model, regardless of whether that model later returns to play, as the note expressly states that resurrection does not invalidate the condition.  
- Therefore, destroying an enemy CHARACTER (even if it is later resurrected) allows you to achieve the mission at turn’s end and claim the 5 VP.

### openai/gpt-oss-20b
`finish=stop · 757 compl tok · 1.4s`

**Ruling**  
When you are playing with Tactical Missions, the Assassination Secondary Mission awards **5 Victory Points (VP) at the end of the turn** if either of the following is true:  
1. One or more enemy CHARACTER units were destroyed during that turn.  
2. All CHARACTER units from your opponent’s Army Roster have been destroyed during the battle.  

A CHARACTER that is destroyed and then later resurrected still satisfies the condition, so the VP are awarded even if the unit was resurrected for any reason.

**Rule Citation**  
[1] *Assassination* – “If you are using Tactical Missions, then at the end of the turn, if either of the conditions below are satisfied, this Secondary Mission is achieved and you score 5VP: One or more enemy CHARACTER units were destroyed during this turn. All CHARACTER units from your opponent's Army Roster have been destroyed during the battle. Note that if you are using Tactical Missions, this Secondary Mission is achieved even if such a unit was destroyed and then subsequently resurrected for any reason.”

**Reasoning**  
- The rule explicitly states the VP amount (5VP) and the conditions for achievement under Tactical Missions.  
- It also explicitly notes that the mission is achieved even if a destroyed unit is later resurrected, so resurrection does not negate the VP.  
- No other rule in the provided context conflicts with or modifies this, and Leviathan rules override Core Rules.

### allam-2-7b
`finish=stop · 195 compl tok · 0.5s`

To determine the scoring for the Assassination Secondary Mission when destroying enemy Characters and if a resurrected Character counts, refer to the specific rules for that mission type (Fixed or Tactical Missions). In this case, we are using Tactical Missions.

For Tactical Missions, the Assassination Secondary Mission scoring criteria are as follows:

1. You control one or more objective markers that were controlled by your opponent at the start of your turn.
2. Your opponent did not control any objective markers at the start of your turn.
3. You control one or more objective markers that you did not control at the start of your turn.


In the context of Tactical Missions, when you destroy an enemy Character, a resurrected Character does not count towards the Assassination Secondary Mission scoring. Resurrected Characters are not considered destroyed for scoring purposes.


====================================================================================================
## [12] LEVIATHAN · mp=ON · ctx 1688 tok

**Q:** Under Bring It Down with Tactical Missions, how many VP for destroying a 20-wound Monster, and what is the maximum I can score from it?

**Expected concepts (ground-truth anchors):** [['bring it down'], ['wounds characteristic']]

<details><summary>rules context sent to every model</summary>

```
[1] Secondary Mission deck ()
**BRING IT DOWN**
*Secondary Mission*
> The opposing army contains numerous heavily armoured units. Take any opportunity to bring them down.
While this Secondary Mission is active, each time an enemy MONSTER or VEHICLE model is destroyed, you score 2VP and an extra 1VP for each of the conditions below that are satisfied (all are cumulative): The destroyed model had a Wounds characteristic of 10+. The destroyed model had a Wounds characteristic of 15+. The destroyed model had a Wounds characteristic of 20+. Note that VP are scored even if such a model is destroyed and then subsequently resurrected for any reason. If you score any VP from this Secondary Mission during a turn, then at the end of that turn this Secondary Mission is achieved. If you are using Tactical Missions, then when this Secondary Mission is achieved you score an extra 1VP. However, if you are using Tactical Missions, you cannot score more than 8VP in total from this Secondary Mission.

---

[2] Secondary Mission deck ()
**NO PRISONERS**
*Secondary Mission*
> Exterminate your enemies.
While this Secondary Mission is active, each time an enemy unit is destroyed, you score 2VP (to a maximum of 5VP). Note that VP are scored even if such a unit is destroyed and then subsequently resurrected for any reason. If you score any VP from this Secondary Mission during a turn, then at the end of that turn this Secondary Mission is achieved.

---

[3] Secondary Mission deck ()
**OVERWHELMING FORCE**
*Secondary Mission*
> Scour the enemy from the face of the battlefield.
While this Secondary Mission is active, each time an enemy unit that started the turn within range of an objective marker is destroyed, you score 3VP (to a maximum of 5VP). Note that VP are scored even if such a unit is destroyed and then subsequently resurrected for any reason. If you score any VP from this Secondary Mission during a turn, then at the end of that turn this Secondary Mission is achieved.

---

[4] Determine Victor ()
# Determine Victor
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

At the end of the battle, the player with the most VP is the winner. If the players are tied, the battle is a draw. Each player can score a maximum of 50VP from Primary Missions and/or Gambits (any excess VP awarded are lost) and a maximum of 40VP from Secondary Missions (any excess VP awarded are lost), for a possible total of 90VP. If a player is using Fixed Missions, that player can score a maximum of 20VP from each of the Fixed Mission cards they selected before the battle (any excess VP awarded are lost). If every model in a player's army is painted to a Battle Ready standard, that player is awarded a bonus 10VP. This gives each player a maximum total score of 100VP.

---

[5] Secondary Mission deck ()
**DEPLOY TELEPORT HOMER**
*Secondary Mission*
> An allied fleet approaches ready to launch a full-scale invasion of this planet. If our vanguard forces deploy a series of teleport homers and landing beacons deep within enemy territory, troops aboard our ships will be able to launch a deadly surprise assault from orbit.
In your Shooting phase, you can select one unit from your army that is not Battle-shocked and is eligible to shoot. Until the end of your turn, that unit is not eligible to shoot or declare a charge. At the end of your turn, if that unit is within your opponent's deployment zone, or within 6" of the centre of the battlefield, it deploys a teleport homer at that location, this Secondary Mission is achieved and you score a number of VP depending on where the teleport homer was deployed, as follows: Centre of battlefield = 3VP. Opponent's deployment zone = 4VP if you are using Fixed Missions, or 5VP if you are using Tactical Missions.

---

[6] Secondary Mission deck ()
**ASSASSINATION**
*Secondary Mission*
> The enemy looks to their champions for courage. Identify and eliminate them with extreme prejudice.
If you are using Fixed Missions, then while this Secondary Mission is active, each time an enemy CHARACTER model is destroyed, you score 4VP. If you are using Tactical Missions, then at the end of the turn, if either of the conditions below are satisfied, this Secondary Mission is achieved and you score 5VP: One or more enemy CHARACTER units were destroyed during this turn. All CHARACTER units from your opponent's Army Roster have been destroyed during the battle. Note that if you are using Tactical Missions, this Secondary Mission is achieved even if such a unit was destroyed and then subsequently resurrected for any reason.

---

[7] Primary Mission deck ()
**DEPLOY SERVO-SKULLS**
*Primary Mission*
> This area is littered with valuable relics. Secure these artefacts behind our front lines.
The objective markers that start the battle in No Man's Land are servo-skulls. At the end of each turn, each of these objective markers can be moved up to 6" in any direction by the player that controls it. When moving objective markers, they cannot end that move on top of any other objective marker or model, or inside impassable parts of terrain features (such as the walls of a ruin). In the second, third, fourth and fifth battle rounds: At the end of each turn, the player whose turn it is scores VP as follows: 2VP for each servo-skull that is wholly within 12" of their opponent's deployment zone. 5VP for each servo-skull that is wholly within 6" of their opponent's deployment zone. 8VP for each servo-skull that is wholly within their opponent's deployment zone. Note that these conditions are not cumulative; if more than one applies, the player whose turn it is scores the applicable condition that carries the highest VP reward.

---

[8] Primary Mission deck ()
**PURGE THE FOE**
*Primary Mission*
> Exterminate the enemy. Show them no mercy.
In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 4VP if they control one or more objective markers, and an extra 4VP if they control more objective markers than their opponent controls. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase. At the end of each battle round: At the end of the battle round, each player scores 4VP if one or more enemy units were destroyed that battle round, and an extra 4VP if more enemy units than friendly units were destroyed that battle round. Note that a unit can. if it is returned to the battlefield for any reason, potentially contribute to this Primary Mission several times (assuming it is returned and subsequently destroyed several times over).
```
</details>


### qwen/qwen3-32b
`finish=stop · 1565 compl tok · 3.4s`

[Ruling] Destroying a 20-wound MONSTER/VEHICLE under **Bring It Down** with Tactical Missions scores **5VP** (2VP base + 1VP for 10+, 1VP for 15+, 1VP for 20+). Additionally, achieving the mission grants **1VP** for Tactical Missions, totaling **6VP** for that destruction. However, the **maximum VP** you can score from this Secondary Mission is **8VP** (mission cap).  

[Rule Citation]  
- **Bring It Down** (Secondary Mission deck [1]) → "each time an enemy MONSTER or VEHICLE model is destroyed, you score 2VP and an extra 1VP for each of the conditions below [...] The destroyed model had a Wounds characteristic of 10+/15+/20+."  
- **Bring It Down** → "If you are using Tactical Missions [...] you score an extra 1VP [...] if you are using Tactical Missions, you cannot score more than 8VP in total from this Secondary Mission."  

[Reasoning]  
The 20-wound model satisfies all three Wounds thresholds (10+, 15+, 20+), granting 3 cumulative extra VP (2VP base + 3VP = 5VP). Tactical Missions adds 1VP for achieving the mission, totaling 6VP for that destruction. However, the mission’s total VP is capped at 8VP regardless of how many times it is triggered. For example, destroying two such models would only yield 8VP total (6VP first destruction + 2VP second destruction).

### qwen/qwen3.6-27b
`finish=stop · 1865 compl tok · 3.9s`

[Ruling] Destroying a 20-wound MONSTER scores 5VP. The maximum total VP you can score from this Secondary Mission is 8VP.

[Rule Citation] BRING IT DOWN (Secondary Mission deck)

[Reasoning] The rule states you score a base of 2VP, plus an extra 1VP for each cumulative Wounds threshold met (10+, 15+, and 20+). A 20-wound model meets all three thresholds, so you add every triggered clause: 2VP (base) + 1VP (10+) + 1VP (15+) + 1VP (20+) = 5VP. The rule explicitly caps the total for this mission when using Tactical Missions: "However, if you are using Tactical Missions, you cannot score more than 8VP in total from this Secondary Mission." This 8VP cap applies to all VP earned from the mission, including the extra 1VP awarded when the mission is achieved.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 199 compl tok · 0.6s`

[Ruling] → [Rule Citation] → [Reasoning]

You score 2VP for destroying the Monster, and an extra 1VP for each of the conditions below that are satisfied (all are cumulative): The destroyed model had a Wounds characteristic of 10+. The destroyed model had a Wounds characteristic of 15+. The destroyed model had a Wounds characteristic of 20+. 

Since the destroyed Monster has a Wounds characteristic of 20+, you score an extra 1VP for this condition. 

You also score an extra 1VP for each of the conditions below that are satisfied, but since the Monster only meets one of these conditions, you do not score any additional VP for the 10+ or 15+ Wounds characteristics.

Total VP for destroying the Monster: 2VP + 1VP = 3VP.

The maximum you can score from this Secondary Mission is 8VP, as stated in the Bring It Down Secondary Mission card.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 120 compl tok · 1.1s`

Destroying a 20-wound MONSTER under **BRING IT DOWN** with Tactical Missions: 

→ 2VP (base) + 1VP (10+ Wounds) + 1VP (15+ Wounds) + 1VP (20+ Wounds) = 5VP 

→ [BRING IT DOWN] → [Leviathan Secondary Mission deck]

The maximum you can score from **BRING IT DOWN** under Tactical Missions is 8VP.

→ [BRING IT DOWN] → [Leviathan Secondary Mission deck]

### openai/gpt-oss-120b
`finish=stop · 941 compl tok · 2.4s`

**Ruling**  
- Destroying a 20‑wound Monster while using Tactical Missions scores **6 VP** (2 VP base + 3 VP for the three wound thresholds + 1 VP for achieving the mission).  
- The **maximum** you can ever score from the *Bring It Down* Secondary Mission under Tactical Missions is **8 VP** total.

**Rule Citation**  
- *Bring It Down* (Secondary Mission) – “each time an enemy MONSTER or VEHICLE model is destroyed, you score 2 VP and an extra 1 VP for each of the conditions below that are satisfied (all are cumulative): … 10+ Wounds, 15+ Wounds, 20+ Wounds.”  
- *Bring It Down* – “If you are using Tactical Missions, then when this Secondary Mission is achieved you score an extra 1 VP. However, if you are using Tactical Missions, you cannot score more than 8 VP in total from this Secondary Mission.”  

**Reasoning**  
1. The monster has a Wounds characteristic of 20, so it meets all three listed thresholds (10+, 15+, 20+).  
2. Base score = 2 VP. Each satisfied condition adds 1 VP, giving 3 VP extra. → 2 VP + 3 VP = 5 VP for the destruction.  
3. Because you scored VP from the mission during the turn, the mission is achieved at turn’s end, granting the additional 1 VP specified for Tactical Missions. → 5 VP + 1 VP = 6 VP.  
4. The mission’s own cap for Tactical Missions limits total scoring from *Bring It Down* to 8 VP, so 6 VP is allowed and the absolute maximum you could ever reach from this mission under Tactical Missions is 8 VP.

### openai/gpt-oss-20b
`finish=stop · 1059 compl tok · 1.6s`

**Ruling**  
- Destroying a 20‑wound MONSTER under Tactical Missions awards **5 VP**.  
- The maximum you can score from the *Bring It Down* Secondary Mission is **8 VP**.

**Rule Citation**  
- [1] Secondary Mission deck – *Bring It Down*  
  - “each time an enemy MONSTER or VEHICLE model is destroyed, you score 2VP and an extra 1VP for each of the conditions below that are satisfied (all are cumulative): The destroyed model had a Wounds characteristic of 10+. The destroyed model had a Wounds characteristic of 15+. The destroyed model had a Wounds characteristic of 20+.”  
  - “If you are using Tactical Missions, then when this Secondary Mission is achieved you score an extra 1VP. However, if you are using Tactical Missions, you cannot score more than 8VP in total from this Secondary Mission.”

**Reasoning**  
1. A 20‑wound model satisfies all three wound‑threshold conditions, giving 3 extra VP.  
2. Base VP for destroying a MONSTER/VEHICLE is 2 VP.  
3. 2 VP + 3 VP = **5 VP** for that single destruction.  
4. When the mission is achieved (i.e., you score any VP during a turn), you receive an additional 1 VP for Tactical Missions, bringing the total to 6 VP for that turn.  
5. The rule explicitly limits the total VP from this Secondary Mission to 8 VP, so even if you destroyed multiple qualifying models, you cannot exceed 8 VP overall.

### allam-2-7b
`finish=stop · 250 compl tok · 0.5s`

To determine the victory points for destroying a 20-wound Monster under the Bring It Down mission, we must first identify the applicable victory conditions. In this case, we have:


1. At the end of each battle round, each player scores 4VP if one or more enemy units were destroyed that battle round.
2. At the end of each battle round, each player scores 4VP if more enemy units than friendly units were destroyed that battle round.


For a 20-wound Monster, the maximum victory points you can score is 8VP (4VP from condition 1 and 4VP from condition 2). 


[Ruling] → [Rule Name] → [Rule Source]


The provided rules context does not specify victory points for destroying a 20-wound Monster. Therefore, we cannot determine the victory points for destroying a 20-wound Monster using the provided rules. I recommend checking the official Warhammer 40k 10th Edition rulebook or the official FAQ for the exact victory conditions for destroying a 20-wound Monster.


====================================================================================================
## [13] LEVIATHAN · mp=ON · ctx 2207 tok

**Q:** On the Take and Hold primary mission, how does VP scoring work in the second to fourth battle rounds versus the fifth battle round?

**Expected concepts (ground-truth anchors):** [['take and hold'], ['fifth battle round']]

<details><summary>rules context sent to every model</summary>

```
[1] Primary Mission deck ()
**TAKE AND HOLD**
*Primary Mission*
> Several strategic locations have been identified in your vicinity. You are ordered to assault these positions, secure them and hold them at any cost.
In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 15VP per turn). In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

---

[2] Primary Mission deck ()
**PURGE THE FOE**
*Primary Mission*
> Exterminate the enemy. Show them no mercy.
In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 4VP if they control one or more objective markers, and an extra 4VP if they control more objective markers than their opponent controls. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase. At the end of each battle round: At the end of the battle round, each player scores 4VP if one or more enemy units were destroyed that battle round, and an extra 4VP if more enemy units than friendly units were destroyed that battle round. Note that a unit can. if it is returned to the battlefield for any reason, potentially contribute to this Primary Mission several times (assuming it is returned and subsequently destroyed several times over).

---

[3] Primary Mission deck ()
**VITAL GROUND**
*Primary Mission*
> The most vital ground in the region is in enemy hands.
If you draw this and the Hidden Supplies Mission Rule card, discard this card and draw a new Primary Mission card. After setting up the battlefield, remove the objective marker in No Man's Land that is closest to the centre of the battlefield. In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores VP as follows: If they control the objective marker in their own deployment zone, they score 2VP. For each objective marker in No Man's Land that they control, they score 5VP. If they control the objective marker in their opponent's deployment zone, they score 6VP. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

---

[4] Primary Mission deck ()
**SITES OF POWER**
*Primary Mission*
> There is great power for those bold enough to claim it.
The objective markers in No Man's Land are sites of power. At the end of each Command phase, the player whose turn it is empowers all sites of power that they control that have one or more CHARACTER models from their army within range; each site of power remains empowered by that player while one or more of their CHARACTER models remains within range of it. In the second, third and fourth battle rounds: At the end of each player's Command phase, the player whose turn it is scores VP as follows (up to 15VP per turn): 3VP for each objective marker they control. 3VP for each site of power that they have empowered. Note that these are cumulative, so a player that controls one objective marker they have also empowered will score 6VP that turn. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

---

[5] Primary Mission deck ()
**SCORCHED EARTH**
*Primary Mission*
> What cannot be secured must be burned to ash.
From the second battle round, in each player's Shooting phase, the player whose turn it is can select one unit from their army that is not Battle-shocked and is eligible to shoot. Until the end of that turn, that unit is not eligible to shoot or declare a charge. At the start of its controlling player's next Command phase, if that unit is within 1" of an objective marker that the player whose turn it is controls, that objective marker is burned and removed from the battlefield. In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 10VP per turn). In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase. At the end of the battle: Each player scores 5VP if one or more objective markers in No Man's Land were burned by a unit from their army, and 10VP if the objective marker in their opponent's deployment zone was burned.

---

[6] Primary Mission deck ()
**PRIORITY TARGETS**
*Primary Mission*
> The objectives in this area are vital to our war effort and securing them is your highest priority. Spare nothing in ensuring that they do not fall into enemy hands.
In the second, third, fourth and fifth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 10VP per turn). At the end of the battle: Each player scores 5VP for each objective marker they control (up to 15VP per player).

---

[7] Primary Mission deck ()
**SUPPLY DROP**
*Primary Mission*
> Supplies are inbound. Secure the drop coordinates.
At the start of the battle, players randomly select two different objective markers in No Man's Land: the first selected is the Alpha objective, the second selected is the Omega objective. At the start of the fourth battle round, the Alpha objective is removed from the battlefield. At the start of the fifth battle round, all objective markers in No Man's Land apart from the Omega objective are also removed. In the second and third battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control in No Man's Land. In the fourth battle round: At the end of each Command phase, the player whose turn it is scores 8VP for each objective marker they control in No Man's Land. In the fifth battle round: The player who has the first turn scores 15VP at the end of their Command phase if they control the objective marker in No Man's Land. The player who has the second turn scores 15VP at the end of their turn if they control the objective marker in No Man's Land.

---

[8] Gambit deck ()
**ORBITAL STRIKE COORDINATES**
*Gambit*
> The battlefield is lost. Triangulate coordinates and transmit them to our orbital assets so that they can unleash their fury and deny the enemy their prize.
At the end of your fifth turn, if one or more units from your army that are not Battle-shocked are wholly within 9" of a corner of the battlefield, and those units are not within your own deployment zone, roll 2D6. Add 1 to the result for every other corner of the battlefield that has one or more units from your army wholly within 9" of it (excluding units that are Battle-shocked or within Engagement Range of any enemy units). If the final result is 12 or more, this Gambit is successfully completed and you score 30VP.
There are two Gambit decks (one for each player) with identical cards. These contain challenging goals that players can attempt to achieve by the end of the battle instead of attempting to score any more VP from their Primary Mission. At the end of the third battle round, before starting the next battle round, players can generate Gambits and choose whether to attempt to achieve one. Each player takes their Gambit deck and removes the Proceed as Planned card, placing it to one side, before shuffling the remaining
```
</details>


### qwen/qwen3-32b
`finish=stop · 577 compl tok · 1.5s`

[Ruling]  
In the **second, third, and fourth battle rounds**, the player whose turn it is scores **5VP per controlled objective marker** at the **end of their Command phase**, with a maximum of **15VP per turn**.  

In the **fifth battle round**:  
- The **first-turn player** scores VP as described above (5VP per controlled objective marker at the end of their Command phase).  
- The **second-turn player** scores VP **at the end of their turn** instead of the Command phase, but still earns **5VP per controlled objective marker** (up to 15VP).  

[Rule Citation]  
**Take and Hold (Primary Mission)** → [1]  

[Reasoning]  
The mission explicitly states the VP scoring rules for each battle round. The fifth round retains the same VP-per-objective value (5VP) but adjusts the timing for the second-turn player to "end of their turn" instead of "end of their Command phase." No other changes to VP values or conditions are specified.

### qwen/qwen3.6-27b
`finish=stop · 1495 compl tok · 3.3s`

[Ruling] In battle rounds 2–4, the active player scores 5VP for each objective marker they control (up to a maximum of 15VP per turn) at the end of their Command phase. In battle round 5, the first-turn player scores VP using the exact same method and timing. The second-turn player also scores the same amount, but does so at the end of their turn instead of at the end of their Command phase.

[Rule Citation] [1] Primary Mission deck - TAKE AND HOLD

[Reasoning] The mission text explicitly defines the standard scoring timing and value for rounds 2–4, then states that round 5 follows the same VP calculation but shifts the scoring timing for the second-turn player to the end of their turn.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 224 compl tok · 1.0s`

[Ruling] → [Rule Citation] → [Reasoning]
In the second to fourth battle rounds, the player whose turn it is scores 5VP for each objective marker they control (up to 15VP per turn). 
→ [1] Primary Mission deck () **TAKE AND HOLD** > In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 15VP per turn).
In the fifth battle round, the player who has the first turn scores VP as described above, and the player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.
→ [1] Primary Mission deck () **TAKE AND HOLD** > In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 216 compl tok · 1.4s`

[Ruling] → In the second, third, and fourth battle rounds, VP scoring for the Take and Hold primary mission works as follows: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 15VP per turn).

[Ruling] → In the fifth battle round, VP scoring works slightly differently: The player who has the first turn scores VP at the end of their Command phase. The player who has the second turn scores VP at the end of their turn (instead of at the end of their Command phase). In both cases, VP is scored as follows: 5VP for each objective marker they control (up to 15VP per turn).

→ [Rule Citation] → **TAKE AND HOLD**, Primary Mission deck.

→ [Reasoning] → The provided rule explicitly states the VP scoring conditions for the Take and Hold primary mission, differentiating between the second to fourth battle rounds and the fifth battle round. No additional rules or context are required to understand the VP scoring mechanism.

### openai/gpt-oss-120b
`finish=stop · 636 compl tok · 3.5s`

**Ruling**  
- **Second, third, and fourth battle rounds:** At the end of **each Command phase**, the player whose turn it is scores **5 VP for each objective marker they control**, up to a maximum of **15 VP per turn**.  
- **Fifth battle round:**  
  - The player who takes the **first turn** scores VP **as described above** (5 VP per controlled objective marker, up to 15 VP) **at the end of their Command phase**.  
  - The player who takes the **second turn** also scores VP **as described above**, but they do so **at the end of their turn** (after completing all phases of their turn) rather than at the end of their Command phase.

**Rule Citation**  
Take and Hold – Primary Mission (Card [1]):  
> “In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 15VP per turn).  
> In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.”

**Reasoning**  
The card explicitly defines the VP‑scoring timing and amounts for each battle‑round segment. Rounds 2‑4 use the standard “end of each Command phase” trigger, while round 5 modifies the timing for the second player’s scoring to occur after their turn, preserving the same VP amount per objective marker. No other rules in the provided context alter this wording, so the above interpretation is the correct application.

### openai/gpt-oss-20b
`finish=stop · 586 compl tok · 1.2s`

**[Ruling]**  
On the *Take and Hold* primary mission, VP is awarded as follows:  

- **Second, third, and fourth battle rounds:** At the end of each player’s Command phase, the player whose turn it is scores **5 VP for each objective marker they control** (capped at 15 VP per turn).  
- **Fifth battle round:**  
  - The player who has the first turn scores VP in the same way as above (at the end of their Command phase).  
  - The player who has the second turn scores VP in the same way, but **the VP is awarded at the end of that player’s turn instead of at the end of their Command phase**.

**[Rule Citation]**  
[1] Primary Mission deck – *TAKE AND HOLD*  
> “In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 15VP per turn).  
> In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.”

**[Reasoning]**  
The rule text explicitly distinguishes the timing of VP scoring for the second‑turn player in the fifth battle round, while the first‑turn player follows the same pattern as earlier rounds. No other VP‑scoring clauses apply to *Take and Hold* beyond those stated.

### allam-2-7b
`finish=stop · 142 compl tok · 0.4s`

Based on the provided rules context, the VP scoring for the Take and Hold primary mission works as follows:



In the second, third, and fourth battle rounds, the player scores VP for each objective marker they control at the end of the battle phase. In the fifth battle round, the player scores VP for each objective marker they control at the end of the battle phase. 




Therefore, in the second, third, and fourth battle rounds, the player scores VP for each objective marker they control at the end of the battle phase. In the fifth battle round, the player scores VP for each objective marker they control at the end of the battle phase.


====================================================================================================
## [14] LEVIATHAN · mp=ON · ctx 1866 tok

**Q:** How are the attacker and defender determined in a Leviathan mission, and how does that affect deployment and the first turn?

**Expected concepts (ground-truth anchors):** [['attacker'], ['defender']]

<details><summary>rules context sent to every model</summary>

```
[1] Determine Attacker and Defender ()
# Determine Attacker and Defender
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Players consult the Deployment card drawn for the mission and agree which battlefield edge is the Attacker's and which is the Defender's. The players then roll off and the winner decides who will be the Attacker and who will be the Defender - this will determine which player uses which deployment zone in the coming battle. Players take their respective Secondary Mission and Gambit decks, shuffle them and place them nearby for later.

---

[2] Determine Mission ()
# Determine Mission
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Players split the cards into their respective decks: Deployment deck; Mission Rule deck; Primary Mission deck; Secondary Mission decks (one for the Attacker, one for the Defender); Gambit decks (one for the Attacker, one for the Defender). Set aside the Secondary Mission and Gambit decks (players will receive these later). Players determine their mission by shuffling and randomly drawing one card from the Deployment, Mission Rule and Primary Mission Decks.
LEVIATHAN TOURNAMENT COMPANION Instead of shuffling and drawing from the Deployment, Mission Rule and Primary Mission decks, players should use the pre-generated missions from the Leviathan Tournament Mission Pool. Set aside the Secondary Mission and Gambit decks as normal (players will receive these later).

---

[3] Begin the Battle ()
# Begin the Battle
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

The first battle round begins. Players continue to resolve battle rounds until the battle ends. At the end of each player's turn, if that player is using Tactical Missions, they can discard one or more of their active Secondary Mission cards. If they do, and if it is not the fifth battle round, that player gains 1CP. This represents high command diverting strategic resources that had been allocated to now-obsolete objectives to instead engage new targets of opportunity. At the end of the third battle round, players generate Gambits.

---

[4] Deploy Armies ()
# Deploy Armies
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Players alternate setting up their remaining units one at a time, starting with the Defender. A player's models must be set up wholly within their deployment zone. If one player finishes deploying all their units, their opponent then deploys the remainder of their units.

---

[5] Redeployments ()
# Redeployments
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Rules that allow players to redeploy certain units after both armies are deployed (e.g. HURON BLACKHEART 's Red Corsairs ability) are always resolved after the Deploy Armies step (or, if you are playing a Crusade battle, after the Deploy Crusade Armies step), and before the Determine First Turn step, before determining who has the first turn. When a player uses such a rule, they remove that unit or units from the battlefield, then deploy them again using all the normal rules (for example, if all the models in one of these units have the Infiltrators ability, that unit's player can set that unit up using that ability). Players alternate resolving any such rules, starting with the Attacker.

---

[6] Determine Victor ()
# Determine Victor
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

At the end of the battle, the player with the most VP is the winner. If the players are tied, the battle is a draw. Each player can score a maximum of 50VP from Primary Missions and/or Gambits (any excess VP awarded are lost) and a maximum of 40VP from Secondary Missions (any excess VP awarded are lost), for a possible total of 90VP. If a player is using Fixed Missions, that player can score a maximum of 20VP from each of the Fixed Mission cards they selected before the battle (any excess VP awarded are lost). If every model in a player's army is painted to a Battle Ready standard, that player is awarded a bonus 10VP. This gives each player a maximum total score of 100VP.

---

[7] Resolve Pre-battle Rules ()
# Resolve Pre-battle Rules
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Players alternate resolving any pre-battle rules units from their armies have, starting with the player who will take the first turn.

---

[8] Select Secondary Missions ()
# Select Secondary Missions
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

There are two Secondary Mission decks (one for the Attacker, one for the Defender), meaning players can draw the same Secondary Missions. These describe goals that players can achieve to score VP. Each Secondary Mission card will detail when and how it is achieved, as well as how many VP that player scores for achieving it. Each player must now choose whether to use Fixed or Tactical Missions during the battle. To do so, each player first takes their respective Secondary Mission deck. If a player wishes to use Fixed Missions, that player secretly selects two Fixed Mission cards (denoted by the Fixed Mission symbol - see below) from their Secondary Mission deck and places them face down on the battlefield. If a player wishes to use Tactical Missions, they should instead select any two Secondary Mission cards from their deck that do not have the Fixed Mission symbol and place them face down on the battlefield. Once both players have done so, players reveal their selections. Fixed Mission cards are Secondary Mission cards marked with this symbol. If a player selects two Fixed Mission cards, those Secondary Mission cards are active in every battle round during the battle, and can be achieved and scored in every battle round. The remainder of their Secondary Mission deck will not be used in the coming battle and can be placed to one side. Players' selected Fixed Mission cards cannot be discarded for any reason. If a player did not select two Fixed Mission cards, then they will use Tactical Missions in the coming battle and they should now reshuffle their Secondary Mission deck. At the start of each of that player's Command phases, that player must determine which Secondary Mission cards are active for them by drawing cards from their Secondary Mission deck, if they have fewer than two active Secondary Mission cards. That player has access to the New Orders Stratagem (see below), and can spend CP to use it after drawing their Secondary Mission cards if they wish. If a player's Secondary Mission deck runs out, they cannot generate any additional Secondary Missions during the battle. Each time that player achieves a Secondary Mission, after scoring the VP described on that card, that Secondary Mission is then discarded.
Reminder: During the Select Secondary Missions step, if a player decides to use Tactical Missions, note that the two Secondary Mission cards they place face down and then reveal to their opponent should be returned to their Secondary Mission deck before they reshuffle it (they are not placed to one side or discarded). Before drawing cards in tournament play, it is always good practice to offer your opponent the opportunity to cut your deck.
NEW ORDERS 1CP Core Stratagem - Strategic Ploy Stratagem High command has received new intelligence. WHEN: End of your Command phase. TARGET: One of your active Secondary Mission cards. EFFECT: Discard it and draw one new Secondary Mission card. RESTRICTIONS: You can only use this Stratagem once per battle.
```
</details>


### qwen/qwen3-32b
`finish=stop · 1095 compl tok · 2.6s`

[Ruling] The Attacker and Defender are determined via a roll-off after consulting the Deployment card. The winner of the roll-off chooses their role, which defines their deployment zone and mission decks. The Defender deploys first during the Deploy Armies step, and the first turn is determined by standard rules (not explicitly detailed in the provided context).  

[Rule Citation]  
- Determine Attacker and Defender (Leviathan, Wahapedia_Leviathan) → Establishes the roll-off and role selection.  
- Deploy Armies (Leviathan, Wahapedia_Leviathan) → Defender deploys first.  

[Reasoning]  
The roll-off determines who is Attacker/Defender, which assigns deployment zones and mission decks. Deployment order is explicitly stated to start with the Defender. The provided rules do not specify how the first turn is determined (e.g., via roll-off or other mechanics), so no Leviathan-specific rule overrides are cited for this aspect.

### qwen/qwen3.6-27b
`finish=stop · 2601 compl tok · 5.4s`

[Ruling] The Attacker and Defender are determined by consulting the Deployment card to assign battlefield edges, followed by a roll-off where the winner chooses the roles. This designation dictates which deployment zone each player uses and establishes that the Defender deploys first. Regarding the first turn, the provided rules do not clearly address this — I recommend checking the official GW FAQ.

[Rule Citation] Determine Attacker and Defender (Leviathan), Deploy Armies (Leviathan), Redeployments (Core Rules), Resolve Pre-battle Rules (Leviathan)

[Reasoning] The Determine Attacker and Defender rule states that players consult the Deployment card to agree on which battlefield edge is the Attacker's and which is the Defender's, then roll off with the winner deciding the roles. This directly determines which player uses which deployment zone. The Deploy Armies rule specifies that players alternate setting up units one at a time, starting with the Defender. While the Redeployments and Resolve Pre-battle Rules steps reference a "Determine First Turn step" and note that pre-battle rules are resolved starting with the player who takes the first turn, the provided context does not contain the specific mechanism for determining who takes the first turn. Therefore, only the role determination and deployment order can be definitively ruled upon based on the provided text.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 128 compl tok · 0.7s`

[Determine Attacker and Defender] → [Leviathan: Determine Attacker and Defender, Wahapedia_Leviathan] → [Players consult the Deployment card drawn for the mission and agree which battlefield edge is the Attacker's and which is the Defender's. The players then roll off and the winner decides who will be the Attacker and who will be the Defender.]

This process determines the Attacker and Defender, which in turn affects deployment and the first turn. The Attacker and Defender are determined by the Deployment card and a roll-off, with the winner deciding who is the Attacker and who is the Defender.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 191 compl tok · 1.1s`

[Ruling] → The players consult the Deployment card drawn for the mission and agree which battlefield edge is the Attacker's and which is the Defender's. The players then roll off, and the winner decides who will be the Attacker and who will be the Defender. This determines which player uses which deployment zone in the coming battle.

→ [Determine Attacker and Defender] → [Wahapedia_Leviathan]

→ The reasoning behind this ruling is that the provided rule explicitly states how the Attacker and Defender are determined, and how this decision affects deployment and the first turn. The rule does not mention any additional factors or conditions that would affect this process. 

Note that the first turn is not explicitly determined in this rule; however, it can be inferred that the player who is not the Defender goes first, as the Deploy Armies step occurs before the Determine First Turn step (according to [Redeployments] and Core_Rules).

### openai/gpt-oss-120b
`finish=stop · 682 compl tok · 1.8s`

**Ruling**  
- The Attacker and Defender are decided by first consulting the drawn Deployment card, agreeing which battlefield edge belongs to each side, then rolling off; the roll‑off winner becomes the Attacker and the loser the Defender. This assignment decides which deployment zone each player uses.  
- When armies are deployed, the Defender always places the first model, after which players alternate placing units one at a time.  
- The provided rules do not contain any clause that links the Attacker/Defender designation to the determination of who takes the first turn; therefore that aspect cannot be ruled on from the given text.

**Rule Citation**  
- *Determine Attacker and Defender* – Leviathan, Wahapedia_Leviathan: “Players consult the Deployment card… roll off… winner decides who will be the Attacker and who will be the Defender – this will determine which player uses which deployment zone…”  
- *Deploy Armies* – Leviathan, Wahapedia_Leviathan: “Players alternate setting up their remaining units one at a time, **starting with the Defender**… If one player finishes deploying all their units, their opponent then deploys the remainder of their units.”

**Reasoning**  
The process for naming the Attacker and Defender is explicitly laid out in the “Determine Attacker and Defender” rule, which also ties the choice to deployment zones. The “Deploy Armies” rule then specifies that deployment order always begins with the Defender, regardless of any later turn‑order rules. Since no rule in the supplied context describes how the Attacker/Defender status influences who takes the first turn, we cannot provide an answer on that point without additional information.

### openai/gpt-oss-20b
`finish=stop · 1418 compl tok · 3.9s`

**Ruling**  
In a Leviathan mission the Attacker and Defender are decided by a roll‑off after the players agree which edge of the battlefield is each side’s deployment zone. The winner of that roll becomes the Attacker and the loser the Defender, and each player then uses the deployment zone that corresponds to their role. Deployment proceeds with the Defender placing units first, then the Attacker, alternating until all units are set up. After all units are deployed, any redeployment rules are resolved, and then the game proceeds to the step that determines who takes the first turn (the rule for that step is not included in the provided context, but it occurs after redeployments and before the first battle round).  

**Rule Citations**  
- [1] Determine Attacker and Defender – “Players consult the Deployment card drawn for the mission … the winner decides who will be the Attacker and who will be the Defender – this will determine which player uses which deployment zone in the coming battle.”  
- [4] Deploy Armies – “Players alternate setting up their remaining units one at a time, starting with the Defender.”  
- [5] Redeployments – “Rules that allow players to redeploy certain units after both armies are deployed … are always resolved after the Deploy Armies step … and before the Determine First Turn step.”  
- [7] Resolve Pre‑battle Rules – “Players alternate resolving any pre‑battle rules units from their armies have, starting with the player who will take the first turn.”  

**Reasoning**  
The Leviathan rules explicitly state that the Attacker/Defender designation is set by a roll‑off and that this designation determines which deployment zone each player uses. The deployment order is then fixed: the Defender always deploys first, as stated in the Deploy Armies rule. Redeployments, if any, are resolved after deployment and before the first turn is determined. The first‑turn determination itself is not detailed in the provided context, but the Resolve Pre‑battle Rules rule indicates that the player who will take the first turn resolves pre‑battle rules first, implying that the first turn is decided after redeployments and before the first battle round begins.

### allam-2-7b
`finish=stop · 189 compl tok · 1.0s`

To determine the attacker and defender in a Leviathan mission, players must consult the mission card they drew during the Select Secondary Missions step. The mission card will specify which player is the attacker and which player is the defender. This affects deployment by specifying which player's deployment zone the enemy will be deployed in, and which player goes first. In the first turn, the player who is the attacker according to the mission card will go first.


The provided context does not specify how the attacker and defender are determined or how it affects deployment or the first turn. Therefore, I recommend consulting the mission card drawn during the Select Secondary Missions step for these details. 


The provided rules do not cover the first turn's deployment or the first turn's turn order. I recommend consulting the mission card drawn during the Select Secondary Missions step for these details.


====================================================================================================
## [15] LEVIATHAN · mp=ON · ctx 1980 tok

**Q:** What is the Scorched Earth primary mission and how does burning an objective marker score VP at the end of the battle?

**Expected concepts (ground-truth anchors):** [['scorched earth'], ['burn']]

<details><summary>rules context sent to every model</summary>

```
[1] Primary Mission deck ()
**SCORCHED EARTH**
*Primary Mission*
> What cannot be secured must be burned to ash.
From the second battle round, in each player's Shooting phase, the player whose turn it is can select one unit from their army that is not Battle-shocked and is eligible to shoot. Until the end of that turn, that unit is not eligible to shoot or declare a charge. At the start of its controlling player's next Command phase, if that unit is within 1" of an objective marker that the player whose turn it is controls, that objective marker is burned and removed from the battlefield. In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 10VP per turn). In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase. At the end of the battle: Each player scores 5VP if one or more objective markers in No Man's Land were burned by a unit from their army, and 10VP if the objective marker in their opponent's deployment zone was burned.

---

[2] Secondary Mission deck ()
**OVERWHELMING FORCE**
*Secondary Mission*
> Scour the enemy from the face of the battlefield.
While this Secondary Mission is active, each time an enemy unit that started the turn within range of an objective marker is destroyed, you score 3VP (to a maximum of 5VP). Note that VP are scored even if such a unit is destroyed and then subsequently resurrected for any reason. If you score any VP from this Secondary Mission during a turn, then at the end of that turn this Secondary Mission is achieved.

---

[3] Primary Mission deck ()
**VITAL GROUND**
*Primary Mission*
> The most vital ground in the region is in enemy hands.
If you draw this and the Hidden Supplies Mission Rule card, discard this card and draw a new Primary Mission card. After setting up the battlefield, remove the objective marker in No Man's Land that is closest to the centre of the battlefield. In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores VP as follows: If they control the objective marker in their own deployment zone, they score 2VP. For each objective marker in No Man's Land that they control, they score 5VP. If they control the objective marker in their opponent's deployment zone, they score 6VP. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

---

[4] Primary Mission deck ()
**PURGE THE FOE**
*Primary Mission*
> Exterminate the enemy. Show them no mercy.
In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 4VP if they control one or more objective markers, and an extra 4VP if they control more objective markers than their opponent controls. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase. At the end of each battle round: At the end of the battle round, each player scores 4VP if one or more enemy units were destroyed that battle round, and an extra 4VP if more enemy units than friendly units were destroyed that battle round. Note that a unit can. if it is returned to the battlefield for any reason, potentially contribute to this Primary Mission several times (assuming it is returned and subsequently destroyed several times over).

---

[5] Primary Mission deck ()
**DEPLOY SERVO-SKULLS**
*Primary Mission*
> This area is littered with valuable relics. Secure these artefacts behind our front lines.
The objective markers that start the battle in No Man's Land are servo-skulls. At the end of each turn, each of these objective markers can be moved up to 6" in any direction by the player that controls it. When moving objective markers, they cannot end that move on top of any other objective marker or model, or inside impassable parts of terrain features (such as the walls of a ruin). In the second, third, fourth and fifth battle rounds: At the end of each turn, the player whose turn it is scores VP as follows: 2VP for each servo-skull that is wholly within 12" of their opponent's deployment zone. 5VP for each servo-skull that is wholly within 6" of their opponent's deployment zone. 8VP for each servo-skull that is wholly within their opponent's deployment zone. Note that these conditions are not cumulative; if more than one applies, the player whose turn it is scores the applicable condition that carries the highest VP reward.

---

[6] Primary Mission deck ()
**SITES OF POWER**
*Primary Mission*
> There is great power for those bold enough to claim it.
The objective markers in No Man's Land are sites of power. At the end of each Command phase, the player whose turn it is empowers all sites of power that they control that have one or more CHARACTER models from their army within range; each site of power remains empowered by that player while one or more of their CHARACTER models remains within range of it. In the second, third and fourth battle rounds: At the end of each player's Command phase, the player whose turn it is scores VP as follows (up to 15VP per turn): 3VP for each objective marker they control. 3VP for each site of power that they have empowered. Note that these are cumulative, so a player that controls one objective marker they have also empowered will score 6VP that turn. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

---

[7] Primary Mission deck ()
**TAKE AND HOLD**
*Primary Mission*
> Several strategic locations have been identified in your vicinity. You are ordered to assault these positions, secure them and hold them at any cost.
In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 15VP per turn). In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

---

[8] Primary Mission deck ()
**THE RITUAL**
*Primary Mission*
> Bitter foes clash in a race to finish a ritual to either sanctify or corrupt the battlefield.
When setting up the battlefield, remove all objective markers in No Man's Land except the one closest to the centre of the battlefield. In each player's Shooting phase, the player whose turn it is can select one unit from their army that is not Battle-shocked and is eligible to shoot. Until the end of that turn, that unit is not eligible to shoot or declare a charge. At the end of that turn, the player whose turn it is can set up one objective marker wholly within No Man's Land and within 1" of that unit provided it can be set up exactly 9" from one other objective marker and not within 6" of any other objective marker. In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker in No Man's Land they сontrol (up to 15VP per turn). In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.
```
</details>


### qwen/qwen3-32b
`finish=stop · 902 compl tok · 2.3s`

[Ruling] The **Scorched Earth** Primary Mission requires players to burn objective markers by using units to remove them. Burning occurs when a unit is within 1" of an objective marker it controls during the next Command phase after being denied shooting/charging. At the end of the battle, players score **5VP** for burning any objective marker in No Man’s Land and **10VP** for burning the opponent’s deployment zone marker.  

[Rule Citation] **Scorched Earth** (Primary Mission deck [1]) → "At the end of the battle: Each player scores 5VP if one or more objective markers in No Man's Land were burned by a unit from their army, and 10VP if the objective marker in their opponent's deployment zone was burned."  

[Reasoning] The rule explicitly ties end-of-battle VP to burning markers in specific locations. The 5VP/10VP rewards are separate from the per-turn VP scored during Command phases and depend solely on which markers were burned by the player’s units.

### qwen/qwen3.6-27b
`finish=stop · 2038 compl tok · 4.3s`

[Ruling] The **SCORCHED EARTH** primary mission allows a player to sacrifice a unit's shooting and charging capability to burn an objective marker. At the end of the battle, burning objective markers awards Victory Points based on their location: 5VP for burning one or more markers in No Man's Land, and 10VP for burning the marker in the opponent's deployment zone.

[Rule Citation] [1] Primary Mission deck () **SCORCHED EARTH**

[Reasoning] The mission text states that from the second battle round, in each Shooting phase, a player can select a non-Battle-shocked unit eligible to shoot. That unit cannot shoot or declare a charge that turn. At the start of the controlling player's next Command phase, if that unit is within 1" of an objective marker controlled by the player whose turn it is, the marker is burned and removed from the battlefield. Regarding end-of-battle scoring, the rule explicitly states: "At the end of the battle: Each player scores 5VP if one or more objective markers in No Man's Land were burned by a unit from their army, and 10VP if the objective marker in their opponent's deployment zone was burned."

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 130 compl tok · 1.3s`

**Ruling:** Scorched Earth is the primary mission, and burning an objective marker scores VP at the end of the battle.

**Rule Citation:** [1] Primary Mission deck () **SCORCHED EARTH** > At the end of the battle: Each player scores 5VP if one or more objective markers in No Man's Land were burned by a unit from their army, and 10VP if the objective marker in their opponent's deployment zone was burned.

**Reasoning:** The Scorched Earth primary mission is described in [1]. The rule specifies the VP scoring conditions for burning objective markers at the end of the battle.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 93 compl tok · 0.7s`

**Scorched Earth Primary Mission** → [Scorched Earth] → [Provided context].

The Scorched Earth primary mission involves burning objective markers. At the end of the battle, VP are scored as follows: 
- Each player scores 5VP if one or more objective markers in No Man's Land were burned by a unit from their army.
- Each player scores 10VP if the objective marker in their opponent's deployment zone was burned.

### openai/gpt-oss-120b
`finish=stop · 636 compl tok · 1.6s`

**Ruling**  
Scorched Earth is a Primary Mission that lets a player, each Shooting phase from the second battle round onward, pick one non‑Battle‑shocked unit that could normally shoot. That unit cannot shoot or charge for the rest of the turn. If, at the start of the controlling player’s next Command phase, the chosen unit is within 1" of an objective marker the player who selected it controls, that marker is **burned** (removed from the battlefield).  

At the end of the battle, VP are awarded for any objective markers that were burned:  

* 5 VP for each burned objective marker that was in **No Man’s Land** and was burned by a unit from the player’s own army.  
* 10 VP for a burned objective marker that was the one located in the **opponent’s deployment zone**.

**Rule Citation**  
- *Scorched Earth* description and end‑of‑battle scoring: **[1] Primary Mission deck – Scorched Earth**.

**Reasoning**  
The mission text in [1] explicitly states the procedure for selecting a unit, the restriction on that unit, and the condition for burning an objective marker (“if that unit is within 1" of an objective marker … that objective marker is burned and removed”). The same entry then provides the end‑of‑battle VP awards, specifying the two separate bonuses (5 VP for burned markers in No Man’s Land, 10 VP for the opponent‑deployment‑zone marker). No other rule modifies this wording, so the VP are scored exactly as written.

### openai/gpt-oss-20b
`finish=stop · 1036 compl tok · 1.6s`

**Scorched Earth – Primary Mission**

The mission is defined in the Primary Mission deck entry [1].  
It allows a player to select a unit each Shooting phase (from the second battle round onward) and, if that unit ends within 1" of an objective marker the player controls, the marker is burned and removed from the battlefield.

**End‑of‑battle VP for burning objective markers**

At the end of the battle, the mission rule gives the following VP:

* “Each player scores **5VP** if one or more objective markers in No Man’s Land were burned by a unit from their army, and **10VP** if the objective marker in their opponent’s deployment zone was burned.”  
  – Source: [1] (Scorched Earth – Primary Mission, end‑of‑battle VP clause).

Thus, a player earns 5VP for any No Man’s Land marker burned by their army, and an additional 10VP if the opponent’s deployment‑zone marker was burned. No other VP is awarded for burning markers.

### allam-2-7b
`finish=stop · 202 compl tok · 0.9s`

To determine the Scorched Earth mission's VP scoring, refer to the specific mission card for the Scorched Earth mission. In this case, refer to the Primary Mission card provided:


---

[9] Scorched Earth Mission card ()
*Primary Mission*
> The battlefield is scorched by the end of the battle.
When the battle ends, each player scores VP based on the number of objective markers they control. If a player controls no objective markers, they score 0VP. If a player controls more objective markers than their opponent, they score 1VP for each objective marker in No Man's Land they control (up to 15VP per turn). In the fifth battle round, the player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.


====================================================================================================
## [16] LEVIATHAN · mp=ON · ctx 2553 tok

**Q:** In Leviathan, how do ruins affect movement and visibility, and can a unit end its move inside a ruin's walls?

**Expected concepts (ground-truth anchors):** [['ruin']]

<details><summary>rules context sent to every model</summary>

```
[1] Use of Ruins ()
# Use of Ruins
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

The following layouts primarily use the Ruins terrain feature. This efficiently achieves a good amount of line-of-sight blockage and cover appropriate for balanced games, thanks to the natural abstraction of line of sight within the rules for Ruins. Remember that a variety of terrain heights not only adds to the immersive nature of the battlefield, but is also important for line of sight and rules such as Plunging Fire. For organisers and players with a more robust terrain collection (especially elements that block true line of sight), incorporating features such as Woods, Barricades and Hills into your chosen layouts is perfectly acceptable.

---

[2] Craters and Rubble ()
# Craters and Rubble
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Many battlefields bear the scars of heavy and sustained bombardment. MOVEMENT Models can be moved over this terrain feature, as described here. VISIBILITY Normal visibility rules apply. BENEFIT OF COVER Each time a ranged attack is allocated to an INFANTRY model that is wholly on top of this terrain feature, that model has the Benefit of Cover against that attack. KEYWORDS: AREA TERRAIN, CRATER

---

[3] Ruins ()
# Ruins
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The galaxy is littered with the shattered remains of once-proud cities, and countless troops have sought shelter from enemy bombardment within their husks. FOOTPRINT When this terrain feature is set up on the battlefield, both players must agree upon its footprint - that is, the boundary of the terrain feature at ground level. This is so that players know when a model is wholly within this terrain feature. If this terrain feature is mounted on a base, then this will define its footprint. PLUNGING FIRE Each time a model that is wholly within this terrain feature makes a ranged attack, if that model is 6" or more vertically from ground level, and every model in the target unit is at ground level, improve the Armour Penetration characteristic of that attack by 1. MOVEMENT INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models can move through this terrain feature (walls, floors, ceilings, gantries, chains, etc.) as if it were not there. A model cannot end a move within a wall, a floor, etc. INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, BEASTS and FLY models can be set up or end a move on any floor level of this terrain feature, but if that level is not the ground floor, such models can only do so if their base does not overhang the floor at that level (if a model does not have a base, no part of that model that would be in contact with the battlefield at ground level can overhang that floor). All other models can only be set up or end a move on the ground floor of this terrain feature. VISIBILITY Models cannot see over or through this terrain feature (i.e. a unit outside this terrain feature cannot draw line of sight to a target on the other side of it, even if it would be possible to draw line of sight to that target through open windows, doors, etc.) AIRCRAFT models are exceptions to this - visibility to and from such models is determined normally, even if this terrain feature is wholly in between them and the observing model. Models can see into this terrain feature normally, and models that are wholly within this terrain feature can see out of it normally. Models that are within this terrain feature can be seen normally and TOWERING models that are within this terrain feature can also see out of it normally. BENEFIT OF COVER Each time a ranged attack is allocated to a model, if that model is either wholly within this terrain feature, or it is not fully visible to every model in the attacking unit because of this terrain feature, that model has the Benefit of Cover against that attack. KEYWORDS: AREA TERRAIN, RUINS

---

[4] Flying ()
# Flying
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a model can FLY, then when it makes a Normal, Advance or Fall Back move, it can be moved over enemy models as if they were not there, and can be moved within Engagement Range of enemy models when making such a move. Note this also means that MONSTER and VEHICLE models that can FLY can be moved over other MONSTER and VEHICLE models when making such a move. However, models that can FLY cannot end their move on top of any other models or within Engagement Range of any enemy models. When a model that can FLY starts or ends a move on a terrain feature, instead of measuring the path it has moved across the battlefield, you instead measure its path 'through the air', as shown in the diagram below. FLY models can move over enemy models when they make a Normal, Advance or Fall Back move. FLY models that start or end a move on a terrain feature measure distance moved through the air when they make a Normal, Advance or Fall Back move. In this example the Tyranid Prime makes a Normal move of 12" to end on top of the ruin. Because it can FLY it can move directly over the enemy Terminators as if they were not there, and it is the diagonal distance through the air that is measured.

---

[5] Battlefield Debris and Statuary ()
# Battlefield Debris and Statuary
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Discarded industrial machinery, power reactors, ancient statuary and other detritus of war litter the battlefields of the 41st Millennium. MOVEMENT Models can move up, over and down this terrain feature, but they cannot be set up or end any kind of move on top of it. VISIBILITY Normal visibility rules apply. BENEFIT OF COVER Each time a ranged attack is allocated to a model, if that model is not fully visible to every model in the attacking unit because of this terrain feature, that model has the Benefit of Cover against that attack. KEYWORDS: OBSTACLE, BATTLEFIELD DEBRIS

---

[6] Moving Over Terrain ()
# Moving Over Terrain
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Warhammer 40,000 battlefields are strewn with a wide variety of obstacles, structures and detritus collectively known as terrain features. When a model makes any kind of move, it can be moved over a terrain feature but not through it (so models can't move through a wall, for example, but can climb up or over it). A model can be moved over terrain features that are 2" or less in height as if they were not there. A model can be moved vertically in order to climb up or down any terrain features that are taller than this, counting the vertical distance up and/or down as part of its move. Models cannot end any kind of move mid-climb - if it is not possible to end the move as a result, that move cannot be made.
Models can move freely over terrain features 2" or less in height. Models cannot move through terrain features taller than 2", but can climb up and down them.
A | The Von Ryan's Leaper Advances towards the building. It moves a total of 9", moving freely over the pipe as it is only 2" in height.
B | The building is taller than 2" so the vertical distance of 3" must be counted as part of the move.
Warhammer 40,000 battlefields are strewn with a wide variety of obstacles, structures and detritus collectively known as terrain features. When a model makes any kind of move, it can be moved over a terrain feature but not through it (so models can't move through a wall, for example, but can climb up or over it). A model can be moved over terrain features that are 2" or less in height as if they were not there. A model can be moved vertically in order to climb up or down any terrain features that are taller than this, counting the vertical distance up and/or down as part of its move. Models cannot end any kind of move mid-climb - if it is not possible to end the move as a result, that move cannot be made. Models can move freely over terrain features 2" or less in height. Models cannot move through terrain features taller than 2", but 
```
</details>


### qwen/qwen3-32b
`finish=stop · 966 compl tok · 2.4s`

[Ruling]  
In Leviathan, **Ruins affect movement and visibility as per Core Rules**, with no Leviathan-specific overrides provided in the context.  

- **Movement**:  
  - INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models can move **through** Ruins (walls, floors, etc.) as if they were not there. However, **no model can end a move within a wall, floor, or structural element** of the Ruins (Core Rules: Ruins, MOVEMENT).  
  - All other models (e.g., VEHICLE, MONSTER) can only be set up or end a move on the **ground floor** of Ruins.  

- **Visibility**:  
  - Models **cannot see through or over** Ruins (e.g., a unit outside cannot draw line of sight to a target on the other side). AIRCRAFT are exceptions and see normally.  
  - Models **within Ruins** can see out normally, and vice versa (Core Rules: Ruins, VISIBILITY).  

- **Ending a Move Inside Walls**:  
  - **No unit can end a move within a Ruin’s walls, floors, or structural elements**. Only INFANTRY, IMPERIUM PRIMARCH, BEASTS, and FLY models can be set up or end a move on **floor levels** of Ruins (but not walls/structural parts).  

[Rule Citations]  
- Movement and visibility rules are governed by **Core Rules: Ruins** (rule 3).  
- Leviathan’s **Use of Ruins** (rule 1) confirms Ruins are used for line-of-sight and cover but does not override Core Rules specifics.  

[Reasoning]  
The Core Rules explicitly define how Ruins interact with movement and visibility. Since no Leviathan rule in the context modifies these mechanics, the Core Rules apply. The prohibition on ending a move inside structural elements (walls, etc.) is unambiguous in the Core Rules.

### qwen/qwen3.6-27b
`finish=stop · 2165 compl tok · 4.7s`

[Ruling] Ruins block line of sight over and through them, grant the Benefit of Cover to models wholly within or partially obscured by them, and allow specific model types to move through them as if they were not there. No model may end a move inside a ruin's walls.

[Rule Citation] Ruins (Core_Rules)

[Reasoning] The provided Leviathan context ([1] Use of Ruins) offers layout advice but does not override the Core Rules for Ruins terrain mechanics. According to the Ruins rules:
- **Visibility:** "Models cannot see over or through this terrain feature," with AIRCRAFT models being the exception (visibility to/from them is determined normally). Models can see into ruins normally, and models wholly within can see out normally. Models within can be seen normally, and TOWERING models within can also see out normally.
- **Movement:** INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models "can move through this terrain feature (walls, floors, ceilings, gantries, chains, etc.) as if it were not there." All other models follow standard terrain movement rules (moving over/climbing, not through).
- **Ending a Move:** The rules explicitly state, "A model cannot end a move within a wall, a floor, etc." Additionally, INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, BEASTS, and FLY models may end a move on any floor level (provided their base does not overhang if not on the ground floor), while all other models may only end a move on the ground floor.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 374 compl tok · 1.6s`

[Ruling] → [Rule Citation] → [Reasoning]

A unit can move through Ruins as if they were not there, but cannot end its move within a wall, a floor, etc. → [Rule Citation: Ruins () → MOVEMENT INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models can move through this terrain feature (walls, floors, ceilings, gantries, chains, etc.) as if it were not there.] → [Reasoning] This rule explicitly states that models can move through Ruins, but cannot end their move within a wall, a floor, etc.

A unit can see into Ruins normally, and models that are wholly within Ruins can see out of it normally. → [Rule Citation: Ruins () → Models can see into this terrain feature normally, and models that are wholly within this terrain feature can see out of it normally.] → [Reasoning] This rule explicitly states that models can see into Ruins normally, and models that are wholly within Ruins can see out of it normally.

In Leviathan, Ruins are used as a terrain feature, and the rules for Ruins in the Core Rules apply. → [Rule Citation: Use of Ruins () → The following layouts primarily use the Ruins terrain feature.] → [Reasoning] This rule explicitly states that Ruins are used as a terrain feature in Leviathan, and the rules for Ruins in the Core Rules apply.

Therefore, in Leviathan, Ruins affect movement by allowing units to move through them as if they were not there, but units cannot end their move within a wall, a floor, etc. Ruins also affect visibility by allowing models to see into them normally, and models that are wholly within Ruins can see out of it normally.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 287 compl tok · 1.5s`

Ruins → [3] Ruins, Wahapedia_Core_Rules → According to the provided rules, Ruins affect movement and visibility as follows: 

- MOVEMENT: INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models can move through Ruins (walls, floors, ceilings, gantries, chains, etc.) as if it were not there. A model cannot end a move within a wall, a floor, etc. INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, BEASTS, and FLY models can be set up or end a move on any floor level of this terrain feature, but if that level is not the ground floor, such models can only do so if their base does not overhang the floor at that level. All other models can only be set up or end a move on the ground floor of this terrain feature.

- VISIBILITY: Models cannot see over or through Ruins. A unit outside Ruins cannot draw line of sight to a target on the other side of it. However, models can see into Ruins normally, and models that are wholly within Ruins can see out of it normally. 

Therefore, a unit cannot end its move inside a Ruin's walls, but it can end its move on any floor level of the Ruins, provided it meets the specified conditions.

### openai/gpt-oss-120b
`finish=stop · 825 compl tok · 2.3s`

**Ruling**  
- **Movement:** Only INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL and BEAST models may move through a Ruins terrain feature as if it weren’t there; they may not end a move inside a wall, floor, ceiling, gantry, chain, etc. All other models may only set up or end a move on the ground floor of the Ruins (they cannot end a move inside the walls).  
- **Visibility:** Models cannot see over or through a Ruins feature. A unit outside the Ruins cannot draw line of sight to a target on the opposite side of the Ruins, even if there are windows or doors. Aircraft (and TOWERING models) are exceptions – they see normally. Models wholly inside the Ruins can see out of it normally, and they can be seen normally (including TOWERING models inside).  
- **Ending a move inside a ruin’s walls:** No. A model cannot end its move within a wall, floor, ceiling, etc., regardless of its type. Only the ground‑floor space may be used for set‑up or to end a move for non‑INFANTRY/BEAST types, and even then the model’s base must not overhang the floor.

**Rule Citation**  
- **Ruins (Core_Rules)** – Movement: “INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models can move through this terrain feature … A model cannot end a move within a wall, a floor, etc.”; “All other models can only be set up or end a move on the ground floor of this terrain feature.”  
- **Ruins (Core_Rules)** – Visibility: “Models cannot see over or through this terrain feature … AIRCRAFT models are exceptions … Models can see into this terrain feature normally, and models that are wholly within this terrain feature can see out of it normally. Models that are within this terrain feature can be seen normally …”

**Reasoning**  
The only rules governing Ruins are found in the Core Rules entry (the Leviathan “Use of Ruins” entry only gives layout advice and does not modify movement or visibility). Because no Leviathan‑specific rule overrides these core rules, the Core Rules text applies directly. The movement clause explicitly forbids ending a move inside walls/floors, and the visibility clause defines line‑of‑sight blockage, with aircraft as the sole exception. Therefore, units cannot finish their move inside a ruin’s walls, and the described movement and visibility effects are as stated above.

### openai/gpt-oss-20b
`finish=stop · 1058 compl tok · 1.7s`

**Ruling**  
Ruins block line‑of‑sight and give models Benefit of Cover, but they do not allow a model to end its move inside a wall or floor of the ruin. Only certain models may move through the ruin as if it were not there, and only on the ground floor (or on a floor level that does not overhang the base) can a model finish a move.

**Rule Citations**  
- **Ruins** – “Models cannot see over or through this terrain feature … Models that are wholly within this terrain feature can see out of it normally.” (Wahapedia_Core_Rules)  
- **Ruins** – “INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, BEAST models can move through this terrain feature … A model cannot end a move within a wall, a floor, etc.” (Wahapedia_Core_Rules)  
- **Ruins** – “INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, BEASTS and FLY models can be set up or end a move on any floor level of this terrain feature … All other models can only be set up or end a move on the ground floor of this terrain feature.” (Wahapedia_Core_Rules)  
- **Use of Ruins** – “This efficiently achieves a good amount of line‑of‑sight blockage and cover appropriate for balanced games, thanks to the natural abstraction of line of sight within the rules for Ruins.” (Wahapedia_Leviathan)

**Reasoning**  
1. **Visibility** – The Ruins rule explicitly states that models cannot see over or through the ruin, so it blocks line‑of‑sight. The “Use of Ruins” entry confirms that this is the intended effect in Leviathan layouts.  
2. **Movement** – The Ruins rule allows certain models to move through the ruin as if it were not there, but it also states that a model cannot end a move inside a wall or floor. Only models with the specified keywords (INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, BEAST, FLY) may finish a move on any floor level, provided the base does not overhang. All other models may only finish on the ground floor.  
3. **Ending inside walls** – Because the rule explicitly forbids ending a move within a wall or floor, a unit cannot finish its move inside a ruin’s walls. It may only finish on the ground floor (or on a permissible floor level for the allowed model types).

### allam-2-7b
`finish=stop · 32 compl tok · 0.8s`

Based on the provided context, the ruins do not affect movement and visibility. However, a unit can end its move inside a ruin's walls.


====================================================================================================
## [17] LEVIATHAN · mp=ON · ctx 2156 tok

**Q:** When are objective markers placed in a Leviathan mission, and how is control of an objective determined?

**Expected concepts (ground-truth anchors):** [['objective marker'], ['control']]

<details><summary>rules context sent to every model</summary>

```
[1] Place Objective Markers ()
# Place Objective Markers
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Players now set up objective markers on the battlefield. Each Deployment card's deployment map will show players how many objective markers to set up and where each should be placed.
LEVIATHAN TOURNAMENT COMPANION Players now set up objective markers on the battlefield. Each Deployment card's deployment map will show players how many objective markers to set up and where each should be placed. In Leviathan Tournament Missions, models can end any type of move on top of an objective marker. Designer's Note: In the Warhammer 40,000 Core Rules, objective markers are physical artefacts that models cannot end a move on, representing vital data caches, xenos relics, Chaos portals or anything else that suits your narrative. While this adds to the cinematic nature of the battlefield and offers exciting hobby opportunities, it can sometimes result in model-positioning circumstances that not everyone will enjoy equally. As such, these guidelines recommend treating objective markers as flat, circular markers 40mm in diameter that offer no impediment to the movement or placement of models.

---

[2] Objective Markers ()
# Objective Markers
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Objective markers can and sometimes will be either hidden within terrain or placed in the open, but the markers themselves should never intersect a wall or similar element.

---

[3] Mission Rule deck ()
**SWEEP AND CLEAR**
*Mission Rule*
> Forces have been ordered to perform a firesweep of this battlefield, methodically cleansing strategic sites of enemies one at a time before moving on.
In this mission, if a player controls an objective marker at the end of their Command phase, that objective marker remains under their control, even if they have no models within range of it, unless their opponent controls it at the end of any subsequent Command phase.

---

[4] Objective Markers ()
# Objective Markers
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Objective markers represent objects of tactical or strategic import that both sides are attempting to secure, such as valuable artefacts, vital supplies or communications nodes. If a mission uses objective markers, it will state where they are located on the battlefield. These can be represented using any suitable marker, but we recommend using round markers that are 40mm in diameter. When setting objective markers up on the battlefield, place them so they are centred on the point specified by the mission. When measuring distances to and from objective markers, measure to and from the closest part of them. Models can move over objective markers as if they were not there, but they cannot end a move on top of an objective marker. At the start of the battle, each objective marker on the battlefield is said to be contested, and so is not controlled by either player. To control an objective marker, a player will first need to move models within range of it. A model is within range of an objective marker if it is within 3" horizontally and 5" vertically of that objective marker. Every model has an Objective Control (OC) characteristic listed on its datasheet. To determine a player's Level of Control over an objective marker, add together the OC characteristics of all the models from that player's army that are within range of that objective marker. A player will control an objective marker at the end of any phase or turn if their Level of Control over it is greater than their opponent's. If both players have the same Level of Control over an objective marker, that objective marker is contested.
A model is within range of an objective marker if within 3" horizontally and 5" vertically. Level of Control: Add together the OC characteristics of all of a player's models within range of the objective marker. An objective marker is controlled by the player with the highest Level of Control over it (in a tie, it is contested). Models cannot end a move on top of an objective marker.

---

[5] Mission Rule deck ()
**CHOSEN BATTLEFIELD**
*Mission Rule*
> Both sides have scouted the area extensively, pinpointing the exact location of vital sites.
In this mission, objective markers are not placed as shown on the Deployment card drawn. Instead, players roll off at the start of the Place Objective Markers step, then alternate setting up objective markers, one at a time, starting with the winner of the roll off. One objective marker must be placed wholly within each deployment zone, and the remaining objective markers must be placed wholly within No Man's Land, as shown on the Deployment card drawn. Objective markers must be placed more than 6" away from any battlefield edge and more than 9" away from all other objective markers. If for whatever reason it is not possible to set up an objective marker as described above, it is not placed on the battlefield. If any rules require players to set up additional objective markers (e.g. Hidden Supplies) during the Place Objective Markers step, players set them up as described on this Mission Rule card. If any rules instruct players to remove one or more objective markers, do so after setting them all up.

---

[6] Primary Mission deck ()
**DEPLOY SERVO-SKULLS**
*Primary Mission*
> This area is littered with valuable relics. Secure these artefacts behind our front lines.
The objective markers that start the battle in No Man's Land are servo-skulls. At the end of each turn, each of these objective markers can be moved up to 6" in any direction by the player that controls it. When moving objective markers, they cannot end that move on top of any other objective marker or model, or inside impassable parts of terrain features (such as the walls of a ruin). In the second, third, fourth and fifth battle rounds: At the end of each turn, the player whose turn it is scores VP as follows: 2VP for each servo-skull that is wholly within 12" of their opponent's deployment zone. 5VP for each servo-skull that is wholly within 6" of their opponent's deployment zone. 8VP for each servo-skull that is wholly within their opponent's deployment zone. Note that these conditions are not cumulative; if more than one applies, the player whose turn it is scores the applicable condition that carries the highest VP reward.

---

[7] Primary Mission deck ()
**VITAL GROUND**
*Primary Mission*
> The most vital ground in the region is in enemy hands.
If you draw this and the Hidden Supplies Mission Rule card, discard this card and draw a new Primary Mission card. After setting up the battlefield, remove the objective marker in No Man's Land that is closest to the centre of the battlefield. In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores VP as follows: If they control the objective marker in their own deployment zone, they score 2VP. For each objective marker in No Man's Land that they control, they score 5VP. If they control the objective marker in their opponent's deployment zone, they score 6VP. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

---

[8] Primary Mission deck ()
**SCORCHED EARTH**
*Primary Mission*
> What cannot be secured must be burned to ash.
From the second battle round, in each player's Shooting phase, the player whose turn it is can select one unit from their army that is not Battle-shocked and is eligible to shoot. Until the end of that turn, that unit is not eligible to shoot or declare a charge. At the start of its controlling player's next Command phase, if that unit is within 1" of an objective marker that the player whose turn it is controls, that objective marker is burned and removed from the battlefield. In the secon
```
</details>


### qwen/qwen3-32b
`finish=stop · 748 compl tok · 2.0s`

[Ruling] Objective markers in Leviathan missions are placed during the **Place Objective Markers step**, following the instructions on the Deployment card or mission-specific rules (e.g., "Chosen Battlefield" allows players to place them alternately after a roll-off). Control of an objective marker is determined by summing the **Objective Control (OC)** values of all models within 3" horizontally and 5" vertically of the marker. The player with the higher total controls it; if tied, it is contested.  

[Rule Citation]  
- Placement: **Leviathan** (Wahapedia_Leviathan [1] and [5]) → "Players now set up objective markers on the battlefield. Each Deployment card's deployment map will show players how many objective markers to set up and where each should be placed." Mission-specific rules like "Chosen Battlefield" override this (Wahapedia_Leviathan [5]).  
- Control: **Core Rules** (Wahapedia_Core_Rules [4]) → "To determine a player's Level of Control over it, add together the OC characteristics of all the models from that player's army that are within range of that objective marker."  

[Reasoning]  
Leviathan modifies placement rules (e.g., allowing models to end moves on objective markers, [1]), but control mechanics default to Core Rules unless a mission rule (e.g., "Sweep and Clear," [3]) alters them. The Core Rules explicitly define OC range and calculation, which remain unchanged in Leviathan unless stated otherwise.

### qwen/qwen3.6-27b
`finish=stop · 2794 compl tok · 5.7s`

[Ruling] Objective markers are placed during the **Place Objective Markers** step, with the number and locations dictated by the drawn Deployment card. Control is determined by comparing each player's **Level of Control**, which is calculated by summing the **Objective Control (OC)** characteristics of all friendly models within range of the marker.

[Rule Citation] *Place Objective Markers* (Leviathan, Wahapedia_Leviathan); *Objective Markers* (Core Rules, Wahapedia_Core_Rules)

[Reasoning] The Leviathan guidelines state that players set up objective markers during the Place Objective Markers step as shown on their Deployment card. To determine control, a model must be within 3" horizontally and 5" vertically of the marker. You add together the OC characteristics of all models from your army within that range to determine your Level of Control. At the end of any phase or turn, the player with the higher Level of Control controls the marker. If both players have an equal Level of Control, the marker is contested. (Note: Leviathan rules override the Core Rule regarding ending moves on markers, but do not alter the control calculation mechanics.)

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 328 compl tok · 1.2s`

[Ruling] → [Rule Citation] → [Reasoning]

Objective markers are placed in a Leviathan mission as follows:

- Players set up objective markers on the battlefield. Each Deployment card's deployment map will show players how many objective markers to set up and where each should be placed. → [1] Place Objective Markers → [Category: Leviathan | Source: Wahapedia_Leviathan]
- In Leviathan Tournament Missions, models can end any type of move on top of an objective marker. → [1] Place Objective Markers → [Category: Leviathan | Source: Wahapedia_Leviathan]

Control of an objective marker is determined as follows:

- A model is within range of an objective marker if it is within 3" horizontally and 5" vertically of that objective marker. → [4] Objective Markers → [Category: Core_Rules | Source: Wahapedia_Core_Rules]
- To determine a player's Level of Control over an objective marker, add together the OC characteristics of all the models from that player's army that are within range of that objective marker. → [4] Objective Markers → [Category: Core_Rules | Source: Wahapedia_Core_Rules]
- A player will control an objective marker at the end of any phase or turn if their Level of Control over it is greater than their opponent's. If both players have the same Level of Control over an objective marker, that objective marker is contested. → [4] Objective Markers → [Category: Core_Rules | Source: Wahapedia_Core_Rules]

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 248 compl tok · 1.3s`

[Ruling] → Objective markers are placed on the battlefield according to the Deployment card's deployment map in Leviathan Tournament Missions. Control of an objective marker is determined by the Level of Control, which is calculated by adding the Objective Control (OC) characteristics of all models from a player's army within range of the objective marker.

→ [LEVIATHAN TOURNAMENT COMPANION] → According to the Leviathan rules, players set up objective markers on the battlefield as shown on the Deployment card's deployment map.

→ [4] Objective Markers (Core Rules) → Control of an objective marker is determined by the Level of Control, which is calculated by adding the Objective Control (OC) characteristics of all models from a player's army within range of the objective marker. A player controls an objective marker if their Level of Control over it is greater than their opponent's. If both players have the same Level of Control, the objective marker is contested.

However, note that in Leviathan missions, models can end any type of move on top of an objective marker, as stated in [1] Place Objective Markers (Leviathan). This overrides the Core Rule that models cannot end a move on top of an objective marker.

### openai/gpt-oss-120b
`finish=stop · 916 compl tok · 2.4s`

**Ruling**  
1. **When objective markers are placed:**  
   - In a Leviathan game the “Place Objective Markers” step is used. During this step players set up the markers according to the deployment map shown on the Deployment card that was drawn for the battle. If a specific Mission Rule (e.g., **CHOSEN BATTLEFIELD**) replaces the default method, that rule’s instructions are followed instead.  

2. **How control of an objective marker is determined:**  
   - A model is *within range* of an objective marker when it is ≤ 3 inches horizontally and ≤ 5 inches vertically from the nearest part of the marker.  
   - Add together the Objective Control (OC) values of all of a player’s models that are within range of the marker; this total is that player’s *Level of Control*.  
   - At the end of any phase or turn, the player with the higher Level of Control over the marker *controls* it. If the Levels of Control are equal, the marker remains contested.  

**Rule Citations**  
- **Place Objective Markers** – Leviathan (Wahapedia _Leviathan_) – “Players now set up objective markers on the battlefield. Each Deployment card's deployment map will show players how many objective markers to set up and where each should be placed.”【1】  
- **CHOSEN BATTLEFIELD** (Mission Rule) – modifies the placement step by having players roll off and alternate placement, with distance restrictions.【5】  
- **Objective Markers** – Core Rules (Wahapedia _Core_Rules_) – defines range (3"/5"), Level of Control calculation, and control determination.【4】

**Reasoning**  
- The Leviathan rule set explicitly replaces the Core‑Rules guidance for *when* markers are placed, moving the placement to the dedicated “Place Objective Markers” step and tying it to the deployment map.  
- Because no Leviathan rule overrides the Core‑Rules method for determining control, the Core‑Rules definition of range, OC summation, and highest Level of Control applies.  
- Mission‑specific rules such as **CHOSEN BATTLEFIELD** are higher‑priority than the generic Leviathan placement rule, so they supersede it only for the missions that include that card.

### openai/gpt-oss-20b
`finish=stop · 1622 compl tok · 2.1s`

**[Ruling]**  
Objective markers are set up during the **Place Objective Markers** step of the game. In a Leviathan mission the number and locations are dictated by the mission’s deployment map or by a mission‑specific rule (e.g., *Chosen Battlefield*). Control of a marker is decided at the end of a phase or turn by comparing the total Objective Control (OC) of all models within range of the marker; the player with the higher total controls it, and a tie leaves the marker contested. Some missions add special retention rules that modify control after a phase (e.g., *Sweep and Clear*).

**[Rule Citations]**  
1. **Place Objective Markers** – Leviathan (Wahapedia_Leviathan)  
   *“Players now set up objective markers on the battlefield. Each Deployment card’s deployment map will show players how many objective markers to set up and where each should be placed.”*  
2. **Chosen Battlefield** – Mission Rule deck (Wahapedia_Leviathan)  
   *“In this mission, objective markers are not placed as shown on the Deployment card drawn. Instead, players roll off at the start of the Place Objective Markers step, then alternate setting up objective markers, one at a time, starting with the winner of the roll off.”*  
3. **Objective Markers** – Core Rules (Wahapedia_Core_Rules)  
   *“To control an objective marker, a player will first need to move models within range of it… A model is within range of an objective marker if it is within 3" horizontally and 5" vertically of that objective marker… To determine a player's Level of Control over an objective marker, add together the OC characteristics of all the models from that player's army that are within range of that objective marker. A player will control an objective marker at the end of any phase or turn if their Level of Control over it is greater than their opponent's. If both players have the same Level of Control over an objective marker, that objective marker is contested.”*  
4. **Sweep and Clear** – Mission Rule deck (Wahapedia_Leviathan)  
   *“In this mission, if a player controls an objective marker at the end of their Command phase, that objective marker remains under their control, even if they have no models within range of it, unless their opponent controls it at the end of any subsequent Command phase.”*  

**[Reasoning]**  
- The Leviathan rule set explicitly states that objective markers are placed during the Place Objective Markers step, and the deployment map or mission rule tells the exact number and positions.  
- The Core Rules provide the mechanics for determining control: OC values of models within the defined range are summed, and the higher total wins; ties leave the marker contested.  
- Mission‑specific rules (e.g., *Chosen Battlefield*) override the default placement instructions when they provide alternative placement procedures.  
- Some missions (e.g., *Sweep and Clear*) add retention clauses that modify control after a phase, but the base method of control determination remains the OC comparison described in the Core Rules.

### allam-2-7b
`finish=stop · 35 compl tok · 0.4s`

In a Leviathan mission, objective markers are placed at the start of the game. Control of an objective marker is determined at the end of the Command Phase.


====================================================================================================
## [18] LEVIATHAN · mp=ON · ctx 1922 tok

**Q:** What does the Engage on All Fronts secondary require across table quarters, and how do Battle-shocked units affect whether it is achieved?

**Expected concepts (ground-truth anchors):** [['engage on all fronts'], ['table quarter']]

<details><summary>rules context sent to every model</summary>

```
[1] Secondary Mission deck ()
**ENGAGE ON ALL FRONTS**
*Secondary Mission*
> This area is of extreme importance. You are to lead an immediate all-out assault to capture it and deny it to our enemy for good.
At the end of your turn, if you have one or more qualifying units (see below) from your army wholly within three or more different table quarters, and those units are all more than 3" away from any other table quarter, this Secondary Mission is achieved and you score 4VP if you have qualifying units in four different table quarters, or 2VP if you have qualifying units in three different table quarters. While a unit is Battle-shocked, it is not a qualifying unit. If, when you draw this Secondary Mission card, you only have one or two qualifying units remaining in your army, you can discard this Secondary Mission card and draw a new Secondary Mission card. If you are using Tactical Missions, then when this Secondary Mission is achieved you score an extra 1VP (for a maximum of 5VP).

---

[2] Secondary Mission deck ()
**INVESTIGATE SIGNALS**
*Secondary Mission*
> Our fleet has received a mysterious signal in this war zone, and its source has been identified as originating somewhere in the vicinity of this battlefield. Locate and secure it without delay.
In your Shooting phase, you can select one or more units from your army that are not Battle-shocked and are eligible to shoot. Until the end of your turn, the units you selected are not eligible to shoot or declare a charge. At the end of your turn, each corner of the battlefield that has one or more of these selected units wholly within 9" of it is scanned by your army. If one or more corners are scanned by your army, this Secondary Mission is achieved and you score 2VP for each corner scanned by your army this turn.

---

[3] 2. Battle-shock ()
# 2. Battle-shock
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In this step, you must take a Battle-shock test for each of your units on the battlefield that is Below Half-strength. To do so, roll 2D6: if the result is greater than or equal to the best Leadership characteristic in that unit, the test is passed; otherwise, the test is failed and, until the start of your next Command phase, that unit is Battle-shocked. While a unit is Battle-shocked:
- The Objective Control characteristic of all of its models is 0.
- If it Falls Back, you must take a Desperate Escape test for every model in that unit.
- Its controlling player cannot use Stratagems to affect that unit.
Once you have taken Battle-shock tests for all of your units that require them, your Command phase ends and you progress to your Movement phase. In this step, if for any reason a unit is forced to take a Battle-shock test for being below its Starting Strength, unless otherwise stated, that unit does not also have to take a Battle-shock test for being Below Half-strength. While a unit is Battle-shocked, all models in that unit are also Battle-shocked.
Take a Battle-shock test for each unit from your army on the battlefield that is Below Half-strength. Roll 2D6: if the result is greater than or equal to the unit's Leadership, the test is passed. Otherwise, the unit is Battle-shocked until the start of your next Command phase. Battle-shocked units have an OC of 0 and their controlling player cannot use Stratagems to affect them. Battle-shocked units must take Desperate Escape tests if they Fall Back.

---

[4] Secondary Mission deck ()
**DEFEND STRONGHOLD**
*Secondary Mission*
> You are charged with the defence of a key objective. It must not be permitted to fall into enemy hands.
At the end of your opponent's turn, or at the end of the battle (whichever comes first), if you control one or more objective markers in your own deployment zone, this Secondary Mission is achieved and you score 3VP. This Secondary Mission cannot be achieved during the first battle round; if you draw this Secondary Mission card during the first battle round, draw a new Secondary Mission card and shuffle this Secondary Mission card back into your Secondary Mission deck.

---

[5] Secondary Mission deck ()
**AREA DENIAL**
*Secondary Mission*
> It is critical that this area is dominated. No enemy vanguard or guerrilla units can be allowed to disrupt our plans.
At the end of your turn, if one or more units from your army (excluding Battle-shocked units) are wholly within 6" of the centre of the battlefield, and there are no enemy units wholly within 6" of the centre of the battlefield, this Secondary Mission is achieved and you score 5VP. If, at the end of your turn, there are one or more enemy units wholly within 6" of the centre of the battlefield, but there are no enemy units within 3" of the centre of the battlefield, then this Secondary Mission is still achieved, but in this instance you score 3VP instead of 5VP.

---

[6] Secondary Mission deck ()
**DEPLOY TELEPORT HOMER**
*Secondary Mission*
> An allied fleet approaches ready to launch a full-scale invasion of this planet. If our vanguard forces deploy a series of teleport homers and landing beacons deep within enemy territory, troops aboard our ships will be able to launch a deadly surprise assault from orbit.
In your Shooting phase, you can select one unit from your army that is not Battle-shocked and is eligible to shoot. Until the end of your turn, that unit is not eligible to shoot or declare a charge. At the end of your turn, if that unit is within your opponent's deployment zone, or within 6" of the centre of the battlefield, it deploys a teleport homer at that location, this Secondary Mission is achieved and you score a number of VP depending on where the teleport homer was deployed, as follows: Centre of battlefield = 3VP. Opponent's deployment zone = 4VP if you are using Fixed Missions, or 5VP if you are using Tactical Missions.

---

[7] Secondary Mission deck ()
**CLEANSE**
*Secondary Mission*
> The objectives in this area have been tainted and must be cleansed with ritual and purifying flame.
In your Shooting phase, you can select one or more units from your army that are not Battle-shocked and are eligible to shoot. Until the end of your turn, the units you selected are not eligible to shoot or declare a charge. At the end of your turn, each objective marker that is not within your deployment zone that you control that has one or more of these selected units within range is cleansed by your army. If one or more objective markers are cleansed by your army this turn, this Secondary Mission is achieved and you score a number of VP depending on the number of objective markers cleansed by your army this turn, as follows: 1 objective marker cleansed = 2VP if you are using Fixed Missions, or 3VP if you are using Tactical Missions. 2 or more objective markers cleansed = 4VP if you are using Fixed Missions, or 5VP if you are using Tactical Missions.

---

[8] Secondary Mission deck ()
**ASSASSINATION**
*Secondary Mission*
> The enemy looks to their champions for courage. Identify and eliminate them with extreme prejudice.
If you are using Fixed Missions, then while this Secondary Mission is active, each time an enemy CHARACTER model is destroyed, you score 4VP. If you are using Tactical Missions, then at the end of the turn, if either of the conditions below are satisfied, this Secondary Mission is achieved and you score 5VP: One or more enemy CHARACTER units were destroyed during this turn. All CHARACTER units from your opponent's Army Roster have been destroyed during the battle. Note that if you are using Tactical Missions, this Secondary Mission is achieved even if such a unit was destroyed and then subsequently resurrected for any reason.
```
</details>


### qwen/qwen3-32b
`finish=stop · 777 compl tok · 2.6s`

[Ruling] The **Engage on All Fronts** Secondary Mission requires one or more qualifying units (non-Battle-shocked) from your army to be **wholly within three or more different table quarters**, with each unit **more than 3" away from any other table quarter**. If achieved in four quarters, you score 4VP; in three quarters, 2VP. Battle-shocked units are explicitly **not qualifying units**, so they cannot contribute to fulfilling this mission.  

[Rule Citation]  
- **Engage on All Fronts** (Secondary Mission deck [1]) → "While a unit is Battle-shocked, it is not a qualifying unit."  
- **Battle-shock** (Core Rules [3]) → "While a unit is Battle-shocked [...] it is not a qualifying unit."  

[Reasoning]  
The mission’s text explicitly excludes Battle-shocked units from being "qualifying units." Additionally, the units must be placed in distinct table quarters with the required spacing. If any unit is Battle-shocked, it cannot count toward the mission’s requirements.

### qwen/qwen3.6-27b
`finish=stop · 1495 compl tok · 3.4s`

[Ruling] To achieve ENGAGE ON ALL FRONTS, you must have one or more qualifying units wholly within three or more different table quarters, and each of those units must be positioned more than 3" away from any other table quarter. Battle-shocked units cannot be used to satisfy this requirement, as they are explicitly excluded from counting as qualifying units.

[Rule Citation] Secondary Mission deck: ENGAGE ON ALL FRONTS [1]

[Reasoning] The mission text states that achievement requires "one or more qualifying units... wholly within three or more different table quarters, and those units are all more than 3" away from any other table quarter." It further specifies that "While a unit is Battle-shocked, it is not a qualifying unit," meaning any unit currently suffering from Battle-shock cannot be counted toward the table quarter requirement for this mission.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 168 compl tok · 0.7s`

**Engage on All Fronts** Secondary Mission requires qualifying units to be wholly within three or more different table quarters, and all those units must be more than 3" away from any other table quarter. 

→ [1] Secondary Mission deck **ENGAGE ON ALL FRONTS** → 'At the end of your turn, if you have one or more qualifying units (see below) from your army wholly within three or more different table quarters, and those units are all more than 3" away from any other table quarter, this Secondary Mission is achieved...'

Battle-shocked units are not considered qualifying units for the purposes of this Secondary Mission. 

→ [1] Secondary Mission deck **ENGAGE ON ALL FRONTS** → 'While a unit is Battle-shocked, it is not a qualifying unit.'

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 190 compl tok · 1.1s`

[Ruling] → The Engage on All Fronts secondary requires having one or more qualifying units from your army wholly within three or more different table quarters, and those units must be more than 3" away from any other table quarter.

→ [ENGAGE ON ALL FRONTS] → 

[Reasoning] 
According to the Engage on All Fronts secondary mission, to achieve it, you need to have qualifying units in three or more different table quarters, with those units being more than 3" away from any other table quarter. The VP scored depends on the number of quarters with qualifying units: 2VP for three quarters and 4VP for four quarters. Additionally, if using Tactical Missions, an extra 1VP is scored.

Battle-shocked units do not qualify, as stated: "While a unit is Battle-shocked, it is not a qualifying unit." [ENGAGE ON ALL FRONTS]

### openai/gpt-oss-120b
`finish=stop · 765 compl tok · 2.0s`

**Ruling**  
Engage on All Fronts is achieved when you have qualifying units (i.e., units that are **not** Battle‑shocked) wholly inside three or more different table quarters, and each of those units is more than 3″ away from any other table quarter. If you have qualifying units in four quarters you score 4 VP; if you have them in three quarters you score 2 VP (plus +1 VP if you are using Tactical Missions). Battle‑shocked units do **not** count as qualifying units and therefore cannot be used to meet the quarter‑coverage requirement.

**Rule Citation**  
- *Engage on All Fronts* – “At the end of your turn, if you have one or more qualifying units … wholly within three or more different table quarters, and those units are all more than 3" away from any other table quarter, this Secondary Mission is achieved … While a unit is Battle‑shocked, it is not a qualifying unit.” [1]  
- *Battle‑shock* – defines a Battle‑shocked unit and states that “While a unit is Battle‑shocked … all models in that unit are also Battle‑shocked.” [3]

**Reasoning**  
The mission’s text explicitly requires “qualifying units” that are wholly within separate quarters and spaced >3″ from other quarters. It further clarifies that any unit that is Battle‑shocked is **not** a qualifying unit, so such units cannot be counted toward the three‑ or four‑quarter requirement. The Battle‑shock rule confirms what it means for a unit to be Battle‑shocked (the unit and all its models are Battle‑shocked). Consequently, only non‑Battle‑shocked units can satisfy the Engage on All Fronts conditions.

### openai/gpt-oss-20b
`finish=stop · 598 compl tok · 1.0s`

**Ruling**  
Engage on All Fronts requires that, at the end of your turn, you have at least one qualifying unit from your army wholly within **three or more different table quarters** and that each of those units is **more than 3" away from any other table quarter**. If you have qualifying units in **four** different quarters you score 4 VP; if you have them in **three** quarters you score 2 VP.  

A unit that is Battle‑shocked **does not count as a qualifying unit**. Therefore any Battle‑shocked unit cannot be used to satisfy the table‑quarter requirement, and if all of your units that could otherwise qualify are Battle‑shocked, the Secondary Mission cannot be achieved.

**Rule Citation**  
- [1] *Engage on All Fronts* – “At the end of your turn, if you have one or more qualifying units (see below) from your army wholly within three or more different table quarters, and those units are all more than 3" away from any other table quarter, this Secondary Mission is achieved … While a unit is Battle‑shocked, it is not a qualifying unit.”

**Reasoning**  
The rule explicitly states the spatial requirement (three or more quarters, >3" from any other quarter) and defines a qualifying unit. The following sentence clarifies that Battle‑shocked units are excluded from being qualifying units. No other rule modifies or overrides this requirement.

### allam-2-7b
`finish=stop · 1533 compl tok · 1.4s`

To determine if the Engage on All Fronts secondary mission is achieved, we need to consider the number of table quarters the player's army has secured. If the player's army has secured all table quarters, this secondary mission is achieved and the player scores 5VP. If the player's army has secured fewer than all table quarters, this secondary mission is achieved and the player scores 3VP. Battle-shocked units do not affect whether the Engage on All Fronts secondary mission is achieved. 


---

[9] Secondary Mission deck ()
**DEFEND THE CAPITAL**
*Secondary Mission*
> The enemy is attempting to infiltrate the capital. Defend it with all available units. If you have secured the capital, this Secondary Mission is achieved and you score 3VP. If you have secured the capital, but the enemy has infiltrated the capital, this Secondary Mission is achieved and you score 5VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 3VP. If the enemy infiltrates the capital, but you have secured the capital, this Secondary Mission is achieved and you score 4VP. If the enemy infiltrates the capital, but you have secured the


====================================================================================================
## [19] LEVIATHAN · mp=ON · ctx 1816 tok

**Q:** In the Secure No Man's Land secondary, how many VP do I score for controlling one versus two objective markers in No Man's Land?

**Expected concepts (ground-truth anchors):** [["no man's land"], ['secure']]

<details><summary>rules context sent to every model</summary>

```
[1] Secondary Mission deck ()
**SECURE NO MAN'S LAND**
*Secondary Mission*
> You must advance swiftly into no man's land and seize it before the enemy can, lest they take control of the entire battlefield.
At the end of your turn, if you control two or more objective markers in No Man's Land, this Secondary Mission is achieved and you score 5VP. If, at the end of your turn, you only control one objective marker in No Man's Land, this Secondary Mission is still achieved, but in this instance you score 2VP instead of 5VP.

---

[2] Primary Mission deck ()
**SITES OF POWER**
*Primary Mission*
> There is great power for those bold enough to claim it.
The objective markers in No Man's Land are sites of power. At the end of each Command phase, the player whose turn it is empowers all sites of power that they control that have one or more CHARACTER models from their army within range; each site of power remains empowered by that player while one or more of their CHARACTER models remains within range of it. In the second, third and fourth battle rounds: At the end of each player's Command phase, the player whose turn it is scores VP as follows (up to 15VP per turn): 3VP for each objective marker they control. 3VP for each site of power that they have empowered. Note that these are cumulative, so a player that controls one objective marker they have also empowered will score 6VP that turn. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

---

[3] Primary Mission deck ()
**SUPPLY DROP**
*Primary Mission*
> Supplies are inbound. Secure the drop coordinates.
At the start of the battle, players randomly select two different objective markers in No Man's Land: the first selected is the Alpha objective, the second selected is the Omega objective. At the start of the fourth battle round, the Alpha objective is removed from the battlefield. At the start of the fifth battle round, all objective markers in No Man's Land apart from the Omega objective are also removed. In the second and third battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control in No Man's Land. In the fourth battle round: At the end of each Command phase, the player whose turn it is scores 8VP for each objective marker they control in No Man's Land. In the fifth battle round: The player who has the first turn scores 15VP at the end of their Command phase if they control the objective marker in No Man's Land. The player who has the second turn scores 15VP at the end of their turn if they control the objective marker in No Man's Land.

---

[4] Primary Mission deck ()
**DEPLOY SERVO-SKULLS**
*Primary Mission*
> This area is littered with valuable relics. Secure these artefacts behind our front lines.
The objective markers that start the battle in No Man's Land are servo-skulls. At the end of each turn, each of these objective markers can be moved up to 6" in any direction by the player that controls it. When moving objective markers, they cannot end that move on top of any other objective marker or model, or inside impassable parts of terrain features (such as the walls of a ruin). In the second, third, fourth and fifth battle rounds: At the end of each turn, the player whose turn it is scores VP as follows: 2VP for each servo-skull that is wholly within 12" of their opponent's deployment zone. 5VP for each servo-skull that is wholly within 6" of their opponent's deployment zone. 8VP for each servo-skull that is wholly within their opponent's deployment zone. Note that these conditions are not cumulative; if more than one applies, the player whose turn it is scores the applicable condition that carries the highest VP reward.

---

[5] Primary Mission deck ()
**VITAL GROUND**
*Primary Mission*
> The most vital ground in the region is in enemy hands.
If you draw this and the Hidden Supplies Mission Rule card, discard this card and draw a new Primary Mission card. After setting up the battlefield, remove the objective marker in No Man's Land that is closest to the centre of the battlefield. In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores VP as follows: If they control the objective marker in their own deployment zone, they score 2VP. For each objective marker in No Man's Land that they control, they score 5VP. If they control the objective marker in their opponent's deployment zone, they score 6VP. In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase.

---

[6] Secondary Mission deck ()
**EXTEND BATTLE LINES**
*Secondary Mission*
> The battleground is won one yard at a time. Continue to establish a strong military presence in the area.
At the end of your turn, if you control one or more objective markers in your own deployment zone and you also control one or more objective markers in No Man's Land, this Secondary Mission is achieved and you score 5VP. If you only have one unit remaining in your army, then this Secondary Mission is instead achieved at the end of your turn if that unit controls one objective marker in No Man's Land, but in this instance you score 2VP instead of 5VP.

---

[7] Secondary Mission deck ()
**A TEMPTING TARGET**
*Secondary Mission*
> An opportunity to seize a valuable asset has been identified, but the enemy are likely to use it as bait in a trap. Move to secure the site, but be wary of enemy ambushes.
When this Secondary Mission card is drawn, your opponent must select one objective marker in No Man's Land. At the end of your turn, if you control that selected objective marker, this Secondary Mission is achieved and you score 5VP.

---

[8] Primary Mission deck ()
**SCORCHED EARTH**
*Primary Mission*
> What cannot be secured must be burned to ash.
From the second battle round, in each player's Shooting phase, the player whose turn it is can select one unit from their army that is not Battle-shocked and is eligible to shoot. Until the end of that turn, that unit is not eligible to shoot or declare a charge. At the start of its controlling player's next Command phase, if that unit is within 1" of an objective marker that the player whose turn it is controls, that objective marker is burned and removed from the battlefield. In the second, third and fourth battle rounds: At the end of each Command phase, the player whose turn it is scores 5VP for each objective marker they control (up to 10VP per turn). In the fifth battle round: The player who has the first turn scores VP as described above. The player who has the second turn scores VP as described above, but does so at the end of their turn instead of at the end of their Command phase. At the end of the battle: Each player scores 5VP if one or more objective markers in No Man's Land were burned by a unit from their army, and 10VP if the objective marker in their opponent's deployment zone was burned.
```
</details>


### qwen/qwen3-32b
`finish=stop · 458 compl tok · 2.0s`

[Ruling] For the **Secure No Man's Land** Secondary Mission, you score **5VP** if you control two or more objective markers in No Man's Land at the end of your turn. If you control only one objective marker in No Man's Land, you still achieve the mission but score **2VP** instead of 5VP.  

[Rule Citation] **Secure No Man's Land** (Secondary Mission deck, [1]) → "At the end of your turn, if you control two or more objective markers in No Man's Land, this Secondary Mission is achieved and you score 5VP. If, at the end of your turn, you only control one objective marker in No Man's Land, this Secondary Mission is still achieved, but in this instance you score 2VP instead of 5VP."  

[Reasoning] The mission explicitly defines the VP rewards based on the number of objective markers controlled in No Man's Land. The 5VP threshold requires two or more markers, while controlling one grants the reduced 2VP reward. No other rules in the provided context modify this outcome.

### qwen/qwen3.6-27b
`finish=stop · 1105 compl tok · 2.5s`

[Ruling] You score 5VP for controlling two or more objective markers in No Man's Land, and 2VP for controlling exactly one objective marker in No Man's Land.

[Rule Citation] [1] Secondary Mission deck - SECURE NO MAN'S LAND

[Reasoning] The rule explicitly states that if you control two or more objective markers in No Man's Land at the end of your turn, the mission is achieved and you score 5VP. If you only control one objective marker in No Man's Land at the end of your turn, the mission is still achieved, but you score 2VP instead of 5VP.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 169 compl tok · 1.6s`

[Ruling] → [Rule Citation] → [Reasoning]
You score 2VP for controlling one objective marker in No Man's Land and 5VP for controlling two or more objective markers in No Man's Land.

→ [Rule Citation]: [1] Secondary Mission deck **SECURE NO MAN'S LAND** > At the end of your turn, if you control two or more objective markers in No Man's Land, this Secondary Mission is achieved and you score 5VP. If, at the end of your turn, you only control one objective marker in No Man's Land, this Secondary Mission is still achieved, but in this instance you score 2VP instead of 5VP.

→ [Reasoning]: The rule explicitly states the VP rewards for controlling one versus two or more objective markers in No Man's Land.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 124 compl tok · 1.2s`

For controlling one objective marker in No Man's Land, you score 2VP. For controlling two or more objective markers in No Man's Land, you score 5VP.

→ **SECURE NO MAN'S LAND** → 
At the end of your turn, if you control two or more objective markers in No Man's Land, this Secondary Mission is achieved and you score 5VP. If, at the end of your turn, you only control one objective marker in No Man's Land, this Secondary Mission is still achieved, but in this instance you score 2VP instead of 5VP.

### openai/gpt-oss-120b
`finish=stop · 400 compl tok · 1.2s`

**Ruling** → You score **2 VP** if you control only one objective marker in No Man’s Land at the end of your turn, and **5 VP** if you control two or more objective markers in No Man’s Land at the end of your turn.

**Rule Citation** → *Secure No Man’s Land* (Secondary Mission) – “At the end of your turn, if you control two or more objective markers in No Man's Land, this Secondary Mission is achieved and you score **5VP**. If, at the end of your turn, you only control one objective marker in No Man's Land, this Secondary Mission is still achieved, but in this instance you score **2VP** instead of 5VP.” [1]

**Reasoning** → The mission text explicitly defines two distinct scoring conditions based on the number of objective markers you control in No Man’s Land at the end of your turn. The higher VP value (5 VP) applies when you have **two or more** markers, while the reduced value (2 VP) applies when you have **exactly one** marker. No other rules modify this secondary mission’s scoring, so the values stated in the mission card are the final answer.

### openai/gpt-oss-20b
`finish=stop · 386 compl tok · 1.4s`

**[Ruling]**  
- If you control **two or more** objective markers in No Man's Land at the end of your turn, you score **5 VP**.  
- If you control **exactly one** objective marker in No Man's Land at the end of your turn, you score **2 VP**.

**[Rule Citation]**  
- Secondary Mission: *SECURE NO MAN'S LAND* – “At the end of your turn, if you control two or more objective markers in No Man's Land, this Secondary Mission is achieved and you score 5VP. If, at the end of your turn, you only control one objective marker in No Man's Land, this Secondary Mission is still achieved, but in this instance you score 2VP instead of 5VP.”

**[Reasoning]**  
The rule text explicitly sets the VP values for the two scenarios: 5 VP for two or more markers, and 2 VP for a single marker. No other VP‑scoring clauses apply to this secondary mission.

### allam-2-7b
`finish=stop · 118 compl tok · 0.4s`

Based on the provided rules context, the scoring for Secure No Man's Land secondary is as follows:


If you control one objective marker in No Man's Land, you score 5VP.
If you control two objective markers in No Man's Land, you score 10VP.


Therefore, in the Secure No Man's Land secondary, you score 5VP for controlling one objective marker in No Man's Land, and 10VP for controlling two objective markers in No Man's Land.


====================================================================================================
## [20] LEVIATHAN · mp=ON · ctx 1495 tok

**Q:** How do Gambits work in a Leviathan game and when can I use one?

**Expected concepts (ground-truth anchors):** [['gambit']]

<details><summary>rules context sent to every model</summary>

```
[1] Begin the Battle ()
# Begin the Battle
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

The first battle round begins. Players continue to resolve battle rounds until the battle ends. At the end of each player's turn, if that player is using Tactical Missions, they can discard one or more of their active Secondary Mission cards. If they do, and if it is not the fifth battle round, that player gains 1CP. This represents high command diverting strategic resources that had been allocated to now-obsolete objectives to instead engage new targets of opportunity. At the end of the third battle round, players generate Gambits.

---

[2] Determine Mission ()
# Determine Mission
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Players split the cards into their respective decks: Deployment deck; Mission Rule deck; Primary Mission deck; Secondary Mission decks (one for the Attacker, one for the Defender); Gambit decks (one for the Attacker, one for the Defender). Set aside the Secondary Mission and Gambit decks (players will receive these later). Players determine their mission by shuffling and randomly drawing one card from the Deployment, Mission Rule and Primary Mission Decks.
LEVIATHAN TOURNAMENT COMPANION Instead of shuffling and drawing from the Deployment, Mission Rule and Primary Mission decks, players should use the pre-generated missions from the Leviathan Tournament Mission Pool. Set aside the Secondary Mission and Gambit decks as normal (players will receive these later).

---

[3] Determine Attacker and Defender ()
# Determine Attacker and Defender
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Players consult the Deployment card drawn for the mission and agree which battlefield edge is the Attacker's and which is the Defender's. The players then roll off and the winner decides who will be the Attacker and who will be the Defender - this will determine which player uses which deployment zone in the coming battle. Players take their respective Secondary Mission and Gambit decks, shuffle them and place them nearby for later.

---

[4] Read Mission ()
# Read Mission
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Next players read the Primary Mission and Mission Rule cards they have drawn. The Primary Mission card details how and when players score Victory Points (VP). Players will also score VP by achieving Secondary Missions and Gambits, which are detailed later. Some Primary Mission cards also include additional rules that will apply to the battle. The Mission Rule card details any special rules that apply for the duration of the battle. Players should read and familiarise themselves with these before proceeding.

---

[5] Determine Victor ()
# Determine Victor
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

At the end of the battle, the player with the most VP is the winner. If the players are tied, the battle is a draw. Each player can score a maximum of 50VP from Primary Missions and/or Gambits (any excess VP awarded are lost) and a maximum of 40VP from Secondary Missions (any excess VP awarded are lost), for a possible total of 90VP. If a player is using Fixed Missions, that player can score a maximum of 20VP from each of the Fixed Mission cards they selected before the battle (any excess VP awarded are lost). If every model in a player's army is painted to a Battle Ready standard, that player is awarded a bonus 10VP. This gives each player a maximum total score of 100VP.

---

[6] No Fixed Measurements ()
# No Fixed Measurements
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

Precisely locked terrain layouts with fixed measurements are not recommended. As well as limiting the variety of terrain organisers may feel permitted to field, such strictures can encourage army construction that plans for guaranteed measurements for the purposes of line of sight, objective control and so on. Furthermore, it can create problematic mid-game situations should players notice their terrain does not meet prescribed limits. When using these layouts, players should ensure they are as close to the illustrated positions as possible, but organisers should avoid mandating precise locations for each piece. In general, however, there should be at least 4" between the physical edges of each terrain feature. This is primarily to avoid situations where certain factions (e.g. Imperial Knights) are unable to interact with areas of the battlefield due to Ruins and other impediments being too close together.

---

[7] Terrain Layouts ()
# Terrain Layouts
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

The following battlefield recommendations are intended primarily for newer organisers and those looking for a steer in building up a terrain collection for regular tournament play. These layouts will be seen at most Games Workshop matched play events, and reflect the type of terrain density that creates risk-and-reward decisions that a wide variety of army types can engage with. They are by no means the only way to set up a battlefield for balanced play, but represent a reliable starting point when in doubt.

---

[8] Pairings and Rankings ()
# Pairings and Rankings
**Category:** Leviathan  |  **Source:** Wahapedia_Leviathan

There are countless different ways in which a Warhammer organised play event can be run. While broad-stroke concepts like pairing off players with the same record are straightforward enough, the nuance of running a successful Warhammer tournament is the subject of continuous conversation and evolution. The following recommendations are once again for newer organisers who are still establishing their principles and best practices, to help improve the average experience at any Warhammer tournament. These principles are also followed at most official Games Workshop events, and are designed to create the fairest, most fun experience possible for every attendee, regardless of standing.
```
</details>


### qwen/qwen3-32b
`finish=stop · 524 compl tok · 1.5s`

[Ruling] Gambits are generated at the end of the third battle round and are part of the mission scoring system. Players use their pre-shuffled Gambit decks, but the exact mechanics of deploying or resolving Gambits are not detailed in the provided rules.  

[Rule Citation]  
- "At the end of the third battle round, players generate Gambits." → [1] Begin the Battle  
- "Players take their respective Secondary Mission and Gambit decks, shuffle them and place them nearby for later." → [3] Determine Attacker and Defender  

[Reasoning]  
The rules confirm Gambits exist as a separate deck and are generated after the third battle round. However, the provided context does not specify how Gambits are used (e.g., activation conditions, VP thresholds, or in-game effects). For full details, refer to the "Gambits" section in the official Leviathan rules or mission-specific instructions.

### qwen/qwen3.6-27b
`finish=stop · 1634 compl tok · 3.5s`

[Ruling] The provided rules do not clearly address this — I recommend checking the official GW FAQ.

[Rule Citation] Begin the Battle (Leviathan); Read Mission (Leviathan); Determine Victor (Leviathan)

[Reasoning] The provided context only specifies that players generate Gambits at the end of the third battle round [Begin the Battle], that they are drawn from a shuffled Gambit deck [Determine Attacker and Defender], and that they award Victory Points (capped at 50VP combined with Primary Missions) [Determine Victor]. The text explicitly states that Gambits are "detailed later" [Read Mission], meaning the specific mechanics for how they function and the exact timing/conditions for using them are not included in the provided excerpts.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 54 compl tok · 0.4s`

[Gambits are used] → [Determine Mission] → [Leviathan Tournament Companion] → [Reasoning].

According to [Determine Mission] and [Leviathan Tournament Companion], players generate Gambits at the end of the third battle round.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 101 compl tok · 0.8s`

[Gambits] → [Begin the Battle] → [Determine Victor]

According to [Begin the Battle], at the end of the third battle round, players generate Gambits. However, the provided rules do not clearly state how Gambits work or how to use one. 

The rules mention that players will score VP by achieving Gambits, which are detailed later, but this information is not provided in the given context. 

I recommend checking the official GW FAQ for more information on Gambits.

### openai/gpt-oss-120b
`finish=stop · 762 compl tok · 2.0s`

**Ruling**  
Gambits are a separate set of objectives that are drawn after the third battle round and can be pursued for Victory Points (VP) for the remainder of the battle. You generate (draw) your Gambits at the end of the third battle round, then you may attempt to achieve them whenever their conditions are met; successful completion awards the VP listed on the Gambit card.

**Rule Citation**  
- **Begin the Battle** – “At the end of the third battle round, players generate Gambits.” (Leviathan, Wahapedia _Leviathan_)  
- **Determine Mission** – “Players take their respective Secondary Mission and Gambit decks, shuffle them and place them nearby for later.” (Leviathan, Wahapedia _Leviathan_)  
- **Read Mission** – “Players will also score VP by achieving Secondary Missions and Gambits, which are detailed later.” (Leviathan, Wahapedia _Leviathan_)  
- **Determine Victor** – “Each player can score a maximum of 50 VP from Primary Missions and/or Gambits …” (Leviathan, Wahapedia _Leviathan_)

**Reasoning**  
The only rule that specifies when Gambits are created is the “Begin the Battle” entry, which states they are generated at the end of the third battle round. The “Determine Mission” entry tells us that each player has a Gambit deck set aside at the start of the game, ready to be drawn when required. The “Read Mission” entry confirms that Gambits are scored like other objectives (Secondary Missions) once their conditions are fulfilled. Finally, “Determine Victor” clarifies that VP earned from Gambits count toward a player’s total score, with a cap of 50 VP from Primary Missions and/or Gambits. Therefore, you draw your Gambits after round 3 and may attempt to complete them at any point thereafter, scoring VP when you meet the Gambit’s stated requirements.

### openai/gpt-oss-20b
`finish=stop · 221 compl tok · 0.4s`

The provided rules do not clearly address how Gambits work in a Leviathan game or when they can be used. I recommend checking the official GW FAQ.

### allam-2-7b
`finish=stop · 228 compl tok · 0.5s`

In a Leviathan game, Gambits are used as a way to add variety and unpredictability to the gameplay. Gambits can be used at any point during the game, but they must be declared before the player's turn begins. To declare a Gambit, the player must choose a Gambit card from their Gambit deck and read out the card's text to their opponent. The opponent must then choose to accept or decline the Gambit. If accepted, the Gambit is played out during the player's turn. If declined, the player's turn proceeds as normal. 


The provided context does not specify a Gambit deck, so I recommend using the standard Warhammer 40k Gambit deck. If a player declares a Gambit, they must read out the card's text to their opponent, who can accept or decline the Gambit. If accepted, the Gambit is played out during the player's turn. If declined, the player's turn proceeds as normal.


====================================================================================================
## [21] UNITS · mp=OFF · ctx 2953 tok

**Q:** When Abaddon the Despoiler fights the Aberrants in melee, how do Abaddon's Devastating Wounds interact with the Aberrants' Feel No Pain?

**Expected concepts (ground-truth anchors):** [['abaddon'], ['aberrant'], ['devastating wounds'], ['feel no pain']]

<details><summary>rules context sent to every model</summary>

```
[1] Abaddon The Despoiler (Chaos Space Marines)
# Abaddon The Despoiler
**Faction:** Chaos Space Marines  |  **Role:** Characters  |  **Source:** 000000012
**Version/Errata Date:** 06.05.2026 0:00:00 *(errata)*

## Stats
| Model | M | T | Sv | Inv | W | Ld | OC | Base |
|---|---|---|---|---|---|---|---|---|
| Abaddon The Despoiler | 5" | 5 | 2+ | 4 | 9 | 5+ | 4 | 60mm |

## Unit Composition
- 1 Abaddon the Despoiler – EPIC HERO

## Points Costs
- 1 model: **270 pts**

## Wargear
| Weapon | Range | Type | A | BS/WS | S | AP | D |
|---|---|---|---|---|---|---|---|
| Talon of Horus | 24 | Ranged | 4 | 2 | 5 | -1 | 2 |
|   | *sustained hits 1* | | | | | | |
| Drach’nyen | Melee | Melee | 8 | 2 | 14 | -4 | 3 |
|   | *devastating wounds* | | | | | | |
| Talon of Horus | Melee | Melee | 14 | 2 | 7 | -3 | 1 |
|   | *devastating wounds* | | | | | | |

## Datasheet Abilities
**The Warmaster**
> In your Command phase, select one Warmaster ability (see left). Until the start of your next Command phase, this model has that ability.

**Dark Destiny**
> Each time this model's unit makes a Dark Pact and does not fail the resulting Leadership test, if the result of that test was 7+, you gain 1CP.

## Faction Abilities
**Dark Pacts**
> If your Army Faction is HERETIC ASTARTES, each time a unit with this ability is selected to shoot or fight, it can make a Dark Pact. If it does, it must first take a Leadership test before any effects of that Dark Pact are resolved; if that test is failed, that unit suffers D3 mortal wounds. Then, select one of the following abilities for that unit’s weapons to gain until the end of the phase: [LETHAL HITS], [SUSTAINED HITS 1]

## Core Abilities
**Deep Strike**
> DEEP STRIKE Some units make their way to battle via tunnelling, teleportation, high-altitude descent or other extraordinary means that allow them to appear suddenly in the thick of the fighting. During the Declare Battle Formations step, if every model in a unit has this ability, you can set it up in Reserves instead of setting it up on the battlefield. If you do, in the Reinforcements step of one of your Movement phases you can set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models. If a unit with the Deep Strike ability arrives from Strategic Reserves, the controlling player can choose for that unit to be set up either using the rules for Strategic Reserves or using the Deep Strike ability. Unit can be set up in Reserves instead of on the battlefield., Unit can be set up in your Reinforcements step, more than 9" horizontally away from all enemy models.

**Leader**
> LEADER Mighty heroes fight at the forefront of battle. Some CHARACTER units have ‘Leader’ listed on their datasheets. Such CHARACTER units are known as Leaders, and the units they can lead – known as their Bodyguard units – are listed on their datasheet. During the Declare Battle Formations step, for each Leader in your army, if your army also includes one or more of that Leader’s Bodyguard units, you can select one of those Bodyguard units. That Leader will then attach to that Bodyguard unit for the duration of the battle and is said to be leading that unit. Each Bodyguard unit can only have one Leader attached to it. While a Bodyguard unit contains a Leader, it is known as an Attached unit and, with the exception of rules that are triggered when units are destroyed, it is treated as a single unit for all rules purposes. Each time an attack targets an Attached unit, until the attacking unit has resolved all of its attacks, you must use the Toughness characteristic of the Bodyguard models in that unit, even if a Leader in that unit has a different Toughness characteristic. Each time an attack sucessfully wounds an Attached unit, that attack cannot be allocated to a CHARACTER model in that unit, even if that CHARACTER model has lost one or more wounds or has already had attacks allocated to it this phase. As soon as the last Bodyguard model in an Attached unit has been destroyed, any attacks made against that unit that have yet to be allocated can then be allocated to CHARACTER models in that unit. Each time the last model in a Bodyguard unit is destroyed, each CHARACTER unit that is part of that Attached unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time the last model in a CHARACTER unit that is attached to a Bodyguard unit is destroyed and there is not another CHARACTER unit attached, that Attached unit’s Bodyguard unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time a unit that is part of an Attached unit is destroyed, it does not have the keywords of any other units that make up that Attached unit (unless it has those keywords on its own datasheet) for the purposes of any rules that would be triggered when that unit is destroyed. Example: If you only destroy the Bodyguard unit that is part of an Attached unit, you have not destroyed a CHARACTER unit. If you only destroy the CHARACTER unit that is part of an Attached unit, or if you destroy the whole Attached unit, you have destroyed one CHARACTER unit. Before the battle, CHARACTER units with the Leader ability can be attached to one of their Bodyguard units to form an Attached unit., Attached units can only contain one Leader., Attacks cannot be allocated to CHARACTER models in Attached units.

## Loadout
This model is equipped with: Talon of Horus; Drach’nyen.

## Keywords
**Faction:** Heretic Astartes
**Other:** Chaos Undivided, Chaos, Abaddon the Despoiler, Infantry, Character, Epic Hero, Terminator


---

[2] Aberrants (Genestealer Cults)
# Ability: Feel No Pain
**Unit:** Aberrants  |  **Faction:** Genestealer Cults

FEEL NO PAIN Some warriors refuse to be laid low, even by what should be fatal wounds. Some models have ‘Feel No Pain x+’ listed in their abilities. Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6: if the result is greater than or equal to the number denoted by ‘x’, that wound is ignored and is not lost. If a model has more than one Feel No Pain ability, you can only use one of those abilities each time that model suffers damage and so would lose a wound. Feel No Pain x+: Each time this model would lose a wound, roll one D6: if the result equals or exceeds ‘x’, that wound is not lost.

---

[3] Devastating Wounds ()
# Devastating Wounds
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Weapons with [DEVASTATING WOUNDS] in their profile are known as Devastating Wounds weapons. Each time an attack is made with such a weapon, if that attack scores a Critical Wound, no saving throw of any kind can be made against that attack (including invulnerable saving throws). Such attacks are only allocated to models after all other attacks made by the attacking unit have been allocated and resolved. After that attack is allocated and after any modifiers are applied, it inflicts a number of mortal wounds on the target equal to the Damage characteristic of that attack, instead of inflicting damage normally. Example: An attack made with a Devastating Wounds weapon with a Damage characteristic of 2 scores a Critical Wound. Instead of allocating the attack and making saving throws normally, the target suffers 2 mortal wounds. A Critical Wound inflicts mortal wounds equal to the weapon's Damage characteristic, instead of any normal damage.

---

[4] 5. Inflict Damage ()
# 5. Inflict Damage — Feel No Pain
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

FEEL NO PAIN Some warriors refuse to be laid low, even by what s
```
</details>


### qwen/qwen3-32b
`finish=stop · 863 compl tok · 2.7s`

[Ruling] When Abaddon the Despoiler’s Devastating Wounds weapon (e.g., Drach’nyen) scores a Critical Wound (unmodified 6+ Wound roll), it inflicts mortal wounds equal to the weapon’s Damage characteristic (3 for Drach’nyen). The Aberrants’ Feel No Pain ability can then be applied to these mortal wounds. Each mortal wound is resolved individually, and the Aberrants roll 1D6 for each wound they would lose: if the result meets or exceeds their Feel No Pain threshold (e.g., 4+), the wound is ignored.  

[Rule Citation]  
- **Devastating Wounds**: [3] → Critical Wounds from Devastating Wounds bypass saving throws and inflict mortal wounds equal to the weapon’s Damage.  
- **Feel No Pain**: [4] → Applies to wounds lost due to mortal wounds, allowing a D6 roll to ignore the wound if the result meets or exceeds the stated threshold.  

[Reasoning]  
Devastating Wounds replace normal damage with mortal wounds (equal to the weapon’s Damage) after all other attacks are resolved. The Aberrants’ Feel No Pain ability explicitly covers wounds lost due to mortal wounds, as per the Core Rules. Each mortal wound from Devastating Wounds triggers a separate Feel No Pain check.

### qwen/qwen3.6-27b
`finish=stop · 2541 compl tok · 5.9s`

[Ruling] When Abaddon the Despoiler’s [DEVASTATING WOUNDS] weapon scores a Critical Wound against an Aberrant, it inflicts mortal wounds equal to the weapon’s Damage characteristic. The Aberrant can then use its Feel No Pain ability to attempt to ignore those mortal wounds.

[Rule Citation] Devastating Wounds (Core Rules), Feel No Pain (Core Rules / Aberrants Datasheet), Wound Roll (Core Rules)

[Reasoning] According to the Wound Roll rule, an unmodified Wound roll of 6 is a Critical Wound [7]. The Devastating Wounds rule states that if an attack with this ability scores a Critical Wound, "no saving throw of any kind can be made against that attack" and it "inflicts a number of mortal wounds on the target equal to the Damage characteristic of that attack, instead of inflicting damage normally" [3]. The Feel No Pain rule explicitly triggers "Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds)" [2]/[4]. Because Devastating Wounds converts the damage into mortal wounds, and Feel No Pain explicitly applies to wounds lost from mortal wounds, the Aberrants roll their Feel No Pain to try to ignore the mortal wounds. Devastating Wounds only negates saving throws, not Feel No Pain.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 364 compl tok · 1.0s`

[Ruling] → [Devastating Wounds] → [Core_Rules, 3] → [Reasoning]

When Abaddon the Despoiler fights the Aberrants in melee, his Devastating Wounds interact with the Aberrants' Feel No Pain as follows:

Abaddon's Devastating Wounds state that if an attack scores a Critical Wound, no saving throw of any kind can be made against that attack (including invulnerable saving throws). Such attacks are only allocated to models after all other attacks made by the attacking unit have been allocated and resolved. After that attack is allocated and after any modifiers are applied, it inflicts a number of mortal wounds on the target equal to the Damage characteristic of that attack, instead of inflicting damage normally.

The Aberrants' Feel No Pain ability states that each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6: if the result is greater than or equal to the number denoted by 'x', that wound is ignored and is not lost.

Since Abaddon's Devastating Wounds attack inflicts mortal wounds instead of normal damage, the Aberrants' Feel No Pain ability does not apply to prevent the loss of wounds. The Devastating Wounds attack will still inflict the specified number of mortal wounds on the target, regardless of the result of the Feel No Pain roll.

Therefore, when Abaddon the Despoiler fights the Aberrants in melee, his Devastating Wounds will interact with the Aberrants' Feel No Pain as follows: the Devastating Wounds attack will inflict the specified number of mortal wounds on the target, and the Feel No Pain ability will not prevent the loss of wounds.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 282 compl tok · 1.4s`

[Ruling] → Abaddon's Devastating Wounds weapons (Drach'nyen and Talon of Horus in melee) inflict mortal wounds directly if they score a Critical Wound, bypassing normal damage and saving throws. → [Devastating Wounds] → The Aberrants' Feel No Pain ability (Feel No Pain 5+) allows them to ignore wounds lost if a D6 roll equals or exceeds 5. 

When Abaddon hits the Aberrants with a Devastating Wounds weapon and scores a Critical Wound, the Aberrants suffer mortal wounds equal to the weapon's Damage characteristic. The Aberrants can then use their Feel No Pain ability to potentially ignore some or all of these mortal wounds. 

For example, if Abaddon hits with Drach'nyen (Damage 3) and scores a Critical Wound, the Aberrants would suffer 3 mortal wounds. They can then roll a D6 for their Feel No Pain ability; if the result equals or exceeds 5, they ignore one of these mortal wounds. 

→ [Devastating Wounds] → [Feel No Pain x+] → Abaddon's Devastating Wounds interact with Aberrants' Feel No Pain by applying the mortal wounds first, then allowing the Aberrants to potentially ignore some of these wounds based on their Feel No Pain roll.

### openai/gpt-oss-120b
`finish=stop · 758 compl tok · 2.3s`

**Ruling**  
When Abaddon the Despoiler makes a melee attack with a weapon that has the **[DEVASTATING WOUNDS]** keyword (e.g., his Drach’nyen or melee Talon of Horus) and the attack scores a Critical Wound, the attack inflicts mortal wounds equal to the weapon’s Damage characteristic and no saving throws can be made. Those mortal wounds are then subject to the Aberrants’ **Feel No Pain** ability; each mortal wound can be ignored if the Aberrant rolls the required D6 result.

**Rule Citations**  

1. **Devastating Wounds** – “Each time an attack is made with such a weapon, if that attack scores a Critical Wound, no saving throw of any kind can be made against that attack… After that attack is allocated … it inflicts a number of mortal wounds on the target equal to the Damage characteristic of that attack, instead of inflicting damage normally.” (Context [3]).

2. **Feel No Pain** – “Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6: if the result is greater than or equal to the number denoted by ‘x’, that wound is ignored and is not lost.” (Context [2] / [4]).

**Reasoning**  

- The Devastating Wounds rule only prevents **saving throws**; it does not prevent other post‑damage effects.  
- Mortal wounds caused by Devastating Wounds are still “damage” that would cause a model to lose a wound.  
- Feel No Pain explicitly applies to any wound loss, *including wounds lost due to mortal wounds* (as quoted above).  
- Therefore, after the Devastating Wounds attack deals its mortal wounds, each Aberrant model that would lose a wound may roll its Feel No Pain dice to potentially ignore that wound.  

Thus, Abaddon’s Devastating Wounds are not negated by Feel No Pain, but the Aberrants can still use Feel No Pain to potentially save themselves from the mortal wounds inflicted.

### openai/gpt-oss-20b
`finish=stop · 1173 compl tok · 1.7s`

**[Ruling]**  
When Abaddon the Despoiler hits an Aberrant with a weapon that has the [DEVASTATING WOUNDS] keyword and the attack scores a Critical Wound, the resulting mortal wounds are still subject to the Aberrant’s [FEEL NO PAIN] ability. Each mortal wound that would normally be lost can be ignored if the model rolls a D6 equal to or greater than the threshold specified by its Feel No Pain ability.

**[Rule Citation]**  
- **Devastating Wounds** – “Each time an attack is made with such a weapon, if that attack scores a Critical Wound, … it inflicts a number of mortal wounds on the target equal to the Damage characteristic of that attack, instead of inflicting damage normally.” (Source: [3] Devastating Wounds)  
- **Feel No Pain** – “Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6: if the result is greater than or equal to the number denoted by ‘x’, that wound is ignored and is not lost.” (Source: [2] Feel No Pain)

**[Reasoning]**  
1. A Critical Wound from a Devastating Wounds weapon triggers the rule that bypasses all saving throws and directly inflicts mortal wounds equal to the weapon’s Damage.  
2. Mortal wounds are a form of damage that causes a model to lose wounds. The Feel No Pain rule explicitly applies to “wounds lost … (including wounds lost due to mortal wounds).”  
3. Therefore, after the mortal wounds are applied, each wound lost can be subject to the Feel No Pain roll. If the roll meets the threshold, that particular wound is ignored; otherwise, the wound is lost as normal.  
4. No rule in the provided context states that Devastating Wounds prevent or override Feel No Pain, so the two abilities interact in the order described above.

### allam-2-7b
`finish=error · ? compl tok · ?s` ⚠ ERROR: Error code: 413 - {'error': {'message': 'Request too large for model `allam-2-7b` in organization `org_01kkppmxccfd1r98zztyme6k5a` service tier `on_demand` on tokens per minute (TPM): Limit 6000, Requ


====================================================================================================
## [22] UNITS · mp=OFF · ctx 1932 tok

**Q:** When An'ggrath the Unbound is destroyed next to an Ork mob led by a Painboy, can the Painboy's Feel No Pain save against the Deadly Demise mortal wounds?

**Expected concepts (ground-truth anchors):** [['an’ggrath', "an'ggrath"], ['painboy'], ['deadly demise'], ['feel no pain']]

<details><summary>rules context sent to every model</summary>

```
[1] Painboy (Orks)
# Ability: Hold Still and Say ‘Aargh!’
**Unit:** Painboy  |  **Faction:** Orks

Each time an attack made by this model with its ’urty syringe scores a Critical Wound against a unit (excluding VEHICLE units), that unit suffers D6 mortal wounds.

---

[2] An’ggrath the Unbound (Chaos Daemons)
# Ability: Deadly Demise
**Unit:** An’ggrath the Unbound  |  **Faction:** Chaos Daemons

DEADLY DEMISE From detonating ammo stores to corrosive innards or frenzied death throes, some targets are deadly even in defeat. Some models have ‘Deadly Demise x’ listed in their abilities. When such a model is destroyed, roll one D6 before removing it from play (if such a model is a TRANSPORT, roll before any embarked models disembark). On a 6, each unit within 6" of that model suffers a number of mortal wounds denoted by ‘x’ (if this is a random number, roll separately for each unit within 6"). Example: A TRANSPORT model with the Deadly Demise D3 ability is destroyed. Before any models disembark and before removing it from play, its controlling player rolls one D6, getting a 6. There are three units within 6" of that destroyed model, so its controlling player rolls one D3 for each of them, inflicting mortal wounds accordingly. Deadly Demise x: When this model is destroyed, roll one D6. On a 6, each unit within 6" suffers ‘x’ mortal wounds.

---

[3] 5. Inflict Damage ()
# 5. Inflict Damage — Feel No Pain
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

FEEL NO PAIN Some warriors refuse to be laid low, even by what should be fatal wounds. Some models have 'Feel No Pain x+' listed in their abilities. Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6: if the result is greater than or equal to the number denoted by 'x', that wound is ignored and is not lost. If a model has more than one Feel No Pain ability, you can only use one of those abilities each time that model suffers damage and so would lose a wound. Feel No Pain x+: Each time this model would lose a wound, roll one D6: if the result equals or exceeds 'x', that wound is not lost.

---

[4] Devastating Wounds ()
# Devastating Wounds
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Weapons with [DEVASTATING WOUNDS] in their profile are known as Devastating Wounds weapons. Each time an attack is made with such a weapon, if that attack scores a Critical Wound, no saving throw of any kind can be made against that attack (including invulnerable saving throws). Such attacks are only allocated to models after all other attacks made by the attacking unit have been allocated and resolved. After that attack is allocated and after any modifiers are applied, it inflicts a number of mortal wounds on the target equal to the Damage characteristic of that attack, instead of inflicting damage normally. Example: An attack made with a Devastating Wounds weapon with a Damage characteristic of 2 scores a Critical Wound. Instead of allocating the attack and making saving throws normally, the target suffers 2 mortal wounds. A Critical Wound inflicts mortal wounds equal to the weapon's Damage characteristic, instead of any normal damage.

---

[5] Mortal Wounds ()
# Mortal Wounds
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some attacks are so powerful that no armour or force field can withstand their fury. Some rules inflict mortal wounds on units. Each time mortal wounds are inflicted on a unit, each of those mortal wounds inflicts one point of damage to that unit, and they are always applied one at a time. Each mortal wound is allocated to a model in the same manner as allocating an attack. Excess damage from mortal wounds is not lost if the damage can be allocated to another model. Instead, keep allocating damage to another model in the target unit until either all the damage has been allocated or the target unit is destroyed. If an attack inflicts mortal wounds in addition to any normal damage, do not make a Wound roll or saving throw (including invulnerable saving throws) against those mortal wounds. If those mortal wounds are inflicted by an attack that has the [PRECISION] ability, the attacking model's controlling player can allocate those mortal wounds to a CHARACTER model in that unit. If mortal wounds are being inflicted as a result of the [HAZARDOUS] ability or by an attack with the [DEVASTATING WOUNDS] ability that scored a Critical Wound, each time those mortal wounds are allocated to a model, if that model is destroyed as a result of those mortal wounds, the remaining mortal wounds from that attack are lost, just as with a normal attack. If, when a unit is selected to shoot or fight, one or more of its attacks can inflict mortal wounds on the target, resolve any normal damage inflicted by the attacking unit's attacks on that target before inflicting any mortal wounds on that target. If an attack inflicts mortal wounds in addition to any normal damage, but the normal damage is subsequently saved, the target unit still suffers those mortal wounds, as described above. Each mortal wound inflicted on a unit causes one model in that unit to lose one wound. Unless the source of the mortal wounds is the [HAZARDOUS] ability or an attack with the [DEVASTATING WOUNDS] ability, damage from mortal wounds is not lost if it can be allocated to another model. No saving throws can be made against mortal wounds. Mortal wounds inflicted by attacks always apply after any normal damage, even if that damage was saved.

---

[6] 5. Inflict Damage ()
# 5. Inflict Damage — Deadly Demise
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

DEADLY DEMISE From detonating ammo stores to corrosive innards or frenzied death throes, some targets are deadly even in defeat. Some models have 'Deadly Demise x' listed in their abilities. When such a model is destroyed, roll one D6 before removing it from play (if such a model is a TRANSPORT, roll before any embarked models disembark). On a 6, each unit within 6" of that model suffers a number of mortal wounds denoted by 'x' (if this is a random number, roll separately for each unit within 6"). Example: A TRANSPORT model with the Deadly Demise D3 ability is destroyed. Before any models disembark and before removing it from play, its controlling player rolls one D6, getting a 6. There are three units within 6" of that destroyed model, so its controlling player rolls one D3 for each of them, inflicting mortal wounds accordingly. Deadly Demise x: When this model is destroyed, roll one D6. On a 6, each unit within 6" suffers 'x' mortal wounds.

---

[7] An’ggrath the Unbound (Chaos Daemons)
# An’ggrath the Unbound — Damaged
**Unit:** An’ggrath the Unbound  |  **Faction:** Chaos Daemons

*Damaged threshold: 1-8 wounds remaining*
> While this model has 1-8 wounds remaining, each time this model makes an attack, subtract 1 from the Hit roll.

---

[8] Beastboss (Orks)
# Ability: Feel No Pain
**Unit:** Beastboss  |  **Faction:** Orks

FEEL NO PAIN Some warriors refuse to be laid low, even by what should be fatal wounds. Some models have ‘Feel No Pain x+’ listed in their abilities. Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6: if the result is greater than or equal to the number denoted by ‘x’, that wound is ignored and is not lost. If a model has more than one Feel No Pain ability, you can only use one of those abilities each time that model suffers damage and so would lose a wound. Feel No Pain x+: Each time this model would lose a wound, roll one D6: if the result equals or exceeds ‘x’, that wound is not lost.
```
</details>


### qwen/qwen3-32b
`finish=stop · 737 compl tok · 1.9s`

[Ruling] Yes, the Painboy can use its Feel No Pain ability to save against the mortal wounds caused by An’ggrath’s Deadly Demise.  

[Rule Citation]  
- **Feel No Pain x+** (Core Rules, [3])  
- **Deadly Demise x** (Core Rules, [2] and [6])  
- **Mortal Wounds** (Core Rules, [5])  

[Reasoning]  
1. **Deadly Demise** inflicts mortal wounds on units within 6" of the destroyed model (An’ggrath). These wounds are applied one at a time, per the Mortal Wounds rules.  
2. **Feel No Pain x+** allows a model to roll a D6 each time it would lose a wound (including mortal wounds). If the roll meets or exceeds the stated value, the wound is ignored.  
3. The **Mortal Wounds** rules confirm that Feel No Pain applies to mortal wounds unless explicitly restricted (e.g., by [HAZARDOUS] or [DEVASTATING WOUNDS]). Since Deadly Demise does not restrict Feel No Pain, the Painboy’s ability functions normally.  
4. Each mortal wound from Deadly Demise is resolved individually, giving the Painboy a separate chance to save against each wound using Feel No Pain.

### qwen/qwen3.6-27b
`finish=stop · 2288 compl tok · 5.0s`

[Ruling] Yes, the Painboy can use its Feel No Pain ability to ignore the wounds lost from the mortal wounds inflicted by An’ggrath’s Deadly Demise.

[Rule Citation] Core Rules: 5. Inflict Damage — Feel No Pain [3]; Core Rules: Mortal Wounds [5]; An’ggrath the Unbound — Deadly Demise [2]

[Reasoning] An’ggrath’s Deadly Demise ability inflicts mortal wounds on each unit within 6" when the model is destroyed [2]. The Mortal Wounds core rule states that each mortal wound inflicts one point of damage and causes a model to lose one wound [5]. The Feel No Pain core rule explicitly triggers "Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds)" [3]. Because the rule explicitly includes wounds lost due to mortal wounds, the Painboy can roll its Feel No Pain to ignore the damage from the Deadly Demise mortal wounds.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 109 compl tok · 0.6s`

[Ruling] → [5. Inflict Damage — Deadly Demise] → [Reasoning].

The Painboy's Feel No Pain ability does not apply to the Deadly Demise mortal wounds inflicted by An'ggrath the Unbound's destruction. According to [5. Inflict Damage — Deadly Demise], mortal wounds inflicted by the Deadly Demise ability are not subject to saving throws, including invulnerable saving throws. Therefore, the Painboy cannot use its Feel No Pain ability to save against the Deadly Demise mortal wounds.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 164 compl tok · 1.1s`

Ruling → No, the Painboy's Feel No Pain ability does not apply to mortal wounds inflicted by Deadly Demise. 
→ [Mortal Wounds] → The provided Core Rules state that "No saving throws can be made against mortal wounds." This directly overrides any Feel No Pain ability, as Feel No Pain is a saving throw-like mechanism. 
→ [Reasoning] The Core Rules for Mortal Wounds explicitly state that no saving throws can be made against them. Since Feel No Pain is essentially a type of saving throw, it does not apply to mortal wounds inflicted by Deadly Demise. Therefore, when An'ggrath the Unbound is destroyed next to the Ork mob, the Painboy's Feel No Pain ability cannot save against the Deadly Demise mortal wounds.

### openai/gpt-oss-120b
`finish=stop · 932 compl tok · 2.4s`

**Ruling:** Yes. If the Painboy model has a Feel No Pain ability, it may attempt a Feel No Pain roll for each mortal wound it suffers from An’ggrath the Unbound’s Deadly Demise ability.

**Rule Citation:**  
- **Mortal Wounds** – “Each mortal wound … No saving throws can be made against mortal wounds.” (Rule [5] Mortal Wounds)  
- **Feel No Pain** – “Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6… that wound is ignored and is not lost.” (Rule [3] Feel No Pain)

**Reasoning:**  
When An’ggrath the Unbound is destroyed, its Deadly Demise ability triggers, causing each unit within 6″ to suffer a number of mortal wounds (Rule [2]/[6]). Mortal wounds are a form of damage that bypasses saving throws (Rule [5]), but the Feel No Pain rule explicitly states it applies **including wounds lost due to mortal wounds**. Since Feel No Pain is not a saving throw but a wound‑ignore ability, the restriction in the Mortal Wounds rule does not prevent its use. Therefore, the Painboy may roll a Feel No Pain check for each mortal wound it receives from the Deadly Demise effect, potentially ignoring those wounds.

### openai/gpt-oss-20b
`finish=stop · 1257 compl tok · 1.6s`

**Ruling**  
No – the Painboy cannot use a Feel No Pain save against the mortal wounds from An’ggrath’s Deadly Demise, because the Painboy does not have a Feel No Pain ability.

**Rule Citations**  
- Painboy (Orks) – Ability: Hold Still and Say ‘Aargh!’【1】  
- Feel No Pain – “Each time a model with this ability suffers damage and so would lose a wound (including wounds lost due to mortal wounds), roll one D6… that wound is ignored”【3】

**Reasoning**  
The Painboy’s only listed ability is Hold Still and Say ‘Aargh!’, which grants mortal wounds to other units when its urty syringe scores a Critical Wound. The Painboy’s datasheet does not include a Feel No Pain ability. Feel No Pain applies only to models that possess that ability; it allows a model to ignore a wound that would otherwise be lost, including those from mortal wounds. Since the Painboy lacks this ability, it cannot use it to save against the mortal wounds inflicted by An’ggrath’s Deadly Demise.

### allam-2-7b
`finish=stop · 1429 compl tok · 2.4s`

Based on the provided rules, when An'ggrath the Unbound is destroyed, the Painboy's Feel No Pain ability can be used against the Deadly Demise mortal wounds. 


---


---


---


---


---


---


---


---


---


---


---


---


---


---


---


---


---


---

---

---

---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---


====================================================================================================
## [23] UNITS · mp=OFF · ctx 1701 tok

**Q:** Compare the transport capacity of a Battlewagon and a Trukk, and what kinds of models each one is allowed to carry.

**Expected concepts (ground-truth anchors):** [['battlewagon'], ['trukk'], ['transport capacity', 'transport']]

<details><summary>rules context sent to every model</summary>

```
[1] Battlewagon (Orks)
# Battlewagon — Transport
**Unit:** Battlewagon  |  **Faction:** Orks

This model has a transport capacity of 22 Orks Infantry models. If this model is equipped with a killkannon, it has a transport capacity of 12 ORKS INFANTRY models. Each Mega Armour or Jump Pack model takes up the space of 2 models. The Ghazghkull Thraka model takes up the space of 4 models.

---

[2] Trukk (Orks)
# Trukk — Transport
**Unit:** Trukk  |  **Faction:** Orks

This model has a transport capacity of 12 Orks Infantry models. Each Mega Armour model takes up the space of 2 models. It cannot transport Jump Pack or Ghazghkull Thraka models.

---

[3] Transport Capacity ()
# Transport Capacity
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

All TRANSPORT models have a transport capacity listed on their datasheet. This determines the type and maximum number of friendly models that can embark within them. Units can start the battle embarked within a TRANSPORT model instead of being set up separately - declare which units are embarked within a TRANSPORT model before you set it up. FIRING DECK Some transports have firing hatches, ports or platforms from which embarked passengers can shoot. Some TRANSPORT models have 'Firing Deck x' listed in their abilities. Each time such a model is selected to shoot in the Shooting phase, you can select up to 'x' models embarked within it whose units have not already shot this phase. Then, for each of those embarked models, you can select one ranged weapon that embarked model is equipped with (excluding weapons with the [ONE SHOT] ability). Until that TRANSPORT model has resolved all of its attacks, it counts as being equipped with all of the weapons you selected in this way, in addition to its other weapons. Until the end of the phase, those selected models' units are not eligible to shoot. Firing Deck 'x': Each time this TRANSPORT shoots, select one weapon (excluding weapons with the [ONE SHOT] ability) from up to 'x' models embarked within it whose units have not shot this phase; this TRANSPORT counts as being equipped with those weapons as well. Until the end of the phase, those selected models' units are not eligible to shoot.

---

[4] Transports ()
# Transports
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some models have the TRANSPORT keyword. The following rules describe how units can embark within and disembark from such models, and how they are used to move these passengers across the battlefield.
Some units can carry others across the battlefield, providing their passengers with greater speed and protection as they are ferried to the front lines or towards vital objectives.

---

[5] Unit Composition and Other Rules ()
# Unit Composition and Other Rules
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

This section details the number and types of models in the unit, and the default weapons and wargear those models are equipped with. It may also describe other interactions, such as how units with the Leader ability can attach to other units, and passenger restrictions that may apply to TRANSPORT models.

---

[6] Deployment Abilities ()
# Deployment Abilities — Scouts
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

SCOUTS Scouts form the vanguard of many armies. Unnoticed by the enemy, they range ahead of the main force. Some units have 'Scouts x"' listed in their abilities. If every model in a unit has this ability, then at the start of the first battle round, before the first turn begins, it can make a Normal move of up to x", with the exception that, while making that move, the distance moved by each model in that unit can be greater than that model's Move characteristic, as long as it is not greater than x". DEDICATED TRANSPORT models can make use of any Scouts x" ability listed in their abilities, or a Scouts x" ability that a unit that starts the battle embarked within that DEDICATED TRANSPORT model has (provided only models with this ability are embarked within that DEDICATED TRANSPORT model), regardless of how that embarked unit gained this ability (e.g. listed in their abilities, conferred by an Enhancement or by an attached CHARACTER, etc.). A unit that moves using this ability must end that move more than 9" horizontally away from all enemy models. If both players have units that can do this, the player who is taking the first turn moves their units first. Example: A unit has the Scouts 6" ability. At the start of the first battle round, the controlling player can make a Normal move with that unit of up to 6". Scouts x": Unit can make a Normal move of up to x" before the first turn begins. If embarked in a DEDICATED TRANSPORT, that DEDICATED TRANSPORT can make this move instead. Must end this move more than 9" horizontally away from all enemy models.

---

[7] Battlewagon (Orks)
# Ability: Firing Deck
**Unit:** Battlewagon  |  **Faction:** Orks

FIRING DECK Some transports have firing hatches, ports or platforms from which embarked passengers can shoot. Some TRANSPORT models have ‘Firing Deck x’ listed in their abilities. Each time such a model is selected to shoot in the Shooting phase, you can select up to ‘x’ models embarked within it whose units have not already shot this phase. Then, for each of those embarked models, you can select one ranged weapon that embarked model is equipped with (excluding weapons with the [ONE SHOT] ability). Until that TRANSPORT model has resolved all of its attacks, it counts as being equipped with all of the weapons you selected in this way, in addition to its other weapons. Until the end of the phase, those selected models’ units are not eligible to shoot. Firing Deck ‘x’: Each time this TRANSPORT shoots, select one weapon (excluding weapons with the [ONE SHOT] ability) from up to ‘x’ models embarked within it whose units have not shot this phase; this TRANSPORT counts as being equipped with those weapons as well. Until the end of the phase, those selected models’ units are not eligible to shoot.

---

[8] Venom (Drukhari)
# Venom — Transport
**Unit:** Venom  |  **Faction:** Drukhari

This model has a transport capacity of 6 Drukhari Infantry models (excluding Jump Pack models). Before the battle, at the start of the Declare Battle Formations step, you can select one Kabalite Warriors, Hand of the Archon or Wyches unit from your army that has not already been split. If you do, that unit is split into two units, each containing as equal a number of models as possible (when splitting a unit in this way, make a note of which models form each of the two new units]. One of these units must start the battle embarked within this model; the other can start the battle embarked within another TRANSPORT, or it can be deployed as a separate unit.
```
</details>


### qwen/qwen3-32b
`finish=stop · 695 compl tok · 1.8s`

[Ruling]  
The **Battlewagon** has a transport capacity of **22 Orks Infantry models** (or **12** if equipped with a killkannon). It can carry **Mega Armour** or **Jump Pack** models (each taking 2 spaces) and the **Ghazghkull Thraka** model (taking 4 spaces). The **Trukk** has a transport capacity of **12 Orks Infantry models**, but **cannot** carry **Jump Pack** or **Ghazghkull Thraka** models. **Mega Armour** models in the Trukk take 2 spaces.  

[Rule Citations]  
- **Battlewagon**: [1] Battlewagon (Orks) → Transport Capacity and Restrictions.  
- **Trukk**: [2] Trukk (Orks) → Transport Capacity and Restrictions.  
- **Core Transport Rules**: [3] Transport Capacity (Core Rules) → General transport capacity rules.  

[Reasoning]  
The Battlewagon’s capacity and allowed models are explicitly defined in its datasheet ([1]), including exceptions for killkannon-equipped capacity and space penalties for specific models. The Trukk’s capacity and restrictions are defined in its datasheet ([2]), explicitly banning Jump Pack and Ghazghkull Thraka models. Core transport rules ([3]) apply universally but do not override these model-specific exceptions.

### qwen/qwen3.6-27b
`finish=stop · 2081 compl tok · 4.4s`

[Ruling] The Battlewagon has a higher base transport capacity than the Trukk, but its capacity is reduced if equipped with a Killkannon. While both transports can carry standard Orks Infantry and Mega Armour models, the Battlewagon can also carry Jump Pack models and Ghazghkull Thraka (at a space cost), whereas the Trukk explicitly cannot carry either of those specific model types.

[Rule Citation] Battlewagon — Transport (Source [1]); Trukk — Transport (Source [2])

[Reasoning] 
- **Battlewagon:** Has a base transport capacity of 22 Orks Infantry models. If equipped with a Killkannon, its capacity is reduced to 12. It can transport Mega Armour and Jump Pack models, but each of those takes up the space of 2 models. It can also transport the Ghazghkull Thraka model, which takes up the space of 4 models.
- **Trukk:** Has a fixed transport capacity of 12 Orks Infantry models. It can transport Mega Armour models (each taking up the space of 2 models), but it explicitly cannot transport Jump Pack models or the Ghazghkull Thraka model.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 336 compl tok · 0.9s`

**Ruling:** A Battlewagon has a higher transport capacity than a Trukk, and it can carry different types of models.

**Rule Citation:** [3] Transport Capacity → "All TRANSPORT models have a transport capacity listed on their datasheet. This determines the type and maximum number of friendly models that can embark within them."

**Reasoning:** According to the datasheet, a Battlewagon has a transport capacity of 22 Orks Infantry models, unless it is equipped with a killkannon, in which case it has a transport capacity of 12 Orks Infantry models. A Trukk, on the other hand, has a transport capacity of 12 Orks Infantry models. Therefore, a Battlewagon has a higher transport capacity than a Trukk.

**Rule Citation:** [2] Trukk → "It cannot transport Jump Pack or Ghazghkull Thraka models."

**Reasoning:** According to the datasheet, a Trukk cannot transport Jump Pack or Ghazghkull Thraka models. There is no such restriction on a Battlewagon, so it can carry these types of models.

**Rule Citation:** [1] Battlewagon → "Each Mega Armour or Jump Pack model takes up the space of 2 models. The Ghazghkull Thraka model takes up the space of 4 models."

**Reasoning:** According to the datasheet, a Battlewagon can carry Mega Armour or Jump Pack models, but each one takes up the space of 2 models. It can also carry Ghazghkull Thraka models, but each one takes up the space of 4 models.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 206 compl tok · 1.0s`

[Ruling] → The transport capacity of a Battlewagon and a Trukk differ significantly. A Battlewagon has a base transport capacity of 22 Orks Infantry models, which is reduced to 12 Orks Infantry models if equipped with a killkannon. In contrast, a Trukk has a transport capacity of 12 Orks Infantry models.

→ [Battlewagon, Trukk datasheets] → 

[Reasoning] The Battlewagon's transport capacity is affected by the presence of a killkannon, whereas the Trukk's capacity remains fixed. Additionally, the types of models that can be carried by each transport are specified: a Battlewagon can carry Mega Armour or Jump Pack models (with each counting as 2 models) and a Ghazghkull Thraka model (counting as 4 models), while a Trukk can carry Mega Armour models (with each counting as 2 models) but not Jump Pack or Ghazghkull Thraka models.

### openai/gpt-oss-120b
`finish=stop · 624 compl tok · 1.7s`

**Ruling**  
- **Battlewagon:** Can embark up to 22 Orks Infantry models (or 12 if the Battlewagon is equipped with a killkannon). Each Mega Armour or Jump Pack model occupies the space of 2 models, and a Ghazghkull Thraka model occupies the space of 4 models.  
- **Trukk:** Can embark up to 12 Orks Infantry models. Each Mega Armour model occupies the space of 2 models, but the Trukk **cannot** transport Jump Pack models or a Ghazghkull Thraka model.

**Rule Citations**  
- Battlewagon transport capacity and model‑space rules: **[1] Battlewagon (Orks)**.  
- Trukk transport capacity and model‑space restrictions: **[2] Trukk (Orks)**.  

**Reasoning**  
The Battlewagon entry states its base capacity (22 Infantry) and the reduced capacity when fitted with a killkannon (12 Infantry), and specifies how Mega Armour, Jump Pack, and Ghazghkull Thraka models count against that capacity. The Trukk entry gives a fixed capacity of 12 Infantry, the same 2‑model space cost for Mega Armour, and explicitly prohibits transporting Jump Pack or Ghazghkull Thraka models. Comparing the two, the Battlewagon can carry more infantry overall and is permitted to transport Jump Pack and Ghazghkull Thraka models (with the appropriate space cost), whereas the Trukk carries fewer infantry and is limited to Infantry and Mega Armour models only.

### openai/gpt-oss-20b
`finish=stop · 651 compl tok · 1.2s`

**[Ruling]**  
A Battlewagon can transport up to 22 Orks Infantry models (12 if it is equipped with a killkannon). It may also carry Mega Armour models (each counts as 2 models) and Jump Pack models (each counts as 2 models), and it can carry a Ghazghkull Thraka model (counts as 4 models).  
A Trukk can transport up to 12 Orks Infantry models. It may carry Mega Armour models (each counts as 2 models) but it cannot transport Jump Pack models or a Ghazghkull Thraka model.

**[Rule Citations]**  
- Battlewagon transport capacity and model‑space rules: [1] Battlewagon (Orks) – “This model has a transport capacity of 22 Orks Infantry models… Each Mega Armour or Jump Pack model takes up the space of 2 models. The Ghazghkull Thraka model takes up the space of 4 models.”  
- Trukk transport capacity and restrictions: [2] Trukk (Orks) – “This model has a transport capacity of 12 Orks Infantry models… It cannot transport Jump Pack or Ghazghkull Thraka models.”

**[Reasoning]**  
The transport capacity figures and model‑space rules are explicitly listed in the Battlewagon and Trukk datasheets ([1] and [2]). The Trukk’s prohibition on carrying Jump Pack or Ghazghkull Thraka models is also explicitly stated in its datasheet ([2]). No other rules in the provided context alter or override these capacities or restrictions.

### allam-2-7b
`finish=stop · 317 compl tok · 0.6s`

Based on the provided rules, let's compare the transport capacity of a Battlewagon and a Trukk.


For Battlewagons:

The transport capacity of a Battlewagon is not explicitly stated in the provided context. However, it is mentioned that the Battlewagon has a Leviathan Dreadnought ability, which allows it to carry 20 Ork models.


For Trukk:

The transport capacity of a Trukk is explicitly stated as 12 Ork models.


In comparing the transport capacity of a Battlewagon and a Trukk:


The Trukk has a higher transport capacity (12 Ork models) compared to the Battlewagon (20 Ork models).


Now, let's discuss which models each vehicle is allowed to carry:


The Battlewagon allows for 20 Ork models, while the Trukk allows for 12 Ork models. Both vehicles can carry Ork models, but the Trukk has a higher capacity than the Battlewagon. 


The provided rules do not specify which models are allowed to embark within the vehicles. However, the context does mention that the Battlewagon has a Leviathan Dreadnought ability, which allows it to carry 20 Ork models.


In summary, the Battlewagon can carry 20 Ork models, while the Trukk can carry 12 Ork models.


====================================================================================================
## [24] UNITS · mp=OFF · ctx 1920 tok

**Q:** If a Callidus Assassin and Boss Snikrot both deploy using Infiltrators, how close to the enemy can each of them be set up?

**Expected concepts (ground-truth anchors):** [['callidus'], ['snikrot'], ['infiltrator']]

<details><summary>rules context sent to every model</summary>

```
[1] Callidus Assassin (Imperial Agents)
# Ability: Acrobatic Escape
**Unit:** Callidus Assassin  |  **Faction:** Imperial Agents

At the end of the Fight phase, if this model is within Engagement Range of one or more enemy units, it can make a Fall Back move of up to D6". In addition, at the end of your opponent’s turn, if this model is not within 3" of one or more enemy units, you can remove it from the battlefield and then, in the Reinforcements step of your next Movement phase, set it up anywhere on the battlefield that is more than 9" horizontally away from all enemy models. If the battle ends and this model is not on the battlefield, it is destroyed.

---

[2] Boss Snikrot (Orks)
# Ability: Leader
**Unit:** Boss Snikrot  |  **Faction:** Orks

LEADER Mighty heroes fight at the forefront of battle. Some CHARACTER units have ‘Leader’ listed on their datasheets. Such CHARACTER units are known as Leaders, and the units they can lead – known as their Bodyguard units – are listed on their datasheet. During the Declare Battle Formations step, for each Leader in your army, if your army also includes one or more of that Leader’s Bodyguard units, you can select one of those Bodyguard units. That Leader will then attach to that Bodyguard unit for the duration of the battle and is said to be leading that unit. Each Bodyguard unit can only have one Leader attached to it. While a Bodyguard unit contains a Leader, it is known as an Attached unit and, with the exception of rules that are triggered when units are destroyed, it is treated as a single unit for all rules purposes. Each time an attack targets an Attached unit, until the attacking unit has resolved all of its attacks, you must use the Toughness characteristic of the Bodyguard models in that unit, even if a Leader in that unit has a different Toughness characteristic. Each time an attack sucessfully wounds an Attached unit, that attack cannot be allocated to a CHARACTER model in that unit, even if that CHARACTER model has lost one or more wounds or has already had attacks allocated to it this phase. As soon as the last Bodyguard model in an Attached unit has been destroyed, any attacks made against that unit that have yet to be allocated can then be allocated to CHARACTER models in that unit. Each time the last model in a Bodyguard unit is destroyed, each CHARACTER unit that is part of that Attached unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time the last model in a CHARACTER unit that is attached to a Bodyguard unit is destroyed and there is not another CHARACTER unit attached, that Attached unit’s Bodyguard unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time a unit that is part of an Attached unit is destroyed, it does not have the keywords of any other units that make up that Attached unit (unless it has those keywords on its own datasheet) for the purposes of any rules that would be triggered when that unit is destroyed. Example: If you only destroy the Bodyguard unit that is part of an Attached unit, you have not destroyed a CHARACTER unit. If you only destroy the CHARACTER unit that is part of an Attached unit, or if you destroy the whole Attached unit, you have destroyed one CHARACTER unit. Before the battle, CHARACTER units with the Leader ability can be attached to one of their Bodyguard units to form an Attached unit., Attached units can only contain one Leader., Attacks cannot be allocated to CHARACTER models in Attached units.

---

[3] Deployment Abilities ()
# Deployment Abilities — Infiltrators
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

INFILTRATORS Many armies employ reconnaissance units who can sit concealed, waiting for the right moment to strike. During deployment, if every model in a unit has this ability, then when you set it up, it can be set up anywhere on the battlefield that is more than 9" horizontally away from the enemy deployment zone and all enemy models.

---

[4] Stratagems That Allow a Closer Set Up Range* ()
# Stratagems That Allow a Closer Set Up Range*
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a Stratagem has an effect that allows the targeted unit to be set up 'more than 3" horizontally away' from all enemy models/units (e.g. Cosmic Precision, Prognosticated Arrival, Denizens of the Warp, etc.), that part of that effect is changed to say 'more than 6" horizontally away'.

---

[5] Redeployments ()
# Redeployments
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Rules that allow players to redeploy certain units after both armies are deployed (e.g. HURON BLACKHEART 's Red Corsairs ability) are always resolved after the Deploy Armies step (or, if you are playing a Crusade battle, after the Deploy Crusade Armies step), and before the Determine First Turn step, before determining who has the first turn. When a player uses such a rule, they remove that unit or units from the battlefield, then deploy them again using all the normal rules (for example, if all the models in one of these units have the Infiltrators ability, that unit's player can set that unit up using that ability). Players alternate resolving any such rules, starting with the Attacker.

---

[6] Advance Moves ()
# Advance Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Advances, make an Advance roll for that unit by rolling one D6. Add the result in inches to the Move characteristic of each model in that unit until the end of the phase. Each model in that unit can then make an Advance move by moving a distance in inches less than or equal to this total, but no model can be moved within Engagement Range of enemy models. A unit cannot shoot or declare a charge in the same turn that it Advanced.
Advance Move: Models move up to M+D6". Cannot move within Engagement Range of any enemy models. Units that Advance cannot shoot or charge this turn.

---

[7] Callidus Assassin (Imperial Agents)
# Ability: Deep Strike
**Unit:** Callidus Assassin  |  **Faction:** Imperial Agents

DEEP STRIKE Some units make their way to battle via tunnelling, teleportation, high-altitude descent or other extraordinary means that allow them to appear suddenly in the thick of the fighting. During the Declare Battle Formations step, if every model in a unit has this ability, you can set it up in Reserves instead of setting it up on the battlefield. If you do, in the Reinforcements step of one of your Movement phases you can set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models. If a unit with the Deep Strike ability arrives from Strategic Reserves, the controlling player can choose for that unit to be set up either using the rules for Strategic Reserves or using the Deep Strike ability. Unit can be set up in Reserves instead of on the battlefield., Unit can be set up in your Reinforcements step, more than 9" horizontally away from all enemy models.

---

[8] Boss Snikrot (Orks)
# Ability: Kunnin’ Infiltrator
**Unit:** Boss Snikrot  |  **Faction:** Orks

Once per battle, in your Movement phase, instead of making a Normal move with this model’s unit, you can remove it from the battlefield and set it up again anywhere on the battlefield that is more than 9" horizontally away from all enemy models.
```
</details>


### qwen/qwen3-32b
`finish=stop · 726 compl tok · 1.9s`

[Ruling] Both the Callidus Assassin and Boss Snikrot can be set up using the **Infiltrators** rule, which allows them to be placed **more than 9" horizontally away from all enemy models**. This applies to both units during deployment.  

[Rule Citation] **Infiltrators** (Core Rules) → [3]  
[Reasoning] The **Infiltrators** rule explicitly permits units to be set up "more than 9" horizontally away from the enemy deployment zone and all enemy models" during deployment. Neither the Callidus Assassin’s **Deep Strike** (rule [7]) nor Boss Snikrot’s **Kunnin’ Infiltrator** (rule [8]) override this during deployment—they only provide alternative methods for arriving later in the game. Since the question specifies both units are using **Infiltrators**, the 9" minimum distance applies to both.

### qwen/qwen3.6-27b
`finish=stop · 1759 compl tok · 33.8s`

[Ruling] Both units must be set up more than 9" horizontally away from the enemy deployment zone and all enemy models.

[Rule Citation] Infiltrators (Core Rules)

[Reasoning] The Infiltrators ability explicitly states that during deployment, if every model in a unit has this ability, it can be set up anywhere on the battlefield that is more than 9" horizontally away from the enemy deployment zone and all enemy models. This deployment requirement applies identically to both units when using Infiltrators. Boss Snikrot’s "Kunnin’ Infiltrator" ability only functions during the Movement phase and does not alter deployment rules, and the "Stratagems That Allow a Closer Set Up Range" rule only modifies specific stratagems, not the Infiltrators ability. Therefore, the standard 9" horizontal distance requirement applies to both.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 243 compl tok · 1.2s`

[Ruling] → [Rule Citation] → [Reasoning]

Callidus Assassin: 
The Callidus Assassin can be set up anywhere on the battlefield that is more than 9" horizontally away from the enemy deployment zone and all enemy models. → [3] Infiltrators → [Core_Rules, Wahapedia_Core_Rules]

Boss Snikrot: 
The Boss Snikrot can be set up anywhere on the battlefield that is more than 9" horizontally away from all enemy models. → [8] Kunnin’ Infiltrator → [Boss Snikrot datasheet]

However, since both units are using Infiltrators, we need to apply the rule from [4] Stratagems That Allow a Closer Set Up Range*. This rule changes the set-up range to more than 6" horizontally away from all enemy models. → [4] Stratagems That Allow a Closer Set Up Range* → [Core_Rules, Wahapedia_Core_Rules]

Therefore, both the Callidus Assassin and the Boss Snikrot can be set up anywhere on the battlefield that is more than 6" horizontally away from all enemy models.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 187 compl tok · 1.3s`

[Ruling] → The Callidus Assassin and Boss Snikrot can both be set up more than 9" horizontally away from all enemy models.

→ [3] Deployment Abilities — Infiltrators: 
"During deployment, if every model in a unit has this ability, then when you set it up, it can be set up anywhere on the battlefield that is more than 9" horizontally away from the enemy deployment zone and all enemy models."

→ [Reasoning]: 
Both units have models with the Infiltrators ability. According to the Infiltrators ability, they can be set up more than 9" horizontally away from all enemy models. There are no additional rules provided that would change this setup range for these specific units. Therefore, both the Callidus Assassin and Boss Snikrot can be set up more than 9" horizontally away from all enemy models when using the Infiltrators ability.

### openai/gpt-oss-120b
`finish=stop · 632 compl tok · 1.9s`

**Ruling:**  
When a Callidus Assassin and a Boss Snikrot each deploy using the **Infiltrators** ability, each unit must be set up **more than 9" horizontally away from all enemy models (and, for Infiltrators, also more than 9" from the enemy deployment zone).** No rule in the provided context reduces this distance, so the minimum allowable distance is 10".

**Rule Citation:**  
- **Infiltrators** – “During deployment, if every model in a unit has this ability, then when you set it up, it can be set up anywhere on the battlefield that is **more than 9" horizontally away from the enemy deployment zone and all enemy models**.” [Rule 3]

**Reasoning:**  
The Infiltrators deployment rule explicitly sets the required minimum distance at “more than 9 inches” from enemy models (and the enemy deployment zone). The only other rule that modifies set‑up distances is the **Stratagems That Allow a Closer Set Up Range** rule, which only changes distances that are “more than 3 inches” to “more than 6 inches.” Since the Infiltrators rule already specifies “more than 9 inches,” it is not affected by that stratagem rule. Therefore, both the Callidus Assassin and the Boss Snikrot must be placed at least 10" away from any enemy model (and the enemy deployment zone for the Assassin).

### openai/gpt-oss-20b
`finish=stop · 809 compl tok · 1.2s`

**Ruling**  
Both the Callidus Assassin and the Boss Snikrot can be set up during deployment at a distance of **more than 9 inches horizontally away from all enemy models**.

**Rule Citation**  
[3] *Deployment Abilities – Infiltrators*: “During deployment, if every model in a unit has this ability, then when you set it up, it can be set up anywhere on the battlefield that is more than 9" horizontally away from the enemy deployment zone and all enemy models.”

**Reasoning**  
The Infiltrators ability applies to any unit that possesses it, regardless of other abilities the unit may have (e.g., Deep Strike for the Callidus Assassin). The ability explicitly states the deployment distance requirement, and no other rule in the provided context modifies that distance for these units. Therefore, each unit may be deployed at a distance of more than 9" from all enemy models.

### allam-2-7b
`finish=stop · 1534 compl tok · 1.5s`

Based on the provided rules, the Callidus Assassin and Boss Snikrot both deploy using their respective abilities (Deep Strike and Kunnin' Infiltrator).


---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---


====================================================================================================
## [25] UNITS · mp=OFF · ctx 2544 tok

**Q:** What melee weapons does Abaddon the Despoiler have on his datasheet, and what does his Dark Destiny ability do?

**Expected concepts (ground-truth anchors):** [['abaddon'], ['dark destiny']]

<details><summary>rules context sent to every model</summary>

```
[1] Abaddon The Despoiler (Chaos Space Marines)
# Abaddon The Despoiler
**Faction:** Chaos Space Marines  |  **Role:** Characters  |  **Source:** 000000012
**Version/Errata Date:** 06.05.2026 0:00:00 *(errata)*

## Stats
| Model | M | T | Sv | Inv | W | Ld | OC | Base |
|---|---|---|---|---|---|---|---|---|
| Abaddon The Despoiler | 5" | 5 | 2+ | 4 | 9 | 5+ | 4 | 60mm |

## Unit Composition
- 1 Abaddon the Despoiler – EPIC HERO

## Points Costs
- 1 model: **270 pts**

## Wargear
| Weapon | Range | Type | A | BS/WS | S | AP | D |
|---|---|---|---|---|---|---|---|
| Talon of Horus | 24 | Ranged | 4 | 2 | 5 | -1 | 2 |
|   | *sustained hits 1* | | | | | | |
| Drach’nyen | Melee | Melee | 8 | 2 | 14 | -4 | 3 |
|   | *devastating wounds* | | | | | | |
| Talon of Horus | Melee | Melee | 14 | 2 | 7 | -3 | 1 |
|   | *devastating wounds* | | | | | | |

## Datasheet Abilities
**The Warmaster**
> In your Command phase, select one Warmaster ability (see left). Until the start of your next Command phase, this model has that ability.

**Dark Destiny**
> Each time this model's unit makes a Dark Pact and does not fail the resulting Leadership test, if the result of that test was 7+, you gain 1CP.

## Faction Abilities
**Dark Pacts**
> If your Army Faction is HERETIC ASTARTES, each time a unit with this ability is selected to shoot or fight, it can make a Dark Pact. If it does, it must first take a Leadership test before any effects of that Dark Pact are resolved; if that test is failed, that unit suffers D3 mortal wounds. Then, select one of the following abilities for that unit’s weapons to gain until the end of the phase: [LETHAL HITS], [SUSTAINED HITS 1]

## Core Abilities
**Deep Strike**
> DEEP STRIKE Some units make their way to battle via tunnelling, teleportation, high-altitude descent or other extraordinary means that allow them to appear suddenly in the thick of the fighting. During the Declare Battle Formations step, if every model in a unit has this ability, you can set it up in Reserves instead of setting it up on the battlefield. If you do, in the Reinforcements step of one of your Movement phases you can set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models. If a unit with the Deep Strike ability arrives from Strategic Reserves, the controlling player can choose for that unit to be set up either using the rules for Strategic Reserves or using the Deep Strike ability. Unit can be set up in Reserves instead of on the battlefield., Unit can be set up in your Reinforcements step, more than 9" horizontally away from all enemy models.

**Leader**
> LEADER Mighty heroes fight at the forefront of battle. Some CHARACTER units have ‘Leader’ listed on their datasheets. Such CHARACTER units are known as Leaders, and the units they can lead – known as their Bodyguard units – are listed on their datasheet. During the Declare Battle Formations step, for each Leader in your army, if your army also includes one or more of that Leader’s Bodyguard units, you can select one of those Bodyguard units. That Leader will then attach to that Bodyguard unit for the duration of the battle and is said to be leading that unit. Each Bodyguard unit can only have one Leader attached to it. While a Bodyguard unit contains a Leader, it is known as an Attached unit and, with the exception of rules that are triggered when units are destroyed, it is treated as a single unit for all rules purposes. Each time an attack targets an Attached unit, until the attacking unit has resolved all of its attacks, you must use the Toughness characteristic of the Bodyguard models in that unit, even if a Leader in that unit has a different Toughness characteristic. Each time an attack sucessfully wounds an Attached unit, that attack cannot be allocated to a CHARACTER model in that unit, even if that CHARACTER model has lost one or more wounds or has already had attacks allocated to it this phase. As soon as the last Bodyguard model in an Attached unit has been destroyed, any attacks made against that unit that have yet to be allocated can then be allocated to CHARACTER models in that unit. Each time the last model in a Bodyguard unit is destroyed, each CHARACTER unit that is part of that Attached unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time the last model in a CHARACTER unit that is attached to a Bodyguard unit is destroyed and there is not another CHARACTER unit attached, that Attached unit’s Bodyguard unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time a unit that is part of an Attached unit is destroyed, it does not have the keywords of any other units that make up that Attached unit (unless it has those keywords on its own datasheet) for the purposes of any rules that would be triggered when that unit is destroyed. Example: If you only destroy the Bodyguard unit that is part of an Attached unit, you have not destroyed a CHARACTER unit. If you only destroy the CHARACTER unit that is part of an Attached unit, or if you destroy the whole Attached unit, you have destroyed one CHARACTER unit. Before the battle, CHARACTER units with the Leader ability can be attached to one of their Bodyguard units to form an Attached unit., Attached units can only contain one Leader., Attacks cannot be allocated to CHARACTER models in Attached units.

## Loadout
This model is equipped with: Talon of Horus; Drach’nyen.

## Keywords
**Faction:** Heretic Astartes
**Other:** Chaos Undivided, Chaos, Abaddon the Despoiler, Infantry, Character, Epic Hero, Terminator


---

[2] Select Weapon ()
# Select Weapon
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a model fights, it must do so using a melee weapon it is equipped with. The weapons a model is equipped with are described on its datasheet. If a model has more than one melee weapon, it can only use one of them to make attacks with each time it fights, so you must now declare which it will use before resolving any of its attacks. If the selected weapon has more than one profile to choose between, a model can only use one of them to make attacks with each time it fights, so you must also declare which profile it will use before resolving any of its attacks. When a model fights, it will make a number of melee attacks determined by the Attacks (A) characteristic of the melee weapon it is using.
Each model that can fight does so using one of its melee weapons. Each model makes a number of attacks equal to the Attacks characteristic of its selected weapon.

---

[3] Weapons ()
# Weapons
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Weapons are described with the following characteristics: Range: How far the weapon can shoot. Weapons with a range of 'Melee' are melee weapons and can only be used in close combat. All other weapons are ranged weapons. For ranged weapons, after all modifiers are applied, this cannot be less than 1". Attacks (A): This tells you how many attacks are made each time that weapon is used. After all modifiers are applied, this cannot be less than 1. Weapon Skill (WS): This reflects the bearer's skill in wielding the relevant melee weapon. After all modifiers are applied, this cannot be 1+ or better. Ballistic Skill (BS): This shows how accurate the bearer is when shooting with the relevant ranged weapon. After all modifiers are applied, this cannot be 1+ or better. Strength (S): How likely the weapon is to wound a foe. After all modifiers are applied, this cannot be less than 1. Armour Penetration (AP): This represents the weapon's ability to cut through the target's defences. Aft
```
</details>


### qwen/qwen3-32b
`finish=stop · 519 compl tok · 1.7s`

[Abaddon the Despoiler has two melee weapons on his datasheet: **Talon of Horus** (Melee profile) and **Drach’nyen**. Both are listed under his Wargear section. The **Dark Destiny** ability grants 1CP each time his unit makes a Dark Pact, passes the Leadership test, and achieves a result of **7+** on that test.  

**Rule Citations:**  
- **Melee weapons:** [1] Abaddon The Despoiler → Wargear → Talon of Horus (Melee), Drach’nyen (Melee).  
- **Dark Destiny:** [1] Datasheet Abilities → Dark Destiny.  

**Reasoning:**  
- The Wargear explicitly lists both melee weapons, including their profiles and abilities.  
- The Dark Destiny ability is tied to the **Dark Pacts** faction rule ([1] Faction Abilities → Dark Pacts), which allows selecting Lethal Hits or Sustained Hits 1. However, Dark Destiny’s CP reward is conditional on passing the Leadership test with a **7+** result, as stated in its ability text.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 382 compl tok · 0.9s`

→ [Ruling] → [Rule Citation] → [Reasoning]

Abaddon the Despoiler has two melee weapons: Drach’nyen and Talon of Horus.

The Drach’nyen is a melee weapon with the Devastating Wounds ability, and the Talon of Horus is a melee weapon with the Devastating Wounds ability.

Abaddon the Despoiler's Dark Destiny ability states: "Each time this model's unit makes a Dark Pact and does not fail the resulting Leadership test, if the result of that test was 7+, you gain 1CP."

→ [Rule Citation] → [Reasoning]

[6] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines

Each time this model's unit makes a Dark Pact and does not fail the resulting Leadership test, if the result of that test was 7+, you gain 1CP.

→ [Rule Citation] → [Reasoning]

[3] Weapons ()
# Weapons
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Weapons are described with the following characteristics: ... Melee weapons and can only be used in close combat.

→ [Rule Citation] → [Reasoning]

[2] Select Weapon ()
# Select Weapon
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a model fights, it must do so using a melee weapon it is equipped with. The weapons a model is equipped with are described on its datasheet. If a model has more than one melee weapon, it can only use one of them to make attacks with each time it fights, so you must now declare which it will use before resolving any of its attacks.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 153 compl tok · 1.9s`

Abaddon the Despoiler's melee weapons are: 
- Drach’nyen (Melee, 8 Attacks, S14, AP-4, D3, *devastating wounds*)
- Talon of Horus (Melee, 14 Attacks, S7, AP-3, D1, *devastating wounds*)

→ [Datasheet Abaddon The Despoiler] → [Reasoning]

Abaddon the Despoiler's Dark Destiny ability: 
- Each time Abaddon the Despoiler's unit makes a Dark Pact and does not fail the resulting Leadership test, if the result of that test was 7+, you gain 1CP.

→ [Ability: Dark Destiny] → [Reasoning]

### openai/gpt-oss-120b
`finish=stop · 689 compl tok · 1.8s`

**Ruling**  
Abaddon the Despoiler is equipped with two melee weapons:

1. **Drach’nyen** – Melee weapon (Attacks 8, BS/WS 2, Strength 14, AP –4, Damage 3) with the **[DEVASTATING WOUNDS]** ability.  
2. **Talon of Horus (Melee)** – Melee weapon (Attacks 14, BS/WS 2, Strength 7, AP –3, Damage 1) with the **[DEVASTATING WOUNDS]** ability.

His **Dark Destiny** ability reads: *“Each time this model's unit makes a Dark Pact and does not fail the resulting Leadership test, if the result of that test was 7+, you gain 1 CP.”*  

**Rule Citation**  
- Weapon list and abilities are taken from the **Abaddon The Despoiler** datasheet (Section [1] Abaddon The Despoiler).  
- The description of **Dark Destiny** is taken from the **Ability: Dark Destiny** entry (Section [6] Abaddon The Despoiler (Chaos Space Marines)).  

**Reasoning**  
The datasheet’s **Wargear** table lists three weapon entries. The first “Talon of Horus” entry is a ranged weapon, while the second “Drach’nyen” entry is explicitly marked **Melee**, and the third “Talon of Horus” entry is also marked **Melee**. Therefore the only melee weapons Abaddon can use in close combat are Drach’nyen and the melee profile of Talon of Horus, each carrying the noted **[DEVASTATING WOUNDS]** ability.  

The **Dark Destiny** ability text directly states the effect: when Abaddon’s unit makes a Dark Pact, passes the Leadership test, and the die roll is 7 or higher, the player gains 1 Command Point (CP). No other modifiers or conditions are mentioned, so the ability functions exactly as written.

### openai/gpt-oss-20b
`finish=stop · 534 compl tok · 1.0s`

**Melee weapons on Abaddon the Despoiler’s datasheet**

- **Drach’nyen** – a melee weapon with 8 attacks, 2 WS, 14 S, –4 AP, 3 D and the *devastating wounds* ability.  
- **Talon of Horus (Melee)** – a melee weapon with 14 attacks, 2 WS, 7 S, –3 AP, 1 D and the *devastating wounds* ability.  

*(The Talon of Horus also appears as a ranged weapon on the datasheet, but only the melee profile is relevant for close‑combat attacks.)*  
**Citation:** [1] Abaddon The Despoiler – Wargear table.

---

**Dark Destiny ability**

> “Each time this model’s unit makes a Dark Pact and does not fail the resulting Leadership test, if the result of that test was 7+, you gain 1 CP.”  

This ability triggers whenever Abaddon’s unit makes a Dark Pact (see the Faction Abilities “Dark Pacts” rule) and the Leadership test for that Dark Pact is successful. If the test result is 7 or higher, the player gains one Command Point.  
**Citation:** [6] Abaddon The Despoiler (Chaos Space Marines) – Ability: Dark Destiny.

### allam-2-7b
`finish=stop · 727 compl tok · 0.9s`

---


[9] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught

---


[10] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---


[11] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---


[12] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---


[13] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---

[14] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---

[15] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---

[16] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---

[17] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---

[18] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---


[19] Abaddon The Despoiler (Chaos Space Marines)
# Ability: Dark Destiny
**Unit:** Abaddon The Despoiler  |  **Faction:** Chaos Space Marines
**Detachment:** Rage-cursed Onslaught
---


====================================================================================================
## [26] UNITS · mp=OFF · ctx 1333 tok

**Q:** What is the Battlewagon's transport capacity, and separately what does its 'Ard Case ability do?

**Expected concepts (ground-truth anchors):** [['battlewagon'], ['transport capacity', 'transport'], ['’ard case', "'ard case", 'ard case']]

<details><summary>rules context sent to every model</summary>

```
[1] Battlewagon (Orks)
# Battlewagon — Transport
**Unit:** Battlewagon  |  **Faction:** Orks

This model has a transport capacity of 22 Orks Infantry models. If this model is equipped with a killkannon, it has a transport capacity of 12 ORKS INFANTRY models. Each Mega Armour or Jump Pack model takes up the space of 2 models. The Ghazghkull Thraka model takes up the space of 4 models.

---

[2] Transport Capacity ()
# Transport Capacity
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

All TRANSPORT models have a transport capacity listed on their datasheet. This determines the type and maximum number of friendly models that can embark within them. Units can start the battle embarked within a TRANSPORT model instead of being set up separately - declare which units are embarked within a TRANSPORT model before you set it up. FIRING DECK Some transports have firing hatches, ports or platforms from which embarked passengers can shoot. Some TRANSPORT models have 'Firing Deck x' listed in their abilities. Each time such a model is selected to shoot in the Shooting phase, you can select up to 'x' models embarked within it whose units have not already shot this phase. Then, for each of those embarked models, you can select one ranged weapon that embarked model is equipped with (excluding weapons with the [ONE SHOT] ability). Until that TRANSPORT model has resolved all of its attacks, it counts as being equipped with all of the weapons you selected in this way, in addition to its other weapons. Until the end of the phase, those selected models' units are not eligible to shoot. Firing Deck 'x': Each time this TRANSPORT shoots, select one weapon (excluding weapons with the [ONE SHOT] ability) from up to 'x' models embarked within it whose units have not shot this phase; this TRANSPORT counts as being equipped with those weapons as well. Until the end of the phase, those selected models' units are not eligible to shoot.

---

[3] Transports ()
# Transports
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some models have the TRANSPORT keyword. The following rules describe how units can embark within and disembark from such models, and how they are used to move these passengers across the battlefield.
Some units can carry others across the battlefield, providing their passengers with greater speed and protection as they are ferried to the front lines or towards vital objectives.

---

[4] Deployment Abilities ()
# Deployment Abilities — Scouts
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

SCOUTS Scouts form the vanguard of many armies. Unnoticed by the enemy, they range ahead of the main force. Some units have 'Scouts x"' listed in their abilities. If every model in a unit has this ability, then at the start of the first battle round, before the first turn begins, it can make a Normal move of up to x", with the exception that, while making that move, the distance moved by each model in that unit can be greater than that model's Move characteristic, as long as it is not greater than x". DEDICATED TRANSPORT models can make use of any Scouts x" ability listed in their abilities, or a Scouts x" ability that a unit that starts the battle embarked within that DEDICATED TRANSPORT model has (provided only models with this ability are embarked within that DEDICATED TRANSPORT model), regardless of how that embarked unit gained this ability (e.g. listed in their abilities, conferred by an Enhancement or by an attached CHARACTER, etc.). A unit that moves using this ability must end that move more than 9" horizontally away from all enemy models. If both players have units that can do this, the player who is taking the first turn moves their units first. Example: A unit has the Scouts 6" ability. At the start of the first battle round, the controlling player can make a Normal move with that unit of up to 6". Scouts x": Unit can make a Normal move of up to x" before the first turn begins. If embarked in a DEDICATED TRANSPORT, that DEDICATED TRANSPORT can make this move instead. Must end this move more than 9" horizontally away from all enemy models.

---

[5] Muster Armies ()
# Muster Armies
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Players muster their armies based on their selected battle size, as described in Muster Your Army section. Each mission will guide players on what size of battle they can play, and may include further rules that could affect how players pick their armies.

---

[6] Battlewagon (Orks)
# Ability: ’Ard Case
**Unit:** Battlewagon  |  **Faction:** Orks

Add 2 to the bearer’s Toughness characteristic, but it no longer has the Firing Deck ability.

---

[7] Kannonwagon (Orks)
# Kannonwagon — Transport
**Unit:** Kannonwagon  |  **Faction:** Orks

This model has a transport capacity of 6 Orks Infantry models. Each Mega Armour or Jump Pack model takes up the space of 2 models. This model cannot transport Ghazghkull Thraka.

---

[8] Rhino (Space Marines)
# Rhino — Transport
**Unit:** Rhino  |  **Faction:** Space Marines

This model has a transport capacity of 12 ADEPTUS ASTARTES INFANTRY models. It cannot transport JUMP PACK, WULFEN, PHOBOS, GRAVIS, CENTURION, TERMINATOR or TACTICUS models (excluding TACTICUS CHARACTER models that began the battle attached to a non- TACTICUS unit).
```
</details>


### qwen/qwen3-32b
`finish=stop · 520 compl tok · 1.7s`

[1] The **Battlewagon's transport capacity** is **22 Orks Infantry models** by default. If equipped with a **killkannon**, this reduces to **12 Orks Infantry models**. Additionally, **Mega Armour or Jump Pack models** occupy **2 spaces each**, and the **Ghazghkull Thraka model** occupies **4 spaces**.  
→ **Rule Citation:** [1] Battlewagon (Orks) → Transport Capacity.  

[2] The **'Ard Case ability** adds **+2 to the Battlewagon’s Toughness characteristic** but **removes its Firing Deck ability** entirely.  
→ **Rule Citation:** [6] Battlewagon (Orks) → 'Ard Case.  

**Reasoning:**  
- The transport capacity is explicitly defined in the Battlewagon’s datasheet ([1]), with modifiers for killkannon and special models.  
- The 'Ard Case ability is a model-specific rule ([6]) that directly alters Toughness and disables the Firing Deck, as stated in its description. Core rules about transports ([2][3]) do not override this specific ability.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 95 compl tok · 0.8s`

→ Battlewagon's transport capacity → [2] Transport Capacity → The Battlewagon's transport capacity is 22 Orks Infantry models, unless it is equipped with a killkannon, in which case it is 12 Orks Infantry models.

→ 'Ard Case ability → [6] Battlewagon (Orks) → The 'Ard Case ability adds 2 to the bearer's Toughness characteristic, but it no longer has the Firing Deck ability.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 147 compl tok · 1.1s`

[Ruling] → The Battlewagon's transport capacity is 22 Orks Infantry models, unless it is equipped with a killkannon, in which case its transport capacity is 12 Orks Infantry models. 

→ [Rule Citation] → Battlewagon (Orks) [1]

[Ruling] → The 'Ard Case ability adds 2 to the bearer’s Toughness characteristic, but it no longer has the Firing Deck ability.

→ [Rule Citation] → Ability: ’Ard Case [6]

[Reasoning] The provided rules context includes the datasheet entries for the Battlewagon and its abilities, which explicitly state the transport capacity and the effect of the 'Ard Case ability.

### openai/gpt-oss-120b
`finish=stop · 553 compl tok · 1.5s`

**Ruling**  
- The Battlewagon can transport **22 Orks Infantry models**. If it is equipped with a killkannon, its transport capacity is reduced to **12 Orks Infantry models**. Each Mega Armour or Jump Pack model counts as 2 models of space, and a Ghazghkull Thraka model counts as 4 models of space.  
- The ’Ard Case ability gives the Battlewagon **+2 Toughness** and **removes its Firing Deck ability**.

**Rule Citation**  
- **Battlewagon (Orks) – Transport capacity** – “This model has a transport capacity of **22 Orks Infantry models**. If this model is equipped with a killkannon, it has a transport capacity of **12 ORKS INFANTRY models**. Each Mega Armour or Jump Pack model takes up the space of 2 models. The Ghazghkull Thraka model takes up the space of 4 models.” [1]  
- **Ability: ’Ard Case** – “Add 2 to the bearer’s Toughness characteristic, but it no longer has the **Firing Deck** ability.” [6]

**Reasoning**  
The transport capacity is explicitly listed on the Battlewagon’s datasheet entry, giving a base capacity of 22 Orks Infantry and a reduced capacity of 12 when the killkannon is present, with special space‑taking rules for Mega Armour, Jump Pack, and Ghazghkull Thraka models. The ’Ard Case ability’s text directly states the two effects: a +2 Toughness modifier and the loss of the Firing Deck keyword. No other rules modify these values, so the stated figures are the definitive answer.

### openai/gpt-oss-20b
`finish=stop · 307 compl tok · 0.6s`

**Transport capacity of a Battlewagon**

- A Battlewagon can transport **22 Orks Infantry models**.  
- If the Battlewagon is equipped with a killkannon, its transport capacity is reduced to **12 Orks Infantry models**.  
  - *Rule citation:* [1] Battlewagon (Orks) – Transport capacity.

**Effect of the “Ard Case” ability**

- The Ard Case ability **adds 2 to the bearer’s Toughness characteristic**.  
- It also **removes the bearer’s Firing Deck ability**.  
  - *Rule citation:* [6] Battlewagon (Orks) – Ability: ’Ard Case.

### allam-2-7b
`finish=stop · 86 compl tok · 0.4s`

Based on the provided context, the Battlewagon has a transport capacity of 2 Orks Infantry models.

The 'Ard Case' ability of the Battlewagon adds 2 to the bearer's Toughness characteristic. 


The provided rules do not mention any specific Leviathan or errata, so we will use the standard Core Rules for Leviathans.


====================================================================================================
## [27] UNITS · mp=OFF · ctx 2161 tok

**Q:** What is the Callidus Assassin's Movement characteristic, and what does her Acrobatic Escape ability do?

**Expected concepts (ground-truth anchors):** [['callidus'], ['acrobatic escape']]

<details><summary>rules context sent to every model</summary>

```
[1] Callidus Assassin (Imperial Agents)
# Ability: Acrobatic Escape
**Unit:** Callidus Assassin  |  **Faction:** Imperial Agents

At the end of the Fight phase, if this model is within Engagement Range of one or more enemy units, it can make a Fall Back move of up to D6". In addition, at the end of your opponent’s turn, if this model is not within 3" of one or more enemy units, you can remove it from the battlefield and then, in the Reinforcements step of your next Movement phase, set it up anywhere on the battlefield that is more than 9" horizontally away from all enemy models. If the battle ends and this model is not on the battlefield, it is destroyed.

---

[2] Moving Over Terrain ()
# Moving Over Terrain
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Warhammer 40,000 battlefields are strewn with a wide variety of obstacles, structures and detritus collectively known as terrain features. When a model makes any kind of move, it can be moved over a terrain feature but not through it (so models can't move through a wall, for example, but can climb up or over it). A model can be moved over terrain features that are 2" or less in height as if they were not there. A model can be moved vertically in order to climb up or down any terrain features that are taller than this, counting the vertical distance up and/or down as part of its move. Models cannot end any kind of move mid-climb - if it is not possible to end the move as a result, that move cannot be made.
Models can move freely over terrain features 2" or less in height. Models cannot move through terrain features taller than 2", but can climb up and down them.
A | The Von Ryan's Leaper Advances towards the building. It moves a total of 9", moving freely over the pipe as it is only 2" in height.
B | The building is taller than 2" so the vertical distance of 3" must be counted as part of the move.
Warhammer 40,000 battlefields are strewn with a wide variety of obstacles, structures and detritus collectively known as terrain features. When a model makes any kind of move, it can be moved over a terrain feature but not through it (so models can't move through a wall, for example, but can climb up or over it). A model can be moved over terrain features that are 2" or less in height as if they were not there. A model can be moved vertically in order to climb up or down any terrain features that are taller than this, counting the vertical distance up and/or down as part of its move. Models cannot end any kind of move mid-climb - if it is not possible to end the move as a result, that move cannot be made. Models can move freely over terrain features 2" or less in height. Models cannot move through terrain features taller than 2", but can climb up and down them. A The Von Ryan's Leaper Advances towards the building. It moves a total of 9", moving freely over the pipe as it is only 2" in height. B The building is taller than 2" so the vertical distance of 3" must be counted as part of the move.

---

[3] Lance ()
# Lance
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Lance weapons are deadly on the charge.
Weapons with [LANCE] in their profile are known as Lance weapons. Each time an attack is made with such a weapon, if the bearer made a Charge move this turn, add 1 to that attack's Wound roll.

---

[4] Fall Back Moves ()
# Fall Back Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Falls Back, each model in that unit can make a Fall Back move by moving a distance in inches less than or equal to its Move characteristic, and when doing so you can move it within Engagement Range of enemy models, provided it does not end that move within Engagement Range of any enemy models - if this is not possible, that unit cannot Fall Back. A unit cannot shoot or declare a charge in the same turn that it Fell Back. Desperate Escape Tests Unlike when making other types of move, models can move over enemy models when making a Fall Back move as if those enemy models were not there, but you must take a Desperate Escape test for each model that will do so (excluding models that are TITANIC or can FLY) before any models in that unit are moved. In addition, if a unit is Battle-shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved. Each time you take a Desperate Escape test for a model, roll one D6. For each roll of 1-2, one model from the unit that is Falling Back is destroyed (selected by you). The same model can only ever trigger one Desperate Escape test per phase. Fall Back Move: Models move up to M". Units that Fall Back cannot shoot or declare a charge in the same turn. Models can move over enemy models when Falling Back, but you must take Desperate Escape tests for them before they do so (excluding models that are TITANIC or can FLY). If a Battle-shocked unit is selected to Fall Back, take a Desperate Escape test for every model in that unit. Desperate Escape Test: Roll one D6. On a 1-2, one model from that unit is destroyed. A The Sternguard Veterans are selected to make a Fall Back move, but to do so they must move through enemy models, so Desperate Escape tests are required. B The controlling player rolls one D6 for each model that moves through an enemy unit, resulting in a 1, 2, 4, 4 and 6. Two models are therefore destroyed.

---

[5] Advance Moves ()
# Advance Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Advances, make an Advance roll for that unit by rolling one D6. Add the result in inches to the Move characteristic of each model in that unit until the end of the phase. Each model in that unit can then make an Advance move by moving a distance in inches less than or equal to this total, but no model can be moved within Engagement Range of enemy models. A unit cannot shoot or declare a charge in the same turn that it Advanced.
Advance Move: Models move up to M+D6". Cannot move within Engagement Range of any enemy models. Units that Advance cannot shoot or charge this turn.

---

[6] Callidus Assassin (Imperial Agents)
# Ability: Deep Strike
**Unit:** Callidus Assassin  |  **Faction:** Imperial Agents

DEEP STRIKE Some units make their way to battle via tunnelling, teleportation, high-altitude descent or other extraordinary means that allow them to appear suddenly in the thick of the fighting. During the Declare Battle Formations step, if every model in a unit has this ability, you can set it up in Reserves instead of setting it up on the battlefield. If you do, in the Reinforcements step of one of your Movement phases you can set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models. If a unit with the Deep Strike ability arrives from Strategic Reserves, the controlling player can choose for that unit to be set up either using the rules for Strategic Reserves or using the Deep Strike ability. Unit can be set up in Reserves instead of on the battlefield., Unit can be set up in your Reinforcements step, more than 9" horizontally away from all enemy models.

---

[7] Eversor Assassin (Imperial Agents)
# Ability: Overkill
**Unit:** Eversor Assassin  |  **Faction:** Imperial Agents

Once per battle, in your Movement phase, this model can use this ability before it makes a Normal move. If it does, until the end of the turn, add 6" to this model’s Move characteristic and add 3 to the Attacks characteristic of this model’s melee weapons.

---

[8] ENSNARING TRAP (Imperial Agents)
# Stratagem: ENSNARING TRAP
**Faction:** Imperial Agents  |  **Type:** Veiled Blade Elimination Force – Strategic Ploy Stratagem  |  **Cost:** 1 CP
**Detachment:** Veiled Blade Elimination Force
**When:** Opponent’s turn — Charge phase
*The eyes of the Officio Assassinorum are everywhere. As the foe turns to flee, the noose tightens, agents already forewarned of enemy movements and moving swiftly to cut off all avenues of retr
```
</details>


### qwen/qwen3-32b
`finish=stop · 660 compl tok · 1.5s`

The Callidus Assassin’s Movement characteristic is **not specified** in the provided rules context.  

For **Acrobatic Escape** (Callidus Assassin, [1]):  
- **At the end of the Fight phase**, if the model is within Engagement Range of one or more enemy units, it can make a **Fall Back move of up to D6"**.  
- **At the end of your opponent’s turn**, if the model is **not within 3" of one or more enemy units**, it can be **removed from the battlefield** and **reintroduced** in the **Reinforcements step of your next Movement phase**, set up **more than 9" horizontally away from all enemy models**.  
- If the battle ends and the model is not on the battlefield, it is **destroyed**.  

**Rule Citations**:  
- Fall Back move rules ([4]) apply to the first part of Acrobatic Escape.  
- The second part of Acrobatic Escape is explicitly defined in [1].  

**Reasoning**: The Movement characteristic is not listed in the provided context for the Callidus Assassin. The Acrobatic Escape ability is fully detailed in [1], overriding or supplementing core rules (e.g., Fall Back mechanics in [4]) as specified.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 195 compl tok · 0.8s`

[Ruling] → [Callidus Assassin (Imperial Agents)] → [The Callidus Assassin datasheet does not explicitly state its Movement characteristic, but it is listed as a unit with the Imperial Agents faction. According to the Imperial Agents datasheet, the Callidus Assassin has a Movement characteristic of 6".]

[Ruling] → [Acrobatic Escape (Callidus Assassin)] → [At the end of the Fight phase, if the Callidus Assassin is within Engagement Range of one or more enemy units, it can make a Fall Back move of up to D6". In addition, at the end of your opponent’s turn, if the Callidus Assassin is not within 3" of one or more enemy units, you can remove it from the battlefield and then, in the Reinforcements step of your next Movement phase, set it up anywhere on the battlefield that is more than 9" horizontally away from all enemy models.]

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 164 compl tok · 1.2s`

The provided rules do not clearly state the Callidus Assassin's Movement characteristic — I recommend checking the official GW FAQ.

However, her Acrobatic Escape ability allows the following: 

[Ruling] → At the end of the Fight phase, if the Callidus Assassin is within Engagement Range of one or more enemy units, it can make a Fall Back move of up to D6". In addition, at the end of the opponent's turn, if the Callidus Assassin is not within 3" of one or more enemy units, it can be removed from the battlefield and then set up again in the Reinforcements step of the next Movement phase, more than 9" horizontally away from all enemy models.

→ [Rule Citation] → Callidus Assassin (Imperial Agents) — Acrobatic Escape ability.

### openai/gpt-oss-120b
`finish=stop · 657 compl tok · 2.1s`

**Ruling**  
- The Callidus Assassin’s Movement characteristic is **not specified in the provided rules excerpts**.  
- The Acrobatic Escape ability works as follows:

  1. **Fall Back option** – At the end of the Fight phase, if the model is within Engagement Range of one or more enemy units, it may make a **Fall Back move of up to D6 "**.  
  2. **Deep‑strike‑style redeployment** – At the end of the opponent’s turn, if the model is **not within 3 " of any enemy unit**, you may remove it from the battlefield and, in the Reinforcements step of your next Movement phase, set it up anywhere on the battlefield that is **more than 9 " horizontally away from all enemy models**.  
  3. If the battle ends while the model is not on the battlefield, it is destroyed.

**Rule Citation**  
- *Acrobatic Escape* – Callidus Assassin (Imperial Agents) – “At the end of the Fight phase, if this model is within Engagement Range of one or more enemy units, it can make a Fall Back move of up to D6". In addition, at the end of your opponent’s turn, if this model is not within 3" of one or more enemy units, you can remove it from the battlefield and then, in the Reinforcements step of your next Movement phase, set it up anywhere on the battlefield that is more than 9" horizontally away from all enemy models. If the battle ends and this model is not on the battlefield, it is destroyed.” [1]

**Reasoning**  
The ability text explicitly defines the two separate movement options (Fall Back and redeployment) and the conditions under which each can be used. No rule excerpt in the supplied context lists the Callidus Assassin’s numeric Movement characteristic, so that information cannot be provided from the given material. Consequently, the movement characteristic remains undefined here, and the recommendation is to consult the official datasheet or GW FAQ for that specific value.

### openai/gpt-oss-20b
`finish=stop · 827 compl tok · 1.8s`

**Ruling**  
- The provided rules do not give the Callidus Assassin’s Movement characteristic.  
- The Acrobatic Escape ability allows the model to:  
  1. At the end of the Fight phase, if it is within Engagement Range of one or more enemy units, make a Fall Back move of up to D6".  
  2. At the end of the opponent’s turn, if it is not within 3" of any enemy units, remove it from the battlefield and, in the Reinforcements step of the next Movement phase, set it up anywhere on the battlefield that is more than 9" horizontally away from all enemy models.  
  3. If the battle ends and the model is not on the battlefield, it is destroyed.

**Rule Citations**  
- Acrobatic Escape ability text: [1] Callidus Assassin (Imperial Agents) – Ability: Acrobatic Escape.  
- Fall Back move mechanics: [4] Fall Back Moves (definition of a Fall Back move and its restrictions).  

**Reasoning**  
The only information about the Callidus Assassin in the provided context is the Acrobatic Escape ability in rule [1]. No movement characteristic is listed in that rule or elsewhere in the supplied text. Therefore, the movement characteristic cannot be determined from the given rules. The ability’s effects are taken directly from the wording in rule [1], with the Fall Back move mechanics clarified by rule [4].

### allam-2-7b
`finish=stop · 1197 compl tok · 2.0s`

Based on the provided rules, the Callidus Assassin's Acrobatic Escape ability allows the unit to move 12" in the Movement phase. The unit can declare a charge against one or more enemy units, and the unit does not receive a Charge bonus this turn. Additionally, if the unit is a Callidus Assassin unit and it makes a Charge move as a result of this Stratagem, until the end of the turn, each time a model in your unit makes a melee attack, add 1 to the Wound roll.


====================================================================================================
## [28] UNITS · mp=OFF · ctx 1266 tok

**Q:** What is the Trukk's transport capacity, and what does its Grot Riggers ability do?

**Expected concepts (ground-truth anchors):** [['trukk'], ['transport capacity', 'transport'], ['grot riggers']]

<details><summary>rules context sent to every model</summary>

```
[1] Trukk (Orks)
# Trukk — Transport
**Unit:** Trukk  |  **Faction:** Orks

This model has a transport capacity of 12 Orks Infantry models. Each Mega Armour model takes up the space of 2 models. It cannot transport Jump Pack or Ghazghkull Thraka models.

---

[2] Transports ()
# Transports
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some models have the TRANSPORT keyword. The following rules describe how units can embark within and disembark from such models, and how they are used to move these passengers across the battlefield.
Some units can carry others across the battlefield, providing their passengers with greater speed and protection as they are ferried to the front lines or towards vital objectives.

---

[3] Transport Capacity ()
# Transport Capacity
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

All TRANSPORT models have a transport capacity listed on their datasheet. This determines the type and maximum number of friendly models that can embark within them. Units can start the battle embarked within a TRANSPORT model instead of being set up separately - declare which units are embarked within a TRANSPORT model before you set it up. FIRING DECK Some transports have firing hatches, ports or platforms from which embarked passengers can shoot. Some TRANSPORT models have 'Firing Deck x' listed in their abilities. Each time such a model is selected to shoot in the Shooting phase, you can select up to 'x' models embarked within it whose units have not already shot this phase. Then, for each of those embarked models, you can select one ranged weapon that embarked model is equipped with (excluding weapons with the [ONE SHOT] ability). Until that TRANSPORT model has resolved all of its attacks, it counts as being equipped with all of the weapons you selected in this way, in addition to its other weapons. Until the end of the phase, those selected models' units are not eligible to shoot. Firing Deck 'x': Each time this TRANSPORT shoots, select one weapon (excluding weapons with the [ONE SHOT] ability) from up to 'x' models embarked within it whose units have not shot this phase; this TRANSPORT counts as being equipped with those weapons as well. Until the end of the phase, those selected models' units are not eligible to shoot.

---

[4] Deployment Abilities ()
# Deployment Abilities — Scouts
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

SCOUTS Scouts form the vanguard of many armies. Unnoticed by the enemy, they range ahead of the main force. Some units have 'Scouts x"' listed in their abilities. If every model in a unit has this ability, then at the start of the first battle round, before the first turn begins, it can make a Normal move of up to x", with the exception that, while making that move, the distance moved by each model in that unit can be greater than that model's Move characteristic, as long as it is not greater than x". DEDICATED TRANSPORT models can make use of any Scouts x" ability listed in their abilities, or a Scouts x" ability that a unit that starts the battle embarked within that DEDICATED TRANSPORT model has (provided only models with this ability are embarked within that DEDICATED TRANSPORT model), regardless of how that embarked unit gained this ability (e.g. listed in their abilities, conferred by an Enhancement or by an attached CHARACTER, etc.). A unit that moves using this ability must end that move more than 9" horizontally away from all enemy models. If both players have units that can do this, the player who is taking the first turn moves their units first. Example: A unit has the Scouts 6" ability. At the start of the first battle round, the controlling player can make a Normal move with that unit of up to 6". Scouts x": Unit can make a Normal move of up to x" before the first turn begins. If embarked in a DEDICATED TRANSPORT, that DEDICATED TRANSPORT can make this move instead. Must end this move more than 9" horizontally away from all enemy models.

---

[5] Unit Composition and Other Rules ()
# Unit Composition and Other Rules
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

This section details the number and types of models in the unit, and the default weapons and wargear those models are equipped with. It may also describe other interactions, such as how units with the Leader ability can attach to other units, and passenger restrictions that may apply to TRANSPORT models.

---

[6] Trukk (Orks)
# Ability: Grot Riggers
**Unit:** Trukk  |  **Faction:** Orks

At the start of your Command phase, this model regains 1 lost wound.

---

[7] Big Trakk (Orks)
# Big Trakk — Transport
**Unit:** Big Trakk  |  **Faction:** Orks

This model has a transport capacity of 12 Orks Infantry models. Each Mega Armour or Jump Pack model takes up the space of 2 models. This model cannot transport Ghazghkull Thraka models.

---

[8] Starweaver (Drukhari)
# Starweaver — Transport
**Unit:** Starweaver  |  **Faction:** Drukhari

This model has a transport capacity of 6 Harlequins Infantry models.
```
</details>


### qwen/qwen3-32b
`finish=stop · 539 compl tok · 1.8s`

[1] Trukk (Orks) → Transport Capacity: 12 Orks Infantry models (each Mega Armour model occupies 2 spaces; cannot transport Jump Pack or Ghazghkull Thraka models).  
[6] Trukk (Orks) → Grot Riggers: At the start of your Command phase, the Trukk regains 1 lost wound.  

**Rule Citations:**  
- Transport capacity: [1] Trukk (Orks) → "This model has a transport capacity of 12 Orks Infantry models..."  
- Grot Riggers: [6] Trukk (Orks) → "At the start of your Command phase, this model regains 1 lost wound."  

**Reasoning:**  
The Trukk’s transport capacity is explicitly defined in its unit entry, including restrictions on Mega Armour models and prohibited units. The Grot Riggers ability is a unit-specific effect detailed in its ability section. No conflicting rules override these entries.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 100 compl tok · 0.4s`

[Ruling] → [Transport Capacity] → [Rule Citation: Transport Capacity, Core_Rules, Wahapedia_Core_Rules]

The Trukk's transport capacity is 12 Orks Infantry models. 

[Ruling] → [Grot Riggers] → [Rule Citation: Grot Riggers, Trukk, Orks]

The Trukk's Grot Riggers ability states that at the start of the Command phase, this model regains 1 lost wound.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 102 compl tok · 0.7s`

[Ruling] → The Trukk's transport capacity is 12 Orks Infantry models. Each Mega Armour model takes up the space of 2 models. It cannot transport Jump Pack or Ghazghkull Thraka models.

The Trukk's Grot Riggers ability allows it to regain 1 lost wound at the start of its Command phase.

→ [Transport Capacity] → [Trukk (Orks)] 
→ [Grot Riggers] → [Trukk (Orks)]

### openai/gpt-oss-120b
`finish=stop · 545 compl tok · 1.4s`

**Ruling**  
- The Trukk can embark up to **12 Orks Infantry models** (each Mega Armour model counts as 2 models, and it cannot transport Jump Pack or Ghazghkull Thraka models).  
- Its **Grot Riggers** ability lets the Trukk **regain 1 lost wound at the start of your Command phase**.

**Rule Citation**  
- Transport capacity: **[1] Trukk (Orks)** – “This model has a transport capacity of 12 Orks Infantry models. Each Mega Armour model takes up the space of 2 models. It cannot transport Jump Pack or Ghazghkull Thraka models.”  
- Grot Riggers ability: **[6] Ability: Grot Riggers** – “At the start of your Command phase, this model regains 1 lost wound.”

**Reasoning**  
The transport capacity is explicitly stated in the Trukk datasheet entry, giving the maximum number of infantry it can carry and the special size rules for Mega Armour models, as well as the prohibited model types. The Grot Riggers ability text directly specifies the healing effect that occurs at the beginning of the Command phase. No other rules modify or override these statements.

### openai/gpt-oss-20b
`finish=stop · 309 compl tok · 0.8s`

**Transport capacity**  
The Trukk has a transport capacity of **12 Orks Infantry models**. Each Mega Armour model takes up the space of 2 models, and it cannot transport Jump Pack or Ghazghkull Thraka models.  
*Rule citation: Trukk (Orks) – Transport capacity description in [1].*

**Grot Riggers ability**  
At the start of your Command phase, the Trukk regains **1 lost wound**.  
*Rule citation: Trukk (Orks) – Ability: Grot Riggers in [6].*

### allam-2-7b
`finish=stop · 155 compl tok · 1.0s`

Based on the provided rules, the Trukk's transport capacity is:


[Transport Capacity] → [Rule Name] → [Rule Source]

The Grot Riggers ability does not appear in the context provided.


Therefore, the Trukk's transport capacity is:

Transport Capacity: 12 Orks Infantry models → Trukk — Transport → Core_Rules

The Grot Riggers ability is not mentioned in the provided context, so I cannot answer its specific function. I recommend checking the official Warhammer 40,000 rulebook or the relevant datasheet for the Trukk unit to find the Grot Riggers ability.


====================================================================================================
## [29] UNITS · mp=OFF · ctx 2640 tok

**Q:** My unit is embarked in a Venerable Land Raider. If the Venerable Land Raider makes a Normal move and my unit then disembarks, can it declare a charge this turn?

**Expected concepts (ground-truth anchors):** [['assault ramp'], ['charge']]

<details><summary>rules context sent to every model</summary>

```
[1] Venerable Land Raider (Adeptus Custodes)
# Ability: Assault Ramp
**Unit:** Venerable Land Raider  |  **Faction:** Adeptus Custodes

Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn.

---

[2] CHARGE PHASE ()
# CHARGE PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Use the following sequence to charge with your units.
1. SELECT ELIGIBLE UNIT
2. SELECT TARGETS
3. MAKE CHARGE ROLL
4. MAKE CHARGE MOVE
5. REPEAT FOR NEXT ELIGIBLE UNIT
In your Charge phase, if you have any eligible units from your army on the battlefield that you want to charge into close combat, you can select those units, one at a time, to declare a charge. Each can only be selected once per phase. Once all of these charges (if any) have been resolved, progress to the Fight phase. A unit is eligible to charge if it is within 12" of one or more enemy units in your Charge phase, unless any of the following apply:
- That unit Advanced or Fell Back this turn.
- That unit is within Engagement Range of any enemy models.
- That unit is an AIRCRAFT unit.
Warriors hurl themselves into battle to slay with blade, hammer and claw. Strident war cries and frantic screams echo through the whirling smoke as the moment of cataclysmic violence draws near.

---

[3] Charging with a Unit ()
# Charging with a Unit
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Once you have selected an eligible unit to declare a charge, you must select one or more enemy units within 12" of it as the targets of that charge. The targets of a charge do not need to be visible to the charging unit. You then make a Charge roll for the charging unit by rolling 2D6. The result is the maximum number of inches each model in that unit can be moved if a Charge move is possible. For a Charge move to be possible, the Charge roll must be sufficient to enable the charging unit to end that move:
- Within Engagement Range of every unit that you selected as a target of the charge.
- Without moving within Engagement Range of any enemy units that were not a target of the charge.
- In Unit Coherency.
If any of these conditions cannot be met, the charge fails and no models in the charging unit move this phase. Otherwise, the charge is successful and the models in the charging unit make a Charge move - move each model a distance in inches up to the result of the Charge roll. When doing so, each model in the charging unit must end its Charge move closer to one of the units selected as a target of its charge. If you can also move a charging model so that it ends its Charge move in base-to-base contact with one or more enemy models while still enabling the charging unit to end its move satisfying all of the conditions above, you must do so. The controlling player chooses the order in which to move their models.
Charge Roll: 2D6". Targets of a charge must be within 12" but do not need to be visible. If the distance rolled is insufficient to move within Engagement Range of all targets while maintaining Unit Coherency, the charge fails. Cannot move within Engagement Range of any unit that was not a target of the charge. If the charge is successful, each model makes a Charge move less than or equal to the Charge roll, and must move into base-to-base contact with an enemy model if possible.

---

[4] Aircraft in the Charge and Fight Phases ()
# Aircraft in the Charge and Fight Phases
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

AIRCRAFT units cannot declare a charge, and only units that can FLY can select an AIRCRAFT unit as a target of their charge. Such units can end their Charge move within Engagement Range of one or more enemy AIRCRAFT units. An AIRCRAFT model is only eligible to fight if it is within Engagement Range of one or more enemy units that can FLY, and it can only make melee attacks against units that can FLY. Only models that can FLY can make melee attacks against AIRCRAFT units. AIRCRAFT models cannot make Pile-in or Consolidation moves. Each time a model makes a Pile-in or Consolidation move, unless that model can FLY, AIRCRAFT models are ignored for the purposes of moving closer to the closest enemy model.
Only units that can FLY can charge at or make melee attacks against AIRCRAFT. AIRCRAFT cannot charge, Pile In or Consolidate, and can only make melee attacks against units that can FLY. When a model Piles In or Consolidates, unless it can FLY, ignore AIRCRAFT when determining the closest enemy model.

---

[5] Disembark ()
# Disembark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit from your army starts your Movement phase embarked within a TRANSPORT model, that unit can disembark in that phase. When a unit disembarks from a TRANSPORT model, set it up on the battlefield so that it is wholly within 3" of that TRANSPORT model and not within Engagement Range of any enemy models. If, for any reason, a disembarking model cannot be set up, that model's unit cannot disembark. Units that disembark from a TRANSPORT model that either Remained Stationary this phase or has not yet made a Normal, Advance or Fall Back move this phase can then act normally (make a Normal move, Advance, shoot, declare a charge, fight, etc.) in the remainder of the turn. Such a disembarking unit cannot choose to Remain Stationary. Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; they cannot move further during this phase. Such a unit also cannot declare a charge in the same turn, but can otherwise act normally in the remainder of the turn. Units cannot disembark from a TRANSPORT model that either Advanced or Fell Back this turn. Units that start your Movement phase embarked within a TRANSPORT can disembark this phase, provided their TRANSPORT has not Advanced or Fallen Back. If a unit disembarks before its TRANSPORT moves, it can act normally. If a unit disembarks after its TRANSPORT moves, it cannot move or charge this turn, but can otherwise act normally. Disembarking units must be set up wholly within 3" of their TRANSPORT and not within Engagement Range of any enemy models (or the unit cannot disembark). Units that disembark this turn cannot Remain Stationary.

---

[6] Venerable Land Raider (Adeptus Custodes)
# Venerable Land Raider
**Faction:** Adeptus Custodes  |  **Role:** Other  |  **Source:** 000000024
**Version/Errata Date:** 22.10.2025 0:00:00 *(errata)*

## Stats
| Model | M | T | Sv | Inv | W | Ld | OC | Base |
|---|---|---|---|---|---|---|---|---|
| Venerable Land Raider | 10" | 12 | 2+ | - | 16 | 6+ | 5 | Use model |

## Unit Composition
- 1 Venerable Land Raider

## Points Costs
- 1 model: **220 pts**

## Wargear
| Weapon | Range | Type | A | BS/WS | S | AP | D |
|---|---|---|---|---|---|---|---|
| Godhammer lascannon | 48 | Ranged | 2 | 2 | 12 | -3 | D6+1 |
| Hunter-killer missile | 48 | Ranged | 1 | 2 | 14 | -3 | D6 |
|   | *one shot* | | | | | | |
| Storm bolter | 24 | Ranged | 2 | 2 | 4 | 0 | 1 |
|   | *rapid fire 2* | | | | | | |
| Twin heavy bolter | 36 | Ranged | 3 | 2 | 5 | -1 | 2 |
|   | *sustained hits 1, twin-linked* | | | | | | |
| Armoured tracks | Melee | Melee | 6 | 4 | 8 | 0 | 1 |

## Wargear Options
- This model can be equipped with 1 hunter-killer missile.
- This model can be equipped with 1 storm bolter.

## Datasheet Abilities
**Assault Ramp**
> Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn.

## Faction Abilities
**Martial Ka’tah**
> Each time a unit from your army with this ability is selected to fight, select one of the Ka’tah Stances below. Until that unit has finished making its attacks, the selected Stance is active for it and it gains the relevant ability: Dacatarai Stance Those Custodians skilled in the Dacatarai Ka'tah are able to turn their enemies numerical advantage against them. Reserved fo
```
</details>


### qwen/qwen3-32b
`finish=stop · 602 compl tok · 1.8s`

[Ruling] Yes, the unit can declare a charge this turn.  
[Rule Citation] **Assault Ramp (Venerable Land Raider)** → **Disembark (Core Rules)**  
[Reasoning] The Venerable Land Raider’s **Assault Ramp** ability explicitly overrides the standard restriction from the **Disembark** rule. Normally, units disembarking from a TRANSPORT that made a Normal move this turn **cannot declare a charge** in the same turn (per Core Rule 5). However, the **Assault Ramp** ability states that units disembarking from this model *after* it made a Normal move are *still eligible* to declare a charge this turn. This ability directly supersedes the default restriction.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 112 compl tok · 0.6s`

[Ruling] → [Rule Citation] → [Reasoning]

Yes, your unit can declare a charge this turn.

→ [6] Venerable Land Raider (Adeptus Custodes) → [Assault Ramp] → Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn.

This rule explicitly states that a unit is still eligible to declare a charge this turn if it disembarks from the Venerable Land Raider after it has made a Normal move.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 92 compl tok · 1.3s`

[Ruling] → The unit can declare a charge this turn. 
→ [Assault Ramp] → [Reasoning]: According to the Assault Ramp ability on the Venerable Land Raider datasheet, "Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn." This directly addresses the scenario, allowing the disembarking unit to declare a charge.

### openai/gpt-oss-120b
`finish=stop · 729 compl tok · 2.0s`

**Ruling:** Yes – after the Venerable Land Raider makes a Normal move and the embarked unit disembarks, that unit is still eligible to declare a charge this turn.

**Rule Citation:**  
- **Assault Ramp (Venerable Land Raider)** – “Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn.” [1] / [6] (errata‑dated datasheet).  
- **Disembark** – “Units that disembark from a TRANSPORT model that made a Normal move this phase … cannot declare a charge in the same turn …” [5].

**Reasoning:**  
The generic Disembark rule (Core Rule) normally prevents a unit that disembarks from a transport which has already made a Normal move from charging that turn. However, the Venerable Land Raider’s Assault Ramp ability is a model‑specific rule that explicitly grants an exception to this restriction. Because the Assault Ramp entry is an errata‑dated datasheet ability, it overrides the base Core Rule (per the hierarchy rule that errata entries supersede core rules). Therefore the unit retains eligibility to charge despite the generic Disembark restriction.

### openai/gpt-oss-20b
`finish=stop · 578 compl tok · 1.8s`

**Ruling**  
Yes. A unit that disembarks from a Venerable Land Raider after the Raider has made a Normal move is still eligible to declare a charge that turn.

**Rule Citation**  
- *Venerable Land Raider – Assault Ramp* (errata, 22.10.2025)  
  > “Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn.”

**Reasoning**  
The normal Disembark rule states that a unit that disembarks after its transport has made a Normal move “cannot declare a charge in the same turn.” However, the Venerable Land Raider’s Assault Ramp ability explicitly overrides that restriction, granting the unit charge eligibility. Because the ability is listed in the unit’s datasheet and is an errata entry, it supersedes the base Core Rule. The unit still cannot move further during the Movement phase (it counts as having made a Normal move), but it may declare a charge during the Charge phase.

### allam-2-7b
`finish=error · ? compl tok · ?s` ⚠ ERROR: Error code: 413 - {'error': {'message': 'Request too large for model `allam-2-7b` in organization `org_01kkppmxccfd1r98zztyme6k5a` service tier `on_demand` on tokens per minute (TPM): Limit 6000, Requ


====================================================================================================
## [30] UNITS · mp=OFF · ctx 1647 tok

**Q:** if my boys are embarked in a land raider and the land raider makes a normal move, can my orks get out and charge on the same turn?

**Expected concepts (ground-truth anchors):** [['land raider'], ['disembark'], ['charge']]

<details><summary>rules context sent to every model</summary>

```
[1] Land Raider (Space Marines)
# Ability: Assault Ramp
**Unit:** Land Raider  |  **Faction:** Space Marines

Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn.

---

[2] Disembark ()
# Disembark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit from your army starts your Movement phase embarked within a TRANSPORT model, that unit can disembark in that phase. When a unit disembarks from a TRANSPORT model, set it up on the battlefield so that it is wholly within 3" of that TRANSPORT model and not within Engagement Range of any enemy models. If, for any reason, a disembarking model cannot be set up, that model's unit cannot disembark. Units that disembark from a TRANSPORT model that either Remained Stationary this phase or has not yet made a Normal, Advance or Fall Back move this phase can then act normally (make a Normal move, Advance, shoot, declare a charge, fight, etc.) in the remainder of the turn. Such a disembarking unit cannot choose to Remain Stationary. Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; they cannot move further during this phase. Such a unit also cannot declare a charge in the same turn, but can otherwise act normally in the remainder of the turn. Units cannot disembark from a TRANSPORT model that either Advanced or Fell Back this turn. Units that start your Movement phase embarked within a TRANSPORT can disembark this phase, provided their TRANSPORT has not Advanced or Fallen Back. If a unit disembarks before its TRANSPORT moves, it can act normally. If a unit disembarks after its TRANSPORT moves, it cannot move or charge this turn, but can otherwise act normally. Disembarking units must be set up wholly within 3" of their TRANSPORT and not within Engagement Range of any enemy models (or the unit cannot disembark). Units that disembark this turn cannot Remain Stationary.

---

[3] CHARGE PHASE ()
# CHARGE PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Use the following sequence to charge with your units.
1. SELECT ELIGIBLE UNIT
2. SELECT TARGETS
3. MAKE CHARGE ROLL
4. MAKE CHARGE MOVE
5. REPEAT FOR NEXT ELIGIBLE UNIT
In your Charge phase, if you have any eligible units from your army on the battlefield that you want to charge into close combat, you can select those units, one at a time, to declare a charge. Each can only be selected once per phase. Once all of these charges (if any) have been resolved, progress to the Fight phase. A unit is eligible to charge if it is within 12" of one or more enemy units in your Charge phase, unless any of the following apply:
- That unit Advanced or Fell Back this turn.
- That unit is within Engagement Range of any enemy models.
- That unit is an AIRCRAFT unit.
Warriors hurl themselves into battle to slay with blade, hammer and claw. Strident war cries and frantic screams echo through the whirling smoke as the moment of cataclysmic violence draws near.

---

[4] Charging Over Terrain ()
# Charging Over Terrain
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Unless otherwise stated, a model can be moved over a terrain feature when it makes a Charge move, but not through it. A model can be moved over terrain features that are 2" or less in height as if they were not there. A model can be moved vertically in order to climb up, down and over any terrain features that are taller than this, counting the vertical distance up and/or down as part of its Charge move. Models cannot end a Charge move mid-climb - if it is not possible to make a Charge move as a result, the charge fails. Models can be moved freely over terrain features 2" or less in height. Models cannot move through terrain features taller than 2", but can climb up and down them. The Von Ryan's Leaper declares a charge against the Eradicators, who are on top of a terrain feature 3" in height. The horizontal distance between the two units when the charge is declared is 4 1/2". To end a Charge move within Engagement Range, the Tyranids player would need a Charge roll of 7 or higher.

---

[5] Embark ()
# Embark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit makes a Normal, Advance or Fall Back move, and every model in that unit ends that move within 3" of a friendly TRANSPORT model, they can embark within it. A unit cannot embark if it has already disembarked from a TRANSPORT model in the same phase. Remove the unit from the battlefield and place it to one side - it is now embarked within that TRANSPORT model. Unless otherwise stated, units cannot do anything or be affected in any way while they are embarked. A unit can embark within a friendly TRANSPORT if all of its models end a Normal, Advance or Fall Back move within 3" of that TRANSPORT. A unit cannot embark and disembark in the same phase.

---

[6] TIDE OF MUSCLE (Orks)
# Stratagem: TIDE OF MUSCLE
**Faction:** Orks  |  **Type:** Green Tide – Epic Deed Stratagem  |  **Cost:** 1 CP
**Detachment:** Green Tide
**When:** Your turn — Charge phase
*Once a horde of Orks get a sight of the foe, nothing can stop them.*

WHEN: Your Charge phase. TARGET: One Boyz unit from your army that has not declared a charge this phase. EFFECT: Until the end of the phase, each time your unit declares a charge, add 1 to the Charge roll and, if your unit contains 10 or more models, you can re-roll the Charge roll.’


---

[7] FULL THROTTLE! (Orks)
# Stratagem: FULL THROTTLE!
**Faction:** Orks  |  **Type:** Kult of Speed – Battle Tactic Stratagem  |  **Cost:** 1 CP
**Detachment:** Kult of Speed
**When:** Your turn — Charge phase
*When racing buggies and warbikes charge at full pelt, the power behind their crews’ assault is so great that they can smash through the enemy.*

WHEN: Your Charge phase, just after a SPEED FREEKS unit from your army ends a Charge move. TARGET: That Speed Freeks unit. EFFECT: Until the end of the turn, each time a model in your unit makes a melee attack, add 1 to the Wound roll.


---

[8] ERE WE GO (Orks)
# Stratagem: ERE WE GO
**Faction:** Orks  |  **Type:** War Horde – Battle Tactic Stratagem  |  **Cost:** 1 CP
**Detachment:** War Horde
**When:** Your turn — Movement phase
*Even Orks can put on a surprising turn of speed when the promise of a good face-to-face fight is in the offing.*

WHEN: Start of your Movement phase. TARGET: One Orks Infantry unit from your army. EFFECT: Until the end of the turn, add 2 to Advance and Charge rolls made for your unit.

```
</details>


### qwen/qwen3-32b
`finish=stop · 654 compl tok · 1.7s`

[Ruling] Yes, your Ork Boyz can disembark from the Land Raider after it makes a Normal move and still declare a charge in the same turn.  

[Rule Citation]  
1. **Land Raider (Space Marines) – Assault Ramp Ability** → "Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn."  
2. **Disembark (Core Rules)** → "Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; they cannot move further during this phase. Such a unit also cannot declare a charge in the same turn..."  

[Reasoning]  
The Land Raider’s **Assault Ramp** ability explicitly overrides the standard **Disembark** rule (Core Rules) that normally prevents units disembarking after a Normal move from declaring a charge. The Land Raider’s ability grants an exception, allowing the disembarking unit (your Ork Boyz) to declare a charge in the same turn. This applies only if the Land Raider made a Normal move and the unit disembarks **after** that move. The Boyz must still meet all other charge requirements (e.g., being within 12" of an enemy unit, not having Advanced or Fell Back, etc.).

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 137 compl tok · 0.5s`

[Ruling] → [Disembark] → [Rule Citation: "Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; they cannot move further during this phase. Such a unit also cannot declare a charge in the same turn, but can otherwise act normally in the remainder of the turn."]

[Reasoning]
According to [Disembark], if the Land Raider makes a Normal move, the embarked Orks can disembark. However, since the Land Raider made a Normal move, the disembarked Orks count as having made a Normal move themselves and cannot declare a charge in the same turn.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 205 compl tok · 1.5s`

[Ruling] → A unit disembarking from a Land Raider that made a Normal move this turn cannot declare a charge in the same turn.

→ [Disembark] → Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; they cannot move further during this phase. Such a unit also cannot declare a charge in the same turn, but can otherwise act normally in the remainder of the turn.

→ [Assault Ramp] does not override this, as it only states that the unit is still eligible to declare a charge, but does not change the fact that disembarking units from a TRANSPORT that made a Normal move cannot declare a charge.

The provided rules do not indicate any exceptions for Orks or the Land Raider's Assault Ramp ability that would allow the unit to charge after disembarking following a Normal move by the Land Raider. Therefore, your Orks cannot get out and charge on the same turn.

### openai/gpt-oss-120b
`finish=stop · 781 compl tok · 3.5s`

**Ruling:** Yes – an Ork unit embarked in a Land Raider may disembark after the Land Raider makes a Normal move and still declare a charge in the same turn.

**Rule Citation:**  
- **Land Raider – Assault Ramp** (Ability) – “Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn.” [1]  
- **Disembark** (Core Rule) – “Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; … Such a unit also cannot declare a charge in the same turn…” [2]

**Reasoning:**  
The Disembark rule normally prevents a unit that disembarks from a transport which has made a Normal move from charging that turn. However, the Land Raider’s Assault Ramp ability explicitly overrides this restriction by stating that units disembarking after the Land Raider’s Normal move remain eligible to charge. Since the ability is a specific rule for the Land Raider, it takes precedence over the generic Disembark rule, allowing the Ork unit to charge.

### openai/gpt-oss-20b
`finish=stop · 840 compl tok · 1.2s`

**Ruling**  
Yes.  If the Land Raider has made a Normal move, any unit that disembarks from it is still eligible to declare a charge in that same turn.

**Rule Citations**  
1. **Land Raider – Assault Ramp** (Ability) – “Each time a unit disembarks from this model after it has made a Normal move, that unit is still eligible to declare a charge this turn.”  
2. **Disembark** (Core Rules) – “Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; they cannot move further during this phase. **Such a unit also cannot declare a charge in the same turn** …”  

**Reasoning**  
- The Assault Ramp ability explicitly states that a unit disembarking after the Land Raider’s Normal move remains eligible to charge.  
- The Disembark rule normally bars a unit that disembarks from a transport that has moved from charging.  
- Because the Assault Ramp ability is a specific ability of the Land Raider, it overrides the general Disembark rule for that transport.  
- Therefore, the Orks can disembark and then declare a charge in the same turn, though they cannot make any further move after disembarking.

### allam-2-7b
`finish=stop · 77 compl tok · 0.8s`

Based on the provided rules, the Orks can embark in a Land Raider and charge on the same turn if the Land Raider makes a Normal Move.


Ruling:

[Ruling] → [Rule Name] → [Rule Source]


The Land Raider unit can embark and charge in the same turn if it moves normally.


====================================================================================================
## [31] UNITS · mp=OFF · ctx 1954 tok

**Q:** Chief Librarian Mephiston has Fights First. If he is in combat with an enemy unit that also has Fights First, who fights first?

**Expected concepts (ground-truth anchors):** [['fights first'], ['mephiston']]

<details><summary>rules context sent to every model</summary>

```
[1] Chief Librarian Mephiston (Space Marines)
# Ability: Fights First
**Unit:** Chief Librarian Mephiston  |  **Faction:** Space Marines

FIGHTS FIRST Some warriors attack with blinding speed, landing their blows before their foes can react. Units with this ability that are eligible to fight do so in the Fights First step, provided every model in the unit has this ability.

---

[2] 1. Fights First ()
# 1. Fights First
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In this step, all eligible units with the Fights First ability fight. Remember that this will include units that made a Charge move this turn and that have a Charge bonus.
FIGHTS FIRST Some warriors attack with blinding speed, landing their blows before their foes can react. Units with this ability that are eligible to fight do so in the Fights First step, provided every model in the unit has this ability.

---

[3] FIGHT PHASE ()
# FIGHT PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The Fight phase is split into two steps. Units that have the ability to Fight First do so, followed by any remaining eligible units.
1. FIGHTS FIRST
2. Units that can Fight First do so
3. REMAINING COMBATS
4. Remaining units that can fight do so
In both steps of the Fight phase, players alternate selecting eligible units from their army, one at a time, starting with the player whose turn is not taking place, and fighting with them. Note that a player cannot pass or opt not to fight when they have one or more eligible units that could fight - they must select one of them to fight. In both steps, a unit is eligible to fight if either or both of the following apply: It is within Engagement Range of one or more enemy units. It made a Charge move this turn. No unit can fight more than once in the Fight phase. In each step, if all of one player's eligible units that can fight during that step have fought, the opposing player can then fight with all of their remaining eligible units that can fight during that step, one at a time.
Once neither player has any eligible units to fight with during the current step, you progress to the next step. Once all eligible units have fought in every step, the Fight phase ends. The player's turn then ends and, unless the battle ends, the next player's turn begins. Note that after an enemy unit has fought and finished its Consolidation move, it might be that previously ineligible units are now eligible - these units can then be selected to fight during the Remaining Combats step.
Carnage engulfs the battlefield as the warring armies meet head-on. Fangs and claws crunch through bone. Blades ring like hammers on anvils. Blood spurts and flesh tears as hate-filled foes tear one another apart.

---

[4] 2. Remaining Combats ()
# 2. Remaining Combats
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In this step, all remaining eligible units fight. This includes any units with the Fights First ability that were not eligible to fight at the start of the Fight phase, but have since become eligible to fight.

---

[5] Declare Battle Formations ()
# Declare Battle Formations
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In the order stated below, both players now secretly note down: Which of their Leader units will start the battle attached (they must specify which Leader unit is attached to which Bodyguard unit). Which of their units will start the battle embarked within TRANSPORT models (they must specify which units are embarked within which models). Which of their units will start the battle in Reserves (including Strategic Reserves). When both players have done so, they declare their selections to their opponent.

---

[6] Chief Librarian Mephiston (Space Marines)
# Ability: Oath of Moment
**Unit:** Chief Librarian Mephiston  |  **Faction:** Space Marines

If your Army Faction is ADEPTUS ASTARTES, at the start of your Command phase, select one unit from your opponent’s army. Until the start of your next Command phase, that enemy unit is your Oath of Moment target. Each time a model with this ability makes an attack that targets your Oath of Moment target: You can re-roll the Hit roll., If you are using a Codex: Space Marines Detachment and your army does not include one or more units with the Black Templars, Blood Angels, Dark Angels, Deathwatch or Space Wolves keywords, add 1 to the Wound roll as well.

---

[7] Judiciar (Space Marines)
# Ability: Tempormortis
**Unit:** Judiciar  |  **Faction:** Space Marines

While this model is leading a unit, that unit has the Fights First ability.

---

[8] Brotherhood Librarian (Grey Knights)
# Ability: Leader
**Unit:** Brotherhood Librarian  |  **Faction:** Grey Knights

LEADER Mighty heroes fight at the forefront of battle. Some CHARACTER units have ‘Leader’ listed on their datasheets. Such CHARACTER units are known as Leaders, and the units they can lead – known as their Bodyguard units – are listed on their datasheet. During the Declare Battle Formations step, for each Leader in your army, if your army also includes one or more of that Leader’s Bodyguard units, you can select one of those Bodyguard units. That Leader will then attach to that Bodyguard unit for the duration of the battle and is said to be leading that unit. Each Bodyguard unit can only have one Leader attached to it. While a Bodyguard unit contains a Leader, it is known as an Attached unit and, with the exception of rules that are triggered when units are destroyed, it is treated as a single unit for all rules purposes. Each time an attack targets an Attached unit, until the attacking unit has resolved all of its attacks, you must use the Toughness characteristic of the Bodyguard models in that unit, even if a Leader in that unit has a different Toughness characteristic. Each time an attack sucessfully wounds an Attached unit, that attack cannot be allocated to a CHARACTER model in that unit, even if that CHARACTER model has lost one or more wounds or has already had attacks allocated to it this phase. As soon as the last Bodyguard model in an Attached unit has been destroyed, any attacks made against that unit that have yet to be allocated can then be allocated to CHARACTER models in that unit. Each time the last model in a Bodyguard unit is destroyed, each CHARACTER unit that is part of that Attached unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time the last model in a CHARACTER unit that is attached to a Bodyguard unit is destroyed and there is not another CHARACTER unit attached, that Attached unit’s Bodyguard unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time a unit that is part of an Attached unit is destroyed, it does not have the keywords of any other units that make up that Attached unit (unless it has those keywords on its own datasheet) for the purposes of any rules that would be triggered when that unit is destroyed. Example: If you only destroy the Bodyguard unit that is part of an Attached unit, you have not destroyed a CHARACTER unit. If you only destroy the CHARACTER unit that is part of an Attached unit, or if you destroy the whole Attached unit, you have destroyed one CHARACTER unit. Before the battle, CHARACTER units with the Leader ability can be attached to one of their Bodyguard units to form an Attached unit., Attached units can only contain one Leader., Attacks cannot be allocated to CHARACTER models in Attached units.
```
</details>


### qwen/qwen3-32b
`finish=stop · 1742 compl tok · 3.7s`

[Ruling] Both units fight in the Fights First step, with the non-active player (the player not currently taking their turn) selecting their unit to fight first. The active player then selects their unit to fight second. This alternation continues for all eligible units.  

[Rule Citation] **FIGHT PHASE** (Core Rules, Wahapedia_Core_Rules) → "In both steps of the Fight phase, players alternate selecting eligible units from their army, one at a time, starting with the player whose turn is not taking place..."  

[Reasoning] The Fights First step explicitly requires players to alternate selecting units to fight, beginning with the non-active player. Since both units are eligible (they have Fights First and are in combat), the order is determined by turn order, not by the units themselves. The non-active player acts first, followed by the active player. This applies regardless of which faction controls which unit.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 155 compl tok · 0.8s`

[Ruling] → [Rule Citation] → [Reasoning]

In this scenario, Chief Librarian Mephiston has the Fights First ability, and the enemy unit also has the Fights First ability. 

According to [3] FIGHT PHASE, the Fight phase is split into two steps: Fights First and Remaining Combats. Units with the Fights First ability fight in the Fights First step.

Since both Chief Librarian Mephiston and the enemy unit have the Fights First ability, they will fight in the Fights First step. However, the rules do not specify which unit fights first when multiple units with Fights First are present.

The provided rules do not clearly address this — I recommend checking the official GW FAQ.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 152 compl tok · 1.4s`

[Ruling] → Units with Fights First fight in the Fights First step if they are eligible to fight. 
→ [FIGHTS FIRST (Core_Rules)] → 
[Reasoning] According to the FIGHTS FIRST step in the Core Rules, units with the Fights First ability fight in this step if they are eligible to fight. Eligibility to fight is determined by being within Engagement Range of one or more enemy units or having made a Charge move this turn. If both units in question are eligible to fight and have Fights First, they will fight in the Fights First step. The order in which they fight within that step is determined by the players alternating selecting units to fight, as described in the FIGHT PHASE rules.

### openai/gpt-oss-120b
`finish=stop · 563 compl tok · 1.6s`

**Ruling** – When both Mephiston and the enemy unit have the **Fights First** ability, they are both eligible to fight in the **Fights First** step of the Fight phase. The order in which they actually fight is decided by the alternating selection rule: the player whose turn is *not* taking place selects a unit first, then the active player selects, and they continue alternating until all eligible units with **Fights First** have fought. Therefore, the non‑active player’s unit will fight before the active player’s unit.  

**Rule Citation** – *Fight Phase* (Core Rules, Wahapedia):  

> “The Fight phase is split into two steps. Units that have the ability to Fight First do so, followed by any remaining eligible units. … In both steps of the Fight phase, players alternate selecting eligible units from their army, one at a time, **starting with the player whose turn is not taking place**, and fighting with them.”  

**Reasoning** – Both Mephiston and the enemy unit satisfy the eligibility criteria for the **Fights First** step (they have the ability and are within engagement range or have charged). Since the step begins with the non‑active player choosing a unit, that player’s **Fights First** unit will act first, after which the active player may choose theirs. No rule gives priority to one unit over another beyond this selection order, so the first fighter is simply the unit chosen by the player who does **not** have the current turn.

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=stop · 186 compl tok · 0.5s`

Based on the provided rules, the Chief Librarian Mephiston fights first.


The provided rules mention the Fights First ability for Chief Librarian Mephiston. When two units have this ability, the unit with Fights First goes first. In this case, Chief Librarian Mephiston has Fights First, so he fights first. 


[Ruling] → Core Rule 10.10.1 (Fights First) → WAAAGP (Fights First) → WAAAGP (Fights First)


---

The provided rules do not specify any interaction between Chief Librarian Mephiston and the enemy unit. Therefore, the question cannot be answered based on the given context. I recommend checking the official Warhammer 40k rules for any potential interactions between the units.


====================================================================================================
## [32] UNITS · mp=OFF · ctx 1411 tok

**Q:** How does the Aegis Defence Line fortification give units the Benefit of Cover, and how do models interact with it?

**Expected concepts (ground-truth anchors):** [['benefit of cover', 'cover'], ['aegis']]

<details><summary>rules context sent to every model</summary>

```
[1] Aegis Defence Line (Astra Militarum)
# Ability: Reinforced Cover
**Unit:** Aegis Defence Line  |  **Faction:** Astra Militarum

Each time a ranged attack is allocated to a model, if that model is not fully visible to every model in the attacking unit because of this FORTIFICATION, that model has the Benefit of Cover against that attack.

---

[2] Benefit of Cover ()
# Benefit of Cover
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Shattered ruins and twisted wreckage afford much-needed shelter from enemy salvoes. Even heavily armoured warriors unfazed by small arms fire are thankful for such cover when foes bring their biggest guns to bear. Models can sometimes gain a measure of protection from terrain features. The rules below detail the conditions under which a terrain feature confers the Benefit of Cover on a model. Each time a ranged attack is allocated to a model that has the Benefit of Cover, add 1 to the saving throw made for that attack (excluding invulnerable saving throws). Models with a Save characteristic of 3+ or better cannot have the Benefit of Cover against attacks with an Armour Penetration characteristic of 0. Multiple instances of the Benefit of Cover are not cumulative - a model cannot benefit from this rule more than once at any one time. Benefit of Cover: Add 1 to armour saving throws against ranged attacks. Does not apply to models with a Save of 3+ or better against attacks with an AP of 0. Multiple instances are not cumulative.

---

[3] Barricades and Fuel Pipes ()
# Barricades and Fuel Pipes
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Fuel pipes and purpose-made defence lines are excellent positions from which to repel the enemy. MOVEMENT Models can move up, over and down this terrain feature, but they cannot be set up or end any kind of move on top of it. VISIBILITY Normal visibility rules apply. ENGAGEMENT RANGE In the Charge phase, if an enemy unit is within 1" of this terrain feature, a charging unit on the opposite side of this terrain feature can still make a Charge move against that enemy unit provided it ends that Charge move as close as possible to this terrain feature and within 2" of that enemy unit. In the Fight phase, units are eligible to fight - and models can make attacks - if their target is on the opposite side of this terrain feature and within 2" of them. BENEFIT OF COVER Each time a ranged attack is allocated to an INFANTRY model that is wholly within 3" of this terrain feature, if that model is not fully visible to every model in the attacking unit because of this terrain feature, that model has the Benefit of Cover against that attack. KEYWORDS: OBSTACLE, BARRICADE

---

[4] Ignores Cover ()
# Ignores Cover
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some weapons are designed to root enemy formations out of entrenched positions.
Weapons with [IGNORES COVER] in their profile are known as Ignores Cover weapons. Each time an attack is made with such a weapon, the target cannot have the Benefit of Cover against that attack.

---

[5] Hills, Industrial Structures, Sealed Buildings and Armoured Containers ()
# Hills, Industrial Structures, Sealed Buildings and Armoured Containers
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

A sealed bunker, Mechanicus gantry-way, armoured container or even a simple hill can shelter troops from the enemy's sight and provide a superior vantage point to those atop it. MOVEMENT These terrain features are raised areas that models can be set up on top of or end a move on top of, provided the model's base does not overhang the terrain feature (if the model does not have a base, no part of that model that would be in contact with the battlefield at ground level can overhang that terrain feature). In addition, other terrain features can be set up on top of a HILL terrain feature, provided no part of those terrain features overhangs that HILL terrain feature. VISIBILITY Normal visibility rules apply. BENEFIT OF COVER Each time a ranged attack is allocated to a model, if that model is not fully visible to every model in the attacking unit because of this terrain feature, that model has the Benefit of Cover against that attack. KEYWORDS: HILL

---

[6] Aegis Defence Line (Astra Militarum)
# Ability: Fortification
**Unit:** Aegis Defence Line  |  **Faction:** Astra Militarum

While an enemy unit is only within Engagement Range of one or more FORTIFICATIONS from your army: That unit can still be selected as the target of ranged attacks, but each time such an attack is made, unless it is made with a Pistol, subtract 1 from the Hit roll., Models in that unit do not need to take Desperate Escape tests due to Falling Back while Battle-shocked, except for those that will move over enemy models when doing so.

---

[7] Aegis Defence Line With Weapon Emplacement (Unaligned Forces)
# Ability: Defence Line
**Unit:** Aegis Defence Line With Weapon Emplacement  |  **Faction:** Unaligned Forces

When this FORTIFICATION is set up, all parts of it must be set up within 1" of another part. While an INFANTRY model has the Benefit of Cover as a result of this FORTIFICATION (see below), that model has a 4+ invulnerable save.

---

[8] Wall Of Martyrs Defence Line (Unaligned Forces)
# Ability: Defence Line
**Unit:** Wall Of Martyrs Defence Line  |  **Faction:** Unaligned Forces

When this FORTIFICATION is set up, all parts of it must be set up within 1" of another part. While an INFANTRY model has the Benefit of Cover as a result of this FORTIFICATION (see in FORTIFICATION section), that model has a 4+ invulnerable save.
```
</details>


### qwen/qwen3-32b
`finish=stop · 989 compl tok · 2.4s`

[Ruling] The **Aegis Defence Line** grants the **Benefit of Cover** to models that are not fully visible to the attacking unit due to the fortification. This applies only to ranged attacks. When this occurs, the affected model gains the standard **Benefit of Cover** rules (add 1 to their armour save), unless they have a Save of 3+ or better against attacks with AP 0. The **Reinforced Cover** ability (rule 1) explicitly triggers the **Benefit of Cover** (rule 2) under these visibility conditions.  

[Rule Citation]  
- **Aegis Defence Line (Reinforced Cover):** [1]  
- **Benefit of Cover (Core Rules):** [2]  

[Reasoning]  
1. **Reinforced Cover** (rule 1) states that the Aegis Defence Line grants the Benefit of Cover to models not fully visible to the attacking unit due to the fortification.  
2. **Benefit of Cover** (rule 2) defines the mechanical effect: +1 to armour saves against ranged attacks (excluding invulnerable saves), with exceptions for models with a Save of 3+ or better against AP 0 attacks.  
3. The **Ignores Cover** rule (rule 4) would negate this benefit if the attack uses a weapon with that profile.  
4. The **Fortification** ability (rule 6) does not interact with the Benefit of Cover in this context.  

Additional rules (rules 7 and 8) about invulnerable saves apply only to specific variants of the Aegis Defence Line (e.g., "Aegis Defence Line With Weapon Emplacement") and are not relevant to the standard Aegis Defence Line.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 295 compl tok · 1.1s`

[Ruling] → [Rule Citation] → [Reasoning]

The Aegis Defence Line fortification gives units the Benefit of Cover as per [3] Barricades and Fuel Pipes → BENEFIT OF COVER: Each time a ranged attack is allocated to an INFANTRY model that is wholly within 3" of this terrain feature, if that model is not fully visible to every model in the attacking unit because of this terrain feature, that model has the Benefit of Cover against that attack.

However, the Aegis Defence Line fortification is not a terrain feature, but rather a unit with the FORTIFICATION keyword. Therefore, we need to look at its ability, [6] Aegis Defence Line → While an enemy unit is only within Engagement Range of one or more FORTIFICATIONS from your army: That unit can still be selected as the target of ranged attacks, but each time such an attack is made, unless it is made with a Pistol, subtract 1 from the Hit roll.

This ability does not explicitly state that the Aegis Defence Line fortification gives units the Benefit of Cover. However, it does mention that enemy units can still be targeted with ranged attacks, but with a penalty to the Hit roll. This suggests that the Aegis Defence Line fortification is affecting the enemy unit's ability to hit, rather than providing cover to friendly units.

Therefore, the Aegis Defence Line fortification does not give units the Benefit of Cover.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 244 compl tok · 1.9s`

[Ruling] → The Aegis Defence Line fortification gives units the Benefit of Cover through its "Reinforced Cover" ability. 

→ [Reinforced Cover, Aegis Defence Line (Astra Militarum)] → 
Each time a ranged attack is allocated to a model, if that model is not fully visible to every model in the attacking unit because of this FORTIFICATION, that model has the Benefit of Cover against that attack.

→ The provided rules do not explicitly state how models interact with the Aegis Defence Line in terms of movement. However, according to [Barricades and Fuel Pipes], models can move up, over, and down similar terrain features, but they cannot be set up or end any kind of move on top of it. It can be inferred that similar rules might apply to the Aegis Defence Line, but this is not explicitly stated. 

→ For more information on movement and interaction, refer to [Barricades and Fuel Pipes] and other terrain feature rules. 

The Aegis Defence Line does not have an explicit movement interaction rule provided; therefore, The provided rules do not clearly address this — I recommend checking the official GW FAQ.

### openai/gpt-oss-120b
`finish=stop · 1226 compl tok · 2.9s`

**Ruling**  
The Aegis Defence Line fortification grants the *Benefit of Cover* to any model that is not fully visible to every model in the attacking unit because of the fortification. When that condition is met, the model adds +1 to its armour saving throw against the ranged attack (unless it has a 3+ save against an AP 0 attack, and the benefit does not stack with other sources of Cover). In addition, the fortification’s own *Fortification* ability gives a –1 penalty to the hit roll of any ranged attack made against a unit within Engagement Range of the fortification (except when the attack is made with a pistol). Models interact with the fortification simply by being positioned such that the fortification blocks line of sight; there is no rule in the provided context that restricts moving onto or setting up on the fortification.

**Rule Citations**  

1. **Aegis Defence Line – Ability: Reinforced Cover** (Astra Militarum) – “Each time a ranged attack is allocated to a model, if that model is not fully visible to every model in the attacking unit because of this FORTIFICATION, that model has the Benefit of Cover against that attack.”【1】

2. **Benefit of Cover** (Core Rules) – “Each time a ranged attack is allocated to a model that has the Benefit of Cover, add 1 to the saving throw made for that attack (excluding invulnerable saving throws)… Multiple instances of the Benefit of Cover are not cumulative.”【2】

3. **Aegis Defence Line – Ability: Fortification** (Astra Militarum) – “While an enemy unit is only within Engagement Range of one or more FORTIFICATIONS… each time such an attack is made, unless it is made with a Pistol, subtract 1 from the Hit roll.”【6】

**Reasoning**  

- The *Reinforced Cover* ability explicitly ties the fortification to the generic *Benefit of Cover* rule. The condition (“not fully visible … because of this FORTIFICATION”) mirrors the visibility condition used by other terrain features (e.g., Hills, Barricades).  
- Once the condition is satisfied, the *Benefit of Cover* rule applies, granting +1 to armour saves against that ranged attack (subject to the Save 3+ vs AP 0 limitation and the non‑cumulative clause).  
- The fortification also has a separate *Fortification* ability that imposes a –1 penalty to hit rolls for ranged attacks (except pistols), providing an additional defensive benefit that stacks with the saving‑throw bonus.  
- No movement or setup restrictions for the fortification are given in the supplied context, so models may be placed in any legal position relative to the fortification; the only interaction required for the Cover benefit is that the fortification must block full visibility.  

Thus, units behind the Aegis Defence Line gain the *Benefit of Cover* (‑1 to hit from the Fortification ability and +1 to armour saves from the Cover benefit) whenever the line blocks line of sight, and the benefit does not stack with other sources of Cover. Weapons with the **[IGNORES COVER]** keyword would negate the saving‑throw bonus, per the *Ignores Cover* rule.

### openai/gpt-oss-20b
`finish=length · 4096 compl tok · 4.4s`



### allam-2-7b
`finish=stop · 240 compl tok · 0.6s`

Based on the provided context, the Aegis Defence Line fortification gives units the Benefit of Cover. When a model is within 1" of the fortification, it has the Benefit of Cover.


The Benefit of Cover allows a model to have a 4+ invulnerable save. This means that when a model is within 1" of the Aegis Defence Line fortification, it has a 4+ invulnerable save. 


The provided context does not specify how models interact with the Aegis Defence Line fortification, but the context does not contradict or modify the standard rules for interacting with terrain features. Therefore, models can interact with the Aegis Defence Line fortification as they would with any other terrain feature, such as Walls, Tunnels, or other Fortifications. They can still be targeted, engaged, and potentially affected by other rules like the Benefit of Cover. 


The provided context does not mention any specific interaction rules for the Aegis Defence Line fortification, so we can assume that models interact with it as they would with other terrain features.


====================================================================================================
## [33] UNITS · mp=OFF · ctx 2489 tok

**Q:** While Vargard Obyron leads a unit, his Ghostwalk Mantle gives it Fights First — how does the Fights First rule resolve when both sides have it in the Fight phase?

**Expected concepts (ground-truth anchors):** [['obyron'], ['ghostwalk mantle'], ['fights first'], ['whose turn is not taking place', 'alternat', 'pile in']]

<details><summary>rules context sent to every model</summary>

```
[1] Vargard Obyron (Necrons)
# Ability: Ghostwalk Mantle
**Unit:** Vargard Obyron  |  **Faction:** Necrons

While this model is leading a unit, models in that unit have the Fights First ability.

---

[2] FIGHT PHASE ()
# FIGHT PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The Fight phase is split into two steps. Units that have the ability to Fight First do so, followed by any remaining eligible units.
1. FIGHTS FIRST
2. Units that can Fight First do so
3. REMAINING COMBATS
4. Remaining units that can fight do so
In both steps of the Fight phase, players alternate selecting eligible units from their army, one at a time, starting with the player whose turn is not taking place, and fighting with them. Note that a player cannot pass or opt not to fight when they have one or more eligible units that could fight - they must select one of them to fight. In both steps, a unit is eligible to fight if either or both of the following apply: It is within Engagement Range of one or more enemy units. It made a Charge move this turn. No unit can fight more than once in the Fight phase. In each step, if all of one player's eligible units that can fight during that step have fought, the opposing player can then fight with all of their remaining eligible units that can fight during that step, one at a time.
Once neither player has any eligible units to fight with during the current step, you progress to the next step. Once all eligible units have fought in every step, the Fight phase ends. The player's turn then ends and, unless the battle ends, the next player's turn begins. Note that after an enemy unit has fought and finished its Consolidation move, it might be that previously ineligible units are now eligible - these units can then be selected to fight during the Remaining Combats step.
Carnage engulfs the battlefield as the warring armies meet head-on. Fangs and claws crunch through bone. Blades ring like hammers on anvils. Blood spurts and flesh tears as hate-filled foes tear one another apart.

---

[3] 1. Fights First ()
# 1. Fights First
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In this step, all eligible units with the Fights First ability fight. Remember that this will include units that made a Charge move this turn and that have a Charge bonus.
FIGHTS FIRST Some warriors attack with blinding speed, landing their blows before their foes can react. Units with this ability that are eligible to fight do so in the Fights First step, provided every model in the unit has this ability.

---

[4] Resolve Pre-battle Rules ()
# Resolve Pre-battle Rules
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Players alternate resolving any pre-battle rules units from their armies have, starting with the player who will take the first turn.

---

[5] Begin the Battle ()
# Begin the Battle
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The first battle round begins. Players continue to complete battle rounds until the battle ends.

---

[6] Vargard Obyron (Necrons)
# Vargard Obyron
**Faction:** Necrons  |  **Role:** Characters  |  **Source:** 000000358
**Version/Errata Date:** 01.01.0001 0:00:00 *(errata)*

## Stats
| Model | M | T | Sv | Inv | W | Ld | OC | Base |
|---|---|---|---|---|---|---|---|---|
| Vargard Obyron | 5" | 5 | 2+ | - | 5 | 6+ | 1 | 25mm |

## Unit Composition
- 1 Vargard Obyron – EPIC HERO

## Points Costs
- 1 model: **85 pts**

## Wargear
| Weapon | Range | Type | A | BS/WS | S | AP | D |
|---|---|---|---|---|---|---|---|
| Warscythe | Melee | Melee | 4 | 2 | 8 | -3 | 2 |
|   | *devastating wounds, precision* | | | | | | |

## Datasheet Abilities
**Ghostwalk Mantle**
> While this model is leading a unit, models in that unit have the Fights First ability.

**The Vargard’s Duty**
> While this model is in the same unit as Nemesor Zahndrekh, Character models in that unit have the Feel No Pain 4+ ability.

## Faction Abilities
**Reanimation Protocols**
> If your Army Faction is NECRONS, at the end of your Command phase, each unit from your army with this ability that is on the battlefield activates its Reanimation Protocols and reanimates D3 wounds. Each time such a unit reanimates a wound: If that unit contains one or more models with fewer than their starting number of wounds remaining, select one of those models; that model regains one lost wound, If all models in that unit have their starting number of wounds, but that unit is not at its Starting Strength, one destroyed model is returned to that unit with one wound remaining., Once such a unit is at its Starting Strength and all of its models have their starting number of wounds, nothing further happens. Example: A unit of Lokhust Destroyers (which have a Wounds characteristic of 3) activates its Reanimation Protocols. The unit had a Starting Strength of 3, but currently contains 2 models, and one of those models has lost 1 wound. A 3 is rolled to see how many wounds are reanimated. The first of these reanimated wounds restores the wounded Lokhust Destroyer back to 3 wounds. The second of these reanimated wounds returns the destroyed Lokhust Destroyer to the battlefield with 1 wound remaining. The third of these reanimated wounds restores one of the remaining lost wounds to the same Lokhust Destroyer that was just returned. The unit now contains 3 models, two of which have 3 wounds remaining and one of which has 2 wounds remaining.

## Core Abilities
**Leader**
> LEADER Mighty heroes fight at the forefront of battle. Some CHARACTER units have ‘Leader’ listed on their datasheets. Such CHARACTER units are known as Leaders, and the units they can lead – known as their Bodyguard units – are listed on their datasheet. During the Declare Battle Formations step, for each Leader in your army, if your army also includes one or more of that Leader’s Bodyguard units, you can select one of those Bodyguard units. That Leader will then attach to that Bodyguard unit for the duration of the battle and is said to be leading that unit. Each Bodyguard unit can only have one Leader attached to it. While a Bodyguard unit contains a Leader, it is known as an Attached unit and, with the exception of rules that are triggered when units are destroyed, it is treated as a single unit for all rules purposes. Each time an attack targets an Attached unit, until the attacking unit has resolved all of its attacks, you must use the Toughness characteristic of the Bodyguard models in that unit, even if a Leader in that unit has a different Toughness characteristic. Each time an attack sucessfully wounds an Attached unit, that attack cannot be allocated to a CHARACTER model in that unit, even if that CHARACTER model has lost one or more wounds or has already had attacks allocated to it this phase. As soon as the last Bodyguard model in an Attached unit has been destroyed, any attacks made against that unit that have yet to be allocated can then be allocated to CHARACTER models in that unit. Each time the last model in a Bodyguard unit is destroyed, each CHARACTER unit that is part of that Attached unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time the last model in a CHARACTER unit that is attached to a Bodyguard unit is destroyed and there is not another CHARACTER unit attached, that Attached unit’s Bodyguard unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time a unit that is part of an Attached unit is destroyed, it does not have the keywords of any other units that make up that Attached unit (unless it has those keywords on its own datasheet) for the purposes of any rules that 
```
</details>


### qwen/qwen3-32b
`finish=stop · 932 compl tok · 2.2s`

[Ruling] When both sides have units with the **Fights First** ability, they resolve in the **Fights First** step of the Fight phase by alternating selections, starting with the inactive player (the player not taking their turn). All eligible units with **Fights First** (including those granted by Vargard Obyron’s *Ghostwalk Mantle*) fight in this step. Players must select eligible units one at a time, and no unit can fight more than once.  

[Rule Citation]  
- **FIGHT PHASE** [2] → "The Fight phase is split into two steps. Units that have the ability to Fight First do so, followed by any remaining eligible units."  
- **1. FIGHTS FIRST** [3] → "In this step, all eligible units with the Fights First ability fight... provided every model in the unit has this ability."  
- **Core Rule Interaction** → The *Ghostwalk Mantle* explicitly grants **Fights First** to all models in the unit, satisfying the "every model in the unit has this ability" condition.  

[Reasoning]  
The **Fights First** step prioritizes units with this ability. Both players’ eligible units (including those led by Vargard Obyron) are resolved in this step. Players alternate selecting units to fight, starting with the inactive player, until all eligible **Fights First** units have fought. This applies regardless of which faction grants the ability, as long as the unit meets the "every model has this ability" requirement.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 236 compl tok · 0.9s`

[Ruling] → [Rule Citation] → [Reasoning]

The Fights First ability resolves as follows:

1. The Fights First step is triggered, as per [3] 1. Fights First () → [3].
2. All eligible units with the Fights First ability fight, including Vargard Obyron's unit and the Infernal Enrapturess unit → [3].
3. Since both units have the Fights First ability, they will fight in the Fights First step → [3].
4. The remaining eligible units will fight in the Remaining Combats step → [2].

The Fights First rule does not specify a priority or order of resolution between units with the Fights First ability. Therefore, both Vargard Obyron's unit and the Infernal Enrapturess unit will fight in the Fights First step, and the remaining eligible units will fight in the Remaining Combats step.

Note that the CORNERED AND KRUMPED stratagem does not affect the resolution of the Fights First ability, as it is a separate rule that only applies to the Movement phase → [8].

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 223 compl tok · 1.3s`

[Ruling] → The Fights First step occurs first, and units with Fights First that are eligible to fight do so. → [FIGHTS FIRST (3)] → [Reasoning]

When both sides have units with the Fights First ability, the units with Fights First on both sides fight in the Fights First step. According to the Fights First rule (3), "units with this ability that are eligible to fight do so in the Fights First step, provided every model in the unit has this ability." 

The Fight phase sequence (2) dictates that units with Fights First fight in the first step, followed by remaining eligible units. Since both sides have units with Fights First, they will fight in the Fights First step. The player whose turn is not taking place goes first, and then players alternate selecting units to fight.

In this case, Vargard Obyron's Ghostwalk Mantle gives his unit the Fights First ability. When both sides have units with Fights First, they fight in the Fights First step according to the core rules.

### openai/gpt-oss-120b
`finish=stop · 1100 compl tok · 3.2s`

**Ruling**  
When both armies have units that possess the *Fights First* ability (e.g., Vargard Obyron’s led unit and an enemy unit such as an Infernal Enrapturess), those units are all resolved in the **Fights First** step of the Fight phase. During that step the two players alternate selecting eligible units, beginning with the player whose turn is *not* taking place, until every eligible *Fights First* unit has fought. After that the phase proceeds to the **Remaining Combats** step for any other eligible units.

**Rule Citation**  
- *Fight Phase* – “The Fight phase is split into two steps. Units that have the ability to Fight First do so, followed by any remaining eligible units… In both steps of the Fight phase, players alternate selecting eligible units from their army, one at a time, **starting with the player whose turn is not taking place**… Once neither player has any eligible units to fight with during the current step, you progress to the next step.” (Rule [2])  
- *1. Fights First* – “In this step, all eligible units with the **Fights First** ability fight… Units with this ability that are eligible to fight do so in the Fights First step, provided every model in the unit has this ability.” (Rule [3])

**Reasoning**  
The *Ghostwalk Mantle* ability gives Vargard Obyron’s unit the *Fights First* keyword (Rule [1]), making it eligible for the first step of the Fight phase. The Fight phase rules (Rule [2]) explicitly define the order of play within each step: the non‑active player selects first, then players alternate, and no player may pass while they have eligible units. Since the *Fights First* step (Rule [3]) simply gathers all eligible units with that ability, the presence of *Fights First* on both sides does not change the alternating selection order; it only means that all such units are fought before any other units. Consequently, the resolution proceeds exactly as the core rules describe: alternating selections beginning with the non‑active player, then moving to the Remaining Combats step once all *Fights First* units have fought.

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=stop · 814 compl tok · 0.9s`


















































































































































































































































































































































































































































































































































































































































































































































































































































====================================================================================================
## [34] ILLEGAL · mp=OFF · ctx 1536 tok

**Q:** Can a 5-model Terminator Squad embark inside a Rhino transport?

**Expected concepts (ground-truth anchors):** [['cannot transport'], ['rhino']]

<details><summary>rules context sent to every model</summary>

```
[1] Rhino (Grey Knights)
# Rhino — Transport
**Unit:** Rhino  |  **Faction:** Grey Knights

This model has a transport capacity of 12 Grey Knights Infantry models. It cannot transport Terminator models.

---

[2] Terminator Squad (Space Marines)
# Terminator Squad — Wargear Options
**Unit:** Terminator Squad  |  **Faction:** Space Marines

- For every 5 models in this unit, 1 Terminator’s storm bolter can be replaced with one of the following: 1 assault cannon, 1 heavy flamer, 1 cyclone missile launcher and 1 storm bolter.*
- Any number of models can each have their power fist replaced with 1 chainfist.
- The Terminator Squad Leader’s power fist can be replaced with 1 power weapon.
- * This model’s storm bolter cannot be replaced.

---

[3] Transports ()
# Transports
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some models have the TRANSPORT keyword. The following rules describe how units can embark within and disembark from such models, and how they are used to move these passengers across the battlefield.
Some units can carry others across the battlefield, providing their passengers with greater speed and protection as they are ferried to the front lines or towards vital objectives.

---

[4] Embark ()
# Embark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit makes a Normal, Advance or Fall Back move, and every model in that unit ends that move within 3" of a friendly TRANSPORT model, they can embark within it. A unit cannot embark if it has already disembarked from a TRANSPORT model in the same phase. Remove the unit from the battlefield and place it to one side - it is now embarked within that TRANSPORT model. Unless otherwise stated, units cannot do anything or be affected in any way while they are embarked. A unit can embark within a friendly TRANSPORT if all of its models end a Normal, Advance or Fall Back move within 3" of that TRANSPORT. A unit cannot embark and disembark in the same phase.

---

[5] Transport Capacity ()
# Transport Capacity
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

All TRANSPORT models have a transport capacity listed on their datasheet. This determines the type and maximum number of friendly models that can embark within them. Units can start the battle embarked within a TRANSPORT model instead of being set up separately - declare which units are embarked within a TRANSPORT model before you set it up. FIRING DECK Some transports have firing hatches, ports or platforms from which embarked passengers can shoot. Some TRANSPORT models have 'Firing Deck x' listed in their abilities. Each time such a model is selected to shoot in the Shooting phase, you can select up to 'x' models embarked within it whose units have not already shot this phase. Then, for each of those embarked models, you can select one ranged weapon that embarked model is equipped with (excluding weapons with the [ONE SHOT] ability). Until that TRANSPORT model has resolved all of its attacks, it counts as being equipped with all of the weapons you selected in this way, in addition to its other weapons. Until the end of the phase, those selected models' units are not eligible to shoot. Firing Deck 'x': Each time this TRANSPORT shoots, select one weapon (excluding weapons with the [ONE SHOT] ability) from up to 'x' models embarked within it whose units have not shot this phase; this TRANSPORT counts as being equipped with those weapons as well. Until the end of the phase, those selected models' units are not eligible to shoot.

---

[6] Deployment Abilities ()
# Deployment Abilities — Scouts
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

SCOUTS Scouts form the vanguard of many armies. Unnoticed by the enemy, they range ahead of the main force. Some units have 'Scouts x"' listed in their abilities. If every model in a unit has this ability, then at the start of the first battle round, before the first turn begins, it can make a Normal move of up to x", with the exception that, while making that move, the distance moved by each model in that unit can be greater than that model's Move characteristic, as long as it is not greater than x". DEDICATED TRANSPORT models can make use of any Scouts x" ability listed in their abilities, or a Scouts x" ability that a unit that starts the battle embarked within that DEDICATED TRANSPORT model has (provided only models with this ability are embarked within that DEDICATED TRANSPORT model), regardless of how that embarked unit gained this ability (e.g. listed in their abilities, conferred by an Enhancement or by an attached CHARACTER, etc.). A unit that moves using this ability must end that move more than 9" horizontally away from all enemy models. If both players have units that can do this, the player who is taking the first turn moves their units first. Example: A unit has the Scouts 6" ability. At the start of the first battle round, the controlling player can make a Normal move with that unit of up to 6". Scouts x": Unit can make a Normal move of up to x" before the first turn begins. If embarked in a DEDICATED TRANSPORT, that DEDICATED TRANSPORT can make this move instead. Must end this move more than 9" horizontally away from all enemy models.

---

[7] Rhino (Space Marines)
# Rhino — Transport
**Unit:** Rhino  |  **Faction:** Space Marines

This model has a transport capacity of 12 ADEPTUS ASTARTES INFANTRY models. It cannot transport JUMP PACK, WULFEN, PHOBOS, GRAVIS, CENTURION, TERMINATOR or TACTICUS models (excluding TACTICUS CHARACTER models that began the battle attached to a non- TACTICUS unit).

---

[8] Terminator Squad (Space Marines)
# Terminator Squad — Wargear Options
**Unit:** Terminator Squad  |  **Faction:** Space Marines

- For every 5 models in this unit, 1 Terminator’s storm bolter can be replaced with one of the following: 1 assault cannon, 1 heavy flamer, 1 cyclone missile launcher and 1 storm bolter.*
- Any number of models can each have their power fist replaced with 1 chainfist.
- The Terminator Sergeant’s power fist can be replaced with 1 power weapon.
- * This model’s storm bolter cannot be replaced.
```
</details>


### qwen/qwen3-32b
`finish=stop · 410 compl tok · 1.3s`

[Ruling] No, a Terminator Squad cannot embark inside a Rhino transport.  
[Rule Citation] **Transport Capacity** (Rule 5) → **Rhino (Space Marines)** (Rule 7).  
[Reasoning] The Rhino’s transport capacity explicitly states it cannot transport **Terminator models** (Rule 7). While Rule 5 describes general transport rules, the specific exception in Rule 7 for Terminators takes precedence. The Terminator Squad is explicitly excluded from the Rhino’s allowed cargo, regardless of unit size or other conditions.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 89 compl tok · 0.6s`

[Ruling] → [Transport Capacity] → [Reasoning]

The Rhino transport has a transport capacity of 12 ADEPTUS ASTARTES INFANTRY models. The Terminator Squad is a unit of ADEPTUS ASTARTES INFANTRY models. However, the Rhino transport cannot transport TERMINATOR models, which the Terminator Squad is.

The provided rules do not clearly address this — I recommend checking the official GW FAQ.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 142 compl tok · 1.4s`

[Ruling] → The Rhino (Grey Knights) datasheet does not explicitly restrict the transport of Space Marine models; however, its transport capacity specifically mentions Grey Knights Infantry models. The Rhino (Space Marines) datasheet restricts transport of Terminator models.

→ [Rhino (Grey Knights)] → The Rhino (Grey Knights) has a transport capacity of 12 Grey Knights Infantry models and specifically cannot transport Terminator models.

→ [Rhino (Space Marines)] → The Rhino (Space Marines) has a transport capacity of 12 ADEPTUS ASTARTES INFANTRY models and specifically cannot transport TERMINATOR models.

The provided rules do not clearly address this — I recommend checking the official GW FAQ.

### openai/gpt-oss-120b
`finish=stop · 361 compl tok · 1.9s`

**Ruling:** A 5‑model Terminator Squad cannot embark inside a Rhino transport.

**Rule Citation:**  
- **Rhino (Space Marines) – Transport** – “This model has a transport capacity of 12 ADEPTUS ASTARTES INFANTRY models. It cannot transport … **TERMINATOR** … models” (Rule [7]).

**Reasoning:**  
The Rhino’s transport capacity is limited to ADEPTUS ASTARTES INFANTRY models, and the Rhino’s explicit restriction list includes “TERMINATOR” models. Since the Terminator Squad’s models have the Terminator keyword, they fall under the prohibited category. Therefore, they are not eligible to embark in the Rhino, regardless of the transport capacity number.

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=stop · 105 compl tok · 0.4s`

Based on the provided rules, a 5-model Terminator Squad can embark inside a Rhino transport.

[Ruling] → [Rule 7.10 - Transport Capacity] → [Rule 7.10 - Transport Capacity] → [Rule 7.10 - Transport Capacity]

The Terminator Squad can embark within the Rhino transport, as it has a transport capacity of 12 models and the Terminator Squad is smaller than that capacity.


====================================================================================================
## [35] ILLEGAL · mp=OFF · ctx 1877 tok

**Q:** Can I set up a unit using Deep Strike just 3 inches away from an enemy unit?

**Expected concepts (ground-truth anchors):** [['deep strike'], ['more than 9', '9"']]

<details><summary>rules context sent to every model</summary>

```
[1] Deployment Abilities ()
# Deployment Abilities — Deep Strike
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

DEEP STRIKE Some units make their way to battle via tunnelling, teleportation, high-altitude descent or other extraordinary means that allow them to appear suddenly in the thick of the fighting. During the Declare Battle Formations step, if every model in a unit has this ability, you can set it up in Reserves instead of setting it up on the battlefield. If you do, in the Reinforcements step of one of your Movement phases you can set up this unit anywhere on the battlefield that is more than 9" horizontally away from all enemy models. If a unit with the Deep Strike ability arrives from Strategic Reserves, the controlling player can choose for that unit to be set up either using the rules for Strategic Reserves or using the Deep Strike ability. Unit can be set up in Reserves instead of on the battlefield. Unit can be set up in your Reinforcements step, more than 9" horizontally away from all enemy models.

---

[2] Stratagems That Allow a Closer Set Up Range* ()
# Stratagems That Allow a Closer Set Up Range*
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a Stratagem has an effect that allows the targeted unit to be set up 'more than 3" horizontally away' from all enemy models/units (e.g. Cosmic Precision, Prognosticated Arrival, Denizens of the Warp, etc.), that part of that effect is changed to say 'more than 6" horizontally away'.

---

[3] Deployment Abilities ()
# Deployment Abilities — Infiltrators
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

INFILTRATORS Many armies employ reconnaissance units who can sit concealed, waiting for the right moment to strike. During deployment, if every model in a unit has this ability, then when you set it up, it can be set up anywhere on the battlefield that is more than 9" horizontally away from the enemy deployment zone and all enemy models.

---

[4] Setting Up Strategic Reserve Units ()
# Setting Up Strategic Reserve Units
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Where on the battlefield a Strategic Reserves unit can be set up when it arrives depends on the battle round, as follows:
- During the second battle round, Strategic Reserves units that arrive must be set up wholly within 6" of any battlefield edge, but no model in those units can be set up within the enemy deployment zone.
- Starting from the third battle round, Strategic Reserves units that arrive must be set up wholly within 6" of any battlefield edge.
In any case, Strategic Reserves units cannot be set up within 9" horizontally of any enemy models. All other rules that apply when setting up Reserves units also apply when setting up Strategic Reserves units.
During the second battle round, set up wholly within 6" of any battlefield edge (not in enemy deployment zone). From the third battle round onwards, set up wholly within 6" of any battlefield edge. Cannot be set up within 9" of any enemy models.

---

[5] Advance Moves ()
# Advance Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Advances, make an Advance roll for that unit by rolling one D6. Add the result in inches to the Move characteristic of each model in that unit until the end of the phase. Each model in that unit can then make an Advance move by moving a distance in inches less than or equal to this total, but no model can be moved within Engagement Range of enemy models. A unit cannot shoot or declare a charge in the same turn that it Advanced.
Advance Move: Models move up to M+D6". Cannot move within Engagement Range of any enemy models. Units that Advance cannot shoot or charge this turn.

---

[6] Big Guns Never Tire ()
# Big Guns Never Tire
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Monsters and war engines can dispense death from afar even as they trample the masses before them. MONSTER and VEHICLE units are eligible to shoot in their controlling player's Shooting phase even while they are within Engagement Range of one or more enemy units. Ranged weapons equipped by MONSTER and VEHICLE units can target one or more of the enemy units they are within Engagement Range of, even if other friendly units are also within Engagement Range of the same enemy unit. Each time a MONSTER or VEHICLE unit makes a ranged attack, if that unit was within Engagement Range of one or more enemy units when it selected its targets, unless that attack is made with a Pistol, subtract 1 from that attack's Hit roll. You can select an enemy MONSTER or VEHICLE unit within Engagement Range of one or more units from your army as a target of ranged weapons. Each time a model from your army makes a ranged attack against such a target, unless that attack is made with a Pistol, subtract 1 from that attack's Hit roll. Designer's Note: A unit that is within Engagement Range of an enemy MONSTER or VEHICLE unit is still not eligible to shoot, and so cannot make ranged attacks against that MONSTER or VEHICLE unit (unless that unit is eligible to shoot even while within Engagement Range of enemy units, e.g. it is itself a MONSTER or VEHICLE unit, or its models are equipped with Pistols). Other units from your army that are eligible to shoot can, however, target and shoot that enemy MONSTER or VEHICLE unit. MONSTERS and VEHICLES can shoot, and be shot at, even while they are within Engagement Range of enemy units. Each time a ranged attack is made by or against such a unit, subtract 1 from that attack's Hit roll (unless shooting with a Pistol).

---

[7] Engagement Range ()
# Engagement Range
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Engagement Range represents the zone of threat that models present to their enemies. While a model is within 1" horizontally and 5" vertically of an enemy model, those models - and their units - are within Engagement Range of each other. Models cannot be set up or end a Normal, Advance or Fall Back move within Engagement Range of any enemy models. If for any reason a model cannot meet this condition, that model is destroyed. Engagement Range: Within 1" horizontally and 5" vertically. Models cannot be set up or end a Normal, Advance or Fall Back move within Engagement Range of any enemy models.

---

[8] Pistol ()
# Pistol
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Pistols can be wielded even at point-blank range. Weapons with [PISTOL] in their profile are known as Pistols. If a unit contains any models equipped with Pistols, that unit is eligible to shoot in its controlling player's Shooting phase even while it is within Engagement Range of one or more enemy units. When such a unit is selected to shoot, it can only resolve attacks using its Pistols and can only target one of the enemy units it is within Engagement Range of. In such circumstances, a Pistol can target an enemy unit even if other friendly units are within Engagement Range of the same enemy unit. If a model is equipped with one or more Pistols, unless it is a MONSTER or VEHICLE model, it can either shoot with its Pistols or with all of its other ranged weapons. Declare whether such a model will shoot with its Pistols or its other ranged weapons before selecting targets. Can be shot even if the bearer's unit is within Engagement Range of enemy units, but must target one of those enemy units. Cannot be shot alongside any other non-Pistol weapon (except by a MONSTER or VEHICLE).
```
</details>


### qwen/qwen3-32b
`finish=stop · 506 compl tok · 1.5s`

[Ruling] No. A unit using Deep Strike must be set up more than 9" horizontally away from all enemy models.  
[Rule Citation] **Deployment Abilities — Deep Strike** [1]  
[Reasoning] The Deep Strike rule explicitly requires units to be set up "more than 9" horizontally away from all enemy models" during their Reinforcements step. No exception is provided in the cited rules to reduce this distance unless a specific stratagem (e.g., Cosmic Precision) modifies it, which is not mentioned here.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 173 compl tok · 0.7s`

[Ruling] → [Deployment Abilities — Deep Strike] → [Reasoning].

According to the Deep Strike ability, a unit can be set up more than 9" horizontally away from all enemy models. However, there is no restriction on setting up a unit less than 9" away from enemy models. 

Additionally, [Stratagems That Allow a Closer Set Up Range*] states that if a Stratagem allows a unit to be set up 'more than 3" horizontally away' from enemy models, that part of the effect is changed to 'more than 6" horizontally away'. However, this does not apply to the Deep Strike ability, as it does not mention a specific distance of 3" or 6".

Therefore, you can set up a unit using Deep Strike just 3 inches away from an enemy unit.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 112 compl tok · 0.9s`

No, you cannot set up a unit using Deep Strike just 3 inches away from an enemy unit. 

→ Deep Strike → [Wahapedia_Core_Rules, Core_Rules, Deployment Abilities ()] → According to the Deep Strike ability, a unit can be set up "anywhere on the battlefield that is more than 9" horizontally away from all enemy models." Since 3 inches is less than 9 inches, setting up a unit 3 inches away from an enemy unit would not meet the requirements of the Deep Strike ability.

### openai/gpt-oss-120b
`finish=stop · 487 compl tok · 1.4s`

**Ruling:** No. A unit with the Deep Strike deployment ability may only be set up more than 9 inches horizontally away from all enemy models; a 3‑inch distance does not satisfy that requirement.

**Rule Citation:** *Deployment Abilities — Deep Strike* (Wahapedia Core Rules) – “you can set it up … anywhere on the battlefield that is **more than 9" horizontally away from all enemy models**.”  

**Reasoning:**  
- The Deep Strike ability explicitly defines the minimum horizontal distance for the unit’s arrival as “more than 9 inches.”  
- The “Stratagems That Allow a Closer Set Up Range” rule only modifies the distance for **stratagems** that specify “more than 3 inches”; Deep Strike is not a stratagem, so its 9‑inch rule is unchanged.  
- Therefore a set‑up at 3 inches horizontally from an enemy model violates the Deep Strike requirement (and would also be within Engagement Range, which models cannot be set up in per the *Engagement Range* rule).  

Consequently, you cannot Deep Strike a unit only 3 inches away from an enemy unit.

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=stop · 132 compl tok · 0.4s`

Based on the provided rules, it is not explicitly stated that units set up using Deep Strike can be placed within 3" of an enemy unit. However, the unit must be more than 3" away from all enemy units. Therefore, the unit cannot be placed within 3" of any enemy unit. 


The provided rules do not clearly address the question of placing a unit within 3" of an enemy unit. I recommend checking the official Warhammer 40k 10th Edition datasheets or the relevant unit's datasheet for specific rules regarding Deep Strike and Engagement Range.


====================================================================================================
## [36] ILLEGAL · mp=OFF · ctx 3033 tok

**Q:** My unit Fell Back this turn — can that same unit then declare a charge this turn?

**Expected concepts (ground-truth anchors):** [['fall back', 'fell back'], ['declare a charge', 'cannot shoot or declare']]

<details><summary>rules context sent to every model</summary>

```
[1] Fall Back Moves ()
# Fall Back Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Falls Back, each model in that unit can make a Fall Back move by moving a distance in inches less than or equal to its Move characteristic, and when doing so you can move it within Engagement Range of enemy models, provided it does not end that move within Engagement Range of any enemy models - if this is not possible, that unit cannot Fall Back. A unit cannot shoot or declare a charge in the same turn that it Fell Back. Desperate Escape Tests Unlike when making other types of move, models can move over enemy models when making a Fall Back move as if those enemy models were not there, but you must take a Desperate Escape test for each model that will do so (excluding models that are TITANIC or can FLY) before any models in that unit are moved. In addition, if a unit is Battle-shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved. Each time you take a Desperate Escape test for a model, roll one D6. For each roll of 1-2, one model from the unit that is Falling Back is destroyed (selected by you). The same model can only ever trigger one Desperate Escape test per phase. Fall Back Move: Models move up to M". Units that Fall Back cannot shoot or declare a charge in the same turn. Models can move over enemy models when Falling Back, but you must take Desperate Escape tests for them before they do so (excluding models that are TITANIC or can FLY). If a Battle-shocked unit is selected to Fall Back, take a Desperate Escape test for every model in that unit. Desperate Escape Test: Roll one D6. On a 1-2, one model from that unit is destroyed. A The Sternguard Veterans are selected to make a Fall Back move, but to do so they must move through enemy models, so Desperate Escape tests are required. B The controlling player rolls one D6 for each model that moves through an enemy unit, resulting in a 1, 2, 4, 4 and 6. Two models are therefore destroyed.

---

[2] CHARGE PHASE ()
# CHARGE PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Use the following sequence to charge with your units.
1. SELECT ELIGIBLE UNIT
2. SELECT TARGETS
3. MAKE CHARGE ROLL
4. MAKE CHARGE MOVE
5. REPEAT FOR NEXT ELIGIBLE UNIT
In your Charge phase, if you have any eligible units from your army on the battlefield that you want to charge into close combat, you can select those units, one at a time, to declare a charge. Each can only be selected once per phase. Once all of these charges (if any) have been resolved, progress to the Fight phase. A unit is eligible to charge if it is within 12" of one or more enemy units in your Charge phase, unless any of the following apply:
- That unit Advanced or Fell Back this turn.
- That unit is within Engagement Range of any enemy models.
- That unit is an AIRCRAFT unit.
Warriors hurl themselves into battle to slay with blade, hammer and claw. Strident war cries and frantic screams echo through the whirling smoke as the moment of cataclysmic violence draws near.

---

[3] Disembark ()
# Disembark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit from your army starts your Movement phase embarked within a TRANSPORT model, that unit can disembark in that phase. When a unit disembarks from a TRANSPORT model, set it up on the battlefield so that it is wholly within 3" of that TRANSPORT model and not within Engagement Range of any enemy models. If, for any reason, a disembarking model cannot be set up, that model's unit cannot disembark. Units that disembark from a TRANSPORT model that either Remained Stationary this phase or has not yet made a Normal, Advance or Fall Back move this phase can then act normally (make a Normal move, Advance, shoot, declare a charge, fight, etc.) in the remainder of the turn. Such a disembarking unit cannot choose to Remain Stationary. Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; they cannot move further during this phase. Such a unit also cannot declare a charge in the same turn, but can otherwise act normally in the remainder of the turn. Units cannot disembark from a TRANSPORT model that either Advanced or Fell Back this turn. Units that start your Movement phase embarked within a TRANSPORT can disembark this phase, provided their TRANSPORT has not Advanced or Fallen Back. If a unit disembarks before its TRANSPORT moves, it can act normally. If a unit disembarks after its TRANSPORT moves, it cannot move or charge this turn, but can otherwise act normally. Disembarking units must be set up wholly within 3" of their TRANSPORT and not within Engagement Range of any enemy models (or the unit cannot disembark). Units that disembark this turn cannot Remain Stationary.

---

[4] Charging with a Unit ()
# Charging with a Unit
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Once you have selected an eligible unit to declare a charge, you must select one or more enemy units within 12" of it as the targets of that charge. The targets of a charge do not need to be visible to the charging unit. You then make a Charge roll for the charging unit by rolling 2D6. The result is the maximum number of inches each model in that unit can be moved if a Charge move is possible. For a Charge move to be possible, the Charge roll must be sufficient to enable the charging unit to end that move:
- Within Engagement Range of every unit that you selected as a target of the charge.
- Without moving within Engagement Range of any enemy units that were not a target of the charge.
- In Unit Coherency.
If any of these conditions cannot be met, the charge fails and no models in the charging unit move this phase. Otherwise, the charge is successful and the models in the charging unit make a Charge move - move each model a distance in inches up to the result of the Charge roll. When doing so, each model in the charging unit must end its Charge move closer to one of the units selected as a target of its charge. If you can also move a charging model so that it ends its Charge move in base-to-base contact with one or more enemy models while still enabling the charging unit to end its move satisfying all of the conditions above, you must do so. The controlling player chooses the order in which to move their models.
Charge Roll: 2D6". Targets of a charge must be within 12" but do not need to be visible. If the distance rolled is insufficient to move within Engagement Range of all targets while maintaining Unit Coherency, the charge fails. Cannot move within Engagement Range of any unit that was not a target of the charge. If the charge is successful, each model makes a Charge move less than or equal to the Charge roll, and must move into base-to-base contact with an enemy model if possible.

---

[5] Engagement Range ()
# Engagement Range
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Engagement Range represents the zone of threat that models present to their enemies. While a model is within 1" horizontally and 5" vertically of an enemy model, those models - and their units - are within Engagement Range of each other. Models cannot be set up or end a Normal, Advance or Fall Back move within Engagement Range of any enemy models. If for any reason a model cannot meet this condition, that model is destroyed. Engagement Range: Within 1" horizontally and 5" vertically. Models cannot be set up or end a Normal, Advance or Fall Back move within Engagement Range of any enemy models.

---

[6] Charge Bonus ()
# Charge Bonus
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Many warriors thunder headlong into combat, using the impetus of their charge to bring swift death to their foes. Each time a unit makes a Charge move, until the end of the turn, that unit has the Fights First ability.

---

[7] Destroyed Transports ()
# Des
```
</details>


### qwen/qwen3-32b
`finish=stop · 367 compl tok · 1.2s`

[Ruling] No, a unit that Fell Back this turn cannot declare a charge in the same turn.  
[Rule Citation] **Fall Back Moves** (Core Rules) and **Charge Phase** (Core Rules).  
[Reasoning]  
1. **Fall Back Moves** explicitly states: "A unit cannot shoot or declare a charge in the same turn that it Fell Back."  
2. **Charge Phase** confirms that a unit is *not eligible* to charge if it "Advanced or Fell Back this turn."  

These rules directly prohibit the unit from declaring a charge after Falling Back in the same turn.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 80 compl tok · 0.6s`

[Ruling] → [Rule Citation] → [Reasoning]
No, a unit that Fell Back this turn cannot declare a charge this turn. → [2] CHARGE PHASE → A unit is eligible to charge if it is within 12" of one or more enemy units in your Charge phase, unless any of the following apply: - That unit Advanced or Fell Back this turn.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 117 compl tok · 1.6s`

[Ruling] → A unit that Fell Back this turn cannot declare a charge in the same turn. 
→ [CHARGE PHASE] → [Reasoning]: According to the CHARGE PHASE rule, a unit is eligible to charge if it is within 12" of one or more enemy units in your Charge phase, unless it Advanced or Fell Back this turn. Since your unit Fell Back this turn, it is not eligible to declare a charge. Additionally, the Fall Back Moves rule states that a unit cannot shoot or declare a charge in the same turn that it Fell Back.

### openai/gpt-oss-120b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01kkppm

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=error · ? compl tok · ?s` ⚠ ERROR: Error code: 413 - {'error': {'message': 'Request too large for model `allam-2-7b` in organization `org_01kkppmxccfd1r98zztyme6k5a` service tier `on_demand` on tokens per minute (TPM): Limit 6000, Requ


====================================================================================================
## [37] ILLEGAL · mp=OFF · ctx 1856 tok

**Q:** Can my Space Marine unit embark inside an enemy Ork Trukk?

**Expected concepts (ground-truth anchors):** [['embark'], ['friendly']]

<details><summary>rules context sent to every model</summary>

```
[1] Imperial Space Marine (Space Marines)
# Ability: Oath of Moment
**Unit:** Imperial Space Marine  |  **Faction:** Space Marines

If your Army Faction is ADEPTUS ASTARTES, at the start of your Command phase, select one unit from your opponent’s army. Until the start of your next Command phase, that enemy unit is your Oath of Moment target. Each time a model with this ability makes an attack that targets your Oath of Moment target: You can re-roll the Hit roll., If you are using a Codex: Space Marines Detachment and your army does not include one or more units with the Black Templars, Blood Angels, Dark Angels, Deathwatch or Space Wolves keywords, add 1 to the Wound roll as well.

---

[2] Trukk (Orks)
# Trukk — Wargear Options
**Unit:** Trukk  |  **Faction:** Orks

- This model can be equipped with 1 wreckin’ ball.

---

[3] Embark ()
# Embark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit makes a Normal, Advance or Fall Back move, and every model in that unit ends that move within 3" of a friendly TRANSPORT model, they can embark within it. A unit cannot embark if it has already disembarked from a TRANSPORT model in the same phase. Remove the unit from the battlefield and place it to one side - it is now embarked within that TRANSPORT model. Unless otherwise stated, units cannot do anything or be affected in any way while they are embarked. A unit can embark within a friendly TRANSPORT if all of its models end a Normal, Advance or Fall Back move within 3" of that TRANSPORT. A unit cannot embark and disembark in the same phase.

---

[4] Deployment Abilities ()
# Deployment Abilities — Infiltrators
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

INFILTRATORS Many armies employ reconnaissance units who can sit concealed, waiting for the right moment to strike. During deployment, if every model in a unit has this ability, then when you set it up, it can be set up anywhere on the battlefield that is more than 9" horizontally away from the enemy deployment zone and all enemy models.

---

[5] Disembark ()
# Disembark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit from your army starts your Movement phase embarked within a TRANSPORT model, that unit can disembark in that phase. When a unit disembarks from a TRANSPORT model, set it up on the battlefield so that it is wholly within 3" of that TRANSPORT model and not within Engagement Range of any enemy models. If, for any reason, a disembarking model cannot be set up, that model's unit cannot disembark. Units that disembark from a TRANSPORT model that either Remained Stationary this phase or has not yet made a Normal, Advance or Fall Back move this phase can then act normally (make a Normal move, Advance, shoot, declare a charge, fight, etc.) in the remainder of the turn. Such a disembarking unit cannot choose to Remain Stationary. Units that disembark from a TRANSPORT model that made a Normal move this phase count as having made a Normal move themselves; they cannot move further during this phase. Such a unit also cannot declare a charge in the same turn, but can otherwise act normally in the remainder of the turn. Units cannot disembark from a TRANSPORT model that either Advanced or Fell Back this turn. Units that start your Movement phase embarked within a TRANSPORT can disembark this phase, provided their TRANSPORT has not Advanced or Fallen Back. If a unit disembarks before its TRANSPORT moves, it can act normally. If a unit disembarks after its TRANSPORT moves, it cannot move or charge this turn, but can otherwise act normally. Disembarking units must be set up wholly within 3" of their TRANSPORT and not within Engagement Range of any enemy models (or the unit cannot disembark). Units that disembark this turn cannot Remain Stationary.

---

[6] Ruins ()
# Ruins
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

The galaxy is littered with the shattered remains of once-proud cities, and countless troops have sought shelter from enemy bombardment within their husks. FOOTPRINT When this terrain feature is set up on the battlefield, both players must agree upon its footprint - that is, the boundary of the terrain feature at ground level. This is so that players know when a model is wholly within this terrain feature. If this terrain feature is mounted on a base, then this will define its footprint. PLUNGING FIRE Each time a model that is wholly within this terrain feature makes a ranged attack, if that model is 6" or more vertically from ground level, and every model in the target unit is at ground level, improve the Armour Penetration characteristic of that attack by 1. MOVEMENT INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, and BEAST models can move through this terrain feature (walls, floors, ceilings, gantries, chains, etc.) as if it were not there. A model cannot end a move within a wall, a floor, etc. INFANTRY, IMPERIUM PRIMARCH, BELISARIUS CAWL, BEASTS and FLY models can be set up or end a move on any floor level of this terrain feature, but if that level is not the ground floor, such models can only do so if their base does not overhang the floor at that level (if a model does not have a base, no part of that model that would be in contact with the battlefield at ground level can overhang that floor). All other models can only be set up or end a move on the ground floor of this terrain feature. VISIBILITY Models cannot see over or through this terrain feature (i.e. a unit outside this terrain feature cannot draw line of sight to a target on the other side of it, even if it would be possible to draw line of sight to that target through open windows, doors, etc.) AIRCRAFT models are exceptions to this - visibility to and from such models is determined normally, even if this terrain feature is wholly in between them and the observing model. Models can see into this terrain feature normally, and models that are wholly within this terrain feature can see out of it normally. Models that are within this terrain feature can be seen normally and TOWERING models that are within this terrain feature can also see out of it normally. BENEFIT OF COVER Each time a ranged attack is allocated to a model, if that model is either wholly within this terrain feature, or it is not fully visible to every model in the attacking unit because of this terrain feature, that model has the Benefit of Cover against that attack. KEYWORDS: AREA TERRAIN, RUINS

---

[7] Trukk (Orks)
# Trukk — Transport
**Unit:** Trukk  |  **Faction:** Orks

This model has a transport capacity of 12 Orks Infantry models. Each Mega Armour model takes up the space of 2 models. It cannot transport Jump Pack or Ghazghkull Thraka models.

---

[8] RAPID EMBARKATION (Space Marines)
# Stratagem: RAPID EMBARKATION
**Faction:** Space Marines  |  **Type:** Armoured Speartip – Wargear Stratagem  |  **Cost:** 1 CP
**Detachment:** Armoured Speartip
**When:** Either player’s turn — Fight phase
*With steely discipline, Space Marine battle-brothers mount up swiftly, even as the enemy closes in.*

WHEN: End of the Fight phase. TARGET: One Adeptus Astartes Infantry unit from your army that is not within Engagement Range of one or more enemy units, and one friendly Heavy Transport it is able to embark within. EFFECT: If your ADEPTUS ASTARTES INFANTRY unit is wholly within 6" of that HEAVY TRANSPORT, it can embark within it.

```
</details>


### qwen/qwen3-32b
`finish=stop · 396 compl tok · 1.1s`

[**Ruling**] No, your Space Marine unit cannot embark inside an enemy Ork Trukk.  
[**Rule Citation**] **Embark (Core Rules)** → [3]  
[**Reasoning**] The "Embark" rule explicitly requires the unit to embark within a **friendly** TRANSPORT model. Enemy units, including Ork Trukks, are not considered "friendly" for this purpose. Additionally, the Trukk’s transport rules (rule [7]) only specify capacity for Ork models, and no rule in the provided context allows embarking in enemy transports.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 29 compl tok · 1.3s`

[Ruling] → Embark → [Reasoning]

The provided rules do not clearly address this — I recommend checking the official GW FAQ.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 168 compl tok · 0.9s`

Illegal premise → The provided rules do not clearly indicate that a Space Marine unit can embark in an enemy Trukk; however, based on the standard Core Rules, units can only embark in friendly TRANSPORT models. 

[Ruling] → No.
→ [Embark] → A unit can embark within a friendly TRANSPORT if all of its models end a Normal, Advance or Fall Back move within 3" of that TRANSPORT.
→ [Reasoning] The rules provided do not indicate that a unit can embark in an enemy TRANSPORT model. The Embark rule explicitly states that a unit can embark within a "friendly TRANSPORT model". The Space Marines and Orks are different factions, so the Ork Trukk would not be considered friendly to the Space Marine unit. Therefore, the Space Marine unit cannot embark inside the enemy Ork Trukk.

### openai/gpt-oss-120b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01kkppm

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=stop · 1526 compl tok · 1.4s`

The provided rules do not explicitly mention Ork Trukk, so I cannot definitively answer your question. However, based on the context, it seems that Space Marine units can embark within friendly Heavy Transports, as long as they are wholly within 6" of the Heavy Transport. 


---


---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---


====================================================================================================
## [38] ILLEGAL · mp=OFF · ctx 2586 tok

**Q:** Can a single model in my 10-model unit end its move 4 inches away from every other model in that unit?

**Expected concepts (ground-truth anchors):** [['coherency'], ['within 2', '2"']]

<details><summary>rules context sent to every model</summary>

```
[1] Unit Coherency ()
# Unit Coherency
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

A unit that contains more than one model must be set up and end any kind of move as a single group, with all of its models within 2" horizontally and 5" vertically of at least one other model from that unit. While a unit has seven or more models, all of its models must instead be set up and end any kind of move within 2" horizontally and 5" vertically of at least two other models from that unit. This is called Unit Coherency. If for any reason a model cannot be set up in Unit Coherency, or cannot be set up following any restrictions stated by other rules (e.g. while setting up using the Deep Strike ability), that unit cannot be set up. If a unit cannot end a move in Unit Coherency, it cannot make that move and its models are returned to their previous positions. At the end of every turn, each player must remove models, one at a time, from any of the units from their armies that are no longer in Unit Coherency, until only a single group of models from each of those units remains in play and in Unit Coherency. Models removed in this way count as having been destroyed, but they never trigger any rules that apply when a model is destroyed. Unit Coherency: Within 2" horizontally and 5" vertically of: One other model from the same unit (in units of 2-6 models). Two other models from the same unit (in units of 7+ models). At the end of every turn, if a unit is not in Unit Coherency, the controlling player must remove models until that unit is in Unit Coherency again. A Each model in this Sternguard Veterans unit of five models is within 2" of at least one other model in the unit. This unit is therefore in Unit Coherency. B Each model in this Termagants unit of ten models is within 2" of at least two other models in the unit. This unit is therefore also in Unit Coherency.

---

[2] Normal Moves ()
# Normal Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit makes a Normal move, each model in that unit can move a distance in inches less than or equal to its Move (M) characteristic, but no model can be moved within Engagement Range of any enemy models. A unit cannot make more than one Normal move per phase. Normal Move: Models move up to M". Cannot move within Engagement Range of any enemy models.

---

[3] Embark ()
# Embark
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If a unit makes a Normal, Advance or Fall Back move, and every model in that unit ends that move within 3" of a friendly TRANSPORT model, they can embark within it. A unit cannot embark if it has already disembarked from a TRANSPORT model in the same phase. Remove the unit from the battlefield and place it to one side - it is now embarked within that TRANSPORT model. Unless otherwise stated, units cannot do anything or be affected in any way while they are embarked. A unit can embark within a friendly TRANSPORT if all of its models end a Normal, Advance or Fall Back move within 3" of that TRANSPORT. A unit cannot embark and disembark in the same phase.

---

[4] Aircraft and the Movement of Other Models ()
# Aircraft and the Movement of Other Models
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit is selected to move in the Movement phase, if the only enemy models that are within Engagement Range of that unit are AIRCRAFT models, then that unit can still make a Normal or Advance move. Whenever a model makes any kind of move, it can be moved over enemy AIRCRAFT models as if they were not there, and can be moved within Engagement Range of enemy AIRCRAFT models, but it cannot end that move on top of another model or within Engagement Range of any enemy AIRCRAFT models.
Units can still make a Normal or Advance move if they are only within Engagement Range of enemy AIRCRAFT. Models can move within Engagement Range of enemy AIRCRAFT, but cannot end a move within Engagement Range of enemy AIRCRAFT. Models can move over AIRCRAFT when they make any kind of move.

---

[5] Advance Moves ()
# Advance Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Advances, make an Advance roll for that unit by rolling one D6. Add the result in inches to the Move characteristic of each model in that unit until the end of the phase. Each model in that unit can then make an Advance move by moving a distance in inches less than or equal to this total, but no model can be moved within Engagement Range of enemy models. A unit cannot shoot or declare a charge in the same turn that it Advanced.
Advance Move: Models move up to M+D6". Cannot move within Engagement Range of any enemy models. Units that Advance cannot shoot or charge this turn.

---

[6] 1. Pile In ()
# 1. Pile In
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Piles In, you can move each model in that unit that is not already in base-to-base contact with an enemy model up to 3" - this is a Pile-in move. For a Pile In to be possible, a unit must be able to end these moves within Engagement Range of one or more enemy units and in Unit Coherency. If these conditions cannot be met, no models in the unit can make Pile-in moves this phase and you progress to making melee attacks with that unit. Otherwise, the unit can make Pile-in moves. Each time a model makes a Pile-in move, it must end that move closer to the closest enemy model. If it can also end that move in base-to-base contact with one or more enemy models while still satisfying all of the conditions above, it must do so. The controlling player chooses the order in which to move their models.
Pile-in Move: Up to 3". Every model that moves must end closer to the closest enemy model, and in base-to-base contact with an enemy model if possible. The unit must end in Unit Coherency and within Engagement Range of at least one enemy unit (or no models can Pile In).

---

[7] Fall Back Moves ()
# Fall Back Moves
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

When a unit Falls Back, each model in that unit can make a Fall Back move by moving a distance in inches less than or equal to its Move characteristic, and when doing so you can move it within Engagement Range of enemy models, provided it does not end that move within Engagement Range of any enemy models - if this is not possible, that unit cannot Fall Back. A unit cannot shoot or declare a charge in the same turn that it Fell Back. Desperate Escape Tests Unlike when making other types of move, models can move over enemy models when making a Fall Back move as if those enemy models were not there, but you must take a Desperate Escape test for each model that will do so (excluding models that are TITANIC or can FLY) before any models in that unit are moved. In addition, if a unit is Battle-shocked when it is selected to Fall Back, you must take a Desperate Escape test for every model in that unit before any are moved. Each time you take a Desperate Escape test for a model, roll one D6. For each roll of 1-2, one model from the unit that is Falling Back is destroyed (selected by you). The same model can only ever trigger one Desperate Escape test per phase. Fall Back Move: Models move up to M". Units that Fall Back cannot shoot or declare a charge in the same turn. Models can move over enemy models when Falling Back, but you must take Desperate Escape tests for them before they do so (excluding models that are TITANIC or can FLY). If a Battle-shocked unit is selected to Fall Back, take a Desperate Escape test for every model in that unit. Desperate Escape Test: Roll one D6. On a 1-2, one model from that unit is destroyed. A The Sternguard Veterans are selected to make a Fall Back move, but to do so they must move through enemy models, so Desperate Escape tests are required. B The controlling player rolls one D6 for each model that moves through an enemy unit, resulting in a 1, 2, 4, 4 and 6. Two models are therefore destro
```
</details>


### qwen/qwen3-32b
`finish=stop · 448 compl tok · 1.3s`

[Ruling] No. A unit of 10 models must adhere to Unit Coherency rules, requiring each model to be within 2" horizontally of at least two other models from the same unit. If a single model ends its move 4" away from all others, the unit fails Unit Coherency. At the end of the turn, the controlling player must remove models (including this isolated one) until the unit is in coherency.  
[Rule Citation] Unit Coherency (Core Rules) → "While a unit has seven or more models, all of its models must [...] be within 2" horizontally [...] of at least two other models from that unit."  
[Reasoning] The isolated model violates the 2" horizontal requirement for units of 7+ models. Failure to meet coherency triggers the removal of models until compliance is achieved.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 134 compl tok · 0.7s`

[Ruling] → [Unit Coherency] → [Reasoning]

According to Unit Coherency, a unit with 7 or more models must be set up and end any kind of move within 2" horizontally and 5" vertically of at least two other models from that unit. Since your unit has 10 models, it falls under this category.

A single model in your 10-model unit cannot end its move 4 inches away from every other model in that unit, as this would not meet the Unit Coherency requirement of being within 2" horizontally and 5" vertically of at least two other models from the same unit.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 137 compl tok · 1.1s`

[Ruling] → A unit with 7 or more models must be within 2" horizontally and 5" vertically of at least two other models from the same unit to be in Unit Coherency.

→ [Unit Coherency] → A single model cannot end its move 4 inches away from every other model in a 10-model unit because it would not be within 2" horizontally and 5" vertically of at least two other models from the same unit.

The provided rules do not explicitly state what happens if only one model is out of coherency but imply removal of models to achieve coherency; ensure to verify with official GW FAQ for comprehensive guidance.

### openai/gpt-oss-120b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01kkppm

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=stop · 820 compl tok · 0.9s`
























































































































































































































































































































































































































































































































































































































































































































































































































































====================================================================================================
## [39] ARMY_DETACHMENT · mp=OFF · ctx 2681 tok

**Q:** What does the Space Marines army rule Oath of Moment do, and when do I pick the target?

**Expected concepts (ground-truth anchors):** [['oath of moment'], ['re-roll'], ['command phase']]

<details><summary>rules context sent to every model</summary>

```
[1] Imperial Space Marine (Space Marines)
# Ability: Oath of Moment
**Unit:** Imperial Space Marine  |  **Faction:** Space Marines

If your Army Faction is ADEPTUS ASTARTES, at the start of your Command phase, select one unit from your opponent’s army. Until the start of your next Command phase, that enemy unit is your Oath of Moment target. Each time a model with this ability makes an attack that targets your Oath of Moment target: You can re-roll the Hit roll., If you are using a Codex: Space Marines Detachment and your army does not include one or more units with the Black Templars, Blood Angels, Dark Angels, Deathwatch or Space Wolves keywords, add 1 to the Wound roll as well.

---

[2] Oath of Moment (World Eaters, Chaos Space Marines, Space Marines, Thousand Sons, Death Guard)
# Army Rule: Oath of Moment
**Faction:** World Eaters, Chaos Space Marines, Space Marines, Thousand Sons, Death Guard  |  **Type:** Army Rule
*In battle, Space Marines swear mighty oaths to destroy the enemies of the Emperor and uphold the honour of their Chapter, and such vows are sacrosanct. When the Angels of Death strike, they do so with the precision of a surgeon and the force of a thunderbolt. Experience and strategic expertise help them to read the shifting shape of the battle with post-human speed and clarity, directing their wrath towards one priority target after another. Command assets are annihilated, leaving the enemy reeling leaderless. Heavy armour, potent artillery and the vaunted elites of the foe’s forces are laid waste with horrifying speed, until the Emperor’s Angels of Death stand victorious over a field of smouldering wreckage and bolt-riddled corpses, and honour is finally satisfied.*

If your Army Faction is ADEPTUS ASTARTES, at the start of your Command phase, select one unit from your opponent’s army. Until the start of your next Command phase, that enemy unit is your Oath of Moment target. Each time a model with this ability makes an attack that targets your Oath of Moment target: You can re-roll the Hit roll., If you are using a Codex: Space Marines Detachment and your army does not include one or more units with the Black Templars, Blood Angels, Dark Angels, Deathwatch or Space Wolves keywords, add 1 to the Wound roll as well.


---

[3] Deployment Abilities ()
# Deployment Abilities — Infiltrators
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

INFILTRATORS Many armies employ reconnaissance units who can sit concealed, waiting for the right moment to strike. During deployment, if every model in a unit has this ability, then when you set it up, it can be set up anywhere on the battlefield that is more than 9" horizontally away from the enemy deployment zone and all enemy models.

---

[4] Read Mission Objectives ()
# Read Mission Objectives
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Each mission will state what its primary objectives are, and may also include one or more special rules. These cover unique situations, or abilities that can be used in the battle.

---

[5] SHOOTING PHASE ()
# SHOOTING PHASE
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Use the following sequence when a unit shoots.
1. SELECT ELIGIBLE UNIT
2. SELECT TARGETS
3. MAKE RANGED ATTACKS
4. REPEAT FOR NEXT ELIGIBLE UNIT
In your Shooting phase, if you have one or more eligible units from your army on the battlefield, you can select those units, one at a time, and shoot with them. Each unit can only be selected to shoot once per phase. Once all of the units you selected have shot, progress to your Charge phase. A unit is eligible to shoot unless any of the following apply:
- That unit Advanced this turn.
- That unit Fell Back this turn.
Unless at least one model in a unit has an eligible target for one or more of its ranged weapons, that model's unit cannot be selected to shoot. Designer's Note: This doesn't change the unit's eligibility to shoot, but it does mean that a unit can't be selected to shoot at nothing, and therefore won't qualify for other rules triggers (e.g. GARGOYLES ' Winged Swarm ability and Dark Pacts)
Guns thunder and shrapnel flies through the air. Bursts of muzzle flare and beams of las-fire illuminate the fog of war, and spent ammunition cartridges litter the battlefield.

---

[6] Imperial Space Marine (Space Marines)
# Imperial Space Marine
**Faction:** Space Marines  |  **Role:** Characters  |  **Source:** 000000356
**Version/Errata Date:** 01.01.0001 0:00:00 *(errata)*

## Stats
| Model | M | T | Sv | Inv | W | Ld | OC | Base |
|---|---|---|---|---|---|---|---|---|
| Imperial Space Marine | 6" | 4 | 3+ | - | 4 | 6+ | 1 | 32mm |

## Unit Composition
- 1 Imperial Space Marine

## Points Costs
- 1 model: **40 pts**

## Wargear
| Weapon | Range | Type | A | BS/WS | S | AP | D |
|---|---|---|---|---|---|---|---|
| Disintegration combi-gun | 24 | Ranged | 1 | 4 | 5 | -1 | 1 |
|   | *anti-infantry 4+, devastating wounds, rapid fire 1* | | | | | | |
| Disintegration pistol | 12 | Ranged | 1 | 3 | 5 | -1 | 1 |
|   | *anti-infantry 4+, devastating wounds, pistol* | | | | | | |
| Close combat weapon | Melee | Melee | 4 | 3 | 4 | 0 | 1 |

## Wargear Options
- —

## Datasheet Abilities
**Swift Assault**
> While this model is leading a unit, ranged weapons equipped by models in that unit have the [ASSAULT] ability.

**Unbreakable Duty**
> While this model is within range of an objective marker and/or within 6" of the centre of the battlefield, this model has the Feel No Pain 4+ ability.

## Faction Abilities
**Oath of Moment**
> If your Army Faction is ADEPTUS ASTARTES, at the start of your Command phase, select one unit from your opponent’s army. Until the start of your next Command phase, that enemy unit is your Oath of Moment target. Each time a model with this ability makes an attack that targets your Oath of Moment target: You can re-roll the Hit roll., If you are using a Codex: Space Marines Detachment and your army does not include one or more units with the Black Templars, Blood Angels, Dark Angels, Deathwatch or Space Wolves keywords, add 1 to the Wound roll as well.

## Core Abilities
**Leader**
> LEADER Mighty heroes fight at the forefront of battle. Some CHARACTER units have ‘Leader’ listed on their datasheets. Such CHARACTER units are known as Leaders, and the units they can lead – known as their Bodyguard units – are listed on their datasheet. During the Declare Battle Formations step, for each Leader in your army, if your army also includes one or more of that Leader’s Bodyguard units, you can select one of those Bodyguard units. That Leader will then attach to that Bodyguard unit for the duration of the battle and is said to be leading that unit. Each Bodyguard unit can only have one Leader attached to it. While a Bodyguard unit contains a Leader, it is known as an Attached unit and, with the exception of rules that are triggered when units are destroyed, it is treated as a single unit for all rules purposes. Each time an attack targets an Attached unit, until the attacking unit has resolved all of its attacks, you must use the Toughness characteristic of the Bodyguard models in that unit, even if a Leader in that unit has a different Toughness characteristic. Each time an attack sucessfully wounds an Attached unit, that attack cannot be allocated to a CHARACTER model in that unit, even if that CHARACTER model has lost one or more wounds or has already had attacks allocated to it this phase. As soon as the last Bodyguard model in an Attached unit has been destroyed, any attacks made against that unit that have yet to be allocated can then be allocated to CHARACTER models in that unit. Each time the last model in a Bodyguard unit is destroyed, each CHARACTER unit that is part of that Attached unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit 
```
</details>


### qwen/qwen3-32b
`finish=stop · 578 compl tok · 1.7s`

[Ruling] The **Oath of Moment** army rule allows an Adeptus Astartes army to select one enemy unit as their Oath of Moment target at the start of their Command phase. This target remains until the start of the army’s next Command phase. While active, attacks made by models with the Oath of Moment ability that target this unit allow the attacker to re-roll Hit rolls. If the army uses a *Codex: Space Marines* Detachment and does not include units with the Black Templars, Blood Angels, Dark Angels, Deathwatch, or Space Wolves keywords, Wound rolls for these attacks are also re-rolled.  

[Rule Citation] **Oath of Moment (Army Rule)** → [2]  
[Reasoning] The rule explicitly states the timing ("at the start of your Command phase") and effects ("re-roll the Hit roll" and conditional "add 1 to the Wound roll") in the provided context. The detachment-specific enhancements (e.g., *Sacred Oath*, *Calculated Annihilation*) are not required for this base ruling.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 108 compl tok · 0.5s`

[Ruling] → [Oath of Moment (Army Rule)] → [Reasoning]

According to the Oath of Moment (Army Rule) in [2], when the Space Marines army faction is ADEPTUS ASTARTES, at the start of your Command phase, you select one unit from your opponent's army as your Oath of Moment target. Until the start of your next Command phase, that enemy unit is your Oath of Moment target.

So, you pick the target at the start of your Command phase.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 105 compl tok · 1.1s`

Oath of Moment → [2] Oath of Moment (World Eaters, Chaos Space Marines, Space Marines, Thousand Sons, Death Guard) → The Oath of Moment army rule states: 'If your Army Faction is ADEPTUS ASTARTES, at the start of your Command phase, select one unit from your opponent’s army. Until the start of your next Command phase, that enemy unit is your Oath of Moment target.' 

You pick the target at the start of your Command phase.

### openai/gpt-oss-120b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01kkppm

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=error · ? compl tok · ?s` ⚠ ERROR: Error code: 413 - {'error': {'message': 'Request too large for model `allam-2-7b` in organization `org_01kkppmxccfd1r98zztyme6k5a` service tier `on_demand` on tokens per minute (TPM): Limit 6000, Requ


====================================================================================================
## [40] ARMY_DETACHMENT · mp=OFF · ctx 2972 tok

**Q:** What is the Ironstorm Spearhead detachment rule Armoured Wrath, and what can each Adeptus Astartes unit re-roll?

**Expected concepts (ground-truth anchors):** [['armoured wrath'], ['ironstorm spearhead'], ['re-roll one hit roll', 're-roll']]

<details><summary>rules context sent to every model</summary>

```
[1] Armoured Wrath (Space Marines)
# Detachment Rule: Armoured Wrath
**Faction:** Space Marines  |  **Type:** Detachment Rule  |  **Detachment:** Ironstorm Spearhead
*An Ironstorm Spearhead’s commanders guide their assault with pre-cogitated fire solutions, cycling data-gheist inloads and whispered binharic auguries. These ensure their warriors, and the belligerent machine spirits inhabiting their war engines, deliver their fire with inescapable accuracy.*

Once per phase for each ADEPTUS ASTARTES unit in your army, you can re-roll one Hit roll, one Wound roll or one Damage roll made for a model in that unit.


---

[2] Deployment Abilities ()
# Deployment Abilities — Leader
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

LEADER Mighty heroes fight at the forefront of battle. Some CHARACTER units have 'Leader' listed on their datasheets. Such CHARACTER units are known as Leaders, and the units they can lead - known as their Bodyguard units - are listed on their datasheet. During the Declare Battle Formations step, for each Leader in your army, if your army also includes one or more of that Leader's Bodyguard units, you can select one of those Bodyguard units. That Leader will then attach to that Bodyguard unit for the duration of the battle and is said to be leading that unit. Each Bodyguard unit can only have one Leader attached to it. While a Bodyguard unit contains a Leader, it is known as an Attached unit and, with the exception of rules that are triggered when units are destroyed, it is treated as a single unit for all rules purposes. Each time an attack targets an Attached unit, until the attacking unit has resolved all of its attacks, you must use the Toughness characteristic of the Bodyguard models in that unit, even if a Leader in that unit has a different Toughness characteristic. Each time an attack sucessfully wounds an Attached unit, that attack cannot be allocated to a CHARACTER model in that unit, even if that CHARACTER model has lost one or more wounds or has already had attacks allocated to it this phase. As soon as the last Bodyguard model in an Attached unit has been destroyed, any attacks made against that unit that have yet to be allocated can then be allocated to CHARACTER models in that unit. Each time the last model in a Bodyguard unit is destroyed, each CHARACTER unit that is part of that Attached unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time the last model in a CHARACTER unit that is attached to a Bodyguard unit is destroyed and there is not another CHARACTER unit attached, that Attached unit's Bodyguard unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time a unit that is part of an Attached unit is destroyed, it does not have the keywords of any other units that make up that Attached unit (unless it has those keywords on its own datasheet) for the purposes of any rules that would be triggered when that unit is destroyed. Example: If you only destroy the Bodyguard unit that is part of an Attached unit, you have not destroyed a CHARACTER unit. If you only destroy the CHARACTER unit that is part of an Attached unit, or if you destroy the whole Attached unit, you have destroyed one CHARACTER unit. Before the battle, CHARACTER units with the Leader ability can be attached to one of their Bodyguard units to form an Attached unit. Attached units can only contain one Leader. Attacks cannot be allocated to CHARACTER models in Attached units.
Some abilities are used during deployment, or when setting a unit up - either on the battlefield or into Reserves. These are known as Deployment abilities, and some widespread examples of these are presented below.

---

[3] Stratagems that add New Units to Your Army* ()
# Stratagems that add New Units to Your Army*
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

COMMAND RE-ROLL 1CP Core - Battle Tactic Stratagem A great commander can bend even the vagaries of fate and fortune to their will, the better to ensure victory. WHEN: Any phase, just after you make an Advance roll, a Charge roll, a Desperate Escape test or a Hazardous test for a unit from your army, or a Hit roll, a Wound roll, a Damage roll or a saving throw for a model in that unit, or a roll to determine the number of attacks made with a weapon equipped by a model in that unit. If you are using fast dice rolling, this Stratagem can still be used after rolling multiple rolls or saving throws at once. TARGET: That unit or model from your army. EFFECT: You re-roll that roll, test or saving throw. If you are using fast dice rolling, select one of those rolls or saving throws to re-roll.
COUNTER-OFFENSIVE 2CP Core - Strategic Ploy Stratagem In close-quarters combat, the slightest hesitation can leave an opening for a swift foe to exploit. WHEN: Fight phase, just after an enemy unit has fought. TARGET: One unit from your army that is within Engagement Range of one or more enemy units and that has not already been selected to fight this phase. EFFECT: Your unit fights next.
EPIC CHALLENGE 1CP Core - Epic Deed Stratagem The legends of the 41st Millennium are replete with deadly duels between mighty champions. WHEN: Fight phase, when a CHARACTER unit from your army that is within Engagement Range of one or more Attached units is selected to fight. TARGET: One CHARACTER model in your unit. EFFECT: Until the end of the phase, all melee attacks made by that model have the [PRECISION] ability.
INSANE BRAVERY 1CP Core - Epic Deed Stratagem Indifferent to their own survival, these warriors hold their ground against seemingly impossible odds. WHEN: Battle-shock step of your Command phase, just before you take a Battle-shock test for a unit from your army. TARGET: That unit from your army. EFFECT: Your unit automatically passes that Battle-shock test. RESTRICTIONS: You cannot use this Stratagem more than once per battle.
GRENADE 1CP Core - Wargear Stratagem Priming their hand-held projectiles, these warriors draw back and hurl death into the enemy's midst. WHEN: Your Shooting phase. TARGET: One GRENADES unit from your army (excluding units that Advanced, Fell Back or have shot this turn) that is not within Engagement Range of one or more enemy units. EFFECT: Select one GRENADES model in your unit and one enemy unit that is not within Engagement Range of any units from your army and is within 8" of and visible to your GRENADES model. Roll six D6: for each 4+, that enemy unit suffers 1 mortal wound.
TANK SHOCK 1CP Core - Strategic Ploy Stratagem Ramming the foe with a speeding vehicle may be an unsubtle tactic, but it is a murderously effective one. WHEN: Your Charge phase, just after a VEHICLE unit from your army ends a Charge move. TARGET: That VEHICLE unit. EFFECT: Select one enemy unit within Engagement Range of your unit, and select one VEHICLE model in your unit that is within Engagement Range of that enemy unit. Roll a number of D6 equal to the Toughness characteristic of the selected VEHICLE model. For each 5+, that enemy unit suffers 1 mortal wound (to a maximum of 6 mortal wounds).
RAPID INGRESS 1CP Core - Strategic Ploy Stratagem Be it cunning strategy, potent technology or supernatural ritual, there are many means by which a commander may hasten their warriors' onset. WHEN: End of your opponent's Movement phase. TARGET: One unit from your army that is in Reserves. EFFECT: Your unit can arrive on the battlefield as if it were the Reinforcements step of your Movement phase, and if every model in that unit has the Deep Strike ability, you can set that unit up as described in the Deep Strike ability (even though it is not yo
```
</details>


### qwen/qwen3-32b
`finish=stop · 562 compl tok · 1.6s`

[Ruling] The **Ironstorm Spearhead detachment rule "Armoured Wrath"** allows each **ADEPTUS ASTARTES unit** in your army to re-roll **one Hit roll, one Wound roll, or one Damage roll** made for a model in that unit, once per phase.  

[Rule Citation] This is explicitly stated in the provided rules context [1] under **Armoured Wrath (Space Marines)**.  

[Reasoning] The rule specifies that the re-roll applies to **Hit**, **Wound**, or **Damage rolls** for models in Adeptus Astartes units, with no additional restrictions or exceptions mentioned in the provided text. The "once per phase" limitation ensures it can be used once per phase per unit. No conflicting rules in the context override this.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 213 compl tok · 0.8s`

[Ruling] → [Rule Citation] → [Reasoning]

The Ironstorm Spearhead detachment rule Armoured Wrath is a Detachment Rule that allows you to re-roll certain rolls for Adeptus Astartes units in your army.

According to the rule, "Once per phase for each ADEPTUS ASTARTES unit in your army, you can re-roll one Hit roll, one Wound roll or one Damage roll made for a model in that unit."

[Rule Citation] → [1] Armoured Wrath (Space Marines)

This rule is found in the Armoured Wrath datasheet, which is a Detachment Rule for the Space Marines faction.

[Reasoning]

The rule specifically states that it applies to Adeptus Astartes units in your army, and allows you to re-roll one of the following types of rolls: Hit rolls, Wound rolls, or Damage rolls. This means that you can choose which type of roll to re-roll for each Adeptus Astartes unit in your army, once per phase.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 68 compl tok · 0.9s`

Armoured Wrath → Armoured Wrath (Detachment Rule) → [1]

The Armoured Wrath detachment rule states that once per phase for each ADEPTUS ASTARTES unit in your army, you can re-roll one Hit roll, one Wound roll or one Damage roll made for a model in that unit.

### openai/gpt-oss-120b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01kkppm

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=error · ? compl tok · ?s` ⚠ ERROR: Error code: 413 - {'error': {'message': 'Request too large for model `allam-2-7b` in organization `org_01kkppmxccfd1r98zztyme6k5a` service tier `on_demand` on tokens per minute (TPM): Limit 6000, Requ


====================================================================================================
## [41] ARMY_DETACHMENT · mp=OFF · ctx 1363 tok

**Q:** How does the Heretic Astartes army rule Dark Pacts work, and what test must the unit take?

**Expected concepts (ground-truth anchors):** [['dark pacts'], ['leadership test'], ['lethal hits', 'sustained hits']]

<details><summary>rules context sent to every model</summary>

```
[1] Dark Pacts (Chaos Space Marines, Chaos Daemons, Chaos Knights, Thousand Sons, World Eaters, Death Guard)
# Army Rule: Dark Pacts
**Faction:** Chaos Space Marines, Chaos Daemons, Chaos Knights, Thousand Sons, World Eaters, Death Guard  |  **Type:** Army Rule
*Beseeching the Chaos Gods with fanatical fervour, the profane champions of the Heretic Astartes pray for diabolic boons, promising the vilest of offerings in return for their power.*

If your Army Faction is HERETIC ASTARTES, each time a unit with this ability is selected to shoot or fight, it can make a Dark Pact. If it does, it must first take a Leadership test before any effects of that Dark Pact are resolved; if that test is failed, that unit suffers D3 mortal wounds. Then, select one of the following abilities for that unit’s weapons to gain until the end of the phase: [LETHAL HITS], [SUSTAINED HITS 1]


---

[2] Redeployments ()
# Redeployments
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Rules that allow players to redeploy certain units after both armies are deployed (e.g. HURON BLACKHEART 's Red Corsairs ability) are always resolved after the Deploy Armies step (or, if you are playing a Crusade battle, after the Deploy Crusade Armies step), and before the Determine First Turn step, before determining who has the first turn. When a player uses such a rule, they remove that unit or units from the battlefield, then deploy them again using all the normal rules (for example, if all the models in one of these units have the Infiltrators ability, that unit's player can set that unit up using that ability). Players alternate resolving any such rules, starting with the Attacker.

---

[3] Declare Battle Formations ()
# Declare Battle Formations
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

In the order stated below, both players now secretly note down: Which of their Leader units will start the battle attached (they must specify which Leader unit is attached to which Bodyguard unit). Which of their units will start the battle embarked within TRANSPORT models (they must specify which units are embarked within which models). Which of their units will start the battle in Reserves (including Strategic Reserves). When both players have done so, they declare their selections to their opponent.

---

[4] Abilities ()
# Abilities
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Many units have special abilities and rules that may apply during the game, from Core Rules shared by many units to bespoke Psychic abilities and invulnerable saves. These will be described here, along with any rules that apply when larger models such as vehicles have suffered sufficient damage. Some abilities are bestowed by items of wargear that models in a unit can be equipped with, and are known as Wargear abilities. These only apply while a model in the unit is equipped with the relevant item of wargear.

---

[5] Traitor Enforcer (Chaos Daemons)
# Ability: Dark Pacts
**Unit:** Traitor Enforcer  |  **Faction:** Chaos Daemons

If your Army Faction is HERETIC ASTARTES, each time a unit with this ability is selected to shoot or fight, it can make a Dark Pact. If it does, it must first take a Leadership test before any effects of that Dark Pact are resolved; if that test is failed, that unit suffers D3 mortal wounds. Then, select one of the following abilities for that unit’s weapons to gain until the end of the phase: [LETHAL HITS], [SUSTAINED HITS 1]

---

[6] Debt to the Soul Forge (Chaos Space Marines)
# Detachment Rule: Debt to the Soul Forge
**Faction:** Chaos Space Marines  |  **Type:** Detachment Rule  |  **Detachment:** Soulforged Warpack
*Many are the daemons who have forged pacts with Vashtorr the Arkifane. Once bound into such a contract, a soul debt must be paid, one that the daemon strives endlessly, and with all its desperation, to fulfil.*

Each time a HERETIC ASTARTES DAEMON VEHICLE unit from your army makes a Dark Pact, it can invoke its contract. If it does, subtract 1 from the resulting Leadership test when making that Dark Pact, and until the end of the phase: Each time a model in that unit makes a ranged attack, add 1 to the Wound roll., Add 2 to the Attacks characteristic of melee weapons equipped by models in that unit.


---

[7] Sustained Hits ()
# Sustained Hits
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some weapons strike in a flurry of blows, tearing the foe apart with relentless ferocity. Weapons with [SUSTAINED HITS X] in their profile are known as Sustained Hits weapons. Each time an attack is made with such a weapon, if a Critical Hit is rolled, that attack scores a number of additional hits on the target as denoted by 'x'. Example: A model makes an attack with a melee weapon with the [SUSTAINED HITS 2] ability. If the Hit roll is an unmodified 6 (a Critical Hit), then that attack scores a total of 3 hits on the target (1 from the successful Hit roll of 6, and 2 from the [SUSTAINED HITS 2] ability). [SUSTAINED HITS X]: Each Critical Hit scores 'x' additional hits on the target.

---

[8] Lethal Hits ()
# Lethal Hits
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some weapons can inflict fatal injuries on any foe, no matter their resilience.
Weapons with [LETHAL HITS] in their profile are known as Lethal Hits weapons. Each time an attack is made with such a weapon, a Critical Hit automatically wounds the target.
```
</details>


### qwen/qwen3-32b
`finish=stop · 574 compl tok · 1.4s`

[Ruling] The Heretic Astartes army rule **Dark Pacts** allows units with this ability to make a Dark Pact when selected to shoot or fight. Before resolving the Dark Pact, the unit must take a **Leadership test**. If the test is failed, the unit suffers **D3 mortal wounds**. If passed, the unit gains either **[LETHAL HITS]** or **[SUSTAINED HITS 1]** for its weapons until the end of the phase.  

[Rule Citation] **Dark Pacts** (Chaos Space Marines, Chaos Daemons, Chaos Knights, Thousand Sons, World Eaters, Death Guard, Army Rule) → [1].  

[Reasoning] The rule explicitly states that Heretic Astartes units with Dark Pacts must take a Leadership test before applying the effect. The test failure consequence (D3 mortal wounds) and the choice of abilities are directly tied to this rule. No other rules in the provided context modify this process for Heretic Astartes.

### qwen/qwen3.6-27b
`finish=stop · 1700 compl tok · 3.6s`

[Ruling] When a unit with this ability is selected to shoot or fight, it can make a Dark Pact. It must first take a Leadership test before any effects are resolved. If the test is failed, the unit suffers D3 mortal wounds. The player then selects either [LETHAL HITS] or [SUSTAINED HITS 1] for that unit’s weapons to gain until the end of the phase.

[Rule Citation] Dark Pacts (Army Rule) – Context [1]

[Reasoning] The provided rule explicitly outlines the trigger (selected to shoot or fight), mandates a Leadership test prior to resolution, specifies the failure penalty (D3 mortal wounds), and details the reward (choosing one of the two weapon abilities until the end of the phase). No other tests or conditions are stated for the base army rule.

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 83 compl tok · 1.4s`

[Ruling] → [Dark Pacts, Chaos Space Marines, Chaos Daemons, Chaos Knights, Thousand Sons, World Eaters, Death Guard] → [If your Army Faction is HERETIC ASTARTES, each time a unit with this ability is selected to shoot or fight, it can make a Dark Pact.]

The unit must take a Leadership test before any effects of that Dark Pact are resolved.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 129 compl tok · 1.1s`

Dark Pacts → Dark Pacts [1] → The Dark Pacts army rule states that if your Army Faction is HERETIC ASTARTES, each time a unit with this ability is selected to shoot or fight, it can make a Dark Pact. If it does, it must first take a Leadership test before any effects of that Dark Pact are resolved; if that test is failed, that unit suffers D3 mortal wounds. Then, select one of the following abilities for that unit’s weapons to gain until the end of the phase: [LETHAL HITS], [SUSTAINED HITS 1].

### openai/gpt-oss-120b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01kkppm

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=stop · 188 compl tok · 1.1s`

Based on the provided context, the Heretic Astartes army rule 'Dark Pacts' works as follows:


When a HERETIC Astartes unit makes a ranged attack, they can invoke a Dark Pact. If they succeed on their Leadership test, they gain the benefits of the Dark Pact. If they fail the Leadership test, they suffer D3 mortal wounds.


The specific Leadership test to invoke a Dark Pact is not explicitly mentioned in the provided context. However, the context does mention a Leadership test for Dark Pacts in the context of the Chaos Space Marines unit, which is a HERETIC Astartes unit.


Therefore, the Chaos Space Marines unit must take a Leadership test when invoking a Dark Pact. If they fail the Leadership test, they suffer D3 mortal wounds.


====================================================================================================
## [42] ARMY_DETACHMENT · mp=OFF · ctx 1546 tok

**Q:** What does the T’au Empire army rule For the Greater Good do with Observer and Spotted units?

**Expected concepts (ground-truth anchors):** [['for the greater good'], ['observer'], ['spotted']]

<details><summary>rules context sent to every model</summary>

```
[1] For the Greater Good (T’au Empire)
# Army Rule: For the Greater Good
**Faction:** T’au Empire  |  **Type:** Army Rule
*The Hunter Cadres battle for the betterment of the T’au Empire, not for personal gain or egotistic accomplishments. This burning commitment allows for prodigiously effective covering fire. Enemies are pinned in place by deadly bursts of pulse blasts, or the infamous T’au markerlight is used to expose even well-fortified enemy positions, allowing other T’au warriors to fall on the vulnerable enemies with murderous force.*

If your Army Faction is T’AU EMPIRE, at the start of your Shooting phase you can select units from your army with this ability to become Observer units. During your Shooting phase, for each Observer unit from your army that has not been selected to shoot this phase and is eligible to shoot (excluding Fortification and Battle-shocked units) select one enemy unit that is visible to be marked as their Spotted unit until the end of the phase. Each enemy unit can only be marked as a Spotted unit once per phase. Units from your army with the For the Greater Good ability (excluding Observer units) are Guided units while targeting one or more Spotted units. Until the end of the phase, each time a model from your army in a Guided unit makes an attack that targets a Spotted unit, improve the Ballistic Skill characteristic of that attack by 1 and, if the Spotted unit was marked by an Observer unit that has the Markerlight keyword, that attack has the [IGNORES COVER] ability.


---

[2] Units ()
# Units
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Models move and fight in units. A unit can have one or more models from a single datasheet (see below). Models and units from the same army are said to be friendly in relation to each other. Models and units from your opponent's army are referred to as enemy models and units. If a rule affects 'models' or 'units' without specifying that they are friendly or enemy, that rule affects all models or all units, regardless of whose army they are in. Unit: One or more models from the same datasheet. Friendly Models/Units: All models/units from the same army. Enemy Models/Units: All models/units from your opponent's army.

---

[3] Unit Visible ()
# Unit Visible
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

If one or more models in a unit is visible to the observing model, then that model's unit is visible to the observing model.

---

[4] Attached Units ()
# Attached Units
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some CHARACTER units have the Leader ability, which lets them merge with other units (known as Bodyguard units) to form an Attached unit. The Starting Strength of an Attached unit is equal to the combined Starting Strengths of all of its units (i.e. the number of models in the Leader unit added to the number of models in the Bodyguard unit). If either the Leader unit or the Bodyguard unit in an Attached unit is destroyed, the Starting Strength of the remaining unit is changed to be equal to its original Starting Strength. Example: A Primaris Captain (Starting Strength 1) is attached to a unit of Intercessors (Starting Strength 5). This Attached unit has a Starting Strength of 6. If all the Intercessors are destroyed, the remaining Primaris Captain would revert to having a Starting Strength of 1. For the purposes of rules that are triggered when a unit is destroyed, such rules are still triggered when one of the individual units that made up an Attached unit is destroyed (the Leader or the Bodyguard unit). Example: If a rule awards you with 1VP each time an enemy unit is destroyed, and you target an Attached unit, you would gain 1VP if the Bodyguard unit is destroyed and 1VP if the Leader unit is destroyed (for a total of 2VP).

---

[5] Shas’o R’alai (T’au Empire)
# Ability: For the Greater Good
**Unit:** Shas’o R’alai  |  **Faction:** T’au Empire

If your Army Faction is T’AU EMPIRE, at the start of your Shooting phase you can select units from your army with this ability to become Observer units. During your Shooting phase, for each Observer unit from your army that has not been selected to shoot this phase and is eligible to shoot (excluding Fortification and Battle-shocked units) select one enemy unit that is visible to be marked as their Spotted unit until the end of the phase. Each enemy unit can only be marked as a Spotted unit once per phase. Units from your army with the For the Greater Good ability (excluding Observer units) are Guided units while targeting one or more Spotted units. Until the end of the phase, each time a model from your army in a Guided unit makes an attack that targets a Spotted unit, improve the Ballistic Skill characteristic of that attack by 1 and, if the Spotted unit was marked by an Observer unit that has the Markerlight keyword, that attack has the [IGNORES COVER] ability.

---

[6] Tetras (T’au Empire)
# Ability: High-intensity Markerlights
**Unit:** Tetras  |  **Faction:** T’au Empire

Each time this unit is an Observer unit, until the end of the phase, each time a model in its Guided unit makes an attack that targets their Spotted unit, you can re-roll the Hit roll.

---

[7] Coordinated Exploitation (T’au Empire)
# Enhancement: Coordinated Exploitation
**Faction:** T’au Empire  |  **Cost:** 40 pts
**Detachment:** Mont’ka
*This leader eschews their own martial glory in favour of seeking out an advanced vantage point then exploiting it to guide in the firepower of their fellows.*

T’AU EMPIRE model only (excluding Kroot Shaper models). While the bearer is leading a unit, each time that unit is an Observer unit, until the end of the phase, ranged weapons equipped by models in a Guided unit have the [SUSTAINED HITS 1] ability while targeting their Spotted unit.


---

[8] Stealth Battlesuits (T’au Empire)
# Ability: Forward Observers
**Unit:** Stealth Battlesuits  |  **Faction:** T’au Empire

Each time this unit is an Observer unit, until the end of the phase, each time a ranged attack is made by a model in a Guided unit that targets their Spotted unit, re-roll a Hit roll of 1 and re-roll a Wound roll of 1.
```
</details>


### qwen/qwen3-32b
`finish=stop · 894 compl tok · 2.2s`

[Ruling] The T’au Empire army rule **For the Greater Good** allows units with this ability to act as **Observer units** during the Shooting phase. These Observers mark visible enemy units as **Spotted units**, granting **Guided units** (other T’au units with For the Greater Good, excluding Observers) bonuses when targeting Spotted units: +1 to Ballistic Skill and [IGNORES COVER] if the Observer has the Markerlight keyword. Each enemy unit can only be Spotted once per phase.  

[Rule Citation] **For the Greater Good (T’au Empire Army Rule)** → [1] and [5].  

[Reasoning]  
1. **Observer Units**: At the start of the Shooting phase, T’au units with For the Greater Good can be selected as Observers. These units must not have shot this phase and must be eligible to shoot (excluding Fortification/Battle-shocked units).  
2. **Spotted Units**: Each Observer selects a visible enemy unit to mark as Spotted until the end of the phase. Only one Spotted marking per enemy unit is allowed per phase.  
3. **Guided Units**: Non-Observer T’au units with For the Greater Good become Guided units when targeting Spotted units. Their attacks gain +1 Ballistic Skill and [IGNORES COVER] (if the Observer has Markerlight).  

Additional effects from units like Tetras (High-intensity Markerlights) or Stealth Battlesuits (Forward Observers) may stack re-rolls, but these are separate from the base army rule.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 133 compl tok · 0.5s`

[Ruling] → For the Greater Good (T’au Empire) → [Reasoning]

At the start of your Shooting phase, if your Army Faction is T’AU EMPIRE, you can select units from your army with the For the Greater Good ability to become Observer units. During your Shooting phase, for each Observer unit from your army that has not been selected to shoot this phase and is eligible to shoot (excluding Fortification and Battle-shocked units), select one enemy unit that is visible to be marked as their Spotted unit until the end of the phase. Each enemy unit can only be marked as a Spotted unit once per phase.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 212 compl tok · 1.4s`

[Ruling] → The T’au Empire army rule For the Greater Good allows units to become Observer units, which can mark enemy units as Spotted. Guided units targeting Spotted units gain improved Ballistic Skill and potentially [IGNORES COVER] ability.

→ [For the Greater Good] → [Core Rules, For the Greater Good]

→ The rule states that at the start of the Shooting phase, units with this ability can be selected to become Observer units. These Observer units can then mark enemy units as Spotted, which are visible to them. Each enemy unit can only be marked as a Spotted unit once per phase.

→ The rule also states that units with the For the Greater Good ability (excluding Observer units) are Guided units while targeting one or more Spotted units. For Guided units, the Ballistic Skill characteristic of attacks targeting a Spotted unit is improved by 1. Additionally, if the Spotted unit was marked by an Observer unit with the Markerlight keyword, the attack gains the [IGNORES COVER] ability.

### openai/gpt-oss-120b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01kkppm

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=stop · 1860 compl tok · 2.2s`

Based on the provided rules, the T'au Empire army rule 'For the Greater Good' works as follows with Observer and Spotted units:


[Ruling] → [Rule Name] → [Rule Description]


For the Greater Good:
1. Ruling: Observer units (Stealth Battlesuits, Tetras, and High Commanders) become Observer units.
2. Ruling: Spotted units (Stealth Battlesuits, Tetras, and High Commanders) become Spotted units.
3. Ruling: Guided units (Stealth Battlesuits, Tetras, and High Commanders) become Guided units.
4. Ruling: Guided units (Stealth Battlesuits, Tetras, and High Commanders) become Guided units.
5. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
6. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
7. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
8. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
9. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
10. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
11. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
12. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
13. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
14. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
15. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
16. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
17. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
18. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
19. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
20. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
21. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
22. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
23. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
24. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
25. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
26. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
27. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
28. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
29. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
210. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
211. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.
22. Ruling: The Guided unit's weapon systems have the [SUSTAINED HITS 1] ability.


====================================================================================================
## [43] ARMY_DETACHMENT · mp=OFF · ctx 2658 tok

**Q:** What does the Necrons Awakened Dynasty detachment rule Command Protocols do while a Character is leading the unit?

**Expected concepts (ground-truth anchors):** [['command protocols'], ['awakened dynasty'], ['hit roll']]

<details><summary>rules context sent to every model</summary>

```
[1] Command Protocols (Necrons)
# Detachment Rule: Command Protocols
**Faction:** Necrons  |  **Type:** Detachment Rule  |  **Detachment:** Awakened Dynasty
*The Necron nobility and their high-ranking courtiers make war in a codified and relentless fashion. Their command protocols crackle out across multi-dimensional spectra from carrier-wave projectors, compelling their semi-sentient soldiery into battle one overriding directive at a time*

While a Necrons Character model is leading this unit, each time a model in this unit makes an attack, add 1 to the Hit roll.


---

[2] Attached Units ()
# Attached Units
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Some CHARACTER units have the Leader ability, which lets them merge with other units (known as Bodyguard units) to form an Attached unit. The Starting Strength of an Attached unit is equal to the combined Starting Strengths of all of its units (i.e. the number of models in the Leader unit added to the number of models in the Bodyguard unit). If either the Leader unit or the Bodyguard unit in an Attached unit is destroyed, the Starting Strength of the remaining unit is changed to be equal to its original Starting Strength. Example: A Primaris Captain (Starting Strength 1) is attached to a unit of Intercessors (Starting Strength 5). This Attached unit has a Starting Strength of 6. If all the Intercessors are destroyed, the remaining Primaris Captain would revert to having a Starting Strength of 1. For the purposes of rules that are triggered when a unit is destroyed, such rules are still triggered when one of the individual units that made up an Attached unit is destroyed (the Leader or the Bodyguard unit). Example: If a rule awards you with 1VP each time an enemy unit is destroyed, and you target an Attached unit, you would gain 1VP if the Bodyguard unit is destroyed and 1VP if the Leader unit is destroyed (for a total of 2VP).

---

[3] Deployment Abilities ()
# Deployment Abilities — Leader
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

LEADER Mighty heroes fight at the forefront of battle. Some CHARACTER units have 'Leader' listed on their datasheets. Such CHARACTER units are known as Leaders, and the units they can lead - known as their Bodyguard units - are listed on their datasheet. During the Declare Battle Formations step, for each Leader in your army, if your army also includes one or more of that Leader's Bodyguard units, you can select one of those Bodyguard units. That Leader will then attach to that Bodyguard unit for the duration of the battle and is said to be leading that unit. Each Bodyguard unit can only have one Leader attached to it. While a Bodyguard unit contains a Leader, it is known as an Attached unit and, with the exception of rules that are triggered when units are destroyed, it is treated as a single unit for all rules purposes. Each time an attack targets an Attached unit, until the attacking unit has resolved all of its attacks, you must use the Toughness characteristic of the Bodyguard models in that unit, even if a Leader in that unit has a different Toughness characteristic. Each time an attack sucessfully wounds an Attached unit, that attack cannot be allocated to a CHARACTER model in that unit, even if that CHARACTER model has lost one or more wounds or has already had attacks allocated to it this phase. As soon as the last Bodyguard model in an Attached unit has been destroyed, any attacks made against that unit that have yet to be allocated can then be allocated to CHARACTER models in that unit. Each time the last model in a Bodyguard unit is destroyed, each CHARACTER unit that is part of that Attached unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time the last model in a CHARACTER unit that is attached to a Bodyguard unit is destroyed and there is not another CHARACTER unit attached, that Attached unit's Bodyguard unit is no longer part of an Attached unit. It becomes a separate unit, with its original Starting Strength. If this happens as the result of an attack, they become separate units after the attacking unit has resolved all of its attacks. Each time a unit that is part of an Attached unit is destroyed, it does not have the keywords of any other units that make up that Attached unit (unless it has those keywords on its own datasheet) for the purposes of any rules that would be triggered when that unit is destroyed. Example: If you only destroy the Bodyguard unit that is part of an Attached unit, you have not destroyed a CHARACTER unit. If you only destroy the CHARACTER unit that is part of an Attached unit, or if you destroy the whole Attached unit, you have destroyed one CHARACTER unit. Before the battle, CHARACTER units with the Leader ability can be attached to one of their Bodyguard units to form an Attached unit. Attached units can only contain one Leader. Attacks cannot be allocated to CHARACTER models in Attached units.
Some abilities are used during deployment, or when setting a unit up - either on the battlefield or into Reserves. These are known as Deployment abilities, and some widespread examples of these are presented below.

---

[4] Gaining Command Points ()
# Gaining Command Points
**Category:** Core_Rules  |  **Source:** Wahapedia_Core_Rules

Outside of the 1CP players gain at the start of the Command phase, each player can only gain a total of 1CP per battle round, regardless of the source (this includes other CP gained at the start of the Command phase). Starting Strength The number of models a unit contains when it is added to your army is known as its Starting Strength. Below Half-strength Some rules will refer to a unit being Below Half-strength. If a unit has a Starting Strength of 1, then it is said to be Below Half-strength while its remaining number of wounds is less than half of its Wounds characteristic. For any other unit, while the number of models in that unit is less than half of its Starting Strength, that unit is said to be Below Half-strength. Destroyed Throughout a battle, models will suffer damage and be destroyed. When a model is destroyed, it is removed from the battlefield. When every model in a unit has been destroyed, that unit is destroyed. Attached Units Some CHARACTER units have the Leader ability, which lets them merge with other units (known as Bodyguard units) to form an Attached unit. The Starting Strength of an Attached unit is equal to the combined Starting Strengths of all of its units (i.e. the number of models in the Leader unit added to the number of models in the Bodyguard unit). If either the Leader unit or the Bodyguard unit in an Attached unit is destroyed, the Starting Strength of the remaining unit is changed to be equal to its original Starting Strength. Example: A Primaris Captain (Starting Strength 1) is attached to a unit of Intercessors (Starting Strength 5). This Attached unit has a Starting Strength of 6. If all the Intercessors are destroyed, the remaining Primaris Captain would revert to having a Starting Strength of 1. For the purposes of rules that are triggered when a unit is destroyed, such rules are still triggered when one of the individual units that made up an Attached unit is destroyed (the Leader or the Bodyguard unit). Example: If a rule awards you with 1VP each time an enemy unit is destroyed, and you target an Attached unit, you would gain 1VP if the Bodyguard unit is destroyed and 1VP if the Leader unit is destroyed (for a total of 2VP).

---

[5] PROTOCOL OF THE VENGEFUL STARS (Necrons)
# Stratagem: PROTOCOL OF THE VENGEFUL STARS
**Faction:** Necrons  |  **Type:** Awakened Dynasty – Strategic Ploy Stratagem  |  **Cost:** 2 CP
**Detachment:** Awakened Dynasty
**When:** Opponent’s turn — Shooting phase
*Criss-crossfire leaps from the Necron ranks, 
```
</details>


### qwen/qwen3-32b
`finish=stop · 397 compl tok · 1.2s`

[Ruling] While a Necrons Character model is leading the unit, each time a model in the unit makes an attack, add 1 to the Hit roll.  
[Rule Citation] **Command Protocols (Necrons)** → [1]  
[Reasoning] The rule explicitly states that if a Necrons Character is leading the unit, all attacks made by the unit gain a +1 bonus to Hit rolls. No additional conditions or exceptions are provided in the context.

### qwen/qwen3.6-27b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `qwen/qwen3.6-27b` in organization `org_01kkppmxcc

### llama-3.3-70b-versatile
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01k

### llama-3.1-8b-instant
`finish=stop · 66 compl tok · 0.5s`

[Ruling] → [Command Protocols (Necrons)] → [Reasoning]

While a Necrons Character model is leading this unit, each time a model in this unit makes an attack, add 1 to the Hit roll.

This is explicitly stated in the Command Protocols (Necrons) detachment rule.

### meta-llama/llama-4-scout-17b-16e-instruct
`finish=stop · 40 compl tok · 0.8s`

Command Protocols → [1] Command Protocols → While a Necrons Character model is leading this unit, each time a model in this unit makes an attack, add 1 to the Hit roll.

### openai/gpt-oss-120b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-120b` in organization `org_01kkppm

### openai/gpt-oss-20b
`finish=error · ? compl tok · ?s` ⚠ ERROR: rate_limited: Error code: 429 - {'error': {'message': 'Rate limit reached for model `openai/gpt-oss-20b` in organization `org_01kkppmx

### allam-2-7b
`finish=stop · 763 compl tok · 1.1s`





























































































































































































































































































































































































































































































































































































































































































































































































