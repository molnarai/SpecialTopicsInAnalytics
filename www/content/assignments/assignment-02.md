+++
date = '2025-01-06T18:20:46-05:00'
due_date = "2025-11-12"
draft = false
title = 'Computer Vision Project'
weight = 20
status = 'Posted'
+++
# **Computer Vision Programming Project: Urban Traffic Sign Recognition and Analysis System**

## **Project Overview**

This programming project challenges to develop a comprehensive computer vision system for analyzing urban traffic signs from real-world street scene imagery. Students will apply classical computer vision techniques, feature extraction methods, traditional machine learning classifiers, and modern deep learning approaches to build a robust traffic sign detection and recognition pipeline. The project uses the [**Mapillary Traffic Sign Dataset**](https://labelbox.com/datasets/mapillary-traffic-sign-dataset/) (https://www.mapillary.com/dataset/trafficsign) , which contains over 100,000 high-resolution images from diverse global locations with varying weather conditions, lighting, viewpoints, and camera sensors—making it an ideal testbed for advanced computer vision methods.



## **Dataset Description**

**Mapillary Traffic Sign Dataset** specifications:

- **Size**: 100,000+ high-resolution street scene images
- **Annotations**: 320,000+ labeled traffic signs with bounding boxes
- **Classes**: 300+ distinct traffic sign categories (students will focus on subset)
- **Diversity**: Global coverage with images from multiple countries, weather conditions, times of day, and camera types
- **Annotation quality**: Fully annotated bounding boxes with class labels
- **Access**: Publicly available for academic use

The image dataset is available on ARC in `/data/project/MSA8395/mapillary_traffic_sign_dataset`


## **Project Requirements**

### **Phase 1: Dataset Preparation, Preprocessing \& Region Proposal**

**Timeline: Week 1**

#### **Part A: Dataset Curation and Exploration**

1. **Dataset Sampling**: From the full Mapillary dataset, create a focused subset:
    - Identify the 20-30 most frequent traffic sign classes
    - Extract 10,000-15,000 images containing these signs
    - Ensure balanced class distribution (or document imbalance strategy)
    - Split data: 70% training, 15% validation, 15% test
2. **Exploratory Analysis**:
    - Analyze class distributions and sign size variations
    - Visualize sample images showing different conditions (weather, lighting, occlusion)
    - Document challenges: scale variation, multiple signs per image, background complexity
    - Examine bounding box annotations and prepare ground truth data

**Deliverable**: Dataset preparation script and exploratory analysis notebook with visualizations.

#### **Part B: Preprocessing Pipeline**

1. **Color Space Analysis**: Convert images to RGB, HSV, and Lab color spaces. Analyze which color space best isolates traffic signs from complex urban backgrounds (sky, buildings, vegetation).
2. **Image Enhancement**:
    - Implement adaptive histogram equalization (CLAHE) for lighting normalization
    - Apply bilateral filtering for noise reduction while preserving edges
    - Test preprocessing on challenging images (nighttime, shadows, rain)
3. **Sign Region Extraction**: Use bounding box annotations to extract sign regions. Implement padding strategy to include context around signs.
4. **Standardization**: Resize extracted signs to uniform dimensions (e.g., 64x64 or 128x128 pixels) while maintaining aspect ratio considerations.

**Deliverable**: Preprocessing pipeline that outputs enhanced, standardized sign images.

#### **Part C: Classical Region Proposal**

Develop a classical computer vision pipeline to detect sign candidates **without using ground truth bounding boxes**:

1. **Color-Based Detection**:
    - Use HSV color space to detect red, blue, and yellow regions (common sign colors)
    - Apply morphological operations (opening, closing) to clean detections
    - Generate candidate regions using connected components
2. **Edge and Shape Detection**:
    - Apply Canny edge detection to find sign boundaries
    - Use Hough Circle Transform to detect circular signs
    - Use Hough Line Transform to detect rectangular/triangular sign boundaries
    - Combine edge and shape information to propose sign candidates
3. **Region Filtering**:
    - Filter candidates by size, aspect ratio, and location
    - Score candidates based on edge strength and color consistency
    - Implement Non-Maximum Suppression to eliminate overlapping proposals
4. **Evaluation**: Compare proposed regions against ground truth using Intersection over Union (IoU). Calculate precision, recall, and F1-score for region proposal at IoU thresholds of 0.3, 0.5, and 0.7.

**Deliverable**: Region proposal module with evaluation metrics showing detection performance before classification.

***

### **Phase 2: Feature Extraction \& Model Development**

**Timeline: Week 2**

#### **Part A: Classical Feature Extraction and ML Classification**

1. **HOG Features**: Extract Histograms of Oriented Gradients from detected sign regions:
    - Experiment with cell sizes (8x8, 16x16) and orientations (9 bins)
    - Visualize HOG representations for different sign classes
    - Document feature vector dimensions
2. **Color Features**:
    - Extract color histograms in HSV space (focus on H and S channels)
    - Compute statistical color features (mean, std for each channel)
    - Combine with HOG for richer representation
3. **ORB Keypoints**: Apply ORB feature detector to extract rotation-invariant descriptors. Create Bag-of-Visual-Words representation using k-means clustering of descriptors.
4. **Feature Combination**: Create comprehensive feature vectors by concatenating HOG, color, and ORB-based features.
5. **Dimensionality Analysis**:
    - Apply PCA and plot cumulative explained variance
    - Use t-SNE to visualize feature spaces in 2D
    - Identify class separability and potential confusion
6. **Classifier Training**:
    - Train **Support Vector Machine** (RBF kernel) with grid search
    - Train **Random Forest** with hyperparameter tuning
    - Evaluate on validation set with confusion matrices and classification reports
    - Identify most challenging class pairs

**Deliverable**: Feature extraction pipeline, trained classical models, and comprehensive evaluation with visualizations.

#### **Part B: Deep Learning Implementation**

1. **Data Preparation**:
    - Create data loaders with augmentation pipeline
    - Implement augmentations: rotation (±20°), translation, scaling, brightness/contrast adjustment, Cutout
    - Ensure validation/test data is not augmented
2. **Transfer Learning Approach**: Fine-tune a pre-trained model for sign classification:
    - Use **EfficientNet-B0** or **MobileNetV2** (efficient for varied input sizes)
    - Replace classification head for your number of classes (20-30)
    - Start with frozen backbone, train classification head
    - Optionally unfreeze and fine-tune entire network
    - Document training strategy and learning rates
3. **Custom CNN Architecture** (optional): Design a custom CNN as comparison:
    - 3-4 convolutional blocks with batch normalization
    - MaxPooling and dropout for regularization
    - Fully connected classification head
4. **Object Detection** (advanced option): Implement **YOLOv5 or YOLOv8** for end-to-end detection and classification:
    - Fine-tune pre-trained YOLO on your subset
    - Train to predict bounding boxes and class labels simultaneously
    - Evaluate using mean Average Precision (mAP)
    - Compare detection results with classical region proposal + classification
5. **Training Protocol**:
    - Track training/validation loss and accuracy curves
    - Implement early stopping and learning rate scheduling
    - Save best model based on validation performance
    - Test on held-out test set

**Deliverable**: Trained deep learning model(s), training history plots, and test set predictions with confidence scores.

***

### **Phase 3: Comparative Analysis \& Final Report**

**Timeline: Week 3**

#### **Comprehensive Evaluation and Analysis**

1. **End-to-End System Comparison**:

Compare **two complete pipelines**:
- **Classical Pipeline**: Color/shape region proposal → HOG+Color features → SVM/RF classification
- **Deep Learning Pipeline**: Transfer learning classification OR YOLO detection (if implemented)

**Metrics to Report**:
- Detection performance: Precision, Recall, F1 at different IoU thresholds
- Classification accuracy, per-class precision/recall
- Combined detection + classification accuracy (correct class in correct location)
- Inference speed (images/second or FPS)
- Model size and memory requirements

**Performance Table**: Create comprehensive comparison showing all metrics across approaches.
2. **Failure Analysis**:
- **Detection Failures**: Analyze missed signs and false positives
    - Categorize by failure mode: occlusion, extreme scale, poor lighting, cluttered background
    - Compare classical vs. deep learning failure patterns
- **Classification Failures**: Examine misclassified signs
    - Identify confused class pairs (visually similar signs)
    - Show examples of challenging cases with model predictions
    - Analyze confidence scores on failures
- **Visualization Gallery**: Create figure showing:
    - Successful detections and classifications
    - Detection failures (missed signs)
    - False positives (non-sign regions detected)
    - Classification errors with predicted vs. true labels
3. **Insights and Recommendations**:

**When Classical Methods Excel**:
- Specific color/shape patterns (high-contrast circular signs)
- Limited training data scenarios
- Interpretable features needed
- Resource-constrained deployment

**When Deep Learning Excels**:
- Complex backgrounds and occlusions
- Weathered or partially visible signs
- Scale and viewpoint variations
- Large labeled datasets available

**Real-World Deployment Scenarios**:
- **Autonomous Vehicles**: Requirements for accuracy, speed, robustness
- **Infrastructure Monitoring**: Municipal sign inventory and maintenance
- **Driver Assistance**: Mobile apps for navigation and safety
- **Accessibility Tools**: Assistive technology for visually impaired users

**Recommendations**: Based on your empirical results, provide guidance on:
- Optimal approach for different deployment constraints
- Data requirements to achieve target accuracy levels
- Strategies for handling your dataset's specific challenges
- Future improvements and research directions

**Deliverable**: Final technical report (10-15 pages) including:

- Executive summary of key findings
- Methodology descriptions for all approaches
- Complete results with tables and visualizations
- Failure analysis with annotated examples
- Critical discussion of tradeoffs and practical considerations
- Conclusions and recommendations with supporting evidence

***

## **Expected Outcomes**

By completing this project, students will produce:

### **Technical Deliverables**

1. **Complete Python Codebase**:
    - Dataset preparation and sampling scripts
    - Preprocessing and enhancement pipeline
    - Classical region proposal implementation
    - Feature extraction module (HOG, color, ORB)
    - Classical ML training and evaluation scripts
    - Deep learning model architecture and training code
    - Evaluation utilities with visualization functions
    - Well-organized, documented, modular code
2. **Trained Models**:
    - Classical models: SVM and Random Forest with engineered features
    - Fine-tuned deep learning model (EfficientNet/MobileNet)
    - Optional: YOLO detector for end-to-end solution
    - Model checkpoints with performance logs
3. **Comprehensive Documentation**:
    - Jupyter notebooks for each project phase
    - Code comments and markdown explanations
    - Hyperparameter choices with justifications
    - Experimental observations and insights
4. **Visual Results**:
    - Dataset exploration visualizations
    - Preprocessing pipeline effects
    - Region proposal results with IoU analysis
    - HOG visualizations and feature space plots (t-SNE, PCA)
    - Confusion matrices for all classifiers
    - Training curves for deep learning
    - Detection and classification result galleries
    - Failure case analysis with annotations
5. **Final Report**: Professional technical document with:
    - Dataset description and curation methodology
    - Detailed methodology for each approach
    - Comprehensive results section with tables and figures
    - Comparative analysis across all methods
    - Failure analysis with examples
    - Discussion of practical implications
    - Conclusions and future work recommendations



## **Grading Rubric**

- **Phase 1 (Data Preparation \& Region Proposal)**: 35%
    - Dataset curation and exploration: 10%
    - Preprocessing pipeline: 10%
    - Classical region proposal and evaluation: 15%
- **Phase 2 (Feature Extraction \& Models)**: 40%
    - Classical features and ML classification: 20%
    - Deep learning implementation and training: 20%
- **Phase 3 (Analysis \& Report)**: 25%
    - End-to-end system comparison: 10%
    - Failure analysis with visualizations: 8%
    - Insights and recommendations: 7%
- **Code Quality \& Documentation**: 10%
    - Code organization and modularity
    - Documentation clarity and completeness
    - Reproducibility with clear instructions
- **Bonus (up to 10%)**:
    - YOLO implementation for end-to-end detection
    - Ensemble methods combining approaches
    - Novel optimizations or techniques
    - Exceptional visualizations and analysis depth
    - Testing on additional challenging scenarios


## **Resources and Tools**

**Required Python Libraries**:

- **OpenCV** (`cv2`): Core image processing and computer vision
- **scikit-image** (`skimage`): Advanced image processing algorithms
- **scikit-learn** (`sklearn`): Classical ML, metrics, dimensionality reduction
- **NumPy/Pandas**: Numerical operations and data management
- **Matplotlib/Seaborn**: Visualization and plotting
- **TensorFlow or PyTorch**: Deep learning framework
- **Albumentations**: Advanced image augmentation
- **Ultralytics** (optional): For YOLO implementation

**Computing Resources**:

- **GPU Access**: Google Colab Pro or university GPU cluster recommended
- **RAM**: Minimum 16GB for handling high-resolution images
- **Storage**: 50-100GB for full dataset (10-20GB for subset)

**Dataset Access**:

- **Mapillary Traffic Sign Dataset**: Available from Mapillary research page <https://labelbox.com/datasets/mapillary-traffic-sign-dataset/> or <https://www.mapillary.com/dataset/trafficsign>
- The image dataset is available on ARC in `/data/project/MSA8395/mapillary_traffic_sign_dataset`



<!-- ## **Timeline and Milestones**

**Week 1: Data Preparation and Classical Computer Vision**

- **Days 1-2**: Dataset download, subset creation, exploratory analysis
- **Days 3-4**: Preprocessing pipeline development and testing
- **Days 5-7**: Classical region proposal implementation and evaluation
- **Milestone**: Submit notebook with dataset analysis, preprocessing pipeline, and region proposal results

**Week 2: Feature Engineering and Model Development**

- **Days 1-3**: Feature extraction (HOG, color, ORB) and classical ML training
- **Days 4-5**: Deep learning model setup and initial training
- **Days 6-7**: Model optimization and evaluation on test set
- **Milestone**: Submit trained models with evaluation metrics and confusion matrices

**Week 3: Integration, Analysis, and Reporting**

- **Days 1-2**: End-to-end pipeline integration and performance comparison
- **Days 3-4**: Failure analysis and visualization creation
- **Days 5-7**: Final report writing with insights and recommendations
- **Milestone**: Submit complete project: code repository, trained models, final report -->


## **Submission Requirements**

1. **Code Repository**: Organized directory structure:
- Create a Project on The GitLab server https:git.insight.gsu.edu
- Add the instructor to your project (as developer)
- Continuously update the repo as your work on your project


```
project/
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_preprocessing_region_proposal.ipynb
│   ├── 03_classical_ml.ipynb
│   ├── 04_deep_learning.ipynb
│   └── 05_analysis.ipynb
├── src/
│   ├── preprocessing.py
│   ├── region_proposal.py
│   ├── features.py
│   ├── models.py
│   └── evaluation.py
├── models/
│   ├── svm_model.pkl
│   ├── rf_model.pkl
│   └── deep_model.pth
├── results/
│   ├── figures/
│   └── metrics/
├── README.md
└── requirements.txt
```

2. **Final Report**: PDF document with:
    - Abstract/Executive Summary
    - Introduction and dataset description
    - Methodology sections for each approach
    - Results with comprehensive tables and figures
    - Comparative analysis and discussion
    - Failure analysis with examples
    - Conclusions and recommendations
    - References
3. **README**: Clear instructions for:
    - Environment setup and dependencies
    - Dataset download and preparation
    - Running each phase of the project
    - Reproducing reported results
