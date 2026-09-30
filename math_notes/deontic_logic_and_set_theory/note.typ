= Decision Theory and Deontic Logic

If we consider all possible actions as the space $cal(A)$, then we can consider the rules of SDL (Standard Deontic Logic), and how it maps to set theoretic primitives and next how that maps to a decision theory. I.e. how to decide on which actions to choose from.

== Rules of SDL

Standard Deontic Logic is usually defined as the normal modal logic $K D$ with the obligation operator $O$.

+ $O phi$: it is obligatory that $phi$.
+ $P phi := not O not phi$: it is permitted that $phi$.
+ $F phi := O not phi$: it is forbidden that $phi$.

Now, consider how these primitives map to standard set theoretic concepts.

$O phi$ is a statement about a set of actions. If $phi subset.eq cal(A)$, then $O phi$ says that the admissible actions must be in $phi$. Equivalently, actions outside $phi$ are forbidden:

#[
  $
    O phi => forall a in phi^c, F {a}.
  $
]

Here $phi^c = cal(A) minus phi$. This is not yet a full preference ordering. SDL does not compare every pair of permitted actions. But when actions are mutually exclusive, an obligation induces a strict decision-theoretic priority over the excluded alternatives.

Suppose $a, b, c in cal(A)$ are mutually exclusive actions. Treat each action as the singleton proposition ${a}$, ${b}$, and ${c}$. Mutual exclusivity means:

#[
  $
    {a} -> not {b}, quad
    {a} -> not {c}, quad
    {b} -> not {a}, quad
    {b} -> not {c}, quad
    {c} -> not {a}, quad
    {c} -> not {b}.
  $
]

If ${a}$ is obligatory, then the alternatives are forbidden:

#[
  $
    O {a}
  $
]

#[
  $
    {a} -> not {b}
  $
]

#[
  $
    O {a} -> O not {b} quad "by Regularity"
  $
]

#[
  $
    O not {b}
  $
]

#[
  $
    F {b} quad "since" quad F phi := O not phi
  $
]

The same argument gives $F {c}$. So, relative to the choice set ${a, b, c}$:

#[
  $
    O {a} => F {b} and F {c}.
  $
]

Now define the induced strict deontic priority relation $succ_D$ as:

#[
  $
    x succ_D y <=> O {x} and F {y}.
  $
]

Then:

#[
  $
    O {a} => a succ_D b and a succ_D c.
  $
]

This relation cannot contain cycles. For example, suppose we had:

#[
  $
    a succ_D b, quad b succ_D c, quad c succ_D a.
  $
]

By the definition of $succ_D$, the first priority gives:

#[
  $
    a succ_D b => F {b}.
  $
]

And the second gives:

#[
  $
    b succ_D c => O {b}.
  $
]

But $F {b}$ is defined as $O not {b}$, so we have:

#[
  $
    O {b} and O not {b}.
  $
]

This contradicts the $D$ axiom:

#[
  $
    not (O phi and O not phi).
  $
]

Therefore SDL, when mapped into decision theory through mutually exclusive actions and the induced priority relation $succ_D$, rules out cycles of strict deontic priority. The point is not that SDL creates a complete ranking over all actions. Rather, obligation over an exclusive choice set creates strict priorities against the forbidden alternatives, and those priorities must be acyclic.




#line(length: 100%)

The proof system contains the usual propositional tautologies and inference rules, plus the following deontic principles:


#[
  $
    frac(phi -> psi, O phi -> O psi) quad "Regularity"
  $
]

#[
  $
    O(phi -> psi) -> (O phi -> O psi) quad "K"
  $
]

#[
  $
    O phi -> P phi quad "D"
  $
]

#[
  $
    frac(phi, O phi) quad "Necessitation"
  $
]

Equivalently, the $D$ axiom can be written as:

#[
  $
    not (O phi and O not phi)
  $
]

This says that SDL does not allow a proposition and its negation to both be obligatory. In the action-space interpretation, if $phi subset.eq cal(A)$ names the set of actions satisfying $phi$, then $O phi$ says that the admissible actions must lie inside $phi$, while $P phi$ says that $phi$ is not ruled out by obligation.
