export type Exercise = {
  id: string; title: string; description: string; starter_code: string
  function_name: string; concept: string; category: string; difficulty: string; tags: string[]; test_count: number
  language: 'python' | 'java' | 'c' | 'web' | 'multi'; execution_mode: 'function' | 'stdin_stdout' | 'browser' | 'multi_language_stdio'
  entry_point: string; starter_files?: Record<string, string> | null; tests?: Record<string, unknown>[]
  languages?: string[]; language_starters?: Record<string, string> | null
  examples?: { input: string; output: string; explanation?: string }[]; constraints?: string[]
}
export type Diagnosis = {
  title: string; category: string; confidence: number; evidence: string[]; explanation: string
}
export type TestResult = { passed: boolean; expected?: unknown; actual?: unknown; error?: string; label?: string; message?: string; timeout?: boolean }
export type Attempt = {
  id: number; exercise_id: string; passed: boolean; status: string; diagnosis: Diagnosis
  test_results: TestResult[]; duration_ms: number; hint_level: number; created_at: string; language?: string
}
export type Mastery = { concept: string; probability: number; attempts: number }
export type ConceptGraph = { nodes: { id: string; mastery: number; attempts: number }[]; edges: { from: string; to: string }[] }
