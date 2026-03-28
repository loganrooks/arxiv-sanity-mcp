# Single-Strategy Characterization Review

**Model:** gte
**Profile:** AI safety / alignment (P4)
**Depth:** full
**Overlap with MiniLM:** 17/20 shared, 3 unique to gte

## Seed Papers
  - [2501.19180] Enhancing Model Defense Against Jailbreaks with Proactive Safety Reasoning (cs.CR)
  - [2511.13788] Scaling Patterns in Adversarial Alignment: Evidence from Multi-LLM Jailbreak Experiments (cs.LG)
  - [2511.21214] Self-Guided Defense: Adaptive Safety Alignment for Reasoning Models via Synthesized Guidelines (cs.CL)
  - [2512.24044] Jailbreaking Attacks vs. Content Safety Filters: How Far Are We in the LLM Safety Arms Race? (cs.CR)
  - [2601.10589] Be Your Own Red Teamer: Safety Alignment via Self-Play and Reflective Experience Replay (cs.CR)

## gte Top-20 Recommendations

### Paper 1: [2501.19180]
**Title:** Enhancing Model Defense Against Jailbreaks with Proactive Safety Reasoning
**Category:** cs.CR
**Score:** 0.9304
**In MiniLM top-20:** True

Large language models (LLMs) are vital for a wide range of applications yet remain susceptible to jailbreak threats, which could lead to the generation of inappropriate responses. Conventional defenses, such as refusal and adversarial training, often fail to cover corner cases or rare domains, leaving LLMs still vulnerable to more sophisticated attacks. We propose a novel defense strategy, Safety Chain-of-Thought (SCoT), which harnesses the enhanced \textit{reasoning capabilities} of LLMs for proactive assessment of harmful inputs, rather than simply blocking them. SCoT augments any refusal training datasets to critically analyze the intent behind each request before generating answers. By employing proactive reasoning, SCoT enhances the generalization of LLMs across varied harmful queries and scenarios not covered in the safety alignment corpus. Additionally, it generates detailed refusals specifying the rules violated. Comparative evaluations show that SCoT significantly surpasses existing defenses, reducing vulnerability to out-of-distribution issues and adversarial manipulations while maintaining strong general capabilities.

### Paper 2: [2512.24044]
**Title:** Jailbreaking Attacks vs. Content Safety Filters: How Far Are We in the LLM Safety Arms Race?
**Category:** cs.CR
**Score:** 0.9241
**In MiniLM top-20:** True

As large language models (LLMs) are increasingly deployed, ensuring their safe use is paramount. Jailbreaking, adversarial prompts that bypass model alignment to trigger harmful outputs, present significant risks, with existing studies reporting high success rates in evading common LLMs. However, previous evaluations have focused solely on the models, neglecting the full deployment pipeline, which typically incorporates additional safety mechanisms like content moderation filters. To address this gap, we present the first systematic evaluation of jailbreak attacks targeting LLM safety alignment, assessing their success across the full inference pipeline, including both input and output filtering stages. Our findings yield two key insights: first, nearly all evaluated jailbreak techniques can be detected by at least one safety filter, suggesting that prior assessments may have overestimated the practical success of these attacks; second, while safety filters are effective in detection, there remains room to better balance recall and precision to further optimize protection and user experience. We highlight critical gaps and call for further refinement of detection accuracy and usability in LLM safety systems.

### Paper 3: [2511.13788]
**Title:** Scaling Patterns in Adversarial Alignment: Evidence from Multi-LLM Jailbreak Experiments
**Category:** cs.LG
**Score:** 0.9046
**In MiniLM top-20:** True

Large language models (LLMs) increasingly operate in multi-agent and safety-critical settings, raising open questions about how their vulnerabilities scale when models interact adversarially. This study examines whether larger models can systematically jailbreak smaller ones - eliciting harmful or restricted behavior despite alignment safeguards. Using standardized adversarial tasks from JailbreakBench, we simulate over 6,000 multi-turn attacker-target exchanges across major LLM families and scales (0.6B-120B parameters), measuring both harm score and refusal behavior as indicators of adversarial potency and alignment integrity. Each interaction is evaluated through aggregated harm and refusal scores assigned by three independent LLM judges, providing a consistent, model-based measure of adversarial outcomes. Aggregating results across prompts, we find a strong and statistically significant correlation between mean harm and the logarithm of the attacker-to-target size ratio (Pearson r = 0.51, p < 0.001; Spearman rho = 0.52, p < 0.001), indicating that relative model size correlates with the likelihood and severity of harmful completions. Mean harm score variance is higher across attackers (0.18) than across targets (0.10), suggesting that attacker-side behavioral diversity contributes more to adversarial outcomes than target susceptibility. Attacker refusal frequency is strongly and negatively correlated with harm (rho = -0.93, p < 0.001), showing that attacker-side alignment mitigates harmful responses. These findings reveal that size asymmetry influences robustness and provide exploratory evidence for adversarial scaling patterns, motivating more controlled investigations into inter-model alignment and safety.

### Paper 4: [2601.10589]
**Title:** Be Your Own Red Teamer: Safety Alignment via Self-Play and Reflective Experience Replay
**Category:** cs.CR
**Score:** 0.9024
**In MiniLM top-20:** True

Large Language Models (LLMs) have achieved remarkable capabilities but remain vulnerable to adversarial ``jailbreak'' attacks designed to bypass safety guardrails. Current safety alignment methods depend heavily on static external red teaming, utilizing fixed defense prompts or pre-collected adversarial datasets. This leads to a rigid defense that overfits known patterns and fails to generalize to novel, sophisticated threats. To address this critical limitation, we propose empowering the model to be its own red teamer, capable of achieving autonomous and evolving adversarial attacks. Specifically, we introduce Safety Self- Play (SSP), a system that utilizes a single LLM to act concurrently as both the Attacker (generating jailbreaks) and the Defender (refusing harmful requests) within a unified Reinforcement Learning (RL) loop, dynamically evolving attack strategies to uncover vulnerabilities while simultaneously strengthening defense mechanisms. To ensure the Defender effectively addresses critical safety issues during the self-play, we introduce an advanced Reflective Experience Replay Mechanism, which uses an experience pool accumulated throughout the process. The mechanism employs a Upper Confidence Bound (UCB) sampling strategy to focus on failure cases with low rewards, helping the model learn from past hard mistakes while balancing exploration and exploitation. Extensive experiments demonstrate that our SSP approach autonomously evolves robust defense capabilities, significantly outperforming baselines trained on static adversarial datasets and establishing a new benchmark for proactive safety alignment.

### Paper 5: [2511.21214]
**Title:** Self-Guided Defense: Adaptive Safety Alignment for Reasoning Models via Synthesized Guidelines
**Category:** cs.CL
**Score:** 0.8855
**In MiniLM top-20:** True

Reasoning models have demonstrated remarkable capabilities in complex reasoning tasks. However, ensuring their safety against adversarial jailbreak prompts remains a critical challenge. Due to the covert and deceptive nature of such prompts, they can often evade built-in safety mechanisms and lead to the generation of harmful content. This underscores the need for an adaptive safety alignment approach that enables models to autonomously reinforce their defenses in response to adversarial inputs. This paper introduces the Synthesized Guideline-based Adaptive Safety Alignment (SGASA) framework, which internalizes model-generated safety guidelines to strengthen models' ability to enhance robustness against harmful adversarial prompts while minimizing unnecessary refusals of benign requests. SGASA consists of two key stages: Data Pre-synthesis, which generates safety guidelines and augmented prompts; and Alignment Fine-tuning, which leverages Supervised Fine-tuning (SFT) and Direct Preference Optimization (DPO) to embed these guidelines into the model. Extensive experiments across multiple datasets demonstrate that SGASA significantly improves model safety, validating its adaptive and scalable effectiveness.

### Paper 6: [2505.07167]
**Title:** One Trigger Token Is Enough: A Defense Strategy for Balancing Safety and Usability in Large Language Models
**Category:** cs.CR
**Score:** 0.8850
**In MiniLM top-20:** True

Large Language Models (LLMs) have been extensively used across diverse domains, including virtual assistants, automated code generation, and scientific research. However, they remain vulnerable to jailbreak attacks, which manipulate the models into generating harmful responses despite safety alignment. Recent studies have shown that current safety-aligned LLMs undergo shallow safety alignment. In this work, we conduct an in-depth investigation into the underlying mechanism of this phenomenon and reveal that it manifests through learned ''safety trigger tokens'' that activate the model's safety patterns when paired with the specific input. Through both analysis and empirical verification, we further demonstrate the high similarity of the safety trigger tokens across different harmful inputs. Accordingly, we propose D-STT, a simple yet effective defense algorithm that identifies and explicitly decodes safety trigger tokens of the given safety-aligned LLM to activate the model's learned safety patterns. In this process, the safety trigger is constrained to a single token, which effectively preserves model usability by introducing minimum intervention in the decoding process. Extensive experiments across diverse jailbreak attacks and benign prompts demonstrate that D-STT significantly reduces output harmfulness while preserving model usability and incurring negligible response time overhead, outperforming ten baseline methods.

### Paper 7: [2509.01631]
**Title:** Unraveling LLM Jailbreaks Through Safety Knowledge Neurons
**Category:** cs.AI
**Score:** 0.8662
**In MiniLM top-20:** True

Large Language Models (LLMs) are increasingly attracting attention in various applications. Nonetheless, there is a growing concern as some users attempt to exploit these models for malicious purposes, including the synthesis of controlled substances and the propagation of disinformation, a technique known as "Jailbreak." While some studies have achieved defenses against jailbreak attacks by modifying output distributions or detecting harmful content, the exact rationale still remains elusive. In this work, we present a novel neuron-level interpretability method that focuses on the role of safety-related knowledge neurons. Unlike existing approaches, our method projects the model's internal representation into a more consistent and interpretable vocabulary space. We then show that adjusting the activation of safety-related neurons can effectively control the model's behavior with a mean ASR higher than 97%. Building on this insight, we propose SafeTuning, a fine-tuning strategy that reinforces safety-critical neurons to improve model robustness against jailbreaks. SafeTuning consistently reduces attack success rates across multiple LLMs and outperforms all four baseline defenses. These findings offer a new perspective on understanding and defending against jailbreak attacks.

### Paper 8: [2508.12897]
**Title:** RAJ-PGA: Reasoning-Activated Jailbreak and Principle-Guided Alignment Framework for Large Reasoning Models
**Category:** cs.AI
**Score:** 0.8570
**In MiniLM top-20:** True

Large Reasoning Models (LRMs) face a distinct safety vulnerability: their internal reasoning chains may generate harmful content even when the final output appears benign. To address this overlooked risk, we first propose a novel attack paradigm, Reasoning-Activated Jailbreak (RAJ) via Concretization, which demonstrates that refining malicious prompts to be more specific can trigger step-by-step logical reasoning that overrides the model's safety protocols. To systematically mitigate this vulnerability, we further develop a scalable framework for constructing high-quality safety alignment datasets. This framework first leverages the RAJ attack to elicit challenging harmful reasoning chains from LRMs, then transforms these high-risk traces into safe, constructive, and educational responses through a tailored Principle-Guided Alignment (PGA) mechanism. Then, we introduce the PGA dataset, a verified alignment dataset containing 3,989 samples using our proposed method. Extensive experiments show that fine-tuning LRMs with PGA dataset significantly enhances model safety, achieving up to a 29.5% improvement in defense success rates across multiple jailbreak benchmarks. Critically, our approach not only defends against sophisticated reasoning-based attacks but also preserves, even enhances, the model's general reasoning capabilities. This work provides a scalable and effective pathway for safety alignment in reasoning-intensive AI systems, addressing the core trade-off between safety and functional performance.

### Paper 9: [2601.03594]
**Title:** Jailbreaking LLMs & VLMs: Mechanisms, Evaluation, and Unified Defense
**Category:** cs.CR
**Score:** 0.8507
**In MiniLM top-20:** True

This paper provides a systematic survey of jailbreak attacks and defenses on Large Language Models (LLMs) and Vision-Language Models (VLMs), emphasizing that jailbreak vulnerabilities stem from structural factors such as incomplete training data, linguistic ambiguity, and generative uncertainty. It further differentiates between hallucinations and jailbreaks in terms of intent and triggering mechanisms. We propose a three-dimensional survey framework: (1) Attack dimension-including template/encoding-based, in-context learning manipulation, reinforcement/adversarial learning, LLM-assisted and fine-tuned attacks, as well as prompt- and image-level perturbations and agent-based transfer in VLMs; (2) Defense dimension-encompassing prompt-level obfuscation, output evaluation, and model-level alignment or fine-tuning; and (3) Evaluation dimension-covering metrics such as Attack Success Rate (ASR), toxicity score, query/time cost, and multimodal Clean Accuracy and Attribute Success Rate. Compared with prior works, this survey spans the full spectrum from text-only to multimodal settings, consolidating shared mechanisms and proposing unified defense principles: variant-consistency and gradient-sensitivity detection at the perception layer, safety-aware decoding and output review at the generation layer, and adversarially augmented preference alignment at the parameter layer. Additionally, we summarize existing multimodal safety benchmarks and discuss future directions, including automated red teaming, cross-modal collaborative defense, and standardized evaluation.

### Paper 10: [2601.00213]
**Title:** Overlooked Safety Vulnerability in LLMs: Malicious Intelligent Optimization Algorithm Request and its Jailbreak
**Category:** cs.CR
**Score:** 0.8429
**In MiniLM top-20:** True

The widespread deployment of large language models (LLMs) has raised growing concerns about their misuse risks and associated safety issues. While prior studies have examined the safety of LLMs in general usage, code generation, and agent-based applications, their vulnerabilities in automated algorithm design remain underexplored. To fill this gap, this study investigates this overlooked safety vulnerability, with a particular focus on intelligent optimization algorithm design, given its prevalent use in complex decision-making scenarios. We introduce MalOptBench, a benchmark consisting of 60 malicious optimization algorithm requests, and propose MOBjailbreak, a jailbreak method tailored for this scenario. Through extensive evaluation of 13 mainstream LLMs including the latest GPT-5 and DeepSeek-V3.1, we reveal that most models remain highly susceptible to such attacks, with an average attack success rate of 83.59% and an average harmfulness score of 4.28 out of 5 on original harmful prompts, and near-complete failure under MOBjailbreak. Furthermore, we assess state-of-the-art plug-and-play defenses that can be applied to closed-source models, and find that they are only marginally effective against MOBjailbreak and prone to exaggerated safety behaviors. These findings highlight the urgent need for stronger alignment techniques to safeguard LLMs against misuse in algorithm design.

### Paper 11: [2511.15304]
**Title:** Adversarial Poetry as a Universal Single-Turn Jailbreak Mechanism in Large Language Models
**Category:** cs.CL
**Score:** 0.8398
**In MiniLM top-20:** True

We present evidence that adversarial poetry functions as a universal single-turn jailbreak technique for Large Language Models (LLMs). Across 25 frontier proprietary and open-weight models, curated poetic prompts yielded high attack-success rates (ASR), with some providers exceeding 90%. Mapping prompts to MLCommons and EU CoP risk taxonomies shows that poetic attacks transfer across CBRN, manipulation, cyber-offence, and loss-of-control domains. Converting 1,200 MLCommons harmful prompts into verse via a standardized meta-prompt produced ASRs up to 18 times higher than their prose baselines. Outputs are evaluated using an ensemble of 3 open-weight LLM judges, whose binary safety assessments were validated on a stratified human-labeled subset. Poetic framing achieved an average jailbreak success rate of 62% for hand-crafted poems and approximately 43% for meta-prompt conversions (compared to non-poetic baselines), substantially outperforming non-poetic baselines and revealing a systematic vulnerability across model families and safety training approaches. These findings demonstrate that stylistic variation alone can circumvent contemporary safety mechanisms, suggesting fundamental limitations in current alignment methods and evaluation protocols.

### Paper 12: [2411.08862]
**Title:** LLMStinger: Jailbreaking LLMs using RL fine-tuned LLMs
**Category:** cs.LG
**Score:** 0.8360
**In MiniLM top-20:** True

We introduce LLMStinger, a novel approach that leverages Large Language Models (LLMs) to automatically generate adversarial suffixes for jailbreak attacks. Unlike traditional methods, which require complex prompt engineering or white-box access, LLMStinger uses a reinforcement learning (RL) loop to fine-tune an attacker LLM, generating new suffixes based on existing attacks for harmful questions from the HarmBench benchmark. Our method significantly outperforms existing red-teaming approaches (we compared against 15 of the latest methods), achieving a +57.2% improvement in Attack Success Rate (ASR) on LLaMA2-7B-chat and a +50.3% ASR increase on Claude 2, both models known for their extensive safety measures. Additionally, we achieved a 94.97% ASR on GPT-3.5 and 99.4% on Gemma-2B-it, demonstrating the robustness and adaptability of LLMStinger across open and closed-source models.

### Paper 13: [2508.10029]
**Title:** Latent Fusion Jailbreak: Blending Harmful and Harmless Representations to Elicit Unsafe LLM Outputs
**Category:** cs.CL
**Score:** 0.8355
**In MiniLM top-20:** True

While Large Language Models (LLMs) have achieved remarkable progress, they remain vulnerable to jailbreak attacks. Existing methods, primarily relying on discrete input optimization (e.g., GCG), often suffer from high computational costs and generate high-perplexity prompts that are easily blocked by simple filters. To overcome these limitations, we propose Latent Fusion Jailbreak (LFJ), a stealthy white-box attack that operates in the continuous latent space. Unlike previous approaches, LFJ constructs adversarial representations by mathematically fusing the hidden states of a harmful query with a thematically similar benign query, effectively masking malicious intent while retaining semantic drive. We further introduce a gradient-guided optimization strategy to balance attack success and computational efficiency. Extensive evaluations on Vicuna-7B, LLaMA-2-7B-Chat, Guanaco-7B, LLaMA-3-70B, and Mistral-7B-Instruct show that LFJ achieves an average Attack Success Rate (ASR) of 94.01%, significantly outperforming state-of-the-art baselines like GCG and AutoDAN while avoiding detectable input artifacts. Furthermore, we identify that thematic similarity in the latent space is a critical vulnerability in current safety alignments. Finally, we propose a latent adversarial training defense that reduces LFJ's ASR by over 80% without compromising model utility.

### Paper 14 [DIVERGENT]: [2512.13655]
**Title:** Comparative Analysis of LLM Abliteration Methods: A Cross-Architecture Evaluation
**Category:** cs.CL
**Score:** 0.8318
**In MiniLM top-20:** False

Safety alignment mechanisms in large language models prevent responses to harmful queries through learned refusal behavior, yet these same mechanisms impede legitimate research applications including cognitive modeling, adversarial testing, and security analysis. While abliteration techniques enable surgical removal of refusal representations through directional orthogonalization, the relative effectiveness of available implementations remains uncharacterized. This study evaluates four abliteration tools (Heretic, DECCP, ErisForge, FailSpy) across sixteen instruction-tuned models (7B-14B parameters), reporting tool compatibility on all 16 models and quantitative metrics on subsets dictated by tool support. Single-pass methods demonstrated superior capability preservation on the benchmarked subset (avg GSM8K change across three models: ErisForge -0.28 pp; DECCP -0.13 pp), while Bayesian-optimized abliteration produced variable distribution shift (KL divergence: 0.043-1.646) with model-dependent capability impact. These findings provide researchers with evidence-based selection criteria for abliteration tool deployment across diverse model architectures. The principal finding indicates that mathematical reasoning capabilities exhibit the highest sensitivity to abliteration interventions, with GSM8K change ranging from +1.51 pp to -18.81 pp (-26.5% relative) depending on tool selection and model architecture.

### Paper 15: [2509.05367]
**Title:** Between a Rock and a Hard Place: The Tension Between Ethical Reasoning and Safety Alignment in LLMs
**Category:** cs.CR
**Score:** 0.8238
**In MiniLM top-20:** True

Large Language Model safety alignment predominantly operates on a binary assumption that requests are either safe or unsafe. This classification proves insufficient when models encounter ethical dilemmas, where the capacity to reason through moral trade-offs creates a distinct attack surface. We formalize this vulnerability through TRIAL, a multi-turn red-teaming methodology that embeds harmful requests within ethical framings. TRIAL achieves high attack success rates across most tested models by systematically exploiting the model's ethical reasoning capabilities to frame harmful actions as morally necessary compromises. Building on these insights, we introduce ERR (Ethical Reasoning Robustness), a defense framework that distinguishes between instrumental responses that enable harmful outcomes and explanatory responses that analyze ethical frameworks without endorsing harmful acts. ERR employs a Layer-Stratified Harm-Gated LoRA architecture, achieving robust defense against reasoning-based attacks while preserving model utility.

### Paper 16: [2601.10173]
**Title:** ReasAlign: Reasoning Enhanced Safety Alignment against Prompt Injection Attack
**Category:** cs.CR
**Score:** 0.8226
**In MiniLM top-20:** True

Large Language Models (LLMs) have enabled the development of powerful agentic systems capable of automating complex workflows across various fields. However, these systems are highly vulnerable to indirect prompt injection attacks, where malicious instructions embedded in external data can hijack agent behavior. In this work, we present ReasAlign, a model-level solution to improve safety alignment against indirect prompt injection attacks. The core idea of ReasAlign is to incorporate structured reasoning steps to analyze user queries, detect conflicting instructions, and preserve the continuity of the user's intended tasks to defend against indirect injection attacks. To further ensure reasoning logic and accuracy, we introduce a test-time scaling mechanism with a preference-optimized judge model that scores reasoning steps and selects the best trajectory. Comprehensive evaluations across various benchmarks show that ReasAlign maintains utility comparable to an undefended model while consistently outperforming Meta SecAlign, the strongest prior guardrail. On the representative open-ended CyberSecEval2 benchmark, which includes multiple prompt-injected tasks, ReasAlign achieves 94.6% utility and only 3.6% ASR, far surpassing the state-of-the-art defensive model of Meta SecAlign (56.4% utility and 74.4% ASR). These results demonstrate that ReasAlign achieves the best trade-off between security and utility, establishing a robust and practical defense against prompt injection attacks in real-world agentic systems. Our code and experimental results could be found at https://github.com/leolee99/ReasAlign.

### Paper 17: [2601.03005]
**Title:** JPU: Bridging Jailbreak Defense and Unlearning via On-Policy Path Rectification
**Category:** cs.CR
**Score:** 0.8188
**In MiniLM top-20:** True

Despite extensive safety alignment, Large Language Models (LLMs) often fail against jailbreak attacks. While machine unlearning has emerged as a promising defense by erasing specific harmful parameters, current methods remain vulnerable to diverse jailbreaks. We first conduct an empirical study and discover that this failure mechanism is caused by jailbreaks primarily activating non-erased parameters in the intermediate layers. Further, by probing the underlying mechanism through which these circumvented parameters reassemble into the prohibited output, we verify the persistent existence of dynamic $\textbf{jailbreak paths}$ and show that the inability to rectify them constitutes the fundamental gap in existing unlearning defenses. To bridge this gap, we propose $\textbf{J}$ailbreak $\textbf{P}$ath $\textbf{U}$nlearning (JPU), which is the first to rectify dynamic jailbreak paths towards safety anchors by dynamically mining on-policy adversarial samples to expose vulnerabilities and identify jailbreak paths. Extensive experiments demonstrate that JPU significantly enhances jailbreak resistance against dynamic attacks while preserving the model's utility.

### Paper 18 [DIVERGENT]: [2601.15698]
**Title:** Beyond Visual Safety: Jailbreaking Multimodal Large Language Models for Harmful Image Generation via Semantic-Agnostic Inputs
**Category:** cs.CV
**Score:** 0.8147
**In MiniLM top-20:** False

The rapid advancement of Multimodal Large Language Models (MLLMs) has introduced complex security challenges, particularly at the intersection of textual and visual safety. While existing schemes have explored the security vulnerabilities of MLLMs, the investigation into their visual safety boundaries remains insufficient. In this paper, we propose Beyond Visual Safety (BVS), a novel image-text pair jailbreaking framework specifically designed to probe the visual safety boundaries of MLLMs. BVS employs a "reconstruction-then-generation" strategy, leveraging neutralized visual splicing and inductive recomposition to decouple malicious intent from raw inputs, thereby leading MLLMs to be induced into generating harmful images. Experimental results demonstrate that BVS achieves a remarkable jailbreak success rate of 98.21\% against GPT-5 (12 January 2026 release). Our findings expose critical vulnerabilities in the visual safety alignment of current MLLMs.

### Paper 19: [2601.03699]
**Title:** RedBench: A Universal Dataset for Comprehensive Red Teaming of Large Language Models
**Category:** cs.CL
**Score:** 0.8062
**In MiniLM top-20:** True

As large language models (LLMs) become integral to safety-critical applications, ensuring their robustness against adversarial prompts is paramount. However, existing red teaming datasets suffer from inconsistent risk categorizations, limited domain coverage, and outdated evaluations, hindering systematic vulnerability assessments. To address these challenges, we introduce RedBench, a universal dataset aggregating 37 benchmark datasets from leading conferences and repositories, comprising 29,362 samples across attack and refusal prompts. RedBench employs a standardized taxonomy with 22 risk categories and 19 domains, enabling consistent and comprehensive evaluations of LLM vulnerabilities. We provide a detailed analysis of existing datasets, establish baselines for modern LLMs, and open-source the dataset and evaluation code. Our contributions facilitate robust comparisons, foster future research, and promote the development of secure and reliable LLMs for real-world deployment. Code: https://github.com/knoveleng/redeval

### Paper 20 [DIVERGENT]: [2601.03401]
**Title:** Rendering Data Unlearnable by Exploiting LLM Alignment Mechanisms
**Category:** cs.CL
**Score:** 0.8040
**In MiniLM top-20:** False

Large language models (LLMs) are increasingly trained on massive, heterogeneous text corpora, raising serious concerns about the unauthorised use of proprietary or personal data during model training. In this work, we address the problem of data protection against unwanted model learning in a realistic black-box setting. We propose Disclaimer Injection, a novel data-level defence that renders text unlearnable to LLMs. Rather than relying on model-side controls or explicit data removal, our approach exploits the models' own alignment mechanisms: by injecting carefully designed alignment-triggering disclaimers to prevent effective learning. Through layer-wise analysis, we find that fine-tuning on such protected data induces persistent activation of alignment-related layers, causing alignment constraints to override task learning even on common inputs. Consequently, models trained on such data exhibit substantial and systematic performance degradation compared to standard fine-tuning. Our results identify alignment behaviour as a previously unexplored lever for data protection and, to our knowledge, present the first practical method for restricting data learnability at LLM scale without requiring access to or modification of the training pipeline.

---

## Review Instructions

You are reviewing the top-20 recommendations from gte for the profile "AI safety / alignment".
Papers marked [DIVERGENT] are in gte's top-20 but NOT in MiniLM's.

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
