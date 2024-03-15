# final-project-mltrinh

HCDE 310 Final Project (Health & You): This is a website that gives information on user-selected health topics. It
combines data from MyHealthFinder API with OpenAI and IBM Text to Speech to give users a summary of health topics that
they are interested in. It also includes an audio recording of the summary (which may take a minute to load).

The website works for both english and spanish users. However, users may only select 3 topics that they are interested
in. This is due to limitations with the openAI API key and flask session storage. Future work can be done to hopefully
increase the topics users can select at a time.

# Necessary APIs and relevant Links

1. [`MyHealthFinder API`](https://health.gov/our-work/national-health-initiatives/health-literacy/consumer-health-content/free-web-content/apis-developers)
2. [`OpenAI`](https://platform.openai.com/docs/overview)
3. [`IBM Text to Speech`](https://cloud.ibm.com/apidocs/text-to-speech)
