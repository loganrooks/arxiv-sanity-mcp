# W5.4 Final Validation: P4 -- AI Safety / Alignment (Broad Breadth)

## Profile Summary

**Seed papers** define a researcher working on AI safety and adversarial attacks on LLMs, with specific interests in: jailbreak defense via trigger tokens, scaling patterns in multi-LLM adversarial alignment, adaptive safety alignment for reasoning models, survey of jailbreak mechanisms and defenses, and politically controversial content generation via jailbreaking text-to-image models. The profile is broad across modalities (text LLMs, VLMs, T2I models) and attack/defense axes, but unified by the concern with adversarial safety. Categories span cs.CR, cs.CL, cs.AI, cs.LG.

---

## Part 1: Per-View Paper Assessment

### View 1: Similar Ideas (MiniLM)

1. **[2501.19180] Proactive Safety Reasoning for Jailbreak Defense** -- Highly relevant. Defense against jailbreaks via proactive reasoning. Same question (how to defend LLMs against jailbreaks), same approach (reasoning-based defense). Excellent match.

2. **[2512.24044] Jailbreaking vs Content Safety Filters** -- Highly relevant. Systematic evaluation of the jailbreak/defense arms race. Directly addresses the survey concern of seed [2601.03594]. Excellent match.

3. **[2506.12382] Secondary Risks of Large Language Models** -- Relevant. Broader safety/alignment perspective on LLM risks. Same community, wider scope. Good placement.

4. **[2601.16506] SafeThinker -- Reasoning about Risk** -- Highly relevant. Defense via risk reasoning to go beyond shallow alignment. Directly connected to seed [2511.21214] (adaptive safety alignment). Excellent.

5. **[2601.05466] Jailbreaking via RL-based Tool-Disguised Attacks** -- Highly relevant. Novel jailbreak attack method. Same artifact (jailbreaking LLMs), complementary role (attack vs defense). Good.

6. **[2509.01631] Safety Knowledge Neurons** -- Highly relevant. Interpretability analysis of jailbreak mechanisms. Same question (why do jailbreaks work?), mechanistic approach. Excellent.

7. **[2512.20293] AprielGuard** -- Relevant. Safety safeguarding system for LLMs. Same application (LLM safety in deployment). Good.

8. **[2601.15331] RECAP -- Adversarial Prompting** -- Relevant. Efficient adversarial prompt generation for LLMs. Same activity (red teaming / adversarial testing). Good.

9. **[2601.03265] Jailbreak-Zero -- Pareto Optimal Red Teaming** -- Highly relevant. Red teaming methodology for LLM safety evaluation. Same concern, methodological innovation. Excellent.

10. **[2601.04389] MiJaBench -- Minority Bias via Jailbreaking** -- Relevant. Jailbreaking to reveal bias. Same method (jailbreaking) applied to a fairness concern. Extends the profile's scope appropriately.

11. **[2601.03005] JPU -- Bridging Jailbreak Defense and Unlearning** -- Highly relevant. Defense via unlearning + on-policy correction. Same question (how to defend), novel method. Good.

12. **[2601.00936] Emoji-Based Jailbreaking** -- Relevant. Novel jailbreak vector (emojis). Same activity (jailbreak attacks), specific technique. Good.

13. **[2508.10390] Jailbreaking Black-Box LLMs with Explicit Prompts** -- Relevant. Black-box jailbreak attacks including on reasoning models. Same activity, practical focus. Good.

14. **[2601.15698] Jailbreaking MLLMs for Harmful Image Generation** -- Highly relevant. Multimodal jailbreaking. Directly connected to seed [2601.05150] (jailbreaking T2I models). Excellent.

15. **[2601.12460] TrojanPraise -- Jailbreak via Benign Fine-Tuning** -- Relevant. Fine-tuning-based jailbreak. Same activity (jailbreak attacks), novel vector (fine-tuning APIs). Good.

16. **[2508.10029] Latent Fusion Jailbreak** -- Relevant. White-box jailbreak via latent representation blending. Same activity, different threat model (white-box). Good.

17. **[2503.01839] Jailbreaking T2I via LLMs** -- Highly relevant. Jailbreaking text-to-image models. Directly connected to seed [2601.05150]. Excellent.

18. **[2508.09201] Detecting Unseen Jailbreak Attacks in LVLMs** -- Relevant. Detection of jailbreaks in vision-language models. Same multimodal safety concern. Good.

19. **[2601.08837] Adversarial Poetry to Adversarial Tales** -- Relevant. Culturally-coded jailbreak techniques with interpretability focus. Same activity (jailbreaking), novel angle (cultural structures). Interesting.

20. **[2508.12897] RAJ-PGA -- Jailbreak for Large Reasoning Models** -- Highly relevant. Reasoning-model-specific jailbreak and alignment. Same concern applied to the new class of reasoning models. Excellent.

**Summary**: MiniLM performs excellently for P4. All 20 papers are relevant, with at least 8-10 being highly relevant. The broad AI safety profile combined with the focused "jailbreaking" theme means semantic similarity correctly captures the entire research landscape. The view surfaces attacks, defenses, evaluations, and interpretability analyses of jailbreaking -- a comprehensive picture. The label "Similar Ideas" is accurate: these papers share the idea of adversarial safety for language models.

---

### View 2: Same Vocabulary (TF-IDF)

1. **[2512.24044] Jailbreaking vs Content Safety Filters** -- (Also in MiniLM.) Highly relevant.

2. **[2503.01839] Jailbreaking T2I via LLMs** -- (Also in MiniLM.) Highly relevant.

3. **[2601.07141] MacPrompt -- Jailbreak T2I Models** -- Relevant. Jailbreaking text-to-image models via macaronic language. Same activity (T2I jailbreaking), novel technique. Good.

4. **[2601.10589] Self-Play Safety Alignment** -- Relevant. Self-play red teaming for safety alignment. Same concern (safety alignment), complementary approach (self-play). Good.

5. **[2601.10141] Understanding Safety in Fine-Tuned LLMs** -- Relevant. How fine-tuning degrades safety. Same concern (safety preservation), different angle (fine-tuning risks). Good.

6. **[2506.08473] AsFT -- Anchoring Safety During Fine-Tuning** -- Relevant. Preserving safety during fine-tuning. Same concern (safety under fine-tuning). Good.

7. **[2601.01887] Safety at One Shot -- Patching Fine-Tuned LLMs** -- Relevant. Restoring safety with minimal data after fine-tuning. Same concern (safety restoration). Good.

8. **[2508.12897] RAJ-PGA** -- (Also in MiniLM.) Highly relevant.

9. **[2601.15801] Safety Vectors in LLMs** -- Relevant. Identifying and exploiting safety-relevant components in LLMs. Mechanistic understanding of safety. Good.

10. **[2508.14904] Magic-Token-Guided Safety Control** -- Relevant. Switchable safety control in LLMs. Same concern (controllable safety), novel method. Good.

11. **[2601.03537] STAR-S -- Self-Taught Reasoning on Safety Rules** -- Relevant. Training models to reason about safety rules. Same concern (safety alignment), specific method (self-taught reasoning). Good.

12. **[2601.10527] Safety Report on GPT-5.2, Gemini 3 Pro, etc.** -- Relevant. Empirical safety evaluation of frontier models. Same activity (safety evaluation), applied focus. Good.

13. **[2601.15698] Jailbreaking MLLMs for Image Generation** -- (Also in MiniLM.) Highly relevant.

14. **[2505.18882] Personalized Safety in LLMs** -- Moderately relevant. User-personalized safety policies. Same broad concern (LLM safety), different angle (personalization). Reasonable.

15. **[2601.00213] Malicious Optimization Algorithm Requests** -- Relevant. Overlooked jailbreak vector (optimization algorithm requests). Same activity (jailbreaking), novel vector. Good.

16. **[2601.05466] Jailbreaking via RL-based Tool-Disguised Attacks** -- (Also in MiniLM.) Highly relevant.

17. **[2601.03265] Jailbreak-Zero** -- (Also in MiniLM.) Highly relevant.

18. **[2601.01627] JMedEthicBench -- Medical Safety in Japanese LLMs** -- Moderately relevant. Medical safety evaluation benchmark. Same broad concern (LLM safety), specific domain (medical, Japanese). Reasonable but narrower application.

19. **[2601.08089] Q-realign -- Quantization + Safety Realignment** -- Relevant. Maintaining safety during model quantization. Same concern (safety preservation under model modifications). Good.

20. **[2601.08000] Case-Augmented Deliberative Alignment** -- Relevant. Alignment methodology using legal reasoning analogy. Same concern (safety alignment), novel method (precedent-based reasoning). Good.

**Summary**: TF-IDF performs well for P4 -- much better than for P3. The broad AI safety profile has distinctive enough vocabulary ("jailbreak," "safety," "alignment," "harmful") that TF-IDF can match meaningfully. All 20 papers are at least moderately relevant. The unique contributions of TF-IDF include fine-tuning safety papers (AsFT, Safety at One Shot, Q-realign), which are a genuinely different cluster that MiniLM does not surface. TF-IDF also uniquely finds application-specific safety papers (medical ethics, personalized safety, deliberative alignment) that broaden the profile's scope in useful ways. The "Same Vocabulary" label is accurate, and for this profile, vocabulary matching works well because the jailbreak/safety vocabulary is specific enough to be a strong relevance signal.

---

### View 3: Adjacent Communities (SPECTER2)

1. **[2506.12382] Secondary Risks of LLMs** -- (Also in MiniLM.) Relevant.

2. **[2501.19180] Proactive Safety Reasoning** -- (Also in MiniLM.) Highly relevant.

3. **[2601.03265] Jailbreak-Zero** -- (Also in MiniLM, TF-IDF.) Highly relevant.

4. **[2512.24044] Jailbreaking vs Content Safety Filters** -- (Also in MiniLM, TF-IDF.) Highly relevant.

5. **[2601.15331] RECAP** -- (Also in MiniLM.) Relevant.

6. **[2601.16506] SafeThinker** -- (Also in MiniLM.) Highly relevant.

7. **[2503.08990] Cross-Behavior Attacks for Black-Box LLM Jailbreaking** -- Relevant. Novel jailbreak technique using cross-behavior transfers. Same activity (jailbreaking), efficient black-box approach. Good.

8. **[2601.20903] ICON -- Multi-Turn Jailbreak Attack** -- Relevant. Multi-turn jailbreak strategy. Same activity, specific threat model (multi-turn). Good.

9. **[2601.07141] MacPrompt** -- (Also in TF-IDF.) Relevant.

10. **[2505.16888] SPECTRE -- System Prompt Poisoning** -- Relevant. Supply-chain attack on LLM system prompts. Adjacent threat vector (system prompt poisoning vs direct jailbreaking). Genuinely adjacent-community concern (supply chain security vs adversarial prompting).

11. **[2601.05466] Jailbreaking via RL-based Tool-Disguised Attacks** -- (In all three views.) Highly relevant.

12. **[2601.00936] Emoji-Based Jailbreaking** -- (Also in MiniLM.) Relevant.

13. **[2601.03699] RedBench -- Universal Red Teaming Dataset** -- Relevant. Benchmark for red teaming LLMs. Same activity (red teaming), infrastructure contribution. Good.

14. **[2601.04603] Constitutional Classifiers++** -- Relevant. Production-grade jailbreak defense. Same concern (defense), practical/deployment focus. Good.

15. **[2511.18790] RoguePrompt -- Dual-Layer Ciphering for Jailbreaking** -- Relevant. Cipher-based jailbreak technique. Same activity, novel vector. Good.

16. **[2601.04389] MiJaBench** -- (Also in MiniLM.) Relevant.

17. **[2601.13359] Sockpuppetting -- Output Prefix Injection Jailbreak** -- Relevant. Jailbreak via output prefix injection. Same activity, novel method. Good.

18. **[2508.10029] Latent Fusion Jailbreak** -- (Also in MiniLM.) Relevant.

19. **[2512.07761] TROJail -- Trajectory-Level Multi-Turn Jailbreaks** -- Relevant. Multi-turn jailbreak optimization. Same activity, specific method (trajectory optimization). Good.

20. **[2601.10589] Self-Play Safety Alignment** -- (Also in TF-IDF.) Relevant.

**Summary**: SPECTER2 performs well for P4, but with a critical problem: it is nearly indistinguishable from MiniLM. Of 20 papers, 12 are shared with MiniLM, and the 8 unique papers (SPECTRE, ICON, RedBench, Constitutional Classifiers++, RoguePrompt, Sockpuppetting, TROJail, Cross-Behavior Attacks) are all from the same jailbreak/safety community, not from truly adjacent communities. SPECTER2 adds more jailbreak techniques and red teaming tools but does not provide the cross-community perspective its label promises.

The label "Adjacent Communities" is inaccurate -- all 20 papers are from the same LLM safety/jailbreaking community. What SPECTER2 actually provides is "more papers from the same citation cluster," which for a broad profile in a hot research area means more of the same kind of paper.

Score compression remains extreme (0.9628-0.9775, spread 0.0146), confirming that SPECTER2 cannot meaningfully rank within this paper set.

---

## Part 2: View Characterization

### Similar Ideas (MiniLM)

- **Label accuracy**: Highly accurate. Every paper shares ideas about adversarial LLM safety.
- **Distinctiveness**: MiniLM's unique papers (Safety Knowledge Neurons, AprielGuard, JPU, Adversarial Poetry, Black-Box Jailbreaking, Detecting Unseen Jailbreaks, TrojanPraise) include mechanistic/interpretability work and detection-focused papers that other views miss.
- **What it finds that others don't**: MiniLM uniquely surfaces interpretability-oriented safety research (Safety Knowledge Neurons, Adversarial Poetry) and detection methods (unseen jailbreak detection) that represent a different research angle from the attack/defense focus of the other views.

### Same Vocabulary (TF-IDF)

- **Label accuracy**: Accurate, and for this profile, vocabulary matching is an effective signal.
- **Distinctiveness**: TF-IDF's unique papers (12 total) include a genuinely different cluster: fine-tuning safety papers (AsFT, Safety at One Shot, Q-realign, understanding safety in fine-tuning) and application-specific safety (medical ethics, personalized safety, deliberative alignment). This cluster is absent from both MiniLM and SPECTER2.
- **What it finds that others don't**: TF-IDF uniquely surfaces the "safety under modification" cluster (fine-tuning, quantization, etc.) and domain-specific safety applications. This is a meaningfully different research concern from jailbreak attack/defense.

### Adjacent Communities (SPECTER2)

- **Label accuracy**: Inaccurate. The papers are from the same community, not adjacent ones. For a broad profile, SPECTER2's citation-graph embeddings converge with semantic embeddings because the entire field shares dense citation patterns.
- **Distinctiveness**: Low relative to MiniLM. The 8 unique papers are additional jailbreak techniques and red teaming tools -- more of the same, not a different perspective.
- **What it finds that others don't**: SPECTER2 uniquely surfaces system prompt poisoning (SPECTRE) and production defense systems (Constitutional Classifiers++), which are practical deployment papers. These are marginally different from MiniLM's picks but not from a different community.

---

## Part 3: Multi-View Assessment

### Coverage
42 unique papers from 60 slots -- the highest overlap of the three profiles. This reflects the fact that AI safety/jailbreaking is a cohesive enough field that all three retrieval strategies converge on the same papers. Coverage is good but redundant.

### Distinctiveness
The most important finding: for P4, the three views collapse into approximately two effective views. MiniLM and SPECTER2 are near-duplicates (12 shared papers, 7-8 unique each). TF-IDF is the most distinctive and also the most useful differentiator, surfacing the "safety under modification" cluster that represents a genuinely different research concern.

The optimal pairing for P4 would be MiniLM (jailbreak attack/defense) + TF-IDF (safety preservation and applied safety). SPECTER2 adds negligible value.

### Label Accuracy
- **"Similar Ideas" (MiniLM)**: Accurate and helpful.
- **"Same Vocabulary" (TF-IDF)**: Accurate, and for this profile, genuinely useful.
- **"Adjacent Communities" (SPECTER2)**: Inaccurate. Same community, not adjacent.

### Overlap Papers
Papers in all three views (Jailbreak-Zero [2601.03265], RL-based Tool-Disguised Attacks [2601.05466], Jailbreaking vs Safety Filters [2512.24044]) are all highly relevant papers that sit at the center of the jailbreak/safety field. The all-three overlap is a decent quality signal for P4, unlike P1 and P3 where overlap papers were merely average.

### Would a Researcher Actually Switch Views?
A P4 researcher would benefit from two views: MiniLM for core jailbreak research, and TF-IDF for the broader safety-under-modification landscape. SPECTER2 would not prompt switching because it surfaces more of what MiniLM already shows. The researcher might scan SPECTER2's unique papers (system prompt poisoning, Constitutional Classifiers++) in passing, but these do not constitute a distinct perspective.

### Information Overload
42 unique papers is still too many. The tail quality is high for P4 (most papers are relevant) but a researcher would still be better served by curated top-10s from two views rather than unfiltered top-20s from three views.

---

## Part 4: Emergent Observations

- The broad AI safety profile reveals that SPECTER2's "Adjacent Communities" function is the weakest for exactly the profile breadth where you might expect it to shine. A broad profile in a hot field means the citation graph is dense -- everyone cites everyone -- so SPECTER2 cannot distinguish communities.
- TF-IDF performs much better for P4 than for P3 because the AI safety field has distinctive vocabulary ("jailbreak," "alignment," "safety filter") that is specific enough to be informative, unlike quantum ML's vocabulary which is dominated by the generic term "quantum."
- The three-view architecture reveals a structural insight about P4: the jailbreak attack/defense subfield (captured by MiniLM and SPECTER2) is distinct from the safety-under-modification subfield (uniquely captured by TF-IDF). This is a genuine research landscape insight -- there are two communities that both use "safety" vocabulary but address different problems (adversarial robustness vs training-time safety).
- For broad profiles, the value of parallel views depends on whether the breadth spans genuinely distinct sub-communities. P4 spans two (jailbreaking and fine-tuning safety), which makes two views useful. If the profile were even broader (spanning AI ethics, governance, and technical safety), more views might be justified.

---

## Part 5: Metric Divergence

The quantitative story would show 42 unique papers and high overlap between MiniLM and SPECTER2, correctly suggesting redundancy. But the quantitative metrics would not reveal that TF-IDF's unique papers are qualitatively the most interesting addition -- they represent a distinct research concern (safety under modification) that is invisible to the other views. A count-based metric would show TF-IDF contributing 12 unique papers vs SPECTER2's 8, but would not capture that TF-IDF's 12 are thematically coherent and complementary while SPECTER2's 8 are just more jailbreak papers.

SPECTER2 score compression is extreme (std = 0.0042), confirming it cannot meaningfully rank these papers. The top-to-bottom score spread of 0.0146 means the difference between the "most related" and "least related" paper is negligible.
