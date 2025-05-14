import numpy as np
import tensorflow as tf
import joblib
import os
import json
import re

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
    """AI-based diagnostic assistant implementation"""
    
    def __init__(self):
        # Define symptom to index mapping for our model
        self.symptom_map = {
            "fever": 0, "cough": 1, "fatigue": 2, "difficulty breathing": 3, 
            "sore throat": 4, "runny nose": 5, "headache": 6, "body aches": 7,
            "nausea": 8, "vomiting": 9, "diarrhea": 10, "chills": 11,
            "loss of taste": 12, "loss of smell": 13, "congestion": 14,
            "chest pain": 15, "abdominal pain": 16, "joint pain": 17,
            "rash": 18, "dizziness": 19
        }
        
        # Define diagnoses with their ICD codes
        self.diagnoses = [
            {"name": "Common Cold", "icd_code": "J00"},
            {"name": "Influenza", "icd_code": "J10.1"},
            {"name": "COVID-19", "icd_code": "U07.1"},
            {"name": "Acute Bronchitis", "icd_code": "J20.9"},
            {"name": "Pneumonia", "icd_code": "J18.9"},
            {"name": "Strep Throat", "icd_code": "J02.0"},
            {"name": "Gastroenteritis", "icd_code": "A09"},
            {"name": "Migraine", "icd_code": "G43.9"},
            {"name": "Urinary Tract Infection", "icd_code": "N39.0"},
            {"name": "Allergic Rhinitis", "icd_code": "J30.9"}
        ]
        
    def preprocess_symptoms(self, symptoms):
        """Convert symptom text to feature vector"""
        # Initialize feature vector with all zeros
        feature_vector = np.zeros(len(self.symptom_map))
        
        # Process each symptom
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            # Find closest match in our symptom map
            for known_symptom in self.symptom_map:
                if known_symptom in symptom_lower:
                    feature_vector[self.symptom_map[known_symptom]] = 1
                    break
        
        return feature_vector
        
    def diagnose(self, symptoms):
        """Generate diagnosis based on provided symptoms"""
        if not symptoms:
            return {"diagnoses": []}
            
        # Convert symptoms to feature vector
        feature_vector = self.preprocess_symptoms(symptoms)
        
        # Use a simple rules-based approach until full ML model is implemented
        # Count number of active symptoms
        symptom_count = np.sum(feature_vector)
        
        # Generate confidence scores for different conditions
        scores = []
        
        # Respiratory symptoms: indices 0, 1, 3, 4, 5, 14
        respiratory = feature_vector[0] + feature_vector[1] + feature_vector[3] + feature_vector[4] + feature_vector[5] + feature_vector[14]
        
        # Digestive symptoms: indices 8, 9, 10, 16
        digestive = feature_vector[8] + feature_vector[9] + feature_vector[10] + feature_vector[16]
        
        # Neurological: indices 6, 12, 13, 19
        neurological = feature_vector[6] + feature_vector[12] + feature_vector[13] + feature_vector[19]
        
        # Cold/flu: high in respiratory, may have fever (0) and body aches (7)
        cold_flu_score = (respiratory / 6) * 0.7 + (feature_vector[0] + feature_vector[7]) / 2 * 0.3
        
        # Gastroenteritis: high in digestive
        gastro_score = digestive / 4
        
        # COVID: respiratory + loss of taste/smell
        covid_score = (respiratory / 6) * 0.5 + (feature_vector[12] + feature_vector[13]) * 0.25 + feature_vector[0] * 0.25
        
        # Generate dynamic results
        results = []
        
        if respiratory > 2:
            confidence = min(0.9, respiratory / 6 * 0.9 + np.random.uniform(0, 0.1))
            
            if feature_vector[12] > 0 or feature_vector[13] > 0:
                # Loss of taste/smell suggests COVID
                results.append({
                    "name": "COVID-19", 
                    "icd_code": "U07.1",
                    "confidence": min(0.95, covid_score + np.random.uniform(0, 0.1))
                })
            
            if feature_vector[0] > 0 and feature_vector[7] > 0:
                # Fever and body aches suggest flu
                results.append({
                    "name": "Influenza", 
                    "icd_code": "J10.1",
                    "confidence": min(0.9, cold_flu_score + np.random.uniform(0, 0.1))
                })
            
            # Add common cold
            results.append({
                "name": "Common Cold", 
                "icd_code": "J00",
                "confidence": min(0.8, (respiratory - 1) / 6 * 0.8 + np.random.uniform(0, 0.1))
            })
            
            if feature_vector[3] > 0 and feature_vector[15] > 0:
                # Difficulty breathing and chest pain suggest pneumonia
                results.append({
                    "name": "Pneumonia", 
                    "icd_code": "J18.9",
                    "confidence": min(0.85, 0.7 + np.random.uniform(0, 0.15))
                })
            
        if digestive > 2:
            results.append({
                "name": "Gastroenteritis", 
                "icd_code": "A09",
                "confidence": min(0.85, gastro_score * 0.8 + np.random.uniform(0, 0.1))
            })
            
        if feature_vector[4] > 0 and feature_vector[0] > 0:
            results.append({
                "name": "Strep Throat", 
                "icd_code": "J02.0",
                "confidence": min(0.7, 0.5 + np.random.uniform(0, 0.2))
            })
            
        if feature_vector[6] > 0:
            results.append({
                "name": "Migraine", 
                "icd_code": "G43.9",
                "confidence": min(0.6, 0.4 + np.random.uniform(0, 0.2))
            })
            
        # If no results or too few symptoms, add some general possibilities
        if len(results) < 2 or symptom_count < 2:
            results = [
                {
                    "name": "Common Cold", 
                    "icd_code": "J00",
                    "confidence": 0.6 + np.random.uniform(0, 0.2)
                },
                {
                    "name": "Seasonal Allergies", 
                    "icd_code": "J30.9",
                    "confidence": 0.4 + np.random.uniform(0, 0.15)
                }
            ]
        
        # Sort results by confidence
        results.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Return diagnoses with confidence levels
        return {"diagnoses": results[:5]}  # Limit to top 5 diagnoses