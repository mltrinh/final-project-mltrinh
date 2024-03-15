# final-project-mltrinh

HCDE 310 Final Project (Health & You): This is a website that gives information on user-selected health topics. It
combines data from MyHealthFinder API with OpenAI and IBM Text to Speech to give users a summary of health topics that
they are interested in. It also includes an audio recording of the summary (which may take a minute to load).

The website works for both english and spanish users. However, users may only select 3 topics that they are interested
in. This is due to limitations with the openAI API key and flask session storage. If you are using a paid version of
openAI API, it may be possible to increase the amount of articles users can select.

NOTE: Be cautious of the import `ssl` and `ssl._create_default_https_context = ssl._create_unverified_context lines`
in the code. There was a problem with certifi verification so this was added in response to the error.

# Necessary APIs and relevant Links

1. [`MyHealthFinder API`](https://health.gov/our-work/national-health-initiatives/health-literacy/consumer-health-content/free-web-content/apis-developers):
   No API key needed. This API provides health information via articles from
   [health.gov](https://health.gov/myhealthfinder).
2. [`OpenAI`](https://platform.openai.com/docs/overview): To obtain an API key, you can do one of two things. If you
   have not used openAI before, you can create a new account, go to [API Keys](https://platform.openai.com/api-keys),
   create new secret key,and then use the $5 free trial. Or for less restrictions, you can upgrade a current
   [openAI account](https://platform.openai.com/account/billing/overview) and then get an API Key.
3. [`IBM Text to Speech`](https://cloud.ibm.com/apidocs/text-to-speech): To obtain an API key, you can start a [free
   trial](https://www.ibm.com/products/text-to-speech), follow the steps to make a new account, go to
   the [text to speech
   catalog page](https://cloud.ibm.com/catalog/services/text-to-speech), select a location (I chose Dallas), then click
   create. If you want to use the free trial (i.e., $200 promotional) make sure you switch the plan from lite to
   standard. Note that this API may ask you to enter credit card information.
