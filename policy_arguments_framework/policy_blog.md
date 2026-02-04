# The Structure of Good Policy Arguments

## Framework

- Arguments are usually considering a counterfactual. What would happen if did policy A compared to policy B (or maybe status quo).
- In other words we can think of this as a potential outcome problem.
- Often arguments are structured by two sets of arguments (link to Lars blog at some point)
    1. Facts about the world, i.e. empirical claims.
    2. Logical deductions.
- In economics, this is often intertwined into a empirical work in a theoretical framework.
However, a lot of economics, is often vague about when and which theoretical claims are supprted. We can think about this, as we want to make a statement:

E[Y(A) | M = m]

where M=m is the model we are using for our reasoning.
- But actually, it would be more kosher (to integrate out this belief). E[Y(A)], is the opject we are interested in, which is the same as integral integral p(m)p(y, m, a) dm dy
- Concretely, we can think of climate economics, often making statements about CO2 quotas (or other ways of pricing the externality), as the best way forward. But in some sense, it takes these as political viable. I.e. they assume this are possible policies in a world where the political economy, might not allow for such policies long run (i.e. climate initiatives will be reversed.)

# The Structure

## 1. Hook + scope
- Why policy arguments matter: they are claims about realistic counterfactuals.
- Focus is positive/empirical, not normative.
- The practical goal: given policy A, what would actually happen (not what we wish would happen).

## 2. Definition + how arguments are built
- A policy argument is a statement about a counterfactual world.
- The success criterion: realism of the counterfactual.
- Empirical claims: facts about the world, parameters, constraints.
- Logical deductions: what follows from those facts inside a model.
- Policy claims are conditional on a model M; model uncertainty is an empirical issue.

## 3. Example: climate policy and political risk (first case)
- Many climate recommendations assume politically feasible CO2 pricing.
- Political economy can make such policies unstable or reversible.
- That feasibility assumption is part of the model; change it and the counterfactual changes.

## 4. How to evaluate a good policy argument
- Are the empirical claims plausible and clearly stated?
- Are the logical steps valid within the stated model?
- Is the counterfactual realistic given political and institutional constraints?

## 5. Second example preview: Copenhagen housing
- Copenhagen housing: expanding supply vs price controls.
- Use the framework to show how different model assumptions change the counterfactual.

## 6. Close
- Summary: good policy arguments are disciplined counterfactuals.
- Invitation to apply the framework to concrete policy debates.

# The blog

Social scientists often claim their relevance through policy recommendations. _How do we get a higher growth rate?_, _How do we improve school wellbeing?_, etc. However, it is often not stated clearly under which circumstances these recommendations are true. Especially in economics, scholars often make strong claims that are true given a set of assumptions that are probably not realistic. This does at first sound a little bit like a rehash of the "economics has too-strong assumptions" critique, but I am actually trying to highlight something else. The right standard is whether the implied counterfactual is realistic. A policy recommendation can be true conditional on a model of the world: if the policy is politically feasible, palatable, and the right resources are thrown at it, it might be the best course of action. But is this really a good characterization of the real world? In other words, policy recommendations should be valued on their predictive quality about a counterfactual world where the policy was implemented. Throughout this blog, I will cover two examples: (1) a CO2 tax and (2) rent control in Copenhagen. We begin with the first and end with the second.

Most economists suggest two policies to combat climate change: a carbon tax and cap-and-trade (CO2 quotas), which are both ways to reduce the climate impact through markets. The first prices the externality, while the second caps the total CO2 amount. Why do economists like these compared to others? Because they allow markets to allocate the right to pollute to those with the highest willingness to pay. I am all for these solutions. I am just not sure what economists are claiming when they suggest them. Assume a center-left government is serious about reducing climate change, and they ask an economist what to do, and the economist suggests a carbon tax. Is the claim that a carbon tax implemented today will have the highest expected reduction in CO2 20 years from now? Or is the claim: conditional on staying in power for the next 20 years, and being able to maintain a stable government structure, it will have the highest expected reduction? These are two very different claims. The political feasibility assumption is part of the model; change it and the counterfactual changes.

Imagine that the center-left government actually implements a carbon tax, which makes them extremely unpopular due to rising food and gas prices, causing them to lose the election. Effectively paving the way for a far-right government that not only reverses the carbon tax but also blocks permits for solar cells and windmills—was it then really a good policy? Summarizing: policy recommendations should take seriously their actual, real-world implications, not just what the narrow model would suggest.


** ONLY CHANGE BELOW** CLIMATE INTRODUCTION SHOULD COME BEFORE POLICY ARGUMENT**

## What is a policy argument


So what is a policy recommendation? At its core, it is a claim about a counterfactual: what would happen to some outcome if we did policy A rather than policy B (or the status quo). And in many instances, it's unclear, exactly what counter factual world that is referred to? is it the real world, or a hypothetical world. Another way to think about it is, that it's a category error in normative policy analysis, i.e., a model of the world is conflated with the real world, when there are being made statements about the real world. In this blog, I will emphasize policy recommendations for the real world.
Put differently, it is a statement about Y(A) relative to Y(B), where Y is the outcome we care about. The point here is not to say what should be valued, but to say what would happen, given the world we live in. A good policy argument therefore succeeds to the extent that its implied counterfactual is realistic. 

The outcome we often care about is the difference:

E[Y(A) - Y(B)] = E[Y(A)] - E[Y(B)]

This notation is called potential outcomes and is usually associated with statistics. Here, I use it the context of using theoretical models to reason about policies. Concretely, Y is the outcome, and A and B are alternative policies.

Formally, we are often saying something like E[Y(A) | M = m], where M is the model we are using. The problem is that we are rarely certain about the correct model. If we are honest about that uncertainty, we should integrate it out. That is, we should weight each model by the probability we assign to it and then average:

E[Y(A)] = ∫ E[Y(A) | M = m] p(m) dm

And if we care about the policy comparison, then:

E[Y(A) - Y(B)] = ∫ (E[Y(A) | m] - E[Y(B) | m]) p(m) dm

Put differently, the argument is not “A is best under model m,” but “A is best after averaging across plausible models.” This is still an empirical claim: it is about which models are plausible and how likely they are. Summarizing, a good policy argument is one where the counterfactual is realistic, the model is explicit, and the remaining model uncertainty is acknowledged rather than hidden.

One important observation here is that the alternative models used to consider the policies (and their associated probabilities) are crucial. In other words, if basically every conveivable model, would yield the same policy recommendation, then choosing the correct would not be as important. However, often times, the important things needed for a realistic counterfactual are some of the things we actually exclude.

# Elaborating on the Carbon Tax Example

Let's again consider the first example, but now with a bit more detail. As mentioned, we imagine a center-left government asking for advice on reducing carbon emissions. We consider that the policy maker only considers 2 different policies. 

- A carbon tax (A)
- An Investment fund in green infrastructure (B)

For simplicity and clarity we will restrict ourselves to two models with starkly different policy recommendations. One model, where any policy implemented will have an infinite life time. I.e. a carbon tax (or investment fund), will sustain themselves until their planned terminations (say 10 years in the future). Conversely, we also consider a model, where the opposition party, if we winning will reverse these policies. We can draw the CO2 emissions (y-axis) as a function of time (x-axis), and we can draw the outcome under the different models in different colors (red and green). Finally we can in one number summarize the aggregate carbon emissions in one number, under each model. I.e. we are considering two policies under a two models; a pure _optimal efficiency_ model, and a game theoretic election model.

Next, we can think about the probabilities of each model of the models being true. Finally we can plot the expected carbon emissions of each policy (y-axis), under varying probabilities of which model is true (x-axis), where the policies expectation intersect, (draw vertical black dashed line), is where one should switch between each model.

# Just use prediction markets

Another way of testing policy recommendations, is to very simply make contracts with the experts making the given policy recommendations. If we implement a carbon tax, how much is carbon emissions reduced in 10 years.

- EXPAND ON THIS

# Rent control in Copenhagen.

- Throwback to older post.
- Rent control is usually considered bad because it restricts supply. However, that does not take into account that currently its NIMBY leftwing politics structural issue that limits supply of housing in copenhagen. (SHOW EVIDENCE OF THIS). In other words, we need to take seriously, that rent control might actually allow for more housing being built, due to the current main limiter is not too low rents, but rather political inaction. Use the graphs from last blog. 
