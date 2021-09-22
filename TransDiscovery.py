#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Donghui
"""
from script import TransDiscovery_step1
from script import TransDiscovery_step2
from timeit import default_timer as timer

def run(args):
    start_time = timer()
    TransDiscovery_step1.run(args)
    step_one_time = timer()
    print('Finished merging association network with BioTransformer knowledgebase in {:.3f} seconds').format(step_one_time-timer)
    TransDiscovery_step2.run(args)
    finish_time = timer()
    print('Finished running TransDiscovery in {:.3f} seconds').format(finish_time-timer)



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
    parser.add_argument("--Association_BioTransformer_merged_result",
                        help="The path to the input file contain merged Association network and BioTransformer result",
                        default="/tmp/step_1.txt")
    
    parser.add_argument("--Molecular_network_edge_path",
                        help="The path to the molecular netowrk edge info",
                        default=None)

    parser.add_argument("--Molecular_network_node_path",
                        help="The path to the molecular netowrk node info",
                        default=None)
    parser.add_argument("--output_path",
                        help="The path to the output file",
                        default=None)

    args = parser.parse_args()
    
    run(args)


 
