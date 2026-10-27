export type Exercise = {
  id: string; title: string; description: string; starter_code: string
  function_name: string; concept: string; difficulty: string; tags: string[]; test_count: number
}
export type Diagnosis = {
  title: string; category: string; confidence: number; evidence: string[]; explanation: string
}
export type TestResult = { passed: boolean; expected?: unknown; actual?: unknown; error?: string }
export type Attempt = {
  id: number; exercise_id: string; passed: boolean; status: string; diagnosis: Diagnosis
  test_results: TestResult[]; duration_ms: number; hint_level: number; created_at: string
}
export type Mastery = { concept: string; probability: number; attempts: number }
export type ConceptGraph = { nodes: { id: string; mastery: number; attempts: number }[]; edges: { from: string; to: string }[] }
