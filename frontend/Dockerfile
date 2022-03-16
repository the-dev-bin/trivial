FROM node:14-alpine

WORKDIR /usr/src/app/frontend

ADD package*.json ./

RUN npm install

EXPOSE 4200

CMD ["npm", "start"]