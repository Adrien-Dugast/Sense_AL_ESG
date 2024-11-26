import nltk
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from nltk.tokenize import sent_tokenize
from collections import Counter

# Download the necessary tokenizer models
nltk.download('punkt')

class Classifier:
    def __init__(self, model_name: str):
        """
        Initialize the Classifier with a Hugging Face model and tokenizer.
        Args:
            model_name (str): The Hugging Face model name or path.
        """
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.pipe_env = pipeline(
            "text-classification", 
            model=self.model, 
            tokenizer=self.tokenizer
        )

    def segment_text(self, text: str) -> list:
        """
        Segment a text into sentences using nltk's sent_tokenize.
        Args:
            text (str): The text to segment.
        Returns:
            list: A list of sentences.
        """
        # Split text into sentences
        sentences = sent_tokenize(text)
        return sentences

    def classify_sentences(self, sentences: list) -> list:
        """
        Classify each sentence using the text-classification pipeline.
        Args:
            sentences (list): List of sentences to classify.
        Returns:
            list: List of classification results for each sentence.
        """
        classifications = self.pipe_env(sentences, padding=True, truncation=True, batch_size=16)
        return classifications

    def find_major_class(self, classifications: list) -> str:
        """
        Find the major class from a list of classification results.
        Args:
            classifications (list): A list of classification results, 
                                     each being a dictionary with 'label' and 'score'.
        Returns:
            str: The label of the major class.
        """
        labels = [classification['label'] for classification in classifications]
        most_common_label = Counter(labels).most_common(1)
        #print(most_common_label)
        return "ESG" if most_common_label[0][0] in ["Environmental", "Social", "Governance"] else None


    def classify_document(self, text: str) -> str:
        """
        Classify the document as a whole based on the majority class of its sentences.
        Args:
            text (str): The input text/document.
        Returns:
            str: The overall class of the document.
        """
        sentences = self.segment_text(text)
        classifications = self.classify_sentences(sentences)
        return self.find_major_class(classifications)


if __name__ == "__main__":
    with open("../data/test_article.txt", "r", encoding="utf-8") as file:
        text = file.read()

    model_name = "yiyanghkust/finbert-esg"

    # Initialize the Classifier
    classifier = Classifier(model_name)
    major_class = classifier.classify_document(text)
    print("Document Class:", major_class)



