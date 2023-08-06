import os
import yaml
import argparse

from evalAIRR.util.input import read_encoded_csv
from evalAIRR.util.corr import export_corr_heatmap
from evalAIRR.util.pca import export_pca_2d_comparison
from evalAIRR.util.univar import export_ks_test
from evalAIRR.util.univar import export_distr_histogram, export_obs_distr_histogram
from evalAIRR.util.univar import export_distr_boxplot, export_obs_distr_boxplot
from evalAIRR.util.univar import export_distr_violinplot, export_obs_distr_violinplot
from evalAIRR.util.univar import export_distr_densityplot, export_obs_distr_densityplot
from evalAIRR.util.univar import export_avg_var_scatter_plot
from evalAIRR.util.univar import export_distance, export_obs_distance
from evalAIRR.util.univar import export_statistics, export_obs_statistics
from evalAIRR.util.copula import export_copula_2d_scatter_plot, export_copula_3d_scatter_plot
from evalAIRR.util.report import export_report

#######################
### PARSE ARGUMENTS ###
#######################

parser = argparse.ArgumentParser(prog='evalairr')
parser.add_argument('-i', '--config', help='path to YAML confuguration file', required=True)

def run():

    #################
    ### READ YAML ###
    #################

    YAML_FILE = parser.parse_args().config
    CONFIG = []
    with open(YAML_FILE, 'r') as stream:
        try:
            CONFIG = (yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

    REPORTS = CONFIG['reports']

    try:
        OUTPUT = CONFIG['output']['path']
    except: 
        OUTPUT = './output/report.html'
        
    #####################
    ### READ DATASETS ###
    #####################

    features_R, data_R = read_encoded_csv(CONFIG['datasets']['real']['path'])
    features_S, data_S = read_encoded_csv(CONFIG['datasets']['sim']['path'])

    ##########################################
    ### CREATE OUTPUT AND TEMP DIRECTORIES ###
    ##########################################

    if not os.path.exists('./output'):
        os.makedirs('./output')
    if not os.path.exists('./output/temp_figures'):
        os.makedirs('./output/temp_figures')
    if not os.path.exists('./output/temp_results'):
        os.makedirs('./output/temp_results')
    if not os.path.exists('./output/temp_statistics'):
        os.makedirs('./output/temp_statistics')

    #############################
    ### FEATURE BASED REPORTS ###
    #############################

    if ('feature_based' in REPORTS):
        reports_f = REPORTS['feature_based']
        for report in reports_f:
            features = reports_f[report]['features']
            report_types = reports_f[report]['report_types']
            for feature in features:

                # KOLMOGOROV-SMIRNOV TEST REPORT
                if 'ks' in report_types:
                    export_ks_test(feature, data_R, data_S, features_R, features_S)

                # DISTRIBUTION HISTOGRAM REPORT
                if 'distr_histogram' in report_types:
                    export_distr_histogram(feature, data_R, data_S, features_R, features_S)

                # DISTRIBUTION BOX PLOT REPORT
                if 'distr_boxplot' in report_types:
                    export_distr_boxplot(feature, data_R, data_S, features_R, features_S)

                # DISTRIBUTION VIOLIN PLOT REPORT
                if 'distr_violinplot' in report_types:
                    export_distr_violinplot(feature, data_R, data_S, features_R, features_S)

                # DISTRIBUTION DENSITY PLOT REPORT
                if 'distr_densityplot' in report_types:
                    export_distr_densityplot(feature, data_R, data_S, features_R, features_S)

                # EUCLIDEAN DISTANCE REPORT
                if 'distance' in report_types:
                    export_distance(feature, data_R, data_S, features_R, features_S)

                # STATISTICS REPORT
                if 'statistics' in report_types:
                    export_statistics(feature, data_R, data_S, features_R, features_S)

    #################################
    ### OBSERVATION BASED REPORTS ###
    #################################

    if ('observation_based' in REPORTS):
        reports_o = REPORTS['observation_based']
        for report in reports_o:
            observations = reports_o[report]['observations']
            report_types = reports_o[report]['report_types']
            for observation_index in observations:

                # OBSERVATION DISTRIBUTION HISTOGRAM REPORT
                if 'observation_distr_histogram' in report_types:
                    export_obs_distr_histogram(observation_index, data_R, data_S)

                # OBSERVATION DISTRIBUTION BOX PLOT REPORT
                if 'observation_distr_boxplot' in report_types:
                    export_obs_distr_boxplot(observation_index, data_R, data_S)

                # OBSERVATION DISTRIBUTION VIOLIN PLOT REPORT
                if 'observation_distr_violinplot' in report_types:
                    export_obs_distr_violinplot(observation_index, data_R, data_S)

                # OBSERVATION DISTRIBUTION DENSITY PLOT REPORT
                if 'observation_distr_densityplot' in report_types:
                    export_obs_distr_densityplot(observation_index, data_R, data_S)

                # OBSERVATION EUCLIDEAN DISTANCE REPORT
                if 'observation_distance' in report_types:
                    export_obs_distance(observation_index, data_R, data_S)

                # OBSERVATION STATISTICS REPORT
                if 'observation_statistics' in report_types:
                    export_obs_statistics(observation_index, data_R, data_S)

    #######################
    ### GENERAL REPORTS ###
    #######################

    if ('general' in REPORTS):
        reports_g = REPORTS['general']

        # CORRELATION MATRIX REPORT
        if ('corr' in reports_g):
            percent_features = reports_g['corr']['percent_features']
            export_corr_heatmap(data_R, data_S, len(features_R), len(features_S), percent_features)

        # PCA 2D REPORT
        if ('pca_2d' in reports_g):
            export_pca_2d_comparison(data_R, data_S)

        # FEATURE AVERAGE VALUE VS VARIANCE REPORT
        if ('feature_average_vs_variance' in reports_g):
            export_avg_var_scatter_plot(data_R, data_S, axis=0)

        # OBSERVATION AVERAGE VALUE VS VARIANCE REPORT
        if ('observation_average_vs_variance' in reports_g):
            export_avg_var_scatter_plot(data_R, data_S, axis=1)

        # COPULA 2D REPORT
        if ('copula_2d' in reports_g):
            copula_reports = reports_g['copula_2d']
            for copula_report in copula_reports:
                if len(copula_reports[copula_report]) > 2:
                    print(f'[WARNING] More than 2 features provided in \'{copula_report}\'! Using only the first 2 for calculations.')
                elif len(copula_reports[copula_report]) < 2:
                    print(f'[ERROR] 2D copula scatter plot report \'{copula_report}\' requires 2 features!')
                    continue
                export_copula_2d_scatter_plot(copula_reports[copula_report][0], copula_reports[copula_report][1], data_R, data_S, features_R, features_S)

        # COPULA 3D REPORT
        if ('copula_3d' in reports_g):
            copula_reports = reports_g['copula_3d']
            for copula_report in copula_reports:
                if len(copula_reports[copula_report]) > 3:
                    print(f'[WARNING] More than 3 features provided in \'{copula_report}\'! Using only the first 3 for calculations.')
                elif len(copula_reports[copula_report]) < 3:
                    print(f'[ERROR] 3D copula scatter plot report \'{copula_report}\' requires 3 features!')
                    continue
                export_copula_3d_scatter_plot(copula_reports[copula_report][0], copula_reports[copula_report][1], copula_reports[copula_report][2], data_R, data_S, features_R, features_S)

    ##########################
    ### EXPORT HTML REPORT ###
    ##########################

    export_report(OUTPUT)