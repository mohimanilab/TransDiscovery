# TransDiscovery
## Short description
This workflow is designed to identify novel biotransformations by intergrating molecular networks (connecting related molecules with similar mass spectra), association networks (connecting co-occurring molecules and microbes) and knowledgebases of microbial enzymes. The identification process is based on the hypothesis that whenever a microbial enzyme biotransforms a substrate molecule to a product, we observe (i) a strong positive correlation between the enzyme/strain and the product, (ii) a strong negative correlation between the enzyme/strain and the substrate, and (iii) an edge in the molecular network between the substrate and the product.
## Main Steps
### preparing input data
The following data is required to successfully run TransDiscovery
#### Association network result
Association network is constructed by calculating pairwise association test between molecular features and microbial features using selected statistical test. The association result can be obtained using the pipeline from [AssociationNetworks](https://github.com/mohimanilab/AssociationNetworks/blob/master/README.md). It takes a metabolic feature matrix and a metagenomic feature matrix as input. The output will be the association between each molecular feature and microbial feature with the corresponding correlation and p-value. 

One vaild association result file is required with at least following columns for the intergration process:
* `mbx_name`: The name of metablic feature
* `mgx_name`: The name of metagenomic feature
* `samples1`: number of the samples the metablic feature is present in
* `samples2`: number of the samples the metagenomic feature is present in
* `samples_shared`: number of the samples both features are present in
* `correlation`: correlation for the association
* `p_value`: p-value for the association


#### Molecular network result
Molecular network is constructed using global natural products social molecular networking ([GNPS](https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp)) infrastructure. First all the MS/MS spectra are clustered by MSCluster and identical spectra are merged into the same clusters and represented as nodes in the network. Then the nodes are matched pairwise using the modification tolerant spectral matching scheme. The output will be the identified nodes and edges between these nodes.

Two valid molecular network result file containing at least following columns is required for the intergration process:

In node information file:

* `cluster index`: The cluster index for the node
* `parent mass`: The parent pass for the node

In edge information file:

* `CLUSTERID1`: The cluster index for the first node in an edge
* `CLUSTERID2`: The cluster index for the second node in an edge

#### Knowledgebases of microbial enzymes
The knowledgebases of microbial enzymes is created using [BioTransformer](https://bitbucket.org/djoumbou/biotransformerjar/src/master/). The input for the software will be a chemical structure database for molecules and the software will search these structures against the biotransformation database. The output will be the possible biotransformation and pontetional products for each input molecule structure. Please put all these result files into one folder and take the folder path as the input for TransDiscovery. 

One valid summarized biotransformation result file with at least following columns is required for the intergration process:
* `Precursor Major Isotope Mass`: The predicted isotope mass for the input structure
* `Major Isotope Mass`: The predicted isotope mass for the potentional substrates
* `SMILES`: The predicted smile string for the input structure
* `Reaction`: The predicted biotransformation name for the input structure
* `Enzyme(s)`: The predicted enzyme(s) responsible for the predicted biotransformation

### TransDiscovery pipeline
The TransDiscovery pipeline contains two major step:
#### Intergrating Association network with BioTransformer result
This step is designed to identify candidate biotransformations by matching the association network with BioTransformer results. In this step the input files will be the generated association network and the BioTransformer predicted substrate-product molecules pairs. If (i) a strong positive correlation exist between the enzyme/strain and the identified product, (ii) a strong negative correlation exist between the enzyme/strain and the identified substrate, then the software will output the substrate, product and enzyme/strain as candidate biotransformation. 

The input parameters are:

* `CLUSTERID1`: The cluster index for the first node in an edge
* `CLUSTERID2`: The cluster index for the second node in an edge





