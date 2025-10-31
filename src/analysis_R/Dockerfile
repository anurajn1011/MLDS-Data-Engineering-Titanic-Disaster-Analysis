FROM rocker/tidyverse

WORKDIR /code

COPY . .

RUN Rscript src/analysis_R/install_packages.R

CMD ["Rscript", "src/analysis_R/analysis.R"]