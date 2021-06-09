# TransDiscovery
## Short description
This workflow is designed to identify novel biotransformations by intergrating molecular networks (connecting related molecules with similar mass spectra), association networks (connecting co-occurring molecules and microbes) and knowledgebases of microbial enzymes. The identification process is based on the hypothesis that whenever a microbial enzyme biotransforms a substrate molecule to a product, we observe (i) a strong positive correlation between the enzyme/strain and the product, (ii) a strong negative correlation between the enzyme/strain and the substrate, and (iii) an edge in the molecular network between the substrate and the product.
## Main Steps
### preparing input data
#### Association network result
Association network is constructed by calculating pairwise association test between molecular features and microbial features. The association result can be obtained using the pipeline from [AssociationNetworks](https://github.com/mohimanilab/AssociationNetworks/blob/master/README.md). It takes a metabolic feature matrix and a metagenomic feature matrix as input. The output will be the association between each molecular feature and microbial feature with the corresponding correlation value and p-value. 

One vaild association result file is required with following columns:
* `mbx_name`: The name of metablic feature
* `mgx_name`: The name of metagenomic feature
* `correlation`: correlation of the association
* `p_value`: p-value for the association

