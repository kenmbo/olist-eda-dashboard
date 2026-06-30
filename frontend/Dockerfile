# ==========================================
# STAGE 1: Build the React application
# ==========================================
FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
# Copy the frontend code
COPY . .

# Build the project (Vite will output files to the /dist folder)
RUN npm run build

# ==========================================
# STAGE 2: Serve the app with Nginx
# ==========================================
FROM nginx:alpine
# Remove the default Nginx index page
RUN rm -rf /usr/share/nginx/html/*
# Copy the compiled static files from the 'builder' stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy a custom Nginx config (Required if using React Router for multiple pages)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (the default HTTP port)
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
