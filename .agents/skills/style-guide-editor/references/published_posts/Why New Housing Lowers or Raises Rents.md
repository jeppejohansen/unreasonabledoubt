# Why New Housing Lowers or Raises Rents

*Disciplining the NIMBY/YIMBY debate with a simple framework.*

Jeppe Johansen · September 10, 2025

Figures: [source PDF](<Why New Housing Lowers or Raises Rents.pdf>).

One of the most important discussions at the current moment revolves around housing policies, especially whether or not to build more in cities, often referred to as the NIMBY/YIMBY[^1] debate. From the new Derek Thompson and Ezra Klein book *Abundance* to Sam Bowman’s examples, many people point to housing as one of the most important policy issues. However, I have long been unsatisfied with the arguments put forward by the pro-housing crowd, not because I think the arguments are wrong, but rather because I feel they are insufficient. Or put differently, they rely on a simple economic heuristic, namely that *demand slopes downwards, so we just need to build more*[^2], which I believe is insufficient to reason about good housing policies. The observation about demand is correct; however, it seems not to take seriously what the NIMBY crowd (and basically the argument you will encounter when you are home for Christmas and speak with your distant family) is putting forward: *Look how expensive it is to live in the city.* This post presents a simple model built on a sound microeconomic foundation that allows for multiple extensions, which can help people reason about housing markets and building-more-in-the-cities-arguments and other suggested policies for making the city more livable. The model also attempts to be accessible for a broad audience, not only economists, so more people have a tool to dissect whether or not suggested housing policies rest on coherent arguments.

## The YIMBY and NIMBY crowds’ arguments

The YIMBY argument basically relies on a very simple heuristic: demand slopes downwards. This might be the most important Econ 101 observation: when things get more expensive, people consume less of it, and conversely, if supply expands, the price drops. Concretely, in the case of housing, people often model housing (at least in the short run) as perfectly inelastic: An expansion of the housing stock will lower the housing price in the city.

The NIMBY argument is harder to distil into a single tenet. Usually, it rests on environmental considerations, vague claims about the “vibe of the city”, but also, importantly for this post, that when we look at prices in cities versus rural areas, housing in cities is considerably more expensive. From there, a lot of people conclude that building more in the city will not lead to lower prices.

Summarized into two plots, the YIMBY and NIMBY positions are, respectively:

In other words, the two arguments are both based on real observations, namely that population density is empirically associated with higher housing prices, while a very robust finding from economics is that expanding the supply lowers the price.

## A Simple Model of Housing

I am fundamentally a YIMBY person; however, I do believe the YIMBY crowd has not really taken the observation from the NIMBY crowd seriously. At least at the surface, these two arguments do seem to be in conflict with each other, and I wanted a framework for thinking about this in a disciplined way. I want the equivalent of a stylized macroeconomic model (IS-LM/AD-AS) model for housing, with reasonable microeconomic foundations, that can be applied exclusively using graphical reasoning, which is what led me to formulate this model. Finally, let me note that this post does not contain the math behind the model, so it can be consumed by a larger crowd; however, the math does exist!

### The Demand Side

First, let’s start by considering the individual household’s decision problem. Every household decides between living in the city or in a rural area, i.e., we make the assumption there are only two types of housing: city and rural, and for simplicity, they are all alike.

The households choose to live in the city if the income minus the price of housing is higher in the city than in the rural area. Of course, this assumption can be adjusted to a more subtle utility formulation; however, it does not change the predictions. Distinguishing between the income in the city and the rural area, we say that in rural areas, they get an average wage and some household-specific rural premium, while in the city, the household also gets an average wage, some household-specific urban premium, and importantly, also an agglomeration premium. Concretely, this implies that the more people that live in the city, the more productive the city population becomes. This is very much in line with research from economics. We can therefore make a stylized description of the utility of living in the city and in rural areas:

- Rural Utility: Rural Base Income + Household Specific Rural Premium − Rural Price
- City Utility: City Base Income + Household Specific City Premium + Agglomeration Effect − City Price

Summarizing, the individual household chooses to live where they have the highest income the price of housing. We realize this is a function of the price delta. We can now aggregate over all households in the economy, and express the aggregate demand for living in the city as a function of the price delta between the city and rural areas. Note here an important observation: all individuals need to either live in the city or in a rural area. The implication being that when we know how many households live in the city, we also know how many live in rural areas. The demand for living in the city is shown in the figure below:

### The Supply Side

We now consider the supply side of the economy. In this part of the economy, we need to consider the supply of housing in both the city and rural areas.

Since we have the population identity, i.e., all households must live either in cities or rural areas, we can also express the supply of rural housing as a function of the number of people living in the city. That is like flipping the supply for rural areas (green graph) along the vertical axis, so it starts from that total population line. This flipping allows us to gauge the price of housing in the city and in rural areas if we know how many people live in the city. Below is a plot that shows this:

We can also read off all the feasible distributions of people living in the city and in rural areas directly from this plot. That is, we cannot have an equilibrium outside of the two vertical lines. This is due to the fact that the vertical lines show the capacity, and if we say we had an equilibrium to the left of the rural capacity, for example (green vertical line), then there would be an excess number of people living in the city, i.e., beyond the capacity of the city.

If we now subtract the rural supply from the city supply, we get a supply function (of both city and rural areas) as a function of the population living in the city, with the price delta on the Y-axis. Why is this important? Because it allows us to graph supply against demand! All of a sudden, we can graphically reason about demand and supply!

Some useful things to observe about the demand and supply. The equilibrium is found by looking at the difference between city and rural prices. In other words, we cannot directly read off the graph what the price level is in the economy; we can only see the difference. Additionally, the slope of the demand (and supply) is important to understand the sensitivity to shocks. The flatter the curve, the more sensitive, i.e., a small shock in the form of a level change to either the demand or supply will imply many people moving either from or to the city.

## The Full Model

Below, we have the full model displayed. The top plot allows us to reason about prices and which supply-side, either city or rural, is subject to a shock. The lower plot is used for reasoning about supply and demand generally in the economy.

We can reason about two different scenarios and how they propagate through the model: demand shocks and supply shocks.

Demand Shocks are easiest to reason about. Concretely, you start in the bottom plot. The shock to the demand curve will yield a new equilibrium (where supply and demand intersect), which allows us to read on the x-axis the number of people living in the city (and therefore also in rural areas), which we then can map to the top plot, where we can read off the new prices[^3]. Concretely, imagine the demand moved upwards/rightward. That corresponds to more people wanting to live in the city, which again allows us to move to the top figure, and read off the prices, which now (in general) will be higher in the city, and lower in rural areas. Summarizing, a demand shock requires:

- Bottom plot: Move demand curve → New equilibrium implies a new city population and new price difference.
- Top plot: New city population → New prices.

Supply Shocks require one more step to reason about. In that case, we start by moving the relevant supply curve (this is what happens in the case below, where we simulate a housing expansion). Concretely, we start in the top plot. We choose which of the supply curves (or both) we want to move/shock. This yields a new aggregate supply curve in the bottom plot. This again yields a new equilibrium, which can be read off from the bottom plot where demand and aggregate supply curve intersect, yielding a new price difference, and a new equilibrium city (and rural) population. The adjusted city population sets in motion a demand adjustment due to the agglomeration being a function of the number of people living in the city. This corresponds to moving the demand curve once more. Summarizing the agglomeration effect: *More people living in the city implies even more people want to live in the city, and vice versa.* The new demand curve yields a new equilibrium, i.e., the price difference and city population adjust.

Moving back to the top plot, we can from the adjusted city population, read off new prices in the city and rural areas. Summarizing the chain of events:

- Top plot: Move the relevant supply curve (rural or city)
- Bottom plot: Adjust supply curve → new equilibrium → new level of agglomeration effect → New demand curve → new equilibrium → new city population and price difference.
- Top plot: New city population → New prices.

## Case: Expanding The Housing Stock In The City

Now we consider one of the most often suggested policies, especially popular among the YIMBY crowd: *we need to build more in the city!* So in three phases (corresponding to blue, red, and green curves in the plots below), we investigate an increase in the housing supply in the city.

We start in the equilibrium shown below. This period is all drawn in blue. The bottom plot shows the equilibrium, where demand and supply intersect, and the blue dots in the top plot show the initial equilibrium prices.

Now, more housing is built in the city. This leads to a supply curve of the city that is pushed down to the right (red). We see that both the expanded capacity (the vertical part of the supply curve) is more rightward, and that the sloped part is moved down. In the bottom plot, we can see this is reflected in a new aggregate supply curve, which (part of) is also moved down and to the right, yielding a new equilibrium. We can see that more households now live in the city compared to the initial equilibrium, and (since demand slopes downwards) the price of housing in the city has become relatively cheaper compared to rural areas. In the top plot, we see that the general price level has decreased. That is, the prices in both the city and in rural areas have fallen.

Now the agglomeration effect kicks in and demand adjusts. The new, increased population in the city leads to agglomeration (i.e., it’s more desirable to live / people earn more in the city). This can be seen in the bottom plot as the new demand curve (green) is moved upwards to the right. This yields a new equilibrium where even more people live in the city. And even more troubling, the price difference has actually increased compared to what it was initially! Additionally, when we move to the top plot, even though the prices fell with the initial expansion of the housing stock, the house prices in the city are actually now higher than they were initially. The agglomeration effect has dominated the initial supply effect! The prices in rural areas have decreased even more.

This example is the extreme case where agglomeration dominates the supply effect. This is not a given feature of the model, but rather depends on individual belief in how strong agglomeration effects and other structural features of the model are. Again, this model should not be seen as a way to give precise predictions, but rather to discipline reasoning in a debate that often seems to lack any sort of rigorous application of a model and disciplined thinking. And now, when you encounter people arguing that building more in the city only raises prices, you know they must assume agglomeration dominates the increased supply. At least if they want to be coherent.

## Conclusion

This blog presents a simple model that allows for graphical reasoning about housing policies based on sound micro foundation, i.e., optimizing households and reasonable supply assumptions, and with the important feature of taking agglomeration effects seriously. An important takeaway is that it bridges two crowds, namely the NIMBY and YIMBY crowds, with a unifying framework that easily allows for extensions. Finally, I investigated one of, if not the most important case in housing policy, namely the obvious *just build more* argument, and what is obvious is that this only leads to lower prices in the city if the agglomeration effect does not end up dominating the supply effect.

[^1]: NIMBY is short for “Not in my backyard,” and YIMBY is for “Yes in my backyard”. These terms distinguish between anti- and pro-building more in the city (and in general) crowds.
[^2]: Yes, there are special cases, but we are not considering those!
[^3]: We wait to model agglomeration effects in demand in the supply shock scenario.
