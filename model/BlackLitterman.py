# encoding: utf-8
# Black-Litterman example code for python (hl.py)
# Copyright (c) Jay Walters, blacklitterman.org, 2012.
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided
# that the following conditions are met:
#
# Redistributions of source code must retain the above
# copyright notice, this list of conditions and the following
# disclaimer.
#
# Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials
# provided with the distribution.
#
# Neither the name of blacklitterman.org nor the names of its
# contributors may be used to endorse or promote products
# derived from this software without specific prior written
# permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.
#
# This program uses the examples from the paper "The Intuition
# Behind Black-Litterman Model  Portfolios", by He and Litterman,
# 1999.  You can find a copy of this  paper at the following url.
#     http://papers.ssrn.com/sol3/papers.cfm?abstract_id=334304
#
# For more details on the Black-Litterman model you can also view
# "The BlackLitterman Model: A Detailed Exploration", by this author
# at the following url.
#     http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1314585
#

import numpy as np
from scipy import linalg


# blacklitterman
#   This function performs the Black-Litterman blending of the prior
#   and the views into a new posterior estimate of the returns as
#   described in the paper by He and Litterman.
# Inputs
#   delta  - Risk tolerance from the equilibrium portfolio
#   weq    - Weights of the assets in the equilibrium portfolio
#   sigma  - Prior covariance matrix
#   tau    - Coefficiet of uncertainty in the prior estimate of the mean (pi)
#   P      - Pick matrix for the view(s)
#   Q      - Vector of view returns
#   Omega  - Matrix of variance of the views (diagonal)
# Outputs
#   Er     - Posterior estimate of the mean returns
#   w      - Unconstrained weights computed given the Posterior estimates
#            of the mean and covariance of returns.
#   lambda - A measure of the impact of each view on the posterior estimates.
#
def blacklitterman(delta, weq, sigma, tau, P, Q, Omega):
    # Reverse optimize and back out the equilibrium returns
    # This is formula (12) page 6.
    pi = weq.dot(sigma * delta)
    print(pi)
    # We use tau * sigma many places so just compute it once
    ts = tau * sigma
    # Compute posterior estimate of the mean
    # This is a simplified version of formula (8) on page 4.
    middle = linalg.inv(np.dot(np.dot(P, ts), P.T) + Omega)
    print(middle)
    print(Q - np.expand_dims(np.dot(P, pi.T), axis=1))
    er = np.expand_dims(pi, axis=0).T + np.dot(np.dot(np.dot(ts, P.T), middle),
                                               (Q - np.expand_dims(np.dot(P, pi.T), axis=1)))
    # Compute posterior estimate of the uncertainty in the mean
    # This is a simplified and combined version of formulas (9) and (15)
    posteriorSigma = sigma + ts - ts.dot(P.T).dot(middle).dot(P).dot(ts)
    print(posteriorSigma)
    # Compute posterior weights based on uncertainty in mean
    w = er.T.dot(linalg.inv(delta * posteriorSigma)).T
    # Compute lambda value
    # We solve for lambda from formula (17) page 7, rather than formula (18)
    # just because it is less to type, and we've already computed w*.
    lmbda = np.dot(linalg.pinv(P).T, (w.T * (1 + tau) - weq).T)
    return [er, w, lmbda]


# Function to display the results of a black-litterman shrinkage
# Inputs
#   title	- Displayed at top of output
#   assets	- List of assets
#   res		- List of results structures from the bl function
#
def display(title, assets, res):
    er = res[0]
    w = res[1]
    lmbda = res[2]
    print('\n' + title)
    line = 'Country\t\t'
    for p in range(len(P)):
        line = line + 'P' + str(p) + '\t'
    line = line + 'mu\tw*'
    print(line)

    i = 0;
    for x in assets:
        line = '{0}\t'.format(x)
        for j in range(len(P.T[i])):
            line = line + '{0:.1f}\t'.format(100 * P.T[i][j])

        line = line + '{0:.3f}\t{1:.3f}'.format(100 * er[i][0], 100 * w[i][0])
        print(line)
        i = i + 1

    line = 'q\t\t'
    i = 0
    for q in Q:
        line = line + '{0:.2f}\t'.format(100 * q[0])
        i = i + 1
    print(line)

    line = 'omega/tau\t'
    i = 0
    for o in Omega:
        line = line + '{0:.5f}\t'.format(o[i] / tau)
        i = i + 1
    print(line)

    line = 'lambda\t\t'
    i = 0
    for l in lmbda:
        line = line + '{0:.5f}\t'.format(l[0])
        i = i + 1
    print(line)


# Take the values from He & Litterman, 1999.
weq = np.array([0.016, 0.022, 0.052, 0.055, 0.116, 0.124, 0.615])
C = np.array([[1.000, 0.488, 0.478, 0.515, 0.439, 0.512, 0.491],
              [0.488, 1.000, 0.664, 0.655, 0.310, 0.608, 0.779],
              [0.478, 0.664, 1.000, 0.861, 0.355, 0.783, 0.668],
              [0.515, 0.655, 0.861, 1.000, 0.354, 0.777, 0.653],
              [0.439, 0.310, 0.355, 0.354, 1.000, 0.405, 0.306],
              [0.512, 0.608, 0.783, 0.777, 0.405, 1.000, 0.652],
              [0.491, 0.779, 0.668, 0.653, 0.306, 0.652, 1.000]])
Sigma = np.array([0.160, 0.203, 0.248, 0.271, 0.210, 0.200, 0.187])
refPi = np.array([0.039, 0.069, 0.084, 0.090, 0.043, 0.068, 0.076])
assets = {'Australia', 'Canada   ', 'France   ', 'Germany  ', 'Japan    ', 'UK       ', 'USA      '}

# Equilibrium covariance matrix
V = np.multiply(np.outer(Sigma, Sigma), C)
# print(V)

# Risk aversion of the market
delta = 2.5

# Coefficient of uncertainty in the prior estimate of the mean
# from footnote (8) on page 11
tau = 0.05
tauV = tau * V

# Define view 1
# Germany will outperform the other European markets by 5%
# Market cap weight the P matrix
# Results should match Table 4, Page 21
P1 = np.array([0, 0, -.295, 1.00, 0, -.705, 0])
Q1 = np.array([0.05])
P = np.array([P1])
Q = np.array([Q1]);
Omega = np.dot(np.dot(P, tauV), P.T) * np.eye(Q.shape[0])
res = blacklitterman(delta, weq, V, tau, P, Q, Omega)
display('View 1', assets, res)

# Define view 2
# Canadian Equities will outperform US equities by 3%
# Market cap weight the P matrix
# Results should match Table 5, Page 22
P2 = np.array([0, 1.0, 0, 0, 0, 0, -1.0])
Q2 = np.array([0.03])
P = np.array([P1, P2])
Q = np.array([Q1, Q2]);
Omega = np.dot(np.dot(P, tauV), P.T) * np.eye(Q.shape[0])
res = blacklitterman(delta, weq, V, tau, P, Q, Omega)
display('View 1 + 2', assets, res)
