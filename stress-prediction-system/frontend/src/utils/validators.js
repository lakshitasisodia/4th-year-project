export const validateStressLevelInput = (data) => {
  const errors = {}
  
  // Exact ranges from backend config.py FIELD_RANGES
  const ranges = {
    anxiety_level: [0, 21],
    self_esteem: [0, 30],
    mental_health_history: [0, 1],
    depression: [0, 27],
    headache: [0, 5],
    blood_pressure: [1, 3],
    sleep_quality: [0, 10],
    breathing_problem: [0, 10],
    noise_level: [0, 5],
    living_conditions: [0, 10],
    safety: [0, 10],
    basic_needs: [0, 10],
    academic_performance: [0, 5],
    study_load: [0, 10],
    teacher_student_relationship: [0, 10],
    future_career_concerns: [0, 10],
    social_support: [0, 12],
    peer_pressure: [0, 10],
    extracurricular_activities: [0, 10],
    bullying: [0, 10]
  }
  
  for (const [field, [min, max]] of Object.entries(ranges)) {
    if (data[field] === undefined || data[field] === '') {
      errors[field] = `${field} is required`
    } else {
      const value = Number(data[field])
      if (isNaN(value)) {
        errors[field] = `${field} must be a number`
      } else if (value < min || value > max) {
        errors[field] = `${field} must be between ${min} and ${max}`
      }
    }
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

export const validateStressTypeInput = (data) => {
  const errors = {}
  
  // Gender validation
  if (data.Gender === undefined || data.Gender === '') {
    errors.Gender = 'Gender is required'
  } else if (![0, 1].includes(Number(data.Gender))) {
    errors.Gender = 'Gender must be 0 or 1'
  }
  
  // Age validation
  if (data.Age === undefined || data.Age === '') {
    errors.Age = 'Age is required'
  } else {
    const age = Number(data.Age)
    if (isNaN(age) || age < 15 || age > 60) {
      errors.Age = 'Age must be between 15 and 60'
    }
  }
  
  // All scale fields (EXACT field names as in backend config.py D2_FEATURES)
  const scaleFields = [
    'Have you recently experienced stress in your life?',
    'Have you noticed a rapid heartbeat or palpitations?',
    'Have you been dealing with anxiety or tension recently?',
    'Do you face any sleep problems or difficulties falling asleep?',
    'Have you been dealing with anxiety or tension recently?.1',
    'Have you been getting headaches more often than usual?',
    'Do you get irritated easily?',
    'Do you have trouble concentrating on your academic tasks?',
    'Have you been feeling sadness or low mood?',
    'Have you been experiencing any illness or health issues?',
    'Do you often feel lonely or isolated?',
    'Do you feel overwhelmed with your academic workload?',
    'Are you in competition with your peers, and does it affect you?',
    'Do you find that your relationship often causes you stress?',
    'Are you facing any difficulties with your professors or instructors?',
    'Is your working environment unpleasant or stressful?',
    'Do you struggle to find time for relaxation and leisure activities?',
    'Is your hostel or home environment causing you difficulties?',
    'Do you lack confidence in your academic performance?',
    'Do you lack confidence in your choice of academic subjects?',
    'Academic and extracurricular activities conflicting for you?',
    'Do you attend classes regularly?',
    'Have you gained/lost weight?'
  ]
  
  scaleFields.forEach(field => {
    if (data[field] === undefined || data[field] === '') {
      errors[field] = `This field is required`
    } else {
      const value = Number(data[field])
      if (isNaN(value) || value < 1 || value > 5) {
        errors[field] = `Must be between 1 and 5`
      }
    }
  })
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}