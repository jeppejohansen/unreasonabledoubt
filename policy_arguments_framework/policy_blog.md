# The Structure of Good Policy Arguments

Social scientists often claim their relevance through policy recommendations. _How do we get a higher growth rate?_, _How do we improve school wellbeing?_, etc. However, it is often not stated clearly under which circumstances these recommendations are true. Especially in economics, scholars often make strong claims that are true given a set of assumptions that are probably not realistic. This does at first sound a little bit like a rehash of the "economics has too-strong assumptions" critique, but I am actually trying to highlight something else. The right standard policy arguments should be held up again is often whether the implied counterfactual is realistic. A policy recommendation can be true conditional on a model of the world: if the policy is politically feasible, palatable, and the right resources are thrown at it, it might be the best course of action. But is this really a good characterization of the real world? In other words, policy recommendations should be valued on their predictive quality about a counterfactual world where the policy was implemented. Throughout this blog, I will cover two examples: (1) a CO2 tax and (2) rent control in Copenhagen. We begin with the first and end with the second.

Most economists suggest two policies to combat climate change: a carbon tax and cap-and-trade (CO2 quotas), which are both ways to reduce the climate impact through markets. The first prices the externality, while the second caps the total CO2 amount. Why do economists like these compared to others? Because they allow markets to allocate the right to pollute to those with the highest willingness to pay. I am all for these solutions. I am just not sure what economists are claiming when they suggest said policies. Assume a center-left government is serious about reducing climate change, and they ask an economist what to do, and the economist suggests a carbon tax. Is the claim that a carbon tax implemented today will have the highest expected reduction in CO2 in 20 years from now? Or is the claim: conditional on staying in power for the next 20 years, and being able to maintain a stable government structure, it will have the highest expected reduction? These are two very different claims. The political feasibility assumption is part of the model; change it and the counterfactual changes.

We can easily imagine a world where the center-left government implements a carbon tax, which makes them extremely unpopular due to rising food and gas prices, causing them to lose the next election, effectively paving the way for a far-right government that not only reverses the carbon tax but also blocks permits for solar cells and windmills. Aks yourself was it then really a good policy? Summarizing: policy recommendations should take seriously their actual, real-world implications, not just what the narrow model would suggest.

## What is a policy argument

So what is a policy argument? I would sugggest they can broadly be categorized into two groups:

1) Statements about the properties of the policy.
2) Statements about the real world under a given policy.

The first one can be thought of statements that point towards desirable (or undesirable) attributes of the policy, e.g. the people most willing to pay to pollute is a good way to figure out who should have the right to pollute. Often these arguments are good, not necessarily because they are implementable, but they highlight a desirable way to think about policies about a given topic. The second, at its core, it is a claim about a counterfactual: what would happen to some outcome if we did policy A rather than policy B (or the status quo). The point here is not to say what should be valued, but to say what would happen, given the world we live in. A good policy argument, in the second category, therefore succeeds to the extent that its implied counterfactual is realistic.

However, there is a common ambiguity in policy recommendations: which counterfactual world are we talking about? Is it the real world, with messy politics, limited state capacity, and voters who might punish you for higher gas prices? Or is it a hypothetical world where the policy is implemented cleanly, enforced perfectly, and kept in place for decades? In practice, economists (and other social scientists) often slide between these worlds without saying so. I.e. is it the first category or the second. In this blog, I emphasize policy arguments about the real world.

Concretely, a policy argument always rests on a model. Here I use “model” in the broad sense: a set of assumptions about behavior, institutions, enforcement, and time horizons that lets you translate “implement policy A” into “here is what happens next.” The model can be implicit or explicit, but it is always there. And because it is there, any policy conclusion is conditional on it.

This brings us to the key complication: model uncertainty. There are usually multiple plausible models of how the world will respond. A responsible policy argument should therefore ask: under each plausible model, what would happen under policy A and under policy B? And then, instead of pretending one model is “the truth,” we should weight the models by how plausible we think they are and average the outcomes. Put differently, the argument is not “A is best under my favorite model,” but “A is best after accounting for the fact that the world might work differently.”

One important observation follows immediately: model uncertainty only matters when different plausible models rank the policies differently. If every reasonable model points to the same policy, then it's easy to choose between policies, however that's rarely the case. The optimal policy is not always the same across models, the “missing assumptions” become the whole argument.

# Demand and Supply and the welfore theorems dominates (as it should)

Often what happens in practice  is (especially when economists make recommendations) is they focus on a demand and supply model and the first and second welfare theorem. Not to go into to much detail, they assume individuals generally are well informed and are able to make somewhat _utility maximizing_ decisions, i.e. people allocate their money towards the consumption and investments they prefer. Additionally, they assume that markets are able to _clear_, that is the price system will allow for getting the economy into an equilibrium, i.e. individuals would not prefer to alter their _consumption basket_ at given prices. Additionally, usually economists will then use insight of the second welfare theorem, which states, that we can redistribute resources (concretely tax the rich and give to the poor). After this transfer prices will readjust the economy into a new equilibrium.

This is a very effective framework for thinking about policies, and should also be the first tool in my opinion, an expert reach for when giving recommendations. In the case of climate change they idea is, that there is an externality (carbon emissions) that is not probably captured by the price system. And both cap-and-trade and carbon taxes, try to integrate these externalities into a standard supply and demand framework, so people will reevaluate their consumption patterns given they now have to pay for their emissions.

This insight here is recommending a carbon tax or a cap and trade system is a really good idea, if it was politically feasiable and palatable, which is probably not the case in the real world. I.e. The policy recommendation is all of a sudden a statement about something completely else than about how to effectively reduce emissions, it's a statement about efficiency, and how to internalize the externalities. It's a bait-and-switch, exchanging one question for another.

# Elaborating on the Carbon Tax Example

Let's again consider the first example, but now with a bit more detail. As mentioned, we imagine a center-left government asking for advice on reducing carbon emissions. We consider that the policy maker only considers 2 different policies. 

- A carbon tax (A)
- An Investment fund in green infrastructure (B)

For simplicity and clarity we will restrict ourselves to two models with starkly different policy recommendations. One model, where any policy implemented will have an infinite life time. I.e. a carbon tax (or investment fund), will sustain themselves until their planned terminations (say 10 years in the future). Conversely, we also consider a model, where the opposition party, if we winning will reverse a carbon tax, but not be able to shut down the climate fund. We can draw the CO2 emissions (y-axis) as a function of time (x-axis), and we can draw the outcome under the different models in different colors (red and green). Finally we can in one number summarize the aggregate carbon emissions in one number, under each model. I.e. we are considering two policies under the two models; a pure _optimal efficiency_ model, and a game theoretic election model. 

*Inserting figure carbon_emissions_by_model*

Next, we can think about the probabilities of each model of the models being true. Finally we can plot the expected carbon emissions of each policy (y-axis), under varying probabilities of which model is true (x-axis), where the policies expectation intersect, is where one should switch between each model, whether to prefer an investment fund or a carbon tax.

*Inserting figure carbon_cumulative_vs_probability*

As seen from the plot, it's not exactly obvious what, is the best policy recommendation, it's strictly a function of what we believe about how the real world of policies actually work. 

# Just use prediction markets

One somewhat obvious way is to make markets for policy recommendations. If experts really believe that a carbon tax will reduce a countries emissions by a certain amount at a given time horizon, well, then they should put there money where there mouths are. This is of course, not the case of categori 1 policy recommendations. It's perfectly reasonable to hightlight the strengths of a carbon tax, without claiming it's the most effective way to reduce emissions, but making policy recommendations more incentive driven, would probably be a very healthy exercise and for injecting a healthy dose of epistemic disciplin into expertice vendors. 

This would additionally, be a very inexpensive way to survey a disciplin about the effects of a policy, and a way to make academics and think tanks work for their money. Concretely, publicly awarded grants could have 20 percent of the funds being allocated into _expertise markets_, where an appropriate incentive structure was implemented for giving advice. In the long run, it would make academics and other experts not only healthy feedback on whether their beliefs are accurate (considering the work of Philip Tetlock, we should probably be scepticle about that), but also, it would be way to disciplin policymakers. Most policies are expensive, and if they bet against the experts, or make choices/decisions that are at odds, with what is suggested, it would be an effictive way to communicate this publicly, while still avoiding an overly political angle, which sometimes can be seen in expert statements.

# Rent control in Copenhagen.


Let's return to a topic of a previous article (the housing market)[https://open.substack.com/pub/unreasonabledoubt/p/why-new-housing-lowers-or-raises?utm_campaign=post-expanded-share&utm_medium=web], concretely, rent control. In the public debate, rent control has been suggested, primarily be left wing politicians, as a way to combat rising housing costs in Copenhagen. Going back to the model, presented earlier, this could be considered a bad idea. Why? because in the long run, we would suspect that the supply, would shrink, or at least not expand, addequatly. The price cap, would artifically, lower the aggregate supply of housing in the city, effectlively, removing many from moving to the city. Again, i believe the (modified) 101 reading of the economic problem is correct! price controls have some pretty bad consequences for the supply. That said, in the case of copenhagen, do I really believe, that removing rent control would have any substantial effect on the supply? Honestly, no! I would not put my money on it, and i do not think many of the proponents of removing rent controls, would either! The limited new housing in copenhagen, is not due to price controls, but the lack of political will (especially by the left wing) to build more. Poorly thought out environmental protection (link) and climate considerations (link), is more likely the real reasons, why Copenhagen is behind on building more housing. Looking at the actual data, we can see that the left wing parties in Copenhagen, actually even though, they keep talking about more and affordable housing, are actually voting against it (link). If rent control is what makes building more feasible, i.e. it makes is politically more expensive for the left wing parties to not build more, then rent control becomes the YIMBY policy position.

# Conclusion




