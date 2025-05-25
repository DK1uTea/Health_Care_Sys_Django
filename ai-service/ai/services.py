import numpy as np
import tensorflow as tf
import joblib
import os
import json
import re

class HealthChatbot:
    """An enhanced healthcare chatbot using NLP techniques"""
    
    def __init__(self):
        # Load comprehensive symptom data from files
        self.symptom_names = ["Fever", "Cough", "Sneezing", "Fatigue", "Loss of Taste", "Itchy Eyes", 
                             "Headache", "Sore Throat", "Runny Nose", "Shortness of Breath", 
                             "Muscle Pain", "Joint Pain", "Rash", "Chest Pain", "Nausea",
                             "Vomiting", "Diarrhea", "Dizziness", "Confusion"]
        
        self.diseases = ["Flu", "Cold", "COVID-19", "Allergy", "Bronchitis", "Pneumonia", 
                        "Strep Throat", "Sinusitis", "Migraine", "Asthma", "Gastroenteritis"]
        
        # Extended symptom-disease mapping
        self.symptom_disease_map = {
            "Fever": ["Flu", "COVID-19", "Strep Throat", "Pneumonia"],
            "Cough": ["Flu", "Cold", "COVID-19", "Bronchitis", "Pneumonia"],
            "Sneezing": ["Cold", "Allergy", "Sinusitis"],
            "Fatigue": ["Flu", "COVID-19", "Pneumonia"],
            "Loss of Taste": ["COVID-19"],
            "Itchy Eyes": ["Allergy"],
            "Headache": ["Flu", "Cold", "Sinusitis", "Migraine"],
            "Sore Throat": ["Flu", "Cold", "Strep Throat"],
            "Runny Nose": ["Cold", "Allergy", "Sinusitis"],
            "Shortness of Breath": ["COVID-19", "Pneumonia", "Asthma"],
            "Muscle Pain": ["Flu", "COVID-19"],
            "Joint Pain": ["Flu"],
            "Rash": ["Allergy"],
            "Chest Pain": ["Pneumonia", "Asthma"],
            "Nausea": ["Gastroenteritis", "Migraine"],
            "Vomiting": ["Gastroenteritis"],
            "Diarrhea": ["Gastroenteritis", "COVID-19"],
            "Dizziness": ["Migraine"],
            "Confusion": ["Pneumonia"]
        }
        
        # Extended keyword detection for natural language
        self.symptom_keywords = {
            "Fever": ["fever", "high temperature", "hot", "burning up", "temperature", "feverish"],
            "Cough": ["cough", "coughing", "hacking", "dry cough", "wet cough", "phlegm", "mucus"],
            "Sneezing": ["sneeze", "sneezing", "achoo", "runny nose", "stuffy nose"],
            "Fatigue": ["tired", "fatigue", "exhausted", "no energy", "weakness", "lethargic", "weak"],
            "Loss of Taste": ["can't taste", "lost taste", "food tastes bland", "no taste", "taste gone"],
            "Itchy Eyes": ["itchy eyes", "eye irritation", "rubbing eyes", "scratchy eyes"],
            "Headache": ["headache", "head hurts", "migraine", "throbbing head", "head pain"],
            "Sore Throat": ["sore throat", "throat pain", "painful throat", "trouble swallowing"],
            "Runny Nose": ["runny nose", "drippy nose", "nasal congestion", "stuffy nose", "blocked nose"],
            "Shortness of Breath": ["shortness of breath", "hard to breathe", "can't breathe", "breathing trouble", "out of breath"],
            "Muscle Pain": ["muscle pain", "body ache", "sore muscles", "aching body"],
            "Joint Pain": ["joint pain", "achy joints", "painful joints", "arthritis"],
            "Rash": ["rash", "skin irritation", "itchy skin", "bumps", "hives", "red skin"],
            "Chest Pain": ["chest pain", "pain in chest", "chest discomfort", "chest tightness"],
            "Nausea": ["nausea", "feel sick", "queasy", "upset stomach"],
            "Vomiting": ["vomiting", "throwing up", "puking", "getting sick"],
            "Diarrhea": ["diarrhea", "loose stool", "frequent bowel movements", "watery stool"],
            "Dizziness": ["dizzy", "dizziness", "lightheaded", "vertigo", "room spinning"],
            "Confusion": ["confused", "confusion", "disoriented", "can't think straight"]
        }

        self.disease_info = {
        "Flu": {
            "description": "Influenza (flu) is a contagious respiratory illness caused by influenza viruses that infect the nose, throat, and lungs. It can cause mild to severe illness, and sometimes can lead to death.",
            "symptoms": "Common symptoms include fever, cough, sore throat, body aches, headache, chills, fatigue, and sometimes diarrhea and vomiting.",
            "transmission": "The flu spreads mainly by droplets made when infected people cough, sneeze or talk.",
            "risk_groups": "People at higher risk include the elderly, young children, pregnant women, and those with certain health conditions.",
            "prevention": "Annual vaccination is the best way to prevent the flu. Also practice good hygiene like handwashing and avoiding close contact with sick people.",
            "when_to_see_doctor": "See a doctor if you have difficulty breathing, persistent chest pain, sudden dizziness, confusion, severe vomiting, or if your symptoms improve but then return with fever and worse cough."
        },
        "Cold": {
            "description": "The common cold is a viral infection of the upper respiratory tract, including the nose and throat. Many types of viruses can cause a common cold.",
            "symptoms": "Symptoms typically include runny or stuffy nose, sore throat, cough, congestion, mild headache, sneezing, and low-grade fever.",
            "transmission": "Colds spread through air droplets when someone with the virus coughs, sneezes or talks, and through hand-to-hand contact.",
            "risk_groups": "Children, elderly, and those with weakened immune systems are more susceptible.",
            "prevention": "Wash hands frequently, avoid touching your face, and stay away from people who are sick.",
            "when_to_see_doctor": "See a doctor if symptoms last more than 10 days, you have a high fever, or you have severe sinus pain."
        },
        "COVID-19": {
            "description": "COVID-19 is a respiratory disease caused by the SARS-CoV-2 virus. It can range from mild to severe, and some cases can be fatal.",
            "symptoms": "Common symptoms include fever, dry cough, fatigue, loss of taste or smell, shortness of breath, body aches, and in some cases, gastrointestinal symptoms.",
            "transmission": "COVID-19 spreads primarily through respiratory droplets when an infected person coughs, sneezes, or talks.",
            "risk_groups": "Older adults and people with underlying medical conditions like heart disease, diabetes, and obesity are at higher risk.",
            "prevention": "Get vaccinated, wear masks in public settings, practice social distancing, and wash hands frequently.",
            "when_to_see_doctor": "Seek emergency medical care if you have trouble breathing, persistent chest pain or pressure, confusion, inability to wake or stay awake, or bluish lips or face."
        },
        "Allergy": {
            "description": "Allergies occur when your immune system reacts to a foreign substance that doesn't cause a reaction in most people.",
            "symptoms": "Symptoms depend on the allergen but often include sneezing, itchy or watery eyes, runny nose, rash, or hives.",
            "transmission": "Allergies are not contagious but can be hereditary.",
            "risk_groups": "People with a family history of allergies are more likely to develop allergic disease.",
            "prevention": "Avoid known allergens, keep windows closed during high pollen seasons, use air purifiers, and take allergy medications preventatively.",
            "when_to_see_doctor": "See a doctor if over-the-counter medications don't help, or if you experience severe symptoms like trouble breathing or swallowing."
        }
    }

    # Add detailed medicine information
        self.medicine_details = {
            "Flu": {
                "prescription": ["Oseltamivir (Tamiflu)", "Zanamivir (Relenza)", "Baloxavir marboxil (Xofluza)"],
                "over_the_counter": ["Acetaminophen (Tylenol)", "Ibuprofen (Advil, Motrin)", "Decongestants", "Cough suppressants"],
                "dosage_notes": "Antiviral drugs work best when started within 48 hours of getting sick. Always follow the prescribed dosage.",
                "side_effects": "Common side effects of antivirals may include nausea and vomiting. OTC medications may cause drowsiness or stomach upset.",
                "warnings": "Aspirin should not be given to children or teenagers with viral illnesses due to risk of Reye's syndrome."
            },
            "Cold": {
                "prescription": [],
                "over_the_counter": ["Decongestants", "Antihistamines", "Pain relievers (Acetaminophen, Ibuprofen)", "Cough suppressants"],
                "dosage_notes": "Follow package instructions. Don't take decongestants for more than 3 days.",
                "side_effects": "Drowsiness, dry mouth, dizziness depending on medication.",
                "warnings": "Avoid combining multiple medications with the same active ingredients."
            },
            "COVID-19": {
                "prescription": ["Paxlovid", "Remdesivir", "Monoclonal antibody treatments"],
                "over_the_counter": ["Acetaminophen (Tylenol)", "Ibuprofen (Advil)", "Cough suppressants"],
                "dosage_notes": "Take medications as directed. Antiviral treatments must be started within 5 days of symptom onset to be effective.",
                "side_effects": "Varies by medication; Paxlovid may cause altered taste, diarrhea, high blood pressure, muscle aches.",
                "warnings": "Many COVID-19 medications have interactions with other drugs. Inform your doctor of all medications you take."
            },
            "Allergy": {
                "prescription": ["Steroid nasal sprays", "Leukotriene modifiers", "Immunotherapy (allergy shots)"],
                "over_the_counter": ["Antihistamines (Zyrtec, Claritin, Allegra)", "Decongestants", "Nasal sprays (Flonase, Nasacort)"],
                "dosage_notes": "Many allergy medications work best when taken regularly throughout allergy season, not just when symptoms appear.",
                "side_effects": "Drowsiness (with some antihistamines), dry mouth, headache, nervousness (with decongestants).",
                "warnings": "Decongestant nasal sprays should not be used for more than 3 days to avoid rebound congestion."
            }
        }
        
        # Test and medicine recommendations
        self.test_map = {
            "Flu": "rapid influenza diagnostic test (RIDT)",
            "Cold": "no specific test needed, but a throat swab may rule out strep",
            "COVID-19": "PCR or rapid antigen test",
            "Allergy": "allergy skin test or blood test",
            "Bronchitis": "chest X-ray to rule out pneumonia",
            "Pneumonia": "chest X-ray and blood tests",
            "Strep Throat": "rapid strep test or throat culture",
            "Sinusitis": "nasal endoscopy or CT scan for chronic cases",
            "Migraine": "neurological examination (diagnosis is clinical)",
            "Asthma": "pulmonary function test (spirometry)",
            "Gastroenteritis": "stool sample test for severe cases"
        }
        
        self.medicine_map = {
            "Flu": "antiviral medications like oseltamivir (Tamiflu), rest, and fluids",
            "Cold": "over-the-counter decongestants, antihistamines, and pain relievers",
            "COVID-19": "rest, fluids, and antipyretics for mild cases; consult doctor for treatments like Paxlovid for higher-risk patients",
            "Allergy": "antihistamines, nasal corticosteroids, or decongestants",
            "Bronchitis": "rest, increased fluid intake, and possibly bronchodilators",
            "Pneumonia": "antibiotics for bacterial pneumonia, rest, and increased fluids",
            "Strep Throat": "antibiotics, usually penicillin or amoxicillin",
            "Sinusitis": "nasal corticosteroids, decongestants, and antibiotics for bacterial cases",
            "Migraine": "pain relievers, triptans, or anti-nausea medications",
            "Asthma": "short-acting beta agonists and inhaled corticosteroids",
            "Gastroenteritis": "oral rehydration solutions and anti-diarrheal medications for some cases"
        }
        
        # Store conversation state
        self.conversation_state = {}  # Store conversation state by session
    
    def process_message(self, message, session_id=None):
        """Process a message from the user and generate a response"""
        if not session_id:
            session_id = "default"
            
        # Initialize session if needed
        if session_id not in self.conversation_state:
            self.conversation_state[session_id] = {
                "detected_symptoms": {},
                "confirmed_symptoms": {},
                "current_question": None,
                "diagnosis_complete": False,
                "previous_messages": [],
                "follow_up_question": None,
                "severity_check": False
            }
            
        state = self.conversation_state[session_id]
        state["previous_messages"].append({"user": message})
        
        # Check if we're waiting for a specific follow-up answer
        if state["follow_up_question"] == "severity":
            severity = self._extract_severity(message)
            if severity:
                state["severity"] = severity
                state["follow_up_question"] = None
                
                # If we have enough symptoms for diagnosis, proceed
                if len(state["confirmed_symptoms"]) >= 2:
                    return self._generate_diagnosis(state)
                else:
                    return {
                        "message": "Thank you. Any other symptoms you're experiencing?",
                        "detected_symptoms": state["confirmed_symptoms"]
                    }
            else:
                state["follow_up_question"] = None  # Reset if we couldn't understand
        
        # Check if we're in the middle of a symptom confirmation
        if state["current_question"]:
            symptom = state["current_question"]
            if self._is_affirmative(message):
                state["confirmed_symptoms"][symptom] = 1
                state["current_question"] = None
                
                # Ask about symptom severity
                state["follow_up_question"] = "severity"
                return {
                    "message": f"I've recorded that you have {symptom.lower()}. How severe is it on a scale of 1-10?",
                    "detected_symptoms": state["confirmed_symptoms"]
                }
            elif self._is_negative(message):
                state["confirmed_symptoms"][symptom] = 0
                state["current_question"] = None
                return {
                    "message": f"I've noted that you don't have {symptom.lower()}. Any other symptoms?",
                    "detected_symptoms": state["confirmed_symptoms"]
                }
        
        # Detect symptoms in the message
        detected = self._detect_symptoms_in_text(message)
        
        if detected:
            # Update detected symptoms
            for symptom in detected:
                state["detected_symptoms"][symptom] = 1
                state["confirmed_symptoms"][symptom] = 1  # Auto-confirm for a better user experience
        
            # Provide detailed information for detected symptoms
            primary_symptom = detected[0]
            related_diseases = self.symptom_disease_map.get(primary_symptom, [])
            
            if related_diseases:
                main_disease = related_diseases[0]
                diagnosis = {
                    "diagnosis": main_disease,
                    "confidence": 0.6,  # Lower confidence with just one symptom
                    "test": self.test_map.get(main_disease, "a medical evaluation"),
                    "medicine": self.medicine_map.get(main_disease, "treatment based on severity")
                }
                
                # Get disease and medicine details
                disease_details = self.disease_info.get(main_disease, {})
                medicine_details = self.medicine_details.get(main_disease, {})
                
                # Build a comprehensive response
                response_message = f"Based on your mention of {primary_symptom.lower()}, you might have {main_disease}. Here's some information:\n\n"
                
                if disease_details:
                    response_message += f"**About {main_disease}**\n{disease_details.get('description', '')}\n\n"
                    response_message += f"**Common Symptoms**\n{disease_details.get('symptoms', '')}\n\n"
                
                response_message += f"**Recommended Testing**\nI recommend {self.test_map.get(main_disease, 'consulting with a healthcare provider')}.\n\n"
                response_message += f"**Treatment Options**\n{self.medicine_map.get(main_disease, 'Consult with a healthcare provider for appropriate treatment.')}\n\n"
                
                if medicine_details:
                    if medicine_details.get('prescription'):
                        response_message += f"**Prescription medications** that may be recommended include: {', '.join(medicine_details['prescription'])}\n\n"
                        
                    if medicine_details.get('over_the_counter'):
                        response_message += f"**Over-the-counter options** include: {', '.join(medicine_details['over_the_counter'])}\n\n"
                
                    if medicine_details.get('dosage_notes'):
                        response_message += f"**Dosage notes**: {medicine_details['dosage_notes']}\n\n"
                
                response_message += "\nDo you have any other symptoms? Providing more information will help me give a more accurate assessment."
                
                # Create response with detailed info
                return {
                    "message": response_message,
                    "detected_symptoms": state["detected_symptoms"],
                    "diagnosis": {
                        "diagnosis": main_disease,
                        "confidence": 0.6,
                        "test": self.test_map.get(main_disease, ""),
                        "medicine": self.medicine_map.get(main_disease, ""),
                        "detailed_info": {
                            "description": disease_details.get('description', ''),
                            "symptoms": disease_details.get('symptoms', ''),
                            "risk_groups": disease_details.get('risk_groups', ''),
                            "prevention": disease_details.get('prevention', ''),
                            "when_to_see_doctor": disease_details.get('when_to_see_doctor', ''),
                            "prescription_meds": medicine_details.get('prescription', []),
                            "otc_meds": medicine_details.get('over_the_counter', []),
                            "dosage_notes": medicine_details.get('dosage_notes', ''),
                            "side_effects": medicine_details.get('side_effects', '')
                        }
                    }
                }
            
            # If we can't find related diseases, fall back to the original behavior
            symptom_to_confirm = detected[0]
            state["current_question"] = symptom_to_confirm
            
            return {
                "message": f"It sounds like you might have {symptom_to_confirm.lower()}. Is that correct?",
                "detected_symptoms": state["detected_symptoms"]
            }
        
        # If enough symptoms are confirmed, make a diagnosis
        if len(state["confirmed_symptoms"]) >= 2 and not state["diagnosis_complete"]:
            return self._generate_diagnosis(state)
        
        # Check for urgency/emergency patterns
        if self._is_emergency(message):
            return {
                "message": "Your symptoms sound serious. Please seek immediate medical attention or call emergency services.",
                "is_emergency": True,
                "detected_symptoms": state["confirmed_symptoms"]
            }
            
        # Default responses if no specific condition is met
        return {
            "message": self._get_default_response(message),
            "detected_symptoms": state["confirmed_symptoms"]
        }
    
    def _detect_symptoms_in_text(self, text):
        """Detect symptoms mentioned in the text"""
        text = text.lower()
        detected_symptoms = []
        
        for symptom, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    detected_symptoms.append(symptom)
                    break
                    
        return detected_symptoms
    
    def _is_affirmative(self, text):
        """Check if the message is affirmative"""
        text = text.lower()
        affirmatives = ["yes", "yeah", "yep", "correct", "right", "true", "sure", "definitely"]
        return any(word in text for word in affirmatives)
    
    def _is_negative(self, text):
        """Check if the message is negative"""
        text = text.lower()
        negatives = ["no", "nope", "not", "don't", "isn't", "wasn't", "haven't", "hasn't", "incorrect", "wrong"]
        return any(word in text for word in negatives)
    
    def _make_diagnosis(self, symptoms):
        """Generate a diagnosis based on symptoms"""
        # Count matches for each disease
        disease_matches = {disease: 0 for disease in self.diseases}
        
        for symptom, value in symptoms.items():
            if value == 1 and symptom in self.symptom_disease_map:
                for disease in self.symptom_disease_map[symptom]:
                    disease_matches[disease] += 1
        
        # Find the disease with the most matching symptoms
        best_match = max(disease_matches.items(), key=lambda x: x[1])
        disease = best_match[0]
        confidence = min(0.95, max(0.4, best_match[1] / len(symptoms)))
        
        return {
            "diagnosis": disease,
            "confidence": confidence,
            "test": self.test_map[disease],
            "medicine": self.medicine_map[disease]
        }
    
    def _get_default_response(self, message):
        """Generate a default response when no symptoms detected"""
        if "hello" in message.lower() or "hi" in message.lower():
            return "Hello! I'm your healthcare assistant. How are you feeling today?"
        elif "help" in message.lower():
            return "I can help you identify potential health conditions based on your symptoms. " + \
                   "Just tell me how you're feeling or what symptoms you're experiencing."
        elif "thank" in message.lower():
            return "You're welcome! Is there anything else I can help you with?"
        else:
            return "I'm not sure I understand. Could you tell me more about your symptoms?"

    def _extract_severity(self, text):
        """Extract severity level from text"""
        text = text.lower()
        # Look for numbers 1-10
        for i in range(1, 11):
            if str(i) in text:
                return i
            
        # Look for text-based severity
        if any(word in text for word in ["mild", "light", "slight", "minor"]):
            return 3
        elif any(word in text for word in ["moderate", "medium", "average"]):
            return 5
        elif any(word in text for word in ["severe", "bad", "serious", "heavy", "intense", "extreme"]):
            return 8
        
        return None

    def _is_emergency(self, text):
        """Check if the message describes an emergency situation"""
        emergency_keywords = [
            "can't breathe", "not breathing", "difficulty breathing", 
            "chest pain", "severe chest pain", "heart attack",
            "stroke", "collapsed", "unconscious", "passed out",
            "bleeding heavily", "severe bleeding", "coughing blood",
            "suicidal", "kill myself", "emergency"
        ]
        
        text = text.lower()
        return any(keyword in text for keyword in emergency_keywords)

    def _generate_diagnosis(self, state):
        """Generate a comprehensive diagnosis response"""
        diagnosis = self._make_diagnosis(state["confirmed_symptoms"])
        state["diagnosis_complete"] = True
        
        # Get severity factor
        severity_factor = state.get("severity", 5) / 5.0
        adjusted_confidence = min(0.95, diagnosis["confidence"] * severity_factor)
        diagnosis["confidence"] = adjusted_confidence
        
        disease = diagnosis["diagnosis"]
        disease_details = self.disease_info.get(disease, {})
        medicine_details = self.medicine_details.get(disease, {})
        
        # Prepare severity text
        severity_text = ""
        if "severity" in state:
            if state["severity"] <= 3:
                severity_text = " Your symptoms seem mild, which is good news. "
            elif state["severity"] <= 6:
                severity_text = " Your symptoms are of moderate severity. "
            else:
                severity_text = " Your symptoms seem quite severe. If they worsen, please consider seeking immediate medical attention. "
        
        # Build a comprehensive response
        response_message = f"Based on your symptoms, I think you might have {disease}.{severity_text}\n\n"
        
        # Add disease information
        if disease_details:
            response_message += f"**About {disease}**\n{disease_details.get('description', '')}\n\n"
            response_message += f"**Common Symptoms**\n{disease_details.get('symptoms', '')}\n\n"
            response_message += f"**Who is at risk**\n{disease_details.get('risk_groups', '')}\n\n"
        
        # Add testing information
        response_message += f"**Recommended Testing**\nI recommend getting a {diagnosis['test']} to confirm this diagnosis.\n\n"
        
        # Add treatment information
        response_message += f"**Treatment Options**\n{diagnosis['medicine']}\n\n"
        
        # Add detailed medicine information if available
        if medicine_details:
            if medicine_details.get('prescription'):
                response_message += f"**Prescription medications** that may be recommended include: {', '.join(medicine_details['prescription'])}\n\n"
                
            if medicine_details.get('over_the_counter'):
                response_message += f"**Over-the-counter options** include: {', '.join(medicine_details['over_the_counter'])}\n\n"
                
            if medicine_details.get('dosage_notes'):
                response_message += f"**Dosage notes**: {medicine_details['dosage_notes']}\n\n"
        
        # Add prevention tips
        if disease_details and disease_details.get('prevention'):
            response_message += f"**Prevention**\n{disease_details['prevention']}\n\n"
        
        # When to see a doctor
        if disease_details and disease_details.get('when_to_see_doctor'):
            response_message += f"**When to see a doctor**\n{disease_details['when_to_see_doctor']}\n\n"
        
        response_message += "Remember: This is not a professional medical diagnosis. Always consult with a healthcare professional for proper evaluation and treatment."
        
        # Add all the detailed info to the diagnosis object
        diagnosis["detailed_info"] = {
            "description": disease_details.get('description', ''),
            "symptoms": disease_details.get('symptoms', ''),
            "risk_groups": disease_details.get('risk_groups', ''),
            "prevention": disease_details.get('prevention', ''),
            "when_to_see_doctor": disease_details.get('when_to_see_doctor', ''),
            "prescription_meds": medicine_details.get('prescription', []),
            "otc_meds": medicine_details.get('over_the_counter', []),
            "dosage_notes": medicine_details.get('dosage_notes', ''),
            "side_effects": medicine_details.get('side_effects', '')
        }
        
        return {
            "message": response_message,
            "diagnosis": diagnosis,
            "detected_symptoms": state["confirmed_symptoms"]
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
        
        # Add detailed disease information
        self.disease_info = {
            "Flu": {
                "description": "Influenza (flu) is a contagious respiratory illness caused by influenza viruses that infect the nose, throat, and lungs. It can cause mild to severe illness, and sometimes can lead to death.",
                "symptoms": "Common symptoms include fever, cough, sore throat, body aches, headache, chills, fatigue, and sometimes diarrhea and vomiting.",
                "transmission": "The flu spreads mainly by droplets made when infected people cough, sneezes or talk.",
                "risk_groups": "People at higher risk include the elderly, young children, pregnant women, and those with certain health conditions.",
                "prevention": "Annual vaccination is the best way to prevent the flu. Also practice good hygiene like handwashing and avoiding close contact with sick people.",
                "when_to_see_doctor": "See a doctor if you have difficulty breathing, persistent chest pain, sudden dizziness, confusion, severe vomiting, or if your symptoms improve but then return with fever and worse cough."
            },
            "Cold": {
                "description": "The common cold is a viral infection of the upper respiratory tract, including the nose and throat. Many types of viruses can cause a common cold.",
                "symptoms": "Symptoms typically include runny or stuffy nose, sore throat, cough, congestion, mild headache, sneezing, and low-grade fever.",
                "transmission": "Colds spread through air droplets when someone with the virus coughs, sneezes or talks, and through hand-to-hand contact.",
                "risk_groups": "Children, elderly, and those with weakened immune systems are more susceptible.",
                "prevention": "Wash hands frequently, avoid touching your face, and stay away from people who are sick.",
                "when_to_see_doctor": "See a doctor if symptoms last more than 10 days, you have a high fever, or you have severe sinus pain."
            },
            "COVID-19": {
                "description": "COVID-19 is a respiratory disease caused by the SARS-CoV-2 virus. It can range from mild to severe, and some cases can be fatal.",
                "symptoms": "Common symptoms include fever, dry cough, fatigue, loss of taste or smell, shortness of breath, body aches, and in some cases, gastrointestinal symptoms.",
                "transmission": "COVID-19 spreads primarily through respiratory droplets when an infected person coughs, sneezes, or talks.",
                "risk_groups": "Older adults and people with underlying medical conditions like heart disease, diabetes, and obesity are at higher risk.",
                "prevention": "Get vaccinated, wear masks in public settings, practice social distancing, and wash hands frequently.",
                "when_to_see_doctor": "Seek emergency medical care if you have trouble breathing, persistent chest pain or pressure, confusion, inability to wake or stay awake, or bluish lips or face."
            },
            "Allergy": {
                "description": "Allergies occur when your immune system reacts to a foreign substance that doesn't cause a reaction in most people.",
                "symptoms": "Symptoms depend on the allergen but often include sneezing, itchy or watery eyes, runny nose, rash, or hives.",
                "transmission": "Allergies are not contagious but can be hereditary.",
                "risk_groups": "People with a family history of allergies are more likely to develop allergic disease.",
                "prevention": "Avoid known allergens, keep windows closed during high pollen seasons, use air purifiers, and take allergy medications preventatively.",
                "when_to_see_doctor": "See a doctor if over-the-counter medications don't help, or if you experience severe symptoms like trouble breathing or swallowing."
            },
            # Add entries for all other diseases in your system
        }

        # More detailed medicine information
        self.medicine_details = {
            "Flu": {
                "prescription": ["Oseltamivir (Tamiflu)", "Zanamivir (Relenza)", "Baloxavir marboxil (Xofluza)"],
                "over_the_counter": ["Acetaminophen (Tylenol)", "Ibuprofen (Advil, Motrin)", "Decongestants", "Cough suppressants"],
                "dosage_notes": "Antiviral drugs work best when started within 48 hours of getting sick. Always follow the prescribed dosage.",
                "side_effects": "Common side effects of antivirals may include nausea and vomiting. OTC medications may cause drowsiness or stomach upset.",
                "warnings": "Aspirin should not be given to children or teenagers with viral illnesses due to risk of Reye's syndrome."
            },
            # Add entries for all other diseases in your system
        }