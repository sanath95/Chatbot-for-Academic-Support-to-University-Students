# Developing a Context-Aware Chatbot for Academic Support

This project consists of the following components:
- Data collection (Webscraping/srh_course_content_scraper.py)
- Data processing (Webscraping/convert_to_fstring.py)
- LLMs implementation (NLP/llama3.ipynb)

---

### How to execute:

- Run the following command in Terminal to install all the required libraries

    > pip install -r requirements.txt

#### Data collection:

- Run the script 'Webscraping/srh_course_content_scraper.py'.
- This will open a chrome browser and start to scrape data from various websites.
    > NOTE: The 'Accept Cookies' popup might cause some data loss. So click it manually the first time it pops up to avoid this issue.
- This creates a 'outputs' folder with the csv file inside it.

#### Data processing

- Run the script 'Webscraping/convert_to_fstring.py'.
- This will read the csv file and convert it to a single python string.
- The string will be saved in a .txt file inside the output folder.

#### LLMs implementation

- [Download Ollama](https://ollama.com/download) as per your system.
- Execute the following commands in the terminal
    > ollama pull llama3

    > ollama serve
- Run the ipynb file on the local machine.

> NOTE: Running the ipynb file on Google Colab might not be possible as it will not be able to access the Ollama model.

---

### Documentation

#### Data Collection and Preprocessing:

- Data collection and preprocessing has been achieved through dynamic web scraping using Selenium.
- All the masters course websites of the SRH Heidelberg website have been scraped.
- The content is saved in a csv file in a structured format.
- The text data is there converted to a single python string object to be fed into the LLM (inspired by ONTEC table extractor).
- This string is saved in a text file.

#### Model Selection and Training:

- Llama3 model has been selected. Other options were Mistral, Bert. But due to time constraints they couldn't be tested.
- The model is not exactly fine tuned with the data; rather the data is being sent as context in order to generate the responses.
- The models were used with different treshhold values. Finally, I concluded that 0.7 is a good value.
- Also, 2 models were created:
    1. One was fed the csv file as the context (after processing with CharacterTextSplitter).
    2. Another model was trained with the single fstring.

#### Testing

- By visual inspection of the generated responses, the optimum treshhold was selected (can be improved using some quantitative metrics).
- I asked some of my classmates to come up with some questions and we asked both the models.
- After some testing, we concluded the model which was fed the python string was giving better output!
- We asked different type of questions like:
    - Questions based on the data provided.
    - Questions based on the data not provided.
    - Completely out of context questions.

#### Performance Evaluation:

- The qualitative aspects of the model were evaluated but not the quantitative metrics.

---

### Conclusion

The model which was fed the python string performed really well for all questions. We can see it handled really well the questions which came out of context. It also provided really detailed answers for questions from within context. The responses have a very human-like nature.

---