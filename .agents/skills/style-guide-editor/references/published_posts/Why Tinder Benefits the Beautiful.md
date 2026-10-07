# Why Tinder Benefits the Beautiful

*Search frictions and match fractions, and who is better off in a world of online dating.*

Jeppe Johansen · November 12, 2024

Figures: [source PDF](<Why Tinder Benefits the Beautiful - Unreasonable Doubt.pdf>).

Online dating is still becoming a more and more popular tool for finding a partner — just look at the graph below.[^1] Intuitively, this makes sense. It’s hard to see who is single and open for a relationship when roaming the real world. However, online dating allows for easy identification of other people looking for a relationship. Especially with the advent of Tinder, it is not uncommon for people to have hundreds if not thousands of matches. That is, singles have hundreds of potential relationships, in the sense that both parties have, at least on a very superficial level, sent a signal of romantic interest. However, many of these people do not end up in relationships. If Tinder really worked, should we not expect a wave of relationships to be formed and a total extinction of singledom? Yet, this is not what statistics tells us. As the figure below shows, though people meet online they are still more single than ever — this blog post explores why. Specifically, this post distills why it is important to distinguish between search friction and match friction. Finally, it also investigates who are the winners and losers of Tinder (and more generally online dating) and why immense reductions in search frictions for partners do not necessarily benefit everyone.

## The Model

Let’s start by setting the stage. To explore the questions above we start by setting up a model. The model used in this post considers a world where men sequentially propose to women who tentatively accept the relationship until a better man swings by. When the men in the model have hit up all the women they were interested in the dating game ends.

Concretely, consider a single-period game, where all men in the “economy” are endowed with $k$ possible women to ask out for a date (we only assume heterosexual relations). Concretely, we could imagine that all men have exactly 5 potential relationship candidates. This is of course a simplification as men know a varying number of single women in real life, however, this simplification does not change the results of the model. These potential partners do not necessarily need to be attractive enough for the men to want to enter relationships with them (or vice versa), rather they consist of the pool of potential partners, i.e. singles.

Now, there is a specific cost to invest in getting a date. First, you use time and effort to get in contact, and secondly, humans allocate emotional real estate in getting a date. In this very simple world, only men ask women out. Again, a simplifying assumption for getting anywhere with the model.

Finally, we also assume that all men and women have a certain level of attractiveness. The attractiveness is defined below, where the attractiveness level is between 0 and 10. The attractiveness level is composed of two subcomponents:

1. A general attractiveness level ($v$)
2. A personal (unique/idiosyncratic) attractiveness level ($v_i$):

$$
\text{attractive}_i = (1-\alpha)v_i + \alpha v, \qquad v_i,v \sim \operatorname{Uniform}(0,10)
$$

So intuitively the attractiveness of a person can be considered a weighted average between an attractiveness level shared by everyone, called $v$, and a unique (idiosyncratic) to the individual level denoted $v$ with subscript $i$. So intuitively all women will rate the men on a scale from 1 to 10. If alpha (the funny looking a in the equation) is 1, all the women will rate the same man equally. Put differently under a regime of alpha=1 a man rated by one woman as 7.2 will also be rated exactly as 7.2 by another woman. However, if alpha=0 then there will be no correlation between ratings of the same man for different women, i.e. one woman will give a man 3.4, and other women will come to an entirely different level of attractiveness. Finally, men value the attractiveness of women by the same model as women do of men.

Now we also need to model how men decide who they will try to get on a date. As described in the beginning they have $k$ potential women they can try to get on a date, but it’s costly to try to get a woman on a date. We model this the following way: The men rank all the women by attractiveness and then have a decision rule whether or not they want to date them. The rule is given as attractiveness minus the cost needs to be above some threshold:

$$
\text{Try to get date}_{i,j} =
\begin{cases}
\text{Yes}, & \text{if } a_{i,j} - j \times c \ge t, \\
\text{No}, & \text{else.}
\end{cases}
$$

Here $i$ denotes the man and $j$ denotes the index of the woman. Again consider the $k$ women sorted by attractiveness, then the third most attractive woman will be indexed with $j=3$. So the formula applied $a-jc$ is attractiveness minus the index $j$ times the cost. The parameter $t$ represents the threshold, that attractiveness − cost must be above for the man to try to get a date. Below is a simple example:

Mike has 5 single women in his life he potentially could get in a relationship with, ordered by his preferences, they are Anna, Beatrice, Caroline, Denice, and Ellen. On a 10-point scale a rank them 7,5,4,2,1, respectively (again, I hope this reader knows this does not reflect my actual view of how this goes, on but helps as a simplifying view). We can now calculate the values. For simplicity assume the cost parameter $c$ is 1, and his threshold is 0:

- Anna: $7 - 1 \times 1 = 6 > 0$ (Mike invites Anna on a date)
- Beatrice: $5 - 2 \times 1 = 3 > 0$ (Mike invites Beatrice on a date)
- Caroline: $4 - 3 \times 1 = 1 > 0$ (Mike invites Caroline on a date)
- Denice: $2 - 4 \times 1 = -2 < 0$ (Mike does not invite Denice on a date)
- Ellen: $1 - 5 \times 1 = -4 < 0$ (Mike does not invite Denice on a date)

We see that given his options, Mike will choose to get into a relationship with Anna, Beatrice, and Caroline (in that order), but he will pass on Denice and Ellen. However, dating markets have the important property, that you are only committed to one relationship at a time. I.e. if Mike asks Anna out and they get into a relationship then Beatrice and Caroline will never get the chance, even if they would have liked to. Concretely, in this model, men interact with all the women that they find attractive enough, i.e. even though Mike can only get into a relationship with one, he contacts all three candidates. This is explored in more depth in the next section. Finally, also note that had Mike only been presented to Denice (and not Anna, Beatrice, Caroline, and Ellen) he would have tried to go on a date with her, since she would be indexed with $j=1$, such that:

- Denice: $2 - 1 \times 1 = 1 > 0$ (Mike invites Denice on a date)

Again this is only the case because in this example, Mike has not been presented with other women than Denice, so he has not invested energy in trying to get on dates with other women. In other words, the women Mike decides to try to get into a relationship with is contingent on the total pool of potential partners he is presented with.

## Clearing The (Dating) Market

After all the men have “suited” the women they deemed attractive enough, the women also sort the “suiters” by attractiveness. Following this the market is “cleared” that is the matching process is performed by the Gale-Shapley/Deferred acceptance algorithm. The process can heuristically be understood like this:

1. Initialization:
   - Every man and woman is initially single.
   - Each man has a list of women in order of his preference.
   - Each woman has a list of men in order of her preference.
2. Proposal:
   - Each day, every single man proposes to the top woman on his list (the woman he most prefers and hasn’t proposed to yet).
   - After the proposals, the women look at all their suitors of the day and if they're single, they'll "tentatively" accept the proposal from the man they like most. If they already have a tentative partner but prefer the new suitor more, they will "break up" with the current suitor and tentatively accept the new suitor's proposal. The rejected man will move on to the next woman on his list the following day.
3. Rejection and Further Proposals:
   - The rejected men from the previous day will propose to the next woman on their list.
   - Again, each woman will pick her most preferred suitor from her current tentative partner and the new suitors of the day.
4. Termination:
   - This process continues with men proposing to the next woman on their list after facing rejections until every man and every woman is paired up. Or alternatively, the men’s lists are exhausted.

The Gale-Shapley algorithm has multiple nice properties, but for this application, those are not necessary to hash out. More importantly is it, to a first-order approximation, a good description of the dating market.

## Search Friction and Match Friction

Before moving to the next section, which more closely compares how Tinder impacts dating markets, let’s first consider the difference between search friction and match friction. Search friction is commonly used to describe inefficiencies that arise when individuals attempt to find mutually beneficial transactions, however, in this model, it’s more narrowly defined as the number of potential partners the individuals could try to get on a date $k$. Match friction in this model refers to how the aggregate market is characterized with regard to the number of relationships. In this model search friction simply conveys how big the potential pool of relationship partners is, concretely $k$. So reducing search friction would correspond to increasing $k$ in this model. Again we see this is an important parameter in dating markets. It has also been recognized earlier as a reason why sexual minorities move to big cities since if the pool of potential partners is very small, it is natural to think it is very hard to find a partner.

In this model match friction is not captured by a parameter but corresponds to the aggregate number of matches in the dating market. A dating market with a lot of match friction will be characterized by a large number of singles, relative to the number of people in relationships. It is important to distinguish between these two types of frictions, since, one can easily see how one can make a mental leap from reducing search friction to implying a reduction in match friction. However, as the paragraph below investigates, this is not necessarily the case: When preferences are correlated, i.e. people generally consider the same people attractive, reducing search cost might not lead to less match friction.

## Simulating Tinder vs The Good Old Days

Let us finally consider the advent of Tinder. Tinder can be considered as a way to reduce search friction, or put differently, increase the number of women men can potentially try to get on a date, $k$. So, the question we can ask with this model is whether a world with reduced search frictions will be characterized by more matches/relationship, i.e. also reduce match friction. We use our model to simulate the different scenarios. We simulate 2500 men and 2500 women. We consider different scenarios along two dimensions:

1. The extent to which people share preferences.
2. The degree of search friction.

We consider a range of values of alpha i.e. the extent to which people share attractiveness valuations, and the number of potential suiters for women. First, we assume a range of values on the interval between 0 and 1 of alpha. Secondly the number of potential suiters $k$ go from 3 to 60. We evaluate the output of the model on the following two metrics: 1) Total number of relationships (denoted matches in the plots) in the economy, and 2) The average attractiveness of men and women in a relationship. These metrics allow us to roughly reason about who is better off and worse off in a world with Tinder. Concretely, will a tool like Tinder create more or fewer relationships, and will the people in relationships appear more or less attractive?[^2]

To summarize, when search friction is reduced, does the match friction then go up or down? Does it actually become easier to get in a relationship, in a world where Tinder exists?

## Simulation Results

The figures below show the results. The three plots show the number of potential partners on the x-axis (what is called $k$ in the model). Again, consider a low number of potential partners as the pre-Tinder era, and conversely a high number of potential partners as the post-Tinder era. The colours of the lines denote the extent of how preferences correlate, going from blue to red, where blue captures where preferences are perfectly uncorrelated (alpha=0), and red captures when they are perfectly correlated (alpha=1). Note, that empirical preferences have been shown to display a high degree of correlation, i.e. the real world seems closer to the red than the blue line.[^3]

The leftmost plot shows how the aggregate total number of relationships evolves under the different scenarios. This is captured by the y-axis that denotes the total number of relationships, which is denoted number of matches on the y-axis label. As the plot shows, the degree to which reducing search friction increases the number of relationships is very contingent on how correlated preferences are. Put differently, Tinder only increases the total number of relationships, if individuals’ preferences differ. If everyone thinks the same people are attractive, Tinder actually reduces the total number of relationships.

Next, even though attractiveness is hard to reason about when it includes an idiosyncratic component, one finds a very consistent pattern, namely, that reducing search friction increases the (perceived) attractiveness of people in relationships, at least as experienced by their partner, because a larger dating pool allows people to match with more attractive partners. This can be seen from the middle and rightmost plot. The y-axis captures the average attractiveness of women and men in a relationship, respectively, which is seen increasing as $k$ increases. Interestingly, the picture is more murky with respect alpha, where the alpha of approximately 0.5 (an intermediate value between the two extremes), is associated with the lowest perceived attractiveness. Intuitively this happens because now preferences are correlated, so congestion becomes a more prominent feature of the market, however, people are still to a high degree ending up in relationships, i.e. as alpha increases, still fewer will end up in relationships.

## Conclusion

Combining these two insights yields an important lesson. In a world with a high degree of shared preferences for partners, reducing search friction makes the world more of a winner-take-all market. Intuitively, this can be understood as when the dating pool expands, more people can approach the most attractive candidates, allowing for “mating congestion” where everyone flocks around the same few attractive candidates. Due to the cost component in the model, which we intuitively can think of as time or energy, women who would be deemed attractive to the males in a model with fewer partners become unattractive as the pool increases.

Why has Tinder not caused a wave of new relationships, and reduced the number of singles in the modern dating environment? As outlined, Tinder reduces only one kind of friction, namely search friction and this is not the only important variable in a dating market. Concretely, as the simulations show, when people share preferences for partners, reducing the search friction by increasing the pool of partners can actually have the complete opposite effect of what is intended, namely more unwilling singles. Additionally, the simulations show that the gains of the larger pool of potential romantic partners accrue to the people who in general are deemed attractive. Concretely, having access to a larger pool of potential partners does not help everyone, only the select few, everyone wants to end up with.

[^1]: The graph is from “Graph of the Day: How Couples Meet, 1940–2020” by Steve Stewart-Williams, published in *The Nature-Nurture-Nietzsche Newsletter*.
[^2]: Attractiveness in this context is challenging to quantify due to its individual-specific component ($v_i$). A more accurate perspective is to view attractiveness not as an objective quality universally agreed upon, but rather as something defined from the partner's unique viewpoint.
[^3]: Cunningham, M.R., Roberts, A.R., Barbee, A.P., Druen, P.B., & Wu, C. (1995). “Their ideas of beauty are, on the whole, the same as ours”: Consistency and variability in the cross-cultural perception of female physical attractiveness. *Journal of Personality and Social Psychology*, 68, 261–279.
