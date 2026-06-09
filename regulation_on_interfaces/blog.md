# Regulation should depend on interfaces.

- Danish politicians want to incentivize danes to have more stocks. Concretely they have introduced the "aktie-spare-konto" a certain bank product that allows you to store stocks and the first amount will be taxed differently.
- This is a good idea but it introduces a very strange coupling between banks and stock deposits?. This is probably a more general issue with regulation: they depend on concretions. Hereobservations from programming would be useful: The dependency inversion principle. Concretely, if you implement a tax, it should not depend on a concrete implementation detail (such as where you stocks are counted), but on a more general notion of "you own stock".
