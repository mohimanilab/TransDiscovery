#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Donghui
"""

import numpy
import pandas
import os
pandas.options.mode.chained_assignment = None  # default='warn'
def run(args):
    print("loading BioTransformer_result")
    folder_path = args.BioTransformer_result_path
    file_list = os.listdir(folder_path)
    for file in file_list:
        file_path = folder_path+file
        biotrans_info = pandas.read_table(file_path,sep = ",")
        biotrans_info["origin_molecule"] = file.split(".")[0]
        if file == file_list[0]:
            all_biotransformer = biotrans_info
        else:
            all_biotransformer = all_biotransformer.append(biotrans_info)
    association_path = args.Association_result_path
    association_info = pandas.read_table(association_path,sep = "\t")

    result = association_info

    print("Start Matching")

    total_col = result.shape[0]
    tolerance = args.tolerance
    substrate_list = []
    enzyme_list = []
    product_list = []
    substrate_direction_list = []
    product_direction_list = []
    substrate_correlation_list = []
    product_correlation_list = []
    p_value_substrate_list = []
    p_value_product_list = []
    substrate_name_list = []
    product_name_list = []
    reaction_name_list = []
    enzyme_ID_list = []
    for s in range(total_col):
        data = result.iloc[s]
        if type(data["mgx_name"]) is float:
            continue
        mass = float(data["mbx_name"].split(" ")[0])-1.007
        mgx_name = data["mgx_name"]
        candidate_product = all_biotransformer[(mass-tolerance<all_biotransformer["Major Isotope Mass"]) & (all_biotransformer["Major Isotope Mass"]<mass+tolerance)]
        if candidate_product.shape[0]==0:
            continue
        all_association = result[(result["mgx_name"]==mgx_name)]
        all_association["mass"] = all_association.mbx_name.str.split(" ",expand = True,)[0].astype(float)-1.007

        for item in range(candidate_product.shape[0]):
            data_reaction = candidate_product.iloc[item]
            target_mass = data_reaction["Precursor Major Isotope Mass"]
            satisfied_match = all_association[(target_mass-tolerance<all_association["mass"]) & (all_association["mass"]<target_mass+tolerance)]
            for k in range(satisfied_match.shape[0]):
                substrate_data = satisfied_match.iloc[k]
                if numpy.abs(substrate_data["correlation"])<args.substrate_rho_value_cutoff:
                    continue
                if numpy.abs(data["correlation"])<args.product_rho_value_cutoff:
                    continue
                if args.neg_sub_pos_prod_only:
                    if data["correlation"]<0:
                        continue
                    if substrate_data["correlation"]>0:
                        continue
                substrate_list.append(substrate_data["mbx_name"])
                enzyme_list.append(substrate_data["mgx_name"])
                product_list.append(data["mbx_name"])
                substrate_direction_list.append(substrate_data["direction"])
                product_direction_list.append(data["direction"])
                substrate_correlation_list.append(substrate_data["correlation"])
                product_correlation_list.append(data["correlation"])
                p_value_substrate_list.append(substrate_data["p_value"])
                p_value_product_list.append(data["p_value"])
                substrate_name_list.append(data_reaction["origin_molecule"])
                product_name_list.append(data_reaction["SMILES"])
                reaction_name_list.append(data_reaction["Reaction"])
                enzyme_ID_list.append(data_reaction["Enzyme(s)"])
              
            
            
    result_df = pandas.DataFrame(
                {'substrate': substrate_list,
                 'enzyme': enzyme_list,
                 'product': product_list,
                 'substrate_direction': substrate_direction_list,        
                 'product_direction': product_direction_list,
                 'substrate_correlation':substrate_correlation_list,
                 'product_correlation' : product_correlation_list,
                 'p_value_substrate': p_value_substrate_list,
                 'p_value_product': p_value_product_list,
                 'substrate_name' : substrate_name_list,
                 'product_name': product_name_list,
                 'reaction_name': reaction_name_list,
                 'enzyme_ID': enzyme_ID_list

                 })
    result_df = result_df[[ 'substrate', 'enzyme','product','substrate_direction', 'product_direction','substrate_correlation','product_correlation', 'p_value_substrate', 'p_value_product','substrate_name','product_name','reaction_name','enzyme_ID']]
    result_df.to_csv(args.output_path,sep = "\t",index = False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Build results.')
    parser.add_argument("--BioTransformer_result_path",
                        help="The path to the BioTransformer result folder",
                        default=None)
    
    parser.add_argument("--Association_result_path",
                        help="The path to the Association network result file",
                        default=None)

    parser.add_argument("--tolerance",
                        help="The mass tolerance when matching molecular features",
                        default=0.02)
    parser.add_argument("--substrate_rho_value_cutoff",
                        help="The rho cutoff for valid association between substrate and enzyme",
                        default=0)
    parser.add_argument("--product_rho_value_cutoff",
                        help="The rho cutoff for valid association between product and enzyme",
                        default=0)
    parser.add_argument("--neg_sub_pos_prod_only",
                        help="True if only consider negative correlation for substrate and positive correlation for product",
                        default=False)

    parser.add_argument("--output_path",
                        help="The path to the output file",
                        default=None)

    args = parser.parse_args()
    
    run(args)


            
