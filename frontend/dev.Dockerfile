FROM node:lts-alpine3.17

WORKDIR /app
COPY public/ /app/public
COPY src/ /app/src
COPY package.json /app/
COPY package-lock.json /app/
COPY README.md /app/
COPY tailwind.config.js /app/

RUN npm install


CMD ["npm", "start"]