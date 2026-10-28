# Code Matrix: Cognitive Computing Project Report

**Course:** Cognitive Computing (23DC2037)  
**Institution:** Karunya Institute of Technology and Sciences  
**Project type:** Skill Based Evaluation  
**Prepared:** October 2026

> Complete student names, registration numbers, faculty details, signatures, and any institution-specific cover pages before submission. This report is an implementation-grounded draft; validate it against the actual running application and course requirements.

## Abstract

Code Matrix is a local coding-practice workspace designed to help learners practice programming and receive feedback that supports their next attempt. It contains 39 catalog exercises spanning programming fundamentals, data structures and algorithms, and small web projects. Learners submit code or web files, run checks, inspect evidence about outcomes, request progressive hints, review prior attempts, see concept mastery estimates, and receive a recommended exercise.

The cognitive computing design combines deterministic rule-based diagnosis, limited Python abstract syntax tree observations, a concept prerequisite graph, Bayesian Knowledge Tracing (BKT)-style mastery updates, and prerequisite-aware recommendation logic. Python, Java, and C code executes in disposable Docker containers with resource controls. Web work is previewed in a sandboxed browser frame. Explanations are deterministic templates; no language model is used. The design emphasizes inspectability and formative feedback.

The repository includes six authored evaluation probes and a catalog inventory script. These are engineering checks, not a representative learner dataset. No external dataset, student study, calibrated diagnosis metric, or learning-gain result is available. The current project therefore demonstrates an implemented prototype but does not establish educational effectiveness.

## Chapter 1 — Introduction

Programming learners commonly encounter errors that are difficult to interpret from a pass/fail result alone. An incorrect output may arise from a missing return statement, a faulty loop, a mistaken condition, or a misunderstanding of the task. Compiler and runtime messages explain some failures, but do not necessarily connect them to the programming concept being practiced.

Code Matrix addresses this problem with an interactive practice workflow. A learner chooses an exercise, writes code in an editor, runs tests, reviews test outcomes and a rule-based diagnosis, and can request conceptual or structural hints before explicitly revealing a worked solution. The system records attempts and updates a concept estimate used in progress views and exercise recommendations.

### 1.1 Problem statement

How can an individual programming practice environment combine execution feedback, explainable diagnosis, progressive help, a learner model, and concept-aware recommendations to support iterative practice?

### 1.2 Objectives

- Provide a browser-based coding workspace for Python, Java, C, HTML, CSS, and JavaScript practice.
- Evaluate console submissions with exercise test cases and web projects with browser checks.
- Give evidence-based, cautious explanations of observed failures.
- Offer progressive hints and reveal worked solutions only on explicit request.
- Maintain per-concept practice estimates and prerequisite relationships.
- Recommend exercises with an explanation of the choice.
- Preserve attempts and progress for a local learner profile.
- Keep execution isolated from the API process and document prototype limitations.

### 1.3 Scope

This is a local prototype for formative individual practice. It is not a classroom-management system, multi-user service, proctored assessment, or validated measure of learner knowledge. It currently has no user authentication. Diagnosis is strongest for execution status and supplied test outcomes; structural Python observations are deliberately limited.

## Chapter 2 — Cognitive Computing Concepts and Background

Code Matrix uses cognitive computing concepts in a small, explicit software design rather than a trained cognitive or language model.

### 2.1 Learner modeling and knowledge tracing

Each concept has an estimated mastery probability and attempt count. The update in `backend/tutor.py` uses BKT-style terms: prior knowledge, learning, guessing, and slipping. Defaults are initial probability 0.25, learning 0.12, guess 0.20, and slip 0.10. A fully passing submission is treated as a correct observation; any incomplete submission is treated as incorrect. These assumptions are documented in the README and have not been fitted or calibrated using learner data.

### 2.2 Knowledge representation

`PREREQUISITES` represents concept dependencies as a directed graph. Examples include Arrays & Hashing as a prerequisite for Two Pointers and Binary Search, and Two Pointers plus Arrays & Hashing for Sliding Window. The graph appears in the progress interface and is used by recommendation logic.

### 2.3 Reasoning and cognitive diagnosis

The tutor combines test outcomes and runtime/compiler status with a small set of Python AST facts: whether code contains a return, loop, conditional, or recursive call. Deterministic rules produce a diagnosis title, evidence, and heuristic confidence. These are descriptions of observed code and outcomes, not assertions about a learner's intent. A single diagnostic label is not proof of a persistent misconception.

### 2.4 Adaptive recommendation

The recommender prioritizes unattempted exercises whose prerequisites have estimated mastery at or above 0.35, then favors the lowest estimated concept mastery. It falls back to other unattempted tasks if no candidate meets the prerequisite threshold, and to the full catalog after all items have been attempted. It provides a textual rationale.

### 2.5 Scaffolding and feedback

Conceptual hints prompt the learner to consider an idea; structural hints point to a more specific implementation action; the worked solution is gated behind an explicit request. Submission history, test results, diagnosis evidence, and progress estimates create a feedback loop for subsequent practice.

### 2.6 Related research

Bayesian Knowledge Tracing provides a probabilistic model for estimating skill acquisition from sequences of responses. Intelligent tutoring research motivates representing domain knowledge and responding to learner evidence. Code Matrix adapts these broad ideas in a lightweight programming tutor; it does not implement a full production cognitive tutor or claim a novel algorithm.

## Chapter 3 — Data, Methodology, and Architecture

### 3.1 Data sources and catalog

The practice bank is authored and stored in project source files, principally `backend/catalog.py`, `backend/dsa_catalog.py`, `backend/extended_dsa.py`, `backend/multilang_fundamentals.py`, and `backend/ui_catalog.py`. It contains 39 exercises, categorized across fundamentals, DSA topics, and browser-based web projects. Exercise records include prompts, concepts, difficulty, starter code or files, tests, and solutions. The catalog inventory by category and difficulty is generated in `reports/evaluation_results.json`.

This content is not an externally collected dataset and does not contain a labeled corpus of student misconceptions. Runtime submissions are local application data and are not used as a research dataset in this report. No demographic information is included. There is no training, validation, or test split because the current system does not train a statistical classifier.

### 3.2 Input preparation

API request models validate submission fields. The backend checks exercise identity, supported language, required files, and source size. Console code runs against exercise-specific test inputs. Python submissions can be parsed into ASTs for structural observations. Web work uses a sandboxed iframe with a restrictive content policy; browser checks examine selectors, text, computed style, and interactions. Browser check results are client-reported and are appropriate for practice feedback, not high-stakes grading.

### 3.3 System architecture

1. React and TypeScript present the dashboard, catalog, editor, progress, and attempt history.
2. Monaco Editor collects console code or multi-file web projects.
3. FastAPI validates submissions, selects the exercise test cases, and orchestrates evaluation.
4. Python, Java, and C run in disposable Docker containers configured with no network, a read-only root filesystem, resource limits, and bounded execution. Student code is not executed inside the FastAPI process.
5. The tutor evaluates returned status and test outcomes and applies deterministic diagnosis rules. Python AST observations support selected structural diagnoses.
6. SQLAlchemy persists exercises, submissions, and mastery estimates to SQLite by default or PostgreSQL when configured.
7. Mastery and prerequisites feed the recommendation endpoint; the user interface displays the recommendation reason.

The architecture diagram is provided at `assets/architecture.png` and should be checked for legibility in the final formatted report.

### 3.4 Submission workflow

An exercise is selected and edited; the learner runs checks; the system returns outcomes; a diagnosis describes evidence; the learner may request hints or a solution; the attempt is saved; mastery is updated; and the recommendation endpoint selects a next task. Console test results are produced by the server-side runner. Web checks execute in the learner's browser and are sent to the API for storage and feedback.

### 3.5 Core algorithm summaries

For an observation `correct`, the BKT-style update first computes a Bayesian posterior using the configured guess and slip terms, then adds the learning transition. The implementation clamps the result between 0.01 and 0.99. This simplified update does not account for hint usage when updating mastery.

For recommendations, the system excludes attempted exercises where possible, filters remaining exercises by prerequisite mastery threshold, and selects the candidate with the lowest estimated mastery. It falls back when the eligible set is empty and includes a reason in the response.

## Chapter 4 — Implementation

### 4.1 Technology stack

The frontend uses React, TypeScript, Vite, and Monaco Editor. The backend uses Python, FastAPI, Pydantic, SQLAlchemy, and Python AST. SQLite and PostgreSQL are supported for persistence. Docker runner images provide isolated Python, Java, and C execution. The web preview is a sandboxed iframe.

### 4.2 Main modules

- `backend/main.py`: API routes, submission orchestration, persistence, mastery, and recommendation endpoints.
- `backend/tutor.py`: prerequisite map, AST facts, diagnoses, hints, and BKT-style updates.
- `backend/*catalog*.py`: exercise catalogs, tests, and starter content.
- `backend/runner.py` and `backend/stdio_runner.py`: isolated program execution.
- `backend/models.py` and `backend/db.py`: persistent records and database setup.
- `src/App.tsx`: application pages and learner interactions.
- `assets/architecture.png`: system architecture diagram.

### 4.3 Application functions

The UI includes an overview, Code Studio, UI Studio, progress view, and attempt history. The API supports exercise retrieval, submission, hints, attempt history, mastery, concept graph, recommendation, and progress. The frontend locally saves unfinished editor drafts by exercise and language. The project currently supports one local learner profile.

### 4.4 Safety and privacy considerations

Console code executes in disposable containers with resource controls and no network access. The API fails closed when Docker is unavailable. AST parsing is used for analysis, not as a security mechanism. Web preview checks are client-side practice feedback. Authentication and learner-scoped multi-user storage are not implemented. These constraints should be considered before any deployment beyond local use.

## Chapter 5 — Testing and Evaluation

### 5.1 Reproducible probe script

Run `python scripts/evaluate_tutor.py` from the repository root to regenerate `reports/evaluation_results.json`. The script inventories the 39 catalog exercises by category and difficulty and sends six fixed authored scenarios through the production `diagnose` function: a passing submission, a missing-return example, a loop-boundary-like mismatch, a wrong output, a syntax error, and an index runtime error.

### 5.2 Current results

The run completed successfully and reported 39 catalog entries. Of six probes, the observed diagnosis titles were: one “All checks passed,” three “Some expected output did not match,” one syntax issue, and one possible out-of-bounds index. This is behavior on a small hand-authored software probe set only. It is not diagnosis accuracy, precision, recall, F1, recommendation quality, or evidence of learning gain.

The probes reveal that several distinct logical mistakes currently receive the same generic output-mismatch diagnosis. The missing-return and loop-boundary probes did not receive their intended specialized diagnosis. This is a concrete limitation and an opportunity for future improvements to diagnostic rules and their evaluation.

### 5.3 Evaluation design needed for stronger claims

For a meaningful diagnosis study, define a taxonomy, collect a larger varied set of representative submissions with appropriate consent, have a reviewer label expected diagnosis classes, and resolve disagreements. Freeze the label mapping before evaluation, keep a held-out set, report per-class precision, recall, macro-F1, and a confusion matrix, and include false-positive examples. For recommendation relevance, define a separate rubric and evaluate decisions across multiple learner profiles. For learning effectiveness, an appropriately approved study would need a comparison design and unseen post-practice tasks. Do not invent or infer these results from the current probes.

### 5.4 Verification status

The evaluation script was executed and its output was reviewed. Python bytecode compilation for backend and script files completed successfully. These checks establish that the script runs and the Python modules compile; they do not establish frontend correctness, runner security, diagnosis quality, or educational impact. No automated test suite or classroom study is claimed here.

### 5.5 Live demonstration sequence

1. Start the backend and frontend using the README instructions.
2. Open a beginner exercise and submit a correct solution; show test results and saved attempt.
3. Submit an intentionally incorrect solution; discuss the observed evidence and the possibility that a diagnosis may be generic.
4. Request the conceptual hint, then the structural hint, and show that the worked solution requires an explicit action.
5. Open Learning Progress and show the concept estimate and prerequisite graph.
6. Request or view the next exercise and explain the displayed recommendation reason.
7. If time permits, demonstrate a web project and clarify the client-reported nature of browser checks.

Insert screenshots captured from the actual running Code Matrix application after performing this sequence. Do not use mock screenshots as evidence of a live run.

## Chapter 6 — Discussion, Limitations, and Future Work

Code Matrix integrates a functioning practice workflow with several cognitive computing ideas: a concept knowledge representation, rule-based reasoning, a learner model, scaffolding, and an adaptive recommendation. Its transparent deterministic methods make it possible to trace feedback to test outcomes and code observations.

The current evidence is limited. The catalog is hand-authored; no external dataset or learner misconception corpus is used. The AST feature set is small and Python-only. The diagnosis rules can miss real causes or produce generic feedback, as shown by the probes. Confidence numbers are heuristic and uncalibrated. Mastery parameters are assumptions, and binary all-tests-passed observations are coarse. Recommendations have not been evaluated with learners. Browser-based results are client-reported. There is no user authentication, and no study measures learning outcomes.

Future work should first improve and test diagnosis rules against an independently labeled submission set. Additional work includes broader language-aware structural analysis, stronger mastery evidence and parameter calibration, recommendation relevance evaluation, larger tested exercise content, multi-user authentication and privacy controls, and a controlled study of learning outcomes with appropriate institutional review.

## Conclusion

Code Matrix is a local cognitive computing prototype for coding practice. It evaluates submissions, provides cautious deterministic feedback and progressive hints, tracks BKT-style per-concept estimates, represents prerequisites, and recommends further practice. Its execution isolation and explainable rule structure support a practical demonstration. The current evaluation only checks six authored scenarios and a catalog inventory; it does not establish model performance or improved learning. Full claims about educational value require a larger independent evaluation and learner study.

## References

1. Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the acquisition of procedural knowledge. *User Modeling and User-Adapted Interaction, 4*, 253–278. https://doi.org/10.1007/BF01099821
2. Anderson, J. R., Corbett, A. T., Koedinger, K. R., & Pelletier, R. (1995). Cognitive tutors: Lessons learned. *The Journal of the Learning Sciences, 4*(2), 167–207.
3. VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist, 46*(4), 197–221.
4. Aamodt, A., & Plaza, E. (1994). Case-based reasoning: Foundational issues, methodological variations, and system approaches. *AI Communications, 7*(1), 39–59.
5. Code Matrix source code and authored catalog: `backend/tutor.py`, `backend/main.py`, `backend/catalog.py`, related catalog modules, and `scripts/evaluate_tutor.py`.
6. *IA3 Rubrics—Cognitive Computing*. Course rubric supplied by the student, October 2026.

## Submission checklist for the student

- Fill in names, registration number, signatures, and institutional formatting.
- Run the application and capture genuine screenshots for the demonstration chapter.
- Complete the prescribed online certification course to 100% and attach the valid certificate separately.
- Confirm citation and AI-assistance disclosure requirements with course policy and add any required references.
- Review the report, evaluation output, and project behavior yourself before submission; the repository probe results are not a substitute for a learner study.
