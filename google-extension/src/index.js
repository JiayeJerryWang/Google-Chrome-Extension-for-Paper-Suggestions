// Based on the GitHub repo shared by TAs
// https://dev.to/debosthefirst/how-to-build-a-chrome-extension-that-makes-api-calls-1g04
// https://github.com/onedebos/covtension
import axios from "axios";
const server = "http://127.0.0.1:4100/";

const errors = document.querySelector(".errors");
const loading = document.querySelector(".loading");
const results = document.querySelector(".result-container");

const selection = document.querySelector(".selection");
const papers = document.querySelector(".papers");
const scholar = document.querySelector(".scholar");
const google = document.querySelector(".google");


results.style.display = "none";
loading.style.display = "none";
errors.textContent = "";

// grab the form
const form = document.querySelector(".form-data");
// grab the key words
const textbox = document.querySelector(".textbox-input");

// obtain the user's selection with their mouse
chrome.tabs.executeScript( {
  code: "window.getSelection().toString();"
}, function(selection) {
  document.getElementById("highlight").innerHTML = selection[0];

  // https://stackoverflow.com/questions/11770858/setting-html-textbox-value-using-javascript-function
  document.querySelector(".textbox-input").value = selection[0];
});

// declare a method to search by key words
const searchForKeyWords = async textboxValue => {
  loading.style.display = "block";
  errors.textContent = "";

  textboxValue = textboxValue.replace(/[\r\n]+/gm,"");
  // visit the server's API
  try {
    const stringResponse = await axios({
      method: 'post',
      url: `${server}`,
      data: {
        selection: textboxValue
      },
      responseType:'json',
    });
    let jsonResponse = stringResponse.data;

    selection.textContent = jsonResponse["selection"];

    // set the list of HTML for relevant papers
    let text = '';
    jsonResponse["relevantPapers"].forEach((ele, ind) =>{
      if (ind<5){
        console.log(ele);
        text += '<p><a href=\"'+ ele.link + '\" target=\"_blank\">' + ele.paperTitle + '</a>' + 
                '<br><b>Abstract:</b> ' + ele.abstract + '</p>';
      }
    })
    papers.textContent = 'Relevant Papers:' ;
    document.getElementById("papersroutput").innerHTML = text;

    // set the list of HTML for Google Scholar results
    let text1 = '';
    jsonResponse["scholarResults"].forEach((ele, ind) =>{
      if (ind<5){
        console.log(ele);
        text1 += '<p><a href=\"'+ ele.link + '\" target=\"_blank\">' + ele.title + '</a>' +
                  '<br><b>Snippet:</b> ' + ele.snippet +
                  '<br><b>Publication_info:</b> ' + ele.publication_info + '</p>';
      }
    })
    
    scholar.textContent = 'Google Scholar Results:' ;
    document.getElementById("scholaroutput").innerHTML = text1;

    // set the list of HTML for Google Search results
    let text2 = '';
    jsonResponse["googleResult"].forEach((ele, ind) =>{
      if (ind<5){
        console.log(ele);
        text2 += '<p><a href=\"'+ ele.links + '\" target=\"_blank\">'+ ele.title + '</a>' + 
                  '<br><b>Snippet:</b> ' + ele.snippet + '</p>';
      }
    })
    google.textContent = 'Google Search Results:' ;
    document.getElementById("googleoutput").innerHTML = text2;


    loading.style.display = "none";
    results.style.display = "block";
  } catch (error) {
    loading.style.display = "none";
    results.style.display = "none";
    errors.textContent = "Error!";
  }
};

// declare a function to handle form submission
const handleSubmit = async e => {
  e.preventDefault();
  searchForKeyWords(textbox.value);
  console.log(textbox.value);
};

form.addEventListener("submit", e => handleSubmit(e));
