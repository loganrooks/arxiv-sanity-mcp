# W5.4 Final Validation: P1 -- RL for Robotics (Medium Breadth)

## Profile Summary

**Seed papers** define a researcher working on reinforcement learning for robotics, with emphasis on: offline model-based RL for real robots, RL-enhanced embodied reasoning, flow-based policy learning, deep RL for magnetic robot control, and growing policy optimization for legged locomotion. The profile is coherent around the intersection of RL algorithms and physical robot control, spanning manipulation, locomotion, and specialized domains (GI navigation). Categories cluster on cs.RO with secondary cs.LG and cs.AI.

---

## Part 1: Per-View Paper Assessment

### View 1: Similar Ideas (MiniLM)

1. **[2505.22094] ReinFlow** -- Highly relevant. RL fine-tuning of flow matching policies for robotic control. Directly extends seed paper [2509.25756] (SAC Flow). Same question, same method family. Excellent match to "Similar Ideas."

2. **[2601.19707] Qflex -- Scalable Exploration via Value-Guided Flow** -- Relevant. High-dimensional continuous control with flow-based exploration. Same method family (flow + RL), broader scope (musculoskeletal models). Appropriate for "Similar Ideas."

3. **[2601.16109] Robust Torque-based Locomotion via Model-Based Supervision** -- Highly relevant. Residual RL for bipedal locomotion with sim-to-real transfer. Same application (locomotion) and same hybrid approach (model-based + RL). Correct placement.

4. **[2601.15761] SigEnt-SAC for Real-World Robot Learning** -- Relevant. Off-policy RL for real-world robotics with novel entropy formulation. Same method class (SAC variants), same application domain. Good match.

5. **[2601.20701] DMPO -- One-Step Flow Policy Optimization** -- Highly relevant. One-step flow generation with RL fine-tuning for real-time robotic control. Directly connected to seed paper themes (flow + RL + robotics). Strong "Similar Ideas" match.

6. **[2511.00423] BOOM -- Bootstrap Off-policy with World Model** -- Relevant. Model-based RL integrating planning and off-policy learning. Same method family (model-based RL) as seed [2504.16680]. Appropriate placement.

7. **[2509.04069] DRLR -- Exploration-Efficient Deep RL with Demonstrations** -- Relevant. RL with demonstrations for robotics tasks including sim-to-real deployment. Same application domain, complementary method (demonstration-augmented RL). Correct.

8. **[2508.21065] Learning on the Fly -- Policy Adaptation via Differentiable Simulation** -- Relevant. Online policy adaptation for quadrotor control using differentiable simulation. Same concern (sim-to-real), different platform (aerial vs ground). Good.

9. **[2601.01948] SDP -- Diffusion Policy from Primitive Skills** -- Moderately relevant. Skill-conditioned diffusion policy for manipulation. Adjacent method (diffusion, not RL per se), but connected through the generative policy thread. Reasonable placement.

10. **[2512.24288] SiLRI -- Real-world RL from Suboptimal Interventions** -- Relevant. Real-world RL for manipulation with human-in-the-loop. Same paradigm (real-world RL), different emphasis (intervention quality). Good.

11. **[2601.12169] Legged MPC with Smooth Neural Surrogates** -- Relevant. Neural dynamics models for legged MPC. Connects to seed paper themes (model-based approaches for locomotion). Appropriate.

12. **[2601.21394] Space-Based Environmentally-Adaptive Grasping** -- Moderately relevant. SAC-based RL for grasping in space environments. Same method (SAC), novel application domain. The space context is a stretch for an RL-for-robotics researcher, but the RL methodology connects.

13. **[2511.06816] CtrlFlow -- Controllable Flow Matching for Online RL** -- Relevant. Flow matching for trajectory-level synthesis in MBRL. Directly connected to the flow + RL theme of seed papers. Good.

14. **[2601.12397] Di-BM -- Diverse Skills with Mixture of Experts** -- Moderately relevant. Imitation learning with MoE for multi-task manipulation. Tangentially connected (robot learning, but imitation not RL). Borderline.

15. **[2512.09101] MGP -- Masked Generative Policy for Robotic Control** -- Moderately relevant. Generative visuomotor policy. Connected through robotic control, but the core method (masked transformers) is distant from RL. Borderline placement.

16. **[2601.16985] Neuro-Symbolic Learning for Open-World Robotics** -- Relevant. Hybrid TAMP + RL for robotic adaptation. Same concern (RL for robotics), with a neuro-symbolic twist. Appropriate.

17. **[2512.16881] PolaRiS -- Real-to-Sim Evaluations for Generalist Robot Policies** -- Moderately relevant. Evaluation framework, not an RL algorithm. Connected through sim-to-real concerns. Somewhat tangential.

18. **[2509.18631] Sim-and-Real Policy Co-Training via Domain Adaptation** -- Relevant. Sim-to-real transfer for manipulation. Same application concern (bridging sim-real gap). Good.

19. **[2512.17853] AnyTask -- Automated Sim-to-Real Policy Learning** -- Moderately relevant. Automated task generation for sim-to-real. Infrastructure-level paper rather than algorithmic RL contribution. Tangentially connected.

20. **[2601.00969] V-VLAPS -- Value-augmented VLA Planning** -- Moderately relevant. MCTS planning with VLA models. Connected through robotic manipulation, but the VLA focus is a different research thread. Borderline.

**Summary**: The top ~12 papers are solidly relevant, sharing either the same RL algorithms or the same robotics applications. The bottom third drifts toward adjacent concerns (evaluation, imitation learning, VLA models). The view correctly captures "similar ideas" in the sense of semantic nearness, though it includes some methodologically distant papers that happen to share vocabulary about robot learning.

---

### View 2: Same Vocabulary (TF-IDF)

1. **[2410.24164] pi_0 -- VLA Flow Model for General Robot Control** -- Relevant but different emphasis. A foundation model paper about generalist robot policies. Shares vocabulary ("reinforcement learning," "robot control," "flow matching") but is a VLA/foundation model paper, not an RL algorithm paper. The keyword overlap is real but the research question differs.

2. **[2601.21713] Cloth Manipulation via Modular RL** -- Relevant. RL for cloth manipulation with sim-to-real. Shares vocabulary and application domain. Reasonable placement.

3. **[2505.18763] GenPO -- Diffusion Models + On-Policy RL** -- Relevant. Diffusion policies with PPO for locomotion/manipulation. Direct keyword match and methodological relevance. Good.

4. **[2510.11027] Vlaser -- VLA with Embodied Reasoning** -- Moderately relevant. VLA model for robot control. Shares "robot" and "policy" vocabulary but is fundamentally a vision-language model paper. TF-IDF is picking up shared surface terms.

5. **[2410.11234] Bayes Adaptive MCTS for Offline MBRL** -- Relevant. Offline model-based RL with planning. Direct methodological relevance to seed [2504.16680]. Good.

6. **[2601.15419] Unified Latent Space for Cross-Embodiment Robot Control** -- Moderately relevant. Cross-embodiment control using contrastive learning. Shares "robot control" vocabulary but the method (contrastive latent spaces) is distant from RL.

7. **[2508.21065] Learning on the Fly** -- (Also in MiniLM view.) Relevant. Differentiable simulation for policy adaptation.

8. **[2512.17853] AnyTask** -- (Also in MiniLM view.) Moderately relevant. Automated sim-to-real pipeline.

9. **[2410.15979] Learning Quadrotor Control via Differentiable Simulation** -- Relevant. Differentiable simulation for quadrotor RL. Good keyword match and methodological relevance.

10. **[2601.06845] Code Evolution for Control via LLM-Driven Search** -- Weakly relevant. LLM-driven policy synthesis. Shares "control" vocabulary but is fundamentally about evolutionary search with LLMs, not RL. TF-IDF is matching surface terms like "reinforcement learning" and "control policies."

11. **[2601.08136] Reverse Flow Matching for Online RL** -- Relevant. Unified framework for training diffusion/flow policies with RL. Direct methodological connection.

12. **[2509.04069] DRLR** -- (Also in MiniLM view.) Relevant.

13. **[2512.24125] Unified Embodied VLM Reasoning** -- Moderately relevant. VLA model with flow-matching action tokenizer. Shares terms but is primarily a VLM reasoning paper.

14. **[2601.07821] Failure-Aware RL for Real-World Manipulation** -- Relevant. Offline-to-online RL with safety considerations. Good match.

15. **[2601.00610] Vision-based Goal-Reaching Control** -- Relevant. Hierarchical RL framework for mobile robot control. Shares vocabulary and application domain.

16. **[2512.23870] Max-Entropy RL with Flow Matching** -- Relevant. SAC with flow-based policies. Direct algorithmic connection to seed papers.

17. **[2512.01052] Autonomous Grasping on Quadruped Robot** -- Moderately relevant. Quadruped with grasping capability. Shares "robot" and "grasping" vocabulary but is more of a systems integration paper. TF-IDF correctly matched the vocabulary.

18. **[2601.05241] RoboVIP -- Multi-View Video for Robot Manipulation** -- Weakly relevant. Data augmentation for robot policy training. Connected through "manipulation" and "policy" terms but is fundamentally a data augmentation/vision paper.

19. **[2512.24288] SiLRI** -- (Also in MiniLM view.) Relevant.

20. **[2601.01409] Sampling Strategy for MPPI on Legged Robots** -- Relevant. MPPI control for quadruped locomotion. Shares domain (legged robots) and vocabulary. The method (sampling-based optimal control) is adjacent to but distinct from RL.

**Summary**: TF-IDF produces a wider, less focused set. It correctly matches on shared vocabulary ("reinforcement learning," "robot," "policy," "control," "manipulation," "simulation") but this vocabulary matching surfaces papers from adjacent communities (VLA models, foundation models, systems integration) that share terms without sharing research questions. The view contains both true hits (GenPO, BAMCTS, flow matching papers) and vocabulary coincidences (Vlaser, RoboVIP, code evolution). The label "Same Vocabulary" is technically accurate -- these papers really do use the same words -- but the implication for a researcher is that this view mixes deep relevance with surface relevance.

---

### View 3: Adjacent Communities (SPECTER2)

1. **[2505.22094] ReinFlow** -- (Also in MiniLM, TF-IDF overlap.) Highly relevant.

2. **[2601.15761] SigEnt-SAC** -- (Also in MiniLM.) Relevant.

3. **[2601.19707] Qflex** -- (Also in MiniLM.) Relevant.

4. **[2512.24288] SiLRI** -- (Also in MiniLM, TF-IDF.) Relevant.

5. **[2505.18763] GenPO** -- (Also in TF-IDF.) Relevant.

6. **[2404.13879] Lipschitz-Regularized Critics for Policy Robustness** -- Relevant. RL robustness against transition dynamics uncertainty. Same concern (robust RL for real-world deployment). This is the kind of theoretically-oriented RL paper that SPECTER2 should surface -- same community, slightly different angle.

7. **[2601.20701] DMPO** -- (Also in MiniLM.) Highly relevant.

8. **[2601.21251] SMP -- MoE Diffusion Policies for Manipulation** -- Moderately relevant. Multi-task manipulation via mixture-of-experts diffusion. Adjacent community (diffusion policies for robots) but not RL-focused. Reasonable for "Adjacent Communities."

9. **[2509.04069] DRLR** -- (In all three views.) Relevant.

10. **[2505.14975] Flattening Hierarchies with Policy Bootstrapping** -- Relevant. Offline goal-conditioned RL for long-horizon tasks. Same method class (offline RL), broader scope. Appropriate cross-community pick.

11. **[2601.03044] SOP -- Scalable Online Post-Training for VLA Models** -- Moderately relevant. Online post-training of VLA models on robot fleets. Adjacent community (VLA post-training uses RL methods but is fundamentally about foundation model deployment). This is genuinely "adjacent community" material.

12. **[2601.18107] MoReBRAC -- Robust Offline Policy Optimization** -- Relevant. Model-based offline RL with uncertainty-aware synthesis. Direct methodological connection.

13. **[2601.16163] Cosmos Policy -- Video Models for Visuomotor Control** -- Moderately relevant. Adapting video generation models into robot policies. Adjacent community (video models -> robot control). Genuinely from a different community.

14. **[2512.09101] MGP** -- (Also in MiniLM.) Moderately relevant.

15. **[2601.07821] Failure-Aware RL** -- (Also in MiniLM, TF-IDF.) Relevant.

16. **[2511.00423] BOOM** -- (Also in MiniLM.) Relevant.

17. **[2601.01948] SDP** -- (Also in MiniLM.) Moderately relevant.

18. **[2505.02228] Coupled Distributional RND for World Model IL** -- Relevant. World-model-based imitation learning with random network distillation. Adjacent approach (imitation learning with world models) to the RL-for-robotics core.

19. **[2509.18631] Sim-Real Co-Training** -- (Also in MiniLM, TF-IDF.) Relevant.

20. **[2601.19969] E2HiL -- Entropy-Guided Human-in-the-Loop RL** -- Relevant. Human-in-the-loop RL for manipulation. Same paradigm (real-world RL with human guidance).

**Summary**: SPECTER2 produces a list that substantially overlaps with MiniLM (12 of 20 papers shared). The 8 unique papers include some genuinely adjacent-community picks (Cosmos Policy from video generation, SOP from VLA post-training, Lipschitz critics from RL theory) but also papers that are simply the same community with slight variation. The "Adjacent Communities" label is partially misleading for P1 -- most papers are from the same RL-for-robotics community, not truly adjacent ones.

A critical observation: SPECTER2 scores are compressed into a tiny range (0.9610-0.9682, spread of 0.0072). This means SPECTER2 is not meaningfully discriminating among these papers -- it considers them all approximately equally related. The ranking within this view is essentially noise.

---

## Part 2: View Characterization

### Similar Ideas (MiniLM)

- **Label accuracy**: Mostly accurate. The top papers genuinely share ideas (flow-based RL, model-based RL, locomotion RL) with the seeds. The bottom third includes papers that share abstract themes but not specific ideas.
- **Distinctiveness**: MiniLM provides the tightest, most algorithmically-focused recommendations. Papers cluster around specific RL methods (flow matching, SAC variants, model-based RL).
- **What it finds that others don't**: MiniLM uniquely surfaces CtrlFlow (trajectory-level flow matching for RL), torque-based locomotion, legged MPC with neural surrogates, and neuro-symbolic approaches. These are methodologically close to the seeds but may not share exact vocabulary.

### Same Vocabulary (TF-IDF)

- **Label accuracy**: Accurate but the label undersells a problem. These papers share vocabulary, but shared vocabulary in a broad field like RL-for-robotics includes many papers that are not actually about the same research question.
- **Distinctiveness**: TF-IDF has the most unique papers (14 out of 20), meaning it casts the widest net. It surfaces papers that other views miss entirely -- including pi_0 (a landmark VLA paper), Bayes Adaptive MCTS, LLM-driven code evolution, and MPPI control for legged robots.
- **What it finds that others don't**: TF-IDF uniquely surfaces foundation/VLA models (pi_0, Vlaser, RoboVIP), control-theory-adjacent work (MPPI sampling), and systems-level papers (quadruped grasping). These are papers that a researcher might encounter at the same conference but that address different research questions.

### Adjacent Communities (SPECTER2)

- **Label accuracy**: Misleading for P1. The majority of SPECTER2's picks are from the same RL-for-robotics community, not from adjacent communities. SPECTER2's citation-graph embeddings are placing these papers in the same citation neighborhood, not in adjacent ones.
- **Distinctiveness**: Low distinctiveness relative to MiniLM. Only 8 of 20 papers are unique to this view, and several of those (SOP, Cosmos Policy) could arguably be called "adjacent community" while others (Lipschitz critics, offline policy optimization) are the same community.
- **What it finds that others don't**: The genuinely unique picks are Cosmos Policy (video generation -> robotics), SOP (VLA fleet deployment), Lipschitz critics (RL theory), and hierarchical policy bootstrapping. These do represent slightly different angles on the same problem space.

---

## Part 3: Multi-View Assessment

### Coverage
The three views together cover 44 unique papers out of 60 slots. This is reasonable coverage, though the overlap pattern reveals that MiniLM and SPECTER2 are more similar to each other (12 shared) than either is to TF-IDF. The combination does cover the landscape reasonably well: algorithmic RL (MiniLM), broader robotics vocabulary (TF-IDF), and citation-network neighbors (SPECTER2). However, the landscape for RL-for-robotics is well-defined enough that all three views are pulling from roughly the same pool.

### Distinctiveness
MiniLM and SPECTER2 have problematically high overlap (12 of 20 papers shared). For a medium-breadth profile in a well-defined field, these two views are not sufficiently distinct to justify separate presentation. TF-IDF is the most distinctive (14 unique papers) but its distinctiveness comes at the cost of precision -- many of its unique papers are only tangentially relevant.

### Label Accuracy
- **"Similar Ideas" (MiniLM)**: Mostly accurate. The view does surface papers with similar ideas.
- **"Same Vocabulary" (TF-IDF)**: Technically accurate but potentially confusing. A researcher might interpret "Same Vocabulary" as meaning "uses the same technical terms I use," which is true, but the label doesn't warn that shared vocabulary is a weak signal of shared research questions.
- **"Adjacent Communities" (SPECTER2)**: Inaccurate for this profile. The papers are mostly from the same community, not adjacent ones. The label sets an expectation of cross-field discovery that this view does not deliver.

### Overlap Papers
Papers appearing in all three views (SiLRI [2512.24288], DRLR [2509.04069]) are solid, relevant papers but not especially exceptional. They are papers that happen to sit at the intersection of semantic similarity, vocabulary overlap, and citation proximity -- which in a coherent field just means they are straightforwardly relevant. The overlap papers are not more valuable than the best unique picks.

### Would a Researcher Actually Switch Views?
For P1, a researcher would likely be well-served by MiniLM alone. The added value of TF-IDF is surface-level breadth (VLA papers, foundation models) that might be useful for awareness but not for immediate research. SPECTER2 adds almost nothing beyond what MiniLM already provides. A researcher might switch to TF-IDF occasionally to see what is happening in adjacent vocabulary spaces, but would unlikely use SPECTER2 as a separate view.

### Information Overload
60 papers is too many for this profile. The quality tail is long -- papers 15-20 in each view are mostly borderline relevant. A researcher would be better served by the top 10 from each view (30 papers) or even the top 10 from MiniLM plus a "you might also be interested in" sidebar from TF-IDF.

---

## Part 4: Emergent Observations

- The three-view architecture reveals that RL-for-robotics is a well-defined field where semantic similarity, vocabulary, and citation proximity largely converge. This means parallel views add less value for medium-breadth profiles in coherent fields.
- SPECTER2's extreme score compression (std = 0.0022) is a quality signal: it means the model cannot meaningfully rank within this neighborhood. This is a problem for any view that relies on SPECTER2 ranking.
- The most interesting papers surfaced by the parallel architecture are TF-IDF's unique picks (pi_0, Bayes Adaptive MCTS, LLM code evolution) -- these are papers from adjacent but distinct research threads that would be hard to find via semantic similarity alone. This suggests TF-IDF's value is as a "serendipity engine," not as a precision tool.
- The optimal number of views for P1 is arguably two: MiniLM for precision and TF-IDF for breadth. SPECTER2 is redundant.

---

## Part 5: Metric Divergence

The quantitative story for P1 would suggest three distinct retrieval strategies producing complementary results. The qualitative reality is that MiniLM and SPECTER2 are near-duplicates for this profile, and TF-IDF is distinctive but imprecise. The metric of "unique papers per view" (8, 14, 8) suggests equal distinctiveness for MiniLM and SPECTER2, but the qualitative experience is that MiniLM's unique papers are more precisely relevant while SPECTER2's unique papers are mostly same-community variations. Quantitative overlap metrics understate the redundancy between MiniLM and SPECTER2 because they count papers, not the kind of relevance provided.
