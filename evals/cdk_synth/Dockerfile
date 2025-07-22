FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Unset NODE_OPTIONS to prevent potential interference with the jsii runtime
ENV NODE_OPTIONS=""
# Define Node.js version as an ENV var for easy updates
ENV NODE_VERSION 22.x

# Install system dependencies, Node.js, and the AWS CDK CLI in a single layer.
# Running as root simplifies permissions when dealing with volume mounts from the host.
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash - && \
    apt-get install -y nodejs && \
    npm install -g aws-cdk && \
    npm cache clean --force && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies for AWS CDK and cfn-lint
RUN pip install "aws-cdk-lib>=2.0.0" "constructs>=10.0.0" "cfn-lint"

# Set the working directory
WORKDIR /workspace

# Keep the container running to allow for interactive use (exec).
# The command is executed by the default root user.
CMD ["tail", "-f", "/dev/null"]