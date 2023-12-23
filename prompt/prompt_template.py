system_prompt = """
Next, you will act as a professional CBT cognitive behavioral therapy psychologist. 
I will input the "psychological counseling dialogue" between the counselor and the patient. During the whole psychological counseling dialogue, you need to use the professional knowledge of CBT to detect whether there is any key information in the message, and then update the attributes of the given psychological template and reply to the patient."""

score_system_template = """
Next, you will act as a professional CBT cognitive behavioral therapy psychologist. 
I will input the pair of the counselor and the patient's dialogue. You need to use the professional knowledge of CBT to judge counselor's reply whether it is reasonable and healthy and score the conversation.
Only output whether the conversation is reasonable and healthy (True or False) and the score of the conversation. Split using "===".
-----
Example:
```
True
===
0.8
```
"""

guide_prompt = """
This is a template for tracking the mental health, treatment status, and progress of the therapist and patient during the treatment.

# Update guidelines:
When updating template attributes, please consider the process step by step:
1. Check for new content: Examine whether there is new content detected based on the original content. Special attention should be paid to Cognitive Structure Assessment and Intervention. 
2. No new content detected: If there is no new content detected and the attribute contains the original content, retain the original content for the attribute. If the attribute doesn't have the original content, output "unknown."
3. New content detected and summarize: If new content is detected, summarize the new content and original content. Then update the attribute using the summarized content.
4. Check whether all template attributes exist. If there are missing attributes, output "unknown" for the missing attributes. But don't omit any attributes.
5. Attention1: All attributes must be present and filled with "information content" or "original content" or "unknown"! Every attribute cannot be missing!
6. Attention2: You need to extract the key content of the conversation, and then detect whether the attributes need to be updated/appended based on the content of the context and template's attributes! Updates are not just appends, they are changes.
7. Attention3: Strictly follow the format of the template for output and strictly omit attributes or fields. 
8. Important: Output the updated template up to 1500 tokens. If it exceeds 1500 words, please summarize each attribute. For example, "Homework_Assignment" is too long, you can summarize it.
"""

# mental_template = """
# # CBT Psychological Template:
# ```markdown
# ## Personal Information
# - Name: {{name}}
# - Age: {{age}}
# - Gender: {{gender}}
# - Occupation: {{occupation}}
# - Marital Status: {{marital_status}}
#
# ## Risk Assessment
# - Self-harm Risk: {{self_harm_risk}}
# - Harm to Others Risk: {{harm_to_others_risk}}
# - Safety Plan: {{safety_plan}}
#
# ## Living Conditions
# - Sleep: {{sleep_patterns}}
# - Diet: {{eating_habits}}
# - Interpersonal Relationships: {{relationship_status}}
# - Daily Activities: {{activity_levels}}
# - Hobbies: {{hobbies}}
# - Engaged Interests/Motivations: {{engaged_interests}}
# - Stressors: {{stressors}}
#
# ## Cognitive Structure Assessment and Intervention
# - Emotion Recognition and Evaluation: {{emotion_recognition_and_evaluation}}
# - Automatic Thought Recognition and Evaluation: {{automatic_thought_recognition_and_evaluation}}
# - Intermediate Recognition and Correction: {{intermediate_recognition_and_correction}}
# - Core Belief Recognition and Correction: {{core_belief_recognition_and_correction}}
# - Cognitive Restructuring: {{cognitive_restructuring}}
#
# ## CBT Treatment Overview
# - Primary Complaint: {{primary_complaint}}
# - Diagnosis: {{diagnosis}}
# - Treatment Goals: {{treatment_goals}}
# ### Treatment Methods and Content
# - Mood Diary: {{mood_diary}}
# - Cognitive Triple Column Table: {{cognitive_triple_column_table}}
# - Worry List: {{worry_list}}
# - Questioning Technique: {{questioning_technique}}
# - Behavioral Experiment Method: {{behavioral_experiment_method}}
# - Exposure and Response Prevention: {{exposure_and_response_prevention}}
# - Relaxation Techniques: {{relaxation_techniques}}
# - Ask for negative feedback: {{negative_feedback}}
#
# ## CBT Treatment Process
# - Information Collection: {{information_collection}}
# - Agenda Setting: {{agenda_setting}}
# - Triggering Event:{{triggering_event}}
# - Cognitive Behavioral Pattern Analysis: {{cognitive_behavioral_pattern_analysis}}
# - Treatment Review: {{treatment_review}}
# - Treatment Evaluation: {{treatment_evaluation}}
# - Homework Assignment: {{homework_assignment}}
# - Next Session Plan: {{next_session_plan}}
# ```
# ```
# ## Personal Information: A catalog of fundamental patient details covering demographics and occupational information.
#
# ## Risk Assessment: An appraisal of the patient's potential for self-harm and harm to others, along with proposed safety measures.
#
# ## Living Conditions: A snapshot of the patient's daily environment, encompassing sleep quality, dietary habits, social interactions, routine activities, leisure pursuits, motivational aspects, and encountered stressors.
#
# ## Cognitive Structure Assessment and Intervention: An examination and modification approach targeting the patient's emotional interpretation, automatic thoughts, intermediate beliefs, core values, and overarching cognitive patterns.
#
# ## CBT Treatment Overview: A framework outlining the patient's primary issues, diagnostic conclusions, intended therapeutic outcomes, and a compendium of cognitive and behavioral techniques employed within treatment.
#
# ## CBT Treatment Process: A procedural outline detailing the collection of patient information, session agenda formulation, identification of precipitating events, analysis of cognitive-behavioral patterns, continuous assessment and review of treatment efficacy, after-session tasks, and future session strategies.
# ```
# # Please update the psychological template based on the psychological counseling dialogue below:
# Psychological counseling dialogue:
# ```
# {dialogue}
# ```
#
# Just output the updated Psychological template:
# """

# mental_template = """
# # Guidelines:
# {guide}
#
# # Schema:
# {schema}
#
# # CBT Psychological Template:
# {template}
#
# -----
# # Please update the psychological template based on the psychological counseling dialogue and Strictly adhere to the format of the Template
# ## Psychological counseling dialogue
# ```
# {dialogue}
# ```
#
# Just output the updated Psychological template, up to 1500 tokens:
# """

first_template = """
```
{
    "Personal_Information": {
      "Name": "{{name}}",
      "Age": "{{age}}",
      "Gender": "{{gender}}",
      "Occupation": "{{occupation}}",
      "Marital_Status": "{{marital_status}}"
    },
    "Living_Conditions": {
      "Sleep": "{{sleep_patterns}}",
      "Diet": "{{eating_habits}}",
      "Interpersonal_Relationships": "{{relationship_status}}",
      "Engaged_Interests_Motivations": "{{engaged_interests}}",
      "Self_harm_Risk": "{{self_harm_risk}}",
    },
    "Cognitive_Structure_Assessment_and_Intervention": {
      "Emotion_Recognition_and_Evaluation": "{{emotion_recognition_and_evaluation}}",
      "Automatic_Thought_Recognition_and_Evaluation": "{{automatic_thought_recognition_and_evaluation}}",
      "Intermediate_Recognition_and_Correction": "{{intermediate_recognition_and_correction}}",
      "Core_Belief_Recognition_and_Correction": "{{core_belief_recognition_and_correction}}",
      "Cognitive_Restructuring": "{{cognitive_restructuring}}"
    },
    "CBT_Treatment_Overview": {
      "Primary_Complaint": "{{primary_complaint}}",
      "Diagnosis": "{{diagnosis}}",
      "Treatment_Goals": "{{treatment_goals}}",
      "Treatment_Methods_and_Content": "{{treatment_methods_and_content}}"
    },
    "CBT_Treatment_Process": {
      "Agenda_Setting": "{{agenda_setting}}",
      "Triggering_Event": "{{triggering_event}}",
      "Cognitive_Behavioral_Pattern_Analysis": "{{cognitive_behavioral_pattern_analysis}}",
      "Treatment_Review": "{{treatment_review}}",
      "Treatment_Evaluation": "{{treatment_evaluation}}",
      "Homework_Assignment": "{{homework_assignment}}",
    }
}
```
"""

mental_template = """
# Guidelines:
{guide}

# Schema:
{schema}

# CBT Psychological Template that need to be updated:
{template}

# Please update the psychological template based on the current psychological counseling dialogue:
Current psychological counseling dialogue:
```
{dialogue}
```

Output the updated psychological template, Up to 1500 tokens and Your CBT style reply as a doctor. Split using "==="
"""

summarize_template = """
Your task is to summarize the content of the CBT Psychological Template attribute. 
If the content of some attributes is too long, it will be summarized. If it is not long, it will not be modified.
You should summarize the content of the attribute based on the Schema and CBT Psychological Template.
Strictly follow the schema format, the CBT template format for output. Up to 1500 tokens.

# Schema:
{schema}

# CBT Psychological Template:
{template}

# Just output CBT Psychological Template after summarizing:
"""

# 定义 JSON Schema
template_schema = """
"properties": {
    "Personal_Information": {
        "Name",
        "Age",
        "Gender",
        "Occupation",
        "Marital_Status"
    },
    "Living_Conditions": {
        "Sleep",
        "Diet",
        "Interpersonal_Relationships",
        "Engaged_Interests_Motivations",
        "Self_harm_Risk"
    },
    "Cognitive_Structure_Assessment_and_Intervention": {
        "Emotion_Recognition_and_Evaluation",
        "Automatic_Thought_Recognition_and_Evaluation",
        "Intermediate_Recognition_and_Correction",
        "Core_Belief_Recognition_and_Correction",
        "Cognitive_Restructuring"
    },
    "CBT_Treatment_Overview": {
        "Primary_Complaint",
        "Diagnosis",
        "Treatment_Goals",
        "Treatment_Methods_and_Content"
    },
    "CBT_Treatment_Process": {
        "Agenda_Setting",
        "Triggering_Event",
        "Cognitive_Behavioral_Pattern_Analysis",
        "Treatment_Review",
        "Treatment_Evaluation",
        "Homework_Assignment"
    }
}
"""