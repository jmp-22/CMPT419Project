# CMPT419Project

To run this project, a few prerequisites are needed. Firstly, the dataset is not included in this project by default. So, you will need to download audio data and transcriptions from the dataset page on huggingface. The dataset can be found here: 
https://huggingface.co/datasets/jacktol/atc-dataset

To download, you will need a huggingface token. Please follow the instructions here to create an account and/or generate a token:
https://huggingface.co/docs/huggingface_hub/quick-start

Once you have a token, you can begin! Please note that approximately 700 mb of storage is required.

## 1. Install Dataset

Open  
> install_dataset.ipynb

in your favourite code editor (VSCode was used for this project). Running the cells in order will load the audio files and accompanying transcriptions to your project folder. Names will be automatically set and should not be manually renamed to avoid file path confusion later in this project. Please note that the download can take anywhere from 2-10 minutes depending on network speed.

## 2. Filter Dataset

Once the dataset has been downloaded, open 
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

TBD

