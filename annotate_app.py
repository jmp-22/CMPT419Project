import sys
import pandas as pd
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QWidget, QComboBox, QMessageBox, QFileDialog)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import sounddevice as sd
import soundfile as sf

class ATCAnnotationGUI(QMainWindow):
    def __init__(self, csv_path, audio_directory, current_index=0):
        super().__init__()
        self.setWindowTitle("ATC Audio Annotation Tool")
        self.resize(600, 400)

        # Load dataset
        self.df = pd.read_csv(csv_path, index_col=0)
        self.audio_directory = audio_directory
        
        # Tracking annotation progress
        self.current_index = current_index
        self.annotations = self.load_existing_annotations()

        # Setup UI
        self.init_ui()

    def init_ui(self):
        # Central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Transcription display
        self.transcription_label = QLabel("Transcription will appear here")
        main_layout.addWidget(self.transcription_label)
        
        self.suspected_label = QLabel("Suspected Label: None")
        main_layout.addWidget(self.suspected_label)
        
        self.current_label = QLabel("Current Label: None")
        main_layout.addWidget(self.current_label)
        
        

        # Audio playback buttons
        audio_layout = QHBoxLayout()
        play_button = QPushButton("Play Audio")
        play_button.clicked.connect(self.play_audio)
        audio_layout.addWidget(play_button)

        main_layout.addLayout(audio_layout)

        # Question type selection
        question_layout = QHBoxLayout()
        self.question_type_combo = QComboBox()
        self.question_type_combo.currentIndexChanged.connect(self.update_label)
        self.question_type_combo.addItems(["Select Type", "yn", "wh", "imp", "nq", "unknown"])
        question_layout.addWidget(QLabel("Question Type:"))
        question_layout.addWidget(self.question_type_combo)

        main_layout.addLayout(question_layout)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        prev_button = QPushButton("Previous")
        next_button = QPushButton("Next")
        save_button = QPushButton("Save Annotations")

        prev_button.clicked.connect(self.previous_clip)
        next_button.clicked.connect(self.next_clip)
        save_button.clicked.connect(self.save_annotations)

        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(next_button)
        nav_layout.addWidget(save_button)

        main_layout.addLayout(nav_layout)

        # Progress label
        self.progress_label = QLabel("Clip 0/0")
        main_layout.addWidget(self.progress_label)
    

        # Load first clip
        self.load_clip()

    def load_existing_annotations(self):
        """Load existing annotations from the CSV file into a dictionary."""
        annotations = {}
        
        # Ensure the necessary columns exist
        if 'audio_path' in self.df.columns and 'label' in self.df.columns:
            for _, row in self.df.iterrows():
                audio_path = row['audio_path']
                question_type = row['label']
                
                # Only store non-empty annotations
                if pd.notna(question_type):
                    annotations[audio_path] = question_type

        return annotations

    def play_audio(self):
        # Play audio file
        if self.current_index < len(self.df):
            audio_path = self.df.iloc[self.current_index]['audio_path']
            
            #print(f"Playing audio: {audio_path}")
            
            # Use sounddevice for audio playback
            data, samplerate = sf.read(audio_path)
            sd.play(data, samplerate)

    def load_clip(self):
        if self.current_index < len(self.df):
            # Load transcription
            current_row = self.df.iloc[self.current_index]
            self.transcription_label.setText(str(current_row['text']))
            
            if current_row['potential_question'] == 1:
                self.suspected_label.setText("Suspected Label: Question")
            else:
                self.suspected_label.setText("Suspected Label: Statement")
            
            #print("Current label ", current_row['label'])
            
   
            self.current_label.setText(f"Current Label: {self.annotations.get(current_row['audio_path'])}")
            
            # Update progress
            self.progress_label.setText(f"Clip {self.current_index}/{len(self.df)}, Audio Path: {current_row['audio_path']}")
            
            # Reset question type combo
            self.question_type_combo.setCurrentIndex(0)
            
            # Play audio
            self.play_audio()
            
    def update_label(self):
        selected_type = self.question_type_combo.currentText()
        if selected_type != "Select Type":
            self.current_label.setText(f"Current Label: {selected_type}")
            self.next_clip()
            

    def next_clip(self):
        # Save current annotation
        self.save_current_annotation()
        
        # Move to next clip
        if self.current_index < len(self.df) - 1:
            self.current_index += 1
            self.load_clip()

    def previous_clip(self):
        # Save current annotation
        self.save_current_annotation()
        
        # Move to previous clip
        if self.current_index > 0:
            self.current_index -= 1
            self.load_clip()

    def save_current_annotation(self):
        # Check if a type is selected
        # Check if a type is selected
        selected_type = self.question_type_combo.currentText()
        if selected_type != "Select Type":
            # Get current row index
            idx = self.current_index
            
            # Update the DataFrame directly
            self.df.at[idx, 'label'] = selected_type
            
            # Also update self.annotations (optional, if you still want a dict)
            audio_path = self.df.iloc[idx]['audio_path']
            self.annotations[audio_path] = selected_type

    def save_annotations(self):
        
        # save the current annotation
        self.save_current_annotation()
        # Open a file dialog to get the save location
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 
                                                "Save Annotations", 
                                                "atc_audio_annotations.csv",  # Default file name
                                                "CSV Files (*.csv);;All Files (*)", 
                                                options=options)
        
        # Check if the user selected a file
        if file_name:
            # Convert annotations to DataFrame
            annotation_df = pd.DataFrame.from_dict(self.annotations, orient='index', columns=['question_type'])
            
            annotation_df.index.name = 'audio_path'  # Ensure 'audio_path' is the index
            annotation_df.reset_index(inplace=True)

            # Save to the selected file
            annotation_df.to_csv(file_name, index=False)
            
            QMessageBox.information(self, 'Success', f'Annotations saved successfully to {file_name}!')

def main(csv_path, audio_directory, starting_index):
    app = QApplication(sys.argv)
    ex = ATCAnnotationGUI(csv_path, audio_directory, starting_index)
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Replace with your actual paths
    csv_path = sys.argv[1]
    starting_index = int(sys.argv[2])
    audio_directory = "audio_files"
    main(csv_path, audio_directory, starting_index)