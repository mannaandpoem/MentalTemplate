system_prompt_template = """
Next, you will act as a professional CBT cognitive behavioral therapy psychologist. 
I will input the "psychological counseling dialogue" between the counselor and the patient. During the whole psychological counseling dialogue, you need to use the professional knowledge of CBT to detect whether there is any key information in the message, and then decide whether to update the attributes of the given psychological template. 
Note: 
1. All attributes must be present and filled with "information content" or "original content" or "unknown"! Avoid other unmentioned words such as "ongoing" and "pending"!
2. Updates are based on the content of the template's attributes!
3. If no update is needed, output "no update required"! If an update is needed, only output the updated "psychological template"! 
"""

mental_template = """
This is a template for tracking the mental health, treatment status, and progress of the therapist and patient during the treatment.

# Update guidelines:
When updating template attributes, please consider the process step by step:
1. Check for new content: Examine whether there is new content detected based on the original content.
2. No new content detected: If there is no new content detected and the attribute contains the original content, retain the original content for the attribute. If the attribute doesn't have the original content, output "unknown."
3. New content detected: If new content is detected, update the attribute using the original content as a base.
4. Output: Output the updated content for the attribute.Note: 
- 1. All attributes must be present and filled with "information content" or "original content" or "unknown"! Avoid other unmentioned words such as "ongoing" and "pending"
- 2. Updates are based on the content of the template's attributes!

# CBT Psychological Template:
```markdown
## Personal Information
- Name: {{name}}
- Age: {{age}}
- Gender: {{gender}}
- Occupation: {{occupation}}
- Marital Status: {{marital_status}}

## Risk Assessment
- Self-harm Risk: {{self_harm_risk}}
- Harm to Others Risk: {{harm_to_others_risk}}
- Safety Plan: {{safety_plan}}

## Living Conditions
- Sleep: {{sleep_patterns}}
- Diet: {{eating_habits}}
- Interpersonal Relationships: {{relationship_status}}
- Daily Activities: {{activity_levels}}
- Hobbies: {{hobbies}}
- Engaged Interests/Motivations: {{engaged_interests}}
- Stressors: {{stressors}}

## Cognitive Structure Assessment and Intervention
- Emotion Recognition and Evaluation: {{emotion_recognition_and_evaluation}}
- Automatic Thought Recognition and Evaluation: {{automatic_thought_recognition_and_evaluation}}
- Intermediate Recognition and Correction: {{intermediate_recognition_and_correction}}
- Core Belief Recognition and Correction: {{core_belief_recognition_and_correction}}
- Cognitive Restructuring: {{cognitive_restructuring}}

## CBT Treatment Overview
- Primary Complaint: {{primary_complaint}}
- Diagnosis: {{diagnosis}}
- Treatment Goals: {{treatment_goals}}
### Treatment Methods and Content
- Mood Diary: {{mood_diary}}
- Cognitive Triple Column Table: {{cognitive_triple_column_table}}
- Worry List: {{worry_list}} 
- Questioning Technique: {{questioning_technique}}
- Behavioral Experiment Method: {{behavioral_experiment_method}}
- Exposure and Response Prevention: {{exposure_and_response_prevention}}
- Relaxation Techniques: {{relaxation_techniques}}
- Ask for negative feedback: {{negative_feedback}}

## CBT Treatment Process
- Information Collection: {{information_collection}} 
- Agenda Setting: {{agenda_setting}} 
- Triggering Event:{{triggering_event}}
- Cognitive Behavioral Pattern Analysis: {{cognitive_behavioral_pattern_analysis}} 
- Treatment Review: {{treatment_review}}
- Treatment Evaluation: {{treatment_evaluation}}
- Homework Assignment: {{homework_assignment}}
- Next Session Plan: {{next_session_plan}}
```

# Please update the psychological template based on the psychological counseling dialogue below: 
Psychological counseling dialogue:
```
{dialogue}
```

Just output the updated Psychological template:
"""

new_mental_template = """
This is a template for tracking the mental health, treatment status, and progress of the therapist and patient during the treatment.

# Update guidelines:
When updating template attributes, please consider the process step by step:
1. Check for new content: Examine whether there is new content detected based on the original content.
2. No new content detected: If there is no new content detected and the attribute contains the original content, retain the original content for the attribute. If the attribute doesn't have the original content, output "unknown."
3. New content detected: If new content is detected, update the attribute using the original content as a base.
4. Output: Output the updated content for the attribute.Note: 
- 1. All attributes must be present and filled with "information content" or "original content" or "unknown"! Avoid other unmentioned words such as "ongoing" and "pending"
- 2. Updates are based on the content of the template's attributes!

# CBT Psychological Template that need to be updated:
{template}

# Please update the psychological template based on the current psychological counseling dialogue:
Current psychological counseling dialogue:
```
{dialogue}
```

Just output the updated psychological template:
"""
