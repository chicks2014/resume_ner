from text_extract import text_extracter as te
from text_preprocessing import text_preprocess as tp

class prediction_pipeline:
    def __init__(self):
        self.resume_source = r"..\resumes\prediction\01_resume_source"
        self.resume_extracted = r"..\resumes\prediction\02_resume_extracted"
        self.resume_cleaned = r"..\resumes\prediction\04_resume_cleaned"
        self.resume_not_extracted = r"..\resumes\prediction\03_resume_not_extracted"
        self.resume_cleaned_folder_path = r"..\resumes\prediction\04_resume_cleaned"
        self.pre_processed_folder_path = r"..\resumes\prediction\05_resume_pre_processed\"


    def predict(self):
        text_extr = te.text_extracter(self.resume_source, self.resume_extracted, self.resume_cleaned, self.resume_not_extracted)

        text_extr.text_extraction()
        text_extr.text_cleaning()

        text_prep = tp.text_preprocess(self.resume_cleaned_folder_path, self.pre_processed_folder_path)
        text_prep.preprocess_text()

