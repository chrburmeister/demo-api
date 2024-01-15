# Don't do this on production workloads, pin a version instead. It does not matter for this api.

FROM node:latest
ENV PORT=8080
WORKDIR /usr/src/app
COPY package.json ./
RUN npm install
COPY . .
USER node
CMD [ "node", "server.js" ]
