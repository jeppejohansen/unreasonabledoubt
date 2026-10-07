---
name: blog-elicitation
description: Interview the author to establish a post's central thesis or model question, then save an agreed paragraph-by-paragraph bullet outline beside the blog draft. Use when the user wants to develop an Unreasonable Doubt idea through questions, not when they ask for a prose draft or a quick edit.
---

This is a collaborative interview inspired by [Allium's elicitation approach](https://github.com/juxt/allium/blob/main/skills/elicit/SKILL.md): discover the author's intent, ask one focused question at a time, follow implications, record open questions, and revise earlier decisions when new answers conflict. Use [Basbøll's paragraph principle](https://inframethodology.cbs.dk/?p=5670) when outlining: one identifiable claim per paragraph, supported, elaborated, or defended.

If invoked without a pitch, first ask the author for it in their own words and wait. If a pitch is already present, start from it. Keep track of settled answers and open questions; do not re-ask what the author has settled.

## 1. Orient briefly, if needed

Notice whether the post mainly advances a thesis, develops a model to investigate a question, or does both. Use that distinction to choose questions, not to force the author into a category. Skip this step when the pitch already makes the approach clear.

## 2. Establish the central point

Before planning sections or paragraphs, drill into what the post is about. For a thesis-led post, clarify the claim the author wants readers to accept, why it matters, and the competing intuition. For a model-led post, clarify the question the model answers, its key mechanism, and the intended takeaway or result. A model can support a broader thesis. If the result is not yet known, confirm what the model is meant to test and leave the conclusion open.

Ask the next question that would most sharpen this point, one at a time. When you think you understand it, state the proposed central thesis or model question and takeaway in one or two sentences, then ask the author if you have it right. If they correct or reject it, revise your understanding and read it back again. **Move to the outline only after the author explicitly confirms the central point.** Do not infer confirmation from silence or a request to keep exploring.

## 3. Build the paragraph outline

With the central point agreed, elicit the opening puzzle, audience, competing intuition, assumptions, mechanism, concrete example, expected figures or tables, empirical support, strongest objection, limitations, and conclusion as they become relevant. Ask why a proposed step follows from the previous one. When the author is unsure, offer a small set of plausible options and mark the choice as open until they decide. Do not invent their position, evidence, or model results.

The deliverable is a Markdown outline grouped under useful section headings, with **one bullet for each planned paragraph and exactly one sentence in each bullet**. That sentence states the paragraph's single claim; include a brief support cue or an unresolved source, figure, or decision as a parenthetical phrase within the sentence when helpful. Review the full bullet sequence for gaps, repetition, and whether the ending answers the opening puzzle. Continue asking focused questions and revising until the author accepts the structure or asks to stop. Do not turn the outline into prose without a separate request.

When the post directory is clear, keep the working outline in `outline.md` beside `blog.md`, preserving existing user material. Once the author accepts the outline, write or update that file even if the interview took place entirely in the conversation. If no directory is chosen, work in the conversation and ask where the post will live before finishing; use `just make-blog <slug>` only when they want a new post folder.
