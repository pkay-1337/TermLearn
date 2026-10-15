/**
 * Extreme C - Chapter 09 Interactive Web Study Engine
 * Implements 5-Stage Micro-Stepping, Notional Machine State Visualizer,
 * Real-Time Heap Leak Detection, and Continuous Parameter Scrubbers.
 */

// Chapter 9 Micro-Steps Definition
const STEPS = [
  {
    stage: "Stage 1 of 5: Intuitive Puzzle",
    title: "Connecting Pointers to Memory",
    prompt: "A pointer holds a memory address. Assign <span class='var-blue'>ptr_a</span> to point to <span class='var-emerald'>car_1</span> at address <code>0x6020</code>:",
    renderWidget: (state) => `
      <div class="memory-split-grid">
        <div class="memory-pane">
          <div class="pane-title">Stack Frame</div>
          <div class="memory-row ${state.p1Target === 'node_1' ? 'targeted' : ''}">
            <span class="var-blue">car_t* ptr_a</span>
            <select id="p1-select" class="pointer-select">
              <option value="" ${!state.p1Target ? 'selected' : ''}>NULL (0x0)</option>
              <option value="node_1" ${state.p1Target === 'node_1' ? 'selected' : ''}>car_1 (0x6020)</option>
              <option value="node_2" ${state.p1Target === 'node_2' ? 'selected' : ''}>car_2 (0x6040)</option>
            </select>
          </div>
        </div>
        <div class="memory-pane">
          <div class="pane-title">Heap RAM</div>
          <div class="memory-row ${state.p1Target === 'node_1' ? 'targeted' : ''}">
            <div>
              <span class="var-emerald">car_1</span>
              <span style="color: var(--text-dim); font-size: 11px;">[0x6020]</span>
            </div>
            <span style="font-family: var(--font-mono); font-size: 12px;">speed: ${state.speed}</span>
          </div>
        </div>
      </div>
      <div id="diag-box" class="diagnostic-banner ${state.p1Target === 'node_1' ? 'success' : 'info'}">
        ${state.p1Target === 'node_1'
          ? "✅ <strong>Pointer Connected:</strong> <code>ptr_a</code> holds <code>0x6020</code>. Reading <code>*ptr_a</code> accesses <code>car_1</code>."
          : "👉 Select <code>car_1 (0x6020)</code> from the dropdown to connect <code>ptr_a</code> to its heap address."}
      </div>
    `,
    validate: (state) => state.p1Target === "node_1",
    onNext: (state) => { state.p2Target = "node_1"; }
  },
  {
    stage: "Stage 2 of 5: Pattern Induction",
    title: "Pointer Aliasing & Synchronized State",
    prompt: "Both <span class='var-blue'>ptr_a</span> and <span class='var-purple'>ptr_b</span> reference <span class='var-emerald'>car_1</span>. Scrub the speed slider and observe how mutating memory through one pointer instantly reflects in both:",
    renderWidget: (state) => `
      <div class="memory-split-grid">
        <div class="memory-pane">
          <div class="pane-title">Stack Frame (Aliases)</div>
          <div class="memory-row targeted">
            <span class="var-blue">ptr_a</span> ➔ <span style="font-family: var(--font-mono);">0x6020</span>
          </div>
          <div class="memory-row targeted">
            <span class="var-purple">ptr_b</span> ➔ <span style="font-family: var(--font-mono);">0x6020</span>
          </div>
        </div>
        <div class="memory-pane">
          <div class="pane-title">Heap Memory (Shared)</div>
          <div class="memory-row targeted">
            <div>
              <span class="var-emerald">car_1</span>
              <span style="color: var(--text-dim); font-size: 11px;">[0x6020]</span>
            </div>
            <span style="font-family: var(--font-mono); font-size: 13px; font-weight: bold; color: var(--var-amber);">
              ${state.speed} km/h
            </span>
          </div>
        </div>
      </div>

      <!-- Continuous Parameter Scrubber -->
      <div style="background: #111827; border: 1px solid var(--bg-subtle); border-radius: var(--radius-md); padding: 16px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px;">
          <span>Drag to scrub <code>ptr_a-&gt;speed</code>:</span>
          <span class="var-amber" style="font-family: var(--font-mono);">${state.speed} km/h</span>
        </div>
        <input type="range" id="speed-scrubber" min="40" max="220" value="${state.speed}" style="width: 100%; accent-color: var(--interactive-blue); cursor: pointer;">
      </div>

      <div class="formula-card">
        <div>
          <code>ptr_a-&gt;speed</code> = <span class="var-amber">${state.speed}</span>
        </div>
        <div>
          <code>ptr_b-&gt;speed</code> = <span class="var-amber">${state.speed}</span>
        </div>
      </div>

      <div class="diagnostic-banner success">
        🔗 <strong>Aliasing Active:</strong> Modifying <code>ptr_a-&gt;speed</code> modifies the physical bytes at <code>0x6020</code>. Reading through <code>ptr_b-&gt;speed</code> immediately returns the identical value!
      </div>
    `,
    validate: (state) => state.speed !== 100, // True once scrubbed
  },
  {
    stage: "Stage 3 of 5: Productive Failure",
    title: "The Dangling Loss: Unreferenced Heap Leak",
    prompt: "What happens if <span class='var-blue'>ptr_a</span> is redirected to <span class='var-amber'>car_2</span> while no other pointer holds <span class='var-emerald'>car_1</span>? Try pointing <span class='var-blue'>ptr_a</span> to <code>car_2</code>:",
    renderWidget: (state) => {
      const isLeaked = state.p1Target === "node_2" && state.p2Target !== "node_1";
      return `
        <div class="memory-split-grid">
          <div class="memory-pane">
            <div class="pane-title">Stack Pointers</div>
            <div class="memory-row">
              <span class="var-blue">ptr_a</span>
              <select id="leak-select" class="pointer-select">
                <option value="node_1" ${state.p1Target === 'node_1' ? 'selected' : ''}>car_1 (0x6020)</option>
                <option value="node_2" ${state.p1Target === 'node_2' ? 'selected' : ''}>car_2 (0x6040)</option>
              </select>
            </div>
            <div class="memory-row" style="color: var(--text-dim);">
              <span class="var-purple">ptr_b</span> ➔ NULL (0x0)
            </div>
          </div>
          <div class="memory-pane">
            <div class="pane-title">Heap RAM</div>
            <div class="memory-row ${isLeaked ? 'leaked' : 'targeted'}">
              <div>
                <span class="var-emerald">car_1</span>
                <span style="color: var(--text-dim); font-size: 11px;">[0x6020]</span>
              </div>
              ${isLeaked ? '<span class="var-danger" style="font-size: 11px; font-weight: bold;">🚨 UNREFERENCED</span>' : '<span style="font-size: 11px;">Owned</span>'}
            </div>
            <div class="memory-row ${state.p1Target === 'node_2' ? 'targeted' : ''}">
              <div>
                <span class="var-amber">car_2</span>
                <span style="color: var(--text-dim); font-size: 11px;">[0x6040]</span>
              </div>
              <span style="font-size: 11px;">${state.p1Target === 'node_2' ? 'Active' : 'Allocated'}</span>
            </div>
          </div>
        </div>

        <div class="diagnostic-banner ${isLeaked ? 'danger' : 'info'}">
          ${isLeaked
            ? "🚨 <strong>Memory Leak Triggered!</strong> Address <code>0x6020</code> has 0 references. Its pointer was lost before calling <code>free()</code>. That memory cannot be reclaimed until the process terminates!"
            : "Select <code>car_2</code> to trigger the lost pointer trap and observe the leak detector."}
        </div>
      `;
    },
    validate: (state) => state.p1Target === "node_2",
  },
  {
    stage: "Stage 4 of 5: Subgoal Naming",
    title: "The Ownership Invariant",
    prompt: "In systems programming, we eliminate leaks by enforcing an explicit invariant: <strong>Single Owner Responsibility</strong>.",
    renderWidget: () => `
      <div style="background: #111827; border: 1px solid var(--bg-subtle); border-radius: var(--radius-md); padding: 18px; line-height: 1.6;">
        <h4 style="color: var(--interactive-blue); margin-bottom: 8px;">Subgoal: "Transfer Ownership vs. Borrowing"</h4>
        <ul style="padding-left: 20px; font-size: 14px; color: var(--text-muted); display: flex; flex-direction: column; gap: 8px;">
          <li><strong style="color: var(--text-primary);">Exclusive Owner:</strong> Exactly one pointer variable is designated as the owner responsible for calling <code>free()</code>.</li>
          <li><strong style="color: var(--text-primary);">Borrower:</strong> Pointers can read or mutate the target, but MUST NOT free it.</li>
          <li><strong style="color: var(--text-primary);">Move / Hand-off:</strong> When transferring ownership, set the old pointer to <code>NULL</code> immediately.</li>
        </ul>
      </div>

      <details class="deep-dive" open>
        <summary>Why C Compilers Cannot Auto-Enforce This</summary>
        <p>Unlike Rust's borrow checker which enforces ownership at compile time, standard C compilers treat all pointers as raw addresses. The discipline must live inside the programmer's mental model and architectural conventions.</p>
      </details>

      <div class="diagnostic-banner success">
        💡 <strong>Core Principle:</strong> Every <code>malloc()</code> must have exactly one unambiguously designated <code>free()</code> site.
      </div>
    `,
    validate: () => true
  },
  {
    stage: "Stage 5 of 5: Formal Abbreviation",
    title: "C Code Execution & Lifecyle Stepper",
    prompt: "Step through the canonical C ownership lifecycle. Observe how the stack frame and heap addresses evolve together synchronously:",
    renderWidget: (state) => {
      const codeLines = [
        "car_t* ptr_a = malloc(sizeof(car_t)); // 1. Allocate owner",
        "ptr_a->speed = 120;                  // 2. Initialize state",
        "car_t* ptr_b = ptr_a;                // 3. Borrow reference",
        "free(ptr_a);                         // 4. Owner frees memory",
        "ptr_a = NULL; ptr_b = NULL;          // 5. Zero dangling pointers"
      ];
      return `
        <div class="code-container">
          ${codeLines.map((line, idx) => `
            <div class="code-line ${state.codeStep === idx ? 'highlight' : ''}">
              <span style="color: var(--text-dim); display: inline-block; width: 24px;">${idx + 1}</span>
              <span>${line}</span>
            </div>
          `).join('')}
        </div>

        <div style="display: flex; gap: 10px; margin-top: 10px;">
          <button id="step-code-btn" class="btn btn-secondary" style="flex: 1;">
            Step Forward (${state.codeStep + 1}/${codeLines.length})
          </button>
          <button id="reset-code-btn" class="btn btn-secondary">
            Reset
          </button>
        </div>

        <div class="diagnostic-banner ${state.codeStep >= 3 ? 'success' : 'info'}">
          ${state.codeStep === 0 ? "Line 1: <code>malloc</code> requests bytes on the Heap and returns address <code>0x6020</code> into <code>ptr_a</code>." :
            state.codeStep === 1 ? "Line 2: Dereferencing <code>ptr_a-&gt;speed</code> writes 120 directly to the allocated heap struct." :
            state.codeStep === 2 ? "Line 3: <code>ptr_b</code> copies the address <code>0x6020</code> (Borrower). Both pointers now alias the block." :
            state.codeStep === 3 ? "Line 4: Owner calls <code>free(ptr_a)</code>. The heap block is released back to the OS runtime." :
            "Line 5: Setting pointers to <code>NULL</code> prevents catastrophic use-after-free or double-free defects!"}
        </div>
      `;
    },
    validate: (state) => state.codeStep >= 3
  }
];

// Reactive Application State
const appState = {
  currentStep: 0,
  p1Target: "node_1",
  p2Target: null,
  speed: 100,
  codeStep: 0
};

// UI Element Handles
const cardViewport = document.getElementById("card-viewport");
const btnPrev = document.getElementById("btn-prev");
const btnNext = document.getElementById("btn-next");
const progressSteps = document.querySelectorAll(".progress-step");

function renderCurrentStep() {
  const step = STEPS[appState.currentStep];
  
  // Update Progress Pills
  progressSteps.forEach((pill, idx) => {
    pill.classList.remove("active", "completed");
    if (idx < appState.currentStep) {
      pill.classList.add("completed");
    } else if (idx === appState.currentStep) {
      pill.classList.add("active");
    }
  });

  // Render Step Card
  cardViewport.innerHTML = `
    <article class="step-card">
      <div class="card-stage-label">${step.stage}</div>
      <h2 style="font-size: 20px; font-weight: 700; margin-top: -12px;">${step.title}</h2>
      <p class="card-prompt">${step.prompt}</p>
      ${step.renderWidget(appState)}
    </article>
  `;

  // Attach Step-Specific Event Handlers
  attachStepHandlers();

  // Update Nav Buttons
  btnPrev.disabled = appState.currentStep === 0;
  if (appState.currentStep === STEPS.length - 1) {
    btnNext.textContent = "Finish Chapter Study 🎉";
  } else {
    btnNext.textContent = "Check & Next →";
  }
}

function attachStepHandlers() {
  // Step 1: Pointer Select
  const p1Select = document.getElementById("p1-select");
  if (p1Select) {
    p1Select.addEventListener("change", (e) => {
      appState.p1Target = e.target.value;
      renderCurrentStep();
    });
  }

  // Step 2: Speed Scrubber
  const speedScrubber = document.getElementById("speed-scrubber");
  if (speedScrubber) {
    speedScrubber.addEventListener("input", (e) => {
      appState.speed = parseInt(e.target.value, 10);
      renderCurrentStep();
    });
  }

  // Step 3: Leak Select
  const leakSelect = document.getElementById("leak-select");
  if (leakSelect) {
    leakSelect.addEventListener("change", (e) => {
      appState.p1Target = e.target.value;
      renderCurrentStep();
    });
  }

  // Step 5: Code Stepper
  const stepCodeBtn = document.getElementById("step-code-btn");
  if (stepCodeBtn) {
    stepCodeBtn.addEventListener("click", () => {
      if (appState.codeStep < 4) {
        appState.codeStep++;
      }
      renderCurrentStep();
    });
  }

  const resetCodeBtn = document.getElementById("reset-code-btn");
  if (resetCodeBtn) {
    resetCodeBtn.addEventListener("click", () => {
      appState.codeStep = 0;
      renderCurrentStep();
    });
  }
}

// Navigation Handlers
btnNext.addEventListener("click", () => {
  const step = STEPS[appState.currentStep];
  if (step.validate && !step.validate(appState)) {
    alert("Please complete the interactive manipulation check before moving forward!");
    return;
  }
  if (step.onNext) {
    step.onNext(appState);
  }
  if (appState.currentStep < STEPS.length - 1) {
    appState.currentStep++;
    renderCurrentStep();
  } else {
    alert("Congratulations! You have completed the Chapter 09 Web Interactive Study.");
  }
});

btnPrev.addEventListener("click", () => {
  if (appState.currentStep > 0) {
    appState.currentStep--;
    renderCurrentStep();
  }
});

progressSteps.forEach((pill) => {
  pill.addEventListener("click", () => {
    const targetIdx = parseInt(pill.dataset.step, 10);
    if (targetIdx <= appState.currentStep) {
      appState.currentStep = targetIdx;
      renderCurrentStep();
    }
  });
});

// Initialize on Load
renderCurrentStep();
