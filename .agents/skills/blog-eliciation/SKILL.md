---
name: blog-eliciation
description: Interview the author from a blog pitch to an agreed paragraph-by-paragraph bullet outline for an Unreasonable Doubt post. Use when the user wants to develop an idea through questions, not when they ask for a prose draft or a quick edit.
---

This is a collaborative interview inspired by [Allium's elicitation approach](https://github.com/juxt/allium/blob/main/skills/elicit/SKILL.md): discover the author's intent, ask one focused question at a time, follow implications, record open questions, and revise earlier decisions when new answers conflict. Use [Basbøll's paragraph principle](https://inframethodology.cbs.dk/?p=5670): one identifiable claim per paragraph, supported, elaborated, or defended.

If invoked without a pitch, first ask the author for their pitch in their own words and wait. If a pitch is already present, start from it. Do not write an outline from a vague pitch and end the interview. Ask the next question that would most improve the argument, one at a time; use the answer to update a working map and avoid re-asking what the author has settled. Briefly read back decisions at natural milestones and invite correction.

Elicit the opening puzzle, main claim, audience, competing intuition, model assumptions, mechanism, concrete example, expected figures or tables, empirical support, strongest objection, limitations, and conclusion as they become relevant. Ask why a proposed step follows from the previous one. When the author is unsure, offer a small set of plausible options and mark the choice as open until they decide. Do not invent their position, evidence, or model results.

The deliverable is a Markdown outline grouped under useful section headings, with **one bullet for each planned paragraph**. Each bullet states the paragraph's single claim; add a short support or evidence cue in the same bullet when helpful. Mark unresolved sources, figures, or decisions inline. Review the full bullet sequence for gaps, repetition, and whether the ending answers the opening puzzle. Continue asking focused questions and revising until the author accepts the structure or asks to stop. Do not turn the outline into prose without a separate request.

When the post directory is clear, keep the working outline in `blogs/<slug>/outline.md`, preserving existing user material. If no directory is chosen, work in the conversation until the author chooses one; use `just make-blog <slug>` only when they want a new post folder.
