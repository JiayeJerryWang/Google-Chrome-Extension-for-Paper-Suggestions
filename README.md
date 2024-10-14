# Google Chrome Extension for Paper Suggestions

This project is a Google Chrome extension that provides paper suggestions related to a course based on phrases highlighted by users. It uses React for the front end and Node.js for the back end, implementing a PLSA (Probabilistic Latent Semantic Analysis) model to recommend relevant research papers.
The theme of our project is Google Chrome Extension for paper suggestions based on key-phrase from all mentioned papers in lectures of CS410, which is an educational chrome extension to help students in the CS410 course. When browsing web pages, students might have problems of understanding the concepts or keywords and want to learn more about them. To help students better understand the content in our course, we design a Google Chrome extension, which shows the relevant papers of terms and the related content in these papers when users highlight the terms. These relevant papers are chosen from the offline database containing all research papers mentioned at the end of each lecture. The relevance between papers and the query content is computed based on the PLSA model. Students are also provided with academic information from Google Scholar and general information from Google Search by this extension. These recommendations are based on the relevance of the highlighted words or phrases when students browse web pages.

## Features
- **Phrase Highlighting**: Users can highlight any phrase on a webpage to get suggestions for related research papers.
- **Paper Suggestions**: The extension provides a list of related papers based on the highlighted phrase, fetched from a backend service.
- **React-based Front End**: The extension's interface is built using React, providing a responsive and dynamic user experience.
- **Node.js Back End**: The back end is built using Node.js to serve paper suggestions, using trained PLSA models to process large datasets.
- **PLSA-based Paper Recommendation**: A PLSA model is implemented to analyze large datasets and provide the most relevant research papers related to the user's query.

## Project Structure
- **Frontend (React)**: Handles the user interface, interactions, and displays the suggested research papers.
- **Backend (Node.js)**: Manages HTTP requests and connects to a PLSA model that processes datasets and returns related paper suggestions.
- **PLSA Model**: The model processes large datasets of research papers to find the most relevant content based on user input.

## Related Work
### Machine Learning
- Our PLSA model is modified and trained based on MP3.
- Main library used: NumPy, BeautifulSoup, os, json.

### Server
- It is mainly implemented in JavaScript and running by Node.js. 
- It utilizes a lot of standard libraries provided by Node.js and libraries distributed by npm. Some of them are http, url, path, request, and cheerio.
- We referred to many online tutorials and blogs while developing our server program. The links of them are commented inside our code files.

### Chrome Extension
- It is mainly implemented in JavaScript.
- It utilized Google Chrome APIs.

## Technical Architecture
### Architecture Diagram
- The google-extension folder contains both the compiled scripts in the dist folder and the source code in src folder. By following the online project mentioned above, we put the HTML file and icon images into the dist folder as well.
    - The extension first captures the highlighted words of users and sends it to the server via HTTP connections. After receiving the output from the server, it changes the HTML file to display the results.
- The server folder contains our dependency list and the source code files. 
    - The server basically sets up a HTTP server and listens to the request from our Google Chrome Extension. After receiving the request, it creates a subprocess to run the Machine Learning prediction program and sends request to Google Scholar and Google Search. With this retrieved information, it sends the response containing these three outputs with JSON via HTTP connections to the extension.
   
In addition to the detailed code structure or architecture for our project demonstrated by the attached diagram above, we explain the process of our pre-trained PLSA model in the following:
### Machine Learning
#### Pdf2txt.py 
The first task of building the PLSA model is to pre-process the paper documents. We have downloaded all the papers mentioned in the lecture as pdf files. We need to reformat the papers from pdf documents to txt documents, which can be easily read by python. In fact, the difficulty is that many papers have subfields (columns), which are hard to process. The Optical Character Recognition (OCR) method is hard to implement and does not have a good performance for our dataset. We utilized the tree hierarchy of html documents to distinguish different parts of paper documents. In pdf2txt.py, we traverse the folder which contains the paper documents and reformat them from pdf file to html file. Then we extract the content in html file and save as txt file. In that case the paper content can be read by our PLSA model. We already run pdf2txt.py and produced the txt files of papers, so that users do not need to run it again.
#### Plsa.py
Plsa file contains our model, which is modified based on MP3. We used PLSA model to compute the relevance between query sentences and paper documents. For the parameters, we choose 10 topics and iterate to likelihood convergence with maximum iteration of 100. The PLSA model will compute the probability matrix of words occurred in documents when converged: 
$$ P(w) = \sum_{i=j}^k\pi_{d, j} P(w|\theta_j)$$
The probability matrix has a shape of (number of vocabulary, number of documents). The model can save the probability matrix and the vocabulary as two txt files, which can be used in main.py to find the relative papers based on query sentences. PLSA model is already trained and adjust in plsa.py, and the prob_matrix.txt and vocabulary.txt have already produced, so users do not need to run it again.
#### Main.py
Main.py has the query sentences as input and print the relative paper titles, a part of content related to query, and the paper links to the backend program. We segment the query sentences into word level, and compute the probability of combination of these words utilizing the probability matrix produced by our PLSA model. Then we will choose one or two papers which have the highest relevance scores as relative papers. Then we find the context of the query sentence appearing in the paper content. We print the titles, the context content, and paper links to our server to let it show on our extension.

## Installation and Usage
### Installation
Requirement: 
- Python Version >= 3.5 and 
- Numpy installed
```Bash
python --version
```
```Bash
pip install numpy
```
We implement and run programs in the following sequence.

#### Windows 
1. Download Node.js and install from (https://nodejs.org/en/download/)
2. Clone the repository

3. Change the current directory to `server`    

4. Turn on the server

```
npm install
```
```
node index.js
```
5. Upload google extension to Chome

    Visit `chrome://extensions/` in your Chrome Browser

    Click `Load unpacked` on the top left side

    Select the `dist` folder in the google-extension

6. Start using the extension


#### MacOS / Linux

1. Download Node.js and install (https://nodejs.org/en/download/).  

2. Clone the repository
  
3. change the current directory to `server`

4. Turn on the server
```
npm install
```
```
node index.js
```

5. Install the google-extension in Google Chrome.

    Visit `chrome://extensions/` in your Chrome Browser

    Click `Load unpacked` on the top left side

    Select the `dist` folder in the google-extension

6. Start to use the extension.


### Usage
1. Pin the extension on google chrome

2. On the web page, high light the text that you want to search for

3. Click open the extension, the high light text should be displayed in the textbox, you can also manually change it or enter new text information

4. Click the "Search Text" button, then the input text and the result will be displayed.

5. The result is consist of 3 parts. The first part will be the relevant papers suggestions from all mentioned papers in the course CS410. The second part will be the relevant paper suggestions from google scholar based on the inputed search text. The third part will be the relevant google search results based on the inputed search text. You can click the triangle or the bold headings to expand the lists of them.

## Disclaimer
1. There is a slight limitation on the highlighted / entered text: the highlight get selection feature may not work on certain PDFs that are opened on the chrome. Also, in case of certain special characters (Eg: certain new line characters), the result may display "error".

2. Also, there is a slight limitation on the time use (rate limiting) of the google extension. Since Google Scholar / Google Search may block the IP address for a period of time if too many requests are sent in a given amount of time without passing Google's reCAPTCHA test, the server program may return the code 429. In this case, some results cannot be retrieved from Google and thus displayed by our extension due to the temporary block by Google.

3. We now only support and test English words, but it maybe support all UTF-8 symbols.
