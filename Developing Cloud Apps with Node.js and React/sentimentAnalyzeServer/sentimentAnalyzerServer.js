const express = require('express');
const app = new express();
const dotenv=require('dotenv');
dotenv.config();

app.use(express.static('client'))

const cors_app = require('cors');
app.use(cors_app());

app.get("/",(req,res)=>{
    res.render('index.html');
  });

app.get("/url/emotion", (req,res) => {

     analyzeEmotionUrl(req.query.url,res);
   // return res.send({"happy":"90","sad":"10"});
});

app.get("/url/sentiment", (req,res) => {
  //  return res.send("url sentiment for "+req.query.url);
   //  analyzeEmotionUrl(req.query.url,res);
    analyzeSentimentUrl(req.query.url,res);
});

app.get("/text/emotion", (req,res) => {
   // return res.send({"happy":"10","sad":"90"});
  analyzeEmotionText(req.query.text,res);
});

app.get("/text/sentiment", (req,res) => {
 //   return res.send("text sentiment for "+req.query.text);
    analyzeSentimentText(req.query.text,res);
});

let server = app.listen(8080, () => {
    console.log('Listening', server.address().port)
})

function getNLUInstance() {
let api_key = process.env.API_KEY; 
let api_url = process.env.API_URL;
const NaturallanguageUnderstandingV1 = require('ibm-watson/natural-language-understanding/v1');
const { IamAuthenticator } = require('ibm-watson/auth');

const naturalLanguageUnderstanding = new NaturallanguageUnderstandingV1({

version: '2020-08-01',

authenticator: new IamAuthenticator({

apikey: api_key,

}),

serviceUrl: api_url,

});

return naturalLanguageUnderstanding;

}




function analyzeEmotionUrl(url,res){
    const naturalLanguageUnderstanding= getNLUInstance();
    const analyzeParams = {
  'url':url,
  'features': {
    'emotion': {
    }
  }
};
naturalLanguageUnderstanding.analyze(analyzeParams)
  .then(analysisResults => {
    console.log(JSON.stringify(analysisResults, null, 2));
   // return analysisResults.result.emotion.document.emotion;
   res.send(analysisResults.result.emotion.document.emotion);
  })
  .catch(err => {
    console.log('error:', err);
  });

}


function analyzeEmotionText(sampleText,res){
    const naturalLanguageUnderstanding= getNLUInstance();
    const analyzeParams = {
  'html':sampleText,
  'features': {
    'emotion': {     
    }
  }
};
naturalLanguageUnderstanding.analyze(analyzeParams)
  .then(analysisResults => {
    console.log(JSON.stringify(analysisResults, null, 2));
   // return analysisResults.result.emotion.document.emotion;
   res.send(analysisResults.result.emotion.document.emotion);
  })
  .catch(err => {
    console.log('error:', err);
  });

}


function analyzeSentimentText(sampleText,res){
    const naturalLanguageUnderstanding= getNLUInstance();
      
   const analyzeParams = {
      'html': sampleText,
       'features': {
        'sentiment': {
          
        }
       }
    };

    naturalLanguageUnderstanding.analyze(analyzeParams)
      .then(analysisResults => {
        console.log(JSON.stringify(analysisResults, null, 2));
        //.result.entities[0].sentiment
         res.send(analysisResults.result.sentiment.document.label);
        
      })
      .catch(err => {
          
        console.log('error:', err);
         res.send("nutral");
      });

}
function analyzeSentimentUrl(url,res){
    const naturalLanguageUnderstanding= getNLUInstance();
      
   const analyzeParams = {
      'url': url,
       'features': {
        'sentiment': {
          
        }
       }
    };

    naturalLanguageUnderstanding.analyze(analyzeParams)
      .then(analysisResults => {
        console.log(JSON.stringify(analysisResults, null, 2));
         res.send(analysisResults.result.sentiment.document.label);
      })
      .catch(err => {
        console.log('error:', err);
         res.send("nutral");
      });

}