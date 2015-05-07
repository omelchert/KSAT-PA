"""main_kSat_probAlg.py

all-in-one file containing function definitions for a simple local 
search algorithm to solve random k-SAT and constraint satisfaction 
problems as outlined in

   "A Probabilistic Algorithm for k-SAT and Constraint Satisfaction 
   Problems", U. Schoening,
   40th Annual Symposium on Foundations of Computer Science 1999,
   http://dx.doi.org/10.1109/SFFCS.1999.814612

AUTHOR : O. Melchert
DATE   : 05/06/2015
"""
import sys
import random


def constructCNF(nC,nL,nV):
        """construnct random clause in conjunctive normal form 

        \param[in] nC Number of clauses in CNF
        \param[in] nL Number of literals in clause
        \param[in] nV Number of variables
        \param[out] CNF Conjunctive normal form
        """
        return [tuple(random.choice([-vId,vId])\
                  for vId in random.sample(range(1,nV+1),nL))\
                     for ci in range(nC)]


def checkCfg(cnf,cfg):
        """check if configuration satisfies given CNF

        \param[in] cnf Conjunctive normal form
        \param[in] cfg Configuration of binary variables
        \param[out] sat True if cfg satisfies cnf, else False
        """
        sat = True
        # for each individual clause 
        for ci in cnf:
                # compute the numer of satisfied literals 
                nTrue = 0
                for li in ci:
                   if (li>0) == cfg[abs(li)-1]:
                           nTrue += 1
                # if no such literal exists, CNF cannot be sat
                if nTrue == 0:
                        sat = False
                        break
        return sat


def schoening_kSat(cnf,cfg,nTries):
        """simple probabilistic algorithm to solve k-SAT 

        simple local search algorithm to solve random k-SAT and 
        constraint satisfaction problems as outlined in

           "A Probabilistic Algorithm for k-SAT and Constraint 
           Satisfaction Problems",
           U. Schoening,
           40th Annual Symposium on Foundations of Computer Science,
           http://dx.doi.org/10.1109/SFFCS.1999.814612

        NOTES:
        -# for any satisfyable k-CNF formula with N variables
           the algorithm has to be repeated only t times, where
           t is within a polynomial factor of (2(1-1/k))^N 
        -# best complexity bound for 3-Sat known up to 1999

        \param[in] cnf Conjunctive normal form
        \param[in] cfg Configuration of variables
        \param[in] nTries number of proposed cfg updates
        """
        # convenient abbrev to check if given clause is not satisfied
        notSat = lambda ci: checkCfg([ci],cfg)==False

        while nTries:

                # if cnf-formula satisfied by current assignment:
                # stop and return configuration
                if checkCfg(cnf,cfg):
                        break

                # yield variable-id of random literal in random 
                # non-satisfied clause
                vId = abs( 
                           # pick random literal
                           random.choice(
                             # pick random not satisfied clause
                             random.choice(
                               # list of not satisfied clauses
                               [ci for ci in cnf if notSat(ci)]
                             )
                           )
                         ) - 1 
                
                # flip corresponding value in current assignment
                cfg[vId] = 1 - cfg[vId]

                nTries -= 1

        return nTries,cfg


def dumpResult_DIMACS(cnf,cfg):
        """list results in DIMACS format

        NOTE:
        -# for details, see 
           http://www.satcompetition.org/2009/format-benchmarks2009.html

        \param[in] cnf Conjunctive normal form
        \param[in] cfg Configuration of variables
        """
        print "c cnf (num variables) (num clauses) (num literals)"
        print "p cnf %d %d"%(len(cfg),len(cnf))
        for ci in cnf:
          for li in ci:
                  print "%3d"%(li),
          print 0
        print "c (satisfied: 0/1) (cfg: v_1 ... v_N)" 
        print "c %d %s"%(int(checkCfg(cnf,cfg)), "".join([str(vi) for vi in cfg]) )


def main_kSat():

        nV = 10         # number of variables
        nC = 43         # number of clauses in CNF
        k  = 3          # number of literals per clause (k-Sat)

        random.seed(random.randint(0,sys.maxint))

        # generate random CNF 
        myCnf = constructCNF(nC,k,nV)

        # assign initial random binary variables
        myCfg = [random.choice([0,1]) for vi in range(nV)]

        # run simple local search algorithm
        nTriesLeft,myCfg =  schoening_kSat(myCnf,myCfg, 3*nV)

        # list results to standard outstream
        dumpResult_DIMACS(myCnf,myCfg)


main_kSat()
# EOF: main_kSat_probAlg.py
