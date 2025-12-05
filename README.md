# Referee Bias and Racism in the Premier League [2009-2025]

| Course | Course Name | Professor | Semester / Year | 
| ------ | ----------- | --------- | --------------- |
| CPSC 597 | Project | Rong Jin | Fall 2025 |

## Developer & Researcher
| Name | Email | 
| ---- | ----- |
| Erwin Medina | erwin.l.medina@gmail.com |

## Summary & Objective
Premier League fans have long expressed criticism toward referees, often perceiving them as biased individuals whose decisions intentionally influence the outcome of matches. As a fan myself, I have made a conscious effort to move beyond the subjective "my team" perspective and instead approach the game through an objective lens. Nonetheless, I have frequently found it difficult to dismiss the notion that certain referees exhibit bias in their calls and overall decision-making. It is important to acknowledge, however, that officiating is an inherently challenging role. Many decisions must be made instantaneously, often amid the crowd noise, player pressure, and obstructed lines of sight that complicate the referee's judgment. 

This project seeks to take an evidence-based approach. We aim to conduct statistical analyses and apply machine learning techninques to identify potential patterns in referee behavior and predict future trends. Additionally, we will explore whether there is any indication of bias, specifically toward foreign players or potential racial bias, in the distribution of cards. The dataset will encompass Premier League matches spanning from the 2009-2010 season through the 2024-2025 season.

## Things to Know:
- My JupyterLab project is in the Juptyer folder.
- There are multiple `MasterDataset_ML*.xlsx` in that folder because each contains variations of the dataset that I attempted to feed the model.
- In my `Master Datasets` -> `Incident Report Dataset` I have multiple iterations of my completed dataset. The final version being the `Master_ML_ThirdPass`. That version got copied into the Jupyter folder and renamed. Not ideal. I apologize.
- Similarly, the `Player Info Dataset` has mutiple versions of the `Player Information*.xlsx`. Assume v3 is the latest and best version.
- I have multiple `ReadMe` documents throughout my folders in case someone is curious and wants to read through the data and how/why I collected what I did.
- I used streamlit; so fork this project and simply run: `streamlit run app.py` and it should open a localhost.
- If any questions, please email me at the above listed email address.

## Outcome / Results
| Hypothesis | Result |
| ---------- | ------ |
| Can the model determine who the referee is based on game statistics, and stadium information? [Referee Predictor] | Inconclusive |
| Using the same information, does the model lean on foreigners being carded as an important feature? [Racial Bias / Discrimination] | Inconclusive |
| Can the model determine if a game was a win/loss/draw with game statistics, referee information, and stadium information? [Match Outcome Predictor] | Inconclusive |

### Conclusion
-----------
Results show that patterns did not emerge from the features aand scale of data that I provided. However, this does not rule out the existence of meaningful patterns. Perhaps deeper, richer, more granular inputs/data could provide better results. I continue to firmly believe that bias and discrimination exists in the sport, however, quantifying it may be more difficult than anticipated.

### Retrospection
----------
- Possibly start at a lower league, not the most scrutinized, financially powerful, and professionally regulated league in the world with layers of oversight. Start small, find features that might be critical and then move up to larger leagues.
- Using computer vision tools for video analysis to capture fouls that _weren't_ called. However, obtaining extensive video footage of games from decades ago might be problematic. 

## Technologies Used
- Python
- Excel (CSV / xlsx)
- BeautifulSoup4 (Webscraping)
- Machine Learning w/ Scikit Learn (Random Forest, Logistic Regression, Gradient Boosting, SVM, K-Nearest Neighbors)
- JupyterLab
- Streamlit for Demo

## Images
| Description | Image |
| ----------- | ----- |
| Referee Predictor - Multiple Models | <img src="https://i.imgur.com/zbEGrBK.png"> |
| Referee Predictor - Feature Importance | <img src="https://i.imgur.com/Szs6RAg.png"> |
| Match Predictor - Multiple Models | <img src="https://i.imgur.com/8lrdETw.png"> |
| Match Predictor - Feature Importance | <img src="https://i.imgur.com/o7KnWvx.png"> |
| Streamlit Demo - Top | <img src="https://i.imgur.com/26UUWpz.png"> |
| Streamlit Demo - Predict Ref | <img src="https://i.imgur.com/y57GFto.png"> |
| Streamlit Demo - Predict Match | <img src="https://i.imgur.com/o3vfXoz.png">