# Blind Pairwise Qualitative Review

**Profile:** Diffusion models for generation (P6)
**Depth:** full
**Models:** Model B vs Model A (identities withheld)

## Seed Papers
  - [2509.00642] HADIS: Hybrid Adaptive Diffusion Model Serving for Efficient Text-to-Image Generation (cs.DC)
  - [2403.04279] Controllable Generation with Text-to-Image Diffusion Models: A Survey (cs.CV)
  - [2406.14815] Latent diffusion models for parameterization and data assimilation of facies-based geomodels (cs.CV)
  - [2601.05852] Kidney Cancer Detection Using 3D-Based Latent Diffusion Models (cs.CV)
  - [2601.11085] Generation of Chest CT pulmonary Nodule Images by Latent Diffusion Models using the LIDC-IDRI Dataset (eess.IV)

## Recommendations

### Model B Paper 1: [2601.11085]
**Title:** Generation of Chest CT pulmonary Nodule Images by Latent Diffusion Models using the LIDC-IDRI Dataset
**Category:** eess.IV
**Score:** 0.8630

Recently, computer-aided diagnosis systems have been developed to support diagnosis, but their performance depends heavily on the quality and quantity of training data. However, in clinical practice, it is difficult to collect the large amount of CT images for specific cases, such as small cell carcinoma with low epidemiological incidence or benign tumors that are difficult to distinguish from malignant ones. This leads to the challenge of data imbalance. In this study, to address this issue, we proposed a method to automatically generate chest CT nodule images that capture target features using latent diffusion models (LDM) and verified its effectiveness. Using the LIDC-IDRI dataset, we created pairs of nodule images and finding-based text prompts based on physician evaluations. For the image generation models, we used Stable Diffusion version 1.5 (SDv1) and 2.0 (SDv2), which are types of LDM. Each model was fine-tuned using the created dataset. During the generation process, we adjusted the guidance scale (GS), which indicates the fidelity to the input text. Both quantitative and subjective evaluations showed that SDv2 (GS = 5) achieved the best performance in terms of image quality, diversity, and text consistency. In the subjective evaluation, no statistically significant differences were observed between the generated images and real images, confirming that the quality was equivalent to real clinical images. We proposed a method for generating chest CT nodule images based on input text using LDM. Evaluation results demonstrated that the proposed method could generate high-quality images that successfully capture specific medical features.

### Model B Paper 2: [2207.00050]
**Title:** Semantic Image Synthesis via Diffusion Models
**Category:** cs.CV
**Score:** 0.8351

Denoising Diffusion Probabilistic Models (DDPMs) have achieved remarkable success in various image generation tasks compared with Generative Adversarial Nets (GANs). Recent work on semantic image synthesis mainly follows the de facto GAN-based approaches, which may lead to unsatisfactory quality or diversity of generated images. In this paper, we propose a novel framework based on DDPM for semantic image synthesis. Unlike previous conditional diffusion model directly feeds the semantic layout and noisy image as input to a U-Net structure, which may not fully leverage the information in the input semantic mask, our framework processes semantic layout and noisy image differently. It feeds noisy image to the encoder of the U-Net structure while the semantic layout to the decoder by multi-layer spatially-adaptive normalization operators. To further improve the generation quality and semantic interpretability in semantic image synthesis, we introduce the classifier-free guidance sampling strategy, which acknowledge the scores of an unconditional model for sampling process. Extensive experiments on four benchmark datasets demonstrate the effectiveness of our proposed method, achieving state-of-the-art performance in terms of fidelity (FID) and diversity (LPIPS). Our code and pretrained models are available at https://github.com/WeilunWang/semantic-diffusion-model.

### Model B Paper 3: [2406.14815]
**Title:** Latent diffusion models for parameterization and data assimilation of facies-based geomodels
**Category:** cs.CV
**Score:** 0.8309

Geological parameterization entails the representation of a geomodel using a small set of latent variables and a mapping from these variables to grid-block properties such as porosity and permeability. Parameterization is useful for data assimilation (history matching), as it maintains geological realism while reducing the number of variables to be determined. Diffusion models are a new class of generative deep-learning procedures that have been shown to outperform previous methods, such as generative adversarial networks, for image generation tasks. Diffusion models are trained to "denoise", which enables them to generate new geological realizations from input fields characterized by random noise. Latent diffusion models, which are the specific variant considered in this study, provide dimension reduction through use of a low-dimensional latent variable. The model developed in this work includes a variational autoencoder for dimension reduction and a U-net for the denoising process. Our application involves conditional 2D three-facies (channel-levee-mud) systems. The latent diffusion model is shown to provide realizations that are visually consistent with samples from geomodeling software. Quantitative metrics involving spatial and flow-response statistics are evaluated, and general agreement between the diffusion-generated models and reference realizations is observed. Stability tests are performed to assess the smoothness of the parameterization method. The latent diffusion model is then used for ensemble-based data assimilation. Two synthetic "true" models are considered. Significant uncertainty reduction, posterior P$_{10}$-P$_{90}$ forecasts that generally bracket observed data, and consistent posterior geomodels, are achieved in both cases.

### Model B Paper 4: [2601.05852]
**Title:** Kidney Cancer Detection Using 3D-Based Latent Diffusion Models
**Category:** cs.CV
**Score:** 0.8251

In this work, we present a novel latent diffusion-based pipeline for 3D kidney anomaly detection on contrast-enhanced abdominal CT. The method combines Denoising Diffusion Probabilistic Models (DDPMs), Denoising Diffusion Implicit Models (DDIMs), and Vector-Quantized Generative Adversarial Networks (VQ-GANs). Unlike prior slice-wise approaches, our method operates directly on an image volume and leverages weak supervision with only case-level pseudo-labels. We benchmark our approach against state-of-the-art supervised segmentation and detection models. This study demonstrates the feasibility and promise of 3D latent diffusion for weakly supervised anomaly detection. While the current results do not yet match supervised baselines, they reveal key directions for improving reconstruction fidelity and lesion localization. Our findings provide an important step toward annotation-efficient, generative modeling of complex abdominal anatomy.

### Model B Paper 5: [2509.00642]
**Title:** HADIS: Hybrid Adaptive Diffusion Model Serving for Efficient Text-to-Image Generation
**Category:** cs.DC
**Score:** 0.8246

Text-to-image diffusion models have achieved remarkable visual quality but incur high computational costs, making latency-aware, scalable deployment challenging. To address this, we advocate a hybrid architecture that achieves query awareness when serving diffusion models. Unlike existing query-aware serving systems that cascade lightweight and heavyweight models with a fixed configuration, our hybrid architecture first routes each query directly to a suitable model variant, then reroutes it to a cascaded heavyweight model only if necessary. We theoretically analyze conditions for the hybrid architecture to outperform non-hybrid alternatives in latency and response quality. Building on this architecture, we design HADIS, a hybrid serving system for latency-aware diffusion models that jointly optimizes cascade model selection, query routing, and resource allocation. To reduce the complexity of resource management, HADIS uses an offline profiling phase to produce a Pareto-optimal cascade configuration table. At runtime, HADIS selects the best cascade configuration and GPU allocation given latency and workload constraints. Empirical evaluations on real-world traces demonstrate that HADIS improves response quality by up to 35% while reducing latency violation rates by 2.7-45$\times$ compared to state-of-the-art model serving systems.

### Model B Paper 6: [2403.04279]
**Title:** Controllable Generation with Text-to-Image Diffusion Models: A Survey
**Category:** cs.CV
**Score:** 0.8181

In the rapidly advancing realm of visual generation, diffusion models have revolutionized the landscape, marking a significant shift in capabilities with their impressive text-guided generative functions. However, relying solely on text for conditioning these models does not fully cater to the varied and complex requirements of different applications and scenarios. Acknowledging this shortfall, a variety of studies aim to control pre-trained text-to-image (T2I) models to support novel conditions. In this survey, we undertake a thorough review of the literature on controllable generation with T2I diffusion models, covering both the theoretical foundations and practical advancements in this domain. Our review begins with a brief introduction to the basics of denoising diffusion probabilistic models (DDPMs) and widely used T2I diffusion models. We then reveal the controlling mechanisms of diffusion models, theoretically analyzing how novel conditions are introduced into the denoising process for conditional generation. Additionally, we offer a detailed overview of research in this area, organizing it into distinct categories from the condition perspective: generation with specific conditions, generation with multiple conditions, and universal controllable generation. For an exhaustive list of the controllable generation literature surveyed, please refer to our curated repository at https://github.com/PRIV-Creation/Awesome-Controllable-T2I-Diffusion-Models.

### Model B Paper 7: [2410.23530]
**Title:** There and Back Again: On the relation between Noise and Image Inversions in Diffusion Models
**Category:** cs.CV
**Score:** 0.7948

Diffusion Models achieve state-of-the-art performance in generating new samples but lack a low-dimensional latent space that encodes the data into editable features. Inversion-based methods address this by reversing the denoising trajectory, transferring images to their approximated starting noise. In this work, we thoroughly analyze this procedure and focus on the relation between the initial noise, the generated samples, and their corresponding latent encodings obtained through the DDIM inversion. First, we show that latents exhibit structural patterns in the form of less diverse noise predicted for smooth image areas (e.g., plain sky). Through a series of analyses, we trace this issue to the first inversion steps, which fail to provide accurate and diverse noise. Consequently, the DDIM inversion space is notably less manipulative than the original noise. We show that prior inversion methods do not fully resolve this issue, but our simple fix, where we replace the first DDIM Inversion steps with a forward diffusion process, successfully decorrelates latent encodings and enables higher quality editions and interpolations. The code is available at https://github.com/luk-st/taba.

### Model B Paper 8: [2410.01262]
**Title:** Improving Fine-Grained Control via Aggregation of Multiple Diffusion Models
**Category:** cs.CV
**Score:** 0.7912

While many diffusion models perform well when controlling particular aspects such as style, character, and interaction, they struggle with fine-grained control due to dataset limitations and intricate model architecture design. This paper introduces a novel training-free algorithm for fine-grained generation, called Aggregation of Multiple Diffusion Models (AMDM). The algorithm integrates features in the latent data space from multiple diffusion models within the same ecosystem into a specified model, thereby activating particular features and enabling fine-grained control. Experimental results demonstrate that AMDM significantly improves fine-grained control without training, validating its effectiveness. Additionally, it reveals that diffusion models initially focus on features such as position, attributes, and style, with later stages improving generation quality and consistency. AMDM offers a new perspective for tackling the challenges of fine-grained conditional generation in diffusion models. Specifically, it allows us to fully utilize existing or develop new conditional diffusion models that control specific aspects, and then aggregate them using the AMDM algorithm. This eliminates the need for constructing complex datasets, designing intricate model architectures, and incurring high training costs. Code is available at: https://github.com/Hammour-steak/AMDM.

### Model B Paper 9: [2601.04056]
**Title:** Bridging the Discrete-Continuous Gap: Unified Multimodal Generation via Coupled Manifold Discrete Absorbing Diffusion
**Category:** cs.CL
**Score:** 0.7897

The bifurcation of generative modeling into autoregressive approaches for discrete data (text) and diffusion approaches for continuous data (images) hinders the development of truly unified multimodal systems. While Masked Language Models (MLMs) offer efficient bidirectional context, they traditionally lack the generative fidelity of autoregressive models and the semantic continuity of diffusion models. Furthermore, extending masked generation to multimodal settings introduces severe alignment challenges and training instability. In this work, we propose \textbf{CoM-DAD} (\textbf{Co}upled \textbf{M}anifold \textbf{D}iscrete \textbf{A}bsorbing \textbf{D}iffusion), a novel probabilistic framework that reformulates multimodal generation as a hierarchical dual-process. CoM-DAD decouples high-level semantic planning from low-level token synthesis. First, we model the semantic manifold via a continuous latent diffusion process; second, we treat token generation as a discrete absorbing diffusion process, regulated by a \textbf{Variable-Rate Noise Schedule}, conditioned on these evolving semantic priors. Crucially, we introduce a \textbf{Stochastic Mixed-Modal Transport} strategy that aligns disparate modalities without requiring heavy contrastive dual-encoders. Our method demonstrates superior stability over standard masked modeling, establishing a new paradigm for scalable, unified text-image generation.

### Model B Paper 10: [2601.12283]
**Title:** SDiT: Semantic Region-Adaptive for Diffusion Transformers
**Category:** cs.CV
**Score:** 0.7844

Diffusion Transformers (DiTs) achieve state-of-the-art performance in text-to-image synthesis but remain computationally expensive due to the iterative nature of denoising and the quadratic cost of global attention. In this work, we observe that denoising dynamics are spatially non-uniform-background regions converge rapidly while edges and textured areas evolve much more actively. Building on this insight, we propose SDiT, a Semantic Region-Adaptive Diffusion Transformer that allocates computation according to regional complexity. SDiT introduces a training-free framework combining (1) semantic-aware clustering via fast Quickshift-based segmentation, (2) complexity-driven regional scheduling to selectively update informative areas, and (3) boundary-aware refinement to maintain spatial coherence. Without any model retraining or architectural modification, SDiT achieves up to 3.0x acceleration while preserving nearly identical perceptual and semantic quality to full-attention inference.

### Model B Paper 11: [2601.21284]
**Title:** PILD: Physics-Informed Learning via Diffusion
**Category:** cs.LG
**Score:** 0.7837

Diffusion models have emerged as powerful generative tools for modeling complex data distributions, yet their purely data-driven nature limits applicability in practical engineering and scientific problems where physical laws need to be followed. This paper proposes Physics-Informed Learning via Diffusion (PILD), a framework that unifies diffusion modeling and first-principles physical constraints by introducing a virtual residual observation sampled from a Laplace distribution to supervise generation during training. To further integrate physical laws, a conditional embedding module is incorporated to inject physical information into the denoising network at multiple layers, ensuring consistent guidance throughout the diffusion process. The proposed PILD framework is concise, modular, and broadly applicable to problems governed by ordinary differential equations, partial differential equations, as well as algebraic equations or inequality constraints. Extensive experiments across engineering and scientific tasks including estimating vehicle trajectories, tire forces, Darcy flow and plasma dynamics, demonstrate that our PILD substantially improves accuracy, stability, and generalization over existing physics-informed and diffusion-based baselines.

### Model B Paper 12: [2504.13745]
**Title:** ESPLoRA: Enhanced Spatial Precision with Low-Rank Adaption in Text-to-Image Diffusion Models for High-Definition Synthesis
**Category:** cs.CV
**Score:** 0.7799

Diffusion models have revolutionized text-to-image (T2I) synthesis, producing high-quality, photorealistic images. However, they still struggle to properly render the spatial relationships described in text prompts. To address the lack of spatial information in T2I generations, existing methods typically use external network conditioning and predefined layouts, resulting in higher computational costs and reduced flexibility. Our approach builds upon a curated dataset of spatially explicit prompts, meticulously extracted and synthesized from LAION-400M to ensure precise alignment between textual descriptions and spatial layouts. Alongside this dataset, we present ESPLoRA, a flexible fine-tuning framework based on Low-Rank Adaptation, specifically designed to enhance spatial consistency in generative models without increasing generation time or compromising the quality of the outputs. In addition to ESPLoRA, we propose refined evaluation metrics grounded in geometric constraints, capturing 3D spatial relations such as "in front of" or "behind". These metrics also expose spatial biases in T2I models which, even when not fully mitigated, can be strategically exploited by our TORE algorithm to further improve the spatial consistency of generated images. Our method outperforms CoMPaSS, the current baseline framework, on spatial consistency benchmarks.

### Model B Paper 13: [2601.03499]
**Title:** GeoDiff-SAR: A Geometric Prior Guided Diffusion Model for SAR Image Generation
**Category:** eess.IV
**Score:** 0.7751

Synthetic Aperture Radar (SAR) imaging results are highly sensitive to observation geometries and the geometric parameters of targets. However, existing generative methods primarily operate within the image domain, neglecting explicit geometric information. This limitation often leads to unsatisfactory generation quality and the inability to precisely control critical parameters such as azimuth angles. To address these challenges, we propose GeoDiff-SAR, a geometric prior guided diffusion model for high-fidelity SAR image generation. Specifically, GeoDiff-SAR first efficiently simulates the geometric structures and scattering relationships inherent in real SAR imaging by calculating SAR point clouds at specific azimuths, which serves as a robust physical guidance. Secondly, to effectively fuse multi-modal information, we employ a feature fusion gating network based on Feature-wise Linear Modulation (FiLM) to dynamically regulate the weight distribution of 3D physical information, image control parameters, and textual description parameters. Thirdly, we utilize the Low-Rank Adaptation (LoRA) architecture to perform lightweight fine-tuning on the advanced Stable Diffusion 3.5 (SD3.5) model, enabling it to rapidly adapt to the distribution characteristics of the SAR domain. To validate the effectiveness of GeoDiff-SAR, extensive comparative experiments were conducted on real-world SAR datasets. The results demonstrate that data generated by GeoDiff-SAR exhibits high fidelity and effectively enhances the accuracy of downstream classification tasks. In particular, it significantly improves recognition performance across different azimuth angles, thereby underscoring the superiority of physics-guided generation.

### Model B Paper 14: [2601.09044]
**Title:** POWDR: Pathology-preserving Outpainting with Wavelet Diffusion for 3D MRI
**Category:** eess.IV
**Score:** 0.7724

Medical imaging datasets often suffer from class imbalance and limited availability of pathology-rich cases, which constrains the performance of machine learning models for segmentation, classification, and vision-language tasks. To address this challenge, we propose POWDR, a pathology-preserving outpainting framework for 3D MRI based on a conditioned wavelet diffusion model. Unlike conventional augmentation or unconditional synthesis, POWDR retains real pathological regions while generating anatomically plausible surrounding tissue, enabling diversity without fabricating lesions.
  Our approach leverages wavelet-domain conditioning to enhance high-frequency detail and mitigate blurring common in latent diffusion models. We introduce a random connected mask training strategy to overcome conditioning-induced collapse and improve diversity outside the lesion. POWDR is evaluated on brain MRI using BraTS datasets and extended to knee MRI to demonstrate tissue-agnostic applicability. Quantitative metrics (FID, SSIM, LPIPS) confirm image realism, while diversity analysis shows significant improvement with random-mask training (cosine similarity reduced from 0.9947 to 0.9580; KL divergence increased from 0.00026 to 0.01494). Clinically relevant assessments reveal gains in tumor segmentation performance using nnU-Net, with Dice scores improving from 0.6992 to 0.7137 when adding 50 synthetic cases. Tissue volume analysis indicates no significant differences for CSF and GM compared to real images.
  These findings highlight POWDR as a practical solution for addressing data scarcity and class imbalance in medical imaging. The method is extensible to multiple anatomies and offers a controllable framework for generating diverse, pathology-preserving synthetic data to support robust model development.

### Model B Paper 15: [2601.21348]
**Title:** Memorization Control in Diffusion Models from Denoising-centric Perspective
**Category:** cs.LG
**Score:** 0.7717

Controlling memorization in diffusion models is critical for applications that require generated data to closely match the training distribution. Existing approaches mainly focus on data centric or model centric modifications, treating the diffusion model as an isolated predictor. In this paper, we study memorization in diffusion models from a denoising centric perspective. We show that uniform timestep sampling leads to unequal learning contributions across denoising steps due to differences in signal to noise ratio, which biases training toward memorization. To address this, we propose a timestep sampling strategy that explicitly controls where learning occurs along the denoising trajectory. By adjusting the width of the confidence interval, our method provides direct control over the memorization generalization trade off. Experiments on image and 1D signal generation tasks demonstrate that shifting learning emphasis toward later denoising steps consistently reduces memorization and improves distributional alignment with training data, validating the generality and effectiveness of our approach.

### Model B Paper 16: [2601.02881]
**Title:** Towards Agnostic and Holistic Universal Image Segmentation with Bit Diffusion
**Category:** cs.CV
**Score:** 0.7649

This paper introduces a diffusion-based framework for universal image segmentation, making agnostic segmentation possible without depending on mask-based frameworks and instead predicting the full segmentation in a holistic manner. We present several key adaptations to diffusion models, which are important in this discrete setting. Notably, we show that a location-aware palette with our 2D gray code ordering improves performance. Adding a final tanh activation function is crucial for discrete data. On optimizing diffusion parameters, the sigmoid loss weighting consistently outperforms alternatives, regardless of the prediction type used, and we settle on x-prediction. While our current model does not yet surpass leading mask-based architectures, it narrows the performance gap and introduces unique capabilities, such as principled ambiguity modeling, that these models lack. All models were trained from scratch, and we believe that combining our proposed improvements with large-scale pretraining or promptable conditioning could lead to competitive models.

### Model B Paper 17: [2306.04321]
**Title:** Generative Semantic Communication: Diffusion Models Beyond Bit Recovery
**Category:** cs.AI
**Score:** 0.7608

Semantic communication is expected to be one of the cores of next-generation AI-based communications. One of the possibilities offered by semantic communication is the capability to regenerate, at the destination side, images or videos semantically equivalent to the transmitted ones, without necessarily recovering the transmitted sequence of bits. The current solutions still lack the ability to build complex scenes from the received partial information. Clearly, there is an unmet need to balance the effectiveness of generation methods and the complexity of the transmitted information, possibly taking into account the goal of communication. In this paper, we aim to bridge this gap by proposing a novel generative diffusion-guided framework for semantic communication that leverages the strong abilities of diffusion models in synthesizing multimedia content while preserving semantic features. We reduce bandwidth usage by sending highly-compressed semantic information only. Then, the diffusion model learns to synthesize semantic-consistent scenes through spatially-adaptive normalizations from such denoised semantic information. We prove, through an in-depth assessment of multiple scenarios, that our method outperforms existing solutions in generating high-quality images with preserved semantic information even in cases where the received content is significantly degraded. More specifically, our results show that objects, locations, and depths are still recognizable even in the presence of extremely noisy conditions of the communication channel. The code is available at https://github.com/ispamm/GESCO.

### Model B Paper 18: [2510.06584]
**Title:** Improving Artifact Robustness for CT Deep Learning Models Without Labeled Artifact Images via Domain Adaptation
**Category:** cs.CV
**Score:** 0.7605

If a CT scanner introduces a new artifact not present in the training labels, the model may misclassify the images. Although modern CT scanners include design features which mitigate these artifacts, unanticipated or difficult-to-mitigate artifacts can still appear in practice. The direct solution of labeling images from this new distribution can be costly. As a more accessible alternative, this study evaluates domain adaptation as an approach for training models that maintain classification performance despite new artifacts, even without corresponding labels. We simulate ring artifacts from detector gain error in sinogram space and evaluate domain adversarial neural networks (DANN) against baseline and augmentation-based approaches on the OrganAMNIST abdominal CT dataset. We simulate the absence of labels from an unseen distribution via masking in the loss function and selectively detaching unlabeled instances from the computational graph. Our results demonstrate that baseline models trained only on clean images fail to generalize to images with ring artifacts, and traditional augmentation with other distortion types provides no improvement on unseen artifact domains. In contrast, the DANN approach improves classification accuracy on ring artifact images using only unlabeled artifact data during training, demonstrating the viability of domain adaptation for artifact robustness. The domain-adapted model achieved a classification accuracy of 77.4% on ring artifact test data, 38.7% higher than a baseline model only trained on images with no artifact. These findings provide empirical evidence that domain adaptation can effectively address distribution shift in medical imaging without requiring expensive expert labeling of new artifact distributions, suggesting promise for deployment in clinical settings where novel artifacts may emerge.

### Model B Paper 19: [2505.08142]
**Title:** Highly Undersampled MRI Reconstruction via a Single Posterior Sampling of Diffusion Models
**Category:** eess.IV
**Score:** 0.7577

Incoherent k-space undersampling and deep learning-based reconstruction methods have shown great success in accelerating MRI. However, the performance of most previous methods will degrade dramatically under high acceleration factors, e.g., 8$\times$ or higher. Recently, denoising diffusion models (DM) have demonstrated promising results in solving this issue; however, one major drawback of the DM methods is the long inference time due to a dramatic number of iterative reverse posterior sampling steps. In this work, a Single Step Diffusion Model-based reconstruction framework, namely SSDM-MRI, is proposed for restoring MRI images from highly undersampled k-space. The proposed method achieves one-step reconstruction by first training a conditional DM and then iteratively distilling this model four times using an iterative selective distillation algorithm, which works synergistically with a shortcut reverse sampling strategy for model inference. Comprehensive experiments were carried out on both publicly available fastMRI brain and knee images, as well as an in-house multi-echo GRE (QSM) subject. Overall, the results showed that SSDM-MRI outperformed other methods in terms of numerical metrics (e.g., PSNR and SSIM), error maps, image fine details, and latent susceptibility information hidden in MRI phase images. In addition, the reconstruction time for a 320$\times$320 brain slice of SSDM-MRI is only 0.45 second, which is only comparable to that of a simple U-net, making it a highly effective solution for MRI reconstruction tasks.

### Model B Paper 20: [2601.20391]
**Title:** Eliminating Hallucination in Diffusion-Augmented Interactive Text-to-Image Retrieval
**Category:** cs.IR
**Score:** 0.7550

Diffusion-Augmented Interactive Text-to-Image Retrieval (DAI-TIR) is a promising paradigm that improves retrieval performance by generating query images via diffusion models and using them as additional ``views'' of the user's intent. However, these generative views can be incorrect because diffusion generation may introduce hallucinated visual cues that conflict with the original query text. Indeed, we empirically demonstrate that these hallucinated cues can substantially degrade DAI-TIR performance. To address this, we propose Diffusion-aware Multi-view Contrastive Learning (DMCL), a hallucination-robust training framework that casts DAI-TIR as joint optimization over representations of query intent and the target image. DMCL introduces semantic-consistency and diffusion-aware contrastive objectives to align textual and diffusion-generated query views while suppressing hallucinated query signals. This yields an encoder that acts as a semantic filter, effectively mapping hallucinated cues into a null space, improving robustness to spurious cues and better representing the user's intent. Attention visualization and geometric embedding-space analyses corroborate this filtering behavior. Across five standard benchmarks, DMCL delivers consistent improvements in multi-round Hits@10, reaching as high as 7.37\% over prior fine-tuned and zero-shot baselines, which indicates it is a general and robust training framework for DAI-TIR.

---


### Model A Paper 1: [2601.11085]
**Title:** Generation of Chest CT pulmonary Nodule Images by Latent Diffusion Models using the LIDC-IDRI Dataset
**Category:** eess.IV
**Score:** 0.7981

Recently, computer-aided diagnosis systems have been developed to support diagnosis, but their performance depends heavily on the quality and quantity of training data. However, in clinical practice, it is difficult to collect the large amount of CT images for specific cases, such as small cell carcinoma with low epidemiological incidence or benign tumors that are difficult to distinguish from malignant ones. This leads to the challenge of data imbalance. In this study, to address this issue, we proposed a method to automatically generate chest CT nodule images that capture target features using latent diffusion models (LDM) and verified its effectiveness. Using the LIDC-IDRI dataset, we created pairs of nodule images and finding-based text prompts based on physician evaluations. For the image generation models, we used Stable Diffusion version 1.5 (SDv1) and 2.0 (SDv2), which are types of LDM. Each model was fine-tuned using the created dataset. During the generation process, we adjusted the guidance scale (GS), which indicates the fidelity to the input text. Both quantitative and subjective evaluations showed that SDv2 (GS = 5) achieved the best performance in terms of image quality, diversity, and text consistency. In the subjective evaluation, no statistically significant differences were observed between the generated images and real images, confirming that the quality was equivalent to real clinical images. We proposed a method for generating chest CT nodule images based on input text using LDM. Evaluation results demonstrated that the proposed method could generate high-quality images that successfully capture specific medical features.

### Model A Paper 2: [2403.04279]
**Title:** Controllable Generation with Text-to-Image Diffusion Models: A Survey
**Category:** cs.CV
**Score:** 0.7966

In the rapidly advancing realm of visual generation, diffusion models have revolutionized the landscape, marking a significant shift in capabilities with their impressive text-guided generative functions. However, relying solely on text for conditioning these models does not fully cater to the varied and complex requirements of different applications and scenarios. Acknowledging this shortfall, a variety of studies aim to control pre-trained text-to-image (T2I) models to support novel conditions. In this survey, we undertake a thorough review of the literature on controllable generation with T2I diffusion models, covering both the theoretical foundations and practical advancements in this domain. Our review begins with a brief introduction to the basics of denoising diffusion probabilistic models (DDPMs) and widely used T2I diffusion models. We then reveal the controlling mechanisms of diffusion models, theoretically analyzing how novel conditions are introduced into the denoising process for conditional generation. Additionally, we offer a detailed overview of research in this area, organizing it into distinct categories from the condition perspective: generation with specific conditions, generation with multiple conditions, and universal controllable generation. For an exhaustive list of the controllable generation literature surveyed, please refer to our curated repository at https://github.com/PRIV-Creation/Awesome-Controllable-T2I-Diffusion-Models.

### Model A Paper 3: [2601.05852]
**Title:** Kidney Cancer Detection Using 3D-Based Latent Diffusion Models
**Category:** cs.CV
**Score:** 0.7677

In this work, we present a novel latent diffusion-based pipeline for 3D kidney anomaly detection on contrast-enhanced abdominal CT. The method combines Denoising Diffusion Probabilistic Models (DDPMs), Denoising Diffusion Implicit Models (DDIMs), and Vector-Quantized Generative Adversarial Networks (VQ-GANs). Unlike prior slice-wise approaches, our method operates directly on an image volume and leverages weak supervision with only case-level pseudo-labels. We benchmark our approach against state-of-the-art supervised segmentation and detection models. This study demonstrates the feasibility and promise of 3D latent diffusion for weakly supervised anomaly detection. While the current results do not yet match supervised baselines, they reveal key directions for improving reconstruction fidelity and lesion localization. Our findings provide an important step toward annotation-efficient, generative modeling of complex abdominal anatomy.

### Model A Paper 4: [2406.14815]
**Title:** Latent diffusion models for parameterization and data assimilation of facies-based geomodels
**Category:** cs.CV
**Score:** 0.7374

Geological parameterization entails the representation of a geomodel using a small set of latent variables and a mapping from these variables to grid-block properties such as porosity and permeability. Parameterization is useful for data assimilation (history matching), as it maintains geological realism while reducing the number of variables to be determined. Diffusion models are a new class of generative deep-learning procedures that have been shown to outperform previous methods, such as generative adversarial networks, for image generation tasks. Diffusion models are trained to "denoise", which enables them to generate new geological realizations from input fields characterized by random noise. Latent diffusion models, which are the specific variant considered in this study, provide dimension reduction through use of a low-dimensional latent variable. The model developed in this work includes a variational autoencoder for dimension reduction and a U-net for the denoising process. Our application involves conditional 2D three-facies (channel-levee-mud) systems. The latent diffusion model is shown to provide realizations that are visually consistent with samples from geomodeling software. Quantitative metrics involving spatial and flow-response statistics are evaluated, and general agreement between the diffusion-generated models and reference realizations is observed. Stability tests are performed to assess the smoothness of the parameterization method. The latent diffusion model is then used for ensemble-based data assimilation. Two synthetic "true" models are considered. Significant uncertainty reduction, posterior P$_{10}$-P$_{90}$ forecasts that generally bracket observed data, and consistent posterior geomodels, are achieved in both cases.

### Model A Paper 5: [2503.06884]
**Title:** Text-to-Image Diffusion Models Cannot Count, and Prompt Refinement Cannot Help
**Category:** cs.CV
**Score:** 0.7336

Generative modeling is widely regarded as one of the most essential problems in today's AI community, with text-to-image generation having gained unprecedented real-world impacts. Among various approaches, diffusion models have achieved remarkable success and have become the de facto solution for text-to-image generation. However, despite their impressive performance, these models exhibit fundamental limitations in adhering to numerical constraints in user instructions, frequently generating images with an incorrect number of objects. While several prior works have mentioned this issue, a comprehensive and rigorous evaluation of this limitation remains lacking. To address this gap, we introduce T2ICountBench, a novel benchmark designed to rigorously evaluate the counting ability of state-of-the-art text-to-image diffusion models. Our benchmark encompasses a diverse set of generative models, including both open-source and private systems. It explicitly isolates counting performance from other capabilities, provides structured difficulty levels, and incorporates human evaluations to ensure high reliability.
  Extensive evaluations with T2ICountBench reveal that all state-of-the-art diffusion models fail to generate the correct number of objects, with accuracy dropping significantly as the number of objects increases. Additionally, an exploratory study on prompt refinement demonstrates that such simple interventions generally do not improve counting accuracy. Our findings highlight the inherent challenges in numerical understanding within diffusion models and point to promising directions for future improvements.

### Model A Paper 6: [2502.09665]
**Title:** Revealing Subtle Phenotypes in Small Microscopy Datasets Using Latent Diffusion Models
**Category:** cs.CV
**Score:** 0.7332

Identifying subtle phenotypic variations in cellular images is critical for advancing biological research and accelerating drug discovery. These variations are often masked by the inherent cellular heterogeneity, making it challenging to distinguish differences between experimental conditions. Recent advancements in deep generative models have demonstrated significant potential for revealing these nuanced phenotypes through image translation, opening new frontiers in cellular and molecular biology as well as the identification of novel biomarkers. Among these generative models, diffusion models stand out for their ability to produce high-quality, realistic images. However, training diffusion models typically requires large datasets and substantial computational resources, both of which can be limited in biological research. In this work, we propose a novel approach that leverages pre-trained latent diffusion models to uncover subtle phenotypic changes. We validate our approach qualitatively and quantitatively on several small datasets of microscopy images. Our findings reveal that our approach enables effective detection of phenotypic variations, capturing both visually apparent and imperceptible differences. Ultimately, our results highlight the promising potential of this approach for phenotype detection, especially in contexts constrained by limited data and computational capacity.

### Model A Paper 7: [2207.00050]
**Title:** Semantic Image Synthesis via Diffusion Models
**Category:** cs.CV
**Score:** 0.7053

Denoising Diffusion Probabilistic Models (DDPMs) have achieved remarkable success in various image generation tasks compared with Generative Adversarial Nets (GANs). Recent work on semantic image synthesis mainly follows the de facto GAN-based approaches, which may lead to unsatisfactory quality or diversity of generated images. In this paper, we propose a novel framework based on DDPM for semantic image synthesis. Unlike previous conditional diffusion model directly feeds the semantic layout and noisy image as input to a U-Net structure, which may not fully leverage the information in the input semantic mask, our framework processes semantic layout and noisy image differently. It feeds noisy image to the encoder of the U-Net structure while the semantic layout to the decoder by multi-layer spatially-adaptive normalization operators. To further improve the generation quality and semantic interpretability in semantic image synthesis, we introduce the classifier-free guidance sampling strategy, which acknowledge the scores of an unconditional model for sampling process. Extensive experiments on four benchmark datasets demonstrate the effectiveness of our proposed method, achieving state-of-the-art performance in terms of fidelity (FID) and diversity (LPIPS). Our code and pretrained models are available at https://github.com/WeilunWang/semantic-diffusion-model.

### Model A Paper 8: [2501.01761]
**Title:** Adverse Weather Conditions Augmentation of LiDAR Scenes with Latent Diffusion Models
**Category:** cs.CV
**Score:** 0.6791

LiDAR scenes constitute a fundamental source for several autonomous driving applications. Despite the existence of several datasets, scenes from adverse weather conditions are rarely available. This limits the robustness of downstream machine learning models, and restrains the reliability of autonomous driving systems in particular locations and seasons. Collecting feature-diverse scenes under adverse weather conditions is challenging due to seasonal limitations. Generative models are therefore essentials, especially for generating adverse weather conditions for specific driving scenarios. In our work, we propose a latent diffusion process constituted by autoencoder and latent diffusion models. Moreover, we leverage the clear condition LiDAR scenes with a postprocessing step to improve the realism of the generated adverse weather condition scenes.

### Model A Paper 9: [2406.18944]
**Title:** Rethinking and Red-Teaming Protective Perturbation in Personalized Diffusion Models
**Category:** cs.CV
**Score:** 0.6772

Personalized diffusion models (PDMs) have become prominent for adapting pre-trained text-to-image models to generate images of specific subjects using minimal training data. However, PDMs are susceptible to minor adversarial perturbations, leading to significant degradation when fine-tuned on corrupted datasets. These vulnerabilities are exploited to create protective perturbations that prevent unauthorized image generation. Existing purification methods attempt to red-team the protective perturbation to break the protection but often over-purify images, resulting in information loss. In this work, we conduct an in-depth analysis of the fine-tuning process of PDMs through the lens of shortcut learning. We hypothesize and empirically demonstrate that adversarial perturbations induce a latent-space misalignment between images and their text prompts in the CLIP embedding space. This misalignment causes the model to erroneously associate noisy patterns with unique identifiers during fine-tuning, resulting in poor generalization. Based on these insights, we propose a systematic red-teaming framework that includes data purification and contrastive decoupling learning. We first employ off-the-shelf image restoration techniques to realign images with their original semantic content in latent space. Then, we introduce contrastive decoupling learning with noise tokens to decouple the learning of personalized concepts from spurious noise patterns. Our study not only uncovers shortcut learning vulnerabilities in PDMs but also provides a thorough evaluation framework for developing stronger protection. Our extensive evaluation demonstrates its advantages over existing purification methods and its robustness against adaptive perturbations.

### Model A Paper 10: [2504.13745]
**Title:** ESPLoRA: Enhanced Spatial Precision with Low-Rank Adaption in Text-to-Image Diffusion Models for High-Definition Synthesis
**Category:** cs.CV
**Score:** 0.6728

Diffusion models have revolutionized text-to-image (T2I) synthesis, producing high-quality, photorealistic images. However, they still struggle to properly render the spatial relationships described in text prompts. To address the lack of spatial information in T2I generations, existing methods typically use external network conditioning and predefined layouts, resulting in higher computational costs and reduced flexibility. Our approach builds upon a curated dataset of spatially explicit prompts, meticulously extracted and synthesized from LAION-400M to ensure precise alignment between textual descriptions and spatial layouts. Alongside this dataset, we present ESPLoRA, a flexible fine-tuning framework based on Low-Rank Adaptation, specifically designed to enhance spatial consistency in generative models without increasing generation time or compromising the quality of the outputs. In addition to ESPLoRA, we propose refined evaluation metrics grounded in geometric constraints, capturing 3D spatial relations such as "in front of" or "behind". These metrics also expose spatial biases in T2I models which, even when not fully mitigated, can be strategically exploited by our TORE algorithm to further improve the spatial consistency of generated images. Our method outperforms CoMPaSS, the current baseline framework, on spatial consistency benchmarks.

### Model A Paper 11: [2306.04321]
**Title:** Generative Semantic Communication: Diffusion Models Beyond Bit Recovery
**Category:** cs.AI
**Score:** 0.6620

Semantic communication is expected to be one of the cores of next-generation AI-based communications. One of the possibilities offered by semantic communication is the capability to regenerate, at the destination side, images or videos semantically equivalent to the transmitted ones, without necessarily recovering the transmitted sequence of bits. The current solutions still lack the ability to build complex scenes from the received partial information. Clearly, there is an unmet need to balance the effectiveness of generation methods and the complexity of the transmitted information, possibly taking into account the goal of communication. In this paper, we aim to bridge this gap by proposing a novel generative diffusion-guided framework for semantic communication that leverages the strong abilities of diffusion models in synthesizing multimedia content while preserving semantic features. We reduce bandwidth usage by sending highly-compressed semantic information only. Then, the diffusion model learns to synthesize semantic-consistent scenes through spatially-adaptive normalizations from such denoised semantic information. We prove, through an in-depth assessment of multiple scenarios, that our method outperforms existing solutions in generating high-quality images with preserved semantic information even in cases where the received content is significantly degraded. More specifically, our results show that objects, locations, and depths are still recognizable even in the presence of extremely noisy conditions of the communication channel. The code is available at https://github.com/ispamm/GESCO.

### Model A Paper 12: [2601.04056]
**Title:** Bridging the Discrete-Continuous Gap: Unified Multimodal Generation via Coupled Manifold Discrete Absorbing Diffusion
**Category:** cs.CL
**Score:** 0.6561

The bifurcation of generative modeling into autoregressive approaches for discrete data (text) and diffusion approaches for continuous data (images) hinders the development of truly unified multimodal systems. While Masked Language Models (MLMs) offer efficient bidirectional context, they traditionally lack the generative fidelity of autoregressive models and the semantic continuity of diffusion models. Furthermore, extending masked generation to multimodal settings introduces severe alignment challenges and training instability. In this work, we propose \textbf{CoM-DAD} (\textbf{Co}upled \textbf{M}anifold \textbf{D}iscrete \textbf{A}bsorbing \textbf{D}iffusion), a novel probabilistic framework that reformulates multimodal generation as a hierarchical dual-process. CoM-DAD decouples high-level semantic planning from low-level token synthesis. First, we model the semantic manifold via a continuous latent diffusion process; second, we treat token generation as a discrete absorbing diffusion process, regulated by a \textbf{Variable-Rate Noise Schedule}, conditioned on these evolving semantic priors. Crucially, we introduce a \textbf{Stochastic Mixed-Modal Transport} strategy that aligns disparate modalities without requiring heavy contrastive dual-encoders. Our method demonstrates superior stability over standard masked modeling, establishing a new paradigm for scalable, unified text-image generation.

### Model A Paper 13: [2511.16870]
**Title:** Align & Invert: Solving Inverse Problems with Diffusion and Flow-based Models via Representation Alignment
**Category:** cs.CV
**Score:** 0.6507

Enforcing alignment between the internal representations of diffusion or flow-based generative models and those of pretrained self-supervised encoders has recently been shown to provide a powerful inductive bias, improving both convergence and sample quality. In this work, we extend this idea to inverse problems, where pretrained generative models are employed as priors. We propose applying representation alignment (REPA) between diffusion or flow-based models and a DINOv2 visual encoder, to guide the reconstruction process at inference time. Although ground-truth signals are unavailable in inverse problems, we empirically show that aligning model representations of approximate target features can substantially enhance reconstruction quality and perceptual realism. We provide theoretical results showing (a) that REPA regularization can be viewed as a variational approach for minimizing a divergence measure in the DINOv2 embedding space, and (b) how under certain regularity assumptions REPA updates steer the latent diffusion states toward those of the clean image. These results offer insights into the role of REPA in improving perceptual fidelity. Finally, we demonstrate the generality of our approach by We integrate REPA into multiple state-of-the-art inverse problem solvers, and provide extensive experiments on super-resolution, box inpainting, Gaussian deblurring, and motion deblurring confirming that our method consistently improves reconstruction quality, while also providing efficiency gains reducing the number of required discretization steps.

### Model A Paper 14: [2410.01262]
**Title:** Improving Fine-Grained Control via Aggregation of Multiple Diffusion Models
**Category:** cs.CV
**Score:** 0.6493

While many diffusion models perform well when controlling particular aspects such as style, character, and interaction, they struggle with fine-grained control due to dataset limitations and intricate model architecture design. This paper introduces a novel training-free algorithm for fine-grained generation, called Aggregation of Multiple Diffusion Models (AMDM). The algorithm integrates features in the latent data space from multiple diffusion models within the same ecosystem into a specified model, thereby activating particular features and enabling fine-grained control. Experimental results demonstrate that AMDM significantly improves fine-grained control without training, validating its effectiveness. Additionally, it reveals that diffusion models initially focus on features such as position, attributes, and style, with later stages improving generation quality and consistency. AMDM offers a new perspective for tackling the challenges of fine-grained conditional generation in diffusion models. Specifically, it allows us to fully utilize existing or develop new conditional diffusion models that control specific aspects, and then aggregate them using the AMDM algorithm. This eliminates the need for constructing complex datasets, designing intricate model architectures, and incurring high training costs. Code is available at: https://github.com/Hammour-steak/AMDM.

### Model A Paper 15: [2509.00642]
**Title:** HADIS: Hybrid Adaptive Diffusion Model Serving for Efficient Text-to-Image Generation
**Category:** cs.DC
**Score:** 0.6447

Text-to-image diffusion models have achieved remarkable visual quality but incur high computational costs, making latency-aware, scalable deployment challenging. To address this, we advocate a hybrid architecture that achieves query awareness when serving diffusion models. Unlike existing query-aware serving systems that cascade lightweight and heavyweight models with a fixed configuration, our hybrid architecture first routes each query directly to a suitable model variant, then reroutes it to a cascaded heavyweight model only if necessary. We theoretically analyze conditions for the hybrid architecture to outperform non-hybrid alternatives in latency and response quality. Building on this architecture, we design HADIS, a hybrid serving system for latency-aware diffusion models that jointly optimizes cascade model selection, query routing, and resource allocation. To reduce the complexity of resource management, HADIS uses an offline profiling phase to produce a Pareto-optimal cascade configuration table. At runtime, HADIS selects the best cascade configuration and GPU allocation given latency and workload constraints. Empirical evaluations on real-world traces demonstrate that HADIS improves response quality by up to 35% while reducing latency violation rates by 2.7-45$\times$ compared to state-of-the-art model serving systems.

### Model A Paper 16: [2506.16233]
**Title:** Can AI Dream of Unseen Galaxies? Conditional Diffusion Model for Galaxy Morphology Augmentation
**Category:** astro-ph.GA
**Score:** 0.6406

Observational astronomy relies on visual feature identification to detect critical astrophysical phenomena. While machine learning (ML) increasingly automates this process, models often struggle with generalization in large-scale surveys due to the limited representativeness of labeled datasets, whether from simulations or human annotation, a challenge pronounced for rare yet scientifically valuable objects. To address this, we propose a conditional diffusion model to synthesize realistic galaxy images for augmenting ML training data (hereafter GalaxySD). Leveraging the Galaxy Zoo 2 dataset which contains visual feature, galaxy image pairs from volunteer annotation, we demonstrate that GalaxySD generates diverse, high-fidelity galaxy images that closely adhere to the specified morphological feature conditions. Moreover, this model enables generative extrapolation to project well-annotated data into unseen domains and advancing rare object detection. Integrating synthesized images into ML pipelines improves performance in standard morphology classification, boosting completeness and purity by up to 30% across key metrics. For rare object detection, using early-type galaxies with prominent dust lane features (~0.1% in GZ2 dataset) as a test case, our approach doubled the number of detected instances, from 352 to 872, compared to previous studies based on visual inspection. This study highlights the power of generative models to bridge gaps between scarce labeled data and the vast, uncharted parameter space of observational astronomy and sheds insight for future astrophysical foundation model developments. Our project homepage is available at https://galaxysd-webpage.streamlit.app/.

### Model A Paper 17: [2601.09213]
**Title:** SpikeVAEDiff: Neural Spike-based Natural Visual Scene Reconstruction via VD-VAE and Versatile Diffusion
**Category:** cs.CV
**Score:** 0.6390

Reconstructing natural visual scenes from neural activity is a key challenge in neuroscience and computer vision. We present SpikeVAEDiff, a novel two-stage framework that combines a Very Deep Variational Autoencoder (VDVAE) and the Versatile Diffusion model to generate high-resolution and semantically meaningful image reconstructions from neural spike data. In the first stage, VDVAE produces low-resolution preliminary reconstructions by mapping neural spike signals to latent representations. In the second stage, regression models map neural spike signals to CLIP-Vision and CLIP-Text features, enabling Versatile Diffusion to refine the images via image-to-image generation.
  We evaluate our approach on the Allen Visual Coding-Neuropixels dataset and analyze different brain regions. Our results show that the VISI region exhibits the most prominent activation and plays a key role in reconstruction quality. We present both successful and unsuccessful reconstruction examples, reflecting the challenges of decoding neural activity. Compared with fMRI-based approaches, spike data provides superior temporal and spatial resolution. We further validate the effectiveness of the VDVAE model and conduct ablation studies demonstrating that data from specific brain regions significantly enhances reconstruction performance.

### Model A Paper 18: [2503.21791]
**Title:** SeisRDT: Latent Diffusion Model Based On Representation Learning For Seismic Data Interpolation And Reconstruction
**Category:** physics.geo-ph
**Score:** 0.6365

Due to limitations such as geographic, physical, or economic factors, collected seismic data often have missing traces. Traditional seismic data reconstruction methods face the challenge of selecting numerous empirical parameters and struggle to handle large-scale continuous missing traces. With the advancement of deep learning, various diffusion models have demonstrated strong reconstruction capabilities. However, these UNet-based diffusion models require significant computational resources and struggle to learn the correlation between different traces in seismic data. To address the complex and irregular missing situations in seismic data, we propose a latent diffusion transformer utilizing representation learning for seismic data reconstruction. By employing a mask modeling scheme based on representation learning, the representation module uses the token sequence of known data to infer the token sequence of unknown data, enabling the reconstructed data from the diffusion model to have a more consistent data distribution and better correlation and accuracy with the known data. We propose the Representation Diffusion Transformer architecture, and a relative positional bias is added when calculating attention, enabling the diffusion model to achieve global modeling capability for seismic data. Using a pre-trained data compression model compresses the training and inference processes of the diffusion model into a latent space, which, compared to other diffusion model-based reconstruction methods, reduces computational and inference costs. Reconstruction experiments on field and synthetic datasets indicate that our method achieves higher reconstruction accuracy than existing methods and can handle various complex missing scenarios.

### Model A Paper 19: [2601.09044]
**Title:** POWDR: Pathology-preserving Outpainting with Wavelet Diffusion for 3D MRI
**Category:** eess.IV
**Score:** 0.6352

Medical imaging datasets often suffer from class imbalance and limited availability of pathology-rich cases, which constrains the performance of machine learning models for segmentation, classification, and vision-language tasks. To address this challenge, we propose POWDR, a pathology-preserving outpainting framework for 3D MRI based on a conditioned wavelet diffusion model. Unlike conventional augmentation or unconditional synthesis, POWDR retains real pathological regions while generating anatomically plausible surrounding tissue, enabling diversity without fabricating lesions.
  Our approach leverages wavelet-domain conditioning to enhance high-frequency detail and mitigate blurring common in latent diffusion models. We introduce a random connected mask training strategy to overcome conditioning-induced collapse and improve diversity outside the lesion. POWDR is evaluated on brain MRI using BraTS datasets and extended to knee MRI to demonstrate tissue-agnostic applicability. Quantitative metrics (FID, SSIM, LPIPS) confirm image realism, while diversity analysis shows significant improvement with random-mask training (cosine similarity reduced from 0.9947 to 0.9580; KL divergence increased from 0.00026 to 0.01494). Clinically relevant assessments reveal gains in tumor segmentation performance using nnU-Net, with Dice scores improving from 0.6992 to 0.7137 when adding 50 synthetic cases. Tissue volume analysis indicates no significant differences for CSF and GM compared to real images.
  These findings highlight POWDR as a practical solution for addressing data scarcity and class imbalance in medical imaging. The method is extensible to multiple anatomies and offers a controllable framework for generating diverse, pathology-preserving synthetic data to support robust model development.

### Model A Paper 20: [2601.08022]
**Title:** Training Free Zero-Shot Visual Anomaly Localization via Diffusion Inversion
**Category:** cs.CV
**Score:** 0.6327

Zero-Shot image Anomaly Detection (ZSAD) aims to detect and localise anomalies without access to any normal training samples of the target data. While recent ZSAD approaches leverage additional modalities such as language to generate fine-grained prompts for localisation, vision-only methods remain limited to image-level classification, lacking spatial precision. In this work, we introduce a simple yet effective training-free vision-only ZSAD framework that circumvents the need for fine-grained prompts by leveraging the inversion of a pretrained Denoising Diffusion Implicit Model (DDIM). Specifically, given an input image and a generic text description (e.g., "an image of an [object class]"), we invert the image to obtain latent representations and initiate the denoising process from a fixed intermediate timestep to reconstruct the image. Since the underlying diffusion model is trained solely on normal data, this process yields a normal-looking reconstruction. The discrepancy between the input image and the reconstructed one highlights potential anomalies. Our method achieves state-of-the-art performance on VISA dataset, demonstrating strong localisation capabilities without auxiliary modalities and facilitating a shift away from prompt dependence for zero-shot anomaly detection research. Code is available at https://github.com/giddyyupp/DIVAD.

---

## Review Instructions

You are reviewing recommendations from two models for the interest profile "Diffusion models for generation".
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
