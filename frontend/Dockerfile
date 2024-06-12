FROM node:14-alpine

# Set the work directory
WORKDIR /frontend

# Copy the package.json and package-lock.json files in the work dir
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the project code to the work dir
COPY . .

# Expose the port
EXPOSE 3000

# Command to execute react
CMD ["npm", "start"]
 