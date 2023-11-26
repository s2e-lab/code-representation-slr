# Overview
Repository for the following paper: **A Survey of Source Code Representations for Machine Learning-Based Cybersecurity Tasks** by Casey et al 2023.

# Folder Structure

This repository has two folders:

- `analyses`: it has the CSV files with the metadata for the papers we analyzed. 
- `search`: it has the CSV files downloaded from our thee major sources (ACM, IEEE Xplore, and SpringerLink). 


## Folder: search

This folder has the following CSV files:

- `ACM_papers.csv`:
- `IEEE_papers.csv`:
- `SpringerLink_papers.csv`:
- `surveyed_papers.csv`: It contains the basic metadata for the papers we surveyed. This CSV has the columns:
	- `id`: a unique identified that we assigned for the paper. 
	- `title`: paper's title
	- `bibtex_id`: paper's BibTex ID (which you can use to cite it from the file `analyses/srl.bib`)
	- `url`: the URL to access the paper's publication.
	- `doi`: Digital Object Identifier (DOI) 


## Folder: analyses