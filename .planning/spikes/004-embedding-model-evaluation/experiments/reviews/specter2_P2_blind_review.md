# Blind Pairwise Qualitative Review

**Profile:** Language model reasoning (P2)
**Depth:** full
**Models:** Model B vs Model A (identities withheld)

## Seed Papers
  - [2506.14641] Revisiting Chain-of-Thought Prompting: Zero-shot Can Be Stronger than Few-shot (cs.CL)
  - [2501.01203] HetGCoT: Heterogeneous Graph-Enhanced Chain-of-Thought LLM Reasoning for Academic Question Answering (cs.SI)
  - [2601.03559] DiffCoT: Diffusion-styled Chain-of-Thought Reasoning in LLMs (cs.CL)
  - [2601.10775] LLMs for Game Theory: Entropy-Guided In-Context Learning and Adaptive CoT Reasoning (cs.CL)
  - [2503.10095] Cognitive-Mental-LLM: Evaluating Reasoning in Large Language Models for Mental Health Prediction via Online Text (cs.CL)

## Recommendations

### Model B Paper 1: [2601.03559]
**Title:** DiffCoT: Diffusion-styled Chain-of-Thought Reasoning in LLMs
**Category:** cs.CL
**Score:** 0.9728

Chain-of-Thought (CoT) reasoning improves multi-step mathematical problem solving in large language models but remains vulnerable to exposure bias and error accumulation, as early mistakes propagate irreversibly through autoregressive decoding. In this work, we propose DiffCoT, a diffusion-styled CoT framework that reformulates CoT reasoning as an iterative denoising process. DiffCoT integrates diffusion principles at the reasoning-step level via a sliding-window mechanism, enabling unified generation and retrospective correction of intermediate steps while preserving token-level autoregression. To maintain causal consistency, we further introduce a causal diffusion noise schedule that respects the temporal structure of reasoning chains. Extensive experiments on three multi-step CoT reasoning benchmarks across diverse model backbones demonstrate that DiffCoT consistently outperforms existing CoT preference optimization methods, yielding improved robustness and error-correction capability in CoT reasoning.

### Model B Paper 2: [2601.03769]
**Title:** EntroCoT: Enhancing Chain-of-Thought via Adaptive Entropy-Guided Segmentation
**Category:** cs.AI
**Score:** 0.9646

Chain-of-Thought (CoT) prompting has significantly enhanced the mathematical reasoning capabilities of Large Language Models. We find existing fine-tuning datasets frequently suffer from the "answer right but reasoning wrong" probelm, where correct final answers are derived from hallucinated, redundant, or logically invalid intermediate steps. This paper proposes EntroCoT, a unified framework for automatically identifying and refining low-quality CoT supervision traces. EntroCoT first proposes an entropy-based mechanism to segment the reasoning trace into multiple steps at uncertain junctures, and then introduces a Monte Carlo rollout-based mechanism to evaluate the marginal contribution of each step. By accurately filtering deceptive reasoning samples, EntroCoT constructs a high-quality dataset where every intermediate step in each reasoning trace facilitates the final answer. Extensive experiments on mathematical benchmarks demonstrate that fine-tuning on the subset constructed by EntroCoT consistently outperforms the baseslines of full-dataset supervision.

### Model B Paper 3: [2506.14641]
**Title:** Revisiting Chain-of-Thought Prompting: Zero-shot Can Be Stronger than Few-shot
**Category:** cs.CL
**Score:** 0.9644

In-Context Learning (ICL) is an essential emergent ability of Large Language Models (LLMs), and recent studies introduce Chain-of-Thought (CoT) to exemplars of ICL to enhance the reasoning capability, especially in mathematics tasks. However, given the continuous advancement of model capabilities, it remains unclear whether CoT exemplars still benefit recent, stronger models in such tasks. Through systematic experiments, we find that for recent strong models such as the Qwen2.5 series, adding traditional CoT exemplars does not improve reasoning performance compared to Zero-Shot CoT. Instead, their primary function is to align the output format with human expectations. We further investigate the effectiveness of enhanced CoT exemplars, constructed using answers from advanced models such as \texttt{Qwen2.5-Max} and \texttt{DeepSeek-R1}. Experimental results indicate that these enhanced exemplars still fail to improve the model's reasoning performance. Further analysis reveals that models tend to ignore the exemplars and focus primarily on the instructions, leading to no observable gain in reasoning ability. Overall, our findings highlight the limitations of the current ICL+CoT framework in mathematical reasoning, calling for a re-examination of the ICL paradigm and the definition of exemplars.

### Model B Paper 4: [2411.11930]
**Title:** AtomThink: Multimodal Slow Thinking with Atomic Step Reasoning
**Category:** cs.CV
**Score:** 0.9644

In this paper, we address the challenging task of multimodal reasoning by incorporating the notion of ``slow thinking'' into multimodal large language models (MLLMs). Our core idea is that models can learn to adaptively use different levels of reasoning to tackle questions of varying complexity. We propose a novel paradigm of Self-structured Chain of Thought (SCoT), which consists of minimal semantic atomic steps. Unlike existing methods that rely on structured templates or free-form paradigms, our method not only generates flexible CoT structures for various complex tasks but also mitigates the phenomenon of overthinking for easier tasks. To introduce structured reasoning into visual cognition, we design a novel AtomThink framework with four key modules: (i) a data engine to generate high-quality multimodal reasoning paths; (ii) a supervised fine-tuning (SFT) process with serialized inference data; (iii) a policy-guided multi-turn inference method; and (iv) an atomic capability metric to evaluate the single-step utilization rate. Extensive experiments demonstrate that the proposed AtomThink significantly improves the performance of baseline MLLMs, achieving more than 10\% average accuracy gains on MathVista and MathVerse. Compared to state-of-the-art structured CoT approaches, our method not only achieves higher accuracy but also improves data utilization by 5 $\times$ and boosts inference efficiency by 85.3\%. Our code is publicly available at https://github.com/Kun-Xiang/AtomThink.

### Model B Paper 5: [2601.02902]
**Title:** Logical Phase Transitions: Understanding Collapse in LLM Logical Reasoning
**Category:** cs.AI
**Score:** 0.9620

Symbolic logical reasoning is a critical yet underexplored capability of large language models (LLMs), providing reliable and verifiable decision-making in high-stakes domains such as mathematical reasoning and legal judgment. In this study, we present a systematic analysis of logical reasoning under controlled increases in logical complexity, and reveal a previously unrecognized phenomenon, which we term Logical Phase Transitions: rather than degrading smoothly, logical reasoning performance remains stable within a regime but collapses abruptly beyond a critical logical depth, mirroring physical phase transitions such as water freezing beyond a critical temperature threshold. Building on this insight, we propose Neuro-Symbolic Curriculum Tuning, a principled framework that adaptively aligns natural language with logical symbols to establish a shared representation, and reshapes training dynamics around phase-transition boundaries to progressively strengthen reasoning at increasing logical depths. Experiments on five benchmarks show that our approach effectively mitigates logical reasoning collapse at high complexity, yielding average accuracy gains of +1.26 in naive prompting and +3.95 in CoT, while improving generalization to unseen logical compositions. Code and data are available at https://github.com/AI4SS/Logical-Phase-Transitions.

### Model B Paper 6: [2507.11408]
**Title:** KisMATH: Do LLMs Have Knowledge of Implicit Structures in Mathematical Reasoning?
**Category:** cs.CL
**Score:** 0.9590

Chain-of-thought (CoT) traces have been shown to improve performance of large language models on a plethora of reasoning tasks, yet there is no consensus on the mechanism by which this boost is achieved. To shed more light on this, we introduce Causal CoT Graphs (CCGraphs), which are directed acyclic graphs automatically extracted from reasoning traces that model fine-grained causal dependencies in language-model outputs. A collection of 1671 mathematical reasoning problems from MATH500, GSM8K, and AIME, together with their associated CCGraphs, has been compiled into our dataset -- KisMATH. Our detailed empirical analysis with 15 open-weight LLMs shows that (i) reasoning nodes in the CCGraphs are causal contributors to the final answer, which we argue is constitutive of reasoning; and (ii) LLMs emphasize the reasoning paths captured by the CCGraphs, indicating that the models internally realize structures similar to our graphs. KisMATH enables controlled, graph-aligned interventions and opens avenues for further investigation into the role of CoT in LLM reasoning.

### Model B Paper 7: [2305.14934]
**Title:** GRACE: Discriminator-Guided Chain-of-Thought Reasoning
**Category:** cs.CL
**Score:** 0.9559

In the context of multi-step reasoning, e.g., with chain-of-thought, language models (LMs) can easily assign a high likelihood to incorrect steps. As a result, decoding strategies that optimize for solution likelihood often yield incorrect solutions. To address this issue, we propose Guiding chain-of-thought ReAsoning with a CorrectnEss Discriminator (GRACE), a stepwise decoding approach that steers the decoding process towards producing correct reasoning steps. GRACE employs a step-level verifier or discriminator trained with a contrastive loss over correct and incorrect steps, which is used during decoding to score next-step candidates based on their correctness. Importantly, GRACE only requires sampling from the LM, without the need for LM training or fine-tuning. Using models from FLAN-T5 and LLaMA families, we evaluate GRACE over four math and two symbolic reasoning tasks, where it exhibits substantial performance gains compared to greedy decoding, verifiers, and self-consistency in most settings. When further combined with self-consistency, GRACE outperforms all the baselines by sizeable margins. Human and LLM evaluations over GSM8K show that GRACE not only improves the final answer accuracy but also the correctness of the intermediate reasoning. Our implementation can be accessed at https://github.com/mukhal/grace.

### Model B Paper 8: [2503.10095]
**Title:** Cognitive-Mental-LLM: Evaluating Reasoning in Large Language Models for Mental Health Prediction via Online Text
**Category:** cs.CL
**Score:** 0.9555

Large Language Models (LLMs) have demonstrated potential in predicting mental health outcomes from online text, yet traditional classification methods often lack interpretability and robustness. This study evaluates structured reasoning techniques-Chain-of-Thought (CoT), Self-Consistency (SC-CoT), and Tree-of-Thought (ToT)-to improve classification accuracy across multiple mental health datasets sourced from Reddit. We analyze reasoning-driven prompting strategies, including Zero-shot CoT and Few-shot CoT, using key performance metrics such as Balanced Accuracy, F1 score, and Sensitivity/Specificity. Our findings indicate that reasoning-enhanced techniques improve classification performance over direct prediction, particularly in complex cases. Compared to baselines such as Zero Shot non-CoT Prompting, and fine-tuned pre-trained transformers such as BERT and Mental-RoBerta, and fine-tuned Open Source LLMs such as Mental Alpaca and Mental-Flan-T5, reasoning-driven LLMs yield notable gains on datasets like Dreaddit (+0.52\% over M-LLM, +0.82\% over BERT) and SDCNL (+4.67\% over M-LLM, +2.17\% over BERT). However, performance declines in Depression Severity, and CSSRS predictions suggest dataset-specific limitations, likely due to our using a more extensive test set. Among prompting strategies, Few-shot CoT consistently outperforms others, reinforcing the effectiveness of reasoning-driven LLMs. Nonetheless, dataset variability highlights challenges in model reliability and interpretability. This study provides a comprehensive benchmark of reasoning-based LLM techniques for mental health text classification. It offers insights into their potential for scalable clinical applications while identifying key challenges for future improvements.

### Model B Paper 9: [2601.04157]
**Title:** FLEx: Language Modeling with Few-shot Language Explanations
**Category:** cs.CL
**Score:** 0.9553

Language models have become effective at a wide range of tasks, from math problem solving to open-domain question answering. However, they still make mistakes, and these mistakes are often repeated across related queries. Natural language explanations can help correct these errors, but collecting them at scale may be infeasible, particularly in domains where expert annotators are required. To address this issue, we introduce FLEx ($\textbf{F}$ew-shot $\textbf{L}$anguage $\textbf{Ex}$planations), a method for improving model behavior using a small number of explanatory examples. FLEx selects representative model errors using embedding-based clustering, verifies that the associated explanations correct those errors, and summarizes them into a prompt prefix that is prepended at inference-time. This summary guides the model to avoid similar errors on new inputs, without modifying model weights. We evaluate FLEx on CounterBench, GSM8K, and ReasonIF. We find that FLEx consistently outperforms chain-of-thought (CoT) prompting across all three datasets and reduces up to 83\% of CoT's remaining errors.

### Model B Paper 10: [2601.06098]
**Title:** Automatic Question Generation for Intuitive Learning Utilizing Causal Graph Guided Chain of Thought Reasoning
**Category:** cs.AI
**Score:** 0.9538

Intuitive learning is crucial for developing deep conceptual understanding, especially in STEM education, where students often struggle with abstract and interconnected concepts. Automatic question generation has become an effective strategy for personalized and adaptive learning. However, its effectiveness is hindered by hallucinations in large language models (LLMs), which may generate factually incorrect, ambiguous, or pedagogically inconsistent questions. To address this issue, we propose a novel framework that combines causal-graph-guided Chain-of-Thought (CoT) reasoning with a multi-agent LLM architecture. This approach ensures the generation of accurate, meaningful, and curriculum-aligned questions. Causal graphs provide an explicit representation of domain knowledge, while CoT reasoning facilitates a structured, step-by-step traversal of related concepts. Dedicated LLM agents are assigned specific tasks such as graph pathfinding, reasoning, validation, and output, all working within domain constraints. A dual validation mechanism-at both the conceptual and output stages-greatly reduces hallucinations. Experimental results demonstrate up to a 70% improvement in quality compared to reference methods and yielded highly favorable outcomes in subjective evaluations.

### Model B Paper 11: [2510.25065]
**Title:** Reasoning-Aware Proxy Reward Model using Process Mining
**Category:** cs.AI
**Score:** 0.9538

Recent advances in sparse reward policy gradient methods have enabled effective reinforcement learning (RL) for language models post-training. However, for reasoning tasks such as mathematical problem solving, binarized outcome rewards provide limited feedback on intermediate reasoning steps. While some studies have attempted to address this issue by estimating overall reasoning quality, it remains unclear whether these rewards are reliable proxies for the quality of stepwise reasoning. In this study, we consider reasoning as a structured process and propose \textbf{TACReward}, the reward model that can be seamlessly integrated into sparse reward policy gradient methods without additional human annotation costs or architectural modifications. TACReward aggregates stepwise structural deviations between teacher and policy reasoning using process mining techniques, producing a scalar output reward range of $[0, 1]$ to indicate reasoning quality. Experiments on multiple mathematical reasoning benchmarks demonstrate that integrating the TACReward into sparse reward frameworks encourages the policy model to improve the structural quality of reasoning. Consequently, this leads to consistent performance improvements over existing sparse reward frameworks. Our code and model are publicly available at \href{https://github.com/Thrillcrazyer/TACReward}{GitHub} and \href{https://huggingface.co/Thrillcrazyer/TACReward7B}{HuggingFace}

### Model B Paper 12: [2601.10775]
**Title:** LLMs for Game Theory: Entropy-Guided In-Context Learning and Adaptive CoT Reasoning
**Category:** cs.CL
**Score:** 0.9538

We propose a novel LLM-based framework for reasoning in discrete, game-theoretic tasks, illustrated with \emph{Tic-Tac-Toe}. The method integrates in-context learning with entropy-guided chain-of-thought (CoT) reasoning and adaptive context retrieval. The model dynamically adjusts both the number of retrieved examples and reasoning paths according to token-level uncertainty: concise reasoning with minimal context is used when uncertainty is low, whereas higher uncertainty triggers expanded multi-path CoT exploration. Experimental evaluation against a sub-optimal algorithmic opponent shows that entropy-aware adaptive reasoning substantially improves decision quality, increasing the average game outcome from \(-11.6\%\) with the baseline LLM to \(+9.5\%\) with entropy-guided adaptive reasoning over 100 games (win = +1, tie = 0, loss = -1), while maintaining a relatively low number of LLM queries per game. Statistical validation confirms that the improvement is significant, and correlation analysis reveals a negative association between token-level entropy and move optimality. These findings demonstrate that uncertainty-guided adaptive reasoning effectively enhances LLM performance in sequential decision-making environments.

### Model B Paper 13: [2601.08058]
**Title:** Reasoning Beyond Chain-of-Thought: A Latent Computational Mode in Large Language Models
**Category:** cs.CL
**Score:** 0.9529

Chain-of-Thought (CoT) prompting has improved the reasoning performance of large language models (LLMs), but it remains unclear why it works and whether it is the unique mechanism for triggering reasoning in large language models. In this work, we study this question by directly analyzing and intervening on the internal representations of LLMs with Sparse Autoencoders (SAEs), identifying a small set of latent features that are causally associated with LLM reasoning behavior. Across multiple model families and reasoning benchmarks, we find that steering a single reasoning-related latent feature can substantially improve accuracy without explicit CoT prompting. For large models, latent steering achieves performance comparable to standard CoT prompting while producing more efficient outputs. We further observe that this reasoning-oriented internal state is triggered early in generation and can override prompt-level instructions that discourage explicit reasoning. Overall, our results suggest that multi-step reasoning in LLMs is supported by latent internal activations that can be externally activated, while CoT prompting is one effective, but not unique, way of activating this mechanism rather than its necessary cause.

### Model B Paper 14: [2601.03682]
**Title:** From Implicit to Explicit: Token-Efficient Logical Supervision for Mathematical Reasoning in LLMs
**Category:** cs.CL
**Score:** 0.9527

Recent studies reveal that large language models (LLMs) exhibit limited logical reasoning abilities in mathematical problem-solving, instead often relying on pattern-matching and memorization. We systematically analyze this limitation, focusing on logical relationship understanding, which is a core capability underlying genuine logical reasoning, and reveal that errors related to this capability account for over 90\% of incorrect predictions, with Chain-of-Thought Supervised Fine-Tuning (CoT-SFT) failing to substantially reduce these errors. To address this bottleneck, we propose First-Step Logical Reasoning (FSLR), a lightweight training framework targeting logical relationship understanding. Our key insight is that the first planning step-identifying which variables to use and which operation to apply-encourages the model to derive logical relationships directly from the problem statement. By training models on this isolated step, FSLR provides explicit supervision for logical relationship understanding, unlike CoT-SFT which implicitly embeds such relationships within complete solution trajectories. Extensive experiments across multiple models and datasets demonstrate that FSLR consistently outperforms CoT-SFT under both in-distribution and out-of-distribution settings, with average improvements of 3.2\% and 4.6\%, respectively. Moreover, FSLR achieves 4-6x faster training and reduces training token consumption by over 80\%.

### Model B Paper 15: [2501.01203]
**Title:** HetGCoT: Heterogeneous Graph-Enhanced Chain-of-Thought LLM Reasoning for Academic Question Answering
**Category:** cs.SI
**Score:** 0.9519

Academic question answering (QA) in heterogeneous scholarly networks presents unique challenges requiring both structural understanding and interpretable reasoning. While graph neural networks (GNNs) capture structured graph information and large language models (LLMs) demonstrate strong capabilities in semantic comprehension, current approaches lack integration at the reasoning level. We propose HetGCoT, a framework enabling LLMs to effectively leverage and learn information from graphs to reason interpretable academic QA results. Our framework introduces three technical contributions: (1) a framework that transforms heterogeneous graph structural information into LLM-processable reasoning chains, (2) an adaptive metapath selection mechanism identifying relevant subgraphs for specific queries, and (3) a multi-step reasoning strategy systematically incorporating graph contexts into the reasoning process. Experiments on OpenAlex and DBLP datasets show our approach outperforms all sota baselines. The framework demonstrates adaptability across different LLM architectures and applicability to various scholarly question answering tasks.

### Model B Paper 16: [2510.24940]
**Title:** SemCoT: Accelerating Chain-of-Thought Reasoning through Semantically-Aligned Implicit Tokens
**Category:** cs.CL
**Score:** 0.9508

The verbosity of Chain-of-Thought (CoT) reasoning hinders its mass deployment in efficiency-critical applications. Recently, implicit CoT approaches have emerged, which encode reasoning steps within LLM's hidden embeddings (termed ``implicit reasoning'') rather than explicit tokens. This approach accelerates CoT by reducing the reasoning length and bypassing some LLM components. However, existing implicit CoT methods face two significant challenges: (1) they fail to preserve the semantic alignment between the implicit reasoning (when transformed to natural language) and the ground-truth reasoning, resulting in a significant CoT performance degradation, and (2) they focus on reducing the length of the implicit reasoning; however, they neglect the considerable time cost for an LLM to generate one individual implicit reasoning token. To tackle these challenges, we propose a novel semantically-aligned implicit CoT framework termed SemCoT. In particular, for the first challenge, we design a contrastively trained sentence transformer that evaluates semantic alignment between implicit and explicit reasoning, which is used to enforce semantic preservation during implicit reasoning optimization. To address the second challenge, we introduce an efficient implicit reasoning generator by finetuning a lightweight language model using knowledge distillation. This generator is guided by our sentence transformer to distill ground-truth reasoning into semantically aligned implicit reasoning, while also optimizing for accuracy. SemCoT is the first approach that enhances CoT efficiency by jointly optimizing token-level generation speed and preserving semantic alignment with ground-truth reasoning. Extensive experiments demonstrate the superior performance of SemCoT compared to state-of-the-art methods in both efficiency and effectiveness. Our code can be found at https://github.com/YinhanHe123/SemCoT/.

### Model B Paper 17: [2512.20144]
**Title:** Multi-hop Reasoning via Early Knowledge Alignment
**Category:** cs.CL
**Score:** 0.9488

Retrieval-Augmented Generation (RAG) has emerged as a powerful paradigm for Large Language Models (LLMs) to address knowledge-intensive queries requiring domain-specific or up-to-date information. To handle complex multi-hop questions that are challenging for single-step retrieval, iterative RAG approaches incorporating reinforcement learning have been proposed. However, existing iterative RAG systems typically plan to decompose questions without leveraging information about the available retrieval corpus, leading to inefficient retrieval and reasoning chains that cascade into suboptimal performance. In this paper, we introduce Early Knowledge Alignment (EKA), a simple but effective module that aligns LLMs with retrieval set before planning in iterative RAG systems with contextually relevant retrieved knowledge. Extensive experiments on six standard RAG datasets demonstrate that by establishing a stronger reasoning foundation, EKA significantly improves retrieval precision, reduces cascading errors, and enhances both performance and efficiency. Our analysis from an entropy perspective demonstrate that incorporating early knowledge reduces unnecessary exploration during the reasoning process, enabling the model to focus more effectively on relevant information subsets. Moreover, EKA proves effective as a versatile, training-free inference strategy that scales seamlessly to large models. Generalization tests across diverse datasets and retrieval corpora confirm the robustness of our approach. Overall, EKA advances the state-of-the-art in iterative RAG systems while illuminating the critical interplay between structured reasoning and efficient exploration in reinforcement learning-augmented frameworks. The code is released at \href{https://github.com/yxzwang/EarlyKnowledgeAlignment}{Github}.

### Model B Paper 18: [2601.02739]
**Title:** Mitigating Prompt-Induced Hallucinations in Large Language Models via Structured Reasoning
**Category:** cs.CL
**Score:** 0.9483

To address hallucination issues in large language models (LLMs), this paper proposes a method for mitigating prompt-induced hallucinations. Building on a knowledge distillation chain-style model, we introduce a code module to guide knowledge-graph exploration and incorporate code as part of the chain-of-thought prompt, forming an external knowledge input that provides more accurate and structured information to the model. Based on this design, we develop an improved knowledge distillation chain-style model and leverage it to analyze and constrain the reasoning process of LLMs, thereby improving inference accuracy. We empirically evaluate the proposed approach using GPT-4 and LLaMA-3.3 on multiple public datasets. Experimental results demonstrate that incorporating code modules significantly enhances the model's ability to capture contextual information and effectively mitigates prompt-induced hallucinations. Specifically, HIT@1, HIT@3, and HIT@5 improve by 15.64%, 13.38%, and 13.28%, respectively. Moreover, the proposed method achieves HIT@1, HIT@3, and HIT@5 scores exceeding 95% across several evaluation settings. These results indicate that the proposed approach substantially reduces hallucination behavior while improving the accuracy and verifiability of large language models.

### Model B Paper 19: [2601.01011]
**Title:** Intention Collapse: Intention-Level Metrics for Reasoning in Language Models
**Category:** cs.CL
**Score:** 0.9476

Language generation maps a rich, high-dimensional internal state to a single token sequence. We study this many-to-one mapping through the lens of intention collapse: the projection from an internal intention space I to an external language space L. We introduce three cheap, model-agnostic metrics computed on a pre-collapse state I: (i) intention entropy Hint(I), (ii) effective dimensionality deff(I), and (iii) recoverability Recov(I), operationalized as probe AUROC for predicting eventual success. We evaluate these metrics in a 3x3 study across models (Mistral-7B, LLaMA-3.1-8B, Qwen-2.5-7B) and benchmarks (GSM8K, ARC-Challenge, AQUA-RAT), comparing baseline, chain-of-thought (CoT), and a babble control (n=200 items per cell). CoT increases average accuracy from 34.2% to 47.3% (+13.1 pp), driven by large gains on GSM8K but consistent degradations on ARC-Challenge. Across models, CoT induces distinct entropy regimes relative to baseline, dH = Hint(CoT) - Hint(Base): Mistral shows dH < 0 (lower-entropy CoT), whereas LLaMA shows dH > 0 (higher-entropy CoT), highlighting heterogeneity in CoT-induced internal uncertainty. Finally, probe AUROC is significantly above chance in a subset of settings and can dissociate from behavioral accuracy (e.g., high AUROC alongside lower CoT accuracy on ARC-Challenge for Qwen), suggesting that informative internal signal is not always reliably converted into a final discrete decision under constrained response formats.

### Model B Paper 20: [2508.01191]
**Title:** Is Chain-of-Thought Reasoning of LLMs a Mirage? A Data Distribution Lens
**Category:** cs.AI
**Score:** 0.9474

Chain-of-Thought (CoT) prompting has been shown to be effective in eliciting structured reasoning (i.e., CoT reasoning) from large language models (LLMs). Regardless of its popularity, recent studies expose its failures in some reasoning tasks, raising fundamental questions about the nature of CoT reasoning. In this work, we propose a data distribution lens to understand when and why CoT reasoning succeeds or fails. We hypothesize that CoT reasoning reflects a structured inductive bias learned from in-distribution data, enabling models to conditionally generate reasoning trajectories that approximate those observed during training. As such, the effectiveness of CoT reasoning is fundamentally governed by the nature and degree of distribution discrepancy between training data and test queries. Guided by this lens, we dissect CoT reasoning via three dimensions: task, length, and format. To test the hypothesis, we introduce DataAlchemy, an abstract and fully controllable environment that trains LLMs from scratch and systematically probes them under various distribution conditions. Through rigorous controlled experiments, we reveal that CoT reasoning is a brittle mirage when it is pushed beyond training distributions, emphasizing the ongoing challenge of achieving genuine and generalizable reasoning.

---


### Model A Paper 1: [2506.14641]
**Title:** Revisiting Chain-of-Thought Prompting: Zero-shot Can Be Stronger than Few-shot
**Category:** cs.CL
**Score:** 0.8454

In-Context Learning (ICL) is an essential emergent ability of Large Language Models (LLMs), and recent studies introduce Chain-of-Thought (CoT) to exemplars of ICL to enhance the reasoning capability, especially in mathematics tasks. However, given the continuous advancement of model capabilities, it remains unclear whether CoT exemplars still benefit recent, stronger models in such tasks. Through systematic experiments, we find that for recent strong models such as the Qwen2.5 series, adding traditional CoT exemplars does not improve reasoning performance compared to Zero-Shot CoT. Instead, their primary function is to align the output format with human expectations. We further investigate the effectiveness of enhanced CoT exemplars, constructed using answers from advanced models such as \texttt{Qwen2.5-Max} and \texttt{DeepSeek-R1}. Experimental results indicate that these enhanced exemplars still fail to improve the model's reasoning performance. Further analysis reveals that models tend to ignore the exemplars and focus primarily on the instructions, leading to no observable gain in reasoning ability. Overall, our findings highlight the limitations of the current ICL+CoT framework in mathematical reasoning, calling for a re-examination of the ICL paradigm and the definition of exemplars.

### Model A Paper 2: [2508.01191]
**Title:** Is Chain-of-Thought Reasoning of LLMs a Mirage? A Data Distribution Lens
**Category:** cs.AI
**Score:** 0.8218

Chain-of-Thought (CoT) prompting has been shown to be effective in eliciting structured reasoning (i.e., CoT reasoning) from large language models (LLMs). Regardless of its popularity, recent studies expose its failures in some reasoning tasks, raising fundamental questions about the nature of CoT reasoning. In this work, we propose a data distribution lens to understand when and why CoT reasoning succeeds or fails. We hypothesize that CoT reasoning reflects a structured inductive bias learned from in-distribution data, enabling models to conditionally generate reasoning trajectories that approximate those observed during training. As such, the effectiveness of CoT reasoning is fundamentally governed by the nature and degree of distribution discrepancy between training data and test queries. Guided by this lens, we dissect CoT reasoning via three dimensions: task, length, and format. To test the hypothesis, we introduce DataAlchemy, an abstract and fully controllable environment that trains LLMs from scratch and systematically probes them under various distribution conditions. Through rigorous controlled experiments, we reveal that CoT reasoning is a brittle mirage when it is pushed beyond training distributions, emphasizing the ongoing challenge of achieving genuine and generalizable reasoning.

### Model A Paper 3: [2503.10095]
**Title:** Cognitive-Mental-LLM: Evaluating Reasoning in Large Language Models for Mental Health Prediction via Online Text
**Category:** cs.CL
**Score:** 0.8016

Large Language Models (LLMs) have demonstrated potential in predicting mental health outcomes from online text, yet traditional classification methods often lack interpretability and robustness. This study evaluates structured reasoning techniques-Chain-of-Thought (CoT), Self-Consistency (SC-CoT), and Tree-of-Thought (ToT)-to improve classification accuracy across multiple mental health datasets sourced from Reddit. We analyze reasoning-driven prompting strategies, including Zero-shot CoT and Few-shot CoT, using key performance metrics such as Balanced Accuracy, F1 score, and Sensitivity/Specificity. Our findings indicate that reasoning-enhanced techniques improve classification performance over direct prediction, particularly in complex cases. Compared to baselines such as Zero Shot non-CoT Prompting, and fine-tuned pre-trained transformers such as BERT and Mental-RoBerta, and fine-tuned Open Source LLMs such as Mental Alpaca and Mental-Flan-T5, reasoning-driven LLMs yield notable gains on datasets like Dreaddit (+0.52\% over M-LLM, +0.82\% over BERT) and SDCNL (+4.67\% over M-LLM, +2.17\% over BERT). However, performance declines in Depression Severity, and CSSRS predictions suggest dataset-specific limitations, likely due to our using a more extensive test set. Among prompting strategies, Few-shot CoT consistently outperforms others, reinforcing the effectiveness of reasoning-driven LLMs. Nonetheless, dataset variability highlights challenges in model reliability and interpretability. This study provides a comprehensive benchmark of reasoning-based LLM techniques for mental health text classification. It offers insights into their potential for scalable clinical applications while identifying key challenges for future improvements.

### Model A Paper 4: [2601.03559]
**Title:** DiffCoT: Diffusion-styled Chain-of-Thought Reasoning in LLMs
**Category:** cs.CL
**Score:** 0.8007

Chain-of-Thought (CoT) reasoning improves multi-step mathematical problem solving in large language models but remains vulnerable to exposure bias and error accumulation, as early mistakes propagate irreversibly through autoregressive decoding. In this work, we propose DiffCoT, a diffusion-styled CoT framework that reformulates CoT reasoning as an iterative denoising process. DiffCoT integrates diffusion principles at the reasoning-step level via a sliding-window mechanism, enabling unified generation and retrospective correction of intermediate steps while preserving token-level autoregression. To maintain causal consistency, we further introduce a causal diffusion noise schedule that respects the temporal structure of reasoning chains. Extensive experiments on three multi-step CoT reasoning benchmarks across diverse model backbones demonstrate that DiffCoT consistently outperforms existing CoT preference optimization methods, yielding improved robustness and error-correction capability in CoT reasoning.

### Model A Paper 5: [2601.21909]
**Title:** From Meta-Thought to Execution: Cognitively Aligned Post-Training for Generalizable and Reliable LLM Reasoning
**Category:** cs.AI
**Score:** 0.7765

Current LLM post-training methods optimize complete reasoning trajectories through Supervised Fine-Tuning (SFT) followed by outcome-based Reinforcement Learning (RL). While effective, a closer examination reveals a fundamental gap: this approach does not align with how humans actually solve problems. Human cognition naturally decomposes problem-solving into two distinct stages: first acquiring abstract strategies (i.e., meta-knowledge) that generalize across problems, then adapting them to specific instances. In contrast, by treating complete trajectories as basic units, current methods are inherently problem-centric, entangling abstract strategies with problem-specific execution. To address this misalignment, we propose a cognitively-inspired framework that explicitly mirrors the two-stage human cognitive process. Specifically, Chain-of-Meta-Thought (CoMT) focuses supervised learning on abstract reasoning patterns without specific executions, enabling acquisition of generalizable strategies. Confidence-Calibrated Reinforcement Learning (CCRL) then optimizes task adaptation via confidence-aware rewards on intermediate steps, preventing overconfident errors from cascading and improving execution reliability. Experiments across four models and eight benchmarks show 2.19\% and 4.63\% improvements in-distribution and out-of-distribution respectively over standard methods, while reducing training time by 65-70% and token consumption by 50%, demonstrating that aligning post-training with human cognitive principles yields not only superior generalization but also enhanced training efficiency.

### Model A Paper 6: [2510.24940]
**Title:** SemCoT: Accelerating Chain-of-Thought Reasoning through Semantically-Aligned Implicit Tokens
**Category:** cs.CL
**Score:** 0.7574

The verbosity of Chain-of-Thought (CoT) reasoning hinders its mass deployment in efficiency-critical applications. Recently, implicit CoT approaches have emerged, which encode reasoning steps within LLM's hidden embeddings (termed ``implicit reasoning'') rather than explicit tokens. This approach accelerates CoT by reducing the reasoning length and bypassing some LLM components. However, existing implicit CoT methods face two significant challenges: (1) they fail to preserve the semantic alignment between the implicit reasoning (when transformed to natural language) and the ground-truth reasoning, resulting in a significant CoT performance degradation, and (2) they focus on reducing the length of the implicit reasoning; however, they neglect the considerable time cost for an LLM to generate one individual implicit reasoning token. To tackle these challenges, we propose a novel semantically-aligned implicit CoT framework termed SemCoT. In particular, for the first challenge, we design a contrastively trained sentence transformer that evaluates semantic alignment between implicit and explicit reasoning, which is used to enforce semantic preservation during implicit reasoning optimization. To address the second challenge, we introduce an efficient implicit reasoning generator by finetuning a lightweight language model using knowledge distillation. This generator is guided by our sentence transformer to distill ground-truth reasoning into semantically aligned implicit reasoning, while also optimizing for accuracy. SemCoT is the first approach that enhances CoT efficiency by jointly optimizing token-level generation speed and preserving semantic alignment with ground-truth reasoning. Extensive experiments demonstrate the superior performance of SemCoT compared to state-of-the-art methods in both efficiency and effectiveness. Our code can be found at https://github.com/YinhanHe123/SemCoT/.

### Model A Paper 7: [2601.08058]
**Title:** Reasoning Beyond Chain-of-Thought: A Latent Computational Mode in Large Language Models
**Category:** cs.CL
**Score:** 0.7566

Chain-of-Thought (CoT) prompting has improved the reasoning performance of large language models (LLMs), but it remains unclear why it works and whether it is the unique mechanism for triggering reasoning in large language models. In this work, we study this question by directly analyzing and intervening on the internal representations of LLMs with Sparse Autoencoders (SAEs), identifying a small set of latent features that are causally associated with LLM reasoning behavior. Across multiple model families and reasoning benchmarks, we find that steering a single reasoning-related latent feature can substantially improve accuracy without explicit CoT prompting. For large models, latent steering achieves performance comparable to standard CoT prompting while producing more efficient outputs. We further observe that this reasoning-oriented internal state is triggered early in generation and can override prompt-level instructions that discourage explicit reasoning. Overall, our results suggest that multi-step reasoning in LLMs is supported by latent internal activations that can be externally activated, while CoT prompting is one effective, but not unique, way of activating this mechanism rather than its necessary cause.

### Model A Paper 8: [2601.09805]
**Title:** Improving Chain-of-Thought for Logical Reasoning via Attention-Aware Intervention
**Category:** cs.AI
**Score:** 0.7546

Modern logical reasoning with LLMs primarily relies on employing complex interactive frameworks that decompose the reasoning process into subtasks solved through carefully designed prompts or requiring external resources (e.g., symbolic solvers) to exploit their strong logical structures. While interactive approaches introduce additional overhead or depend on external components, which limit their scalability. In this work, we introduce a non-interactive, end-to-end framework for reasoning tasks, enabling reasoning to emerge within the model itself-improving generalization while preserving analyzability without any external resources. We show that introducing structural information into the few-shot prompt activates a subset of attention heads that patterns aligned with logical reasoning operators. Building on this insight, we propose Attention-Aware Intervention (AAI), an inference-time intervention method that reweights attention scores across selected heads identified by their logical patterns. AAI offers an efficient way to steer the model's reasoning toward leveraging prior knowledge through attention modulation. Extensive experiments show that AAI enhances logical reasoning performance across diverse benchmarks, and model architectures, while incurring negligible additional computational overhead. Code is available at https://github.com/phuongnm94/aai_for_logical_reasoning.

### Model A Paper 9: [2601.10775]
**Title:** LLMs for Game Theory: Entropy-Guided In-Context Learning and Adaptive CoT Reasoning
**Category:** cs.CL
**Score:** 0.7505

We propose a novel LLM-based framework for reasoning in discrete, game-theoretic tasks, illustrated with \emph{Tic-Tac-Toe}. The method integrates in-context learning with entropy-guided chain-of-thought (CoT) reasoning and adaptive context retrieval. The model dynamically adjusts both the number of retrieved examples and reasoning paths according to token-level uncertainty: concise reasoning with minimal context is used when uncertainty is low, whereas higher uncertainty triggers expanded multi-path CoT exploration. Experimental evaluation against a sub-optimal algorithmic opponent shows that entropy-aware adaptive reasoning substantially improves decision quality, increasing the average game outcome from \(-11.6\%\) with the baseline LLM to \(+9.5\%\) with entropy-guided adaptive reasoning over 100 games (win = +1, tie = 0, loss = -1), while maintaining a relatively low number of LLM queries per game. Statistical validation confirms that the improvement is significant, and correlation analysis reveals a negative association between token-level entropy and move optimality. These findings demonstrate that uncertainty-guided adaptive reasoning effectively enhances LLM performance in sequential decision-making environments.

### Model A Paper 10: [2507.11408]
**Title:** KisMATH: Do LLMs Have Knowledge of Implicit Structures in Mathematical Reasoning?
**Category:** cs.CL
**Score:** 0.7466

Chain-of-thought (CoT) traces have been shown to improve performance of large language models on a plethora of reasoning tasks, yet there is no consensus on the mechanism by which this boost is achieved. To shed more light on this, we introduce Causal CoT Graphs (CCGraphs), which are directed acyclic graphs automatically extracted from reasoning traces that model fine-grained causal dependencies in language-model outputs. A collection of 1671 mathematical reasoning problems from MATH500, GSM8K, and AIME, together with their associated CCGraphs, has been compiled into our dataset -- KisMATH. Our detailed empirical analysis with 15 open-weight LLMs shows that (i) reasoning nodes in the CCGraphs are causal contributors to the final answer, which we argue is constitutive of reasoning; and (ii) LLMs emphasize the reasoning paths captured by the CCGraphs, indicating that the models internally realize structures similar to our graphs. KisMATH enables controlled, graph-aligned interventions and opens avenues for further investigation into the role of CoT in LLM reasoning.

### Model A Paper 11: [2305.14934]
**Title:** GRACE: Discriminator-Guided Chain-of-Thought Reasoning
**Category:** cs.CL
**Score:** 0.7444

In the context of multi-step reasoning, e.g., with chain-of-thought, language models (LMs) can easily assign a high likelihood to incorrect steps. As a result, decoding strategies that optimize for solution likelihood often yield incorrect solutions. To address this issue, we propose Guiding chain-of-thought ReAsoning with a CorrectnEss Discriminator (GRACE), a stepwise decoding approach that steers the decoding process towards producing correct reasoning steps. GRACE employs a step-level verifier or discriminator trained with a contrastive loss over correct and incorrect steps, which is used during decoding to score next-step candidates based on their correctness. Importantly, GRACE only requires sampling from the LM, without the need for LM training or fine-tuning. Using models from FLAN-T5 and LLaMA families, we evaluate GRACE over four math and two symbolic reasoning tasks, where it exhibits substantial performance gains compared to greedy decoding, verifiers, and self-consistency in most settings. When further combined with self-consistency, GRACE outperforms all the baselines by sizeable margins. Human and LLM evaluations over GSM8K show that GRACE not only improves the final answer accuracy but also the correctness of the intermediate reasoning. Our implementation can be accessed at https://github.com/mukhal/grace.

### Model A Paper 12: [2601.03682]
**Title:** From Implicit to Explicit: Token-Efficient Logical Supervision for Mathematical Reasoning in LLMs
**Category:** cs.CL
**Score:** 0.7386

Recent studies reveal that large language models (LLMs) exhibit limited logical reasoning abilities in mathematical problem-solving, instead often relying on pattern-matching and memorization. We systematically analyze this limitation, focusing on logical relationship understanding, which is a core capability underlying genuine logical reasoning, and reveal that errors related to this capability account for over 90\% of incorrect predictions, with Chain-of-Thought Supervised Fine-Tuning (CoT-SFT) failing to substantially reduce these errors. To address this bottleneck, we propose First-Step Logical Reasoning (FSLR), a lightweight training framework targeting logical relationship understanding. Our key insight is that the first planning step-identifying which variables to use and which operation to apply-encourages the model to derive logical relationships directly from the problem statement. By training models on this isolated step, FSLR provides explicit supervision for logical relationship understanding, unlike CoT-SFT which implicitly embeds such relationships within complete solution trajectories. Extensive experiments across multiple models and datasets demonstrate that FSLR consistently outperforms CoT-SFT under both in-distribution and out-of-distribution settings, with average improvements of 3.2\% and 4.6\%, respectively. Moreover, FSLR achieves 4-6x faster training and reduces training token consumption by over 80\%.

### Model A Paper 13: [2601.03769]
**Title:** EntroCoT: Enhancing Chain-of-Thought via Adaptive Entropy-Guided Segmentation
**Category:** cs.AI
**Score:** 0.7366

Chain-of-Thought (CoT) prompting has significantly enhanced the mathematical reasoning capabilities of Large Language Models. We find existing fine-tuning datasets frequently suffer from the "answer right but reasoning wrong" probelm, where correct final answers are derived from hallucinated, redundant, or logically invalid intermediate steps. This paper proposes EntroCoT, a unified framework for automatically identifying and refining low-quality CoT supervision traces. EntroCoT first proposes an entropy-based mechanism to segment the reasoning trace into multiple steps at uncertain junctures, and then introduces a Monte Carlo rollout-based mechanism to evaluate the marginal contribution of each step. By accurately filtering deceptive reasoning samples, EntroCoT constructs a high-quality dataset where every intermediate step in each reasoning trace facilitates the final answer. Extensive experiments on mathematical benchmarks demonstrate that fine-tuning on the subset constructed by EntroCoT consistently outperforms the baseslines of full-dataset supervision.

### Model A Paper 14: [2601.17420]
**Title:** CoT-Seg: Rethinking Segmentation with Chain-of-Thought Reasoning and Self-Correction
**Category:** cs.CV
**Score:** 0.7309

Existing works of reasoning segmentation often fall short in complex cases, particularly when addressing complicated queries and out-of-domain images. Inspired by the chain-of-thought reasoning, where harder problems require longer thinking steps/time, this paper aims to explore a system that can think step-by-step, look up information if needed, generate results, self-evaluate its own results, and refine the results, in the same way humans approach harder questions. We introduce CoT-Seg, a training-free framework that rethinks reasoning segmentation by combining chain-of-thought reasoning with self-correction. Instead of fine-tuning, CoT-Seg leverages the inherent reasoning ability of pre-trained MLLMs (GPT-4o) to decompose queries into meta-instructions, extract fine-grained semantics from images, and identify target objects even under implicit or complex prompts. Moreover, CoT-Seg incorporates a self-correction stage: the model evaluates its own segmentation against the original query and reasoning trace, identifies mismatches, and iteratively refines the mask. This tight integration of reasoning and correction significantly improves reliability and robustness, especially in ambiguous or error-prone cases. Furthermore, our CoT-Seg framework allows easy incorporation of retrieval-augmented reasoning, enabling the system to access external knowledge when the input lacks sufficient information. To showcase CoT-Seg's ability to handle very challenging cases ,we introduce a new dataset ReasonSeg-Hard. Our results highlight that combining chain-of-thought reasoning, self-correction, offers a powerful paradigm for vision-language integration driven segmentation.

### Model A Paper 15: [2601.04157]
**Title:** FLEx: Language Modeling with Few-shot Language Explanations
**Category:** cs.CL
**Score:** 0.7250

Language models have become effective at a wide range of tasks, from math problem solving to open-domain question answering. However, they still make mistakes, and these mistakes are often repeated across related queries. Natural language explanations can help correct these errors, but collecting them at scale may be infeasible, particularly in domains where expert annotators are required. To address this issue, we introduce FLEx ($\textbf{F}$ew-shot $\textbf{L}$anguage $\textbf{Ex}$planations), a method for improving model behavior using a small number of explanatory examples. FLEx selects representative model errors using embedding-based clustering, verifies that the associated explanations correct those errors, and summarizes them into a prompt prefix that is prepended at inference-time. This summary guides the model to avoid similar errors on new inputs, without modifying model weights. We evaluate FLEx on CounterBench, GSM8K, and ReasonIF. We find that FLEx consistently outperforms chain-of-thought (CoT) prompting across all three datasets and reduces up to 83\% of CoT's remaining errors.

### Model A Paper 16: [2601.02714]
**Title:** Time-Scaling Is What Agents Need Now
**Category:** cs.AI
**Score:** 0.7242

Early artificial intelligence paradigms exhibited separated cognitive functions: Neural Networks focused on "perception-representation," Reinforcement Learning on "decision-making-behavior," and Symbolic AI on "knowledge-reasoning." With Transformer-based large models and world models, these paradigms are converging into cognitive agents with closed-loop "perception-decision-action" capabilities.
  Humans solve complex problems under limited cognitive resources through temporalized sequential reasoning. Language relies on problem space search for deep semantic reasoning. While early large language models (LLMs) could generate fluent text, they lacked robust semantic reasoning capabilities. Prompting techniques like Chain-of-Thought (CoT) and Tree-of-Thought (ToT) extended reasoning paths by making intermediate steps explicit. Recent models like DeepSeek-R1 enhanced performance through explicit reasoning trajectories. However, these methods have limitations in search completeness and efficiency.
  This highlights the need for "Time-Scaling"--the systematic extension and optimization of an agent's ability to unfold reasoning over time. Time-Scaling refers to architectural design utilizing extended temporal pathways, enabling deeper problem space exploration, dynamic strategy adjustment, and enhanced metacognitive control, paralleling human sequential reasoning under cognitive constraints. It represents a critical frontier for enhancing deep reasoning and problem-solving without proportional increases in static model parameters. Advancing intelligent agent capabilities requires placing Time-Scaling principles at the forefront, positioning explicit temporal reasoning management as foundational.

### Model A Paper 17: [2501.01203]
**Title:** HetGCoT: Heterogeneous Graph-Enhanced Chain-of-Thought LLM Reasoning for Academic Question Answering
**Category:** cs.SI
**Score:** 0.7208

Academic question answering (QA) in heterogeneous scholarly networks presents unique challenges requiring both structural understanding and interpretable reasoning. While graph neural networks (GNNs) capture structured graph information and large language models (LLMs) demonstrate strong capabilities in semantic comprehension, current approaches lack integration at the reasoning level. We propose HetGCoT, a framework enabling LLMs to effectively leverage and learn information from graphs to reason interpretable academic QA results. Our framework introduces three technical contributions: (1) a framework that transforms heterogeneous graph structural information into LLM-processable reasoning chains, (2) an adaptive metapath selection mechanism identifying relevant subgraphs for specific queries, and (3) a multi-step reasoning strategy systematically incorporating graph contexts into the reasoning process. Experiments on OpenAlex and DBLP datasets show our approach outperforms all sota baselines. The framework demonstrates adaptability across different LLM architectures and applicability to various scholarly question answering tasks.

### Model A Paper 18: [2601.06098]
**Title:** Automatic Question Generation for Intuitive Learning Utilizing Causal Graph Guided Chain of Thought Reasoning
**Category:** cs.AI
**Score:** 0.7202

Intuitive learning is crucial for developing deep conceptual understanding, especially in STEM education, where students often struggle with abstract and interconnected concepts. Automatic question generation has become an effective strategy for personalized and adaptive learning. However, its effectiveness is hindered by hallucinations in large language models (LLMs), which may generate factually incorrect, ambiguous, or pedagogically inconsistent questions. To address this issue, we propose a novel framework that combines causal-graph-guided Chain-of-Thought (CoT) reasoning with a multi-agent LLM architecture. This approach ensures the generation of accurate, meaningful, and curriculum-aligned questions. Causal graphs provide an explicit representation of domain knowledge, while CoT reasoning facilitates a structured, step-by-step traversal of related concepts. Dedicated LLM agents are assigned specific tasks such as graph pathfinding, reasoning, validation, and output, all working within domain constraints. A dual validation mechanism-at both the conceptual and output stages-greatly reduces hallucinations. Experimental results demonstrate up to a 70% improvement in quality compared to reference methods and yielded highly favorable outcomes in subjective evaluations.

### Model A Paper 19: [2508.17627]
**Title:** The Evolution of Thought: Tracking LLM Overthinking via Reasoning Dynamics Analysis
**Category:** cs.CL
**Score:** 0.7172

Test-time scaling via explicit reasoning trajectories significantly boosts large language model (LLM) performance but often triggers overthinking. To explore this, we analyze reasoning through two lenses: Reasoning Length Dynamics, which reveals a compensatory trade-off between thinking and answer content length that eventually leads to thinking redundancy, and Reasoning Semantic Dynamics, which identifies semantic convergence and repetitive oscillations. These dynamics uncover an instance-specific Reasoning Completion Point (RCP), beyond which computation continues without further performance gain. Since the RCP varies across instances, we propose a Reasoning Completion Point Detector (RCPD), an inference-time early-exit method that identifies the RCP by monitoring the rank dynamics of termination tokens (e.g., </think>). Across AIME and GPQA benchmarks using Qwen3 and DeepSeek-R1, RCPD reduces token usage by up to 44% while preserving accuracy, offering a principled approach to efficient test-time scaling.

### Model A Paper 20: [2601.14560]
**Title:** Rewarding How Models Think Pedagogically: Integrating Pedagogical Reasoning and Thinking Rewards for LLMs in Education
**Category:** cs.CL
**Score:** 0.7150

Large language models (LLMs) are increasingly deployed as intelligent tutoring systems, yet research on optimizing LLMs specifically for educational contexts remains limited. Recent works have proposed reinforcement learning approaches for training LLM tutors, but these methods focus solely on optimizing visible responses while neglecting the model's internal thinking process. We introduce PedagogicalRL-Thinking, a framework that extends pedagogical alignment to reasoning LLMs in education through two novel approaches: (1) Pedagogical Reasoning Prompting, which guides internal reasoning using domain-specific educational theory rather than generic instructions; and (2) Thinking Reward, which explicitly evaluates and reinforces the pedagogical quality of the model's reasoning traces. Our experiments reveal that domain-specific, theory-grounded prompting outperforms generic prompting, and that Thinking Reward is most effective when combined with pedagogical prompting. Furthermore, models trained only on mathematics tutoring dialogues show improved performance on educational benchmarks not seen during training, while preserving the base model's factual knowledge. Our quantitative and qualitative analyses reveal that pedagogical thinking reward produces systematic reasoning trace changes, with increased pedagogical reasoning and more structured instructional decision-making in the tutor's thinking process.

---

## Review Instructions

You are reviewing recommendations from two models for the interest profile "Language model reasoning".
You do NOT know which model is which. Assess each set independently.

For EACH model's recommendation set:

1. **Per-paper relevance** (if full depth): For each paper, is it relevant to the seeds?
   - Relevant via similar topic/method
   - Relevant via adjacent community
   - Productive provocation (challenges assumptions, opens new directions)
   - Noise (no meaningful connection)

2. **Set-level assessment**:
   - Does this set map a research landscape or just list similar papers?
   - What aspects of the interest does it cover? What's missing?
   - Set coherence vs diversity balance

3. **Comparative assessment**:
   - Which set would better serve a researcher with this interest? Why?
   - What does each set find that the other misses?
   - Character of each set's errors (noise vs adjacent vs vocabulary match)

4. **Emergent observations**:
   - Anything surprising or noteworthy about the recommendations?
   - What kind of researcher would prefer each set?

5. **Absent researcher note**:
   - What would you need to know about the researcher's actual situation to assess properly?
   - What are you assuming about their needs?

6. **Metric divergence flags**:
   - Does your qualitative impression contradict any quantitative expectations?
