import numpy as np

class HealthChatbot:
    """A simplified healthcare chatbot using rule-based logic"""
    
    def __init__(self):
        self.symptom_names = ["Fever", "Cough", "Sneezing", "Fatigue", "Loss of Taste", "Itchy Eyes"]
        self.diseases = ["Flu", "Cold", "COVID-19", "Allergy"]
        self.symptom_disease_map = {
            "Fever": ["Flu", "COVID-19"],
            "Cough": ["Flu", "Cold", "COVID-19"],
            "Sneezing": ["Cold", "Allergy"],
            "Fatigue": ["Flu", "COVID-19"],
            "Loss of Taste": ["COVID-19"],
            "Itchy Eyes": ["Allergy"]
        }
        self.test_map = {
            "Flu": "Influenza A/B test",
            "Cold": "Nasal swab",
            "COVID-19": "PCR test",
            "Allergy": "Allergy skin test"
        }
        self.medicine_map = {
            "Flu": "Oseltamivir (Tamiflu)",
            "Cold": "Rest, fluids, antihistamines",
            "COVID-19": "Isolation + Paracetamol",
            "Allergy": "Loratadine or Cetirizine"
        }
    
    def get_diagnosis(self, symptoms_dict):
        """Simple rule-based diagnosis"""
        # Count symptoms for each disease
        disease_scores = {disease: 0 for disease in self.diseases}
        
        for symptom, has_symptom in symptoms_dict.items():
            if has_symptom == 1 and symptom in self.symptom_disease_map:
                for disease in self.symptom_disease_map[symptom]:
                    disease_scores[disease] += 1
        
        # Find the disease with highest score
        max_score = 0
        diagnosis = "Cold"  # Default diagnosis
        
        for disease, score in disease_scores.items():
            if score > max_score:
                max_score = score
                diagnosis = disease
        
        # Calculate confidence (simplified)
        total_symptoms = sum(symptoms_dict.values())
        confidence = 0.5  # Base confidence
        if total_symptoms > 0:
            confidence = min(0.9, 0.5 + (max_score / total_symptoms) * 0.4)
        
        return {
            "diagnosis": diagnosis,
            "test": self.test_map.get(diagnosis, "Consult your doctor"),
            "medicine": self.medicine_map.get(diagnosis, "Consult your doctor"),
            "results": [
                {"name": d, "probability": 0.8 if d == diagnosis else 0.2, "uncertainty": 0.1} 
                for d in self.diseases
            ],
            "confidence": confidence,
            "uncertainty": 0.1
        }


class DiagnosticAssistant:
    """Placeholder for existing diagnostic assistant"""
    
    def __init__(self):
        pass
        
    def diagnose(self, symptoms):
        return {"diagnosis": "Sample diagnosis", "confidence": 0.8}