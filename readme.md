# How to use this Rag AI Teaching assistant on your own data
## step 1 --- collect your videos
Move all your video files to the videos folder

## step 2 --- convert mp3 to json
convert all the video mp3 files to json by running video_to_mp3

## step 3 --- Convert mp3 to json 
convert all the mp3 files to json by running mp3_to_json

## step 4 --- Convert the json files to vectors
use the file preprocess_json to convert the json files to a DataFrame with Embeddings and Save it as a JobLib pickle

## step 5 --- Prompt generation and feeding to LLM
Read the joblib file and load it into the memory. Then Create a relevant prompt as per the user query and feed it to the LLM

