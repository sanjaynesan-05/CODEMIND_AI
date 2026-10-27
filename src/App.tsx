import { useEffect, useMemo, useState } from 'react'
import Editor from '@monaco-editor/react'
import {
  Activity, ArrowDownRight, ArrowRight, ArrowUpRight, BookOpen,
  Check, CheckCircle2, ChevronDown, CircleHelp, Clock3, Code2, Command,
  FileCode2, Flame, GraduationCap, Lightbulb, LoaderCircle, LockKeyhole,
  Menu, Play, RotateCcw, Sparkles, Target, Terminal, Trophy, X,
} from 'lucide-react'
import type { Attempt, ConceptGraph, Exercise, Mastery } from './types'

type Page = 'home' | 'studio' | 'progress' | 'attempts'
type Hint = { level: number; label: string; content: string }
const api = async <T,>(path: string, init?: RequestInit): Promise<T> => {
  const response = await fetch(path, { ...init, headers: { 'Content-Type': 'application/json', ...init?.headers } })
  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail || `Request failed (${response.status})`)
  }
  return response.json() as Promise<T>
}

function App() {
  const [page, setPage] = useState<Page>('home')
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [selectedId, setSelectedId] = useState('')
  const [attempts, setAttempts] = useState<Attempt[]>([])
  const [mastery, setMastery] = useState<Mastery[]>([])
  const [conceptGraph, setConceptGraph] = useState<ConceptGraph>({ nodes: [], edges: [] })
  const [recommendation, setRecommendation] = useState<{ exercise: Exercise | null; reason: string } | null>(null)
  const [progress, setProgress] = useState({ attempts: 0, passed: 0, concept_count: 0 })
  const [lastAttempt, setLastAttempt] = useState<Attempt | null>(null)
  const [hint, setHint] = useState<Hint | null>(null)
  const [code, setCode] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [mobileNav, setMobileNav] = useState(false)

  const selected = exercises.find((exercise) => exercise.id === selectedId) ?? null
  const refresh = async () => {
    const [exerciseData, attemptData, masteryData, graphData, recommendData, progressData] = await Promise.all([
      api<Exercise[]>('/api/exercises'), api<Attempt[]>('/api/attempts'), api<Mastery[]>('/api/mastery'),
      api<ConceptGraph>('/api/concepts'),
      api<{ exercise: Exercise | null; reason: string }>('/api/recommendation'), api<typeof progress>('/api/progress'),
    ])
    setExercises(exerciseData); setAttempts(attemptData); setMastery(masteryData); setConceptGraph(graphData)
    setRecommendation(recommendData); setProgress(progressData)
    if (!selectedId && exerciseData.length) setSelectedId(exerciseData[0].id)
  }

  useEffect(() => {
    refresh().catch((err: Error) => setError(err.message)).finally(() => setLoading(false))
    // Initial data fetch only; refresh is called explicitly after submissions.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (!selected) return
    const saved = localStorage.getItem(`codemind-code-${selected.id}`)
    setCode(saved ?? selected.starter_code)
    setLastAttempt(null); setHint(null); setError('')
  }, [selectedId])

  const startExercise = (id: string) => { setSelectedId(id); setPage('studio'); setLastAttempt(null); setHint(null); setError('') }
  const updateCode = (value: string | undefined) => {
    const next = value ?? ''
    setCode(next)
    if (selected) localStorage.setItem(`codemind-code-${selected.id}`, next)
  }
  const submit = async () => {
    if (!selected) return
    setBusy(true); setError(''); setHint(null)
    try {
      const result = await api<Attempt & { message?: string }>('/api/submissions', {
        method: 'POST', body: JSON.stringify({ exercise_id: selected.id, code }),
      })
      setLastAttempt(result); await refresh()
    } catch (err) { setError(err instanceof Error ? err.message : 'Could not check your code.') }
    finally { setBusy(false) }
  }
  const requestHint = async (reveal_solution = false) => {
    if (!lastAttempt) return
    setBusy(true); setError('')
    try {
      setHint(await api<Hint>(`/api/attempts/${lastAttempt.id}/hints`, { method: 'POST', body: JSON.stringify({ reveal_solution }) }))
      if (!reveal_solution) setLastAttempt({ ...lastAttempt, hint_level: Math.max(lastAttempt.hint_level, (hint?.level ?? lastAttempt.hint_level) + 1) })
    } catch (err) { setError(err instanceof Error ? err.message : 'Could not load a hint.') }
    finally { setBusy(false) }
  }
  const nav = (destination: Page) => { setPage(destination); setMobileNav(false) }

  if (loading) return <div className="loading-screen"><div className="brand-mark"><Sparkles size={18} /></div><span>Getting your learning space ready…</span></div>

  return <div className="app-shell">
    <aside className={`sidebar ${mobileNav ? 'sidebar-open' : ''}`}>
      <div className="brand"><div className="brand-mark"><Sparkles size={17} strokeWidth={2.2} /></div><span>codemind<span className="brand-ai">.ai</span></span><button className="mobile-close icon-button" onClick={() => setMobileNav(false)} aria-label="Close navigation"><X size={18} /></button></div>
      <div className="workspace-switch"><div className="avatar avatar-small">S</div><span><b>My learning space</b><small>Python track</small></span><ChevronDown size={15} /></div>
      <div className="nav-caption">LEARN</div>
      <nav className="main-nav">
        <NavButton active={page === 'home'} onClick={() => nav('home')} icon={<Command size={17} />} label="Overview" />
        <NavButton active={page === 'studio'} onClick={() => nav('studio')} icon={<Code2 size={17} />} label="Code studio" />
        <NavButton active={page === 'progress'} onClick={() => nav('progress')} icon={<Activity size={17} />} label="Learning progress" />
        <NavButton active={page === 'attempts'} onClick={() => nav('attempts')} icon={<Clock3 size={17} />} label="Attempt history" count={attempts.length || undefined} />
      </nav>
      <div className="nav-caption exercises-caption">YOUR PRACTICE <button onClick={() => nav('studio')} aria-label="Browse practice"><ArrowRight size={13} /></button></div>
      <div className="exercise-nav-list">{exercises.slice(0, 6).map((exercise, index) => <button className={`exercise-nav-item ${selectedId === exercise.id && page === 'studio' ? 'chosen' : ''}`} key={exercise.id} onClick={() => startExercise(exercise.id)}><span className={`exercise-dot dot-${index % 4}`}>{progressFor(exercise.id, attempts) ? <Check size={11} /> : <span>{String(index + 1).padStart(2, '0')}</span>}</span><span>{exercise.title}</span></button>)}</div>
      <div className="sidebar-bottom"><div className="streak-card"><div className="streak-icon"><Flame size={17} /></div><div><b>{progress.attempts > 0 ? `${Math.min(7, progress.attempts)} day learning streak` : 'Start your streak'}</b><span>Small steps add up.</span></div><ArrowUpRight size={15} /></div><div className="user-row"><div className="avatar">S</div><div className="user-meta"><b>Student</b><small>Personal account</small></div><button className="icon-button" aria-label="Settings"><ChevronDown size={16} /></button></div></div>
    </aside>

    <main className="main-area">
      <header className="topbar"><button className="icon-button mobile-menu" onClick={() => setMobileNav(true)} aria-label="Open navigation"><Menu size={19} /></button><div className="breadcrumbs"><span>Learn</span><span className="crumb-slash">/</span><b>{pageTitle(page)}</b></div><div className="topbar-right"><div className="api-status"><span className="status-pulse" /> Learning workspace</div><div className="avatar avatar-top">S</div></div></header>
      {error && <div className="global-error"><CircleHelp size={16} /><span>{error}</span><button onClick={() => setError('')} aria-label="Dismiss"><X size={15} /></button></div>}
      <div className="page-content">
        {page === 'home' && <HomePage progress={progress} recommendation={recommendation} mastery={mastery} attempts={attempts} onStart={startExercise} onBrowse={() => nav('studio')} onProgress={() => nav('progress')} />}
        {page === 'studio' && <StudioPage exercises={exercises} selected={selected} code={code} onCodeChange={updateCode} onSelect={startExercise} onSubmit={submit} busy={busy} attempt={lastAttempt} hint={hint} onHint={() => requestHint(false)} onSolution={() => requestHint(true)} />}
        {page === 'progress' && <ProgressPage mastery={mastery} graph={conceptGraph} progress={progress} attempts={attempts} defaultExerciseId={recommendation?.exercise?.id ?? exercises[0]?.id} onStart={startExercise} />}
        {page === 'attempts' && <AttemptsPage attempts={attempts} exercises={exercises} onStart={startExercise} />}
      </div>
      <footer className="footer"><span><span className="footer-dot" /> CodeMind AI</span><span>Learn the thinking behind the code.</span><a href="https://github.com" onClick={(event) => event.preventDefault()}>Help center <ArrowUpRight size={12} /></a></footer>
    </main>
  </div>
}

function NavButton({ active, onClick, icon, label, count }: { active: boolean; onClick: () => void; icon: React.ReactNode; label: string; count?: number }) {
  return <button className={`nav-item ${active ? 'active' : ''}`} onClick={onClick}>{icon}<span>{label}</span>{count !== undefined && <span className="nav-count">{count}</span>}</button>
}

function HomePage({ progress, recommendation, mastery, attempts, onStart, onBrowse, onProgress }: { progress: { attempts: number; passed: number; concept_count: number }; recommendation: { exercise: Exercise | null; reason: string } | null; mastery: Mastery[]; attempts: Attempt[]; onStart: (id: string) => void; onBrowse: () => void; onProgress: () => void }) {
  const completion = progress.attempts ? Math.round((progress.passed / progress.attempts) * 100) : 0
  const lowest = [...mastery].sort((a, b) => a.probability - b.probability).slice(0, 3)
  return <div className="home-page">
    <div className="welcome-row"><div><div className="eyebrow"><span className="eyebrow-line" /> YOUR PERSONAL LEARNING SPACE</div><h1>Good to have you here<span className="hello-dot">.</span></h1><p className="welcome-copy">Build confidence one idea at a time. Your next step is ready when you are.</p></div><div className="date-chip"><Sparkles size={14} /> Python fundamentals</div></div>
    <section className="hero-card"><div className="hero-glow" /><div className="hero-copy"><div className="hero-tag"><span className="hero-tag-dot" /> YOUR NEXT STEP</div><h2>{recommendation?.exercise?.title ?? 'Start with a small win'}</h2><p>{recommendation?.reason ?? 'Pick an exercise, explore the editor, and make your first attempt.'}</p><button className="primary-button" onClick={() => recommendation?.exercise && onStart(recommendation.exercise.id)}><Play size={15} fill="currentColor" /> {progress.attempts ? 'Continue learning' : 'Start practicing'} <ArrowRight size={15} /></button></div><div className="hero-art"><div className="orbit orbit-one" /><div className="orbit orbit-two" /><div className="art-code-card"><div className="code-dots"><i /><i /><i /><span>your_next_step.py</span></div><div className="art-code"><span className="token-purple">def</span> <span className="token-blue">learn</span>():<br />&nbsp;&nbsp;<span className="token-green">try_again</span>()<br />&nbsp;&nbsp;<span className="token-purple">return</span> <span className="token-green">progress</span></div><div className="art-result"><span className="art-check"><Check size={12} /></span><span>Every attempt counts</span><ArrowUpRight size={13} /></div></div><div className="floating-spark spark-a"><Sparkles size={15} /></div><div className="floating-spark spark-b"><span>✦</span></div></div><div className="hero-index"><span>01</span><span className="index-rule" /><span>LEARN</span></div></section>
    <div className="section-heading"><div><div className="eyebrow"><span className="eyebrow-line" /> YOUR LEARNING AT A GLANCE</div><h2>Progress that adds up</h2></div><button className="text-link" onClick={onProgress}>View learning progress <ArrowRight size={15} /></button></div>
    <div className="stats-grid"><StatCard icon={<Target size={18} />} tone="lavender" label="Exercises tried" value={String(progress.attempts)} detail="Every try helps you learn" /><StatCard icon={<Trophy size={18} />} tone="mint" label="Checks passed" value={`${progress.passed}`} detail={progress.attempts ? `${completion}% of your attempts` : 'Your first is waiting'} /><StatCard icon={<BookOpen size={18} />} tone="peach" label="Concept areas" value={`${mastery.filter((item) => item.attempts).length} / ${progress.concept_count || 0}`} detail="Practice across Python topics" /><StatCard icon={<Flame size={18} />} tone="blue" label="Learning rhythm" value={progress.attempts ? 'In motion' : 'Ready'} detail="A little practice goes far" /></div>
    <div className="lower-grid"><section className="panel focus-panel"><div className="panel-heading"><div><div className="eyebrow">A GOOD PLACE TO FOCUS</div><h3>Concepts to explore</h3></div><button className="more-button" onClick={onProgress}>See all <ArrowRight size={14} /></button></div><div className="focus-list">{(lowest.length ? lowest : mastery.slice(0, 3)).map((item, index) => <div className="focus-row" key={item.concept}><div className={`focus-symbol focus-${index}`}><ConceptIcon index={index} /></div><div className="focus-info"><b>{item.concept}</b><span>{item.attempts ? `${item.attempts} attempt${item.attempts === 1 ? '' : 's'} · estimated ${Math.round(item.probability * 100)}% mastery` : 'Ready for your first practice'}</span></div><div className="focus-bar"><span style={{ width: `${Math.max(8, item.probability * 100)}%` }} /></div></div>)}</div><div className="soft-note"><Lightbulb size={15} /><span>These are learning estimates from your attempts. They become more useful with practice.</span></div></section>
      <section className="panel recent-panel"><div className="panel-heading"><div><div className="eyebrow">PICK UP WHERE YOU LEFT OFF</div><h3>Recent attempts</h3></div><button className="more-button" onClick={onBrowse}>Practice <ArrowRight size={14} /></button></div>{attempts.length ? <div className="recent-list">{attempts.slice(0, 4).map((attempt) => <div className="recent-row" key={attempt.id}><span className={`recent-status ${attempt.passed ? 'passed' : 'needs-work'}`}>{attempt.passed ? <Check size={12} /> : <ArrowDownRight size={13} />}</span><div className="recent-info"><b>{attempt.diagnosis.title}</b><span>{formatTime(attempt.created_at)}</span></div><span className={`result-label ${attempt.passed ? 'success' : ''}`}>{attempt.passed ? 'Passed' : 'Review'}</span></div>)}</div> : <div className="empty-recent"><div className="empty-icon"><FileCode2 size={19} /></div><b>Your work will show up here</b><span>Try an exercise and your learning history starts here.</span><button className="text-link" onClick={onBrowse}>Browse exercises <ArrowRight size={14} /></button></div>}</section></div>
    <div className="home-bottom-note"><div className="note-badge"><LockKeyhole size={14} /></div><span><b>Your code runs in isolation.</b> Each submission is checked in a restricted, disposable environment.</span><span className="note-separator">·</span><span>Need a hint? Ask for one whenever you like.</span></div>
  </div>
}

function StatCard({ icon, tone, label, value, detail }: { icon: React.ReactNode; tone: string; label: string; value: string; detail: string }) {
  return <div className="stat-card"><div className={`stat-icon ${tone}`}>{icon}</div><div className="stat-label">{label}</div><div className="stat-value">{value}</div><div className="stat-detail">{detail}</div><div className={`stat-trend ${tone}`}>{value === '0' || value === 'Ready' ? <ArrowRight size={13} /> : <ArrowUpRight size={13} />}</div></div>
}

function StudioPage({ exercises, selected, code, onCodeChange, onSelect, onSubmit, busy, attempt, hint, onHint, onSolution }: { exercises: Exercise[]; selected: Exercise | null; code: string; onCodeChange: (code: string | undefined) => void; onSelect: (id: string) => void; onSubmit: () => void; busy: boolean; attempt: Attempt | null; hint: Hint | null; onHint: () => void; onSolution: () => void }) {
  const [filter, setFilter] = useState('All')
  const topics = ['All', ...Array.from(new Set(exercises.map((exercise) => exercise.concept))) ]
  const visibleExercises = filter === 'All' ? exercises : exercises.filter((exercise) => exercise.concept === filter)
  const testsPassed = attempt?.test_results.filter((result) => result.passed).length ?? 0
  return <div className="studio-page">
    <div className="studio-title-row"><div><div className="eyebrow"><span className="eyebrow-line" /> PYTHON PRACTICE</div><h1>Code studio<span className="hello-dot">.</span></h1><p>Write, check, and understand. You can ask for a hint after you submit.</p></div><div className="studio-privacy"><LockKeyhole size={14} /> Isolated execution</div></div>
    <div className="studio-layout"><aside className="exercise-browser panel"><div className="browser-head"><div><div className="eyebrow">PRACTICE LIBRARY</div><h3>Exercises <span>{exercises.length}</span></h3></div><button className="filter-button" title="Filter by concept"><ChevronDown size={15} onClick={() => setFilter(filter === 'All' ? topics[1] ?? 'All' : 'All')} /></button></div><div className="browser-filter"><span>Showing</span><button onClick={() => setFilter(filter === 'All' ? topics[1] ?? 'All' : 'All')}>{filter} <ChevronDown size={12} /></button></div><div className="exercise-cards">{visibleExercises.map((exercise, index) => <button className={`exercise-card ${selected?.id === exercise.id ? 'selected' : ''}`} key={exercise.id} onClick={() => onSelect(exercise.id)}><span className={`exercise-index idx-${index % 4}`}>{String(index + 1).padStart(2, '0')}</span><span className="exercise-card-copy"><b>{exercise.title}</b><small>{exercise.concept}</small><span className="exercise-meta"><i className={exercise.difficulty.toLowerCase()} />{exercise.difficulty}<span>·</span>{exercise.test_count} checks</span></span>{selected?.id === exercise.id && <ArrowRight size={14} className="selected-arrow" />}</button>)}</div><div className="browser-foot"><BookOpen size={14} /> <span>More practice is added as you learn.</span></div></aside>
      <section className="workspace-column">{selected ? <><div className="workspace-top panel"><div className="workspace-exercise-heading"><div className="workspace-icon"><FileCode2 size={18} /></div><div><div className="workspace-kicker">CURRENT EXERCISE <span>·</span> {selected.concept.toUpperCase()}</div><h2>{selected.title}</h2></div></div><div className="difficulty-badge"><i className={selected.difficulty.toLowerCase()} />{selected.difficulty}</div></div>
        <div className="workspace-body"><section className="prompt-card panel"><div className="prompt-label"><BookOpen size={15} /> THE CHALLENGE</div><p>{selected.description}</p><div className="prompt-tags">{selected.tags.map((tag) => <span key={tag}>{tag}</span>)}</div><div className="test-preview"><div><Terminal size={14} /><b>What we’ll check</b></div><span>{selected.test_count} test cases <span className="preview-separator">·</span> edge cases included</span></div></section>
          <section className="editor-card panel"><div className="editor-toolbar"><div className="file-tab"><span className="python-icon">Py</span><span>solution.py</span><span className="unsaved-dot" title="Saved locally" /></div><div className="editor-tools"><span className="editor-saved"><Check size={12} /> Saved locally</span><button className="icon-button editor-reset" onClick={() => onCodeChange(selected.starter_code)} title="Reset starter code"><RotateCcw size={15} /></button></div></div><div className="monaco-wrap"><Editor height="345px" language="python" theme="vs-dark" value={code} onChange={onCodeChange} options={{ minimap: { enabled: false }, fontSize: 14, lineHeight: 23, fontFamily: 'JetBrains Mono, Consolas, monospace', padding: { top: 18 }, scrollBeyondLastLine: false, automaticLayout: true, tabSize: 4, insertSpaces: true, wordWrap: 'on', lineNumbersMinChars: 3, renderLineHighlight: 'line', suggestOnTriggerCharacters: true }} /></div><div className="editor-footer"><div><span className="editor-language"><span /> Python 3</span><span className="editor-footer-divider" /> <span>Code is saved in this browser</span></div><button className="check-button" onClick={onSubmit} disabled={busy || !code.trim()}>{busy ? <LoaderCircle size={15} className="spin" /> : <Play size={14} fill="currentColor" />}{busy ? 'Checking…' : 'Check my code'}<ArrowRight size={14} /></button></div></section>
          {attempt && <section className={`feedback-card panel ${attempt.passed ? 'feedback-pass' : 'feedback-review'}`}><div className="feedback-heading"><span className={`feedback-icon ${attempt.passed ? 'pass' : 'review'}`}>{attempt.passed ? <CheckCircle2 size={17} /> : <Lightbulb size={17} />}</span><div><div className="feedback-kicker">{attempt.passed ? 'NICE WORK' : 'LET’S THINK IT THROUGH'}</div><h3>{attempt.diagnosis.title}</h3></div><span className="confidence-chip">{Math.round(attempt.diagnosis.confidence * 100)}% confidence</span></div><p className="feedback-explanation">{attempt.diagnosis.explanation}</p><div className="evidence-box"><b>What we observed</b>{attempt.diagnosis.evidence.map((item, index) => <span key={index}><i />{item}</span>)}</div>{attempt.test_results.length > 0 && <div className="test-results"><div className="test-results-heading"><span>Test results</span><b>{testsPassed}/{attempt.test_results.length} passed</b></div>{attempt.test_results.map((test, index) => <div className="test-result-row" key={index}><span className={test.passed ? 'test-ok' : 'test-no'}>{test.passed ? <Check size={12} /> : <X size={12} />}</span><span>Check {index + 1}</span><span className="test-output">{test.error ? test.error : `Expected ${formatValue(test.expected)}${test.passed ? '' : ` · got ${formatValue(test.actual)}`}`}</span></div>)}</div>}
            <div className="hint-actions"><div className="hint-action-intro"><Lightbulb size={14} /><span>{attempt.passed ? 'Want to see another approach?' : 'Need a nudge to find your next step?'}</span></div>{!attempt.passed && attempt.hint_level < 2 && <button className="hint-button" onClick={onHint} disabled={busy}><Sparkles size={14} />{attempt.hint_level === 0 ? 'Give me a hint' : 'Another hint'}</button>}<button className="solution-button" onClick={onSolution} disabled={busy}><BookOpen size={14} />Show worked solution</button></div>
            {hint && <div className={`hint-result ${hint.level === 3 ? 'solution-result' : ''}`}><div className="hint-result-title"><span>{hint.level === 3 ? <BookOpen size={14} /> : <Sparkles size={14} />}</span>{hint.label}<span className="hint-result-check"><Check size={13} /></span></div>{hint.level === 3 ? <pre>{hint.content}</pre> : <p>{hint.content}</p>}</div>}
          </section>}
          <div className="workspace-tip"><div><Sparkles size={14} /></div><span><b>Think out loud.</b> Before changing your code, try to explain what each line is meant to do.</span></div>
        </div></> : <div className="panel empty-studio">{exercises.length ? 'Choose an exercise from the library to begin.' : 'Exercises are loading.'}</div>}</section></div>
  </div>
}

function ProgressPage({ mastery, graph, progress, attempts, defaultExerciseId, onStart }: { mastery: Mastery[]; graph: ConceptGraph; progress: { attempts: number; passed: number; concept_count: number }; attempts: Attempt[]; defaultExerciseId?: string; onStart: (id: string) => void }) {
  const values = mastery.map((item) => item.probability)
  const average = values.length ? Math.round(values.reduce((sum, value) => sum + value, 0) / values.length * 100) : 0
  const activeTopics = mastery.filter((item) => item.attempts).length
  return <div className="progress-page"><div className="page-intro"><div><div className="eyebrow"><span className="eyebrow-line" /> YOUR LEARNING JOURNEY</div><h1>Learning progress<span className="hello-dot">.</span></h1><p>Small steps become lasting understanding. Here’s what your practice is showing.</p></div><div className="progress-orb"><div><b>{average}%</b><span>estimated<br />mastery</span></div></div></div>
    <div className="progress-summary-grid"><div className="summary-card"><span className="summary-icon lav"><Target size={17} /></span><span className="summary-label">Exercises attempted</span><b>{progress.attempts}</b><small>Recorded practice attempts</small></div><div className="summary-card"><span className="summary-icon grn"><Trophy size={17} /></span><span className="summary-label">Checks passed</span><b>{progress.passed}</b><small>Fully passed submissions</small></div><div className="summary-card"><span className="summary-icon org"><BookOpen size={17} /></span><span className="summary-label">Concept areas tried</span><b>{activeTopics} <em>/ {progress.concept_count}</em></b><small>Build range as you practice</small></div></div>
    <div className="progress-content-grid"><section className="panel mastery-panel"><div className="panel-heading"><div><div className="eyebrow">LEARNER MODEL</div><h3>Concept understanding</h3></div><span className="estimate-pill"><span /> Estimates</span></div><p className="panel-subtext">These are rough estimates based on your test results, not fixed labels. More attempts make them more informative.</p><div className="mastery-list">{mastery.map((item, index) => <div className="mastery-item" key={item.concept}><div className={`mastery-icon mastery-${index % 4}`}><ConceptIcon index={index} /></div><div className="mastery-main"><div className="mastery-line"><b>{item.concept}</b><span>{Math.round(item.probability * 100)}%</span></div><div className="mastery-track"><span style={{ width: `${item.probability * 100}%` }} /></div><small>{item.attempts ? `${item.attempts} attempt${item.attempts === 1 ? '' : 's'} inform this estimate` : 'Try an exercise to start building this estimate'}</small></div></div>)}</div></section>
      <section className="panel milestones-panel"><div className="panel-heading"><div><div className="eyebrow">KEEP GOING</div><h3>Your learning rhythm</h3></div><span className="rhythm-flame"><Flame size={19} /></span></div><div className="rhythm-card"><div className="rhythm-count">{progress.attempts ? Math.min(progress.attempts, 7) : 0}</div><div><b>{progress.attempts ? 'Practice sessions logged' : 'Your first session is waiting'}</b><span>{progress.attempts ? 'Every submission is another piece of evidence.' : 'Start with a beginner exercise and build from there.'}</span></div></div><div className="milestone-list"><Milestone done={progress.attempts >= 1} label="Make your first attempt" detail={progress.attempts ? 'First step taken' : 'One exercise is all it takes'} /><Milestone done={progress.passed >= 1} label="Pass all checks" detail={progress.passed ? 'You passed a complete exercise' : 'Keep iterating on a submission'} /><Milestone done={activeTopics >= 3} label="Explore three concepts" detail={`${activeTopics} of 3 concepts tried`} /></div><button className="primary-button full-button" onClick={() => { const id = attempts[0]?.exercise_id ?? defaultExerciseId; if (id) onStart(id) }}><Play size={14} fill="currentColor" /> {progress.attempts ? 'Continue practicing' : 'Start your first exercise'} <ArrowRight size={14} /></button></section></div>
    <section className="panel concept-map-panel"><div className="panel-heading"><div><div className="eyebrow">HOW TOPICS CONNECT</div><h3>Concept map</h3></div><span className="estimate-pill"><span /> {graph.nodes.length} concepts</span></div><p className="panel-subtext">Some topics build on earlier ideas. Arrows show the learning prerequisites used when choosing practice.</p><div className="concept-map-grid">{graph.nodes.map((node, index) => { const prereqs = graph.edges.filter((edge) => edge.to === node.id).map((edge) => edge.from); return <div className="concept-map-node" key={node.id}><div className={`map-node-icon map-${index % 4}`}><ConceptIcon index={index} /></div><div className="map-node-copy"><b>{node.id}</b><span>{prereqs.length ? `Builds on ${prereqs.join(', ')}` : 'Foundation topic'}</span></div><div className="map-node-score">{Math.round(node.mastery * 100)}%</div></div>})}</div></section>
    <div className="estimate-disclaimer"><CircleHelp size={15} /><span><b>About these estimates.</b> CodeMind uses a simple Bayesian Knowledge Tracing model to update concept estimates from passing and failing attempts. Estimates are uncertain, especially when there is little practice.</span></div>
  </div>
}

function Milestone({ done, label, detail }: { done: boolean; label: string; detail: string }) {
  return <div className={`milestone ${done ? 'milestone-done' : ''}`}><span>{done ? <Check size={12} /> : <span />}</span><div><b>{label}</b><small>{detail}</small></div></div>
}

function AttemptsPage({ attempts, exercises, onStart }: { attempts: Attempt[]; exercises: Exercise[]; onStart: (id: string) => void }) {
  const [filter, setFilter] = useState('All attempts')
  const visible = useMemo(() => attempts.filter((item) => filter === 'All attempts' || (filter === 'Passed' ? item.passed : !item.passed)), [attempts, filter])
  return <div className="attempts-page"><div className="page-intro"><div><div className="eyebrow"><span className="eyebrow-line" /> YOUR PRACTICE LOG</div><h1>Attempt history<span className="hello-dot">.</span></h1><p>Every attempt is useful evidence. Look back, notice patterns, and try again.</p></div><div className="history-total"><Clock3 size={15} />{attempts.length} saved</div></div><section className="panel history-panel"><div className="history-toolbar"><div className="history-tabs">{['All attempts', 'Passed', 'Needs review'].map((item) => <button className={filter === item ? 'selected-tab' : ''} key={item} onClick={() => setFilter(item)}>{item}<span>{item === 'All attempts' ? attempts.length : item === 'Passed' ? attempts.filter((a) => a.passed).length : attempts.filter((a) => !a.passed).length}</span></button>)}</div><span className="history-sort"><Clock3 size={13} /> Most recent first</span></div>{visible.length ? <div className="history-table"><div className="history-table-head"><span>EXERCISE</span><span>RESULT</span><span>WHAT WE OBSERVED</span><span>WHEN</span><span /></div>{visible.map((attempt) => { const exercise = exercises.find((item) => item.id === attempt.exercise_id); return <div className="history-table-row" key={attempt.id}><div className="history-exercise"><span className={`history-exercise-icon ${attempt.passed ? 'hist-pass' : 'hist-review'}`}>{attempt.passed ? <Check size={14} /> : <FileCode2 size={14} />}</span><span><b>{exercise?.title ?? 'Python exercise'}</b><small>{exercise?.concept ?? 'Concept practice'}</small></span></div><span><i className={`table-result-dot ${attempt.passed ? 'dot-pass' : 'dot-review'}`} />{attempt.passed ? 'Passed' : 'In progress'}</span><span className="history-diagnosis">{attempt.diagnosis.title}</span><span className="history-time">{formatTime(attempt.created_at)}</span><button className="history-retry" onClick={() => onStart(attempt.exercise_id)} aria-label="Retry exercise"><ArrowRight size={15} /></button></div>})}</div> : <div className="history-empty"><div className="empty-icon"><Clock3 size={20} /></div><b>{attempts.length ? 'No attempts in this filter' : 'Your learning story starts here'}</b><span>{attempts.length ? 'Try another filter to see your saved work.' : 'Submit an exercise and the details will be saved here.'}</span>{exercises[0] && <button className="primary-button" onClick={() => onStart(exercises[0].id)}><Play size={14} fill="currentColor" /> Browse exercises <ArrowRight size={14} /></button>}</div>}</section><p className="history-privacy"><LockKeyhole size={14} /> Your attempts are stored locally with this CodeMind learning workspace.</p></div>
}

function ConceptIcon({ index }: { index: number }) {
  const icons = [<Code2 size={16} />, <Activity size={16} />, <Target size={16} />, <GraduationCap size={16} />]
  return icons[index % icons.length]
}
function pageTitle(page: Page) { return ({ home: 'Overview', studio: 'Code studio', progress: 'Learning progress', attempts: 'Attempt history' })[page] }
function progressFor(id: string, attempts: Attempt[]) { return attempts.some((attempt) => attempt.exercise_id === id && attempt.passed) }
function formatTime(date: string) {
  if (!date) return 'Just now'
  const elapsed = Math.max(0, Date.now() - new Date(date).getTime())
  if (elapsed < 60_000) return 'Just now'
  if (elapsed < 3_600_000) return `${Math.floor(elapsed / 60_000)} min ago`
  if (elapsed < 86_400_000) return `${Math.floor(elapsed / 3_600_000)} hr ago`
  return new Date(date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}
function formatValue(value: unknown) { return typeof value === 'string' ? JSON.stringify(value) : JSON.stringify(value) ?? String(value) }

export default App
