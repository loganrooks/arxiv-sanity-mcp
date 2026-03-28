# Single-Strategy Characterization Review

**Model:** qwen3
**Profile:** Language model reasoning (P2)
**Depth:** full
**Overlap with MiniLM:** 14/20 shared, 6 unique to qwen3

## Seed Papers
  - [2506.14641] Revisiting Chain-of-Thought Prompting: Zero-shot Can Be Stronger than Few-shot (cs.CL)
  - [2501.01203] HetGCoT: Heterogeneous Graph-Enhanced Chain-of-Thought LLM Reasoning for Academic Question Answering (cs.SI)
  - [2601.03559] DiffCoT: Diffusion-styled Chain-of-Thought Reasoning in LLMs (cs.CL)
  - [2601.10775] LLMs for Game Theory: Entropy-Guided In-Context Learning and Adaptive CoT Reasoning (cs.CL)
  - [2503.10095] Cognitive-Mental-LLM: Evaluating Reasoning in Large Language Models for Mental Health Prediction via Online Text (cs.CL)

## qwen3 Top-20 Recommendations

### Paper 1: [2601.03559]
**Title:** DiffCoT: Diffusion-styled Chain-of-Thought Reasoning in LLMs
**Category:** cs.CL
**Score:** 0.8547
**In MiniLM top-20:** True

Chain-of-Thought (CoT) reasoning improves multi-step mathematical problem solving in large language models but remains vulnerable to exposure bias and error accumulation, as early mistakes propagate irreversibly through autoregressive decoding. In this work, we propose DiffCoT, a diffusion-styled CoT framework that reformulates CoT reasoning as an iterative denoising process. DiffCoT integrates diffusion principles at the reasoning-step level via a sliding-window mechanism, enabling unified generation and retrospective correction of intermediate steps while preserving token-level autoregression. To maintain causal consistency, we further introduce a causal diffusion noise schedule that respects the temporal structure of reasoning chains. Extensive experiments on three multi-step CoT reasoning benchmarks across diverse model backbones demonstrate that DiffCoT consistently outperforms existing CoT preference optimization methods, yielding improved robustness and error-correction capability in CoT reasoning.

### Paper 2: [2601.08058]
**Title:** Reasoning Beyond Chain-of-Thought: A Latent Computational Mode in Large Language Models
**Category:** cs.CL
**Score:** 0.8504
**In MiniLM top-20:** True

Chain-of-Thought (CoT) prompting has improved the reasoning performance of large language models (LLMs), but it remains unclear why it works and whether it is the unique mechanism for triggering reasoning in large language models. In this work, we study this question by directly analyzing and intervening on the internal representations of LLMs with Sparse Autoencoders (SAEs), identifying a small set of latent features that are causally associated with LLM reasoning behavior. Across multiple model families and reasoning benchmarks, we find that steering a single reasoning-related latent feature can substantially improve accuracy without explicit CoT prompting. For large models, latent steering achieves performance comparable to standard CoT prompting while producing more efficient outputs. We further observe that this reasoning-oriented internal state is triggered early in generation and can override prompt-level instructions that discourage explicit reasoning. Overall, our results suggest that multi-step reasoning in LLMs is supported by latent internal activations that can be externally activated, while CoT prompting is one effective, but not unique, way of activating this mechanism rather than its necessary cause.

### Paper 3: [2506.14641]
**Title:** Revisiting Chain-of-Thought Prompting: Zero-shot Can Be Stronger than Few-shot
**Category:** cs.CL
**Score:** 0.8436
**In MiniLM top-20:** True

In-Context Learning (ICL) is an essential emergent ability of Large Language Models (LLMs), and recent studies introduce Chain-of-Thought (CoT) to exemplars of ICL to enhance the reasoning capability, especially in mathematics tasks. However, given the continuous advancement of model capabilities, it remains unclear whether CoT exemplars still benefit recent, stronger models in such tasks. Through systematic experiments, we find that for recent strong models such as the Qwen2.5 series, adding traditional CoT exemplars does not improve reasoning performance compared to Zero-Shot CoT. Instead, their primary function is to align the output format with human expectations. We further investigate the effectiveness of enhanced CoT exemplars, constructed using answers from advanced models such as \texttt{Qwen2.5-Max} and \texttt{DeepSeek-R1}. Experimental results indicate that these enhanced exemplars still fail to improve the model's reasoning performance. Further analysis reveals that models tend to ignore the exemplars and focus primarily on the instructions, leading to no observable gain in reasoning ability. Overall, our findings highlight the limitations of the current ICL+CoT framework in mathematical reasoning, calling for a re-examination of the ICL paradigm and the definition of exemplars.

### Paper 4: [2601.03769]
**Title:** EntroCoT: Enhancing Chain-of-Thought via Adaptive Entropy-Guided Segmentation
**Category:** cs.AI
**Score:** 0.8399
**In MiniLM top-20:** True

Chain-of-Thought (CoT) prompting has significantly enhanced the mathematical reasoning capabilities of Large Language Models. We find existing fine-tuning datasets frequently suffer from the "answer right but reasoning wrong" probelm, where correct final answers are derived from hallucinated, redundant, or logically invalid intermediate steps. This paper proposes EntroCoT, a unified framework for automatically identifying and refining low-quality CoT supervision traces. EntroCoT first proposes an entropy-based mechanism to segment the reasoning trace into multiple steps at uncertain junctures, and then introduces a Monte Carlo rollout-based mechanism to evaluate the marginal contribution of each step. By accurately filtering deceptive reasoning samples, EntroCoT constructs a high-quality dataset where every intermediate step in each reasoning trace facilitates the final answer. Extensive experiments on mathematical benchmarks demonstrate that fine-tuning on the subset constructed by EntroCoT consistently outperforms the baseslines of full-dataset supervision.

### Paper 5: [2507.11408]
**Title:** KisMATH: Do LLMs Have Knowledge of Implicit Structures in Mathematical Reasoning?
**Category:** cs.CL
**Score:** 0.8258
**In MiniLM top-20:** True

Chain-of-thought (CoT) traces have been shown to improve performance of large language models on a plethora of reasoning tasks, yet there is no consensus on the mechanism by which this boost is achieved. To shed more light on this, we introduce Causal CoT Graphs (CCGraphs), which are directed acyclic graphs automatically extracted from reasoning traces that model fine-grained causal dependencies in language-model outputs. A collection of 1671 mathematical reasoning problems from MATH500, GSM8K, and AIME, together with their associated CCGraphs, has been compiled into our dataset -- KisMATH. Our detailed empirical analysis with 15 open-weight LLMs shows that (i) reasoning nodes in the CCGraphs are causal contributors to the final answer, which we argue is constitutive of reasoning; and (ii) LLMs emphasize the reasoning paths captured by the CCGraphs, indicating that the models internally realize structures similar to our graphs. KisMATH enables controlled, graph-aligned interventions and opens avenues for further investigation into the role of CoT in LLM reasoning.

### Paper 6: [2508.01191]
**Title:** Is Chain-of-Thought Reasoning of LLMs a Mirage? A Data Distribution Lens
**Category:** cs.AI
**Score:** 0.8169
**In MiniLM top-20:** True

Chain-of-Thought (CoT) prompting has been shown to be effective in eliciting structured reasoning (i.e., CoT reasoning) from large language models (LLMs). Regardless of its popularity, recent studies expose its failures in some reasoning tasks, raising fundamental questions about the nature of CoT reasoning. In this work, we propose a data distribution lens to understand when and why CoT reasoning succeeds or fails. We hypothesize that CoT reasoning reflects a structured inductive bias learned from in-distribution data, enabling models to conditionally generate reasoning trajectories that approximate those observed during training. As such, the effectiveness of CoT reasoning is fundamentally governed by the nature and degree of distribution discrepancy between training data and test queries. Guided by this lens, we dissect CoT reasoning via three dimensions: task, length, and format. To test the hypothesis, we introduce DataAlchemy, an abstract and fully controllable environment that trains LLMs from scratch and systematically probes them under various distribution conditions. Through rigorous controlled experiments, we reveal that CoT reasoning is a brittle mirage when it is pushed beyond training distributions, emphasizing the ongoing challenge of achieving genuine and generalizable reasoning.

### Paper 7: [2601.10775]
**Title:** LLMs for Game Theory: Entropy-Guided In-Context Learning and Adaptive CoT Reasoning
**Category:** cs.CL
**Score:** 0.8106
**In MiniLM top-20:** True

We propose a novel LLM-based framework for reasoning in discrete, game-theoretic tasks, illustrated with \emph{Tic-Tac-Toe}. The method integrates in-context learning with entropy-guided chain-of-thought (CoT) reasoning and adaptive context retrieval. The model dynamically adjusts both the number of retrieved examples and reasoning paths according to token-level uncertainty: concise reasoning with minimal context is used when uncertainty is low, whereas higher uncertainty triggers expanded multi-path CoT exploration. Experimental evaluation against a sub-optimal algorithmic opponent shows that entropy-aware adaptive reasoning substantially improves decision quality, increasing the average game outcome from \(-11.6\%\) with the baseline LLM to \(+9.5\%\) with entropy-guided adaptive reasoning over 100 games (win = +1, tie = 0, loss = -1), while maintaining a relatively low number of LLM queries per game. Statistical validation confirms that the improvement is significant, and correlation analysis reveals a negative association between token-level entropy and move optimality. These findings demonstrate that uncertainty-guided adaptive reasoning effectively enhances LLM performance in sequential decision-making environments.

### Paper 8: [2501.01203]
**Title:** HetGCoT: Heterogeneous Graph-Enhanced Chain-of-Thought LLM Reasoning for Academic Question Answering
**Category:** cs.SI
**Score:** 0.7871
**In MiniLM top-20:** True

Academic question answering (QA) in heterogeneous scholarly networks presents unique challenges requiring both structural understanding and interpretable reasoning. While graph neural networks (GNNs) capture structured graph information and large language models (LLMs) demonstrate strong capabilities in semantic comprehension, current approaches lack integration at the reasoning level. We propose HetGCoT, a framework enabling LLMs to effectively leverage and learn information from graphs to reason interpretable academic QA results. Our framework introduces three technical contributions: (1) a framework that transforms heterogeneous graph structural information into LLM-processable reasoning chains, (2) an adaptive metapath selection mechanism identifying relevant subgraphs for specific queries, and (3) a multi-step reasoning strategy systematically incorporating graph contexts into the reasoning process. Experiments on OpenAlex and DBLP datasets show our approach outperforms all sota baselines. The framework demonstrates adaptability across different LLM architectures and applicability to various scholarly question answering tasks.

### Paper 9: [2503.10095]
**Title:** Cognitive-Mental-LLM: Evaluating Reasoning in Large Language Models for Mental Health Prediction via Online Text
**Category:** cs.CL
**Score:** 0.7825
**In MiniLM top-20:** True

Large Language Models (LLMs) have demonstrated potential in predicting mental health outcomes from online text, yet traditional classification methods often lack interpretability and robustness. This study evaluates structured reasoning techniques-Chain-of-Thought (CoT), Self-Consistency (SC-CoT), and Tree-of-Thought (ToT)-to improve classification accuracy across multiple mental health datasets sourced from Reddit. We analyze reasoning-driven prompting strategies, including Zero-shot CoT and Few-shot CoT, using key performance metrics such as Balanced Accuracy, F1 score, and Sensitivity/Specificity. Our findings indicate that reasoning-enhanced techniques improve classification performance over direct prediction, particularly in complex cases. Compared to baselines such as Zero Shot non-CoT Prompting, and fine-tuned pre-trained transformers such as BERT and Mental-RoBerta, and fine-tuned Open Source LLMs such as Mental Alpaca and Mental-Flan-T5, reasoning-driven LLMs yield notable gains on datasets like Dreaddit (+0.52\% over M-LLM, +0.82\% over BERT) and SDCNL (+4.67\% over M-LLM, +2.17\% over BERT). However, performance declines in Depression Severity, and CSSRS predictions suggest dataset-specific limitations, likely due to our using a more extensive test set. Among prompting strategies, Few-shot CoT consistently outperforms others, reinforcing the effectiveness of reasoning-driven LLMs. Nonetheless, dataset variability highlights challenges in model reliability and interpretability. This study provides a comprehensive benchmark of reasoning-based LLM techniques for mental health text classification. It offers insights into their potential for scalable clinical applications while identifying key challenges for future improvements.

### Paper 10: [2601.03682]
**Title:** From Implicit to Explicit: Token-Efficient Logical Supervision for Mathematical Reasoning in LLMs
**Category:** cs.CL
**Score:** 0.7694
**In MiniLM top-20:** True

Recent studies reveal that large language models (LLMs) exhibit limited logical reasoning abilities in mathematical problem-solving, instead often relying on pattern-matching and memorization. We systematically analyze this limitation, focusing on logical relationship understanding, which is a core capability underlying genuine logical reasoning, and reveal that errors related to this capability account for over 90\% of incorrect predictions, with Chain-of-Thought Supervised Fine-Tuning (CoT-SFT) failing to substantially reduce these errors. To address this bottleneck, we propose First-Step Logical Reasoning (FSLR), a lightweight training framework targeting logical relationship understanding. Our key insight is that the first planning step-identifying which variables to use and which operation to apply-encourages the model to derive logical relationships directly from the problem statement. By training models on this isolated step, FSLR provides explicit supervision for logical relationship understanding, unlike CoT-SFT which implicitly embeds such relationships within complete solution trajectories. Extensive experiments across multiple models and datasets demonstrate that FSLR consistently outperforms CoT-SFT under both in-distribution and out-of-distribution settings, with average improvements of 3.2\% and 4.6\%, respectively. Moreover, FSLR achieves 4-6x faster training and reduces training token consumption by over 80\%.

### Paper 11: [2510.24940]
**Title:** SemCoT: Accelerating Chain-of-Thought Reasoning through Semantically-Aligned Implicit Tokens
**Category:** cs.CL
**Score:** 0.7606
**In MiniLM top-20:** True

The verbosity of Chain-of-Thought (CoT) reasoning hinders its mass deployment in efficiency-critical applications. Recently, implicit CoT approaches have emerged, which encode reasoning steps within LLM's hidden embeddings (termed ``implicit reasoning'') rather than explicit tokens. This approach accelerates CoT by reducing the reasoning length and bypassing some LLM components. However, existing implicit CoT methods face two significant challenges: (1) they fail to preserve the semantic alignment between the implicit reasoning (when transformed to natural language) and the ground-truth reasoning, resulting in a significant CoT performance degradation, and (2) they focus on reducing the length of the implicit reasoning; however, they neglect the considerable time cost for an LLM to generate one individual implicit reasoning token. To tackle these challenges, we propose a novel semantically-aligned implicit CoT framework termed SemCoT. In particular, for the first challenge, we design a contrastively trained sentence transformer that evaluates semantic alignment between implicit and explicit reasoning, which is used to enforce semantic preservation during implicit reasoning optimization. To address the second challenge, we introduce an efficient implicit reasoning generator by finetuning a lightweight language model using knowledge distillation. This generator is guided by our sentence transformer to distill ground-truth reasoning into semantically aligned implicit reasoning, while also optimizing for accuracy. SemCoT is the first approach that enhances CoT efficiency by jointly optimizing token-level generation speed and preserving semantic alignment with ground-truth reasoning. Extensive experiments demonstrate the superior performance of SemCoT compared to state-of-the-art methods in both efficiency and effectiveness. Our code can be found at https://github.com/YinhanHe123/SemCoT/.

### Paper 12: [2305.14934]
**Title:** GRACE: Discriminator-Guided Chain-of-Thought Reasoning
**Category:** cs.CL
**Score:** 0.7592
**In MiniLM top-20:** True

In the context of multi-step reasoning, e.g., with chain-of-thought, language models (LMs) can easily assign a high likelihood to incorrect steps. As a result, decoding strategies that optimize for solution likelihood often yield incorrect solutions. To address this issue, we propose Guiding chain-of-thought ReAsoning with a CorrectnEss Discriminator (GRACE), a stepwise decoding approach that steers the decoding process towards producing correct reasoning steps. GRACE employs a step-level verifier or discriminator trained with a contrastive loss over correct and incorrect steps, which is used during decoding to score next-step candidates based on their correctness. Importantly, GRACE only requires sampling from the LM, without the need for LM training or fine-tuning. Using models from FLAN-T5 and LLaMA families, we evaluate GRACE over four math and two symbolic reasoning tasks, where it exhibits substantial performance gains compared to greedy decoding, verifiers, and self-consistency in most settings. When further combined with self-consistency, GRACE outperforms all the baselines by sizeable margins. Human and LLM evaluations over GSM8K show that GRACE not only improves the final answer accuracy but also the correctness of the intermediate reasoning. Our implementation can be accessed at https://github.com/mukhal/grace.

### Paper 13 [DIVERGENT]: [2502.15401]
**Title:** Problem-Solving Logic Guided Curriculum In-Context Learning for LLMs Complex Reasoning
**Category:** cs.CL
**Score:** 0.7509
**In MiniLM top-20:** False

In-context learning (ICL) can significantly enhance the complex reasoning capabilities of large language models (LLMs), with the key lying in the selection and ordering of demonstration examples. Previous methods typically relied on simple features to measure the relevance between examples. We argue that these features are not sufficient to reflect the intrinsic connections between examples. In this study, we propose a curriculum ICL strategy guided by problem-solving logic. We select demonstration examples by analyzing the problem-solving logic and order them based on curriculum learning. Specifically, we constructed a problem-solving logic instruction set based on the BREAK dataset and fine-tuned a language model to analyze the problem-solving logic of examples. Subsequently, we selected appropriate demonstration examples based on problem-solving logic and assessed their difficulty according to the number of problem-solving steps. In accordance with the principles of curriculum learning, we ordered the examples from easy to hard to serve as contextual prompts. Experimental results on multiple benchmarks indicate that our method outperforms previous ICL approaches in terms of performance and efficiency, effectively enhancing the complex reasoning capabilities of LLMs. Our project will be released at https://github.com/maxuetao/CurriculumICL

### Paper 14: [2601.09805]
**Title:** Improving Chain-of-Thought for Logical Reasoning via Attention-Aware Intervention
**Category:** cs.AI
**Score:** 0.7507
**In MiniLM top-20:** True

Modern logical reasoning with LLMs primarily relies on employing complex interactive frameworks that decompose the reasoning process into subtasks solved through carefully designed prompts or requiring external resources (e.g., symbolic solvers) to exploit their strong logical structures. While interactive approaches introduce additional overhead or depend on external components, which limit their scalability. In this work, we introduce a non-interactive, end-to-end framework for reasoning tasks, enabling reasoning to emerge within the model itself-improving generalization while preserving analyzability without any external resources. We show that introducing structural information into the few-shot prompt activates a subset of attention heads that patterns aligned with logical reasoning operators. Building on this insight, we propose Attention-Aware Intervention (AAI), an inference-time intervention method that reweights attention scores across selected heads identified by their logical patterns. AAI offers an efficient way to steer the model's reasoning toward leveraging prior knowledge through attention modulation. Extensive experiments show that AAI enhances logical reasoning performance across diverse benchmarks, and model architectures, while incurring negligible additional computational overhead. Code is available at https://github.com/phuongnm94/aai_for_logical_reasoning.

### Paper 15 [DIVERGENT]: [2411.11930]
**Title:** AtomThink: Multimodal Slow Thinking with Atomic Step Reasoning
**Category:** cs.CV
**Score:** 0.7449
**In MiniLM top-20:** False

In this paper, we address the challenging task of multimodal reasoning by incorporating the notion of ``slow thinking'' into multimodal large language models (MLLMs). Our core idea is that models can learn to adaptively use different levels of reasoning to tackle questions of varying complexity. We propose a novel paradigm of Self-structured Chain of Thought (SCoT), which consists of minimal semantic atomic steps. Unlike existing methods that rely on structured templates or free-form paradigms, our method not only generates flexible CoT structures for various complex tasks but also mitigates the phenomenon of overthinking for easier tasks. To introduce structured reasoning into visual cognition, we design a novel AtomThink framework with four key modules: (i) a data engine to generate high-quality multimodal reasoning paths; (ii) a supervised fine-tuning (SFT) process with serialized inference data; (iii) a policy-guided multi-turn inference method; and (iv) an atomic capability metric to evaluate the single-step utilization rate. Extensive experiments demonstrate that the proposed AtomThink significantly improves the performance of baseline MLLMs, achieving more than 10\% average accuracy gains on MathVista and MathVerse. Compared to state-of-the-art structured CoT approaches, our method not only achieves higher accuracy but also improves data utilization by 5 $\times$ and boosts inference efficiency by 85.3\%. Our code is publicly available at https://github.com/Kun-Xiang/AtomThink.

### Paper 16 [DIVERGENT]: [2601.04254]
**Title:** Scaling Trends for Multi-Hop Contextual Reasoning in Mid-Scale Language Models
**Category:** cs.AI
**Score:** 0.7373
**In MiniLM top-20:** False

We present a controlled study of multi-hop contextual reasoning in large language models, providing a clean demonstration of the task-method dissociation: rule-based pattern matching achieves 100% success on structured information retrieval but only 6.7% on tasks requiring cross-document reasoning, while LLM-based multi-agent systems show the inverse pattern, achieving up to 80% on reasoning tasks where rule-based methods fail. Using a synthetic evaluation framework with 120 trials across four models (LLaMA-3 8B, LLaMA-2 13B, Mixtral 8x7B, DeepSeek-V2 16B), we report three key findings: (1) Multi-agent amplification depends on base capability: statistically significant gains occur only for models with sufficient reasoning ability (p < 0.001 for LLaMA-3 8B, p = 0.014 for Mixtral), with improvements of up to 46.7 percentage points, while weaker models show no benefit, suggesting amplification rather than compensation; (2) Active parameters predict reasoning performance: Mixtral's performance aligns with its ~12B active parameters rather than 47B total, consistent with the hypothesis that inference-time compute drives reasoning capability in MoE architectures; (3) Architecture quality matters: LLaMA-3 8B outperforms LLaMA-2 13B despite fewer parameters, consistent with known training improvements. Our results provide controlled quantitative evidence for intuitions about multi-agent coordination and MoE scaling, while highlighting the dependence of multi-agent benefits on base model capability. We release our evaluation framework to support reproducible research on reasoning in mid-scale models.

### Paper 17 [DIVERGENT]: [2601.19917]
**Title:** PILOT: Planning via Internalized Latent Optimization Trajectories for Large Language Models
**Category:** cs.CL
**Score:** 0.7310
**In MiniLM top-20:** False

Strategic planning is critical for multi-step reasoning, yet compact Large Language Models (LLMs) often lack the capacity to formulate global strategies, leading to error propagation in long-horizon tasks. Our analysis reveals that LLMs possess latent reasoning capabilities that can be unlocked when conditioned on explicit plans from a teacher model; however, runtime reliance on external guidance is often impractical due to latency and availability constraints. To bridge this gap, we propose PILOT (Planning via Internalized Latent Optimization Trajectories), a non-invasive framework designed to internalize the strategic oversight of large models into intrinsic Latent Guidance. Instead of altering backbone weights, PILOT employs a lightweight Hyper-Network to synthesize a query-conditioned Latent Guidance vector. This vector acts as an internal steering mechanism, guiding the model's representations toward optimal reasoning paths. Extensive experiments on mathematical and coding benchmarks demonstrate that PILOT effectively stabilizes reasoning trajectories, consistently outperforming strong baselines (e.g., +8.9% on MATH500) with negligible inference latency.

### Paper 18 [DIVERGENT]: [2512.04359]
**Title:** Efficient Reinforcement Learning with Semantic and Token Entropy for LLM Reasoning
**Category:** cs.AI
**Score:** 0.7257
**In MiniLM top-20:** False

Reinforcement learning with verifiable rewards (RLVR) has demonstrated superior performance in enhancing the reasoning capability of large language models (LLMs). However, this accuracy-oriented learning paradigm often suffers from entropy collapse, which reduces policy exploration and limits reasoning capabilities. To address this challenge, we propose an efficient reinforcement learning framework that leverages entropy signals at both the semantic and token levels to improve reasoning. From the data perspective, we introduce semantic entropy-guided curriculum learning, organizing training data from low to high semantic entropy to guide progressive optimization from easier to more challenging tasks. For the algorithmic design, we adopt non-uniform token treatment by imposing KL regularization on low-entropy tokens that critically impact policy exploration and applying stronger constraints on high-covariance portions within these tokens. By jointly optimizing data organization and algorithmic design, our method effectively mitigates entropy collapse and enhances LLM reasoning. Experimental results across 6 benchmarks with 3 different parameter-scale base models demonstrate that our method outperforms other entropy-based approaches in improving reasoning.

### Paper 19 [DIVERGENT]: [2601.11517]
**Title:** Do explanations generalize across large reasoning models?
**Category:** cs.CL
**Score:** 0.7220
**In MiniLM top-20:** False

Large reasoning models (LRMs) produce a textual chain of thought (CoT) in the process of solving a problem, which serves as a potentially powerful tool to understand the problem by surfacing a human-readable, natural-language explanation. However, it is unclear whether these explanations generalize, i.e. whether they capture general patterns about the underlying problem rather than patterns which are esoteric to the LRM. This is a crucial question in understanding or discovering new concepts, e.g. in AI for science. We study this generalization question by evaluating a specific notion of generalizability: whether explanations produced by one LRM induce the same behavior when given to other LRMs. We find that CoT explanations often exhibit this form of generalization (i.e. they increase consistency between LRMs) and that this increased generalization is correlated with human preference rankings and post-training with reinforcement learning. We further analyze the conditions under which explanations yield consistent answers and propose a straightforward, sentence-level ensembling strategy that improves consistency. Taken together, these results prescribe caution when using LRM explanations to yield new insights and outline a framework for characterizing LRM explanation generalization.

### Paper 20: [2601.14560]
**Title:** Rewarding How Models Think Pedagogically: Integrating Pedagogical Reasoning and Thinking Rewards for LLMs in Education
**Category:** cs.CL
**Score:** 0.7211
**In MiniLM top-20:** True

Large language models (LLMs) are increasingly deployed as intelligent tutoring systems, yet research on optimizing LLMs specifically for educational contexts remains limited. Recent works have proposed reinforcement learning approaches for training LLM tutors, but these methods focus solely on optimizing visible responses while neglecting the model's internal thinking process. We introduce PedagogicalRL-Thinking, a framework that extends pedagogical alignment to reasoning LLMs in education through two novel approaches: (1) Pedagogical Reasoning Prompting, which guides internal reasoning using domain-specific educational theory rather than generic instructions; and (2) Thinking Reward, which explicitly evaluates and reinforces the pedagogical quality of the model's reasoning traces. Our experiments reveal that domain-specific, theory-grounded prompting outperforms generic prompting, and that Thinking Reward is most effective when combined with pedagogical prompting. Furthermore, models trained only on mathematics tutoring dialogues show improved performance on educational benchmarks not seen during training, while preserving the base model's factual knowledge. Our quantitative and qualitative analyses reveal that pedagogical thinking reward produces systematic reasoning trace changes, with increased pedagogical reasoning and more structured instructional decision-making in the tutor's thinking process.

---

## Review Instructions

You are reviewing the top-20 recommendations from qwen3 for the profile "Language model reasoning".
Papers marked [DIVERGENT] are in qwen3's top-20 but NOT in MiniLM's.

### Full Review (all sections required)

1. **Per-paper assessment**: For each paper:
   - Connection to seeds (direct, adjacent, provocative, noise)
   - For DIVERGENT papers especially: is this a genuinely different signal?
   - Discoverability: would a researcher find this via other means?

2. **Set-level assessment**:
   - Does this set map a research landscape or just list similar papers?
   - Coverage: methods, applications, critiques, foundations?
   - What's conspicuously absent?
   - How does the character of divergent papers differ from shared papers?

3. **Emergent observations**:
   - What kind of signal does this model capture that MiniLM doesn't?
   - Is the divergence signal (coherent, valuable) or noise (scattered, irrelevant)?
   - Any productive provocations among the recommendations?

4. **Absent researcher note**:
   - What would you need to know about the researcher to assess this properly?

5. **Metric divergence flags**:
   - Does your qualitative impression contradict quantitative expectations?
