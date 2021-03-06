# TransDiscovery
## Short description
This workflow is designed to identify novel biotransformations by integrating molecular networks (connecting related molecules with similar mass spectra), association networks (connecting co-occurring molecules and microbes) and knowledgebases of microbial enzymes. The identification process is based on the hypothesis that whenever a microbial enzyme biotransforms a substrate molecule to a product, we observe (i) a strong positive correlation between the enzyme/strain and the product, (ii) a strong negative correlation between the enzyme/strain and the substrate, and (iii) an edge in the molecular network between the substrate and the product.

## prerequisite

The following packages in python is required to succssfully run TransDiscovery:
* `pandas`
* `numpy`
* `networkx`

## preparing input data
The following data is required to successfully run TransDiscovery
### Association network result
Association network is constructed by calculating pairwise association test between molecular features and microbial features using selected statistical test. The association result can be obtained using the pipeline from [AssociationNetworks](https://github.com/mohimanilab/AssociationNetworks/blob/master/README.md). It takes a metabolic feature matrix and a metagenomic feature matrix as input. The output will be the association between each molecular feature and microbial feature with the corresponding correlation and p-value. 

One vaild association result file is required with at least following columns for the integration process:
* `mbx_name`: The name of molecular feature
* `mgx_name`: The name of microbial feature
* `samples1`: number of the samples the molecular feature is present in
* `samples2`: number of the samples the microbial feature is present in
* `samples_shared`: number of the samples both features are present in
* `correlation`: correlation for the association
* `p_value`: p-value for the association


### Molecular network result
Molecular network is constructed using global natural products social molecular networking ([GNPS](https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp)) infrastructure. First all the MS/MS spectra are clustered by MSCluster and identical spectra are merged into the same clusters and represented as nodes in the network. Then the nodes are matched pairwise using the modification tolerant spectral matching scheme. The output will be the identified nodes and edges between these nodes.

Two valid molecular network result file containing at least following columns is required for the integration process:

In node information file:

* `cluster index`: The cluster index for the node
* `parent mass`: The parent pass for the node

In edge information file:

* `CLUSTERID1`: The cluster index for the first node in an edge
* `CLUSTERID2`: The cluster index for the second node in an edge

### Knowledgebase of microbial enzymes
The knowledgebase of microbial enzymes is created using [BioTransformer](https://bitbucket.org/djoumbou/biotransformerjar/src/master/). The input for the software will be a chemical structure database for molecules and the software will search these structures against the biotransformation database. The output will be the possible biotransformation and pontetional products for each input molecule structure. Please put all these result files into one folder and take the folder path as the input for TransDiscovery. 

One valid summarized biotransformation result file with at least following columns is required for the integration process:
* `Precursor Major Isotope Mass`: The predicted isotope mass for the input structure
* `Major Isotope Mass`: The predicted isotope mass for the potential substrates
* `SMILES`: The predicted smile string for the input structure
* `Reaction`: The predicted biotransformation name for the input structure
* `Enzyme(s)`: The predicted enzyme(s) responsible for the predicted biotransformation

## TransDiscovery pipeline
The TransDiscovery pipeline contains two major steps:
### Integrating Association network with BioTransformer result
This step is designed to identify candidate biotransformations by matching the association network with BioTransformer results. In this step, the input files will be the generated association network and the BioTransformer predicted substrate-product molecules pairs. If (i) a strong positive correlation exists between the enzyme/strain and the identified product, (ii) a strong negative correlation exists between the enzyme/strain and the identified substrate, then the software will output the substrate, product and enzyme/strain as candidate biotransformation. 
### Validating candidate biotransformations using molecular network
This step is designed to validate candidate biotransformations identified in the previous step. In this step, the input files will be the candidate biotransformations obtained in the previous step and molecular network node/edge files generated from GNPS. If an edge/path in the molecular network between the substrate and the product exists, then the software will record such edge/path and consider this biotransformation as identified biotransformation. 

## Running the workflow
User can perform the TransDiscovery workflow with the following parameters:
```
python TransDiscovery.py \
--BioTransformer_result_path sample_input/BioTransformer_sample_input/ \
--Association_result_path sample_input/AssociationNetwork_sample_input.txt \
--Molecular_network_edge_path sample_input/MolecularNetwork_edge_sample_input.txt \
--Molecular_network_node_path sample_input/MolecularNetwork_node_sample_input.txt \
--tolerance 0.02 \
--substrate_rho_value_cutoff 0.1 \
--product_rho_value_cutoff 0.1 \
--neg_sub_pos_prod_only True \
--output_path output.txt
```

Where: 
* `--BioTransformer_result_path`: The path to the BioTransformer result folder
* `--Association_result_path`: The path to the Association network result file
* `--Molecular_network_edge_path`: The path to the molecular network edge info
* `--Molecular_network_node_path`: The path to the molecular network node info
* `--tolerance`: The mass tolerance when matching molecular features
* `--substrate_rho_value_cutoff`: The rho value correlation cutoff for valid association between substrate and enzyme
* `--product_rho_value_cutoff`: The rho value correlation cutoff for valid association between product and enzyme
* `--neg_sub_pos_prod_only`: True if only consider negative correlation for substrate and positive correlation for product
* `--output_path`: The path to the output file

The output file is a TAB-separated table with the first line being the header and every consecutive line describing a candidate biotransformation. The table has the following columns:

* `substrate`: Molecular feature identified as substrate
* `enzyme`: Microbial feature identified as enzyme
* `product`: MOlecular feature identified as product
* `substrate_correlation`: The rho value correlation between the substrate and the enzyme
* `product_correlation`: The rho value correlation between the product and the enzyme
* `p_value_substrate`: The p-value for the correlation between the substrate and the enzyme
* `p_value_product`: The p-value for the correlation between the product and the enzyme
* `substrate_name`: The corresponding molecule name of the substrate in BioTransformer result
* `product_name`: The corresponding molecule name of the product in BioTransformer result
* `reaction_name`: The corresponding reaction name in BioTransformer result
* `enzyme_ID`: The corresponding enzyme_ID of the enzyme in BioTransformer result
* `molecular_path_2`: Any path composed with less than/equal to 2 edges from substrate molecular feature to product molecular feature in molecular network
* `molecular_path_3`: Any path composed with 3 edges from substrate molecular feature to product molecular feature in molecular network
* `molecular_path_4`: Any path composed with 4 edges from substrate molecular feature to product molecular feature in molecular network

## Authors
Donghui Yan, Liu Cao, Hosein Mohimani

Mohimani Lab, CMU, 2021





