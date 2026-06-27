export interface QuestionItem {
  id: string;
  label: string;
}

export interface QuestionnaireDomain {
  domainId: string;
  domainLabel: string;
  questions: QuestionItem[];
}

export const QUESTIONNAIRE_SCHEMA: QuestionnaireDomain[] = [
  {
    domainId: "marriage",
    domainLabel: "1. Marriage",
    questions: [
      { id: "marriage_promise", label: "1.1 Marriage Promise" },
      { id: "marriage_timing", label: "1.2 Marriage Timing" },
      { id: "delayed_marriage", label: "1.3 Delayed Marriage" },
      { id: "love_marriage", label: "1.4 Love Marriage" },
      { id: "second_marriage", label: "1.5 Second Marriage" },
      { id: "marital_harmony", label: "1.6 Marital Harmony" },
      { id: "separation_risk", label: "1.7 Separation Risk" }
    ]
  },
  {
    domainId: "career",
    domainLabel: "2. Career",
    questions: [
      { id: "career_promise", label: "2.1 Career Promise" },
      { id: "promotion", label: "2.2 Promotion" },
      { id: "job_change", label: "2.3 Job Change" },
      { id: "government_job", label: "2.4 Government Job" },
      { id: "business_success", label: "2.5 Business Success" },
      { id: "foreign_career", label: "2.6 Foreign Career" }
    ]
  },
  {
    domainId: "wealth",
    domainLabel: "3. Wealth",
    questions: [
      { id: "wealth_promise", label: "3.1 Wealth Promise" },
      { id: "wealth_growth", label: "3.2 Wealth Growth" },
      { id: "property_purchase", label: "3.3 Property Purchase" },
      { id: "debt_risk", label: "3.4 Debt Risk" }
    ]
  }
];
