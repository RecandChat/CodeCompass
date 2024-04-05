# AI-Powered GitHub Recommendation Engine
## Introduction
Welcome to our AI-powered Recommendation Engine project, a cutting-edge tool designed to enhance the learning and development journey of software developers. This engine utilizes users' GitHub profiles to offer personalized suggestions for projects, repositories for developers to follow. It's a unique bridge connecting developers with the diverse, rapidly-evolving technology landscape, aiding in skill enhancement and professional growth.

## Motivation
In the dynamic realm of software development, staying updated with the latest trends and technologies is essential. Our project embodies this ethos, leveraging an advanced recommendation system and chatbot to support continuous learning. Targeted at both students and developers, it helps in discovering projects that resonate with personal interests and expertise, fostering a culture of continuous learning and community engagement within the GitHub ecosystem. By keeping pace with emerging technologies, it provides invaluable insights into their relevance and real-world applications.

## Tech Stack and Architecture
### Data Retrieval
Data Source: GitHub API serves as the primary data source, providing access to a vast repository of user profiles and repositories.
Data Extraction: Utilizing Python requests library to fetch data from the GitHub API.
Data Storage: Storing user profiles and repository data in a google drive for easy access and retrieval.
Data Access: Accesing our data files using the google drive API.

### Recommendation Engine
Data Processing: Utilizing Python, pandas, and scikit-learn for robust data handling.
Algorithm Development: Using LightGBM, a hybrid recommendation algorithm, to generate personalized recommendations based on user profiles and preferences.
Technologies and Frameworks: Python is at the core, supplemented with Azure Databricks and AzureML service.
Model Deployment: The engine is deployed as a docker image, for easy deployent, interfacing with the GitHub API, processing data, and delivering tailored recommendations.
User Interface (UI): Created using streamlit, a user-friendly interface for seamless interaction with the recommendation engine.
Front-end Technologies: Crafted using Vue.js/Streamlit for an intuitive and responsive user experience.

### Chatbot Integration
Chatbot Framework: Leveraging OpenAI and AskTheCode to create an interactive chatbot experience.
User Interaction: The chatbot interacts with users, providing recommendations and answering queries related to GitHub repositories and projects.
UI: The chatbot is interfaced using streamlit, ensuring a seamless user experience.

### Overall System Architecture
Architecture Type: We've adopted a microservices architecture for enhanced scalability and flexibility.
APIs and Communication Protocols: RESTful APIs facilitate smooth microservice communication.
Dependencies and External Services: Integrating GitHub API and OpenAI for extended functionalities.

### Testing and QA
Testing Frameworks: Backend testing is rigorously conducted using Pytest.
CI/CD: Implementation of continuous integration and deployment through GitHub Actions, ensuring reliability and consistency.
Documentation
Internal Documentation: Maintained on GitHub wiki, encompassing detailed code comments and internal documentation strategies.
User Documentation: Simple and intuitive - enter your GitHub account name, choose your preferred recommendations, and enjoy tailored suggestions. Feedback is always welcome!

## How to Use 

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. To run the chatbot, navigate to the `fronted/chatbot` directory and run `streamlit run app.py`.
4. To run the recommendation engine, navigate to the `fronted/recommender` directory and run `streamlit run app.py`.
5. Enter your GitHub username and select your preferences to receive personalized recommendations.