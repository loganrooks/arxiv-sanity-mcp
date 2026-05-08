# Single-Strategy Characterization Review

**Model:** specter2
**Profile:** Diffusion models for generation (P6)
**Depth:** full
**Overlap with MiniLM:** 15/20 shared, 5 unique to specter2

## Seed Papers
  - [2509.00642] HADIS: Hybrid Adaptive Diffusion Model Serving for Efficient Text-to-Image Generation (cs.DC)
  - [2403.04279] Controllable Generation with Text-to-Image Diffusion Models: A Survey (cs.CV)
  - [2406.14815] Latent diffusion models for parameterization and data assimilation of facies-based geomodels (cs.CV)
  - [2601.05852] Kidney Cancer Detection Using 3D-Based Latent Diffusion Models (cs.CV)
  - [2601.11085] Generation of Chest CT pulmonary Nodule Images by Latent Diffusion Models using the LIDC-IDRI Dataset (eess.IV)

## specter2 Top-20 Recommendations

### Paper 1: [2403.04279]
**Title:** Controllable Generation with Text-to-Image Diffusion Models: A Survey
**Category:** cs.CV
**Score:** 0.9680
**In MiniLM top-20:** True

In the rapidly advancing realm of visual generation, diffusion models have revolutionized the landscape, marking a significant shift in capabilities with their impressive text-guided generative functions. However, relying solely on text for conditioning these models does not fully cater to the varied and complex requirements of different applications and scenarios. Acknowledging this shortfall, a variety of studies aim to control pre-trained text-to-image (T2I) models to support novel conditions. In this survey, we undertake a thorough review of the literature on controllable generation with T2I diffusion models, covering both the theoretical foundations and practical advancements in this domain. Our review begins with a brief introduction to the basics of denoising diffusion probabilistic models (DDPMs) and widely used T2I diffusion models. We then reveal the controlling mechanisms of diffusion models, theoretically analyzing how novel conditions are introduced into the denoising process for conditional generation. Additionally, we offer a detailed overview of research in this area, organizing it into distinct categories from the condition perspective: generation with specific conditions, generation with multiple conditions, and universal controllable generation. For an exhaustive list of the controllable generation literature surveyed, please refer to our curated repository at https://github.com/PRIV-Creation/Awesome-Controllable-T2I-Diffusion-Models.

### Paper 2: [2601.11085]
**Title:** Generation of Chest CT pulmonary Nodule Images by Latent Diffusion Models using the LIDC-IDRI Dataset
**Category:** eess.IV
**Score:** 0.9597
**In MiniLM top-20:** True

Recently, computer-aided diagnosis systems have been developed to support diagnosis, but their performance depends heavily on the quality and quantity of training data. However, in clinical practice, it is difficult to collect the large amount of CT images for specific cases, such as small cell carcinoma with low epidemiological incidence or benign tumors that are difficult to distinguish from malignant ones. This leads to the challenge of data imbalance. In this study, to address this issue, we proposed a method to automatically generate chest CT nodule images that capture target features using latent diffusion models (LDM) and verified its effectiveness. Using the LIDC-IDRI dataset, we created pairs of nodule images and finding-based text prompts based on physician evaluations. For the image generation models, we used Stable Diffusion version 1.5 (SDv1) and 2.0 (SDv2), which are types of LDM. Each model was fine-tuned using the created dataset. During the generation process, we adjusted the guidance scale (GS), which indicates the fidelity to the input text. Both quantitative and subjective evaluations showed that SDv2 (GS = 5) achieved the best performance in terms of image quality, diversity, and text consistency. In the subjective evaluation, no statistically significant differences were observed between the generated images and real images, confirming that the quality was equivalent to real clinical images. We proposed a method for generating chest CT nodule images based on input text using LDM. Evaluation results demonstrated that the proposed method could generate high-quality images that successfully capture specific medical features.

### Paper 3 [DIVERGENT]: [2410.23530]
**Title:** There and Back Again: On the relation between Noise and Image Inversions in Diffusion Models
**Category:** cs.CV
**Score:** 0.9536
**In MiniLM top-20:** False

Diffusion Models achieve state-of-the-art performance in generating new samples but lack a low-dimensional latent space that encodes the data into editable features. Inversion-based methods address this by reversing the denoising trajectory, transferring images to their approximated starting noise. In this work, we thoroughly analyze this procedure and focus on the relation between the initial noise, the generated samples, and their corresponding latent encodings obtained through the DDIM inversion. First, we show that latents exhibit structural patterns in the form of less diverse noise predicted for smooth image areas (e.g., plain sky). Through a series of analyses, we trace this issue to the first inversion steps, which fail to provide accurate and diverse noise. Consequently, the DDIM inversion space is notably less manipulative than the original noise. We show that prior inversion methods do not fully resolve this issue, but our simple fix, where we replace the first DDIM Inversion steps with a forward diffusion process, successfully decorrelates latent encodings and enables higher quality editions and interpolations. The code is available at https://github.com/luk-st/taba.

### Paper 4: [2503.06884]
**Title:** Text-to-Image Diffusion Models Cannot Count, and Prompt Refinement Cannot Help
**Category:** cs.CV
**Score:** 0.9515
**In MiniLM top-20:** True

Generative modeling is widely regarded as one of the most essential problems in today's AI community, with text-to-image generation having gained unprecedented real-world impacts. Among various approaches, diffusion models have achieved remarkable success and have become the de facto solution for text-to-image generation. However, despite their impressive performance, these models exhibit fundamental limitations in adhering to numerical constraints in user instructions, frequently generating images with an incorrect number of objects. While several prior works have mentioned this issue, a comprehensive and rigorous evaluation of this limitation remains lacking. To address this gap, we introduce T2ICountBench, a novel benchmark designed to rigorously evaluate the counting ability of state-of-the-art text-to-image diffusion models. Our benchmark encompasses a diverse set of generative models, including both open-source and private systems. It explicitly isolates counting performance from other capabilities, provides structured difficulty levels, and incorporates human evaluations to ensure high reliability.
  Extensive evaluations with T2ICountBench reveal that all state-of-the-art diffusion models fail to generate the correct number of objects, with accuracy dropping significantly as the number of objects increases. Additionally, an exploratory study on prompt refinement demonstrates that such simple interventions generally do not improve counting accuracy. Our findings highlight the inherent challenges in numerical understanding within diffusion models and point to promising directions for future improvements.

### Paper 5 [DIVERGENT]: [2507.18988]
**Title:** AEDR: Training-Free AI-Generated Image Attribution via Autoencoder Double-Reconstruction
**Category:** cs.CV
**Score:** 0.9488
**In MiniLM top-20:** False

The rapid advancement of image-generation technologies has made it possible for anyone to create photorealistic images using generative models, raising significant security concerns. To mitigate malicious use, tracing the origin of such images is essential. Reconstruction-based attribution methods offer a promising solution, but they often suffer from reduced accuracy and high computational costs when applied to state-of-the-art (SOTA) models. To address these challenges, we propose AEDR (AutoEncoder Double-Reconstruction), a novel training-free attribution method designed for generative models with continuous autoencoders. Unlike existing reconstruction-based approaches that rely on the value of a single reconstruction loss, AEDR performs two consecutive reconstructions using the model's autoencoder, and adopts the ratio of these two reconstruction losses as the attribution signal. This signal is further calibrated using the image homogeneity metric to improve accuracy, which inherently cancels out absolute biases caused by image complexity, with autoencoder-based reconstruction ensuring superior computational efficiency. Experiments on eight top latent diffusion models show that AEDR achieves 25.5% higher attribution accuracy than existing reconstruction-based methods, while requiring only 1% of the computational time.

### Paper 6: [2601.05852]
**Title:** Kidney Cancer Detection Using 3D-Based Latent Diffusion Models
**Category:** cs.CV
**Score:** 0.9476
**In MiniLM top-20:** True

In this work, we present a novel latent diffusion-based pipeline for 3D kidney anomaly detection on contrast-enhanced abdominal CT. The method combines Denoising Diffusion Probabilistic Models (DDPMs), Denoising Diffusion Implicit Models (DDIMs), and Vector-Quantized Generative Adversarial Networks (VQ-GANs). Unlike prior slice-wise approaches, our method operates directly on an image volume and leverages weak supervision with only case-level pseudo-labels. We benchmark our approach against state-of-the-art supervised segmentation and detection models. This study demonstrates the feasibility and promise of 3D latent diffusion for weakly supervised anomaly detection. While the current results do not yet match supervised baselines, they reveal key directions for improving reconstruction fidelity and lesion localization. Our findings provide an important step toward annotation-efficient, generative modeling of complex abdominal anatomy.

### Paper 7: [2504.13745]
**Title:** ESPLoRA: Enhanced Spatial Precision with Low-Rank Adaption in Text-to-Image Diffusion Models for High-Definition Synthesis
**Category:** cs.CV
**Score:** 0.9466
**In MiniLM top-20:** True

Diffusion models have revolutionized text-to-image (T2I) synthesis, producing high-quality, photorealistic images. However, they still struggle to properly render the spatial relationships described in text prompts. To address the lack of spatial information in T2I generations, existing methods typically use external network conditioning and predefined layouts, resulting in higher computational costs and reduced flexibility. Our approach builds upon a curated dataset of spatially explicit prompts, meticulously extracted and synthesized from LAION-400M to ensure precise alignment between textual descriptions and spatial layouts. Alongside this dataset, we present ESPLoRA, a flexible fine-tuning framework based on Low-Rank Adaptation, specifically designed to enhance spatial consistency in generative models without increasing generation time or compromising the quality of the outputs. In addition to ESPLoRA, we propose refined evaluation metrics grounded in geometric constraints, capturing 3D spatial relations such as "in front of" or "behind". These metrics also expose spatial biases in T2I models which, even when not fully mitigated, can be strategically exploited by our TORE algorithm to further improve the spatial consistency of generated images. Our method outperforms CoMPaSS, the current baseline framework, on spatial consistency benchmarks.

### Paper 8: [2406.14815]
**Title:** Latent diffusion models for parameterization and data assimilation of facies-based geomodels
**Category:** cs.CV
**Score:** 0.9446
**In MiniLM top-20:** True

Geological parameterization entails the representation of a geomodel using a small set of latent variables and a mapping from these variables to grid-block properties such as porosity and permeability. Parameterization is useful for data assimilation (history matching), as it maintains geological realism while reducing the number of variables to be determined. Diffusion models are a new class of generative deep-learning procedures that have been shown to outperform previous methods, such as generative adversarial networks, for image generation tasks. Diffusion models are trained to "denoise", which enables them to generate new geological realizations from input fields characterized by random noise. Latent diffusion models, which are the specific variant considered in this study, provide dimension reduction through use of a low-dimensional latent variable. The model developed in this work includes a variational autoencoder for dimension reduction and a U-net for the denoising process. Our application involves conditional 2D three-facies (channel-levee-mud) systems. The latent diffusion model is shown to provide realizations that are visually consistent with samples from geomodeling software. Quantitative metrics involving spatial and flow-response statistics are evaluated, and general agreement between the diffusion-generated models and reference realizations is observed. Stability tests are performed to assess the smoothness of the parameterization method. The latent diffusion model is then used for ensemble-based data assimilation. Two synthetic "true" models are considered. Significant uncertainty reduction, posterior P$_{10}$-P$_{90}$ forecasts that generally bracket observed data, and consistent posterior geomodels, are achieved in both cases.

### Paper 9: [2207.00050]
**Title:** Semantic Image Synthesis via Diffusion Models
**Category:** cs.CV
**Score:** 0.9446
**In MiniLM top-20:** True

Denoising Diffusion Probabilistic Models (DDPMs) have achieved remarkable success in various image generation tasks compared with Generative Adversarial Nets (GANs). Recent work on semantic image synthesis mainly follows the de facto GAN-based approaches, which may lead to unsatisfactory quality or diversity of generated images. In this paper, we propose a novel framework based on DDPM for semantic image synthesis. Unlike previous conditional diffusion model directly feeds the semantic layout and noisy image as input to a U-Net structure, which may not fully leverage the information in the input semantic mask, our framework processes semantic layout and noisy image differently. It feeds noisy image to the encoder of the U-Net structure while the semantic layout to the decoder by multi-layer spatially-adaptive normalization operators. To further improve the generation quality and semantic interpretability in semantic image synthesis, we introduce the classifier-free guidance sampling strategy, which acknowledge the scores of an unconditional model for sampling process. Extensive experiments on four benchmark datasets demonstrate the effectiveness of our proposed method, achieving state-of-the-art performance in terms of fidelity (FID) and diversity (LPIPS). Our code and pretrained models are available at https://github.com/WeilunWang/semantic-diffusion-model.

### Paper 10: [2306.04321]
**Title:** Generative Semantic Communication: Diffusion Models Beyond Bit Recovery
**Category:** cs.AI
**Score:** 0.9433
**In MiniLM top-20:** True

Semantic communication is expected to be one of the cores of next-generation AI-based communications. One of the possibilities offered by semantic communication is the capability to regenerate, at the destination side, images or videos semantically equivalent to the transmitted ones, without necessarily recovering the transmitted sequence of bits. The current solutions still lack the ability to build complex scenes from the received partial information. Clearly, there is an unmet need to balance the effectiveness of generation methods and the complexity of the transmitted information, possibly taking into account the goal of communication. In this paper, we aim to bridge this gap by proposing a novel generative diffusion-guided framework for semantic communication that leverages the strong abilities of diffusion models in synthesizing multimedia content while preserving semantic features. We reduce bandwidth usage by sending highly-compressed semantic information only. Then, the diffusion model learns to synthesize semantic-consistent scenes through spatially-adaptive normalizations from such denoised semantic information. We prove, through an in-depth assessment of multiple scenarios, that our method outperforms existing solutions in generating high-quality images with preserved semantic information even in cases where the received content is significantly degraded. More specifically, our results show that objects, locations, and depths are still recognizable even in the presence of extremely noisy conditions of the communication channel. The code is available at https://github.com/ispamm/GESCO.

### Paper 11: [2511.16870]
**Title:** Align & Invert: Solving Inverse Problems with Diffusion and Flow-based Models via Representation Alignment
**Category:** cs.CV
**Score:** 0.9429
**In MiniLM top-20:** True

Enforcing alignment between the internal representations of diffusion or flow-based generative models and those of pretrained self-supervised encoders has recently been shown to provide a powerful inductive bias, improving both convergence and sample quality. In this work, we extend this idea to inverse problems, where pretrained generative models are employed as priors. We propose applying representation alignment (REPA) between diffusion or flow-based models and a DINOv2 visual encoder, to guide the reconstruction process at inference time. Although ground-truth signals are unavailable in inverse problems, we empirically show that aligning model representations of approximate target features can substantially enhance reconstruction quality and perceptual realism. We provide theoretical results showing (a) that REPA regularization can be viewed as a variational approach for minimizing a divergence measure in the DINOv2 embedding space, and (b) how under certain regularity assumptions REPA updates steer the latent diffusion states toward those of the clean image. These results offer insights into the role of REPA in improving perceptual fidelity. Finally, we demonstrate the generality of our approach by We integrate REPA into multiple state-of-the-art inverse problem solvers, and provide extensive experiments on super-resolution, box inpainting, Gaussian deblurring, and motion deblurring confirming that our method consistently improves reconstruction quality, while also providing efficiency gains reducing the number of required discretization steps.

### Paper 12: [2509.00642]
**Title:** HADIS: Hybrid Adaptive Diffusion Model Serving for Efficient Text-to-Image Generation
**Category:** cs.DC
**Score:** 0.9415
**In MiniLM top-20:** True

Text-to-image diffusion models have achieved remarkable visual quality but incur high computational costs, making latency-aware, scalable deployment challenging. To address this, we advocate a hybrid architecture that achieves query awareness when serving diffusion models. Unlike existing query-aware serving systems that cascade lightweight and heavyweight models with a fixed configuration, our hybrid architecture first routes each query directly to a suitable model variant, then reroutes it to a cascaded heavyweight model only if necessary. We theoretically analyze conditions for the hybrid architecture to outperform non-hybrid alternatives in latency and response quality. Building on this architecture, we design HADIS, a hybrid serving system for latency-aware diffusion models that jointly optimizes cascade model selection, query routing, and resource allocation. To reduce the complexity of resource management, HADIS uses an offline profiling phase to produce a Pareto-optimal cascade configuration table. At runtime, HADIS selects the best cascade configuration and GPU allocation given latency and workload constraints. Empirical evaluations on real-world traces demonstrate that HADIS improves response quality by up to 35% while reducing latency violation rates by 2.7-45$\times$ compared to state-of-the-art model serving systems.

### Paper 13: [2502.09665]
**Title:** Revealing Subtle Phenotypes in Small Microscopy Datasets Using Latent Diffusion Models
**Category:** cs.CV
**Score:** 0.9405
**In MiniLM top-20:** True

Identifying subtle phenotypic variations in cellular images is critical for advancing biological research and accelerating drug discovery. These variations are often masked by the inherent cellular heterogeneity, making it challenging to distinguish differences between experimental conditions. Recent advancements in deep generative models have demonstrated significant potential for revealing these nuanced phenotypes through image translation, opening new frontiers in cellular and molecular biology as well as the identification of novel biomarkers. Among these generative models, diffusion models stand out for their ability to produce high-quality, realistic images. However, training diffusion models typically requires large datasets and substantial computational resources, both of which can be limited in biological research. In this work, we propose a novel approach that leverages pre-trained latent diffusion models to uncover subtle phenotypic changes. We validate our approach qualitatively and quantitatively on several small datasets of microscopy images. Our findings reveal that our approach enables effective detection of phenotypic variations, capturing both visually apparent and imperceptible differences. Ultimately, our results highlight the promising potential of this approach for phenotype detection, especially in contexts constrained by limited data and computational capacity.

### Paper 14 [DIVERGENT]: [2601.15664]
**Title:** Skywork UniPic 3.0: Unified Multi-Image Composition via Sequence Modeling
**Category:** cs.CV
**Score:** 0.9390
**In MiniLM top-20:** False

The recent surge in popularity of Nano-Banana and Seedream 4.0 underscores the community's strong interest in multi-image composition tasks. Compared to single-image editing, multi-image composition presents significantly greater challenges in terms of consistency and quality, yet existing models have not disclosed specific methodological details for achieving high-quality fusion. Through statistical analysis, we identify Human-Object Interaction (HOI) as the most sought-after category by the community. We therefore systematically analyze and implement a state-of-the-art solution for multi-image composition with a primary focus on HOI-centric tasks. We present Skywork UniPic 3.0, a unified multimodal framework that integrates single-image editing and multi-image composition. Our model supports an arbitrary (1~6) number and resolution of input images, as well as arbitrary output resolutions (within a total pixel budget of 1024x1024). To address the challenges of multi-image composition, we design a comprehensive data collection, filtering, and synthesis pipeline, achieving strong performance with only 700K high-quality training samples. Furthermore, we introduce a novel training paradigm that formulates multi-image composition as a sequence-modeling problem, transforming conditional generation into unified sequence synthesis. To accelerate inference, we integrate trajectory mapping and distribution matching into the post-training stage, enabling the model to produce high-fidelity samples in just 8 steps and achieve a 12.5x speedup over standard synthesis sampling. Skywork UniPic 3.0 achieves state-of-the-art performance on single-image editing benchmark and surpasses both Nano-Banana and Seedream 4.0 on multi-image composition benchmark, thereby validating the effectiveness of our data pipeline and training paradigm. Code, models and dataset are publicly available.

### Paper 15: [2410.01262]
**Title:** Improving Fine-Grained Control via Aggregation of Multiple Diffusion Models
**Category:** cs.CV
**Score:** 0.9384
**In MiniLM top-20:** True

While many diffusion models perform well when controlling particular aspects such as style, character, and interaction, they struggle with fine-grained control due to dataset limitations and intricate model architecture design. This paper introduces a novel training-free algorithm for fine-grained generation, called Aggregation of Multiple Diffusion Models (AMDM). The algorithm integrates features in the latent data space from multiple diffusion models within the same ecosystem into a specified model, thereby activating particular features and enabling fine-grained control. Experimental results demonstrate that AMDM significantly improves fine-grained control without training, validating its effectiveness. Additionally, it reveals that diffusion models initially focus on features such as position, attributes, and style, with later stages improving generation quality and consistency. AMDM offers a new perspective for tackling the challenges of fine-grained conditional generation in diffusion models. Specifically, it allows us to fully utilize existing or develop new conditional diffusion models that control specific aspects, and then aggregate them using the AMDM algorithm. This eliminates the need for constructing complex datasets, designing intricate model architectures, and incurring high training costs. Code is available at: https://github.com/Hammour-steak/AMDM.

### Paper 16: [2601.04056]
**Title:** Bridging the Discrete-Continuous Gap: Unified Multimodal Generation via Coupled Manifold Discrete Absorbing Diffusion
**Category:** cs.CL
**Score:** 0.9381
**In MiniLM top-20:** True

The bifurcation of generative modeling into autoregressive approaches for discrete data (text) and diffusion approaches for continuous data (images) hinders the development of truly unified multimodal systems. While Masked Language Models (MLMs) offer efficient bidirectional context, they traditionally lack the generative fidelity of autoregressive models and the semantic continuity of diffusion models. Furthermore, extending masked generation to multimodal settings introduces severe alignment challenges and training instability. In this work, we propose \textbf{CoM-DAD} (\textbf{Co}upled \textbf{M}anifold \textbf{D}iscrete \textbf{A}bsorbing \textbf{D}iffusion), a novel probabilistic framework that reformulates multimodal generation as a hierarchical dual-process. CoM-DAD decouples high-level semantic planning from low-level token synthesis. First, we model the semantic manifold via a continuous latent diffusion process; second, we treat token generation as a discrete absorbing diffusion process, regulated by a \textbf{Variable-Rate Noise Schedule}, conditioned on these evolving semantic priors. Crucially, we introduce a \textbf{Stochastic Mixed-Modal Transport} strategy that aligns disparate modalities without requiring heavy contrastive dual-encoders. Our method demonstrates superior stability over standard masked modeling, establishing a new paradigm for scalable, unified text-image generation.

### Paper 17 [DIVERGENT]: [2601.21284]
**Title:** PILD: Physics-Informed Learning via Diffusion
**Category:** cs.LG
**Score:** 0.9379
**In MiniLM top-20:** False

Diffusion models have emerged as powerful generative tools for modeling complex data distributions, yet their purely data-driven nature limits applicability in practical engineering and scientific problems where physical laws need to be followed. This paper proposes Physics-Informed Learning via Diffusion (PILD), a framework that unifies diffusion modeling and first-principles physical constraints by introducing a virtual residual observation sampled from a Laplace distribution to supervise generation during training. To further integrate physical laws, a conditional embedding module is incorporated to inject physical information into the denoising network at multiple layers, ensuring consistent guidance throughout the diffusion process. The proposed PILD framework is concise, modular, and broadly applicable to problems governed by ordinary differential equations, partial differential equations, as well as algebraic equations or inequality constraints. Extensive experiments across engineering and scientific tasks including estimating vehicle trajectories, tire forces, Darcy flow and plasma dynamics, demonstrate that our PILD substantially improves accuracy, stability, and generalization over existing physics-informed and diffusion-based baselines.

### Paper 18: [2406.18944]
**Title:** Rethinking and Red-Teaming Protective Perturbation in Personalized Diffusion Models
**Category:** cs.CV
**Score:** 0.9378
**In MiniLM top-20:** True

Personalized diffusion models (PDMs) have become prominent for adapting pre-trained text-to-image models to generate images of specific subjects using minimal training data. However, PDMs are susceptible to minor adversarial perturbations, leading to significant degradation when fine-tuned on corrupted datasets. These vulnerabilities are exploited to create protective perturbations that prevent unauthorized image generation. Existing purification methods attempt to red-team the protective perturbation to break the protection but often over-purify images, resulting in information loss. In this work, we conduct an in-depth analysis of the fine-tuning process of PDMs through the lens of shortcut learning. We hypothesize and empirically demonstrate that adversarial perturbations induce a latent-space misalignment between images and their text prompts in the CLIP embedding space. This misalignment causes the model to erroneously associate noisy patterns with unique identifiers during fine-tuning, resulting in poor generalization. Based on these insights, we propose a systematic red-teaming framework that includes data purification and contrastive decoupling learning. We first employ off-the-shelf image restoration techniques to realign images with their original semantic content in latent space. Then, we introduce contrastive decoupling learning with noise tokens to decouple the learning of personalized concepts from spurious noise patterns. Our study not only uncovers shortcut learning vulnerabilities in PDMs but also provides a thorough evaluation framework for developing stronger protection. Our extensive evaluation demonstrates its advantages over existing purification methods and its robustness against adaptive perturbations.

### Paper 19 [DIVERGENT]: [2601.21348]
**Title:** Memorization Control in Diffusion Models from Denoising-centric Perspective
**Category:** cs.LG
**Score:** 0.9366
**In MiniLM top-20:** False

Controlling memorization in diffusion models is critical for applications that require generated data to closely match the training distribution. Existing approaches mainly focus on data centric or model centric modifications, treating the diffusion model as an isolated predictor. In this paper, we study memorization in diffusion models from a denoising centric perspective. We show that uniform timestep sampling leads to unequal learning contributions across denoising steps due to differences in signal to noise ratio, which biases training toward memorization. To address this, we propose a timestep sampling strategy that explicitly controls where learning occurs along the denoising trajectory. By adjusting the width of the confidence interval, our method provides direct control over the memorization generalization trade off. Experiments on image and 1D signal generation tasks demonstrate that shifting learning emphasis toward later denoising steps consistently reduces memorization and improves distributional alignment with training data, validating the generality and effectiveness of our approach.

### Paper 20: [2601.09044]
**Title:** POWDR: Pathology-preserving Outpainting with Wavelet Diffusion for 3D MRI
**Category:** eess.IV
**Score:** 0.9364
**In MiniLM top-20:** True

Medical imaging datasets often suffer from class imbalance and limited availability of pathology-rich cases, which constrains the performance of machine learning models for segmentation, classification, and vision-language tasks. To address this challenge, we propose POWDR, a pathology-preserving outpainting framework for 3D MRI based on a conditioned wavelet diffusion model. Unlike conventional augmentation or unconditional synthesis, POWDR retains real pathological regions while generating anatomically plausible surrounding tissue, enabling diversity without fabricating lesions.
  Our approach leverages wavelet-domain conditioning to enhance high-frequency detail and mitigate blurring common in latent diffusion models. We introduce a random connected mask training strategy to overcome conditioning-induced collapse and improve diversity outside the lesion. POWDR is evaluated on brain MRI using BraTS datasets and extended to knee MRI to demonstrate tissue-agnostic applicability. Quantitative metrics (FID, SSIM, LPIPS) confirm image realism, while diversity analysis shows significant improvement with random-mask training (cosine similarity reduced from 0.9947 to 0.9580; KL divergence increased from 0.00026 to 0.01494). Clinically relevant assessments reveal gains in tumor segmentation performance using nnU-Net, with Dice scores improving from 0.6992 to 0.7137 when adding 50 synthetic cases. Tissue volume analysis indicates no significant differences for CSF and GM compared to real images.
  These findings highlight POWDR as a practical solution for addressing data scarcity and class imbalance in medical imaging. The method is extensible to multiple anatomies and offers a controllable framework for generating diverse, pathology-preserving synthetic data to support robust model development.

---

## Review Instructions

You are reviewing the top-20 recommendations from specter2 for the profile "Diffusion models for generation".
Papers marked [DIVERGENT] are in specter2's top-20 but NOT in MiniLM's.

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
