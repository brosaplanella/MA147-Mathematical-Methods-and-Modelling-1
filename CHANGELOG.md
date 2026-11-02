# CHANGELOG

## 2026-11-02

* Preface: corrected the author names of Witelski and Bowen in the reading list, updated the link to the module page, and made the chapter names consistent with the chapter titles.
* Chapter 1: fixed underlined text that was not rendering in the HTML version.
* Section 2.1: fixed a cross-reference to the general differential equation.
* Section 2.4: fixed the identification of the coefficients with the general linear equation ($a_1 = -1$, $a_0 = r(t)$).
* Chapter 2, mixing problem example: the amount of chlorine is now consistently denoted $c(t)$ (it was sometimes $q$ or $Q$), and fixed a sign error in the exponent of the solution.
* Chapter 2, coffee cup example: fixed the initial condition ($t_0 = 0$ and $x_0 = T_0$), which is now used from the start of the calculation.
* Chapter 2, separable equations example: fixed the function $\xi(x)$ (it should be $e^{-x}$).
* Section 2.5: in the substitution for quotients of $y$ and $x$, the scaling factor $a$ must be non-zero, and clarified how the invariance motivates the substitution $z = y/x$.
* Section 2.6: "fixed points" replaced with "stationary points" for consistency.
* Section 2.6.3: in the saddle-node bifurcation, fixed the stationary points and the derivatives $f'(x_{1,2}^*)$ for $r<0$ (they should involve $\sqrt{-r}$).
* Section 2.6.3: fixed $f'(x^*)$ in the transcritical bifurcation, and in the pitchfork bifurcation fixed the reference to the sign of $f'$ for $r=0$ and swapped panels a) and c) of the phase line figure so they match the caption.
* Section 2.6.3: the cases in the saddle-node and transcritical bifurcations are now listed in the same order as in the figures ($r<0$, $r=0$, $r>0$), and the caption of the pitchfork bifurcation diagram now explains the line styles.
* Example 2.14 (fishery): the growth rate is now denoted $k$, consistent with the population growth example.
* Section 2.7 and Section 6.3: fixed the definition of linearly independent functions (the equation must hold for all $t$, not for all $l_1, l_2$).
* Section 2.7: in the corollary for the homogeneous initial value problem, $v(t_0)$ replaced with $\dot x(t_0)$, and in the remark that follows it, "and" replaced with "or".
* Section 2.7: fixed a typo in the proof of Lemma 2.4 and made the notation $x_\mathrm{p}$ consistent. The proof of Lemma 2.5 now refers to its own solution formula instead of the one in Lemma 2.6.
* Section 2.8: fixed two sign errors in the computation of the roots in the two real roots example, and made the labelling of $x_1$ and $x_2$ consistent between the two particular integral examples.
* Section 2.8.5: fixed a few minor typos, and completed the truncated caption of the overdamped figure.
* Section 2.8.5: the spring constant is strictly positive ($k > 0$), and clarified in which sense the critically damped case decays faster than the overdamped case.
* Chapter 2: fixed cross-references that rendered as "Section Section", "Figure Figure", etc.
* Chapter 2: fixed minor typos and typesetting issues.
* Example 3.1: small change to clarify notation.
* Chapter 3: small typo in Euler's method.
* Chapter 3: replaced $f_n$ with $s(n)$ for consistency with the notation used in the rest of the notes.
* Section 3.2.2: fixed the general solution of the non-autonomous first order difference equation.
* Section 3.4.1.1: title of the section changed to "Real roots" to be consistent with the other two cases.
* Section 3.4.1.2: defined $p$ and $q$ for complex roots, and added a remark on choosing the correct quadrant for $\theta$ when $p < 0$.
* Example 3.4: removed some legacy text.
* Chapter 3, complex roots example: the final solution is now inside the example box.
* Chapter 3, exponential particular integral example: fixed sign of the coefficient ($D=-3$).
* Proof of Lemma 3.1: fixed a typesetting issue.
* Section 3.6: fixed the logistic map in the remark on the edge cases ($x_{n+1}$ instead of $x_1$) and the notation for $f(x_n)$ in the period two orbit.
* Section 3.6: for $\lambda > 3$ the derivative at the non-zero stationary point of the logistic map is strictly less than $-1$.
* Chapter 3: fixed cross-references that rendered as "Section Section", etc., and the reference to the definition of stationary point for differential equations.
* Chapter 3: fixed minor typos and typesetting issues.
* Example 4.2: added a proper title.
* Chapter 4, law of mass action example: fixed the signs in the actual rate of reaction.
* Section 4.3.1: the second example is from economics, not electrical engineering.
* Example 4.5 (COVID-19): fixed the caption of the 120-day SEIR figure and added the missing figure showing the SEIR model over a year.
* Chapter 4: fixed the typesetting of the derivatives in the SEIR model, and other minor typos.
* Chapter 5: the principle of dimensional homogeneity is an implication ($\implies$), not an equivalence.
* Chapter 5: harmonised the notation for the number of independent variables ($N$), dependent variables ($K$), independent dimensions ($D$) and nondimensional combinations ($P$) between the introduction, the Buckingham Pi Theorem and the scaling argument algorithm (the previous notation clashed with the dimension of mass $M$ and the mass $m$).
* Example 5.1: fixed typo in the dimensions of force (it should be $M L / T^2$), and completed an unfinished sentence.
* Example 5.2: fixed typesetting of $\ddot x(t)$ in the dimensions of $k$ and $c$.
* Example 5.3: $\sqrt{m/k}$ is proportional to (not equal to) the period of the undamped oscillations, and fixed a footnote that said the opposite of what was intended.
* Proof of Proposition 5.3: fixed typesetting of the exponents $n+1$.
* Algorithm 5.2: fixed the index of the last independent variable ($i_N$), and simplified the case with no nondimensional combinations ($d = \Delta d \cdot C$).
* Example 5.6 (Mars rover): added the missing viscosity term in the equation for the powers of $T$, and the parachute is hemispherical (not spherical).
* Chapter 5: fixed minor typos and typesetting issues.
* Chapter 6: systems of differential equations are now $n \times n$ (instead of $m \times m$), consistent with the rest of the chapter, and added a note explaining why the step in systems of difference equations is denoted by $k$.
* Chapter 6: points and vectors are now consistently written as column vectors (i.e. tuples are transposed).
* Section 6.4: fixed several typos in the eigenvalue/eigenvector examples (eigenvector superscripts, "eigenvalue" instead of "eigenvector"), in the general solution ($x^{(2)}$ uses $\lambda_2$), in the repeated eigenvalue derivation (spurious exponential factors), and in the phase portrait algorithm ("eigenvector" instead of "eigenvalue").
* Section 6.4.1: only non-zero multiples of an eigenvector are eigenvectors.
* Examples 6.8 and 6.9: fixed the figures, which did not correspond to the matrix and/or initial condition of the examples.
* Algorithm 6.1: rewrote the guideline for sketching solutions in the real distinct eigenvalues case, which was only correct for unstable nodes; it now covers nodes and saddles.
* Section 6.5: the stationary point for real eigenvalues of opposite sign is now called a *saddle point* (to avoid confusion with the saddle-node bifurcation).
* Section 6.5 (degenerate cases): two zero eigenvalues do not imply that $A$ is the zero matrix; added the case where $A$ has a single eigenvector.
* Section 6.6: stated the principle of linearised stability more precisely (it is inconclusive when some eigenvalues have zero real part).
* Example 6.11 (Lotka-Volterra): added a footnote explaining why the coexistence stationary point is a centre also for the nonlinear system, and removed the claim that the coexistence is stable before analysing it.
* Chapter 6: fixed bold typesetting of vectors in a few places, and minor typos.
* Chapters 2 and 6: the interval on which differential equations are posed is now consistently open, $(\alpha,\beta)$.
* All chapters: minor typesetting and spelling consistency fixes (e.g. $\log$, $e$, COVID-19, Buckingham Pi Theorem).

## 2026-10-26

* Chapter 2: fixed minor typo in the saddle-node bifurcation definition.
* Figure 2.9: fixed some typos in the labels of the axes and the stationary points.

## 2026-10-19

* Chapter 2: in the fishery example, added a remark about the stability of the stationary point in the case $c = r$ and added the name of the bifurcation.
* Chapter 2: small rewording of the title of section 2.8. 

## 2026-10-05

* Chapter 1: fix typo in the definition of vector (in this module vectors are column vectors by definition).
* Chapter 2: fix typo in the coffee cup example (it said the rather redundant statement $T_0 = T_0$).
* Chapter 2: added proof environment to the proof of Lemma 2.3.

## 2026-09-28 (first release)

Initial version of the lecture notes for the academic year 2025-2026, with some major changes from the previous version of the notes. Note that no major changes have been made on the content of the notes, and students who have already studied the previous version of the notes should be able to follow the new version without any problems. The main changes are:

* The notes have been restructured to follow a more logical order: the modelling and dimensional analysis have been moved after the differential and difference equations, which should make it easier to follow.
* The two former chapters on differential equations have been merged into one chapter (current Chapter 2).
* The chapter on mathematical modelling and dimensional analysis has been split into two chapters (current Chapters 4 and 5).
* The non-dimensionalisation methods have been changed to make them more accessible. The old methods will still be accepted in exams and assignments.
* Examples have been changed to be more relevant to the course and the students and their previous knowledge. They have also been adapted to account for the fact that dimensional analysis is not covered until Chapter 5.
