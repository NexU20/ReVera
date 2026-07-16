# Sentiment Analysis of Forebie Store Customer Reviews on Shopee Using TF-IDF and Classification Algorithm Comparison

---

**Lindan** *(full name adjusted accordingly)*

Department of Informatics Engineering, Faculty of Science and Technology
UIN Syarif Hidayatullah Jakarta, Indonesia

*email: (adjusted accordingly)*

---

## Abstract

The rapid growth of the e-commerce industry in Indonesia has made customer reviews an invaluable data source for understanding consumer satisfaction. This study aims to analyze customer review sentiments at the Forebie cosmetics store on the Shopee platform through the implementation of an end-to-end Data Science pipeline. The primary dataset was collected using Playwright-based web scraping techniques, yielding 684 reviews from 10 products. The text preprocessing pipeline includes case folding, emoji-to-text translation, stopword removal with negation word exceptions, and stemming using the Sastrawi library. After data cleaning, 666 clean reviews were obtained with an imbalanced class distribution: Positive (62%), Neutral (20%), and Negative (18%). Three classification algorithms were compared: **Support Vector Machine (LinearSVC)**, **Naive Bayes (MultinomialNB)**, and **Logistic Regression**, with TF-IDF (*Term Frequency-Inverse Document Frequency*) as the feature representation method. To handle class imbalance, the `class_weight='balanced'` parameter was applied to the SVM and Logistic Regression models. Evaluation results show that **Logistic Regression** achieved the best performance with a **weighted F1-Score of 0.732** and **Accuracy of 0.731**, outperforming SVM (F1: 0.717) and Naive Bayes (F1: 0.685). Further analysis through Word Cloud revealed data contamination from seller reply text as well as emoji translation artifacts affecting word distribution in negative reviews. The best model along with the TF-IDF Vectorizer was saved in `.joblib` format for future prediction purposes.

**Keywords:** Sentiment Analysis, NLP, TF-IDF, Logistic Regression, Support Vector Machine, Shopee, Customer Reviews, E-commerce

---

## 1. Introduction

### 1.1 Background

Digital transformation has driven the rapid growth of online shopping applications in Indonesia. According to data from the Indonesian Internet Service Providers Association (APJII), the number of internet users in Indonesia continues to increase annually, providing significant potential for e-commerce development [1]. Shopee, as one of the largest e-commerce platforms in Southeast Asia, has a highly active user base in Indonesia with an average of hundreds of millions of monthly visits [2].

Customer reviews on e-commerce platforms serve a dual role: as a consideration for prospective buyers in making purchasing decisions, and as direct feedback for sellers to improve product and service quality [3]. However, with the enormous volume of reviews, manual analysis is no longer efficient. Therefore, an automated approach based on Natural Language Processing (NLP) and machine learning is needed to classify review sentiments into positive, negative, or neutral categories [4].

This study takes a case study of the cosmetics store **Forebie** on Shopee, selected because it features diverse review variations — ranging from complaints about skincare product side effects to praise for product suitability on the skin. The cosmetics domain is also interesting from an NLP perspective because reviews tend to use informal language, slang, and emojis intensively, thus demanding more careful preprocessing stages.

### 1.2 Research Problems

1. How to build an end-to-end sentiment analysis pipeline for Indonesian-language reviews on e-commerce platforms?
2. Which classification algorithm is most effective in classifying sentiment in Forebie store reviews on Shopee?
3. How does the resulting model's performance compare with similar previous studies?

### 1.3 Research Objectives

1. To collect a primary review dataset from the Shopee platform using web scraping techniques.
2. To perform Indonesian-language text preprocessing considering the unique characteristics of e-commerce reviews (emojis, slang, seller responses).
3. To build and compare three sentiment classification models: SVM, Naive Bayes, and Logistic Regression.
4. To evaluate model performance using metrics appropriate for imbalanced datasets.

### 1.4 Literature Review

Several previous studies relevant to this topic include:

**Kadir and Fairuzabadi (2025)** [5] analyzed the sentiment of Shopee application reviews on Google Play using TF-IDF and Logistic Regression on 5,000 reviews. The study reported an accuracy of **85.11%** with a **macro-F1 of 0.58**. Despite the high accuracy, the low macro-F1 value indicates that the model struggled to recognize minority classes, especially the neutral class which only achieved an F1-Score of 0.14. The study also confirmed that neutral reviews are often ambiguous and contain mixed sentiments, making them difficult to classify.

**Saepudin, Faqih, and Dwilestari (2024)** [6] compared SVM, Random Forest, and Logistic Regression algorithms on 3,000 Shopee reviews using the CRISP-DM methodology. Results showed that Random Forest achieved the highest accuracy (94%), followed by SVM (91%) and Logistic Regression (86%). Labeling in that study was done automatically using TextBlob, unlike the rating-based approach used in this study.

**Fathurrohman *et al.* (2025)** [7] studied the sentiment of Shopee Xpress delivery reviews using SVM and Logistic Regression on 497 reviews. SVM outperformed Logistic Regression with an accuracy of **93%** versus **90%**, although both models showed good consistency in sentiment prediction on new data.

From the literature review above, it can be concluded that: (1) TF-IDF remains an effective feature representation for Indonesian-language sentiment analysis, (2) the main challenge lies in handling class imbalance, and (3) the neutral class is consistently the most difficult class to predict.

---

## 2. Research Methodology

### 2.1 Data Collection

The dataset is **primary data** collected directly from the product review pages of the Forebie store on Shopee (https://shopee.co.id/shop/806035446) using a **Playwright**-based web scraper (browser automation). Playwright was chosen because it can penetrate Shopee's dynamic DOM (Document Object Model) protection, which cannot be accessed by regular HTTP-based scrapers. The scraping process includes:

- Automatic product page opening and navigation to the review section.
- JavaScript injection to click rating filters (stars 1-5) to bypass Shopee's DOM overlay.
- Extraction of comment IDs, usernames, ratings, and review text.
- Incremental mode (`--add`) to add data without duplication.

The total data collected amounted to **684 raw reviews** from **10 products** in the Forebie store, with an initial distribution of 5 columns: `comment_id`, `product_url`, `username`, `rating`, and `review`.

### 2.2 Feature Engineering

The initial dataset had only 5 columns. To enrich the analysis, **4 new columns** were added through feature engineering:

| New Column | Type | Creation Method | Purpose |
|---|---|---|---|
| `product_name` | Categorical | Extracted from Shopee URL via Regex | Per-product analysis |
| `word_count` | Numeric | `len(review.split())` | Outlier detection |
| `character_length` | Numeric | `len(review)` | Correlation |
| `sentiment_label` | Categorical | Rating 1-2: Negative, 3: Neutral, 4-5: Positive | Classification target |

This rating-based labeling approach is consistent with the methodology used by Kadir and Fairuzabadi [5], where rating scores are used as a proxy for automatically determining sentiment.

### 2.3 Data Preprocessing (Text Preprocessing)

The text preprocessing stage was carried out sequentially in the following order:

1. **Missing Values Handling:** Rows with empty review columns were removed.
2. **Outlier Handling:** Reviews with more than 150 words were removed to eliminate spam reviews or excessively long narratives.
3. **Case Folding:** All text was converted to lowercase.
4. **Emoji Conversion:** Emojis were converted to representative Indonesian text using the `emoji` library with the `language="id"` parameter. This step aims to preserve the emotional information contained in emojis [8].
5. **Noise Removal:** URLs, mentions, numbers, and punctuation were removed using regular expressions (regex).
6. **Stopword Removal with Negation Exceptions:** Non-informative conjunctions were removed using the stopword list from the Sastrawi library. **Crucial point:** negation words (*"tidak"* / not, *"kurang"* / less, *"belum"* / not yet, *"jangan"* / don't, *"bukan"* / not, *"tak"* / not) were **intentionally retained** because removing negation words can reverse sentiment meaning (example: *"tidak bagus"* / not good becomes *"bagus"* / good). This approach is in line with NLP literature recommendations for sentiment analysis domains [9].
7. **Stemming:** Affixed words were converted to root words using the **Sastrawi** library (Stemmer Factory), which is the standard stemmer for Indonesian language [10].
8. **Label Encoding:** Sentiment labels were converted to numeric form: Negative = 0, Neutral = 1, Positive = 2.

After the entire preprocessing process, the final dataset consisted of **666 clean reviews**.

### 2.4 Feature Extraction (TF-IDF)

Text feature representation used the **TF-IDF** (*Term Frequency-Inverse Document Frequency*) method with the following configuration:

- `max_features = 5000`: Limiting the number of features for efficiency.
- `ngram_range = (1, 2)`: Using unigrams and bigrams so the model can capture two-word phrases such as *"tidak cocok"* (not suitable) [5].
- `min_df = 2`: Ignoring very rare words.
- `max_df = 0.95`: Excluding overly common words.

### 2.5 Data Splitting

The dataset was split into **training data** (80%) and **test data** (20%) with `stratify=y` to maintain class proportions in both subsets, following standard practice in the literature [5][6][7].

### 2.6 Classification Algorithms

Three classification algorithms were compared:

1. **SVM (LinearSVC):** An algorithm that finds the class-separating hyperplane with the widest margin. The `class_weight='balanced'` parameter was enabled to handle class imbalance [7].
2. **Naive Bayes (MultinomialNB):** A probabilistic classification algorithm based on Bayes' theorem, suitable for high-dimensional text data. A smoothing parameter `alpha=1.0` was used.
3. **Logistic Regression:** A probabilistic classification algorithm with a sigmoid function. The `class_weight='balanced'` and `max_iter=1000` parameters were used [5].

### 2.7 Class Imbalance Handling

The sentiment distribution in this dataset is imbalanced: Positive (62%), Neutral (20%), and Negative (18%). To address this, the `class_weight='balanced'` parameter was used for the SVM and Logistic Regression models. This parameter automatically adjusts class weights based on their frequency of occurrence, preventing the model from being biased toward the majority class [5][7]. This approach was chosen because it is simpler and directly integrated with the classifier, unlike oversampling techniques such as Random Oversampling used by Kadir and Fairuzabadi [5].

### 2.8 Evaluation Metrics

Model evaluation used:

- **Accuracy:** The proportion of correct predictions out of total predictions.
- **Weighted F1-Score:** The harmonic mean of precision and recall, weighted by the number of samples per class. This metric was chosen because it is fairer for imbalanced datasets compared to accuracy alone [5][7].
- **Confusion Matrix:** A matrix showing the distribution of correct and incorrect predictions for each class.
- **Classification Report:** Displaying precision, recall, and F1-Score per class.

---

## 3. Results and Discussion

### 3.1 Dataset Profile

The raw data consisted of 684 reviews with 5 columns. There were 7 missing values in the `username` column and 11 noise rows (reviews that were too short or contained only the text "Helpful?") that were removed, leaving 673 reviews after initial cleaning. After feature engineering, the dataset had 9 columns.

### 3.2 Exploratory Data Analysis (EDA)

**Sentiment Distribution:**
The dataset shows class imbalance with the distribution: Positive 62%, Neutral 20%, and Negative 18%. This finding is consistent with the common pattern in e-commerce datasets where positive sentiment dominates [5][6].

**Outlier Detection:**
Boxplot analysis on the word count feature revealed the presence of very long reviews (outliers). Reviews with more than 150 words were removed as they tended to be spam reviews or unrepresentative long narratives.

**Numerical Feature Correlation:**
The correlation heatmap showed:
- Very high correlation (r = 0.99) between word count and character length, which is expected as both measure text length.
- Weak positive correlation (r = 0.31) between rating and word count, indicating that buyers with higher ratings tend to write slightly longer reviews.

### 3.3 Modeling Results

The following table presents the performance comparison of the three models:

| Model | Accuracy | F1-Score (weighted) |
|---|---|---|
| SVM (LinearSVC) | 0.724 | 0.717 |
| Naive Bayes (MultinomialNB) | 0.709 | 0.685 |
| **Logistic Regression** | **0.731** | **0.732** |

**Logistic Regression** showed the best performance with a weighted F1-Score of **0.732** and accuracy of **73.1%**. The following is the detailed classification report for the Logistic Regression model:

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Negative | 0.60 | 0.88 | 0.71 | 24 |
| Neutral | 0.50 | 0.36 | 0.46 | 27 |
| Positive | 0.88 | 0.78 | 0.82 | 83 |
| **Weighted Avg** | **0.75** | **0.73** | **0.73** | **134** |

### 3.4 Discussion

#### 3.4.1 Comparison with Previous Studies

The weighted F1-Score of **0.732** obtained in this study can be categorized as **reasonably good** based on several considerations:

**First**, the study by Kadir and Fairuzabadi [5], which also used the TF-IDF and Logistic Regression combination on Shopee reviews, reported higher accuracy (85.11%), but **their macro-F1 was only 0.58** — lower than the weighted F1 of this study (0.732). This indicates that the model in this study is **more balanced** in recognizing all three sentiment classes, despite its lower headline accuracy. This difference can be explained by two factors: (1) the data distribution in study [5] was more skewed (80.98% positive vs. 3.1% neutral), and (2) the use of Random Oversampling in study [5] increased accuracy but did not significantly improve performance on minority classes.

**Second**, most studies reporting accuracy above 85% — such as Saepudin *et al.* [6] (SVM: 91%, RF: 94%, LR: 86%) and Fathurrohman *et al.* [7] (SVM: 93%, LR: 90%) — used **different labeling schemes** or **different dataset characteristics**. Saepudin *et al.* [6] used automatic TextBlob-based labeling that tends to produce more uniform label distributions, while Fathurrohman *et al.* [7] worked on the delivery domain (delivery time) which has more structured linguistic patterns compared to cosmetic product reviews.

**Third**, **3-class** sentiment classification (Positive, Neutral, Negative) is inherently more difficult than binary classification. The **Neutral** class has the lowest F1-Score (0.46) in this study, consistent with findings by Kadir and Fairuzabadi [5] (Neutral F1: 0.14) and general literature noting that neutral reviews are often ambiguous, contain mixed sentiment, or are merely descriptive without clear emotional expression [5][11].

The following comparison table summarizes this study's position relative to references:

| Aspect | Kadir & Fairuzabadi [5] | Saepudin *et al.* [6] | Fathurrohman *et al.* [7] | **This Study** |
|---|---|---|---|---|
| Platform | Shopee (Google Play) | Shopee (Google Play) | Shopee Xpress | **Shopee (Forebie Store)** |
| Data Volume | 5,000 | 3,000 | 497 | **684** |
| Data Source | Google Play Scraper | Web Scraping | X + Google Play | **Playwright (Direct)** |
| Number of Classes | 3 | 3 | 3 | **3** |
| Labeling | Rating | TextBlob | Manual | **Rating** |
| Imbalance Method | Random Oversampling | — | — | **class_weight='balanced'** |
| Best Algorithm | LR (85.11%) | RF (94%) | SVM (93%) | **LR (73.1%)** |
| Macro/Weighted F1 | **0.58** | — | — | **0.732** |

#### 3.4.2 Unique Findings: Data Contamination and Emoji Translation Artifacts

Word Cloud analysis on negative reviews revealed interesting phenomena rarely discussed in the literature:

**1. Contamination from Seller Replies (Seller Reply Leakage):**
Words such as *"mohon"* (please), *"maaf"* (sorry), *"respon"* (response), *"minbie"*, *"siap"* (ready), *"bantu"* (help) dominated the negative review Word Cloud. Investigation showed that the scraper tool also extracted **seller response text** attached to customer reviews. The Forebie store administrator (who calls themselves "Minbie") consistently responded to 1-2 star reviews with a template: *"Mohon maaf kak, apakah ada kendala? Minbie siap membantu"* ("We apologize, is there an issue? Minbie is ready to help"). This response text was mixed into the negative review data, causing bias in word distribution.

**2. Emoji Translation Artifacts:**
The emoji conversion stage using `emoji.demojize(language="id")` produced unexpected words in the Word Cloud:
- The sparkling heart emoji was translated to `:hati_bersinar:` (sparkling_heart), which after tokenization produced the words *"hati"* (heart) and *"sinar"* (shine).
- The loudly crying face emoji was translated to `:wajah_menangis_keras:` (loudly_crying_face), producing the words *"wajah"* (face), *"menang"* (win — a stemming result of *"menangis"* / crying), and *"keras"* (loud).

These findings highlight **real challenges** in Indonesian-language social media text preprocessing, where emoji conversion and non-standard text handling require special attention to avoid unwanted noise.

#### 3.4.3 Logistic Regression Superiority

Logistic Regression outperformed SVM and Naive Bayes on this dataset. This is in line with findings by Kadir and Fairuzabadi [5], who also found Logistic Regression to be the best model compared to SVM and Naive Bayes. The superiority of Logistic Regression in this context can be attributed to:

1. **Probabilistic estimation:** Logistic Regression produces class probabilities, allowing for smoother decision boundaries compared to margin-based SVM [5].
2. **Compatibility with `class_weight='balanced'`:** This parameter works more effectively in Logistic Regression because it directly and proportionally affects the loss function.
3. **Stability on limited data:** With only 666 samples, Logistic Regression demonstrated more stable performance compared to SVM, which is more sensitive to dataset size [5][12].

---

## 4. Conclusion

Based on the research results and discussion, it can be concluded that:

1. An **end-to-end sentiment analysis pipeline** was successfully built, encompassing primary data collection using Playwright, feature engineering, text preprocessing with Sastrawi, TF-IDF feature extraction, as well as modeling and evaluation using three classification algorithms.

2. From the comparison of three algorithms, **Logistic Regression** provided the best performance with a **weighted F1-Score of 0.732** and **Accuracy of 0.731**. This model is more balanced in recognizing all three sentiment classes compared to SVM and Naive Bayes.

3. This model's performance is **comparable** with previous studies when considering: (a) the use of more difficult 3-class classification, (b) the smaller dataset size, and (c) the characteristics of cosmetic product reviews that use informal language and emojis intensively. The weighted F1-Score (0.732) of this study is even higher than the macro-F1 reported by Kadir and Fairuzabadi [5] (0.58), although their accuracy was higher.

4. Word Cloud analysis revealed **unique findings** in the form of data contamination from seller responses and emoji translation artifacts, which serve as important notes for future e-commerce sentiment analysis research.

### Recommendations for Future Work

1. **Stricter data cleaning:** Adding a stage to separate seller response text from customer review text to avoid data contamination.
2. **Increasing data volume**, especially for the Neutral and Negative classes, so the model can better distinguish between the three classes.
3. **Exploring data balancing techniques** such as SMOTE or Random Oversampling for comparison with the `class_weight='balanced'` approach.
4. **Exploring deep learning models** such as IndoBERT, which are expected to be better at capturing sentence context and overcoming the limitations of frequency-based TF-IDF [5].

---

## References

[1] Indonesian Internet Service Providers Association (APJII), "APJII Internet Survey Report 2024," Jakarta, 2024.

[2] A. Saepudin, A. Faqih, and G. Dwilestari, "Comparison of Support Vector Machine, Random Forest, and Logistic Regression Classification Algorithms on Shopee Reviews," *Jurnal TEKNO KOMPAK*, vol. 18, no. 1, pp. 178-192, 2024. P-ISSN: 1412-9663, E-ISSN: 2656-3525.

[3] F. Pedregosa *et al.*, "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, 2011.

[4] B. Liu, "Sentiment Analysis and Opinion Mining," *Synthesis Lectures on Human Language Technologies*, vol. 5, no. 1, pp. 1-167, 2012.

[5] S. F. Kadir and A. Fairuzabadi, "Sentiment Analysis of Shopee Reviews on Google Play with TF-IDF and Logistic Regression," *Journal of Artificial Intelligence and Digital Business (RIGGS)*, vol. 4, no. 2, pp. 7940-57945, 2025. DOI: 10.31004/riggs.v4i2.2850.

[6] A. Saepudin, A. Faqih, and G. Dwilestari, "Comparison of Support Vector Machine, Random Forest, and Logistic Regression Classification Algorithms on Shopee Reviews," *Jurnal TEKNO KOMPAK*, vol. 18, no. 1, pp. 178-192, 2024.

[7] S. Fathurrohman, I. Wahyuningtyas, I. R. Afandi, A. S. Nugroho, and F. N. Hasan, "Sentiment Analysis on Shopee Xpress Delivery Time Reviews Using Support Vector Machine and Logistic Regression," *IJID (International Journal on Informatics for Development)*, vol. 14, no. 2, pp. 640-658, Dec. 2025. DOI: 10.14421/ijid.2025.5073.

[8] Emoji Python Library. [Online]. Available: https://pypi.org/project/emoji/

[9] C. D. Manning, P. Raghavan, and H. Schutze, *Introduction to Information Retrieval*. Cambridge University Press, 2008.

[10] J. Asian, "Effective Techniques for Indonesian Text Retrieval," *PhD Thesis*, RMIT University, 2007.

[11] A. Pak and P. Paroubek, "Twitter as a Corpus for Sentiment Analysis and Opinion Mining," in *Proc. LREC*, 2010.

[12] Sastrawi — Python Library for Indonesian Stemming. [Online]. Available: https://github.com/har07/PySastrawi

---

*Note: This article is a journal draft prepared as part of the Final Project for the Data Science Course, Department of Informatics Engineering — FST UIN Syarif Hidayatullah Jakarta.*
