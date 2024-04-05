![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=whit)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![chatGPT](https://img.shields.io/badge/ChatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![SciKitLearn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

# CodeCompass

## Overview

**CodeCompass is a Chabot and Reccomendation engine** that aims to enhance the GitHub experience for developers and learners alike by providing a personalized interface to discover and interact with repositories. Our goal is to make learning and discovery in GitHub intuitive, informative, and tailored to each user's interests and needs.

### Personalized Recommendations
Utilizing GitHub Data and Machine Learning algorithms, the system suggests GitHub projects that resonate with the user's historical interactions and preferences.

![Recommender](https://github.com/RecandChat/CodeCompass/assets/99414447/c97ef5d9-2857-4326-bcbc-f51db1fc3b7b)

### Interactive Exploration and Learning
The embedded chatbot enhances repository exploration, providing valuable insights and fostering a conducive exploration environment.

![Chatbot](https://github.com/RecandChat/CodeCompass/assets/99414447/2eaa069c-fd50-4518-bde3-3661a8d61061)

## Usage

Follow these steps to get CodeCompass up and running on your local machine:

**1.** Clone the repo:
```
git clone https://github.com/RecandChat/CodeCompass
```
**2.** Change to the project directory:
```
cd CodeCompass
```
**3.** Create Secrets Diretory at the root (`secrets/`)
- `askthecode_api`: Your API URL wrapper for the chatbot to make requests.
- `github_token`: Your GitHub API Token.
- `instructions`: Your chatbot system prompt.
- `openAI_key`: Your OpenAI API key.

**4.** Run:
  
Chatbot
```
streamlit run frontend/chatbot/app.py
```
Recommender:
```
streamlit run frontend/recommender/app.py
```
## Further Documentation
For more in-depth information, refer to the `documentation/Final_Report` directory within the repository.

## Contributors
- [Luca Cuneo](https://github.com/Lukasaurus11)
- [Gabriel de Olaguibel](https://github.com/gabrieldeolaguibel)
- [Keti Sulamanidze](https://github.com/KTsula)
- [Felix Gomez-Guillamon](https://github.com/felixggj)
- [Maud Hovland](https://github.com/maudhelen)
- [Miranda Drummond](https://github.com/mirandadrummond)