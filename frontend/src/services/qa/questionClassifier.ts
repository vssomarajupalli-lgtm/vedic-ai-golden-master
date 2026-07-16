// BKL-008A.3 — Deterministic Q&A Engine
// Question Classifier + Intent Registry
// Classifies user questions and maps to engine output types

export type QuestionClass =
  | 'planet'
  | 'house'
  | 'yoga'
  | 'dasha'
  | 'transit'
  | 'probability'
  | 'formula'
  | 'calibration'
  | 'recommendation'
  | 'general'
  | 'unsupported';

export interface ClassifiedQuestion {
  /** Original user question */
  rawQuestion: string;
  /** Classified question type */
  questionClass: QuestionClass;
  /** Extracted entities (planet names, house numbers, etc.) */
  entities: string[];
  /** Confidence in the classification (0-1) */
  confidence: number;
  /** Whether this question is supported */
  isSupported: boolean;
  /** If unsupported, explanation */
  unsupportedReason?: string;
}

export interface IntentMapping {
  questionClass: QuestionClass;
  /** Engine outputs needed to answer */
  requiredEngineOutputs: string[];
  /** Formula references needed */
  requiredFormulaDomains: string[];
  /** Keywords that trigger this intent */
  keywords: string[];
  /** Example questions */
  examples: string[];
}

const INTENT_REGISTRY: IntentMapping[] = [
  {
    questionClass: 'planet',
    requiredEngineOutputs: ['planetStrength', 'probabilityOutput'],
    requiredFormulaDomains: ['Planet Strength'],
    keywords: ['planet', 'sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu',
      'strength', 'dignity', 'exalted', 'debilitated', 'retrograde', 'combust'],
    examples: ['What is the strength of Jupiter?', 'How strong is Saturn in my chart?', 'Is Mars debilitated?'],
  },
  {
    questionClass: 'house',
    requiredEngineOutputs: ['bhavaStrength', 'probabilityOutput'],
    requiredFormulaDomains: ['House Strength'],
    keywords: ['house', 'bhava', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th',
      'ascendant', 'lagna', 'kendra', 'trikona', 'dusthana'],
    examples: ['What is the strength of the 7th house?', 'How is the 10th house?', 'Which houses are strong?'],
  },
  {
    questionClass: 'yoga',
    requiredEngineOutputs: ['probabilityOutput', 'pipelineOutput'],
    requiredFormulaDomains: ['Yoga'],
    keywords: ['yoga', 'combination', 'raja yoga', 'dhana yoga', 'pancha mahapurusha', 'gaja kesari',
      'budha aditya', 'naga yoga', 'kemadruma', 'sanyasa'],
    examples: ['Are there any yogas in my chart?', 'Do I have Raja Yoga?', 'What about Dhana Yoga?'],
  },
  {
    questionClass: 'dasha',
    requiredEngineOutputs: ['dashaOutput', 'probabilityOutput'],
    requiredFormulaDomains: ['Dasha'],
    keywords: ['dasha', 'mahadasha', 'antardasha', 'pratyantar', 'vimshottari', 'period', 'running',
      'current dasha', 'upcoming dasha', 'dasha lord'],
    examples: ['What is my current mahadasha?', 'When does my next dasha start?', 'How is my Venus dasha?'],
  },
  {
    questionClass: 'transit',
    requiredEngineOutputs: ['transitOutput', 'probabilityOutput'],
    requiredFormulaDomains: ['Transit'],
    keywords: ['transit', 'gochara', 'current transit', 'saturn transit', 'jupiter transit', 'rahu transit',
      'sadesati', 'ashtam shani', 'transit effect', 'transit impact'],
    examples: ['What is the current transit effect?', 'How is Saturn transit for me?', 'Am I in Sadesati?'],
  },
  {
    questionClass: 'probability',
    requiredEngineOutputs: ['probabilityOutput'],
    requiredFormulaDomains: ['Probability'],
    keywords: ['probability', 'likelihood', 'chance', 'outcome', 'result', 'score', 'final', 'overall'],
    examples: ['What is the final probability?', 'What is the overall score?', 'How likely is this outcome?'],
  },
  {
    questionClass: 'formula',
    requiredEngineOutputs: ['probabilityOutput', 'transitOutput'],
    requiredFormulaDomains: ['All'],
    keywords: ['formula', 'calculation', 'how is', 'computed', 'derived', 'method', 'algorithm'],
    examples: ['What formula is used for transit activation?', 'How is planet strength calculated?'],
  },
  {
    questionClass: 'calibration',
    requiredEngineOutputs: [],
    requiredFormulaDomains: [],
    keywords: ['calibration', 'constant', 'weight', 'parameter', 'profile', 'setting'],
    examples: ['What calibration constants are used?', 'What is the weight for own sign?'],
  },
  {
    questionClass: 'recommendation',
    requiredEngineOutputs: ['probabilityOutput', 'transitOutput'],
    requiredFormulaDomains: ['All'],
    keywords: ['recommend', 'suggest', 'advice', 'what should', 'should I', 'what to do', 'remedy', 'upaya'],
    examples: ['What do you recommend?', 'Any remedies?', 'What should I do?'],
  },
  {
    questionClass: 'general',
    requiredEngineOutputs: ['probabilityOutput', 'transitOutput', 'dashaOutput'],
    requiredFormulaDomains: ['All'],
    keywords: ['explain', 'tell me', 'summary', 'overview', 'analysis', 'reading', 'report'],
    examples: ['Explain my chart', 'Give me a summary', 'What does my chart say?'],
  },
];

export class QuestionClassifier {
  /**
   * Classify a user question into a question class.
   */
  static classify(question: string): ClassifiedQuestion {
    const normalized = question.toLowerCase().trim();
    const results: { questionClass: QuestionClass; score: number; matchedKeywords: string[] }[] = [];

    for (const intent of INTENT_REGISTRY) {
      let score = 0;
      const matchedKeywords: string[] = [];

      for (const keyword of intent.keywords) {
        if (normalized.includes(keyword.toLowerCase())) {
          score += 1;
          matchedKeywords.push(keyword);
        }
      }

      // Bonus for exact match with examples
      for (const example of intent.examples) {
        if (normalized.includes(example.toLowerCase().substring(0, 20))) {
          score += 2;
        }
      }

      if (score > 0) {
        results.push({ questionClass: intent.questionClass, score, matchedKeywords });
      }
    }

    // Sort by score descending
    results.sort((a, b) => b.score - a.score);

    if (results.length === 0) {
      return {
        rawQuestion: question,
        questionClass: 'unsupported',
        entities: [],
        confidence: 0,
        isSupported: false,
        unsupportedReason: 'No matching keywords found. The question may be outside the deterministic engine scope.',
      };
    }

    const best = results[0];
    const totalMatches = results.reduce((sum, r) => sum + r.score, 0);
    const confidence = totalMatches > 0 ? best.score / totalMatches : 0.5;

    // Extract entities (planets, house numbers, etc.)
    const entities = QuestionClassifier.extractEntities(normalized);

    return {
      rawQuestion: question,
      questionClass: best.questionClass,
      entities,
      confidence,
      isSupported: best.questionClass !== 'unsupported',
    };
  }

  /**
   * Get the intent mapping for a question class.
   */
  static getIntent(questionClass: QuestionClass): IntentMapping | undefined {
    return INTENT_REGISTRY.find(i => i.questionClass === questionClass);
  }

  /**
   * Get suggested follow-up questions for a question class.
   */
  static getFollowUpQuestions(questionClass: QuestionClass, _entities: string[]): string[] {
    const followUps: Record<QuestionClass, string[]> = {
      planet: [
        'What is the overall strength of this planet?',
        'How does this planet affect my chart?',
        'What house is this planet in?',
      ],
      house: [
        'What planets are in this house?',
        'What is the bhava strength?',
        'What domains does this house rule?',
      ],
      yoga: [
        'What is the effect of this yoga?',
        'When will this yoga activate?',
        'Are there any similar yogas?',
      ],
      dasha: [
        'When does this dasha period end?',
        'What is the next dasha?',
        'How does this dasha affect my chart?',
      ],
      transit: [
        'What is the transit activation score?',
        'Which domains are most affected?',
        'When will this transit end?',
      ],
      probability: [
        'What contributes to this probability?',
        'How reliable is this score?',
        'What would change this probability?',
      ],
      formula: [
        'Show me the formula evidence chain',
        'What calibration constants affect this formula?',
        'How was this formula validated?',
      ],
      calibration: [
        'What is the calibration profile version?',
        'How do calibration constants affect the result?',
        'Can calibration be adjusted?',
      ],
      recommendation: [
        'What are the practical implications?',
        'What timing is recommended?',
        'Are there any mitigating factors?',
      ],
      general: [
        'What are the key findings?',
        'What domains are most significant?',
        'What should I focus on?',
      ],
      unsupported: [
        'What can you tell me about my chart?',
        'What is the current transit?',
        'What is my dasha period?',
      ],
    };

    return followUps[questionClass] || followUps.unsupported;
  }

  private static extractEntities(normalized: string): string[] {
    const entities: string[] = [];
    const planetNames = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu'];
    const houseNames = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th',
      'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth'];

    for (const planet of planetNames) {
      if (normalized.includes(planet)) entities.push(planet);
    }
    for (const house of houseNames) {
      if (normalized.includes(house)) entities.push(house);
    }

    return entities;
  }
}