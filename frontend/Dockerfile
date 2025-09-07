FROM node:20-alpine

WORKDIR /app

# Install deps using the lockfile.
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy the rest of the source code.
COPY . .

EXPOSE 3000

# Dev server; Compose overrides it by also passing --host and --port.
CMD ["npm", "run", "dev"]
