# Awesome Safe Learning for Contact-rich Robotic Tasks
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-green) 
![Stars](https://img.shields.io/github/stars/jack-sherman01/Awesome-Learning4Safe-Contact-rich-tasks)
![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Funiversea%2FAwesome-Learning4Safe-Contact-rich-tasks.git&label=Visitors&countColor=%2337d67a&style=flat&labelStyle=none)
[![GitHub license](https://img.shields.io/github/license/universea/Awesome-AI-Scientist-Papers)](https://github.com/jack-sherman01/Awesome-Learning4Safe-Contact-rich-tasks/blob/main/LICENSE)

Welcome to the **Awesome-Safe Learning for Contact-Rich Robotic Tasks** repository! This project collecting research papers in area of learning based methods for safe contact-rich robotics tasks since the last 5 years. For more details, please refer to our survey paper : [Safe Learning for Contact-Rich Robot Tasks: A Survey from classical Learning-Based Methods to Safe Foundation Models](https://www.techrxiv.org/doi/full/10.36227/techrxiv.176472870.03980379/v1/) Authers: Heng Zhang, Rui Dai, Gokhan Solak, Pokuang Zhou, Yu She, Arash Ajoudani, in submission to IJRR, 2025. Any contribution is welcome!

This is a comprehensive paper collection of safe learning for contact-rich robotic tasks, aiming to contribute to the robotics and embodied AI communities. The main contributions are as below: 
## Our contribution:
<p style="text-align: justify;">
  <img src="docs/images/trend.jpg" alt="framework">
  <br>

  <br>
  <strong>A Safety-Centric Taxonomy</strong>
  We introduce a structured taxonomy that categorizes safe learning approaches based on key dimensions, including learning phase (exploration vs. execution), level of safety integration (planning, control, or end-to-end), and modalities used (force/torque, vision, etc.). This survey provides a comprehensive lens through which researchers can analyze existing methods and identify safety design trade-offs.
  <br><br>
  <!-- <img src="docs/images/taxonomy.png" alt="taxonomy"> -->
  <br>
  <strong>Contextualization Within Contact-Rich Tasks</strong>
  Beyond general safe learning, we focus on its application to contact-rich robotic tasks such as insertion, polishing, and assembly. We detail how safety constraints are embedded in these tasks, and map the methods used to specific operational challenges (e.g., compliance, contact-inavatiable tasks, collision avoidance, and force control).
  <br><br>
  <img src="docs/images/task.jpg" alt="overview2">
  <br>
  <strong>Identification of Gaps, Challenges, and Future Directions</strong>
  We synthesize open research questions and outline critical challenges such as sim-to-real transfer under safety constraints, the scarcity of standardized benchmarks, and the need for provably safe generalization. We also discuss underexplored directions, including hybrid control-learning frameworks and human-in-the-loop safety mechanisms. Most importantly, we highlight the challenges and future opportunities in integrating safe contact-rich learning with large robotic foundation models, particularly VLM and VLA.
  <br><br>
  <img src="docs/images/vla.png" alt="future">
</p>

## Table of Contents
- [Awesome Safe Learning for Contact-rich Robotic Tasks](#awesome-safe-learning-for-contact-rich-robotic-tasks)
  - [Our contribution:](#our-contribution)
  - [Table of Contents](#table-of-contents)
  - [Surveys](#surveys)
  - [Papers](#papers)
    - [safe learning for contact-rich robotic tasks](#safe-learning-for-contact-rich-robotic-tasks)
    - [Contact-rich tasks](#contact-rich-tasks)
    - [Sensing And Policy Modalities](#sensing-and-policy-modalities)
    - [Data Acquisition](#data-acquisition)
    - [Safety Evaluation Metrics](#safety-evaluation-metrics)
    - [Safety Abstraction Level](#safety-abstraction-level)
    - [Safety Enforcement Spaces](#safety-enforcement-spaces)
  - [Cite](#cite)
  - [License](#license)

## Surveys
- [Progress and prospects of the human–robot collaboration](https://link.springer.com/article/10.1007/s10514-017-9677-2), Arash Ajoudani, Andrea Maria Zanchettin, Serena Ivaldi, Alin Albu-Schäffer, Kazuhiro Kosuge, Oussama Khatib, Autonomous Robots, 2018
- [Trends and challenges in robot manipulation](https://www.science.org/doi/10.1126/science.aat8414), Aude Billard, Danica Kragic, Science, 2019
- [A review of robot learning for manipulation: Challenges, representations, and algorithms](http://jmlr.org/papers/v22/20-1302.html), Oliver Kroemer, Scott Niekum, George Konidaris, Journal of Machine Learning Research, 2021
- [Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning](https://www.annualreviews.org/content/journals/10.1146/annurev-control-042920-020211), Lukas Brunke, Melissa Greeff, Adam W. Hall, Zhaocong Yuan, Siqi Zhou, Jacopo Panerati, Angela P. Schoellig, Annual Review of Control, Robotics, and Autonomous Systems, 2022
- [A survey of robot manipulation in contact](https://www.sciencedirect.com/science/article/pii/S0921889022001312), Markku Suomalainen, Yiannis Karayiannidis, Ville Kyrki, Robotics and Autonomous Systems, 2022
- [Variable impedance control and learning—A review](https://doi.org/10.3389/frobt.2020.590681), Fares J. Abu-Dakka, Matteo Saveriano, Frontiers in Robotics and AI, 2020
- [A review on reinforcement learning for contact-rich robotic manipulation tasks](https://doi.org/10.1016/j.rcim.2023.102517), Iñigo Elguea-Aguinaco, Antonio Serrano-Muñoz, Dimitrios Chrysostomou, Ibai Inziarte-Hidalgo, Simon Bøgh, Nestor Arana-Arexolaleiba, Robotics and Computer-Integrated Manufacturing, 2023
- [Compare contact model-based control and contact model-free learning: A survey of robotic peg-in-hole assembly strategies](https://arxiv.org/abs/1904.05240), Jing Xu, Zhimin Hou, Zhi Liu, Hong Qiao, arXiv, 2019
- [Learning Control Barrier Functions and their application in Reinforcement Learning: A Survey](https://arxiv.org/abs/2404.16879), Maeva Guerrier, Hassan Fouad, Giovanni Beltrame, arXiv, 2024
- [A review of compliant mechanisms for contact robotics applications](https://www.sciencedirect.com/science/article/pii/S0921889024002860), Zahra Samadikhoshkho, Elliot Saive, Michael G. Lipsett, Robotics and Autonomous Systems, 2024
- [A Survey on Imitation Learning for Contact-Rich Tasks in Robotics](https://arxiv.org/abs/2506.13498), Toshiaki Tsuji, Yasuhiro Kato, Gokhan Solak, Heng Zhang, Tadej Petrič, Francesco Nori, Arash Ajoudani, arXiv, 2025
- [A Comprehensive Survey on Physical Risk Control in the Era of Foundation Model-enabled Robotics](https://arxiv.org/abs/2505.12583), Takeshi Kojima et al., arXiv, 2025
- [Alignment and Safety of Diffusion Models via Reinforcement Learning and Reward Modeling: A Survey](https://arxiv.org/abs/2505.17352), Preeti Lamba, Kiran Ravish, Ankita Kushwaha, Pawan Kumar, arXiv, 2025
- [Towards forceful robotic foundation models: a literature survey](https://arxiv.org/abs/2504.11827), William Xie, Nikolaus Correll, arXiv, 2025
- [State-wise safe reinforcement learning: A survey](https://arxiv.org/abs/2302.03122), Weiye Zhao, Tairan He, Rui Chen, Tianhao Wei, Changliu Liu, IJCAI, 2023
- [Shielded Reinforcement Learning: A review of reactive methods for safe learning](https://ieeexplore.ieee.org/abstract/document/10039301), Haritz Odriozola-Olalde, Maider Zamalloa, Nestor Arana-Arexolaleiba, IEEE/SICE SII, 2023
- [A Review of Safe Reinforcement Learning: Methods, Theories and Applications](https://ieeexplore.ieee.org/abstract/document/10675394), Shangding Gu, Long Yang, Yali Du, Guang Chen, Florian Walter, Jun Wang, Alois Knoll, IEEE TPAMI, 2024
- [Reinforcement learning for assembly robots: A review](https://www.proquest.com/docview/2486868134?pq-origsite=gscholar&fromopenview=true&sourcetype=Scholarly%20Journals), Liliana Stan, Adrian Florin Nicolescu, Cristina Pupăză, Proceedings in Manufacturing Systems, 2020 
- [Towards Sustainable Manufacturing: A Review on Innovations in Robotic Assembly and Disassembly](https://ieeexplore.ieee.org/abstract/document/11023241), Adip Ranjan Das, Maria Koskinopoulou, IEEE Access, 2025 
- [Data-Driven Safety Filters: Hamilton–Jacobi Reachability, Control Barrier Functions, and Predictive Methods for Uncertain Systems](https://ieeexplore.ieee.org/abstract/document/10266799), Kim P. Wabersich, Andrew J. Taylor, Jason J. Choi, Koushil Sreenath, Claire J. Tomlin, Aaron D. Ames, Melanie N. Zeilinger, IEEE Control Systems Magazine, 2023
- [Human-like dexterous manipulation for anthropomorphic five-fingered hands: A review](https://www.sciencedirect.com/science/article/pii/S2667379725000038), Yayu Huang, Dongxuan Fan, Haonan Duan, Dashun Yan, Wen Qi, Jia Sun, Qian Liu, Peng Wang, Biomimetic Intelligence and Robotics, 2025 
- [A Review of Advanced Force Torque Control Strategies for Precise Nut-to-Bolt Mating in Robotic Assembly](https://pubs2.ascee.org/index.php/IJRCS/article/view/1604)., Sy Horng Ting Terence, Yeh Huann Goh, Kar Mun Chin, Yan Kai Tan, Tsung Heng Chiew, Ge Ma, Chong Keat How, International Journal of Robotics & Control Systems, 2025
- [Robots in manufacturing: Programming, control, and safety standards](https://www.sciencedirect.com/science/chapter/edited-volume/pii/B9780443138126000117), Srinivasan Lakshminarayanan, Sreekanth Kana, Alberto De San Bernabe, Sri Harsha Turlapati, Dino Accoto, Domenico Campolo, in Digital Manufacturing (Elsevier), 2024

## Papers
### safe learning for contact-rich robotic tasks

<details open>
<summary>Safe Exploration</summary>
This section introduces safe learning before executing the task, highlighting its importance in ensuring reliable and risk-free performance prior to real execution.

- [The Safety Filter: A Unified View of Safety-Critical Control in Autonomous Systems](https://doi.org/10.1146/annurev-control-071723-102940), Hsu et al., Annu. Rev. Control Robot. Auton. Syst., 2024
- [Safety barrier functions and multi-camera tracking for human–robot shared environment](https://doi.org/10.1016/j.robot.2019.103388), Ferraguti et al., Rob. Auton. Syst., 2020
- [Safety and Efficiency in Robotics: The Control Barrier Functions Approach](https://doi.org/10.1109/MRA.2022.3174699), Ferraguti et al., IEEE Robot. Autom. Mag., 2022
- [Safe Navigation and Obstacle Avoidance Using Differentiable Optimization Based Control Barrier Functions](https://arxiv.org/abs/2304.08586), Dai et al., IEEE Robot. Autom. Lett., 2023
- [Robust Control Barrier Functions Using Uncertainty Estimation With Application to Mobile Robots](https://arxiv.org/abs/2401.01881), Das & Burdick, arXiv, 2024
- [Robust Safe Learning and Control in an Unknown Environment: An Uncertainty-Separated Control Barrier Function Approach](https://doi.org/10.1109/LRA.2023.3309130), Li et al., IEEE Robot. Autom. Lett., 2023
- [Safe and Robust Motion Planning for Dynamic Robotics via Control Barrier Functions](https://doi.org/10.1109/CDC45484.2021.9682803), Manjunath & Nguyen, IEEE CDC, 2021
- [Flow shop scheduling with human–robot collaboration: a joint chance-constrained programming approach](https://doi.org/10.1080/00207543.2023.2181025), Wang & Zhang, Int. J. Prod. Res., 2024
- [Probabilistic Collision Checking With Chance Constraints](https://doi.org/10.1109/TRO.2011.2116190), Du Toit & Burdick, IEEE Trans. Robot., 2011
- [Solving Chance-Constrained Stochastic Programs via Sampling and Integer Programming](https://doi.org/10.1287/educ.1080.0048), Ahmed & Shapiro, in *State-of-the-Art Decision-Making Tools in the Information-Intensive Age*, 2008
- [Safe Human–Robot Collaboration With Risk Tunable Control Barrier Functions](https://doi.org/10.1109/TMECH.2025.3572047), Sharma et al., IEEE/ASME Trans. Mechatron., 2025
</details>

<details open>
<summary>Safe Execution</summary>
Safe execution is crucial in contact-rich robotic tasks, as robots must interact not only with complex and uncertain environments but often also in close proximity to humans . This section focuses on learning methods that ensure safety during the execution of contact-rich tasks, addressing challenges such as safe contact, force control, and compliance.

- [Safe robot execution in model-based reinforcement learning](https://ieeexplore.ieee.org/abstract/document/7354232), Martínez et al., IEEE/RSJ IROS, 2015
- [Reinforcement learning on variable impedance controller for high-precision robotic assembly](https://ieeexplore.ieee.org/abstract/document/8793506), Luo et al., IEEE ICRA, 2019
- [Robotic assembly control reconfiguration based on transfer reinforcement learning for objects with different geometric features](http://dx.doi.org/10.1016/j.engappai.2023.107576), Gai et al., Engineering Applications of Artificial Intelligence, 2024
- [Meta reinforcement learning for robust and adaptable robotic assembly tasks](http://dx.doi.org/10.1109/icces54031.2021.9686128), Hafez et al., IEEE ICCES, 2021
- [Reinforcement learning for assembly robots: A review](https://www.proquest.com/docview/2486868134), Stan et al., Proceedings in Manufacturing Systems, 2020
- [Variable impedance skill learning for contact-rich manipulation](https://ieeexplore.ieee.org/abstract/document/9812508), Yang et al., IEEE Robotics and Automation Letters, 2022
- [Impedance learning-based adaptive control for human–robot interaction](https://ieeexplore.ieee.org/abstract/document/9531394), Sharifi et al., IEEE Transactions on Control Systems Technology, 2021
- [Safety compliant control for robotic manipulator with task and input constraints](https://ieeexplore.ieee.org/abstract/document/9802700), Murtaza et al., IEEE Robotics and Automation Letters, 2022
- [Adaptive admittance control for safety-critical physical human robot collaboration](https://doi.org/10.1016/j.ifacol.2023.10.1772), Sun et al., IFAC-PapersOnLine, 2023
- [Adaptive admittance control for physical human-robot interaction based on imitation and reinforcement learning](https://doi.org/10.1109/m2vip58386.2023.10413438), Guo et al., IEEE M2VIP, 2023
- [A perturbation-robust framework for admittance control of robotic systems with high-stiffness contacts and heavy payload](https://doi.org/10.1109/lra.2024.3406055), Samuel et al., IEEE Robotics and Automation Letters, 2024
- [A review of compliant mechanisms for contact robotics applications](https://www.sciencedirect.com/science/article/pii/S0921889024002860), Samadikhoshkho et al., Robotics and Autonomous Systems, 2025
- [Learning for contact-rich tasks with cobots](https://lup.lub.lu.se/student-papers/search/publication/9120389), Cruz-Oliver, Master's thesis, 2024
- [A survey of optimization-based task and motion planning: From classical to learning approaches](https://ieeexplore.ieee.org/abstract/document/10705419), Zhao et al., IEEE/ASME Transactions on Mechatronics, 2024
- [SRL-VIC: A variable stiffness-based safe reinforcement learning for contact-rich robotic tasks](https://ieeexplore.ieee.org/abstract/document/10517382), Zhang et al., IEEE Robotics and Automation Letters, 2024


</details>

<details open>
<summary>Provable Safety Methods</summary>

- [Safe and Optimal Variable Impedance Control via Certified Reinforcement Learning](http://arxiv.org/abs/2511.16330), Kumar et al., arXiv, 2025
- [Data-Driven Safety Filters: Hamilton–Jacobi Reachability, Control Barrier Functions, and Predictive Methods for Uncertain Systems](https://ieeexplore.ieee.org/abstract/document/10266799), Wabersich et al., IEEE Control Systems Magazine, 2023
- [An Actor-Critic Learning Framework Based on Lyapunov Stability for Automatic Assembly](https://link.springer.com/article/10.1007/s10489-022-03844-2), Li et al., Applied Intelligence, 2023
- [Deep Reinforcement Learning-Based Variable Impedance Control for Grinding Workpieces with Complex Geometry](https://www.emerald.com/insight/content/doi/10.1108/RIA-09-2024-0207), Li et al., Robotic Intelligence and Automation, 2025
- [Impedance Learning-Based Adaptive Force Tracking for Robot on Unknown Terrains](https://ieeexplore.ieee.org/document/10842469), Li et al., IEEE Transactions on Robotics, 2025
- [Contact-Aware Safety in Soft Robots Using High-Order Control Barrier and Lyapunov Functions](https://arxiv.org/abs/2505.03841), Wong et al., arXiv, 2025
- [High-Order Control Barrier Functions-Based Impedance Control of a Robotic Manipulator with Time-Varying Output Constraints](https://www.sciencedirect.com/science/article/abs/pii/S0019057822000726), Wang et al., ISA Transactions, 2022

</details>

<details open>
<summary>Safe foundation models</summary>
Foundation Models & General Large Models (e.g., VLMs, VLAs) have shown great potential in robotics, but ensuring their safety in contact-rich tasks remains a significant challenge. This section explores recent advancements in integrating safety mechanisms into foundation models for robotic applications.

**surveys on safe foundation models:**
  
- [Towards safe robot foundation models](https://arxiv.org/abs/2503.07404), Tölle et al., arXiv, 2025
- [Towards forceful robotic foundation models: a literature survey](https://arxiv.org/abs/2504.11827), Xie & Correll, arXiv, 2025
- [A Comprehensive Survey on Physical Risk Control in the Era of Foundation Model-enabled Robotics](https://arxiv.org/abs/2505.12583), Kojima et al., arXiv, 2025
- [Towards embodied agentic AI: Review and classification of LLM-and VLM-driven robot autonomy and interaction](https://arxiv.org/abs/2508.05294), Salimpour et al., arXiv, 2025
  
  
**Recent Safe Foundation Models for Contact-Rich Tasks:**
  
- [SafeVLA: Towards Safety Alignment of Vision-Language-Action Model via Constrained Learning](https://arxiv.org/abs/2503.03480), Zhang et al., arXiv, 2025
- [VTLA: Vision-Tactile-Language-Action Model with Preference Learning for Insertion Manipulation](https://arxiv.org/abs/2505.09577), Zhang et al., arXiv, 2025
- [Audio-VLA: Adding Contact Audio Perception to Vision-Language-Action Model for Robotic Manipulation](https://arxiv.org/abs/2511.09958), Wei et al., arXiv, 2025
- [SAFE: Multitask Failure Detection for Vision-Language-Action Models](https://arxiv.org/abs/2506.09937), Gu et al., arXiv, 2025
- [ImpedanceGPT: VLM-driven Impedance Control of Swarm of Mini-drones for Intelligent Navigation in Dynamic Environment](https://arxiv.org/abs/2503.02723), Batool et al., arXiv, 2025
- [PhysVLM: Enabling Visual Language Models to Understand Robotic Physical Reachability](https://arxiv.org/abs/2503.08481), Zhou et al., arXiv, 2025
- [MLA: A Multisensory Language-Action Model for Multimodal Understanding and Forecasting in Robotic Manipulation](http://arxiv.org/abs/2509.26642), Liu et al., arXiv, 2025


**Language Conditioned / Text-Guided / LLM Agents for Contact-Rich Tasks:**

- [SayCan: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691), Ahn et al., arXiv, 2022
- [RT-2: Vision-Language-Action Model for Robotic Manipulation](https://arxiv.org/abs/2307.15818), Ahn et al., arXiv, 2023
- [SafeAgentBench: A benchmark for safe task planning of embodied LLM agents](https://arxiv.org/abs/2412.13178), Yin et al., arXiv, 2024
- [Text2Interaction: Establishing Safe and Preferable Human-Robot Interaction](https://arxiv.org/abs/2408.06105), Thumm et al., CoRL, 2024
- [CALAMARI: Contact-aware and language conditioned spatial action MApping for contact-RIch manipulation](https://proceedings.mlr.press/v229/wi23a.html), Wi et al., arXiv, 2023
- [Updating Robot Safety Representations Online From Natural Language Feedback](https://arxiv.org/abs/2409.14580), Santos et al., arXiv, 2025
- [Toward Automated Programming for Robotic Assembly Using ChatGPT](https://arxiv.org/abs/2405.08216), Macaluso et al., arXiv, 2024
- [Learning a High-Quality Robotic Wiping Policy Using Systematic Reward Analysis and Visual-Language Model Based Curriculum](https://arxiv.org/abs/2502.12599), Liu et al., arXiv, 2025
- [OmniVIC: A Self-Improving Variable Impedance Controller with Vision-Language In-Context Learning for Safe Robotic Manipulation](https://arxiv.org/abs/2510.17150), Zhang et al., arXiv, 2025
- [Text to Robotic Assembly of Multi Component Objects using 3D Generative AI and Vision Language Models](https://arxiv.org/abs/2511.02162), Alexander Htet Kyaw et al., arXiv, 2025

</details>

### Contact-rich tasks

<details open>
<summary>Assembly and Insertion</summary>
</details>

<details open>
<summary>Surface Interaction</summary>

- [CHEQ-ing the Box: Safe Variable Impedance Learning for Robotic Polishing](https://arxiv.org/abs/2501.07985), Cramer et al., arXiv, 2025
- [Deep reinforcement learning-based variable impedance control for grinding workpieces with complex geometry](https://www.emerald.com/insight/content/doi/10.1108/RIA-09-2024-0207), Li et al., Robotic Intelligence and Automation, 2024
- [A Contact Model based on Denoising Diffusion to Learn Variable Impedance Control for Contact-rich Manipulation](https://arxiv.org/abs/2403.13221), Okada et al., arXiv, 2024
- [Adaptive Compliance Policy: Learning Approximate Compliance for Diffusion Guided Control](https://ieeexplore.ieee.org/abstract/document/11128452), Hou et al., IEEE International Conference on Robotics and Automation (ICRA), 2025
- [Learning Diffusion Policies from Demonstrations For Compliant Contact-rich Manipulation](https://arxiv.org/abs/2410.19235), Aburub et al., arXiv (preprint), 2024
- [Safe contact-based robot active search using Bayesian optimization and control barrier functions](https://www.frontiersin.org/articles/10.3389/frobt.2024.1344367), Vinter-Hviid et al., Frontiers in Robotics and AI, 2024 
- [A Passivity-Based Variable Impedance Controller for Incremental Learning of Periodic Interactive Tasks](https://arxiv.org/abs/2408.10580), Dalle-Vedove et al., arXiv (preprint), 2024
- [Adaptive Neural Network Force Tracking Control of Flexible Joint Robot With an Uncertain Environment](https://ieeexplore.ieee.org/abstract/document/10173753/), Xinbo et al., IEEE Transactions on Industrial Electronics, 2024 
- [Impedance control and parameter optimization of surface polishing robot based on reinforcement learning](https://journals.sagepub.com/doi/abs/10.1177/09544054221100004), Ding et al., Journal of Engineering Manufacture, 2022
- [A Contact-Safe Reinforcement Learning Framework for Contact-Rich Robot Manipulation](https://ieeexplore.ieee.org/abstract/document/9981185/), Zhu et al., IROS, 2022
- [Online Optimization Method of Controller Parameters for Robot Constant Force Grinding Based on Deep Reinforcement Learning Rainbow](https://link.springer.com/article/10.1007/s10846-022-01688-z), Zhang et al., Journal of Intelligent & Robotic Systems, 2022 
- [Uncertainty-Aware Contact-Safe Model-Based Reinforcement Learning](https://ieeexplore.ieee.org/abstract/document/9376242), Kuo et al., IEEE Robotics and Automation Letters, 2021
- [Safe Online Gain Optimization for Cartesian Space Variable Impedance Control](https://ieeexplore.ieee.org/abstract/document/9926697), Wang et al., IEEE CASE, 2022
- [Model-Free Adaptive Impedance Control for Autonomous Robotic Sanding](https://ieeexplore.ieee.org/abstract/document/9618655), Huo et al., IEEE TASE, 2021
- [Variable Impedance Control in End-Effector Space: An Action Space for Reinforcement Learning in Contact-Rich Tasks](https://ieeexplore.ieee.org/abstract/document/8968201), Martín-Martín et al., IEEE/RSJ IROS, 2019





</details>

<details open>
<summary>Object Manipulation</summary>
</details>

<details open>
<summary>Physical HRI</summary>

- [A Learning Control Strategy for Robot-assisted Bathing via Impedance Sliding Mode Technique With Non-repetitive Tasks](https://link.springer.com/article/10.1007/s12555-022-0436-6), Xu et al., International Journal of Control, Automation and Systems, 2024
- [Force-Constrained Visual Policy: Safe Robot-Assisted Dressing via Multi-Modal Sensing](https://ieeexplore.ieee.org/abstract/document/10465608/), Sun et al., IEEE Robotics and Automation Letters, 2024
- [Task-oriented safety field for robot control in human-robot collaborative assembly based on residual learning](https://www.sciencedirect.com/science/article/pii/S095741742302448X), Zhu et al., Expert Systems with Applications, 2024
- [Impedance learning for human-guided robots in contact with unknown environments](https://ieeexplore.ieee.org/abstract/document/10160165/), Xing et al., IEEE Transactions on Robotics, 2023
- Study on force control for robot massage with a model-based reinforcement learning algorithm
, Xiao et al., Intelligent Service Robotics, 2023
- [Research on Robot Massage Force Control Based on Residual Reinforcement Learning](https://ieeexplore.ieee.org/abstract/document/10374025/), Xiao et al., IEEE Access, 2024
- [Impedance Learning-Based Adaptive Control for Human–Robot Interaction](https://ieeexplore.ieee.org/abstract/document/9531394), Sharifi et al., IEEE Transactions on Control Systems Technology, 2021
- [Learning Variable Impedance Control for Robotic Massage With Deep Reinforcement Learning: A Novel Learning Framework](https://ieeexplore.ieee.org/abstract/document/10385222/), Li et al., IEEE Systems, Man, and Cybernetics Magazine, 2024
- [Text2Interaction: Establishing Safe and Preferable Human-Robot Interaction](https://arxiv.org/abs/2408.06105), Thumm et al., Conference on Robot Learning (CoRL), 2024
- [The path towards contact-based physical human–robot interaction](https://www.sciencedirect.com/science/article/pii/S0921889024002136), Farajtabar et al., Robotics and Autonomous Systems, 2024
- [A human-centered safe robot reinforcement learning framework with interactive behaviors](https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2023.1280341), Gu et al., Frontiers in Neurorobotics, 2023
- [Q-Learning-based model predictive variable impedance control for physical human-robot collaboration](https://www.sciencedirect.com/science/article/pii/S0004370222001114), Roveda et al., Artificial Intelligence, 2022 
- [Adaptive Safety-Critical Control With Uncertainty Estimation for Human–Robot Collaboration](https://ieeexplore.ieee.org/abstract/document/10281398), Zhang et al., IEEE TASE, 2023
- [Model-Based Actor-Critic Learning of Robotic Impedance Control in Complex Interactive Environment](https://ieeexplore.ieee.org/abstract/document/9652099), Zhao et al., IEEE Transactions on Industrial Electronics, 2021
- [Assistive Gym: A Physics Simulation Framework for Assistive Robotics](https://ieeexplore.ieee.org/abstract/document/9197411), Erickson et al., IEEE International Conference on Robotics and Automation (ICRA), 2020


</details>

<details open>
<summary>Other tasks</summary>
</details>

### Sensing And Policy Modalities

<details open>
<summary>Pose and Proprioceptive</summary> 

- [Safe data-driven model predictive control of systems with complex dynamics](https://ieeexplore.ieee.org/document/10113472), Mitsioni et al., IEEE Transactions on Robotics, 2023
- [Robotic imitation of human assembly skills using hybrid trajectory and force learning](https://ieeexplore.ieee.org/abstract/document/9561619?casa_token=VZzClSLo7QQAAAAA:tFOqQs205sGzNHtY1jXleAmQt5SWFz0AO8oDw2RM5EmaSZ_DvmGsLFlC8S3a5cP1yjeiXUDH4WTuFA), Wang et al., IEEE International Conference on Robotics and Automation (ICRA), 2021
- [Should We Learn Contact-Rich Manipulation Policies From Sampling-Based Planners?](https://ieeexplore.ieee.org/abstract/document/10977833?casa_token=BOv75ETm9EgAAAAA:z9ua-iCXwUimmjC_S-RUx4uG8TcfpN_jCOagosS49cckeyPCUIU_r6PE4pUet4pAVgPuq_tMJcjTSA), Zhu et al., IEEE Robotics and Automation Letters, 2025
- [Diffusion forcing: Next-token prediction meets full-sequence diffusion](https://proceedings.neurips.cc/paper_files/paper/2024/hash/2aee1c4159e48407d68fe16ae8e6e49e-Abstract-Conference.html), Chen et al., Advances in Neural Information Processing Systems, 2024
- [Handling long-term safety and uncertainty in safe reinforcement learning](https://arxiv.org/abs/2409.12045), G{\"u}nster et al., arXiv preprint, 2024
- [SCAPE: Learning stiffness control from augmented position control experiences](https://proceedings.mlr.press/v164/kim22b.html), Kim et al., Conference on Robot Learning, 2022
- [Neural networks enhanced optimal admittance control of robot--environment interaction using reinforcement learning](https://ieeexplore.ieee.org/abstract/document/9367005?casa_token=uq_y7aP0sI4AAAAA:blR0GY2c76YPDGr6GMZ7eDqatesmz4X-6ezHUikdFumVSqoeDVZfcegEd7sciBBc2wbSYzCKxigmIA), Peng et al., IEEE Transactions on Neural Networks and Learning Systems, 2021
- [Learning force control for contact-rich manipulation tasks with rigid position-controlled robots](https://ieeexplore.ieee.org/abstract/document/9145608?casa_token=UKUO75P5Ud4AAAAA:gh4YHpE1XGaOKpPxRAJaXwkrZOpBUUxb6jmM38bZe6W4p7knRhQfhQhqKcYYZGUhlbcVUv41pHgxgQ), Beltran-Hernandez et al., IEEE Robotics and Automation Letters, 2020
- [Motion planner augmented reinforcement learning for robot manipulation in obstructed environments](https://proceedings.mlr.press/v155/yamada21a.html), Yamada et al., Conference on Robot Learning, 2021
- [End-to-end reinforcement learning for torque based variable height hopping](https://ieeexplore.ieee.org/abstract/document/10342187?casa_token=oOchBnxAQ8AAAAAA:m_Rlv7MTB1ZxfPVm15f5ljuUGa_sDlYdEZDJ7eutFT1E6JNoxumh1XmsWEplKtUT97o1btqLewZcQQ), Soni et al., 2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2023
- [Safety Augmented Value Estimation From Demonstrations (SAVED): Safe Deep Model-Based RL for Sparse Cost Robotic Tasks](https://ieeexplore.ieee.org/abstract/document/9013084?casa_token=WSWdeVqrTNUAAAAA:tnNqXxA8tX575vTqrlcxzG-y8EE3AT31VQw04DV3AfVorCWF5TCdBZ6IeF0m-15Hhuo1VeVjkPV7Iw), Thananjeyan et al., IEEE Robotics and Automation Letters, 2020
</details>

<details open>
<summary>Force and Torque sensing</summary>
</details>

<details open>
<summary>Vision Sensing</summary>
</details>

<details open>
<summary>Tactile Sensing</summary>
</details>

### Data Acquisition

<details open>
<summary>Simulation-Based Data Generation </summary>

- [Assistive Gym: A Physics Simulation Framework for Assistive Robotics](https://ieeexplore.ieee.org/abstract/document/9197411), Erickson et al., IEEE International Conference on Robotics and Automation (ICRA), 2020

</details>

<details open>
<summary>Real-World Data Collection</summary>
</details>

<details open>
<summary>Hybrid Data Approaches</summary>
</details>
<!-- ## Simulation
## Benchmark -->

### Safety Evaluation Metrics

<details open>
<summary>Safety, Efficiency and Task Objectives </summary>


</details>

<details open>
<summary>Trade-off Between Objectives</summary>
</details>

<details open>
<summary>improved Evaluation</summary>
</details>

### Safety Abstraction Level

<details open>
<summary>High-Level Safety Constraints</summary>
</details>

<details open>
<summary>Low-Level Safety Implementations</summary>
</details>

<details open>
<summary>End-to-End Safety Enhancement</summary>
</details>

<details open>
<summary>Hybrid Safety Approaches</summary>
</details>

### Safety Enforcement Spaces

<details open>
<summary>Task Space</summary>
</details>

<details open>
<summary>Joint Space </summary>
</details>

<details open>
<summary>Dual-Space Safety Enforcement </summary>
</details>

<details open>
<summary>Policy Spaces</summary>
</details>

## Cite
```
bibtex
@article{Zhang_2025,
   title={Safe Learning for Contact-Rich Robot Tasks: A Survey From Classical Learning-Based Methods to Safe Foundation Models},
   author={Zhang, Heng and Dai, Rui and Solak, Gokhan and Zhou, Pokuang and She, Yu and Ajoudani, Arash},
   url={http://arxiv.org/abs/2512.11908},
   journal={arXiv preprint},
   year={2025} }
```
## License
MIT
