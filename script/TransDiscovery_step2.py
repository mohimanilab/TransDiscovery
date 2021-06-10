#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Donghui
"""
import pandas
import numpy as np
import networkx as nx
def run(args):
    biotransformer_result = args.Association_BioTransformer_merged_result
    network_pair = args.Molecular_network_edge
    network_node_info = args.Molecular_network_node
    biotransformer_result_info = pandas.read_table(biotransformer_result,sep = "\t")
    biotransformer_result_info["substrate_mass"] = biotransformer_result_info["substrate"].str.split(" ", n = 1, expand = True)[0].astype("float")
    biotransformer_result_info["product_mass"] = biotransformer_result_info["product"].str.split(" ", n = 1, expand = True)[0].astype("float")
    network_node_info_result = pandas.read_table(network_node_info,sep = "\t")
    biotransformer_result_info["molecular_path_2"] = "NA"
    biotransformer_result_info["molecular_path_3"] = "NA"
    biotransformer_result_info["molecular_path_4"] = "NA"
    print("Creating molecular network")
    result = biotransformer_result_info
    G = nx.Graph()
    file = open(network_pair,"r")
    node_list = []
    for lines in file:
        next(file)
        nodes = lines.split()[0:2]
        for item in nodes:
            item = int(item)
            if item not in node_list:
                G.add_node(item)
                node_list.append(item)
        G.add_edge(int(nodes[0]), int(nodes[1]))
                

    n = G.number_of_nodes()
    m =G.number_of_edges()

    tolerance = args.tolerance
    print("Start matching process")
    for i in range(len(biotransformer_result_info)):
        print(i)
        this_path_2 = []
        this_path_3 = []
        this_path_4 = []
        biotransform_data = biotransformer_result_info.iloc[i]
        substrate_mass = biotransform_data["substrate_mass"]
        product_mass = biotransform_data["product_mass"]
        substrate_candidate = network_node_info_result[(network_node_info_result["parent mass"]>=substrate_mass-tolerance) & (network_node_info_result["parent mass"]<=substrate_mass+tolerance)]["cluster index"]
        product_candidate = network_node_info_result[(network_node_info_result["parent mass"]>=product_mass-tolerance) & (network_node_info_result["parent mass"]<=product_mass+tolerance)]["cluster index"]
        if len(substrate_candidate)==0 | len(product_candidate)==0:
            continue
        for substrate_item in substrate_candidate:
            for product_item in product_candidate:
                if nx.has_path(G,substrate_item,product_item):
                    if len(nx.shortest_path(G, substrate_item, product_item))<=2:
                        this_path_2.append("-".join([str(s) for s in nx.shortest_path(G, substrate_item, product_item)]))
                    if len(nx.shortest_path(G, substrate_item, product_item))==4:
                        this_path_4.append("-".join([str(s) for s in nx.shortest_path(G, substrate_item, product_item)]))
                    if len(nx.shortest_path(G, substrate_item, product_item))==3:
                        this_path_3.append("-".join([str(s) for s in nx.shortest_path(G, substrate_item, product_item)]))
        if len(this_path_2)!=0:
            result.loc[i,"molecular_path_2"] = "#".join(this_path_2)
        if len(this_path_3)!=0:
            result.loc[i,"molecular_path_3"] = "#".join(this_path_3)
        if len(this_path_4)!=0:
            result.loc[i,"molecular_path_4"] = "#".join(this_path_4)
    result.to_csv(args.output_path,sep = "\t",index = False)
                        



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Build results.')
    parser.add_argument("--Association_BioTransformer_merged_result",
                        help="The path to the input file contain merged Association network and BioTransformer result",
                        default=None)
    
    parser.add_argument("--Molecular_network_edge",
                        help="The path to the molecular netowrk edge info",
                        default=None)

    parser.add_argument("--Molecular_network_node",
                        help="The path to the molecular netowrk node info",
                        default=None)
    parser.add_argument("--tolerance",
                        help="The mass tolerance when matching molecular features",
                        default=0.02)
    parser.add_argument("--output_path",
                        help="The path to the output file",
                        default=None)

    args = parser.parse_args()
    
    run(args)


            

    
    
    
    
    
