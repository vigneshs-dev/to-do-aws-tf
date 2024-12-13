# # Use a stable Node.js image
# FROM node:16

# # Install curl for debugging
# RUN apt-get update && apt-get install -y curl && apt-get clean

# # Set the working directory
# WORKDIR /app

# # Copy package.json and package-lock.json
# COPY package*.json ./

# # Install dependencies
# RUN npm install

# # Copy the application files
# COPY . .

# RUN npm run build
# RUN npm install -g serve
# CMD ["serve", "-s", "build", "-l", "3000"]
# EXPOSE 3000



# Stage 1: Build Stage
FROM node:16-alpine AS builder

# Install build dependencies
RUN apk add --no-cache curl

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the application files
COPY . .

# Build the application
RUN npm run build

# Stage 2: Runtime Stage
FROM node:16-alpine

# Set the working directory
WORKDIR /app

# Install a lightweight HTTP server for serving static files
RUN npm install -g serve

# Copy the build output from the builder stage
COPY --from=builder /app/build ./build

# Serve the application
CMD ["serve", "-s", "build", "-l", "3000"]

# Expose the application port
EXPOSE 3000
