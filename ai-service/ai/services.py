import numpy as np
from sklearn.ensemble import RandomForestClassifier
import json
import os

class DiagnosticAssistant:
    """Simplified diagnostic assistant using a mock classifier"""
    
    def __init__(self):
        """Initialize with a simple model or load a pre-trained one"""
        # In a real implementation, you would load a trained model
        self.classifier = RandomForestClassifier(n_estimators=10)
        self._mock_train()
        
    def _mock_train(self):
        """Mock training on symptom data"""
        # This is simplified mock data
        X = np.random.rand(100, 20)  # 20 features representing symptoms
        y = np.random.randint(0, 10, 100)  # 10 different diagnoses
        self.classifier.fit(X, y)
        
        # Load ICD-10 codes for demonstration
        self.icd10_codes = {
            0: {"code": "J06.9", "name": "Acute upper respiratory infection"},
            1: {"code": "J02.9", "name": "Acute pharyngitis"},
            2: {"code": "J01.9", "name": "Acute sinusitis"},
            3: {"code": "J18.9", "name": "Pneumonia, unspecified"},
            4: {"code": "I10", "name": "Essential (primary) hypertension"},
            5: {"code": "E11.9", "name": "Type 2 diabetes mellitus without complications"},
            6: {"code": "M54.5", "name": "Low back pain"},
            7: {"code": "R51", "name": "Headache"},
            8: {"code": "K29.7", "name": "Gastritis, unspecified"},
            9: {"code": "R10.4", "name": "Other and unspecified abdominal pain"}
        }
    
    def analyze_symptoms(self, symptoms, patient_data=None):
        """
        Analyze symptoms and return possible diagnoses
        
        Args:
            symptoms (list): List of symptoms
            patient_data (dict): Patient demographic and history data
            
        Returns:
            dict: Diagnosis results with confidence scores
        """
        # Convert symptoms to feature vector (simplified)
        symptom_vector = self._process_symptoms(symptoms)
        
        # Get prediction probabilities
        proba = self.classifier.predict_proba(symptom_vector.reshape(1, -1))[0]
        
        # Sort by probability and get top 3
        top_indices = proba.argsort()[-3:][::-1]
        top_probas = proba[top_indices]
        
        # Format results
        diagnoses = []
        for i, idx in enumerate(top_indices):
            diagnoses.append({
                "icd_code": self.icd10_codes[idx]["code"],
                "name": self.icd10_codes[idx]["name"],
                "confidence": float(top_probas[i])
            })
        
        return {
            "diagnoses": diagnoses,
            "processing_time": "0.5 seconds"
        }
    
    def _process_symptoms(self, symptoms):
        """
        Process symptoms into a feature vector
        In a real implementation, this would use NLP and medical ontologies
        """
        # For demo, just create a random vector with a seed based on symptoms
        # to ensure consistent results for the same input
        seed = sum(hash(s) % 10000 for s in symptoms)
        np.random.seed(seed)
        return np.random.rand(20)  # 20 features