FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy environment file first for caching
COPY environment.yml .

# Create environment and activate it
RUN conda env update --file environment.yml --name base && conda clean --all --yes

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "occenv", "/bin/bash", "-c"]

# Copy rest of the app
COPY . .

# Command to run the app
CMD ["conda", "run", "-n", "occenv", "gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
