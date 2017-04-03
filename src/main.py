'''
Created on Mar 29, 2017

@author: meike.zehlike
'''
import os
from read_write_rankings.read_and_write_rankings import writePickleToDisk
from ranker.create_FAIR_ranking import createFairRanking
from ranker.create_feldman_ranking import createFeldmanRanking
from utils_and_constants.constants import ESSENTIALLY_ZERO
from dataset_creator.xing_profiles_reader import XingProfilesReader
from dataset_creator.german_credit_data import createGermanCreditDataSet
from dataset_creator.compas_data import createCompasGenderDataSet, createCompasRaceDataSet
from dataset_creator.sat_data import Creator


def main():
    createRankingsAndWriteToDisk()


def createRankingsAndWriteToDisk():
    createSATData(1500)
    createCOMPASData(1000)
    createGermanCreditData(100)
    createXingData(40)


def createXingData(k):
    pairsOfPAndAlpha = [(0.1, 0.1),  # no real results, skip in evaluation
                        (0.2, 0.1),  # no real results, skip in evaluation
                        (0.3, 0.1),  # no real results, skip in evaluation
                        (0.4, 0.1),  # no real results, skip in evaluation
                        (0.5, 0.0168),
                        (0.6, 0.0321),
                        (0.7, 0.0293),
                        (0.8, 0.0328),
                        (0.9, 0.0375)]

    xingReader = XingProfilesReader('../raw_data/Xing/*.json')  # glob gets abs/rel paths matching the regex
    for queryString, candidates in xingReader.entireDataSet.iterrows():
        dumpRankingsToDisk(candidates['protected'], candidates['nonProtected'], k, queryString,
                           "../results/rankingDumps/Xing" + '/' + queryString + '/', pairsOfPAndAlpha)
        writePickleToDisk(candidates['originalOrdering'], os.getcwd() + '/../results/rankingDumps/Xing/'
                          + '/' + queryString + '/' + 'OriginalOrdering.pickle')


def createGermanCreditData(k):

    pairsOfPAndAlpha = [(0.1, 0.1),  # no real results, skip in evaluation
                        (0.2, 0.1),  # no real results, skip in evaluation
                        (0.3, 0.0220),
                        (0.4, 0.0222),
                        (0.5, 0.0207),
                        (0.6, 0.0209),
                        (0.7, 0.0216),
                        (0.8, 0.0216),
                        (0.9, 0.0256)]

    protectedGermanCreditGender, nonProtectedGermanCreditGender = createGermanCreditDataSet(
        "../raw_data/GermanCredit/GermanCredit_sex.csv", "DurationMonth", "CreditAmount",
        "score", "sex", protectedAttribute=["female"])
    dumpRankingsToDisk(protectedGermanCreditGender, nonProtectedGermanCreditGender, k,
                       "GermanCreditGender", "../results/rankingDumps/German Credit/Gender",
                       pairsOfPAndAlpha)

    protectedGermanCreditAge25, nonProtectedGermanCreditAge25 = createGermanCreditDataSet(
        "../raw_data/GermanCredit/GermanCredit_age25.csv", "DurationMonth", "CreditAmount",
        "score", "age25", protectedAttribute=["younger25"])
    dumpRankingsToDisk(protectedGermanCreditAge25, nonProtectedGermanCreditAge25, k,
                       "GermanCreditAge25", "../results/rankingDumps/German Credit/Age25",
                       pairsOfPAndAlpha)

    protectedGermanCreditAge35, nonProtectedGermanCreditAge35 = createGermanCreditDataSet(
        "../raw_data/GermanCredit/GermanCredit_age35.csv", "DurationMonth", "CreditAmount",
        "score", "age35", protectedAttribute=["younger35"])
    dumpRankingsToDisk(protectedGermanCreditAge35, nonProtectedGermanCreditAge35, k,
                       "GermanCreditAge35", "../results/rankingDumps/German Credit/Age35",
                       pairsOfPAndAlpha)

def createCOMPASData(k):

    pairsOfPAndAlpha = [(0.1, 0.0140),
                        (0.2, 0.0115),
                        (0.3, 0.0103),
                        (0.4, 0.0099),
                        (0.5, 0.0096),
                        (0.6, 0.0093),
                        (0.7, 0.0094),
                        (0.8, 0.0095),
                        (0.9, 0.0100)]

    protectedCompasRace, nonProtectedCompasRace = createCompasRaceDataSet(
       "../raw_data/COMPAS/ProPublica_race.csv", "race", "Violence_rawscore", "Recidivism_rawscore",
       "priors_count")
    dumpRankingsToDisk(protectedCompasRace, nonProtectedCompasRace, k, "CompasRace",
                       "../results/rankingDumps/Compas/Race", pairsOfPAndAlpha)

    protectedCompasGender, nonProtectedCompasGender = createCompasGenderDataSet(
       "../raw_data/COMPAS/ProPublica_sex.csv", "sex", "Violence_rawscore", "Recidivism_rawscore",
       "priors_count")
    dumpRankingsToDisk(protectedCompasGender, nonProtectedCompasGender, k, "CompasGender",
                      "../results/rankingDumps/Compas/Gender", pairsOfPAndAlpha)


def createSATData(k):

    SATFile = '../raw_data/SAT/sat_data.pdf'

    pairsOfPAndAlpha = [(0.1, 0.0122),
                        (0.2, 0.0101),
                        (0.3, 0.0092),
                        (0.4, 0.0088),
                        (0.5, 0.0084),
                        (0.6, 0.0085),
                        (0.7, 0.0084),
                        (0.8, 0.0084),
                        (0.9, 0.0096)]

    satSetCreator = Creator(SATFile)
    protectedSAT, nonProtectedSAT = satSetCreator.createSetOfCandidates()
    dumpRankingsToDisk(protectedSAT, nonProtectedSAT, k, "SAT", "../results/rankingDumps/SAT", pairsOfPAndAlpha)


def dumpRankingsToDisk(protected, nonProtected, k, dataSetName, directory, pairsOfPAndAlpha):
    """
    creates all rankings we need for one experimental data set and writes them to disk to be used later

    @param protected:        list of protected candidates, assumed to satisfy in-group monotonicty
    @param nonProtected:     list of non-protected candidates, assumed to satisfy in-group monotonicty
    @param k:                length of the rankings we want to create
    @param dataSetName:      determines which data set is used in this experiment
    @param directory:        directory in which to store the rankings
    @param pairsOfPAndAlpha: contains the mapping of a certain alpha correction to be used for a certain p

    The experimental setting is as follows: for a given data set of protected and non-
    protected candidates we create the following rankings:
    * a colorblind ranking,
    * a ranking as in Feldman et al
    * ten rankings using our FairRankingCreator, with p varying from 0.1, 0.2 to 0.9, whereas alpha
      stays 0.1

    """
    print("====================================================================")
    print("create rankings of {0}".format(dataSetName))

    if not os.path.exists(os.getcwd() + '/' + directory + '/'):
        os.makedirs(os.getcwd() + '/' + directory + '/')

    print("colorblind ranking", end='', flush=True)
    colorblindRanking, colorblindNotSelected = createFairRanking(k, protected, nonProtected, ESSENTIALLY_ZERO, 0.1)
    print(" [Done]")

    print("feldman ranking", end='', flush=True)
    feldmanRanking, feldmanNotSelected = createFeldmanRanking(protected, nonProtected, k)
    print(" [Done]")

    print("fair rankings", end='', flush=True)
    pair01 = [item for item in pairsOfPAndAlpha if item[0] == 0.1][0]
    fairRanking01, fair01NotSelected = createFairRanking(k, protected, nonProtected, pair01[0], pair01[1])
    pair02 = [item for item in pairsOfPAndAlpha if item[0] == 0.2][0]
    fairRanking02, fair02NotSelected = createFairRanking(k, protected, nonProtected, pair02[0], pair02[1])
    pair03 = [item for item in pairsOfPAndAlpha if item[0] == 0.3][0]
    fairRanking03, fair03NotSelected = createFairRanking(k, protected, nonProtected, pair03[0], pair03[1])
    pair04 = [item for item in pairsOfPAndAlpha if item[0] == 0.4][0]
    fairRanking04, fair04NotSelected = createFairRanking(k, protected, nonProtected, pair04[0], pair04[1])
    pair05 = [item for item in pairsOfPAndAlpha if item[0] == 0.5][0]
    fairRanking05, fair05NotSelected = createFairRanking(k, protected, nonProtected, pair05[0], pair05[1])
    pair06 = [item for item in pairsOfPAndAlpha if item[0] == 0.6][0]
    fairRanking06, fair06NotSelected = createFairRanking(k, protected, nonProtected, pair06[0], pair06[1])
    pair07 = [item for item in pairsOfPAndAlpha if item[0] == 0.7][0]
    fairRanking07, fair07NotSelected = createFairRanking(k, protected, nonProtected, pair07[0], pair07[1])
    pair08 = [item for item in pairsOfPAndAlpha if item[0] == 0.8][0]
    fairRanking08, fair08NotSelected = createFairRanking(k, protected, nonProtected, pair08[0], pair08[1])
    pair09 = [item for item in pairsOfPAndAlpha if item[0] == 0.9][0]
    fairRanking09, fair09NotSelected = createFairRanking(k, protected, nonProtected, pair09[0], pair09[1])
    print(" [Done]")

    print("Write rankings to disk", end='', flush=True)
    writePickleToDisk(colorblindRanking, os.getcwd() + '/' + directory + '/' + dataSetName + 'ColorblindRanking.pickle')
    writePickleToDisk(colorblindNotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'ColorblindRankingNotSelected.pickle')
    writePickleToDisk(feldmanRanking, os.getcwd() + '/' + directory + '/' + dataSetName + 'FeldmanRanking.pickle')
    writePickleToDisk(feldmanNotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FeldmanRankingNotSelected.pickle')
    writePickleToDisk(fairRanking01, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking01PercentProtected.pickle')
    writePickleToDisk(fair01NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking01NotSelected.pickle')
    writePickleToDisk(fairRanking02, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking02PercentProtected.pickle')
    writePickleToDisk(fair02NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking02NotSelected.pickle')
    writePickleToDisk(fairRanking03, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking03PercentProtected.pickle')
    writePickleToDisk(fair03NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking03NotSelected.pickle')
    writePickleToDisk(fairRanking04, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking04PercentProtected.pickle')
    writePickleToDisk(fair04NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking04NotSelected.pickle')
    writePickleToDisk(fairRanking05, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking05PercentProtected.pickle')
    writePickleToDisk(fair05NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking05NotSelected.pickle')
    writePickleToDisk(fairRanking06, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking06PercentProtected.pickle')
    writePickleToDisk(fair06NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking06NotSelected.pickle')
    writePickleToDisk(fairRanking07, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking07PercentProtected.pickle')
    writePickleToDisk(fair07NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking07NotSelected.pickle')
    writePickleToDisk(fairRanking08, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking08PercentProtected.pickle')
    writePickleToDisk(fair08NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking08NotSelected.pickle')
    writePickleToDisk(fairRanking09, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking09PercentProtected.pickle')
    writePickleToDisk(fair09NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking09NotSelected.pickle')
    print(" [Done]")



if __name__ == '__main__':
    main()
