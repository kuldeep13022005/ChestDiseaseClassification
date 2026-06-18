FROM python:3.8-slim-buster

# Create a non-root user with UID 1000 for Hugging Face Spaces compatibility
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy application files and set ownership to the 'user'
COPY --chown=user . $HOME/app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Switch to the non-root user
USER user

# Expose the port configured in config and README.md (8080)
EXPOSE 8080

CMD ["python3", "app.py"]