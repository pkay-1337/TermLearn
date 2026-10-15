/**
 * Extreme C - Chapter 09: OOP and Encapsulation in C
 * Interactive Multimodal Study Engine
 * Implements 6 comprehensive pedagogical units, continuous parameter scrubbers,
 * live byte offset inspectors, and simulated compiler diagnostics.
 */

// Curriculum Units Definition
const UNITS = [
  // ---------------------------------------------------------------------------
  // Unit 1: Mental Concepts to Object Models
  // ---------------------------------------------------------------------------
  {
    stage: "Unit 1 of 6: Intuitive Induction",
    title: "Mental Concepts vs. Machine Memory",
    prompt: "Humans analyze reality by forming <strong>mental concepts</strong> (chairs, students, windows) and relationships in a mind map. Software translates this into an <strong>object model</strong> in RAM. Compare the three naming strategies below:",
    renderWidget: (state) => `
      <div class="widget-box">
        <div style="display: flex; gap: 8px; justify-content: center; margin-bottom: 6px;">
          <button class="btn btn-secondary ${state.u1_model === 'adhoc' ? 'active' : ''}" id="btn-u1-adhoc" style="font-size: 12px; padding: 6px 14px; min-height: 36px;">
            1. Ad-Hoc Naming
          </button>
          <button class="btn btn-secondary ${state.u1_model === 'prefix' ? 'active' : ''}" id="btn-u1-prefix" style="font-size: 12px; padding: 6px 14px; min-height: 36px;">
            2. Prefix Convention
          </button>
          <button class="btn btn-primary ${state.u1_model === 'struct' ? 'active' : ''}" id="btn-u1-struct" style="font-size: 12px; padding: 6px 14px; min-height: 36px;">
            3. Explicit Struct Type
          </button>
        </div>

        <div class="compiler-box">
          ${state.u1_model === 'adhoc' ? `
            <div style="color: var(--text-dim); margin-bottom: 6px;">// Code Box 6-2: Ad-Hoc variables without conceptual binding</div>
            <div>char* <span class="var-rose">aaa</span>[10]; <span style="color: var(--text-dim);">// Student first names?</span></div>
            <div>char* <span class="var-rose">bbb</span>[10]; <span style="color: var(--text-dim);">// Surnames?</span></div>
            <div>int   <span class="var-rose">ccc</span>[10]; <span style="color: var(--text-dim);">// Ages?</span></div>
            <div>double <span class="var-rose">ddd</span>[10]; <span style="color: var(--text-dim);">// Exam marks?</span></div>
          ` : state.u1_model === 'prefix' ? `
            <div style="color: var(--text-dim); margin-bottom: 6px;">// Code Box 6-1: Naming convention grouping (Implicit to language)</div>
            <div>char* <span class="var-amber">student_</span>first_names[10];</div>
            <div>char* <span class="var-amber">student_</span>surnames[10];</div>
            <div>int   <span class="var-amber">student_</span>ages[10];</div>
            <div>double <span class="var-amber">student_</span>marks[10];</div>
          ` : `
            <div style="color: var(--text-dim); margin-bottom: 6px;">// Explicit Encapsulation: A single conceptual type enforced by compiler</div>
            <div><span style="color: #c084fc;">typedef struct</span> {</div>
            <div>  char first_name[32];</div>
            <div>  char surname[32];</div>
            <div>  int age;</div>
            <div>  double mark;</div>
            <div>} <span class="var-blue">student_t</span>;</div>
            <div style="margin-top: 6px;"><span class="var-blue">student_t</span> classroom[10]; <span style="color: #22c55e;">// 10 coherent student capsules</span></div>
          `}
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px;">
          <div style="background: rgba(11, 15, 25, 0.5); padding: 10px; border-radius: var(--radius-sm); border: 1px solid var(--bg-subtle);">
            <div style="color: var(--text-muted); font-size: 11px; text-transform: uppercase;">Cognitive Load on Programmer</div>
            <div style="font-size: 15px; font-weight: bold; margin-top: 4px; color: ${state.u1_model === 'adhoc' ? '#ef4444' : state.u1_model === 'prefix' ? '#f59e0b' : '#22c55e'};">
              ${state.u1_model === 'adhoc' ? 'CRITICAL (Extreme extraneous load)' : state.u1_model === 'prefix' ? 'MODERATE (Dependent on human discipline)' : 'MINIMAL (Compiler guards structure)'}
            </div>
          </div>
          <div style="background: rgba(11, 15, 25, 0.5); padding: 10px; border-radius: var(--radius-sm); border: 1px solid var(--bg-subtle);">
            <div style="color: var(--text-muted); font-size: 11px; text-transform: uppercase;">Language Awareness</div>
            <div style="font-size: 15px; font-weight: bold; margin-top: 4px; color: ${state.u1_model === 'struct' ? '#22c55e' : '#94a3b8'};">
              ${state.u1_model === 'struct' ? 'Explicit (Type-safe)' : 'Implicit (Blind to language)'}
            </div>
          </div>
        </div>
      </div>

      <div class="diagnostic-banner ${state.u1_model === 'struct' ? 'success' : 'info'}">
        ${state.u1_model === 'struct'
          ? "✅ <strong>Explicit Encapsulation:</strong> By creating <code>student_t</code>, attributes travel together as a single unit. Passing a pointer to <code>student_t</code> passes the whole student."
          : "👉 Toggle between the three naming strategies to see why ad-hoc variables fail and how struct encapsulation solves it."}
      </div>
    `,
    validate: (state) => state.u1_model === 'struct'
  },

  // ---------------------------------------------------------------------------
  // Unit 2: Prototype vs Class-Based Construction
  // ---------------------------------------------------------------------------
  {
    stage: "Unit 2 of 6: Pattern Discovery",
    title: "Prototype vs. Class-Based Construction",
    prompt: "How do objects come into existence? Prototype-based OOP (*existence precedes essence*) begins empty and adds fields dynamically. Class-based OOP (*essence precedes existence*, C & C++) relies on an upfront blueprint. Scrub through the C lifecycle:",
    renderWidget: (state) => {
      const phases = [
        { label: "1. Allocation (Creation)", desc: "Raw memory allocated on stack/heap (sizeof(car_t) = 48 bytes). Attributes contain indeterminate garbage." },
        { label: "2. Construction (Init)", desc: "car_construct(&car, 'Renault') initializes fields: speed = 0.0, fuel = 0.0, name = 'Renault'." },
        { label: "3. State Mutation", desc: "car_accelerate(&car) and car_refuel(&car, 50.0) mutate internal state attributes." },
        { label: "4. Destruction (Release)", desc: "car_destruct(&car) releases resources and cleans references, preserving referential integrity." }
      ];
      const cur = phases[state.u2_step];
      return `
        <div class="widget-box">
          <div class="scrubber-panel">
            <div class="scrubber-header">
              <span>Scrub Object Lifecycle Phase:</span>
              <span class="var-blue" style="font-family: var(--font-mono);">${cur.label}</span>
            </div>
            <input type="range" class="scrubber" id="u2-scrubber" min="0" max="3" value="${state.u2_step}" step="1">
          </div>

          <div style="background: #070a12; border: 1px solid var(--bg-subtle); border-radius: var(--radius-md); padding: 16px;">
            <div style="font-size: 12px; font-weight: 700; color: var(--interactive-blue); text-transform: uppercase; margin-bottom: 6px;">
              Phase Mechanics
            </div>
            <p style="font-size: 14px; color: var(--text-secondary); line-height: 1.6;">
              ${cur.desc}
            </p>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div style="background: rgba(11, 15, 25, 0.6); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--bg-subtle);">
              <span style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: bold;">Creation vs. Construction</span>
              <p style="font-size: 12px; margin-top: 6px; color: var(--text-secondary);">
                <strong>Creation</strong> allocates bytes.<br>
                <strong>Construction</strong> establishes invariants.
              </p>
            </div>
            <div style="background: rgba(11, 15, 25, 0.6); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--bg-subtle);">
              <span style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: bold;">Class-Based Invariant</span>
              <p style="font-size: 12px; margin-top: 6px; color: var(--text-secondary);">
                In C, structs cannot change member count at runtime. Structure is fixed at compile time.
              </p>
            </div>
          </div>
        </div>

        <div class="diagnostic-banner success">
          💡 <strong>Philosophical Distinction:</strong> In C, <em>essence precedes existence</em>. The blueprint (class / struct) is compiled first; objects can only exist as concrete instances of that pre-determined blueprint.
        </div>
      `;
    },
    validate: (state) => state.u2_step >= 2
  },

  // ---------------------------------------------------------------------------
  // Unit 3: Attribute Encapsulation & Byte Layouts
  // ---------------------------------------------------------------------------
  {
    stage: "Unit 3 of 6: Direct Manipulation",
    title: "Attribute Encapsulation & Byte Layouts",
    prompt: "In C, <code>typedef struct { int x, y; int red, green, blue; } pixel_t;</code> bundles 5 variables into a single contiguous 20-byte block. Drag the coordinate and color scrubbers to inspect memory:",
    renderWidget: (state) => `
      <div class="widget-box">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
          <!-- Left: Scrubber Controls -->
          <div style="display: flex; flex-direction: column; gap: 12px;">
            <div>
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span>X Coordinate (<span class="var-blue">p1.x</span>):</span>
                <span class="var-blue" style="font-family: var(--font-mono); font-weight: bold;">${state.p_x}</span>
              </div>
              <input type="range" class="scrubber" id="u3-x" min="0" max="100" value="${state.p_x}">
            </div>

            <div>
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span>Y Coordinate (<span class="var-amber">p1.y</span>):</span>
                <span class="var-amber" style="font-family: var(--font-mono); font-weight: bold;">${state.p_y}</span>
              </div>
              <input type="range" class="scrubber" id="u3-y" min="0" max="100" value="${state.p_y}">
            </div>

            <div>
              <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                <span>Red Channel (<span class="var-rose">p1.red</span>):</span>
                <span class="var-rose" style="font-family: var(--font-mono); font-weight: bold;">${state.p_r}</span>
              </div>
              <input type="range" class="scrubber" id="u3-r" min="0" max="255" value="${state.p_r}">
            </div>

            <!-- Preview Swatch -->
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 4px;">
              <div style="width: 28px; height: 28px; border-radius: 6px; border: 1px solid var(--bg-subtle); background-color: rgb(${state.p_r}, 128, 200);"></div>
              <span style="font-size: 12px; color: var(--text-muted);">Active Pixel Color</span>
            </div>
          </div>

          <!-- Right: Contiguous Memory Byte Offset Inspector -->
          <div style="background: #070a12; border: 1px solid var(--bg-subtle); border-radius: var(--radius-sm); padding: 10px;">
            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px;">
              Physical Memory Layout (&p1 = 0x7ffd00)
            </div>
            <table class="byte-table">
              <thead>
                <tr>
                  <th>Offset</th>
                  <th>Member</th>
                  <th>Bytes</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                <tr class="active">
                  <td>+0x00</td>
                  <td class="var-blue">int x</td>
                  <td>4 B</td>
                  <td>${state.p_x}</td>
                </tr>
                <tr class="active">
                  <td>+0x04</td>
                  <td class="var-amber">int y</td>
                  <td>4 B</td>
                  <td>${state.p_y}</td>
                </tr>
                <tr class="active">
                  <td>+0x08</td>
                  <td class="var-rose">int red</td>
                  <td>4 B</td>
                  <td>${state.p_r}</td>
                </tr>
                <tr>
                  <td>+0x0C</td>
                  <td style="color: var(--var-emerald);">int green</td>
                  <td>4 B</td>
                  <td>128</td>
                </tr>
                <tr>
                  <td>+0x10</td>
                  <td style="color: var(--var-blue);">int blue</td>
                  <td>4 B</td>
                  <td>200</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="diagnostic-banner success">
        🔍 <strong>Zero-Cost Indirection:</strong> Accessing <code>p1.red</code> is compiled down to a direct base-pointer offset calculation: <code>*(&p1 + 8)</code>. No hash maps, no dictionary lookups!
      </div>
    `,
    validate: (state) => state.p_x !== 56 || state.p_r !== 123
  },

  // ---------------------------------------------------------------------------
  // Unit 4: Behavior Encapsulation & The 'this' Pointer
  // ---------------------------------------------------------------------------
  {
    stage: "Unit 4 of 6: Synchronized Multi-Rep",
    title: "Behavior Encapsulation & The 'this' Pointer",
    prompt: "C does not allow functions inside structs. Instead, we use <strong>implicit behavior encapsulation</strong>: behavior functions accept a pointer to the attribute structure as the first argument (<code>car_accelerate(car_t*)</code>):",
    renderWidget: (state) => `
      <div class="widget-box">
        <!-- Instrument Cluster -->
        <div class="car-dash">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: bold; font-size: 14px; letter-spacing: 0.05em; color: var(--interactive-blue);">
              CAR INSTRUMENT CLUSTER: "${state.car_name}"
            </span>
            <span style="font-size: 12px; color: ${state.car_fuel > 10 ? '#22c55e' : '#ef4444'}; font-weight: bold;">
              ${state.car_fuel > 0 ? 'ENGINE RUNNING' : 'OUT OF FUEL'}
            </span>
          </div>

          <div class="gauges-row">
            <div class="gauge-card">
              <span style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Speedometer</span>
              <div class="gauge-val var-blue">${state.car_speed.toFixed(1)} <span style="font-size: 12px; color: var(--text-muted);">km/h</span></div>
            </div>
            <div class="gauge-card">
              <span style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Fuel Level</span>
              <div class="gauge-val ${state.car_fuel > 20 ? 'var-emerald' : 'var-danger'}">${state.car_fuel.toFixed(1)} <span style="font-size: 12px; color: var(--text-muted);">L</span></div>
            </div>
          </div>

          <div class="dash-controls">
            <button id="btn-car-accel" class="btn btn-primary" style="flex: 1;" ${state.car_fuel <= 0 ? 'disabled' : ''}>
              ⚡ Accelerate (car_accelerate(&car))
            </button>
            <button id="btn-car-brake" class="btn btn-secondary" style="flex: 1;" ${state.car_speed <= 0 ? 'disabled' : ''}>
              🛑 Brake (car_brake(&car))
            </button>
            <button id="btn-car-refuel" class="btn btn-secondary">
              ⛽ Refuel
            </button>
          </div>
        </div>

        <!-- Equivalence Split View: C vs C++ -->
        <div class="equivalence-split">
          <div class="equiv-pane">
            <div class="equiv-title">Procedural C Architecture</div>
            <div style="color: var(--var-blue);">car_accelerate(&car);</div>
            <div style="color: var(--text-dim); margin-top: 4px;">
              Explicitly passes struct pointer as 1st argument.
            </div>
          </div>
          <div class="equiv-pane" style="border-left: 1px solid var(--bg-subtle); padding-left: 12px;">
            <div class="equiv-title">Object-Oriented C++ Equivalent</div>
            <div style="color: var(--var-emerald);">car.Accelerate();</div>
            <div style="color: var(--text-dim); margin-top: 4px;">
              Implicitly passes struct pointer via hidden <code>this</code>.
            </div>
          </div>
        </div>
      </div>

      <div class="diagnostic-banner info">
        🔄 <strong>Mechanical Identity:</strong> When C++ compiles <code>car.Accelerate()</code>, it translates it under the hood directly to <code>Car::Accelerate(Car* const this)</code> — exactly what we write by hand in C!
      </div>
    `,
    validate: (state) => state.car_actions >= 2
  },

  // ---------------------------------------------------------------------------
  // Unit 5: Information Hiding via Opaque Pointers
  // ---------------------------------------------------------------------------
  {
    stage: "Unit 5 of 6: Constrained Sandbox",
    title: "Information Hiding via Opaque Pointers",
    prompt: "If consumers directly access struct fields (e.g. <code>list->items[0]</code>), internal implementation details leak out. In C, we enforce true private encapsulation using an <strong>opaque struct declaration</strong> (incomplete type):",
    renderWidget: (state) => `
      <div class="widget-box">
        <div style="display: flex; gap: 8px; margin-bottom: 4px;">
          <button id="btn-u5-bad" class="btn btn-secondary ${state.u5_mode === 'bad' ? 'active' : ''}" style="font-size: 12px; padding: 6px 14px; min-height: 36px;">
            Direct Field Access (Leaky)
          </button>
          <button id="btn-u5-good" class="btn btn-primary ${state.u5_mode === 'good' ? 'active' : ''}" style="font-size: 12px; padding: 6px 14px; min-height: 36px;">
            Opaque Pointer via Public API
          </button>
        </div>

        <div class="compiler-box">
          <div style="color: var(--text-dim); margin-bottom: 6px;">// consumer_main.c</div>
          <div>#include "list.h" <span style="color: var(--text-dim);">// Contains: struct list_t; (declaration ONLY)</span></div>
          <div style="margin-top: 6px;">struct list_t* list = list_malloc();</div>
          <div>list_init(list);</div>
          <div style="margin-top: 6px;">
            ${state.u5_mode === 'bad'
              ? `<span class="var-danger">list-&gt;size = 100;</span> <span style="color: var(--text-dim);">// Illegal direct access!</span>`
              : `<span class="var-emerald">list_add(list, 100);</span> <span style="color: var(--text-dim);">// Safe public interface!</span>`}
          </div>

          <!-- Compiler Diagnostic Readout -->
          <div class="${state.u5_mode === 'bad' ? 'compiler-error' : 'diagnostic-banner success'}" style="margin-top: 12px; font-size: 12px;">
            ${state.u5_mode === 'bad'
              ? `🚨 <strong>GCC Compile Error:</strong><br>
                 consumer_main.c:8:9: error: dereferencing pointer to incomplete type 'struct list_t'<br>
                 &nbsp;&nbsp;&nbsp;&nbsp;list-&gt;size = 100;<br>
                 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;^~<br>
                 list.h:5:8: note: forward declaration of 'struct list_t'`
              : `✅ <strong>GCC Build Success:</strong><br>
                 0 errors, 0 warnings. The private struct definition remains sealed inside list.c!`}
          </div>
        </div>

        <details class="deep-dive" open>
          <summary>The Opaque Pointer Pattern (ABI Stability)</summary>
          <p>By keeping the struct definition inside <code>list.c</code> rather than <code>list.h</code>, the library author can change array sizes, add caching pointers, or redesign fields without breaking the binary compatibility (ABI) of existing compiled programs!</p>
        </details>
      </div>
    `,
    validate: (state) => state.u5_mode === 'good'
  },

  // ---------------------------------------------------------------------------
  // Unit 6: Encapsulated Lifecycle & Leak Spotter
  // ---------------------------------------------------------------------------
  {
    stage: "Unit 6 of 6: Productive Failure & Diagnostic",
    title: "Encapsulated Lifecycle & Leak Spotter",
    prompt: "When an encapsulated struct holds heap allocations (like <code>list->items</code>), calling <code>free()</code> on the outer pointer alone causes a severe memory leak. Observe the destruction sequence:",
    renderWidget: (state) => `
      <div class="widget-box">
        <div style="display: flex; gap: 8px; margin-bottom: 4px;">
          <button id="btn-u6-leak" class="btn btn-secondary ${state.u6_action === 'leak' ? 'active' : ''}" style="font-size: 12px; padding: 6px 14px; min-height: 36px;">
            Naive Free: free(list)
          </button>
          <button id="btn-u6-clean" class="btn btn-primary ${state.u6_action === 'clean' ? 'active' : ''}" style="font-size: 12px; padding: 6px 14px; min-height: 36px;">
            Full Lifecycle: list_destroy(list); free(list);
          </button>
        </div>

        <!-- Memory State Diagram -->
        <div class="memory-grid">
          <div class="memory-column">
            <div class="column-header">
              <span>Outer Container (list_t)</span>
              <span style="font-family: var(--font-mono);">0x5010</span>
            </div>
            <div class="memory-cell ${state.u6_action === 'leak' || state.u6_action === 'clean' ? '' : 'active'}">
              <span>struct list_t</span>
              <span style="color: var(--text-dim);">${state.u6_action ? 'FREED' : 'Allocated'}</span>
            </div>
          </div>

          <div class="memory-column">
            <div class="column-header">
              <span>Internal Array Buffer</span>
              <span style="font-family: var(--font-mono);">0x8040</span>
            </div>
            <div class="memory-cell ${state.u6_action === 'leak' ? 'leaked' : state.u6_action === 'clean' ? '' : 'active'}">
              <span>int* items [MAX_SIZE]</span>
              <span style="font-weight: bold; color: ${state.u6_action === 'leak' ? '#ef4444' : state.u6_action === 'clean' ? '#22c55e' : '#38bdf8'};">
                ${state.u6_action === 'leak' ? '🚨 LEAKED (UNREFERENCED)' : state.u6_action === 'clean' ? 'SAFELY FREED' : 'Allocated (40 Bytes)'}
              </span>
            </div>
          </div>
        </div>

        <!-- Diagnostic Valgrind Log Box -->
        <div class="compiler-box">
          <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px;">
            Valgrind Memcheck Diagnostic Feed
          </div>
          ${state.u6_action === 'leak' ? `
            <div style="color: #f87171; font-family: var(--font-mono); font-size: 11px;">
              ==9821== LEAK SUMMARY:<br>
              ==9821== &nbsp;&nbsp;&nbsp;&nbsp;definitely lost: 40 bytes in 1 blocks<br>
              ==9821== &nbsp;&nbsp;&nbsp;&nbsp;indirectly lost: 0 bytes in 0 blocks<br>
              ==9821== 40 bytes in 1 blocks are definitely lost in loss record 1 of 1<br>
              ==9821== &nbsp;&nbsp;&nbsp;&nbsp;at 0x4848899: malloc (vgpreload_memcheck.so)<br>
              ==9821== &nbsp;&nbsp;&nbsp;&nbsp;by 0x1091AC: list_init (ExtremeC_examples_chapter6_3.c:56)<br>
              ==9821== &nbsp;&nbsp;&nbsp;&nbsp;by 0x1092F0: main (ExtremeC_examples_chapter6_3_main.c:14)
            </div>
          ` : state.u6_action === 'clean' ? `
            <div style="color: #86efac; font-family: var(--font-mono); font-size: 11px;">
              ==9821== HEAP SUMMARY:<br>
              ==9821== &nbsp;&nbsp;&nbsp;&nbsp;in use at exit: 0 bytes in 0 blocks<br>
              ==9821== &nbsp;&nbsp;&nbsp;&nbsp;total heap usage: 2 allocs, 2 frees, 56 bytes allocated<br>
              ==9821== All heap blocks were freed -- no leaks are possible<br>
              ==9821== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
            </div>
          ` : `
            <div style="color: var(--text-dim); font-size: 11px;">
              Select an action above to test the memory reclamation protocol.
            </div>
          `}
        </div>
      </div>

      <div class="diagnostic-banner ${state.u6_action === 'clean' ? 'success' : 'info'}">
        ${state.u6_action === 'clean'
          ? "🎉 <strong>Mastery Complete!</strong> You have successfully mastered explicit attribute encapsulation, implicit behavior functions, opaque information hiding, and safe lifecycle protocols in C!"
          : "👉 Test the full lifecycle destruction to verify that all nested buffers are reclaimed cleanly."}
      </div>
    `,
    validate: (state) => state.u6_action === 'clean'
  }
];

// Reactive Global State
const appState = {
  currentUnit: 0,
  
  // Unit 1 state
  u1_model: 'prefix',
  
  // Unit 2 state
  u2_step: 0,
  
  // Unit 3 state
  p_x: 56,
  p_y: 34,
  p_r: 123,
  
  // Unit 4 state
  car_name: "Renault",
  car_speed: 0.0,
  car_fuel: 100.0,
  car_actions: 0,
  
  // Unit 5 state
  u5_mode: 'bad',
  
  // Unit 6 state
  u6_action: null
};

// DOM References
const cardViewport = document.getElementById("card-viewport");
const btnPrev = document.getElementById("btn-prev");
const btnNext = document.getElementById("btn-next");
const unitIndicator = document.getElementById("unit-indicator");
const progressSteps = document.querySelectorAll(".progress-step");

function renderUnit() {
  const unit = UNITS[appState.currentUnit];
  
  // Update Progress Pills
  progressSteps.forEach((pill, idx) => {
    pill.classList.remove("active", "completed");
    if (idx < appState.currentUnit) {
      pill.classList.add("completed");
    } else if (idx === appState.currentUnit) {
      pill.classList.add("active");
    }
  });

  // Update Indicator
  if (unitIndicator) {
    unitIndicator.textContent = `Unit ${appState.currentUnit + 1} of ${UNITS.length}`;
  }

  // Render Step Card
  cardViewport.innerHTML = `
    <article class="step-card">
      <div class="card-stage-label">${unit.stage}</div>
      <h2 class="card-title">${unit.title}</h2>
      <p class="card-prompt">${unit.prompt}</p>
      ${unit.renderWidget(appState)}
    </article>
  `;

  // Attach Unit-Specific Event Handlers
  attachUnitHandlers();

  // Update Buttons
  btnPrev.disabled = appState.currentUnit === 0;
  if (appState.currentUnit === UNITS.length - 1) {
    btnNext.textContent = "Finish Chapter Study 🎉";
  } else {
    btnNext.textContent = "Check & Next →";
  }
}

function attachUnitHandlers() {
  // Unit 1 Handlers
  const btnU1Adhoc = document.getElementById("btn-u1-adhoc");
  const btnU1Prefix = document.getElementById("btn-u1-prefix");
  const btnU1Struct = document.getElementById("btn-u1-struct");

  if (btnU1Adhoc) btnU1Adhoc.onclick = () => { appState.u1_model = 'adhoc'; renderUnit(); };
  if (btnU1Prefix) btnU1Prefix.onclick = () => { appState.u1_model = 'prefix'; renderUnit(); };
  if (btnU1Struct) btnU1Struct.onclick = () => { appState.u1_model = 'struct'; renderUnit(); };

  // Unit 2 Handlers
  const u2Scrubber = document.getElementById("u2-scrubber");
  if (u2Scrubber) {
    u2Scrubber.oninput = (e) => {
      appState.u2_step = parseInt(e.target.value, 10);
      renderUnit();
    };
  }

  // Unit 3 Handlers
  const u3X = document.getElementById("u3-x");
  const u3Y = document.getElementById("u3-y");
  const u3R = document.getElementById("u3-r");

  if (u3X) u3X.oninput = (e) => { appState.p_x = parseInt(e.target.value, 10); renderUnit(); };
  if (u3Y) u3Y.oninput = (e) => { appState.p_y = parseInt(e.target.value, 10); renderUnit(); };
  if (u3R) u3R.oninput = (e) => { appState.p_r = parseInt(e.target.value, 10); renderUnit(); };

  // Unit 4 Handlers
  const btnCarAccel = document.getElementById("btn-car-accel");
  const btnCarBrake = document.getElementById("btn-car-brake");
  const btnCarRefuel = document.getElementById("btn-car-refuel");

  if (btnCarAccel) {
    btnCarAccel.onclick = () => {
      if (appState.car_fuel > 0) {
        appState.car_speed += 15.0;
        appState.car_fuel = Math.max(0, appState.car_fuel - 4.5);
        appState.car_actions++;
        renderUnit();
      }
    };
  }
  if (btnCarBrake) {
    btnCarBrake.onclick = () => {
      appState.car_speed = Math.max(0, appState.car_speed - 20.0);
      appState.car_actions++;
      renderUnit();
    };
  }
  if (btnCarRefuel) {
    btnCarRefuel.onclick = () => {
      appState.car_fuel = 100.0;
      appState.car_actions++;
      renderUnit();
    };
  }

  // Unit 5 Handlers
  const btnU5Bad = document.getElementById("btn-u5-bad");
  const btnU5Good = document.getElementById("btn-u5-good");

  if (btnU5Bad) btnU5Bad.onclick = () => { appState.u5_mode = 'bad'; renderUnit(); };
  if (btnU5Good) btnU5Good.onclick = () => { appState.u5_mode = 'good'; renderUnit(); };

  // Unit 6 Handlers
  const btnU6Leak = document.getElementById("btn-u6-leak");
  const btnU6Clean = document.getElementById("btn-u6-clean");

  if (btnU6Leak) btnU6Leak.onclick = () => { appState.u6_action = 'leak'; renderUnit(); };
  if (btnU6Clean) btnU6Clean.onclick = () => { appState.u6_action = 'clean'; renderUnit(); };
}

// Navigation Controls
btnNext.onclick = () => {
  const current = UNITS[appState.currentUnit];
  if (current.validate && !current.validate(appState)) {
    alert("Please interact with the widget or select the correct design approach before continuing!");
    return;
  }
  if (appState.currentUnit < UNITS.length - 1) {
    appState.currentUnit++;
    renderUnit();
  } else {
    alert("🎉 Outstanding work! You have mastered Chapter 09: OOP and Encapsulation in C.");
  }
};

btnPrev.onclick = () => {
  if (appState.currentUnit > 0) {
    appState.currentUnit--;
    renderUnit();
  }
};

progressSteps.forEach((pill) => {
  pill.onclick = () => {
    const idx = parseInt(pill.dataset.step, 10);
    if (idx <= appState.currentUnit) {
      appState.currentUnit = idx;
      renderUnit();
    }
  };
});

// Keyboard Navigation (Left / Right Arrow Keys)
window.addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight" && !btnNext.disabled) {
    btnNext.click();
  } else if (e.key === "ArrowLeft" && !btnPrev.disabled) {
    btnPrev.click();
  }
});

// Initialize First Unit
renderUnit();
