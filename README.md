# TransDiscovery
## Short description
This workflow is designed to identify novel biotransformations by intergrating molecular networks (connecting related molecules with similar mass spectra), association networks (connecting co-occurring molecules and microbes) and knowledgebases of microbial enzymes. The identificatino process is based on the hypothesis that whenever a microbial enzyme biotransforms a substrate molecule to a product, we observe (i) a strong positive correlation between the enzyme/strain and the product, (ii) a strong negative correlation between the enzyme/strain and the substrate, and (iii) an edge in the molecular network between the substrate and the product.
## Main Steps
### preparing input data
#### Association network result
The association result can be obtained using the pipeline from [AssociationNetworks](https://github.com/mohimanilab/AssociationNetworks/blob/master/README.md)
