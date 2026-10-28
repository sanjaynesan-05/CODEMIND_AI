# Code Matrix: Cognitive Computing Project Report

**Course:** Cognitive Computing (23DC2037)  
**Institution:** Karunya Institute of Technology and Sciences  
**Project type:** Skill Based Evaluation  
**Prepared:** October 2026

> **Submission note:** Add student names, registration numbers, faculty details, signatures, institutional cover pages, and genuine screenshots from the running application before final submission. This report describes the implemented local prototype and distinguishes software verification from evidence of educational effectiveness.

## Abstract

Code Matrix is a local, browser-based coding-practice workspace that combines program execution, explainable feedback, progressive scaffolding, learner modeling, and concept-aware exercise recommendation. The system supports 39 authored exercises: 33 console problems in Python, Java, and C, and six multi-file HTML, CSS, and JavaScript projects. A learner selects an exercise, edits starter code in Monaco Editor, runs the relevant checks, studies the returned evidence, requests hints, reviews earlier attempts, and receives a recommendation for a subsequent exercise.

The cognitive-computing design is intentionally transparent. A prerequisite graph represents relationships among concepts; deterministic rules combine execution status, test results, and selected Python abstract syntax tree observations to produce a possible diagnosis; a Bayesian Knowledge Tracing (BKT)-style update maintains a per-concept mastery estimate; and a prerequisite-aware recommender selects an appropriate next task. Hints progress from conceptual guidance to a structural implementation suggestion, while a worked solution is returned only after an explicit request. Python, Java, and C submissions execute in disposable Docker containers with no network access, read-only filesystems, resource limits, and bounded time.

Validation uses a catalog inventory and six authored diagnosis probes. The probes confirm that the implemented workflow recognizes successful execution, syntax errors, an index-related runtime error, and output mismatches. They also reveal that several logical mistakes currently receive the same generic output-mismatch diagnosis. The evidence is therefore sufficient to demonstrate an implemented prototype and reproducible behavior, but not to claim diagnosis accuracy, calibrated confidence, recommendation quality, or learning gain. A larger independently labeled submission set and an appropriately approved learner study would be required for those claims.

**Keywords:** cognitive computing, intelligent tutoring system, programming education, explainable feedback, Bayesian Knowledge Tracing, adaptive recommendation, Docker sandboxing

---

# CHAPTER 1 — INTRODUCTION

## 1.1 Background

Programming is learned through repeated cycles of attempting a solution, observing its behavior, identifying the cause of failure, revising the implementation, and trying again. A simple pass/fail result is useful, but it does not always help a learner understand *why* a solution failed or what to try next. The same incorrect output can result from a missing return statement, an incorrect loop boundary, an invalid condition, or an incorrect interpretation of the problem.

Traditional compilers and test runners provide valuable factual evidence such as syntax messages, runtime exceptions, and expected-versus-actual output. However, that evidence is often separated from the learning concept being practiced. A learner may also reveal a complete solution too early and lose an opportunity to reason independently. These limitations motivate a small intelligent tutoring workflow that connects execution evidence with concept-level feedback and controlled assistance.

Code Matrix is designed as a local prototype for this purpose. It does not attempt to replace a teacher or make unsupported claims about learner intent. Its feedback is explicitly phrased as a possible explanation based on observable code structure and test outcomes.

## 1.2 Problem statement

How can a local programming-practice environment combine reliable execution feedback, explainable cognitive diagnosis, progressive hints, a lightweight learner model, and prerequisite-aware exercise recommendations in one coherent workflow?

## 1.3 Aim

The aim of the project is to design and implement an inspectable cognitive-computing prototype that supports iterative programming practice through evidence-based feedback and adaptive sequencing.

## 1.4 Objectives

The project objectives are to:

1. Provide a browser-based coding workspace for Python, Java, C, HTML, CSS, and JavaScript practice.
2. Evaluate console submissions against exercise-specific test cases.
3. Preview web projects and run browser checks for structure, text, styling, and interaction.
4. Generate cautious, deterministic diagnoses from execution outcomes and selected code-structure facts.
5. Provide conceptual and structural hints before exposing a worked solution.
6. Maintain per-concept practice estimates using a BKT-style update.
7. Represent prerequisite relationships among programming concepts.
8. Recommend a next exercise using attempted status, prerequisite mastery, and estimated concept difficulty.
9. Preserve attempts, test results, diagnoses, and mastery values in local persistence.
10. Isolate submitted console code from the API process and document the prototype’s limitations.

## 1.5 Research and design questions

- Can execution evidence be transformed into feedback that is more useful than a pass/fail label while remaining explainable?
- Can a small prerequisite graph and mastery estimate support a defensible next-exercise recommendation?
- Does the prototype provide an end-to-end loop from attempt to feedback, history, mastery update, and recommendation?
- Which limitations prevent the current implementation from being treated as a validated intelligent tutoring system?

## 1.6 Scope

The project is a local, single-learner formative-practice prototype. It includes a React frontend, a FastAPI backend, a catalog of authored exercises, isolated console execution, browser-based web checks, persistence, diagnosis, hints, progress views, and recommendations.

The following are outside the current scope:

- user accounts, authentication, and multi-user authorization;
- classroom administration, teacher dashboards, or proctored assessment;
- a trained machine-learning or language model;
- a comprehensive misconception classifier;
- a research dataset containing labeled learner submissions;
- a validated measure of learning gain or long-term retention;
- high-stakes grading or security guarantees for internet deployment.

## 1.7 Significance

The project demonstrates how cognitive-computing principles can be implemented with inspectable software components rather than opaque model calls. This is valuable for educational prototypes because a learner or instructor can trace a diagnosis to an observed test result, trace a recommendation to prerequisite estimates, and inspect the assumptions used in the mastery update.

---

# CHAPTER 2 — LITERATURE REVIEW

## 2.1 Cognitive computing in educational software

Cognitive computing systems attempt to support activities associated with human cognition, including reasoning, learning, knowledge representation, adaptation, and interaction. In an educational application, these capabilities are commonly expressed through a domain model, a learner model, an inference or feedback mechanism, and an interaction strategy. Code Matrix adopts this decomposition in a deliberately small and auditable form:

| Cognitive capability | Code Matrix representation |
|---|---|
| Knowledge representation | Exercise concepts and the `PREREQUISITES` directed graph |
| Observation | Test outcomes, execution status, browser checks, and Python AST facts |
| Reasoning | Deterministic diagnosis rules and evidence generation |
| Learning model | Per-concept BKT-style probability and attempt count |
| Adaptation | Prerequisite-aware exercise recommendation |
| Scaffolding | Conceptual hint, structural hint, then explicit solution reveal |

This design is not presented as a complete cognitive tutor. It is an implementation of selected ideas that can be inspected and evaluated independently.

## 2.2 Intelligent tutoring systems

Intelligent tutoring system research generally separates domain knowledge, student modeling, tutoring strategy, and user interface. Cognitive Tutors, for example, use a representation of problem-solving knowledge and student performance to provide step-level assistance. The principle relevant to this project is that feedback should be connected to the learner’s observed work rather than limited to a final score.

Code Matrix follows this principle at a smaller granularity. Its domain knowledge is the exercise catalog and concept graph. Its learner model is the mastery table. Its tutoring strategy is the diagnostic rule set and progressive hint sequence. Its interface is the Code Studio, UI Studio, progress view, and attempt history.

## 2.3 Bayesian Knowledge Tracing

Bayesian Knowledge Tracing models a learner’s probability of knowing a skill from a sequence of observed responses. The classic model uses a prior knowledge probability, a probability of learning after an opportunity, a guess probability, and a slip probability. Code Matrix uses a simplified, fixed-parameter update:

For an observed response \(O_t\), the posterior is:

\[
P(K_t \mid O_t) =
\begin{cases}
\frac{P(K_{t-1})(1-S)}
{P(K_{t-1})(1-S)+(1-P(K_{t-1}))G}, & O_t=\text{correct}\\[6pt]
\frac{P(K_{t-1})S}
{P(K_{t-1})S+(1-P(K_{t-1}))(1-G)}, & O_t=\text{incorrect}
\end{cases}
\]

The learning transition is then applied:

\[
P(K_t)=P(K_t \mid O_t)+(1-P(K_t \mid O_t))L
\]

The implementation uses an initial probability of 0.25, \(L=0.12\), \(G=0.20\), and \(S=0.10\), and clamps the result to the interval 0.01–0.99. A fully passing set of tests is treated as correct; any incomplete attempt is treated as incorrect. These are engineering assumptions, not parameters fitted to learners. Hint usage, partial correctness, problem difficulty, and time-on-task are not currently included in the update.

## 2.4 Knowledge representation and prerequisite graphs

A prerequisite graph provides a compact representation of dependencies between concepts. In the project, examples include:

- Expressions and conditions → Conditions and loops;
- Conditions and loops → Loops and accumulation;
- Arrays & Hashing → Two Pointers;
- Arrays & Hashing → Binary Search;
- Arrays & Hashing and Two Pointers → Sliding Window.

Such a graph supports sequencing decisions and gives learners a visual explanation for why a topic may be recommended. The graph is intentionally authored rather than learned from historical data.

## 2.5 Feedback, scaffolding, and worked examples

Educational research distinguishes feedback that merely reports correctness from feedback that helps a learner regulate the next attempt. Progressive hints can preserve productive struggle by giving increasing support. Code Matrix implements three levels:

1. **Conceptual hint:** identifies the idea to consider.
2. **Structural hint:** points toward a specific code operation or control structure.
3. **Worked solution:** reveals the authored solution only after explicit user action.

This is a simple scaffolding policy. It does not yet measure whether a learner solved the problem independently after receiving a hint.

## 2.6 Case-based and rule-based reasoning

Case-based reasoning uses prior cases to support a current decision. The current prototype stores prior attempts and counts earlier attempts with the same diagnosis title for the exercise. This is used as contextual evidence, not as a learned nearest-neighbor model. The primary diagnosis mechanism remains rule-based because deterministic rules make the source of feedback visible and reproducible.

## 2.7 Programming education tools and gap addressed

Online judges are strong at executing code and comparing results, while code editors and learning platforms provide practice interfaces. The project’s contribution is an integrated local workflow that places execution, evidence, hints, concept estimates, and recommendations in one interface. The gap is addressed as a prototype integration problem rather than a claim of a new educational algorithm.

## 2.8 Literature-review synthesis

The literature supports four design choices:

1. Use observable learner work as the basis for feedback.
2. Maintain an explicit learner model instead of treating all attempts identically.
3. Represent domain relationships so sequencing is explainable.
4. Use scaffolding that increases assistance gradually.

It also identifies the main evaluation requirement: a working tutor is not automatically an effective tutor. Educational effectiveness must be tested with independent labels, appropriate baselines, and learner outcomes.

---

# CHAPTER 3 — METHODOLOGY

## 3.1 Research and development approach

The project follows an implementation-oriented design-and-evaluation methodology:

1. Identify the learning problem and define the scope of a local prototype.
2. Model exercises, concepts, prerequisites, attempts, and mastery.
3. Implement the execution, feedback, hint, progress, and recommendation workflow.
4. Add safety controls around untrusted console submissions.
5. Create reproducible authored probes for core diagnosis branches.
6. Inspect results and document what can and cannot be concluded.

The evaluation is formative software validation, not a controlled educational experiment.

## 3.2 System inputs and data sources

The primary content source is the authored exercise catalog in:

- `backend/catalog.py`;
- `backend/dsa_catalog.py`;
- `backend/extended_dsa.py`;
- `backend/multilang_fundamentals.py`;
- `backend/ui_catalog.py`.

Each exercise can contain an identifier, title, prompt, concept, category, difficulty, starter code or files, test cases, examples, constraints, language variants, and a solution. The catalog contains 39 exercises: 33 console problems and six web projects.

The runtime data model contains:

| Entity | Important fields | Purpose |
|---|---|---|
| Exercise | id, prompt, concept, difficulty, tests, language, execution mode | Defines a practice task |
| Submission | exercise, code/files, language, status, passed, diagnosis, test results, duration | Preserves an attempt |
| Mastery | concept, probability, attempts, updated time | Stores the learner model |

No external learner dataset, demographic data, or labeled misconception corpus is used.

## 3.3 Functional methodology

### 3.3.1 Console workflow

For a console exercise, the learner selects a language and submits code. The API validates the exercise and language, rejects empty or oversized source, chooses the appropriate runner, executes the authored test cases, diagnoses the returned status, saves the attempt, updates mastery, and makes the recommendation available to the frontend.

### 3.3.2 Browser workflow

For a web exercise, the learner supplies `index.html`, `style.css`, and `script.js`. The frontend renders the project in a sandboxed iframe and executes browser checks. The API validates file names, text values, source size, and the number of returned checks before saving the result. Browser checks are client-reported and therefore intended for local formative feedback rather than trusted grading.

### 3.3.3 Diagnostic methodology

The diagnostic function follows an ordered decision process:

1. Browser status and browser checks are handled first.
2. Syntax, timeout, runtime, compile, and rejected states receive status-specific messages.
3. Completed console executions are classified as passed or mismatched.
4. For mismatches, Python AST facts are inspected where available:
   - a recursive call without a conditional branch may indicate a missing stopping condition;
   - no parsed return may indicate a missing return statement;
   - a loop-oriented exercise without a loop may indicate incomplete traversal;
   - an integer difference of one in a loop-containing solution may indicate an off-by-one boundary.
5. If no specialized rule applies, the tutor returns a generic output-mismatch explanation.

Every diagnosis includes a title, concept category, heuristic confidence, evidence, observed AST facts, and a disclaimer that it is a possible explanation rather than a claim about learner intent.

### 3.3.4 Hint methodology

Hints are selected by concept and current hint level. The first request returns a conceptual hint; the next request returns a structural hint. A solution request is a separate explicit action and returns level 3. If a concept has no authored hints, a general trace-the-failing-example prompt is used.

### 3.3.5 Recommendation methodology

The recommender:

1. identifies exercises not yet attempted where possible;
2. filters candidates whose prerequisites meet a mastery threshold of 0.35;
3. favors the candidate associated with the lowest estimated concept mastery;
4. falls back to other unattempted exercises if no candidate meets the threshold;
5. falls back to the full catalog after all exercises have been attempted;
6. returns a textual reason with the recommendation.

The threshold and ranking policy are authored heuristics and have not been validated against expert or learner judgments.

## 3.4 Validation methodology

The reproducible script `python scripts/evaluate_tutor.py`:

- inventories catalog count and category/difficulty combinations;
- sends six fixed authored scenarios through the production `diagnose` function;
- records diagnosis title, category, confidence, and evidence;
- writes `reports/evaluation_results.json`.

The scenarios cover a pass, missing return, loop-boundary-like mismatch, wrong output, syntax error, and index runtime error. Because the scenario labels are not independently adjudicated learner labels, accuracy metrics are intentionally not calculated.

## 3.5 Ethical, privacy, and safety methodology

The prototype stores local practice information and does not collect demographic information. It does not require an external AI key. Console execution is separated from the API process and uses Docker restrictions. The report avoids interpreting code structure as a statement of learner intention and avoids presenting authored probes as educational evidence.

---

# CHAPTER 4 — IMPLEMENTATION

## 4.1 System architecture

The implementation follows a client–API–execution–persistence architecture:

1. **Frontend:** React, TypeScript, Vite, Monaco Editor, and responsive CSS provide the dashboard and studios.
2. **API:** FastAPI exposes exercise, submission, hint, history, progress, mastery, and recommendation endpoints.
3. **Tutor layer:** `backend/tutor.py` contains prerequisite data, AST extraction, diagnosis rules, hints, and BKT-style updates.
4. **Runner layer:** `backend/runner.py` and `backend/stdio_runner.py` prepare and execute test harnesses.
5. **Persistence layer:** SQLAlchemy maps exercises, submissions, and mastery to SQLite or PostgreSQL.
6. **Browser layer:** web exercises render in a sandboxed iframe and return browser-check observations.

The architecture diagram is stored at [`assets/architecture.png`](../assets/architecture.png). Its legibility should be checked after placing it in the final formatted document.

## 4.2 Technology stack

| Layer | Technology | Implementation role |
|---|---|---|
| Frontend | React, TypeScript, Vite | Screens, state, API calls, and interaction |
| Editor | Monaco Editor | Code and multi-file editing |
| Backend | Python, FastAPI, Pydantic | API routes, validation, orchestration |
| Code inspection | Python `ast` | Limited structural observations |
| Execution | Docker runner images | Python, Java, and C isolation |
| Web preview | Sandboxed iframe | HTML/CSS/JavaScript rendering and checks |
| Persistence | SQLAlchemy, SQLite/PostgreSQL | Catalog, attempts, and mastery |
| Styling | CSS and Lucide React | Responsive layout and interface icons |

## 4.3 Exercise catalog

The catalog is divided into Code Studio and UI Studio:

- **Code Studio:** 33 console problems across fundamentals, arrays and hashing, two pointers, stack, binary search, sliding window, dynamic programming, graphs, strings, mathematics, recursion, input, and loops.
- **UI Studio:** six multi-file projects covering HTML structure, CSS styling, JavaScript interaction, and responsive design.

Console problems can use C, Python, or Java where language starters and solutions are provided. The same exercise-level test cases are used to compare behavior across enabled languages.

## 4.4 API and validation implementation

The FastAPI application:

- seeds or updates the local exercise catalog during startup;
- validates exercise identifiers and language selection;
- validates web file names and source size;
- requires all browser checks before a web submission is stored;
- converts runner results into a consistent diagnosis object;
- stores the submission and test results;
- updates the concept mastery estimate;
- exposes progress and recommendation data.

Pydantic request models cap code input at 20,000 characters. The API rejects invalid language selections, missing web files, invalid browser-check booleans, empty console code, and unavailable runner conditions with explicit HTTP errors.

## 4.5 Isolated execution

Console submissions are not executed inside the FastAPI process. The runner:

- parses Python before execution where applicable;
- creates a short-lived Docker container;
- disables networking;
- uses a read-only root filesystem;
- drops Linux capabilities;
- enables `no-new-privileges`;
- runs as an unprivileged user;
- limits memory to 128 MB, CPU to 0.5 CPU, and processes to 32;
- provides a small non-executable temporary filesystem;
- applies a bounded execution timeout;
- mounts the submission input read-only;
- removes the container and temporary files after execution.

These controls reduce risk for a local prototype but should not be interpreted as a complete security audit or production isolation guarantee.

## 4.6 Data persistence

The `Exercise` model stores task content and test definitions. The `Submission` model stores source or web files, selected language, pass status, execution status, diagnosis JSON, test results, duration, and hint level. The `Mastery` model stores one probability and attempt count per concept. SQLite is the default local database; PostgreSQL is supported through configuration and Docker Compose.

## 4.7 User interface

The frontend provides:

- an overview of available practice;
- Code Studio for console exercises;
- UI Studio for web projects;
- test and browser-check result views;
- diagnosis evidence and confidence;
- progressive hints and explicit solution reveal;
- attempt history;
- concept progress and prerequisite graph;
- next-exercise recommendation and rationale.

Unfinished editor drafts are saved locally by exercise and language. The current application is designed for one local learner profile.

## 4.8 Explainability and limitations in implementation

The system does not call an LLM. Explanations are deterministic templates, which makes the output reproducible and avoids external data transfer. The trade-off is limited coverage: the AST feature set is small, Python-specific, and unable to infer all logical causes. Confidence values express rule heuristics, not calibrated probabilities.

---

# CHAPTER 5 — TESTING AND VALIDATION

## 5.1 Testing objectives

Testing was designed to verify:

1. the exercise catalog can be loaded and counted;
2. the diagnosis function returns a structured result;
3. successful execution receives a passing diagnosis;
4. syntax errors are separated from runtime and output errors;
5. runtime index errors produce a specific possible explanation;
6. incomplete outputs retain factual expected-versus-actual evidence;
7. Python modules and the evaluation script compile successfully.

These objectives validate implementation behavior. They do not measure whether learners improve.

## 5.2 Reproducible test procedure

From the repository root, run:

```powershell
python scripts/evaluate_tutor.py
```

The command writes `reports/evaluation_results.json`. The script uses the production catalog and `diagnose` function rather than a separate mock implementation.

## 5.3 Authored probe cases

| Probe | Input condition | Expected validation purpose |
|---|---|---|
| Passed | Correct `sum_list` implementation | Confirm all-tests-passed branch |
| Missing return | Accumulation occurs but no `return` | Observe whether missing-return rule triggers |
| Loop boundary | Fibonacci-like loop returns 2 instead of 3 | Observe mismatch and boundary heuristic |
| Wrong output | Oddness condition used for evenness | Confirm factual mismatch evidence |
| Syntax error | Invalid function definition | Confirm syntax classification |
| Runtime error | Access to `xs[9]` | Confirm index-related runtime classification |

## 5.4 Validation results

The catalog inventory reported **39 exercises**. The diagnosis probe output contained six scenarios:

| Result category | Count | Interpretation |
|---|---:|---|
| All checks passed | 1 | Correct execution was recognized |
| Generic output mismatch | 3 | Logical failures received factual but broad feedback |
| Syntax issue | 1 | Syntax errors were classified separately |
| Possible out-of-bounds index | 1 | `IndexError` was mapped to a specific possible cause |
| **Total** | **6** | All authored probes returned a structured result |

The three generic mismatch cases were the missing-return, loop-boundary, and wrong-output probes. This is an important validation finding: the current implementation’s generic fallback is active for these cases, so the system should not be described as a complete misconception detector.

## 5.5 Verification status

The evaluation output was generated and reviewed. Python bytecode compilation for the backend and evaluation script completed successfully. These checks establish that the authored evaluation path runs and that the examined Python modules are syntactically compilable.

The following are **not** claimed by this report:

- frontend end-to-end test coverage;
- Docker escape resistance or a complete security certification;
- diagnosis precision, recall, F1, or calibration;
- recommendation relevance;
- learner satisfaction;
- learning gain, retention, or transfer;
- production readiness.

## 5.6 Testing limitations and improvements

The probe set is small, authored by the project developer, and not representative of actual learner code. It has no independent ground-truth adjudication. To improve validation:

1. define a diagnosis taxonomy before collecting examples;
2. collect diverse submissions with informed consent and privacy controls;
3. have at least two reviewers label the likely primary issue;
4. resolve disagreements and freeze the evaluation mapping;
5. use a held-out test set;
6. report per-class precision, recall, macro-F1, confusion matrices, and false-positive examples;
7. evaluate recommendations across multiple simulated and real learner profiles;
8. test post-practice performance on unseen but concept-equivalent problems.

## 5.7 Demonstration procedure

For a live demonstration:

1. Start the API, frontend, Docker engine, and runner image.
2. Open a beginner console exercise and submit a correct solution.
3. Show test outcomes, diagnosis evidence, saved attempt, and updated progress.
4. Submit an intentionally incorrect solution and explain the evidence without treating the diagnosis as certainty.
5. Request the conceptual hint, then the structural hint, and show that solution reveal is explicit.
6. Open progress to show concept mastery and prerequisites.
7. Display the recommended exercise and its rationale.
8. Demonstrate a web exercise and explain that its browser checks are client-reported.

Screenshots should be captured from the actual running application and inserted into the final formatted report.

---

# CHAPTER 6 — RESULTS AND DISCUSSION

## 6.1 Functional results

The project achieves its primary prototype objective: it connects exercise selection, editing, execution or browser checking, diagnosis, hints, persistence, mastery estimation, and recommendation in one local workflow. The architecture and code organize these capabilities into understandable modules rather than a single opaque service.

The catalog result confirms a usable breadth of 39 authored practice items. The multi-language console design allows a learner to practice the same general problem-solving objective in C, Python, or Java where configured. The UI Studio adds a separate practice mode for web structure, styling, and interaction.

## 6.2 Cognitive-computing results

The prototype demonstrates the following cognitive-computing behaviors:

- **Observation:** test results and selected code facts are collected.
- **Reasoning:** ordered rules map observations to possible explanations.
- **Knowledge representation:** concepts and prerequisite relationships are explicit.
- **Learner modeling:** each concept receives a probability and attempt count.
- **Adaptation:** recommendations use attempt history and prerequisite mastery.
- **Scaffolding:** help increases from concept-level guidance to code-level guidance.
- **Explainability:** the response includes evidence and a disclaimer.

These results show implementation of the design, not proof that the design improves learning.

## 6.3 Diagnosis discussion

The successful, syntax-error, and index-error probes show that status-specific branches provide useful factual feedback. The generic mismatch results also expose a weakness: output mismatch alone does not distinguish an incorrect algorithm from a missing return, an off-by-one boundary, or a wrong condition when the specialized conditions are not triggered.

This limitation is preferable to an unsupported confident diagnosis, but it reduces tutoring value. The next implementation step should be to expand language-aware structural analysis and add independent labels before increasing the confidence or specificity of diagnoses. The system should continue to phrase such outputs as possibilities.

## 6.4 Learner-model discussion

The BKT-style update provides a compact way to represent change over attempts. A correct submission increases a concept estimate, while an incorrect submission decreases it before a learning transition. The explicit parameters make the behavior easy to inspect and reproduce.

However, the estimate should not be interpreted as a validated probability that a learner truly knows a concept. The model currently treats all tests in a submission as one binary observation, does not account for hints, does not distinguish difficulty, and does not model forgetting or transfer. Calibration against learner data is required before reporting mastery as an assessment result.

## 6.5 Recommendation discussion

The recommendation policy is explainable: it prefers unattempted exercises whose prerequisites appear sufficiently practiced and then favors the lowest estimated concept mastery. The fallback rules prevent the system from becoming empty when no candidate meets the threshold.

The policy may nevertheless recommend a task that is too easy, too difficult, or not aligned with the learner’s immediate goal. It also relies on authored prerequisite relationships and a fixed threshold. Expert review and learner interaction data should be used to assess recommendation relevance.

## 6.6 Safety, privacy, and deployment discussion

The Docker runner is a meaningful safety feature because submitted console code is not executed inside the API process and is constrained by network, filesystem, capability, resource, and timeout controls. The API also validates source size and language/file choices.

The prototype remains local and single-user. It has no authentication, authorization, tenant isolation, abuse monitoring, or production security review. Web checks are client-reported, so they should not be used for trusted grading. Deployment beyond local practice would require a threat model, security testing, stronger isolation review, and privacy documentation.

## 6.7 Future work

Priority improvements are:

1. expand diagnosis rules for common logic errors across Python, Java, and C;
2. preserve structured traces such as input, output, and failing test position;
3. incorporate hint use and partial performance into learner modeling;
4. calibrate BKT parameters using an approved learner dataset;
5. evaluate recommendation quality with expert ratings and learner outcomes;
6. add automated frontend and API integration tests;
7. add authentication and learner-scoped storage if multi-user deployment is required;
8. conduct a security review of runner and browser-preview boundaries;
9. run a controlled or quasi-experimental study of learning gain using unseen tasks.

---

# CONCLUSION

Code Matrix is a functioning local cognitive-computing prototype for programming practice. It combines a catalog of 39 exercises, multi-language console evaluation, web-project checks, deterministic evidence-based diagnosis, progressive hints, BKT-style concept estimates, prerequisite representation, attempt history, and adaptive recommendations. Its modular design makes the relationship between learner activity, system observation, tutor response, and next-step recommendation visible.

The implementation and authored probes establish that the main workflow operates and that several important execution states are handled distinctly. They also show that the diagnosis layer is still limited: three of six logical-failure probes received a generic output-mismatch result. Consequently, the project should be presented as an explainable prototype and not as a validated educational intervention or accurate misconception classifier.

The most important contribution is the integration of cognitive-computing ideas into a practical, inspectable coding workspace while maintaining honest boundaries around evidence. Future work should focus on independently labeled diagnosis evaluation, calibrated learner modeling, recommendation studies, broader automated testing, and stronger deployment security. With those additions, the prototype could progress from a demonstrable project to a rigorously evaluated intelligent programming-practice system.

---

# REFERENCES

1. Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the acquisition of procedural knowledge. *User Modeling and User-Adapted Interaction, 4*, 253–278. https://doi.org/10.1007/BF01099821
2. Anderson, J. R., Corbett, A. T., Koedinger, K. R., & Pelletier, R. (1995). Cognitive tutors: Lessons learned. *The Journal of the Learning Sciences, 4*(2), 167–207. https://doi.org/10.1207/s15327809jls0402_2
3. VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist, 46*(4), 197–221. https://doi.org/10.1080/00461520.2011.611369
4. Aamodt, A., & Plaza, E. (1994). Case-based reasoning: Foundational issues, methodological variations, and system approaches. *AI Communications, 7*(1), 39–59. https://doi.org/10.3233/AIC-1994-7104
5. Python Software Foundation. (2026). *The Python `ast` module documentation*. https://docs.python.org/3/library/ast.html
6. FastAPI. (2026). *FastAPI documentation*. https://fastapi.tiangolo.com/
7. Docker Inc. (2026). *Docker run reference*. https://docs.docker.com/reference/cli/docker/container/run/
8. React. (2026). *React documentation*. https://react.dev/
9. Microsoft. (2026). *Monaco Editor*. https://microsoft.github.io/monaco-editor/
10. Code Matrix source code and authored exercise catalog: `backend/tutor.py`, `backend/main.py`, `backend/runner.py`, `backend/models.py`, catalog modules, and `scripts/evaluate_tutor.py`.
11. *IA3 Rubrics—Cognitive Computing*. Course rubric supplied for the project, October 2026.

## Submission checklist

- Add student and institutional details.
- Insert genuine screenshots from the running application.
- Attach the required certification separately, if applicable.
- Confirm the institution’s citation and AI-assistance disclosure policy.
- Re-run the evaluation script before submission and retain the generated results.
- Review every claim against the actual application behavior.
