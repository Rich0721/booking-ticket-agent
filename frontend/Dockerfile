# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Accept build arguments
ARG NODE_ENV=production
ARG REACT_APP_BACKEND_URL=http://localhost:8000

# Set environment variables for build
ENV NODE_ENV=${NODE_ENV}
ENV REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code and env files
COPY . .
COPY ../env/.env.prod ./.env

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built application from builder
COPY --from=builder /app/build /usr/share/nginx/html

# Expose port
EXPOSE 80

# Set environment
ENV REACT_APP_ENV=production

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
