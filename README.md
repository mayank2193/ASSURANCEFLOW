# Airbnb Assurance Flow

A requirements-to-evidence assurance pipeline built with [`kane-cli`](https://www.npmjs.com/package/@testmuai/kane-cli) for the Airbnb Search & Routing PRD. A PDF requirements doc goes in one end; a sealed, auditable evidence pack comes out the other, with every acceptance criterion traced through a designed test to a proven (or failed) run.

## What's in the repo

| Path | What it is |
|---|---|
| `Airbnb_Search_Routing_PRD.pdf` | The source requirements doc |
| `.context/` | The assurance graph — sources, use-cases, ACs, scenarios, tests, and the review/commit history that produced them |
| `.testmuai/tests/*_test.md` | The designed, runnable tests (1:1 with committed test nodes in the graph) |
| `.testmuai/variables/airbnb.json` | Runnable test data (`{{homepage_url}}`, `{{check_in_date}}`, …) |
| `.testmuai/evidence/*.evidence` | Sealed evidence packs from past runs |
| `.github/workflows/assurance-pipeline.yml` | The 6-stage CI pipeline |
| `.github/actions/kane-setup/` | Composite action: installs kane-cli + Chrome, authenticates |
| `.github/scripts/` | Helper scripts the workflow calls (auto-approve, design loop, test runner) |

## The flow

```mermaid
flowchart LR
    PDF["📄 Airbnb_Search_Routing_PRD.pdf"]

    subgraph S1["1 · Ingest from PDF"]
        direction TB
        A1["context ingest"] --> A2["context extract"] --> A3["approve use-cases"]
    end

    subgraph S2["2 · Design test cases"]
        direction TB
        B1["design tests\n(per use-case)"] --> B2["ACs + scenarios\n+ 1:1 tests"] --> B3["approve derived nodes"]
    end

    subgraph S3["3 · Run\n(author & replay)"]
        direction TB
        C1["testmd run\nper _test.md"] --> C2{"seen\nbefore?"}
        C2 -->|no| C3["author the flow"]
        C2 -->|yes| C4["replay from\nrecording"]
        C3 --> C5["evidence pack\n+ share URL"]
        C4 --> C5
    end

    subgraph S4["4 · Coverage"]
        direction TB
        D1["cover gaps"] --> D2["designed × proven\nribbon"] --> D3{"≥ 70%\ncomplete?"}
    end

    subgraph S5["5 · Maintain\n(rerun-regression)"]
        direction TB
        E1["maintain reconcile\n(if PRD changed)"] --> E2["review card\n(human approves)"]
        E3["nightly cron /\nmanual dispatch"] --> E4["full regression\nrerun"]
    end

    subgraph S6["6 · Evidence"]
        direction TB
        F1["evidence merge"] --> F2["evidence validate\n(L1 profile)"] --> F3["sealed .evidence\nbundle (90d artifact)"]
    end

    PDF --> S1 --> S2 --> S3 --> S4 --> S6
    S4 -.gate: pct < 70%.-> X["❌ fail pipeline"]
    S3 --> S5 --> S6

    style X fill:#f66,color:#fff
```

Stage 3 is where the "author once, replay forever" model pays off: the first CI run against a new test authors it live (an LLM-driven agent actually drives the browser); every run after that replays the recorded steps deterministically — no LLM cost, no flakiness from re-reasoning — until the test's prose or an earlier step changes, which invalidates and re-authors from that point down.

## Stage-by-stage

1. **Ingest from PDF** — `kane-cli context ingest <pdf> --mode ci` lands the source, `context extract` proposes use-cases from it, and a script auto-approves them (nobody's watching an interactive review chat in CI).
2. **Design test cases** — walks every use-case the coverage ribbon flags as incomplete and runs `kane-cli design tests --use-case <id>`, which proposes ACs, scenarios, and a 1:1 test per scenario, then auto-approves the new nodes.
3. **Run (author and replay)** — `kane-cli testmd run` over every `*_test.md`. Pass/fail, duration, and a Test Manager share URL land in the job summary; every evidence pack produced is staged for stage 6.
4. **Coverage** — `kane-cli cover gaps` reports the dual-axis ribbon (% of ACs with a live, passing test vs. % of use-cases fully designed). The job fails the pipeline if completeness drops below 70%.
5. **Maintain (rerun-regression)** — on a nightly cron or manual dispatch: optionally reconciles the graph against an updated PRD (`maintain reconcile`, which only *stages* a plan — nothing commits without a human review), then reruns the entire suite as a regression pass.
6. **Evidence** — merges every evidence pack from stages 3 and 5 into one sealed pack (`kane-cli evidence merge`), validates it (`evidence validate --profile L1`), and uploads it as a 90-day CI artifact — the audit trail for "what did we actually prove, and when."

## Running it

Requires two repo secrets (Settings → Secrets and variables → Actions) — reused from the existing LambdaTest credentials:

- `LT_USERNAME`
- `LT_ACCESS_KEY`

Triggers:
- **Push to `main`** touching a PDF, `.testmuai/tests/**`, or the workflow itself → stages 1–4, 6
- **Pull request** → stages 1–4, 6
- **Nightly cron** (`0 3 * * *`) → stage 5 (regression) → 6
- **Manual dispatch** → all stages; pass `reconcile_pdf` to reconcile against an updated PRD

## Local usage

```bash
export KANE_CLI_USER_AGENT=your-tool-name
kane-cli login --username <user> --access-key <key>

kane-cli context ingest ./Airbnb_Search_Routing_PRD.pdf --mode ci
kane-cli context extract --mode ci
kane-cli design tests --use-case uc-1        # interactive in a TTY
kane-cli testmd run .testmuai/tests/<file>_test.md --agent
kane-cli cover gaps
```
