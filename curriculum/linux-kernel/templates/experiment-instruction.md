# Experiment: <name>

## What this tool answers

<One plain-language sentence. For a tool lab: what question does this tool
answer that another tool cannot? For a kernel lab: what mechanism are you
observing?>

## Mental model

<What does the tool observe? What can it not observe? Where does it sit relative
to the kernel boundary?>

## Guided commands

```sh
<exact commands on a known workload>
```

What to notice:

- <column, event, or counter>
- <default filter>
- <what is missing>

## What you are observing

<One short paragraph in plain language. Name the path or mechanism and what the
learner will see. No jargon before the plain-language explanation.>

## Predict

Write these down before running anything:

1. <prediction about a counter, trace, route, or output>
2. <prediction about which function or interface is involved>
3. <prediction about what happens when the one variable changes>

## Setup

```sh
<exact commands to create the namespace, interfaces, files, or guest>
```

Environment:

- Kernel version:
- Commit/tag:
- Namespace or guest:
- Tools:

## Run

```sh
<exact command>
```

Expected shape of the output:

```text
<small, deterministic output>
```

## Change one thing

Variable:

```sh
<exact command that changes only this variable>
```

Why this variable:

## Filter

Start noisy, then add one filter at a time:

```sh
<unfiltered command>
<filtered command 1>
<filtered command 2>
```

What each filter removed:

## Observe

Capture at least two signals:

```sh
<command 1>
<command 2>
```

Record:

- before:
- after:
- difference:

## Diagnose

Symptom:

<Describe a symptom, not a command. The learner chooses the tool.>

Evidence:

- tool:
- output:
- conclusion:

## Explain

1. Which function owns the transition you observed?
2. Which data structure carries the state?
3. What would happen on a different interface type or kernel version?
4. What surprised you?

## Teach-back

- Three invocations to remember:
- One pitfall:
- One confusing output column:
- One question this tool cannot answer:

## Cleanup

```sh
<exact cleanup commands>
```

## Artifacts

- Trace/log:
- Diff:
- Diagram:
