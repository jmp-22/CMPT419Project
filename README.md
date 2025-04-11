# CMPT419Project

## Project Structure

There are 5 notebooks in this project that must be run in order. 
No dataset is included in this repository, it must be downloaded if you wish to run the following project. However, to generate training results, the train.ipynb notebook can be run using the example file ```N_1000_filtered_train_data_with_features.csv``` located in ```example_files```


Project structure
```
📂 Project Folder Structure
.
├── README.md
├── requirements.txt
├── annotate_app.py

📘 Notebooks
├── install_dataset.ipynb (1)
├── filter_dataset.ipynb (2)
├── annotate_dataset.ipynb (3)
├── extract_and_visualize.ipynb (4)
├── train_prosody_only_binary.ipynb (5.1)
├── train_prosody_only_type.ipynb (5.2)
├── train_multi_modal_binary.ipynb (5.3)
├── train_multi_modal_type.ipynb (5.4)
├── inter_rater_agreement_score.ipynb
├── inter_rater_agreement_scores.ipynb

📀 Final Dataset
├── N_1000_filtered_train_data_with_features.csv

📄 Other CSV Data Files (copy stored in Example Files)
├── N_1000_filtered_train_data.csv
├── filtered_train_data.csv
├── train_data.csv
├── atc_audio_annotations.csv
├── atc_audio_annotations_Jimmy.csv
├── atc_audio_annotations_Jonathan.csv
├── atc_audio_annotations_Lucy.csv

📁 Model Files
├── best_model.pt

📂 audio_files (only exist after installing dataset)


```

To run this project, a few prerequisites are needed. Firstly, the dataset is not included in this project by default. So, you will need to download audio data and transcriptions from the dataset page on huggingface. The dataset can be found here: 
https://huggingface.co/datasets/jacktol/atc-dataset

To download, you will need a huggingface token. Please follow the instructions here to create an account and/or generate a token:
https://huggingface.co/docs/huggingface_hub/quick-start

Once you have a token, you can begin! Please note that approximately 700 mb of storage is required.

## 0. Setup Python Virtual Environment

Create a virtual environment folder by running the following commands in a terminal window inside the Project Directory:

```python3 -m venv env```

```source env/bin/activate```

You should see (env) next to your command prompt.

Run ```pip install -r requirements.txt``` to install required modules

## 1. Install Dataset

Open and run 
> install_dataset.ipynb

(VSCode was used for this project). Running the cells in order will load the audio files and accompanying transcriptions to your project folder. Names will be automatically set and should not be manually renamed to avoid file path confusion later in this project. Please note that the download can take anywhere from 2-10 minutes depending on network speed.

## 2. Filter Dataset

Once the dataset has been downloaded, open and run
> filter_dataset.ipynb 

 to reduce the number of instances to a more usable amount! Run the notebook cells in order to create a CSV containing 1,000 instances. There is roughly a 50/50 split of suspected questions and suspected statements. At the end of this step, you'll be left with a CSV called: 

> N_1000_filtered_train_data.csv 

This will be used in the next step for annotation. 

## 3. Annotate Dataset

If you wish to review clips, examine current annotations, or update annotations, use 
> annotate_dataset.ipynb

 It will open a GUI application to speed up the manual annotation process. Once completed, save your annotations and close the app. You may then need to update the annotation filename in the next cell to match the file you just saved. Then, run the rest of the notebook to merge your annotations with the

> N_1000_filtered_train_data.csv 

dataset.

## 4. Extract and Visualize

Now that you have an annotated dataset of 1,000 examples, it is time to extract prosodic features. To do this, run 

> extract_and_visualize.ipynb

 in order and a new CSV containing the audio paths, transcription, labels, and features will be created. This new file will be called:
 
 > N_1000_filtered_train_data_with_features.csv 
 
 You can also visualize scatter plots of features and graphs showing useful information about the dataset, many of which are used in our report and presentation.

## 5. Train

To train classifiers and generate results, run 

```
5.1 - train_prosody_only_binary.ipynb
5.2 - train_prosody_only_type.ipynb 
5.3 - train_multi_modal_binary.ipynb 
5.4 - train_multi_modal_type.ipynb 
```

# Self-Reflection

In retrospect, we faced difficulty in accurately classifying questions from prosodic features alone. However, we believe that this difficulty is particular to the dataset and application of our project. Many instances of the data were ambiguous to our own ears, due to the style of ATC communication. Operators typically speak with flat inflection in a monotone style, which makes it difficult to an untrained ear to identify questions. However, as we have outlined in our report, questions are being asked in such a way that follows protocol and uses specific language. It is only when unexpected circumstances occur that ATC and pilots may use a tone that conveys more information. The results of our classifier using prosodic features alone was slightly better than random guesses. However, when trained with lexical features, the classifier’s accuracy improved to over 80%. Our classifier methods were suited to the types of numerical features we extracted, but we think that better results could be achieved using a deep-learning approach to capture the complex patterns inherent in speech. To find success doing deep learning, a larger labelled dataset is required for supervised learning, or an unsupervised approach may produce better results if simply trained on spectrogram features. The problem of accurately interpreting tone is far from being solved and many fields, including aviation communication, could benefit from increased focus on prosodic features.







