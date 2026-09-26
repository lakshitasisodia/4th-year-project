export const API_BASE_URL = 'http://localhost:5000/api'

// Dataset 1 (Stress Level) Fields - EXACTLY as backend expects.
// Ranges verified against the complete StressLevelDataset.csv (1100 rows) —
// 12 of these were wrong before (e.g. sleep_quality was 0-10, real data is 0-5).
// Must stay in sync with backend/config.py Config.FIELD_RANGES.
export const STRESS_LEVEL_FIELDS = [
  { name: 'anxiety_level', label: 'Anxiety Level', min: 0, max: 21, type: 'number' },
  { name: 'self_esteem', label: 'Self Esteem', min: 0, max: 30, type: 'number' },
  { name: 'mental_health_history', label: 'Mental Health History', min: 0, max: 1, type: 'select', options: [
    { value: 0, label: 'No' },
    { value: 1, label: 'Yes' }
  ]},
  { name: 'depression', label: 'Depression Score', min: 0, max: 27, type: 'number' },
  { name: 'headache', label: 'Headache Frequency', min: 0, max: 5, type: 'number' },
  { name: 'blood_pressure', label: 'Blood Pressure', min: 1, max: 3, type: 'select', options: [
    { value: 1, label: 'Low' },
    { value: 2, label: 'Normal' },
    { value: 3, label: 'High' }
  ]},
  { name: 'sleep_quality', label: 'Sleep Quality', min: 0, max: 5, type: 'number' },
  { name: 'breathing_problem', label: 'Breathing Problem', min: 0, max: 5, type: 'number' },
  { name: 'noise_level', label: 'Noise Level', min: 0, max: 5, type: 'number' },
  { name: 'living_conditions', label: 'Living Conditions', min: 0, max: 5, type: 'number' },
  { name: 'safety', label: 'Safety', min: 0, max: 5, type: 'number' },
  { name: 'basic_needs', label: 'Basic Needs', min: 0, max: 5, type: 'number' },
  { name: 'academic_performance', label: 'Academic Performance', min: 0, max: 5, type: 'number' },
  { name: 'study_load', label: 'Study Load', min: 0, max: 5, type: 'number' },
  { name: 'teacher_student_relationship', label: 'Teacher-Student Relationship', min: 0, max: 5, type: 'number' },
  { name: 'future_career_concerns', label: 'Future Career Concerns', min: 0, max: 5, type: 'number' },
  { name: 'social_support', label: 'Social Support', min: 0, max: 3, type: 'number' },
  { name: 'peer_pressure', label: 'Peer Pressure', min: 0, max: 5, type: 'number' },
  { name: 'extracurricular_activities', label: 'Extracurricular Activities', min: 0, max: 5, type: 'number' },
  { name: 'bullying', label: 'Bullying', min: 0, max: 5, type: 'number' }
]

// Dataset 2 (Stress Type) Fields - EXACTLY as backend expects (with full question text)
export const STRESS_TYPE_FIELDS = [
  { name: 'Gender', label: 'Gender', type: 'select', options: [
    { value: 0, label: 'Male' },
    { value: 1, label: 'Female' }
  ]},
  { name: 'Age', label: 'Age', min: 15, max: 60, type: 'number' },
  { name: 'Have you recently experienced stress in your life?', label: 'Recently Experienced Stress', min: 1, max: 5, type: 'scale' },
  { name: 'Have you noticed a rapid heartbeat or palpitations?', label: 'Rapid Heartbeat/Palpitations', min: 1, max: 5, type: 'scale' },
  { name: 'Have you been dealing with anxiety or tension recently?', label: 'Anxiety/Tension', min: 1, max: 5, type: 'scale' },
  { name: 'Do you face any sleep problems or difficulties falling asleep?', label: 'Sleep Problems', min: 1, max: 5, type: 'scale' },
  { name: 'Have you been dealing with anxiety or tension recently?.1', label: 'Anxiety/Tension (Verification)', min: 1, max: 5, type: 'scale' },
  { name: 'Have you been getting headaches more often than usual?', label: 'Frequent Headaches', min: 1, max: 5, type: 'scale' },
  { name: 'Do you get irritated easily?', label: 'Easy Irritation', min: 1, max: 5, type: 'scale' },
  { name: 'Do you have trouble concentrating on your academic tasks?', label: 'Concentration Difficulty', min: 1, max: 5, type: 'scale' },
  { name: 'Have you been feeling sadness or low mood?', label: 'Sadness/Low Mood', min: 1, max: 5, type: 'scale' },
  { name: 'Have you been experiencing any illness or health issues?', label: 'Illness/Health Issues', min: 1, max: 5, type: 'scale' },
  { name: 'Do you often feel lonely or isolated?', label: 'Loneliness/Isolation', min: 1, max: 5, type: 'scale' },
  { name: 'Do you feel overwhelmed with your academic workload?', label: 'Academic Workload Overwhelm', min: 1, max: 5, type: 'scale' },
  { name: 'Are you in competition with your peers, and does it affect you?', label: 'Peer Competition Impact', min: 1, max: 5, type: 'scale' },
  { name: 'Do you find that your relationship often causes you stress?', label: 'Relationship Stress', min: 1, max: 5, type: 'scale' },
  { name: 'Are you facing any difficulties with your professors or instructors?', label: 'Professor/Instructor Difficulties', min: 1, max: 5, type: 'scale' },
  { name: 'Is your working environment unpleasant or stressful?', label: 'Unpleasant Work Environment', min: 1, max: 5, type: 'scale' },
  { name: 'Do you struggle to find time for relaxation and leisure activities?', label: 'Lack of Relaxation Time', min: 1, max: 5, type: 'scale' },
  { name: 'Is your hostel or home environment causing you difficulties?', label: 'Home Environment Difficulties', min: 1, max: 5, type: 'scale' },
  { name: 'Do you lack confidence in your academic performance?', label: 'Lack Academic Performance Confidence', min: 1, max: 5, type: 'scale' },
  { name: 'Do you lack confidence in your choice of academic subjects?', label: 'Lack Subject Choice Confidence', min: 1, max: 5, type: 'scale' },
  { name: 'Academic and extracurricular activities conflicting for you?', label: 'Activity Conflict', min: 1, max: 5, type: 'scale' },
  { name: 'Do you attend classes regularly?', label: 'Class Attendance', min: 1, max: 5, type: 'scale' },
  { name: 'Have you gained/lost weight?', label: 'Weight Change', min: 1, max: 5, type: 'scale' }
]

export const SCALE_LABELS = {
  1: 'Never',
  2: 'Rarely',
  3: 'Sometimes',
  4: 'Often',
  5: 'Always'
}
