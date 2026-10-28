"""Browser-preview exercises for the dedicated UI Studio."""


def ui_exercise(*, id, title, category, description, starter_files, tests, tags, solution):
    return {
        "id": id,
        "title": title,
        "description": description,
        "starter_code": starter_files["index.html"],
        "function_name": "",
        "tests": tests,
        "solution": solution,
        "concept": "Web structure and interaction",
        "category": category,
        "difficulty": "Beginner",
        "tags": tags,
        "language": "web",
        "execution_mode": "browser",
        "entry_point": "index.html",
        "starter_files": starter_files,
        "language_starters": None,
        "language_solutions": None,
        "examples": [],
        "constraints": [],
    }


UI_EXERCISES = [
    ui_exercise(
        id="ui-faq-accordion",
        title="Build an FAQ accordion",
        category="JavaScript Interaction",
        description="Style the FAQ panel and make the button reveal the answer: `You can practice every day.` Use the HTML, CSS, and JavaScript tabs.",
        starter_files={
            "index.html": "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>FAQ</title></head><body><main class=\"faq-card\"><h1>Frequently asked question</h1><h2>How do I improve?</h2><button id=\"reveal-answer\" type=\"button\" aria-expanded=\"false\">Show answer</button><p id=\"answer\" aria-live=\"polite\"></p></main></body></html>\n",
            "style.css": "/* Give .faq-card a clear layout, spacing, and rounded corners. */\n",
            "script.js": "// When #reveal-answer is clicked, show the answer in #answer.\n",
        },
        tests=[
            {"id": "faq-card", "label": "The FAQ panel is present", "type": "selector-exists", "selector": ".faq-card"},
            {"id": "faq-heading", "label": "The question is visible", "type": "text-includes", "selector": "h2", "value": "How do I improve?"},
            {"id": "faq-style", "label": "The FAQ panel is styled", "type": "style-not-default", "selector": ".faq-card", "property": "borderRadius"},
            {"id": "faq-click", "label": "The answer appears after clicking", "type": "click-changes", "button": "#reveal-answer", "target": "#answer", "expected": "You can practice every day."},
        ],
        tags=["html", "css", "javascript", "events", "accessibility"],
        solution="""/* style.css */
body { margin: 0; padding: 2rem; font-family: system-ui, sans-serif; background: #f4f2ff; }
.faq-card { max-width: 38rem; margin: 3rem auto; padding: 2rem; border-radius: 1rem; background: white; box-shadow: 0 12px 36px #21164a1c; }
button { padding: .7rem 1rem; border: 0; border-radius: .5rem; background: #7059de; color: white; cursor: pointer; }

// script.js
document.querySelector('#reveal-answer').addEventListener('click', () => {
  document.querySelector('#answer').textContent = 'You can practice every day.';
  document.querySelector('#reveal-answer').setAttribute('aria-expanded', 'true');
});""",
    ),
    ui_exercise(
        id="ui-pricing-card",
        title="Design a pricing card",
        category="CSS Styling",
        description="Turn the plan details into a clear pricing card. Add a rounded card style and make the Choose plan button show `Plan selected` below it.",
        starter_files={
            "index.html": "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Starter plan</title></head><body><main class=\"pricing-card\"><p>CODEMIND PLUS</p><h1>Starter plan</h1><p class=\"price\">$9 <span>per month</span></p><ul><li>Unlimited practice</li><li>Progress tracking</li></ul><button id=\"choose-plan\" type=\"button\">Choose plan</button><p id=\"plan-message\" aria-live=\"polite\"></p></main></body></html>\n",
            "style.css": "/* Style the pricing card, price, feature list, and button. */\n",
            "script.js": "// Update #plan-message when #choose-plan is clicked.\n",
        },
        tests=[
            {"id": "pricing-card", "label": "The pricing card is present", "type": "selector-exists", "selector": ".pricing-card"},
            {"id": "pricing-price", "label": "The monthly price is shown", "type": "text-includes", "selector": ".price", "value": "$9"},
            {"id": "pricing-style", "label": "The card has rounded corners", "type": "style-not-default", "selector": ".pricing-card", "property": "borderRadius"},
            {"id": "pricing-click", "label": "The plan button responds", "type": "click-changes", "button": "#choose-plan", "target": "#plan-message", "expected": "Plan selected"},
        ],
        tags=["html", "css", "layout", "buttons"],
        solution="""/* style.css */
body { margin: 0; padding: 2rem; font-family: system-ui, sans-serif; background: #f5f6fb; }
.pricing-card { max-width: 22rem; margin: 2rem auto; padding: 2rem; border: 1px solid #e6e5ef; border-radius: 1.25rem; background: white; box-shadow: 0 14px 40px #20233a18; }
.price { color: #604bd1; font-size: 2.5rem; font-weight: 700; }
.price span { color: #777; font-size: 1rem; font-weight: 400; }
button { padding: .75rem 1rem; border: 0; border-radius: .5rem; background: #7059de; color: white; cursor: pointer; }

// script.js
document.querySelector('#choose-plan').addEventListener('click', () => {
  document.querySelector('#plan-message').textContent = 'Plan selected';
});""",
    ),
    ui_exercise(
        id="ui-testimonial-slider",
        title="Create a testimonial switcher",
        category="JavaScript Interaction",
        description="Build a testimonial card. Clicking Next should replace the current quote with `Design is how it works.` Style the quote card so it is easy to read.",
        starter_files={
            "index.html": "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Testimonials</title></head><body><main class=\"quote-card\"><h1>What learners say</h1><blockquote id=\"quote\">Small steps make a big difference.</blockquote><button id=\"next-quote\" type=\"button\">Next</button></main></body></html>\n",
            "style.css": "/* Make the quote card readable and visually distinct. */\n",
            "script.js": "// Change #quote to the next testimonial when #next-quote is clicked.\n",
        },
        tests=[
            {"id": "quote-card", "label": "The testimonial card is present", "type": "selector-exists", "selector": ".quote-card"},
            {"id": "quote-content", "label": "A testimonial is visible", "type": "text-includes", "selector": "blockquote", "value": "Small steps"},
            {"id": "quote-style", "label": "The quote card has rounded corners", "type": "style-not-default", "selector": ".quote-card", "property": "borderRadius"},
            {"id": "quote-click", "label": "Next changes the testimonial", "type": "click-changes", "button": "#next-quote", "target": "#quote", "expected": "Design is how it works."},
        ],
        tags=["html", "css", "javascript", "events", "content"],
        solution="""/* style.css */
body { padding: 2rem; font-family: system-ui, sans-serif; background: #f4f2ff; }
.quote-card { max-width: 38rem; margin: 2rem auto; padding: 2rem; border-radius: 1rem; background: white; box-shadow: 0 12px 36px #21164a1c; }
blockquote { color: #4d456d; font-size: 1.5rem; line-height: 1.5; }
button { padding: .65rem 1rem; border: 0; border-radius: .5rem; background: #7059de; color: white; cursor: pointer; }

// script.js
const quotes = ['Small steps make a big difference.', 'Design is how it works.'];
let quoteIndex = 0;
document.querySelector('#next-quote').addEventListener('click', () => {
  quoteIndex = (quoteIndex + 1) % quotes.length;
  document.querySelector('#quote').textContent = quotes[quoteIndex];
});""",
    ),
    ui_exercise(
        id="ui-responsive-hero",
        title="Build a responsive landing hero",
        category="Responsive Design",
        description="Create a welcoming landing-page hero with a heading, supporting copy, and a call-to-action. Use CSS to give the content a readable width, spacing, and a responsive layout.",
        starter_files={
            "index.html": "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Learn by building</title></head><body><main class=\"hero\"><div class=\"hero-copy\"><p class=\"eyebrow\">CODEMIND LEARNING</p><h1>Build something you understand.</h1><p>Practice one concept, test your work, and keep moving forward.</p><a class=\"hero-action\" href=\"#start\">Start learning</a></div><div class=\"hero-art\" aria-hidden=\"true\">&lt;/&gt;</div></main></body></html>\n",
            "style.css": "/* Create a responsive two-column hero that stacks on narrow screens. */\n",
            "script.js": "// No JavaScript is required for this layout challenge.\n",
        },
        tests=[
            {"id": "hero", "label": "The landing hero is present", "type": "selector-exists", "selector": ".hero"},
            {"id": "hero-heading", "label": "The main heading is visible", "type": "text-includes", "selector": "h1", "value": "Build something you understand."},
            {"id": "hero-action", "label": "The call-to-action is present", "type": "selector-exists", "selector": ".hero-action"},
            {"id": "hero-layout", "label": "The hero has a readable width", "type": "style-not-default", "selector": ".hero", "property": "maxWidth"},
        ],
        tags=["html", "css", "responsive", "layout"],
        solution="""/* style.css */
* { box-sizing: border-box; }
body { margin: 0; font-family: system-ui, sans-serif; color: #27243a; background: #f5f4fb; }
.hero { max-width: 70rem; min-height: 28rem; margin: 2rem auto; padding: clamp(1.5rem, 5vw, 4rem); border-radius: 1.5rem; background: white; display: grid; grid-template-columns: 1.4fr 1fr; align-items: center; gap: 2rem; }
.hero h1 { max-width: 12ch; font-size: clamp(2rem, 5vw, 4rem); line-height: 1.05; }
.hero-action { display: inline-block; padding: .8rem 1.1rem; border-radius: .6rem; color: white; background: #7059de; text-decoration: none; }
.hero-art { display: grid; place-items: center; min-height: 14rem; border-radius: 1rem; color: #7059de; background: #f0edff; font-size: 4rem; }
@media (max-width: 650px) { .hero { grid-template-columns: 1fr; } .hero-art { min-height: 8rem; } }

// script.js
// This layout works without JavaScript.""",
    ),
]
